"""Rodada 1: calcula as notas com as regras até a emenda 5 e grava resultados/rodada1/RESUMO.json.

C1 (histórico) sai das séries em dados/series/ e dos valores conferidos em
dados/evidencias/VALORES_DOCUMENTOS.csv; C2 do balanço do g1; C3, C4 e C5 de
dados/evidencias/NOTAS_PROPOSTAS.csv; C6 do estudo de evento do mercado.
Nenhum número é digitado aqui fora das regras do docs/PRE_REGISTRO.md.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import statistics as st
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SERIES = RAIZ / "dados" / "series"
EVID = RAIZ / "dados" / "evidencias"
SAIDA = RAIZ / "resultados"

LADOS = ("lula", "flavio")
TEMAS = ("seguranca", "saude", "economia", "corrupcao", "educacao", "pobreza")
NOME_TEMA = {"seguranca": "Segurança", "saude": "Saúde", "economia": "Economia", "corrupcao": "Corrupção",
             "educacao": "Educação", "pobreza": "Pobreza, fome e desigualdade"}

# ----------------------------------------------------------------- leitura das séries

def _json(nome):
    return json.loads((SERIES / f"{nome}.json").read_text(encoding="utf-8"))


def imf(ind, nome):
    v = _json(nome)["values"][ind]
    return {k: {int(a): float(x) for a, x in v[k].items()} for k in ("BRA", "OEMDC", "WE")}


def wb(nome):
    d = _json(nome)[1]
    out = {}
    for r in d:
        if r["value"] is not None:
            out.setdefault(r["countryiso3code"], {})[int(r["date"])] = float(r["value"])
    return out


def sidra(nome):
    d = _json(nome)[1:]
    return {r["D3C"]: float(r["V"]) for r in d if r["V"] not in ("...", "-", "X")}


def bcb(nome):
    return {dt.datetime.strptime(x["data"], "%d/%m/%Y").date(): float(x["valor"]) for x in _json(nome)}


def documentos():
    out = {}
    for l in csv.DictReader((EVID / "VALORES_DOCUMENTOS.csv").open(encoding="utf-8")):
        if l["uso"] == "principal":
            out.setdefault(l["indicador"], {})[int(l["ano"])] = float(l["valor"])
    return out


def yahoo(nome):
    d = _json(nome)["chart"]["result"][0]
    return {dt.datetime.utcfromtimestamp(t).date(): c for t, c in zip(d["timestamp"], d["indicators"]["quote"][0]["close"]) if c}


# ----------------------------------------------------------------- regras do C1

def media(serie, anos):
    vals = [serie[a] for a in anos if a in serie]
    return sum(vals) / len(vals) if vals else None


def por_ano(ini, fim, anos):
    return (fim - ini) / anos


def cagr(ini, fim, anos):
    return ((fim / ini) ** (1 / anos) - 1) * 100


def comparar(b, l, melhor, dmin):
    """Devolve (pontos_lula, pontos_flavio) de 0 a 2."""
    dif = round(l - b, 9)  # arredonda para a diferença exata não virar 0,0999... por conta de casas decimais
    if abs(dif) < dmin - 1e-9:
        return 1, 1
    lula_melhor = dif > 0 if melhor == "maior" else dif < 0
    return (2, 0) if lula_melhor else (0, 2)


def anos_fracao(fim: str) -> float:
    """Anos entre dez/2022 e um mês AAAAMM."""
    a, m = int(fim[:4]), int(fim[4:])
    return (a - 2022) + (m - 12) / 12


def indicadores_c1(sem_pandemia=False):
    """Uma linha por indicador: valor do mandato Bolsonaro (2019-2022) e do mandato atual de Lula."""
    linhas = []
    doc = documentos()
    anos_b = [2019, 2022] if sem_pandemia else [2019, 2020, 2021, 2022]
    anos_l = [2023, 2024, 2025]

    pib = imf("NGDP_RPCH", "imf-pib")
    dpib = {a: pib["BRA"][a] - pib["OEMDC"][a] for a in pib["BRA"] if a in pib["OEMDC"]}
    linhas.append(("economia", "PIB real, Brasil menos emergentes (p.p. ao ano, média)", media(dpib, anos_b), media(dpib, anos_l), "maior", 0.3, "FMI WEO"))
    inf = imf("PCPIPCH", "imf-inflacao")
    dinf = {a: inf["BRA"][a] - inf["OEMDC"][a] for a in inf["BRA"] if a in inf["OEMDC"]}
    linhas.append(("economia", "Inflação, Brasil menos emergentes (p.p. ao ano, média)", media(dinf, anos_b), media(dinf, anos_l), "menor", 0.5, "FMI WEO"))

    des = sidra("ibge-desocupacao")
    ult_des = max(des)
    linhas.append(("economia", f"Desemprego, variação ao ano (p.p.; até {ult_des[4:]}/{ult_des[:4]})",
                   por_ano(des["201812"], des["202212"], 4), por_ano(des["202212"], des[ult_des], anos_fracao(ult_des)), "menor", 0.2, "IBGE, PNAD Contínua (SIDRA 6381)"))
    div = bcb("bcb-divida-bruta")
    ult_div = max(div)
    linhas.append(("economia", f"Dívida bruta do governo geral, variação ao ano (p.p. do PIB; até {ult_div:%m/%Y})",
                   por_ano(div[dt.date(2018, 12, 1)], div[dt.date(2022, 12, 1)], 4),
                   por_ano(div[dt.date(2022, 12, 1)], div[ult_div], anos_fracao(f"{ult_div:%Y%m}")), "menor", 0.5, "Banco Central (SGS 13762)"))
    ren = sidra("ibge-rendimento-real")
    ult_ren = max(ren)
    linhas.append(("economia", f"Rendimento médio real do trabalho, variação ao ano (%; até {ult_ren[4:]}/{ult_ren[:4]})",
                   cagr(ren["201812"], ren["202212"], 4), cagr(ren["202212"], ren[ult_ren], anos_fracao(ult_ren)), "maior", 0.5, "IBGE, PNAD Contínua (SIDRA 6390)"))

    mvi = doc["mvi_taxa"]
    linhas.append(("seguranca", "Mortes violentas intencionais por 100 mil, variação ao ano", por_ano(mvi[2018], mvi[2022], 4), por_ano(mvi[2022], mvi[2025], 3), "menor", 0.3, "Anuário FBSP 2026"))
    rv = doc["roubo_veiculo_taxa"]
    linhas.append(("seguranca", "Roubo de veículo por 100 mil veículos, variação ao ano (%)", cagr(rv[2018], rv[2022], 4), cagr(rv[2022], rv[2025], 3), "menor", 2.0, "Anuários FBSP 2019, 2023 e 2026"))
    es = doc["estelionato_registros"]
    linhas.append(("seguranca", "Estelionato registrado, variação ao ano (%)", cagr(es[2018], es[2022], 4), cagr(es[2022], es[2025], 3), "menor", 2.0, "Anuários FBSP 2023 e 2026"))

    def rel(nome):
        s = wb(nome)
        return {a: s["BRA"][a] - s["LCN"][a] for a in s["BRA"] if a in s.get("LCN", {})}
    ult_wb = 2024
    for nome, rot, melhor, dmin in [("wb-esperanca-vida", "Esperança de vida, Brasil menos América Latina, variação ao ano (anos)", "maior", 0.1),
                                    ("wb-mortalidade-infantil", "Mortalidade infantil, Brasil menos América Latina, variação ao ano (por mil)", "menor", 0.1),
                                    ("wb-vacina-sarampo", "Vacina de sarampo, Brasil menos América Latina, variação ao ano (p.p.)", "maior", 1.0)]:
        r = rel(nome)
        linhas.append(("saude", rot, por_ano(r[2018], r[2022], 4), por_ano(r[2022], r[ult_wb], ult_wb - 2022), melhor, dmin, "Banco Mundial (OMS/ONU)"))

    for ind, rot in [("ideb_medio", "Ideb do ensino médio, variação por edição"), ("ideb_iniciais", "Ideb dos anos iniciais, variação por edição")]:
        s = doc[ind]
        linhas.append(("educacao", rot, por_ano(s[2017], s[2021], 2), por_ano(s[2021], s[2025], 2), "maior", 0.1, "Inep (via Agência Brasil, Folha de Pernambuco e Inep)"))

    ipc, mm = doc["ipc_brasil"], doc["ipc_media_mundial"]
    r = {a: ipc[a] - mm[a] for a in ipc}
    linhas.append(("corrupcao", "Índice de Percepção da Corrupção, Brasil menos média mundial, variação ao ano (pontos)", por_ano(r[2018], r[2022], 4), por_ano(r[2022], r[2025], 3), "maior", 1.0, "Transparência Internacional"))
    w = wb("wb-wgi-controle-corrupcao")["BRA"]
    linhas.append(("corrupcao", "Controle da Corrupção (Banco Mundial, nota 0 a 100), variação ao ano", por_ano(w[2018], w[2022], 4), por_ano(w[2022], w[2025], 3), "maior", 3.0, "Banco Mundial (WGI)"))

    pob = wb("wb-pobreza-3dolares")["BRA"]
    linhas.append(("pobreza", "Extrema pobreza (US$ 3 por dia), variação ao ano (p.p.)", por_ano(pob[2018], pob[2022], 4), por_ano(pob[2022], pob[2024], 2), "menor", 0.2, "Banco Mundial sobre a PNAD (emenda 5)"))
    gini = {int(k): v for k, v in sidra("ibge-gini").items()}
    linhas.append(("pobreza", "Índice de Gini do rendimento domiciliar per capita, variação ao ano", por_ano(gini[2018], gini[2022], 4), por_ano(gini[2022], gini[2025], 3), "menor", 0.003, "IBGE, PNAD Contínua (SIDRA 7435)"))
    fao = wb("wb-subalimentacao")["BRA"]
    linhas.append(("pobreza", "Subalimentação (FAO, média de 3 anos), variação ao ano (p.p.)", por_ano(fao[2018], fao[2022], 4), por_ano(fao[2022], fao[2024], 2), "menor", 0.5, "FAO (via Banco Mundial)"))

    out = []
    for tema, rot, b, l, melhor, dmin, fonte in linhas:
        pl, pf = comparar(b, l, melhor, dmin)
        out.append({"tema": tema, "indicador": rot, "bolsonaro_2019_2022": round(b, 4), "lula_2023_atual": round(l, 4),
                    "melhor": melhor, "diferenca_minima": dmin, "pontos_lula": pl, "pontos_flavio": pf, "fonte": fonte})
    return out


def indicadores_longo_prazo():
    """Sensibilidade: todos os mandatos de Lula (2003-2010 e 2023 em diante) e governos Dilma, onde há série."""
    out = []
    pib = imf("NGDP_RPCH", "imf-pib"); inf = imf("PCPIPCH", "imf-inflacao")
    dpib = {a: pib["BRA"][a] - pib["OEMDC"][a] for a in pib["BRA"]}
    dinf = {a: inf["BRA"][a] - inf["OEMDC"][a] for a in inf["BRA"]}
    lula_todos = list(range(2003, 2011)) + [2023, 2024, 2025]
    dilma = list(range(2011, 2017))
    bolso = [2019, 2020, 2021, 2022]
    for rot, s, melhor, dmin in [("PIB, Brasil menos emergentes", dpib, "maior", 0.3), ("Inflação, Brasil menos emergentes", dinf, "menor", 0.5)]:
        b, l, d = media(s, bolso), media(s, lula_todos), media(s, dilma)
        pl, pf = comparar(b, l, melhor, dmin)
        out.append({"indicador": rot, "bolsonaro": round(b, 3), "lula_todos_os_mandatos": round(l, 3), "dilma": round(d, 3), "pontos_lula": pl, "pontos_flavio": pf})
    for nome, rot, melhor, dmin in [("wb-esperanca-vida", "Esperança de vida, Brasil menos América Latina", "maior", 0.1),
                                    ("wb-mortalidade-infantil", "Mortalidade infantil, Brasil menos América Latina", "menor", 0.1),
                                    ("wb-vacina-sarampo", "Vacina de sarampo, Brasil menos América Latina", "maior", 1.0)]:
        s = wb(nome)
        r = {a: s["BRA"][a] - s["LCN"][a] for a in s["BRA"] if a in s.get("LCN", {})}
        b = por_ano(r[2018], r[2022], 4)
        l = ((r[2010] - r[2002]) + (r[2024] - r[2022])) / (8 + 2)
        d = por_ano(r[2010], r[2016], 6)
        pl, pf = comparar(b, l, melhor, dmin)
        out.append({"indicador": rot + " (variação ao ano)", "bolsonaro": round(b, 3), "lula_todos_os_mandatos": round(l, 3), "dilma": round(d, 3), "pontos_lula": pl, "pontos_flavio": pf})
    return out


# ----------------------------------------------------------------- C2, C3 a C5

def c2():
    # g1, Promessas dos Políticos (capturas R04, R05, R09): cumpridas + metade das parciais, sobre o total
    lula = (26 + 0.5 * 4) / 36 * 100
    parciais_b = round(0.17 * 58)
    bolso = (19 + 0.5 * parciais_b) / 58 * 100
    return {"lula": round(lula, 2), "flavio": round(bolso, 2), "base": {"lula": "26 cumpridas, 4 em parte e 6 não, de 36 (até 30/06/2026)", "flavio": f"19 cumpridas, {parciais_b} em parte (17%) e 29 não, de 58 (até 31/12/2022, governo Jair Bolsonaro)"}}


def propostas():
    sel = {l["id"]: l for l in csv.DictReader((EVID / "PROPOSTAS_SELECAO.csv").open(encoding="utf-8"))}
    notas = {l["id"]: l for l in csv.DictReader((EVID / "NOTAS_PROPOSTAS.csv").open(encoding="utf-8"))}
    out = []
    for pid, s in sel.items():
        if pid.endswith("-sem"):
            out.append({**s, "sem_proposta": True})
            continue
        n = notas[pid]
        out.append({**s, **n, "sem_proposta": False, "c3_nota": float(n["c3_nota"]), "c4_nota": float(n["c4_nota"]), "c5_nota": float(n["c5_nota"])})
    return out


# ----------------------------------------------------------------- C6

def c6():
    """Estudo de evento. Bolsa: Ibovespa contra o ETF de emergentes (EEM), nos dias de pregão da B3.
    Moeda: PTAX do Banco Central (dólar em reais) contra a média de peso mexicano, rand, peso chileno e
    peso colombiano (Yahoo). As moedas de fora usam a última cotação disponível antes de cada dia, porque
    a Yahoo data o pregão de câmbio de um jeito que não casa com o calendário da B3; o desalinhamento
    aumenta o ruído da base e deixa o teste mais difícil de passar, nunca mais fácil."""
    ib, eem = yahoo("mkt-ibovespa"), yahoo("mkt-eem")
    fx = {k: yahoo(f"mkt-usd{k}") for k in ("mxn", "zar", "clp", "cop")}
    ptax = bcb("bcb-dolar-ptax")
    evento, antes = dt.date(2026, 10, 5), dt.date(2026, 10, 2)

    def ultimo(s, d):
        ks = [k for k in s if k <= d]
        return s[max(ks)] if ks else None

    def ret(s, a, b):
        va, vb = ultimo(s, a), ultimo(s, b)
        return (vb / va - 1) * 100

    def ret_fx_fora(a, b):
        return sum(ret(fx[k], a, b) for k in fx) / len(fx)

    dias = sorted(d for d in set(ib) & set(eem) & set(ptax) if d <= antes)[-251:]
    b_hist, m_hist = [], []
    for a, b in zip(dias[:-1], dias[1:]):
        b_hist.append(ret(ib, a, b) - ret(eem, a, b))
        m_hist.append(ret(ptax, a, b) - ret_fx_fora(a, b))
    sd_b, sd_m = st.pstdev(b_hist), st.pstdev(m_hist)
    bolsa = ret(ib, antes, evento) - ret(eem, antes, evento)
    # câmbio de fora: da última cotação antes do dia do evento até a cotação datada no dia do evento
    fora_evento = sum((fx[k][evento] / ultimo(fx[k], evento - dt.timedelta(days=1)) - 1) * 100 for k in fx) / len(fx)
    moeda = ret(ptax, antes, evento) - fora_evento
    zb, zm = bolsa / sd_b, moeda / sd_m
    a_favor = (zb > 2) + (zm < -2)   # bolsa sobe e real se valoriza
    contra = (zb < -2) + (zm > 2)
    if a_favor == 2:
        nota = {"flavio": 100, "lula": 0}
    elif contra == 2:
        nota = {"flavio": 0, "lula": 100}
    else:
        nota = {"flavio": 50, "lula": 50}
    return {
        "evento": "05/10/2026, primeiro pregão depois do 1º turno",
        "ibovespa_dia_pct": round(ret(ib, antes, evento), 2), "eem_dia_pct": round(ret(eem, antes, evento), 2),
        "bolsa_anormal_pct": round(bolsa, 2), "desvio_padrao_bolsa_pct": round(sd_b, 2), "z_bolsa": round(zb, 1),
        "ptax_dia_pct": round(ret(ptax, antes, evento), 2), "dolar_emergentes_dia_pct": round(fora_evento, 2),
        "moeda_anormal_pct": round(moeda, 2), "desvio_padrao_moeda_pct": round(sd_m, 2), "z_moeda": round(zm, 1),
        "pregoes_na_base": len(b_hist), "nota": nota,
        "juros_futuros": {
            "di_jan2031_05out": {"de": 13.99, "para": 12.70, "fontes": ["M-moneytimes-juros-5-10-26", "M04-noticiasdoplanalto-juros"]},
            "di_jan2031_15out": {"de": 12.494, "para": 12.760, "polymarket_flavio": {"de": 89, "para": 76}, "fontes": ["M-moneytimes-juros-15-10-26", "M02-ocafezinho-juros-16out"]},
        },
    }


# ----------------------------------------------------------------- notas de tema

PESOS = {
    "principal": {"geral": {"C1": 25, "C2": 15, "C3": 30, "C4": 20, "C5": 10, "C6": 0},
                  "economia": {"C1": 20, "C2": 10, "C3": 25, "C4": 20, "C5": 10, "C6": 15}},
    "iguais": {"geral": {"C1": 20, "C2": 20, "C3": 20, "C4": 20, "C5": 20, "C6": 0},
               "economia": {"C1": 100 / 6, "C2": 100 / 6, "C3": 100 / 6, "C4": 100 / 6, "C5": 100 / 6, "C6": 100 / 6}},
    "historico_pesa_mais": {"geral": {"C1": 40, "C2": 20, "C3": 20, "C4": 10, "C5": 10, "C6": 0},
                            "economia": {"C1": 40, "C2": 20, "C3": 10, "C4": 10, "C5": 10, "C6": 10}},
    "execucao_pesa_mais": {"geral": {"C1": 15, "C2": 10, "C3": 45, "C4": 20, "C5": 10, "C6": 0},
                           "economia": {"C1": 15, "C2": 10, "C3": 35, "C4": 20, "C5": 10, "C6": 10}},
}


def notas_por_tema(c1_lin, c2v, props, c6v, pesos_extra=None):
    out = {}
    for tema in TEMAS:
        crit = {lado: {} for lado in LADOS}
        ind = [l for l in c1_lin if l["tema"] == tema]
        crit["lula"]["C1"] = sum(l["pontos_lula"] for l in ind) / len(ind) * 50
        crit["flavio"]["C1"] = sum(l["pontos_flavio"] for l in ind) / len(ind) * 50
        for lado in LADOS:
            crit[lado]["C2"] = c2v[lado]
            ps = [p for p in props if p["tema"] == tema and p["lado"] == lado and not p["sem_proposta"]]
            for c in ("c3", "c4", "c5"):
                crit[lado][c.upper()] = sum(p[f"{c}_nota"] for p in ps) / len(ps)
            crit[lado]["C6"] = c6v["nota"][lado] if tema == "economia" else 0
        cenarios = {}
        for nome, pesos in (pesos_extra or PESOS).items():
            pw = pesos["economia" if tema == "economia" else "geral"]
            tot = {lado: sum(crit[lado][c] * pw[c] for c in pw) / sum(pw.values()) for lado in LADOS}
            dif = tot["lula"] - tot["flavio"]
            ver = "empate" if abs(dif) < 5 else ("Lula" if dif > 0 else "Flávio")
            cenarios[nome] = {"lula": round(tot["lula"], 1), "flavio": round(tot["flavio"], 1), "diferenca": round(dif, 1), "veredito": ver}
        vers = {c["veredito"] for c in cenarios.values()}
        if pesos_extra:
            out[tema] = {k: v for k, v in cenarios.items()}
            continue
        out[tema] = {"nome": NOME_TEMA[tema],
                     "criterios": {lado: {k: round(v, 1) for k, v in crit[lado].items()} for lado in LADOS},
                     "pesos": cenarios, "veredito": cenarios["principal"]["veredito"],
                     "robustez": "firme" if len(vers) == 1 else "depende do peso"}
    return out


def conferencia_planos():
    """Números que os próprios planos citam, conferidos nas séries oficiais."""
    div = bcb("bcb-divida-bruta")
    ipca = {}
    for d, v in bcb("bcb-ipca-mensal").items():
        ipca.setdefault(d.year, 1.0)
        ipca[d.year] *= 1 + v / 100
    ipca = {a: (v - 1) * 100 for a, v in ipca.items()}
    gini = {int(k): v for k, v in sidra("ibge-gini").items()}
    ult = max(div)
    return [
        {"lado": "flavio", "afirmacao": "Reduzimos em 4 pontos percentuais a relação entre a dívida e o PIB (governo Bolsonaro)", "pagina": 29,
         "conferido": f"dez/2018 {div[dt.date(2018, 12, 1)]:.2f}% para dez/2022 {div[dt.date(2022, 12, 1)]:.2f}% ({div[dt.date(2022, 12, 1)] - div[dt.date(2018, 12, 1)]:+.1f} pontos)",
         "situacao": "bate, arredondado"},
        {"lado": "flavio", "afirmacao": "Em quatro anos, a dívida pública cresceu 13 pontos percentuais em relação ao PIB (governo atual)", "pagina": 29,
         "conferido": f"dez/2022 {div[dt.date(2022, 12, 1)]:.2f}% para {ult:%m/%Y} {div[ult]:.2f}% ({div[ult] - div[dt.date(2022, 12, 1)]:+.1f} pontos)",
         "situacao": "não bate com a dívida bruta do governo geral do Banco Central; o plano não diz que conceito usou"},
        {"lado": "lula", "afirmacao": "A inflação alcançou uma média anual de 4,6%", "pagina": 10,
         "conferido": f"IPCA de dezembro a dezembro: 2023 {ipca[2023]:.2f}%, 2024 {ipca[2024]:.2f}%, 2025 {ipca[2025]:.2f}%; média {(ipca[2023] + ipca[2024] + ipca[2025]) / 3:.2f}%",
         "situacao": "bate"},
        {"lado": "lula", "afirmacao": "O Gini atingiu o menor patamar histórico de 0,504", "pagina": 12,
         "conferido": f"IBGE: 2024 {gini[2024]:.3f}; 2025 {gini[2025]:.3f}",
         "situacao": "bate para 2024; na mesma série, 2025 subiu"},
        {"lado": "lula", "afirmacao": "A pobreza extrema recuou para o menor nível da série, de 4,6% da população", "pagina": 12,
         "conferido": "IBGE, linha de US$ 2,15: 4,4% em 2023 e 3,5% em 2024 (capturas X05 e X01)",
         "situacao": "não bate com a série do IBGE na linha de US$ 2,15; o plano não diz a linha"},
    ]


def main():
    c1_lin = indicadores_c1()
    c1_sem = indicadores_c1(sem_pandemia=True)
    longo = indicadores_longo_prazo()
    c2v = c2()
    props = propostas()
    c6v = c6()
    temas = notas_por_tema(c1_lin, c2v, props, c6v)
    temas_sem_pandemia = notas_por_tema(c1_sem, c2v, props, c6v)
    # Sensibilidades NÃO pré-registradas (pedidas pela revisão adversarial; não mudam o veredito oficial)
    sem_c2 = {"sem_C2": {"geral": {**PESOS["principal"]["geral"], "C2": 0}, "economia": {**PESOS["principal"]["economia"], "C2": 0}}}
    sens_sem_c2 = notas_por_tema(c1_lin, c2v, props, c6v, pesos_extra=sem_c2)
    so_propostas = {"so_C3_C4_C5": {"geral": {"C1": 0, "C2": 0, "C3": 30, "C4": 20, "C5": 10, "C6": 0}, "economia": {"C1": 0, "C2": 0, "C3": 30, "C4": 20, "C5": 10, "C6": 0}}}
    sens_props = notas_por_tema(c1_lin, c2v, props, c6v, pesos_extra=so_propostas)
    sem_estel = [l for l in c1_lin if not l["indicador"].startswith("Estelionato")]
    sens_sem_estel = notas_por_tema(sem_estel, c2v, props, c6v)["seguranca"]["pesos"]["principal"]
    sem_c6 = {"sem_C6": {"geral": PESOS["principal"]["geral"], "economia": {**PESOS["principal"]["economia"], "C6": 0}}}
    sens_sem_c6 = notas_por_tema(c1_lin, c2v, props, c6v, pesos_extra=sem_c6)["economia"]["sem_C6"]
    resumo = {
        "gerado_em": dt.date.today().isoformat(),
        "c1_indicadores": c1_lin,
        "c1_sensibilidade_sem_2020_2021": [l for l in c1_sem if l["indicador"].startswith(("PIB", "Inflação"))],
        "c1_sensibilidade_todos_os_mandatos": longo,
        "c2": c2v,
        "c6": c6v,
        "propostas": props,
        "temas": temas,
        "vereditos_sem_2020_2021": {t: temas_sem_pandemia[t]["veredito"] for t in TEMAS},
        "sensibilidade_nao_preregistrada": {
            "sem_C2": {t: sens_sem_c2[t]["sem_C2"] for t in TEMAS},
            "so_propostas_C3_C4_C5": {t: sens_props[t]["so_C3_C4_C5"] for t in TEMAS},
            "seguranca_sem_estelionato": sens_sem_estel,
            "economia_sem_C6": sens_sem_c6,
        },
        "conferencia_planos": conferencia_planos(),
        "stf": {
            "vagas_no_mandato_2027_2030": ["vaga de Barroso (aberta desde out/2025; o Senado rejeitou Jorge Messias por 42 a 34 em abr/2026)",
                                            "Luiz Fux (75 anos em 26/04/2028)", "Cármen Lúcia (75 anos em 19/04/2029)",
                                            "Gilmar Mendes (75 anos em 30/12/2030, no fim do mandato)"],
            "evidencias": ["EV070", "EV071", "EV072", "EV073", "EV074", "EV075", "EV076"],
            "aprovacao_no_senado": "maioria absoluta, 41 de 81",
            "senado_2027": {"direita": 48, "centro": 17, "esquerda": 15},
        },
    }
    destino = SAIDA / "rodada1"  # rodada 1 (pesos e regras até a emenda 5); a rodada 2 está em calcular-rodada2.py
    destino.mkdir(parents=True, exist_ok=True)
    (destino / "RESUMO.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1), encoding="utf-8")
    for t in TEMAS:
        v = temas[t]
        print(f"{v['nome']:<30} Lula {v['pesos']['principal']['lula']:5.1f} | Flávio {v['pesos']['principal']['flavio']:5.1f} -> {v['veredito']} ({v['robustez']})")


if __name__ == "__main__":
    main()
