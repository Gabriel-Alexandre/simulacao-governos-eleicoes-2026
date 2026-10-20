"""Simulação da dívida bruta até 2030 (docs/PRE_REGISTRO.md §8).

Base: cenário base da IFI (RAF nº 113, jun/2026; evidências EV087 a EV090).
A equação da dívida, d_t = d_{t-1} (1 + i_t) / (1 + g_t) - s_t, é calibrada para reproduzir a
base: o juro efetivo implícito i_t sai da própria base da IFI. Em cima dela:

1. Prêmio de juros que o mercado cobra a mais num governo Lula (EV083, EV084, EV085, EV086):
   no dia 15/10/2026 o DI de janeiro de 2031 subiu 0,266 ponto quando a chance de vitória de
   Flávio na Polymarket caiu 13 pontos; a diferença inteira entre os dois resultados fica em
   0,266 / 0,13 = 2,05 pontos ao ano. Faixa: metade disso (1,02) até a diferença citada por
   analistas no BPMoney (13,90 - 11,50 = 2,40).
2. Repasse do juro de mercado para o juro médio da dívida (HIPÓTESE DECLARADA, sem fonte):
   45% em 2027, 65% em 2028, 80% em 2029 e 90% em 2030, porque a dívida é rolada aos poucos.
   Sensibilidade: repasse total imediato e repasse de 50% constante.
3. Esforço fiscal prometido: o plano de Flávio promete superávits primários sem dizer quanto;
   usa-se a diferença entre o cenário otimista e o base da IFI para o governo central
   (0,4 em 2027, 0,6 em 2028, 0,9 em 2029 e 1,2 em 2030, em pontos do PIB).
   O plano de Lula promete manter o arcabouço, que é o que a base da IFI já supõe.
"""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "resultados"

ANOS = [2026, 2027, 2028, 2029, 2030]
DIVIDA_BASE = {2025: 78.6, 2026: 82.5, 2027: 86.4, 2028: 90.1, 2029: 92.7, 2030: 95.7}   # EV087
PIB_NOMINAL = {2025: 12739, 2026: 13667, 2027: 14533, 2028: 15458, 2029: 16361, 2030: 17321}  # EV090
PRIMARIO_BASE = {2026: -0.4, 2027: -0.6, 2028: -0.6, 2029: -0.8, 2030: -1.1}   # EV088 (governo central)
PRIMARIO_OTIMISTA = {2026: -0.4, 2027: -0.2, 2028: 0.0, 2029: 0.1, 2030: 0.1}  # EV089
PREMIO = {"central": 0.266 / 0.13, "baixo": 0.266 / 0.13 / 2, "alto": 13.90 - 11.50}
REPASSE = {"gradual": {2026: 0.0, 2027: 0.45, 2028: 0.65, 2029: 0.80, 2030: 0.90},
           "total": {2026: 0.0, 2027: 1.0, 2028: 1.0, 2029: 1.0, 2030: 1.0},
           "metade": {2026: 0.0, 2027: 0.5, 2028: 0.5, 2029: 0.5, 2030: 0.5}}


def juro_implicito():
    i = {}
    for t in ANOS:
        g = PIB_NOMINAL[t] / PIB_NOMINAL[t - 1] - 1
        i[t] = (DIVIDA_BASE[t] + PRIMARIO_BASE[t]) * (1 + g) / DIVIDA_BASE[t - 1] - 1
    return i


def trajetoria(premio=0.0, repasse="gradual", esforco=False):
    i = juro_implicito()
    d = {2025: DIVIDA_BASE[2025]}
    for t in ANOS:
        g = PIB_NOMINAL[t] / PIB_NOMINAL[t - 1] - 1
        it = i[t] + REPASSE[repasse][t] * premio / 100
        s = PRIMARIO_BASE[t] + ((PRIMARIO_OTIMISTA[t] - PRIMARIO_BASE[t]) if esforco else 0.0)
        d[t] = d[t - 1] * (1 + it) / (1 + g) - s
    return {t: round(d[t], 2) for t in d}


def main():
    base = trajetoria()
    cen = {
        "base_ifi": base,
        "lula_com_premio": trajetoria(PREMIO["central"]),
        "flavio_promessa_cumprida": trajetoria(0.0, esforco=True),
        "flavio_promessa_nao_cumprida_com_premio_de_volta": trajetoria(PREMIO["central"]),
        "lula_se_fizesse_o_mesmo_esforco": trajetoria(PREMIO["central"], esforco=True),
    }
    sens = {}
    for nome_p, p in PREMIO.items():
        for nome_r in REPASSE:
            sens[f"premio_{nome_p}_repasse_{nome_r}"] = round(trajetoria(p, nome_r)[2030] - base[2030], 2)
    res = {
        "premio_central_pp": round(PREMIO["central"], 2),
        "premio_faixa_pp": [round(PREMIO["baixo"], 2), round(PREMIO["alto"], 2)],
        "cenarios": cen,
        "diferenca_2030_so_pelo_juro": round(cen["lula_com_premio"][2030] - base[2030], 2),
        "diferenca_2030_so_pelo_esforco": round(base[2030] - cen["flavio_promessa_cumprida"][2030], 2),
        "diferenca_2030_lula_premio_vs_flavio_cumprida": round(cen["lula_com_premio"][2030] - cen["flavio_promessa_cumprida"][2030], 2),
        "sensibilidade_juro_2030": sens,
        "conferencia_base_reproduzida": all(abs(base[t] - DIVIDA_BASE[t]) < 0.05 for t in ANOS),
    }
    SAIDA.mkdir(exist_ok=True)
    (SAIDA / "SIMULACAO_DIVIDA.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
