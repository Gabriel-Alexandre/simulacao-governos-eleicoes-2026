"""Rodada 2 (emendas 6 a 11, escritas e publicadas antes destas notas): grava resultados/RESUMO.json.

Mudanças em relação à rodada 1 (resultados/rodada1/):
- C2 sai da nota do tema (vira informação geral);
- C3, C4 e C5 medem só o que cada um muda; manter o que existe é base comum;
- o mesmo programa tem o mesmo degrau dos dois lados;
- segurança com os 14 crimes que o Anuário publica igual em 2018, 2022 e 2025;
- mais indicadores, desemprego contra a América Latina e Ideb na janela sem pandemia;
- C7: obras federais paralisadas (painel do TCU);
- tabela de contexto de cada mandato (herança e choques).
"""
from __future__ import annotations

import csv
import datetime as dt
import importlib.util
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("r1", RAIZ / "ferramentas" / "calcular.py")
r1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r1)

LADOS, TEMAS, NOME_TEMA = r1.LADOS, r1.TEMAS, r1.NOME_TEMA
EVID = RAIZ / "dados" / "evidencias"
SAIDA = RAIZ / "resultados"

PESOS = {
    "principal": {
        "com_obras": {"C1": 25, "C3": 30, "C4": 20, "C5": 10, "C7": 15},
        "sem_obras": {"C1": 25, "C3": 30, "C4": 20, "C5": 10},
        "economia": {"C1": 20, "C3": 25, "C4": 20, "C5": 10, "C6": 15, "C7": 10},
    },
    "iguais": {
        "com_obras": {"C1": 20, "C3": 20, "C4": 20, "C5": 20, "C7": 20},
        "sem_obras": {"C1": 25, "C3": 25, "C4": 25, "C5": 25},
        "economia": {"C1": 100 / 6, "C3": 100 / 6, "C4": 100 / 6, "C5": 100 / 6, "C6": 100 / 6, "C7": 100 / 6},
    },
    "historico_pesa_mais": {
        "com_obras": {"C1": 40, "C3": 20, "C4": 10, "C5": 10, "C7": 20},
        "sem_obras": {"C1": 50, "C3": 25, "C4": 15, "C5": 10},
        "economia": {"C1": 40, "C3": 10, "C4": 10, "C5": 10, "C6": 15, "C7": 15},
    },
    "execucao_pesa_mais": {
        "com_obras": {"C1": 15, "C3": 45, "C4": 15, "C5": 10, "C7": 15},
        "sem_obras": {"C1": 15, "C3": 50, "C4": 25, "C5": 10},
        "economia": {"C1": 15, "C3": 35, "C4": 15, "C5": 5, "C6": 15, "C7": 15},
    },
}
COM_OBRAS = {"saude", "educacao", "pobreza"}


def documentos():
    out = {}
    for l in csv.DictReader((EVID / "VALORES_DOCUMENTOS.csv").open(encoding="utf-8")):
        if l["uso"] in ("principal", "rodada2", "informativo"):
            try:
                out.setdefault(l["indicador"], {})[int(l["ano"])] = float(l["valor"])
            except ValueError:
                pass
    return out


def linha(tema, rot, b, l, melhor, dmin, fonte, nota=""):
    pl, pf = r1.comparar(b, l, melhor, dmin)
    return {"tema": tema, "indicador": rot, "bolsonaro_2019_2022": round(b, 4), "lula_2023_atual": round(l, 4),
            "melhor": melhor, "diferenca_minima": dmin, "pontos_lula": pl, "pontos_flavio": pf, "fonte": fonte, "nota": nota}


