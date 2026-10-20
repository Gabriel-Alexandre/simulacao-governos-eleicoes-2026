"""Gera docs/FONTES.md a partir de dados/MANIFESTO.csv, com o tipo de cada fonte e a linha editorial usada no teste das duas pontas."""
import csv
from pathlib import Path
from urllib.parse import urlparse

RAIZ = Path(__file__).resolve().parents[1]
OFICIAL = ("planalto.gov.br", "senado.leg.br", "camara.leg.br", "stf.jus.br", "gov.br", "ibge.gov.br", "bcb.gov.br", "tse.jus.br", "inep.gov.br", "agenciabrasil.ebc.com.br", "ifi")
ACADEMICO = ("scielo", "repec", "ipea.gov.br", "berkeley.edu", "aeaweb.org", "fiocruz.br", "ufc.br", "ufu.br", "ufjf.br", "uem.br", "unisinos.br")
ORGANISMO = ("worldbank.org", "imf.org", "forumseguranca.org.br", "transparenciainternacional.org.br", "poder360.com.br/2019/09/forumseguranca", "conass.org.br", "observatoriodasmetropoles")
ESQUERDA = ("brasildefato.com.br", "cartacapital.com.br", "vermelho.org.br", "ocafezinho.com", "cut.org.br", "fpabramo.org.br")
DIREITA = ("gazetadopovo.com.br", "revistaoeste.com", "jovempan.com.br")
PLANOS = ("plano-flavio.pdf", "Programa-Governo-LULA-2026.pdf")


def tipo(url):
    h = urlparse(url).netloc + urlparse(url).path
    if any(p in url for p in PLANOS):
        return "plano registrado", ""
    if any(d in h for d in ESQUERDA):
        return "imprensa", "esquerda (declarada ou por filiação)"
    if any(d in h for d in DIREITA):
        return "imprensa", "direita (declarada ou por cobertura)"
    if any(d in h for d in OFICIAL):
        return "oficial", ""
    if any(d in h for d in ACADEMICO):
        return "acadêmica", ""
    if any(d in h for d in ORGANISMO) or "anuario" in url.lower():
        return "organismo técnico ou internacional", ""
    if "finance.yahoo" in h:
        return "dado de mercado", ""
    return "imprensa", "geral"


def main():
    linhas = list(csv.DictReader((RAIZ / "dados" / "MANIFESTO.csv").open(encoding="utf-8")))
    out = ["# Fontes", "", "Gerado por `ferramentas/listar-fontes.py` a partir de `dados/MANIFESTO.csv` (url, data, tamanho e sha256 de cada arquivo baixado). O texto extraído de cada página está em `dados/capturas/<id>.txt`; HTML e PDF brutos ficam fora do git e se baixam de novo pelo `docs/REPLICAR.md`.", "",
           f"**{len(linhas)} fontes.** A linha editorial só é marcada para o teste das duas pontas (`docs/TESTE_DAS_DUAS_PONTAS.md`).", "",
           "| id | tipo | linha editorial | capturado em | url |", "|---|---|---|---|---|"]
    for l in linhas:
        t, lin = tipo(l["url"])
        out.append(f"| `{l['id']}` | {t} | {lin} | {l['capturado_em']} | {l['url']} |")
    (RAIZ / "docs" / "FONTES.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(len(linhas), "fontes")


if __name__ == "__main__":
    main()
