"""Baixa as séries numéricas do C1 (histórico) e do C6 (mercado) para dados/series/.

Cada arquivo bruto ganha uma linha em dados/MANIFESTO.csv (url, data, bytes, sha256).
Uso: python ferramentas/coletar-series.py [nome ...]   (sem nome, baixa tudo)
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import sys
import time
from pathlib import Path

import requests

RAIZ = Path(__file__).resolve().parents[1]
SERIES = RAIZ / "dados" / "series"
MANIFESTO = RAIZ / "dados" / "MANIFESTO.csv"
CAMPOS = ["id", "url", "tipo", "capturado_em", "bytes", "sha256", "arquivo_bruto", "arquivo_texto"]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/129.0"}

WB = "https://api.worldbank.org/v2/country/BRA;LCN;WLD/indicator/{ind}?format=json&date=1995:2026&per_page=500"
IMF = "https://www.imf.org/external/datamapper/api/v1/{ind}/BRA/OEMDC/WE"
BCB = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{n}/dados?formato=json&dataInicial={ini}&dataFinal={fim}"
SIDRA = "https://apisidra.ibge.gov.br/values/{caminho}"
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/{sim}?period1={p1}&period2={p2}&interval=1d"

P1 = int(dt.datetime(2025, 7, 1).timestamp())
P2 = int(dt.datetime(2026, 10, 21).timestamp())

FONTES: dict[str, str] = {
    # FMI WEO: Brasil, emergentes (OEMDC) e Hemisfério Ocidental (WE)
    "imf-pib": IMF.format(ind="NGDP_RPCH"),
    "imf-inflacao": IMF.format(ind="PCPIPCH"),
    # Banco Mundial: Brasil, América Latina e Caribe (LCN), mundo (WLD)
    "wb-esperanca-vida": WB.format(ind="SP.DYN.LE00.IN"),
    "wb-mortalidade-infantil": WB.format(ind="SP.DYN.IMRT.IN"),
    "wb-vacina-sarampo": WB.format(ind="SH.IMM.MEAS"),
    "wb-controle-corrupcao-percentil": WB.format(ind="CC.PER.RNK"),
    "wb-gini": WB.format(ind="SI.POV.GINI"),
    "wb-pobreza-3dolares": WB.format(ind="SI.POV.DDAY"),
    "wb-subalimentacao": WB.format(ind="SN.ITK.DEFC.ZS"),
    "wb-pib-crescimento": WB.format(ind="NY.GDP.MKTP.KD.ZG"),
    "wb-wgi-controle-corrupcao": "https://api.worldbank.org/v2/country/BRA;LCN;WLD/indicator/GOV_WGI_CC.SC?source=3&format=json&date=1996:2026&per_page=500",
    # Banco Central (SGS)
    "bcb-divida-bruta": BCB.format(n=13762, ini="01/01/2006", fim="31/12/2026"),
    "bcb-ipca-mensal": BCB.format(n=433, ini="01/01/2002", fim="31/12/2026"),
    "bcb-desemprego-pnad": BCB.format(n=24369, ini="01/01/2012", fim="31/12/2026"),
    "bcb-dolar-ptax": BCB.format(n=1, ini="01/07/2025", fim="20/10/2026"),
    # IBGE (SIDRA)
    "ibge-desocupacao": SIDRA.format(caminho="t/6381/n1/all/v/4099/p/all"),
    "ibge-rendimento-real": SIDRA.format(caminho="t/6390/n1/all/v/5933/p/all"),
    "ibge-gini": SIDRA.format(caminho="t/7435/n1/all/v/10681/p/all"),
    "ibge-pib-anual": SIDRA.format(caminho="t/6784/n1/all/v/9810/p/all"),
    # Mercado (Yahoo Finance, fechamento diário)
    "mkt-ibovespa": YAHOO.format(sim="%5EBVSP", p1=P1, p2=P2),
    "mkt-eem": YAHOO.format(sim="EEM", p1=P1, p2=P2),
    "mkt-ewz": YAHOO.format(sim="EWZ", p1=P1, p2=P2),
    "mkt-usdbrl": YAHOO.format(sim="BRL%3DX", p1=P1, p2=P2),
    "mkt-usdmxn": YAHOO.format(sim="MXN%3DX", p1=P1, p2=P2),
    "mkt-usdzar": YAHOO.format(sim="ZAR%3DX", p1=P1, p2=P2),
    "mkt-usdclp": YAHOO.format(sim="CLP%3DX", p1=P1, p2=P2),
    "mkt-usdcop": YAHOO.format(sim="COP%3DX", p1=P1, p2=P2),
}


def ler_manifesto() -> list[dict]:
    if not MANIFESTO.exists():
        return []
    with MANIFESTO.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def gravar_manifesto(linhas: list[dict]) -> None:
    with MANIFESTO.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        for l in sorted(linhas, key=lambda x: x["id"]):
            w.writerow(l)


def baixar(nome: str, url: str) -> None:
    for tentativa in range(4):
        try:
            r = requests.get(url, headers={} if "imf.org" in url else UA, timeout=180)
            r.raise_for_status()
            json.loads(r.content)  # só aceita JSON válido
            break
        except Exception as e:  # noqa: BLE001
            print(f"{nome}: tentativa {tentativa + 1} falhou ({e})", file=sys.stderr)
            time.sleep(5 * (tentativa + 1))
    else:
        print(f"{nome}: NÃO BAIXOU", file=sys.stderr)
        return
    SERIES.mkdir(parents=True, exist_ok=True)
    alvo = SERIES / f"{nome}.json"
    alvo.write_bytes(r.content)
    linhas = [l for l in ler_manifesto() if l["id"] != f"serie-{nome}"]
    linhas.append({
        "id": f"serie-{nome}", "url": url, "tipo": "json",
        "capturado_em": dt.date.today().isoformat(), "bytes": len(r.content),
        "sha256": hashlib.sha256(r.content).hexdigest(),
        "arquivo_bruto": alvo.relative_to(RAIZ).as_posix(), "arquivo_texto": "",
    })
    gravar_manifesto(linhas)
    print(f"{nome}: {len(r.content)} bytes")


if __name__ == "__main__":
    nomes = sys.argv[1:] or list(FONTES)
    for n in nomes:
        baixar(n, FONTES[n])