CRIMES = [
    ("mvi_casos", "Mortes violentas intencionais"), ("homicidio_doloso", "Homicídio doloso"), ("latrocinio", "Latrocínio"),
    ("feminicidio", "Feminicídio"), ("estupro_total", "Estupro e estupro de vulnerável"), ("tentativa_homicidio", "Tentativa de homicídio"),
    ("lesao_corporal_dolosa", "Lesão corporal dolosa"), ("roubo_veiculo", "Roubo de veículo"), ("furto_veiculo", "Furto de veículo"),
    ("roubo_transeunte", "Roubo a transeunte"), ("roubo_residencia", "Roubo a residência"), ("roubo_comercio", "Roubo a estabelecimento comercial"),
    ("roubo_carga", "Roubo de carga"), ("estelionato_registros", "Estelionato"),
]


def indicadores_c1():
    doc = documentos()
    out = []
    # --- economia
    pib = r1.imf("NGDP_RPCH", "imf-pib"); inf = r1.imf("PCPIPCH", "imf-inflacao")
    dpib = {a: pib["BRA"][a] - pib["OEMDC"][a] for a in pib["BRA"] if a in pib["OEMDC"]}
    dinf = {a: inf["BRA"][a] - inf["OEMDC"][a] for a in inf["BRA"] if a in inf["OEMDC"]}
    out.append(linha("economia", "PIB real, Brasil menos emergentes (p.p. ao ano, média)", r1.media(dpib, [2019, 2020, 2021, 2022]), r1.media(dpib, [2023, 2024, 2025]), "maior", 0.3, "FMI"))
    out.append(linha("economia", "Inflação, Brasil menos emergentes (p.p. ao ano, média)", r1.media(dinf, [2019, 2020, 2021, 2022]), r1.media(dinf, [2023, 2024, 2025]), "menor", 0.5, "FMI"))
    des = r1.wb("wb-desemprego-oit")
    rd = {a: des["BRA"][a] - des["LCN"][a] for a in des["BRA"] if a in des["LCN"]}
    out.append(linha("economia", "Desemprego, Brasil menos América Latina, variação ao ano (p.p.)", r1.por_ano(rd[2018], rd[2022], 4), r1.por_ano(rd[2022], rd[2025], 3), "menor", 0.2, "Banco Mundial (OIT)"))
    div = r1.bcb("bcb-divida-bruta"); ult = max(div)
    out.append(linha("economia", f"Dívida bruta, variação ao ano (p.p. do PIB; até {ult:%m/%Y})", r1.por_ano(div[dt.date(2018, 12, 1)], div[dt.date(2022, 12, 1)], 4),
                     r1.por_ano(div[dt.date(2022, 12, 1)], div[ult], r1.anos_fracao(f"{ult:%Y%m}")), "menor", 0.5, "Banco Central"))
    ren = r1.sidra("ibge-rendimento-real"); ur = max(ren)
    out.append(linha("economia", "Rendimento médio real do trabalho, variação ao ano (%)", r1.cagr(ren["201812"], ren["202212"], 4), r1.cagr(ren["202212"], ren[ur], r1.anos_fracao(ur)), "maior", 0.5, "IBGE"))
    # --- segurança: 14 crimes, taxa composta de variação dos casos
    for chave, rot in CRIMES:
        s = doc[chave]
        out.append(linha("seguranca", f"{rot}, variação ao ano dos casos (%)", r1.cagr(s[2018], s[2022], 4), r1.cagr(s[2022], s[2025], 3), "menor", 2.0, "Anuários FBSP 2019, 2023 e 2026"))
    # --- saúde: contra a América Latina
    for nome, rot, melhor, dmin, ult_l in [("wb-esperanca-vida", "Esperança de vida", "maior", 0.1, 2024), ("wb-mortalidade-infantil", "Mortalidade infantil", "menor", 0.1, 2024),
                                           ("wb-vacina-sarampo", "Vacina de sarampo", "maior", 1.0, 2024), ("wb-vacina-dtp3", "Vacina tríplice bacteriana (DTP3)", "maior", 1.0, 2024),
                                           ("wb-mortalidade-materna", "Mortalidade materna", "menor", 2.0, 2023)]:
        s = r1.wb(nome)
        r = {a: s["BRA"][a] - s["LCN"][a] for a in s["BRA"] if a in s.get("LCN", {})}
        out.append(linha("saude", f"{rot}, Brasil menos América Latina, variação ao ano", r1.por_ano(r[2018], r[2022], 4), r1.por_ano(r[2022], r[ult_l], ult_l - 2022), melhor, dmin, "Banco Mundial (OMS, ONU)"))
    # --- educação: janela sem pandemia (2017 a 2019 contra 2023 a 2025)
    for chave, rot in [("ideb_iniciais", "Ideb dos anos iniciais"), ("ideb_finais", "Ideb dos anos finais"), ("ideb_medio", "Ideb do ensino médio")]:
        s = doc[chave]
        out.append(linha("educacao", f"{rot}, variação por edição (sem pandemia)", s[2019] - s[2017], s[2025] - s[2023], "maior", 0.1, "Inep"))
    # --- corrupção
    ipc, mm = doc["ipc_brasil"], doc["ipc_media_mundial"]
    r = {a: ipc[a] - mm[a] for a in ipc if a in mm}
    out.append(linha("corrupcao", "Percepção da Corrupção, Brasil menos média mundial, variação ao ano", r1.por_ano(r[2018], r[2022], 4), r1.por_ano(r[2022], r[2025], 3), "maior", 1.0, "Transparência Internacional"))
    w = r1.wb("wb-wgi-controle-corrupcao")["BRA"]
    out.append(linha("corrupcao", "Controle da Corrupção (Banco Mundial, 0 a 100), variação ao ano", r1.por_ano(w[2018], w[2022], 4), r1.por_ano(w[2022], w[2025], 3), "maior", 3.0, "Banco Mundial"))
    # --- pobreza
    for nome, rot, dmin in [("wb-pobreza-3dolares", "Extrema pobreza (US$ 3 por dia)", 0.2), ("wb-pobreza-8dolares", "Pobreza (US$ 8,30 por dia)", 0.5)]:
        s = r1.wb(nome)["BRA"]
        out.append(linha("pobreza", f"{rot}, variação ao ano (p.p.)", r1.por_ano(s[2018], s[2022], 4), r1.por_ano(s[2022], s[2024], 2), "menor", dmin, "Banco Mundial sobre a PNAD"))
    gini = {int(k): v for k, v in r1.sidra("ibge-gini").items()}
    out.append(linha("pobreza", "Gini do rendimento domiciliar per capita, variação ao ano", r1.por_ano(gini[2018], gini[2022], 4), r1.por_ano(gini[2022], gini[2025], 3), "menor", 0.003, "IBGE"))
    fao = r1.wb("wb-subalimentacao")["BRA"]
    out.append(linha("pobreza", "Subalimentação (FAO, média de 3 anos), variação ao ano (p.p.)", r1.por_ano(fao[2018], fao[2022], 4), r1.por_ano(fao[2022], fao[2024], 2), "menor", 0.5, "FAO"))
    return out


