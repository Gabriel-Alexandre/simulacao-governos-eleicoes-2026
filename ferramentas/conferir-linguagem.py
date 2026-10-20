"""Confere o texto público: palavras proibidas da doutrina, travessão e soma de temas."""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ARQUIVOS = ["README.md", "RELATORIO.md", "RESUMO_SIMPLES.md", "docs/LEITURA_DA_IA.md", "docs/REVISAO_ADVERSARIAL.md", "docs/TESTE_DAS_DUAS_PONTAS.md", "docs/LIMITE_ELEITORAL.md"]
PROIBIDAS = [r"\bfraude\b(?! eletrônica| em benefício)", r"\bmentiu\b", r"\bmentira\b", r"\bcorrupto\b", r"\bculpado\b", r"\bgolpe\b", r"\bdesastre\b", r"\bcatástrofe\b",
             r"\bmassacre\b", r"\bgenocida\b", r"\bladrão\b", r"\bcomunista\b", r"\bfascista\b", r"venceu o debate", r"ganhou a eleição", r"melhor candidato"]
SOMA = [r"\b\d+ (de|dos) (6|seis) temas\b", r"\bem (cinco|5|quatro|4) (dos|de) (seis|6)\b", r"placar geral (é|de)"]


def main():
    erros = 0
    for a in ARQUIVOS:
        p = RAIZ / a
        if not p.exists():
            continue
        for n, linha in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if "—" in linha:
                print(f"{a}:{n}: travessão"); erros += 1
            for pad in PROIBIDAS + SOMA:
                if re.search(pad, linha, re.I) and "⛔" not in linha and "Palavras" not in linha:
                    print(f"{a}:{n}: '{pad}' -> {linha[:120]}"); erros += 1
    print(f"{erros} problemas de linguagem")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
