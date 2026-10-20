"""Confere que cada trecho citado existe, de fato, no texto capturado da fonte.

Lê dados/evidencias/EVIDENCIAS.csv, VALORES_DOCUMENTOS.csv e PROPOSTAS_SELECAO.csv.
Para cada linha, procura o padrão (texto literal, sem diferença de espaço e de maiúscula)
na captura dados/capturas/<fonte>.txt e grava o trecho encontrado, com contexto, em
resultados/TRECHOS_CONFERIDOS.csv. Sai com erro se algum trecho não for encontrado.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CAPTURAS = RAIZ / "dados" / "capturas"
SAIDA = RAIZ / "resultados" / "TRECHOS_CONFERIDOS.csv"


def normalizar(t: str) -> str:
    return " ".join(t.split()).casefold()


_cache: dict[str, tuple[str, str]] = {}


def texto(fonte: str) -> tuple[str, str]:
    if fonte not in _cache:
        arq = CAPTURAS / f"{fonte}.txt"
        bruto = " ".join(arq.read_text(encoding="utf-8").split())
        _cache[fonte] = (bruto, bruto.casefold())
    return _cache[fonte]


def conferir(arquivo: str, campo_id: str, campo_fonte: str, campo_padrao: str, fonte_fixa: dict | None = None):
    linhas = list(csv.DictReader((RAIZ / "dados" / "evidencias" / arquivo).open(encoding="utf-8")))
    resultado, falhas = [], []
    for l in linhas:
        if fonte_fixa:
            fonte = fonte_fixa.get(l["lado"])
            if not l.get("pagina_plano"):
                continue
        else:
            fonte = l[campo_fonte]
        padrao = normalizar(l[campo_padrao])
        try:
            bruto, low = texto(fonte)
        except FileNotFoundError:
            falhas.append((l[campo_id], fonte, "captura inexistente"))
            continue
        i = low.find(padrao)
        if i < 0:
            falhas.append((l[campo_id], fonte, l[campo_padrao]))
            continue
        trecho = bruto[max(0, i - 120): i + len(padrao) + 120]
        resultado.append({"arquivo": arquivo, "id": l[campo_id], "fonte": fonte, "padrao": l[campo_padrao], "trecho_com_contexto": trecho})
    return resultado, falhas


def main() -> int:
    todos, falhas = [], []
    for args in [
        ("EVIDENCIAS.csv", "id", "fonte", "padrao", None),
        ("VALORES_DOCUMENTOS.csv", "indicador", "fonte", "padrao", None),
        ("PROPOSTAS_SELECAO.csv", "id", "", "trecho_do_plano", {"lula": "G02-plano-lula", "flavio": "G01-plano-flavio"}),
    ]:
        r, f = conferir(*args)
        todos += r
        falhas += f
    SAIDA.parent.mkdir(exist_ok=True)
    with SAIDA.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["arquivo", "id", "fonte", "padrao", "trecho_com_contexto"])
        w.writeheader()
        w.writerows(todos)
    for f in falhas:
        print("NÃO ENCONTRADO:", f)
    print(f"{len(todos)} trechos conferidos, {len(falhas)} falhas")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
