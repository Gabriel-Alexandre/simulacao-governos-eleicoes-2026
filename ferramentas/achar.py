"""Mostra trechos de uma captura que casam com uma expressão (para copiar o trecho exato).
Uso: python ferramentas/achar.py <id-prefixo> <regex> [largura]"""
import re, sys
from pathlib import Path
raiz = Path(__file__).resolve().parents[1] / "dados" / "capturas"
pref, padrao = sys.argv[1], sys.argv[2]
larg = int(sys.argv[3]) if len(sys.argv) > 3 else 220
for f in sorted(raiz.glob(pref + "*.txt")):
    t = " ".join(f.read_text(encoding="utf-8").split())
    for m in list(re.finditer(padrao, t, re.I))[:6]:
        print(f"[{f.stem}] ...{t[max(0, m.start()-larg):m.end()+larg]}...\n")