def c7():
    doc = documentos()
    par, tot = doc["obras_paralisadas_n"], doc["obras_total_n"]
    pct = {a: par[a] / tot[a] * 100 for a in par if a in tot}
    b = (pct[2022] - pct[2018]) / 4
    l = (pct[2025] - pct[2022]) / (2025 + 4 / 12 - (2022 + 8 / 12))
    pl, pf = r1.comparar(b, l, "menor", 1.0)
    return {"pct": {a: round(v, 2) for a, v in pct.items()}, "bolsonaro_pp_ao_ano": round(b, 2), "lula_pp_ao_ano": round(l, 2),
            "nota": {"lula": pl * 50, "flavio": pf * 50},
            "ressalva": "A base de 2018 é o diagnóstico do TCU (contratos), a de 2022 e 2025 é o painel; em 2026 o TCU trocou a carteira (4.215 de 22.414 paralisadas), e não dá para comparar com 2025."}


def propostas_r2():
    sel = {l["id"]: l for l in csv.DictReader((EVID / "PROPOSTAS_SELECAO.csv").open(encoding="utf-8"))}
    r2 = {l["id"]: l for l in csv.DictReader((EVID / "NOTAS_RODADA2.csv").open(encoding="utf-8"))}
    out = []
    for pid, s in sel.items():
        if pid.endswith("-sem"):
            continue
        n = r2[pid]
        d = {**s, "tipo": n["tipo"], "motivo_rodada2": n["motivo_rodada2"]}
        if n["tipo"] == "mudanca":
            d.update(c3_nota=float(n["c3_nota"]), c4_nota=float(n["c4_nota"]), c5_nota=float(n["c5_nota"]))
        out.append(d)
    return out


