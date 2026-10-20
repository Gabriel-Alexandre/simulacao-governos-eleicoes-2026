"""Testes de integridade: cada regra do pré-registro que pode ser checada por máquina."""
import csv
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
R = json.loads((RAIZ / "resultados" / "RESUMO.json").read_text(encoding="utf-8"))
S = json.loads((RAIZ / "resultados" / "SIMULACAO_DIVIDA.json").read_text(encoding="utf-8"))


def rodar(script):
    return subprocess.run([sys.executable, str(RAIZ / "ferramentas" / script)], capture_output=True, text=True, encoding="utf-8")


def test_trechos_conferidos():
    assert rodar("conferir-trechos.py").returncode == 0


def test_linguagem():
    assert rodar("conferir-linguagem.py").returncode == 0


def test_seis_temas_e_veredito_pela_regra():
    assert set(R["temas"]) == {"seguranca", "saude", "economia", "corrupcao", "educacao", "pobreza"}
    for t, v in R["temas"].items():
        p = v["pesos"]["principal"]
        esperado = "empate" if abs(p["lula"] - p["flavio"]) < 5 else ("Lula" if p["lula"] > p["flavio"] else "Flávio")
        assert v["veredito"] == esperado, t


def test_nenhuma_soma_de_temas():
    assert "placar_geral" not in R and "total" not in json.dumps(R["temas"]).lower()


def test_toda_proposta_tem_nota_e_evidencia_ou_motivo():
    notas = {l["id"]: l for l in csv.DictReader((RAIZ / "dados/evidencias/NOTAS_PROPOSTAS.csv").open(encoding="utf-8"))}
    sel = [l for l in csv.DictReader((RAIZ / "dados/evidencias/PROPOSTAS_SELECAO.csv").open(encoding="utf-8")) if not l["id"].endswith("-sem")]
    assert len(sel) == 46
    for l in sel:
        n = notas[l["id"]]
        assert n["c3_motivo"] and n["c4_motivo"] and n["c5_motivo"]
        assert float(n["c3_nota"]) in (100, 80, 60, 35, 25, 10, 0)
        assert float(n["c4_nota"]) in (100, 65, 35, 0)
        assert float(n["c5_nota"]) in (100, 50, 0)


def test_evidencias_citadas_existem():
    ids = {l["id"] for l in csv.DictReader((RAIZ / "dados/evidencias/EVIDENCIAS.csv").open(encoding="utf-8"))}
    for l in csv.DictReader((RAIZ / "dados/evidencias/NOTAS_PROPOSTAS.csv").open(encoding="utf-8")):
        for campo in ("c3_evid", "c4_evid"):
            for e in filter(None, l[campo].split(";")):
                assert e in ids, (l["id"], e)


def test_simulacao_reproduz_a_base_da_ifi():
    assert S["conferencia_base_reproduzida"] is True


def test_c2_pela_regra():
    assert abs(R["c2_informativo"]["lula"] - (26 + 2) / 36 * 100) < 0.01
    assert abs(R["c2_informativo"]["flavio"] - (19 + 5) / 58 * 100) < 0.01


def test_rodada2_c2_fora_e_base_comum_fora_da_media():
    for t, v in R["temas"].items():
        assert "C2" not in v["criterios"]["lula"]
    notas = {l["id"]: l for l in csv.DictReader((RAIZ / "dados/evidencias/NOTAS_RODADA2.csv").open(encoding="utf-8"))}
    assert len(notas) == 46
    for i, n in notas.items():
        if n["tipo"] == "base":
            assert n["c3_nota"] == "" and n["c4_nota"] == ""
        else:
            assert float(n["c3_nota"]) in (100, 80, 60, 35, 25, 10, 0)


def test_rodada2_mesmo_programa_mesma_nota():
    notas = {l["id"]: l for l in csv.DictReader((RAIZ / "dados/evidencias/NOTAS_RODADA2.csv").open(encoding="utf-8"))}
    assert notas["L-H-c"]["c3_nota"] == notas["F-H-c"]["c3_nota"] and notas["L-H-c"]["c4_nota"] == notas["F-H-c"]["c4_nota"]


def test_rodada2_segurança_tem_14_crimes():
    assert sum(1 for l in R["c1_indicadores"] if l["tema"] == "seguranca") == 14