def notas(c1_lin, props, c6v, c7v, pesos=None):
    pesos = pesos or PESOS
    out = {}
    for tema in TEMAS:
        crit = {lado: {} for lado in LADOS}
        ind = [l for l in c1_lin if l["tema"] == tema]
        for lado in LADOS:
            crit[lado]["C1"] = sum(l[f"pontos_{lado}"] for l in ind) / len(ind) * 50
            ps = [p for p in props if p["tema"] == tema and p["lado"] == lado and p["tipo"] == "mudanca"]
            for c in ("c3", "c4", "c5"):
                crit[lado][c.upper()] = sum(p[f"{c}_nota"] for p in ps) / len(ps)
            crit[lado]["C6"] = c6v["nota"][lado] if tema == "economia" else None
            crit[lado]["C7"] = c7v["nota"][lado] if (tema in COM_OBRAS or tema == "economia") else None
        grupo = "economia" if tema == "economia" else ("com_obras" if tema in COM_OBRAS else "sem_obras")
        cen = {}
        for nome, p in pesos.items():
            pw = p[grupo]
            tot = {lado: sum(crit[lado][c] * pw[c] for c in pw) / sum(pw.values()) for lado in LADOS}
            dif = tot["lula"] - tot["flavio"]
            cen[nome] = {"lula": round(tot["lula"], 1), "flavio": round(tot["flavio"], 1), "diferenca": round(dif, 1),
                         "veredito": "empate" if abs(dif) < 5 else ("Lula" if dif > 0 else "Flávio"),
                         "contribuicoes": {c: round(pw[c] * (crit["lula"][c] - crit["flavio"][c]) / sum(pw.values()), 1) for c in pw}}
        vers = {c["veredito"] for c in cen.values()}
        out[tema] = {"nome": NOME_TEMA[tema], "grupo_de_pesos": grupo,
                     "criterios": {lado: {k: (round(v, 1) if v is not None else None) for k, v in crit[lado].items()} for lado in LADOS},
                     "pesos": cen, "veredito": cen[next(iter(cen))]["veredito"], "robustez": "firme" if len(vers) == 1 else "depende do peso"}
    return out


def contexto():
    selic = {dt.datetime.strptime(x["data"], "%d/%m/%Y").date(): float(x["valor"]) for x in json.loads((RAIZ / "dados/series/bcb-selic-meta.json").read_text())}
    des = r1.sidra("ibge-desocupacao")
    div = r1.bcb("bcb-divida-bruta")
    ipca = {}
    for d, v in r1.bcb("bcb-ipca-mensal").items():
        ipca.setdefault(d.year, 1.0); ipca[d.year] *= 1 + v / 100
    pib = r1.imf("NGDP_RPCH", "imf-pib")
    em = lambda anos: round(sum(pib["OEMDC"][a] for a in anos) / len(anos), 2)
    return {
        "bolsonaro": {"selic_no_inicio": selic[dt.date(2018, 12, 31)], "desemprego_no_inicio": des["201812"], "divida_no_inicio": div[dt.date(2018, 12, 1)],
                      "ipca_do_ano_anterior": round((ipca[2018] - 1) * 100, 2), "crescimento_medio_emergentes": em([2019, 2020, 2021, 2022]),
                      "choques": "pandemia (2020 e 2021) e início da guerra na Ucrânia (2022)"},
        "lula_atual": {"selic_no_inicio": selic[dt.date(2022, 12, 30)], "desemprego_no_inicio": des["202212"], "divida_no_inicio": div[dt.date(2022, 12, 1)],
                       "ipca_do_ano_anterior": round((ipca[2022] - 1) * 100, 2), "crescimento_medio_emergentes": em([2023, 2024, 2025]),
                       "choques": "tarifas dos Estados Unidos (2025), enchentes no Rio Grande do Sul (2024) e guerra no Irã (citada no plano de Lula)"},
        "fontes": ["Banco Central (SGS 432, 13762, 433)", "IBGE (SIDRA 6381)", "FMI (emergentes)"],
    }


def main():
    c1_lin = indicadores_c1()
    props = propostas_r2()
    c6v = r1.c6()
    c7v = c7()
    temas = notas(c1_lin, props, c6v, c7v)
    rod1 = json.loads((SAIDA / "rodada1" / "RESUMO.json").read_text(encoding="utf-8"))
    # sensibilidades
    c1_com_pandemia = [dict(l) for l in c1_lin]
    doc = documentos()
    for l in c1_com_pandemia:
        for chave, rot in [("ideb_iniciais", "Ideb dos anos iniciais"), ("ideb_finais", "Ideb dos anos finais"), ("ideb_medio", "Ideb do ensino médio")]:
            if l["indicador"].startswith(rot) and 2021 in doc[chave]:
                b, lv = (doc[chave][2021] - doc[chave][2017]) / 2, (doc[chave][2025] - doc[chave][2021]) / 2
                l["pontos_lula"], l["pontos_flavio"] = r1.comparar(b, lv, "maior", 0.1)
    sens_ideb = notas(c1_com_pandemia, props, c6v, c7v)
    sem_c6 = {"sem_C6": {g: {**v, **({"C6": 0} if "C6" in v else {})} for g, v in PESOS["principal"].items()}}
    sem_c7 = {"sem_C7": {g: {**v, **({"C7": 0} if "C7" in v else {})} for g, v in PESOS["principal"].items()}}
    resumo = {
        "rodada": 2,
        "gerado_em": dt.date.today().isoformat(),
        "c1_indicadores": c1_lin,
        "c7_obras": c7v,
        "c6": c6v,
        "c2_informativo": rod1["c2"],
        "propostas": props,
        "temas": temas,
        "rodada1_vereditos": {t: {"lula": rod1["temas"][t]["pesos"]["principal"]["lula"], "flavio": rod1["temas"][t]["pesos"]["principal"]["flavio"], "veredito": rod1["temas"][t]["veredito"]} for t in TEMAS},
        "sensibilidade": {
            "ideb_com_a_pandemia": {t: sens_ideb[t]["pesos"]["principal"] for t in ("educacao",)},
            "sem_mercado_C6": {"economia": notas(c1_lin, props, c6v, c7v, sem_c6)["economia"]["pesos"]["sem_C6"]},
            "sem_obras_C7": {t: notas(c1_lin, props, c6v, c7v, sem_c7)[t]["pesos"]["sem_C7"] for t in TEMAS},
        },
        "contexto": contexto(),
        "base_comum": [{"id": p["id"], "lado": p["lado"], "tema": p["tema"], "proposta": p["proposta"]} for p in props if p["tipo"] == "base"],
        "conferencia_planos": rod1["conferencia_planos"],
        "stf": rod1["stf"],
        "c1_sensibilidade_todos_os_mandatos": rod1["c1_sensibilidade_todos_os_mandatos"],
        "informativo_seguranca": {"roubo_de_celular": {k: v for k, v in doc.get("roubo_celular", {}).items()}},
    }
    (SAIDA / "RESUMO.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1), encoding="utf-8")
    for t in TEMAS:
        v = temas[t]; p = v["pesos"]["principal"]
        print(f"{v['nome']:<30} Lula {p['lula']:5.1f} | Flávio {p['flavio']:5.1f} -> {v['veredito']:<7} ({v['robustez']}) {p['contribuicoes']}")


if __name__ == "__main__":
    main()
