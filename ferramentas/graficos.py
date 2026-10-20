"""Gera os gráficos de resultados/figuras/ (1920x1080) a partir do RESUMO.json, da simulação e das séries."""
from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
FIG = RAIZ / "resultados" / "figuras"
FIG.mkdir(parents=True, exist_ok=True)
R = json.loads((RAIZ / "resultados" / "RESUMO.json").read_text(encoding="utf-8"))
S = json.loads((RAIZ / "resultados" / "SIMULACAO_DIVIDA.json").read_text(encoding="utf-8"))

COR = {"lula": "#C8553D", "flavio": "#2D6A8A", "base": "#6B6B6B", "faixa_bolso": "#2D6A8A", "faixa_lula": "#C8553D"}
FONTE_RODAPE = "Projeto aberto simulacao-governos-eleicoes-2026"
plt.rcParams.update({"font.size": 15, "axes.titlesize": 22, "axes.titleweight": "bold", "axes.spines.top": False,
                     "axes.spines.right": False, "figure.facecolor": "white", "axes.facecolor": "white"})


def br(x, nd=1, sinal=False):
    t = f"{x:+.{nd}f}" if sinal else f"{x:.{nd}f}"
    return t.replace(".", ",")


def salvar(fig, nome, fonte):
    fig.text(0.01, 0.01, f"Fonte: {fonte}. {FONTE_RODAPE}.", fontsize=11, color="#555555")
    fig.savefig(FIG / nome, dpi=160)
    plt.close(fig)


def novo():
    return plt.subplots(figsize=(12, 6.75))


def notas_por_tema():
    fig, ax = novo()
    temas = list(R["temas"].keys())
    nomes = [R["temas"][t]["nome"] for t in temas]
    y = range(len(temas))
    l = [R["temas"][t]["pesos"]["principal"]["lula"] for t in temas]
    f = [R["temas"][t]["pesos"]["principal"]["flavio"] for t in temas]
    ax.barh([i + 0.2 for i in y], l, height=0.38, color=COR["lula"], label="Caminho de Lula")
    ax.barh([i - 0.2 for i in y], f, height=0.38, color=COR["flavio"], label="Caminho de Flávio")
    for i, t in enumerate(temas):
        ax.text(l[i] + 1, i + 0.2, br(l[i]), va="center", fontsize=13)
        ax.text(f[i] + 1, i - 0.2, br(f[i]), va="center", fontsize=13)
        v = R["temas"][t]
        ax.text(101, i, f"{v['veredito']}\n({v['robustez']})", va="center", fontsize=12, color="#222222")
    ax.set_yticks(list(y)); ax.set_yticklabels(nomes)
    ax.invert_yaxis(); ax.set_xlim(0, 118)
    ax.set_xlabel("Nota do tema (0 a 100), pesos escritos antes")
    ax.set_title("Nota de cada caminho, tema por tema (rodada 2)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.1), ncol=2, frameon=False)
    ax.set_xlabel("")
    fig.text(0.01, 0.055, "Nota de 0 a 100 com os pesos escritos antes. Cada tema fecha sozinho. A IA não soma temas (Res. TSE 23.755/2026, art. 28, §1º-C).", fontsize=12, color="#333333")
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    salvar(fig, "01_notas_por_tema.png", "docs/PRE_REGISTRO.md e resultados/RESUMO.json")


def criterios():
    fig, axes = plt.subplots(1, 2, figsize=(12, 6.75), sharey=True)
    temas = list(R["temas"].keys())
    crits = ["C1", "C3", "C4", "C5", "C6", "C7"]
    rot = ["Histórico", "Caminho", "Maturidade", "Dinheiro", "Mercado", "Obras"]
    for ax, lado, titulo in zip(axes, ("lula", "flavio"), ("Lula", "Flávio")):
        m = [[(R["temas"][t]["criterios"][lado].get(c) if R["temas"][t]["criterios"][lado].get(c) is not None else -1) for c in crits] for t in temas]
        ax.imshow([[max(x, 0) for x in linha] for linha in m], cmap="Greys", vmin=0, vmax=130, aspect="auto")
        for i in range(len(temas)):
            for j in range(len(crits)):
                val = m[i][j]
                txt = "-" if val < 0 else f"{val:.0f}"
                ax.text(j, i, txt, ha="center", va="center", fontsize=13, color="white" if val > 65 else "black")
        ax.set_xticks(range(len(crits))); ax.set_xticklabels(rot, rotation=30, ha="right", fontsize=12)
        ax.set_title(titulo, color=COR[lado])
    axes[0].set_yticks(range(len(temas))); axes[0].set_yticklabels([R["temas"][t]["nome"] for t in temas], fontsize=12)
    fig.suptitle("Nota de cada critério (0 a 100)", fontsize=22, fontweight="bold")
    fig.tight_layout(rect=(0, 0.04, 1, 0.95))
    salvar(fig, "02_criterios_por_tema.png", "resultados/RESUMO.json")


def mercado():
    c6 = R["c6"]
    fig, axes = plt.subplots(1, 3, figsize=(12, 6.75))
    ax = axes[0]
    ax.bar(["Ibovespa", "Emergentes\n(EEM)"], [c6["ibovespa_dia_pct"], c6["eem_dia_pct"]], color=[COR["flavio"], COR["base"]])
    ax.set_title("Bolsa em 05/10 (%)", fontsize=16)
    for i, v in enumerate([c6["ibovespa_dia_pct"], c6["eem_dia_pct"]]):
        ax.text(i, v + 0.15, br(v, 2, True), ha="center", fontweight="bold")
    ax = axes[1]
    ax.bar(["Dólar em reais\n(PTAX)", "Dólar em\noutras moedas"], [c6["ptax_dia_pct"], c6["dolar_emergentes_dia_pct"]], color=[COR["flavio"], COR["base"]])
    ax.set_title("Dólar em 05/10 (%)", fontsize=16)
    for i, v in enumerate([c6["ptax_dia_pct"], c6["dolar_emergentes_dia_pct"]]):
        ax.text(i, v / 2 if v < -1 else v - 0.35, br(v, 2, True), ha="center", color="white" if v < -1 else "black", fontweight="bold")
    ax.axhline(0, color="black", lw=0.8)
    ax = axes[2]
    j = c6["juros_futuros"]
    ax.bar(["05/10\n(Flávio na frente)", "15/10\n(chance de Flávio\n89% → 76%)"],
           [(j["di_jan2031_05out"]["para"] - j["di_jan2031_05out"]["de"]) * 100, (j["di_jan2031_15out"]["para"] - j["di_jan2031_15out"]["de"]) * 100],
           color=[COR["flavio"], COR["lula"]])
    ax.axhline(0, color="black", lw=0.8)
    ax.set_title("Juro de 2031 (pontos-base)", fontsize=16)
    for i, v in enumerate([(j["di_jan2031_05out"]["para"] - j["di_jan2031_05out"]["de"]) * 100, (j["di_jan2031_15out"]["para"] - j["di_jan2031_15out"]["de"]) * 100]):
        ax.text(i, v + 4 if v > 0 else v / 2, br(v, 0, True), ha="center", color="black" if v > 0 else "white", fontweight="bold")
    for a in axes:
        a.tick_params(axis="x", labelsize=12)
    fig.suptitle("O que o mercado precificou", fontsize=22, fontweight="bold")
    fig.tight_layout(rect=(0, 0.05, 1, 0.94))
    salvar(fig, "03_mercado_1turno.png", "B3/Yahoo, Banco Central (PTAX), Money Times, Notícias do Planalto, O Cafezinho")


def divida():
    fig, ax = novo()
    cen = S["cenarios"]
    anos = sorted(int(a) for a in cen["base_ifi"])
    def serie(nome): return [cen[nome][str(a)] for a in anos]
    ax.plot(anos, serie("base_ifi"), color=COR["base"], lw=3, label="Base da IFI (o que vem acontecendo)")
    ax.plot(anos, serie("lula_com_premio"), color=COR["lula"], lw=3, label="Lula, com o juro a mais que o mercado cobra")
    ax.plot(anos, serie("flavio_promessa_cumprida"), color=COR["flavio"], lw=3, label="Flávio, se entregar o superávit prometido")
    for nome, cor in (("lula_com_premio", COR["lula"]), ("flavio_promessa_cumprida", COR["flavio"]), ("base_ifi", COR["base"])):
        ax.text(2030.08, cen[nome]["2030"], br(cen[nome]['2030']) + "%", va="center", color=cor, fontsize=14, fontweight="bold")
    ax.set_xlim(2025, 2030.8)
    ax.set_ylabel("Dívida bruta (% do PIB)")
    ax.set_title("Simulação da dívida até 2030")
    ax.legend(frameon=False, loc="upper left")
    fig.text(0.01, 0.055, "Se Flávio não entregar o superávit, o juro a mais tende a voltar e a linha dele encosta na de Lula.", fontsize=12, color="#333333")
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    salvar(fig, "04_simulacao_divida.png", "IFI (jun/2026), Money Times, O Cafezinho, BPMoney; hipóteses em ferramentas/simular.py")


def sombra(ax, ini_b=2019, fim_b=2022.99, ini_l=2023, fim_l=2026.8):
    ax.axvspan(ini_b, fim_b, color=COR["flavio"], alpha=0.10, lw=0)
    ax.axvspan(ini_l, fim_l, color=COR["lula"], alpha=0.10, lw=0)


def historicos():
    # Mortes violentas (linha conferida no Anuário 2026)
    txt = " ".join((RAIZ / "dados/capturas/S01-fbsp-anuario-2026.txt").read_text(encoding="utf-8").split())
    m = re.search(r"Brasil 27,7 28,0 29,7 28,9 30,2 31,2 27,9 23,0 24,1 23,0 22,7 21,9 20,8 19,1", txt)
    vals = [float(x.replace(",", ".")) for x in m.group(0).split()[1:]]
    anos = list(range(2012, 2026))
    fig, ax = novo(); sombra(ax)
    ax.plot(anos, vals, color="black", lw=3, marker="o")
    ax.set_title("Mortes violentas intencionais por 100 mil"); ax.set_ylim(0, 35)
    ax.text(2019.1, 3, "Bolsonaro", color=COR["flavio"]); ax.text(2023.1, 3, "Lula", color=COR["lula"])
    salvar(fig, "05a_seguranca_mvi.png", "Anuário Brasileiro de Segurança Pública 2026, tabela 02")

    # Dívida e desemprego
    div = {dt.datetime.strptime(x["data"], "%d/%m/%Y"): float(x["valor"]) for x in json.loads((RAIZ / "dados/series/bcb-divida-bruta.json").read_text())}
    fig, ax = novo(); sombra(ax)
    ks = sorted(div); ax.plot([k.year + (k.month - 1) / 12 for k in ks], [div[k] for k in ks], color="black", lw=2.5)
    ax.set_title("Dívida bruta do governo geral (% do PIB)"); ax.set_xlim(2015, 2026.8)
    salvar(fig, "05b_economia_divida.png", "Banco Central, SGS 13762")

    des = json.loads((RAIZ / "dados/series/ibge-desocupacao.json").read_text(encoding="utf-8"))[1:]
    xs = [int(r["D3C"][:4]) + (int(r["D3C"][4:]) - 1) / 12 for r in des]
    fig, ax = novo(); sombra(ax)
    ax.plot(xs, [float(r["V"]) for r in des], color="black", lw=2.5)
    ax.set_title("Desemprego (%, trimestre móvel)"); ax.set_ylim(0, 16)
    salvar(fig, "05c_economia_desemprego.png", "IBGE, PNAD Contínua (SIDRA 6381)")

    wb = json.loads((RAIZ / "dados/series/wb-vacina-sarampo.json").read_text(encoding="utf-8"))[1]
    b = {int(r["date"]): r["value"] for r in wb if r["countryiso3code"] == "BRA" and r["value"]}
    l = {int(r["date"]): r["value"] for r in wb if r["countryiso3code"] == "LCN" and r["value"]}
    fig, ax = novo(); sombra(ax)
    a = [x for x in sorted(b) if x >= 2010]
    ax.plot(a, [b[x] for x in a], color="black", lw=3, marker="o", label="Brasil")
    ax.plot(a, [l[x] for x in a], color=COR["base"], lw=2, ls="--", label="América Latina e Caribe")
    ax.set_title("Vacina de sarampo, 1ª dose (% das crianças)"); ax.legend(frameon=False); ax.set_ylim(60, 100)
    salvar(fig, "05d_saude_vacina.png", "Banco Mundial (OMS/UNICEF)")

    import csv
    ideb = {"Ensino médio": {}, "Anos iniciais": {}}
    for linha in csv.DictReader((RAIZ / "dados/evidencias/VALORES_DOCUMENTOS.csv").open(encoding="utf-8")):
        alvo = {"ideb_medio": "Ensino médio", "ideb_iniciais": "Anos iniciais"}.get(linha["indicador"])
        if alvo:
            ideb[alvo][int(linha["ano"])] = float(linha["valor"])
    ideb = {k: dict(sorted(v.items())) for k, v in ideb.items()}
    fig, ax = novo(); sombra(ax)
    for (nome, s), cor in zip(ideb.items(), ("black", COR["base"])):
        ax.plot(list(s), list(s.values()), marker="o", lw=3, color=cor, label=nome)
        for x, v in s.items():
            ax.text(x, v + 0.07, f"{v:.1f}".replace(".", ","), ha="center", fontsize=12)
    ax.set_title("Ideb (0 a 10)"); ax.set_ylim(3, 7); ax.legend(frameon=False, loc="center right")
    salvar(fig, "05e_educacao_ideb.png", "Inep, via Agência Brasil, Folha de Pernambuco, IBGE e Inep (valores em dados/evidencias)")

    pob = json.loads((RAIZ / "dados/series/wb-pobreza-3dolares.json").read_text(encoding="utf-8"))[1]
    p = {int(r["date"]): r["value"] for r in pob if r["countryiso3code"] == "BRA" and r["value"] is not None}
    fig, ax = novo(); sombra(ax)
    a = [x for x in sorted(p) if x >= 2012]
    ax.plot(a, [p[x] for x in a], color="black", lw=3, marker="o")
    ax.set_title("Extrema pobreza (% da população, US$ 3 por dia)"); ax.set_ylim(0, 9)
    salvar(fig, "05f_pobreza_extrema.png", "Banco Mundial, sobre a PNAD Contínua do IBGE")


def stf():
    fig, ax = novo()
    eventos = [(2025.8, "Barroso se aposenta\n(vaga aberta)"), (2026.33, "Senado rejeita\nMessias (42 a 34)"),
               (2028.32, "Fux, 75 anos"), (2029.30, "Cármen Lúcia,\n75 anos"), (2030.99, "Gilmar Mendes,\n75 anos")]
    ax.axhline(0, color="black", lw=2)
    ax.axvspan(2027.0, 2031.0, color="#EEEEEE")
    ax.text(2027.05, 0.8, "Mandato 2027 a 2030", fontsize=14)
    for i, (x, t) in enumerate(eventos):
        y = 0.45 if i % 2 == 0 else -0.45
        ax.plot([x, x], [0, y * 0.8], color="black", lw=1)
        ax.scatter([x], [0], s=120, color=COR["base"], zorder=3)
        ax.text(x, y, t, ha="center", va="center", fontsize=13)
    ax.set_xlim(2025.5, 2031.3); ax.set_ylim(-1, 1); ax.set_yticks([])
    ax.set_title("Vagas no STF que o próximo governo deve preencher")
    fig.text(0.01, 0.055, "Indicado ao STF precisa de 41 votos no Senado. Senado de 2027: direita 48, centro 17, esquerda 15.", fontsize=12, color="#333333")
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    salvar(fig, "06_stf_vagas.png", "Migalhas, Goiás246, CNN Brasil, Times Brasil; projeto congresso-e-governos-eleicoes-2026")


def robustez():
    fig, ax = novo()
    temas = list(R["temas"].keys())
    cen = ["principal", "iguais", "historico_pesa_mais", "execucao_pesa_mais"]
    rot = ["Pesos\nescritos antes", "Todos\niguais", "Histórico\npesa mais", "Execução\npesa mais", "Sem o critério\nde obras"]
    cores = {"Lula": COR["lula"], "Flávio": COR["flavio"], "empate": "#BBBBBB"}
    for i, t in enumerate(temas):
        vs = [R["temas"][t]["pesos"][c]["veredito"] for c in cen] + [R["sensibilidade"]["sem_obras_C7"][t]["veredito"]]
        for j, v in enumerate(vs):
            ax.add_patch(plt.Rectangle((j, i), 0.95, 0.9, color=cores[v]))
            ax.text(j + 0.47, i + 0.45, v, ha="center", va="center", color="white" if v != "empate" else "black", fontsize=13)
    ax.set_xlim(0, 5); ax.set_ylim(len(temas), 0)
    ax.set_xticks([j + 0.47 for j in range(5)]); ax.set_xticklabels(rot, fontsize=12)
    ax.set_yticks([i + 0.45 for i in range(len(temas))]); ax.set_yticklabels([R["temas"][t]["nome"] for t in temas])
    ax.spines[:].set_visible(False); ax.tick_params(length=0)
    ax.set_title("O veredito muda com o peso? (rodada 2)")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    salvar(fig, "07_robustez.png", "resultados/RESUMO.json")


def crimes():
    ls = [l for l in R["c1_indicadores"] if l["tema"] == "seguranca"]
    fig, ax = plt.subplots(figsize=(12, 6.75))
    y = range(len(ls))
    b = [l["bolsonaro_2019_2022"] for l in ls]; lv = [l["lula_2023_atual"] for l in ls]
    ax.barh([i - 0.2 for i in y], b, height=0.38, color=COR["flavio"], label="Bolsonaro (2018 a 2022)")
    ax.barh([i + 0.2 for i in y], lv, height=0.38, color=COR["lula"], label="Lula (2022 a 2025)")
    ax.axvline(0, color="black", lw=0.8)
    ax.set_yticks(list(y)); ax.set_yticklabels([l["indicador"].split(",")[0] for l in ls], fontsize=11)
    ax.invert_yaxis(); ax.set_xlabel("Variação ao ano dos casos (%); à esquerda de zero, caiu")
    ax.set_title("Segurança: 14 crimes do Anuário")
    ax.legend(frameon=False, loc="upper right", fontsize=12)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    salvar(fig, "08_seguranca_14_crimes.png", "Anuário Brasileiro de Segurança Pública 2019, 2023 e 2026")


def obras():
    o = R["c7_obras"]["pct"]
    fig, ax = novo()
    xs = ["Diagnóstico\n2018", "ago/2022", "abr/2025", "abr/2026\n(carteira nova)"]
    vs = [o["2018"], o["2022"], o["2025"], o["2026"]]
    cores = [COR["base"], COR["flavio"], COR["lula"], "#CCCCCC"]
    ax.bar(xs, vs, color=cores)
    for i, v in enumerate(vs):
        ax.text(i, v + 1, br(v) + "%", ha="center", fontweight="bold")
    ax.set_ylim(0, 60); ax.set_ylabel("Obras federais paralisadas (% do total)")
    ax.set_title("Obras federais paralisadas (TCU)")
    fig.text(0.01, 0.055, "Em 2026 o TCU trocou a carteira (entraram e saíram milhares de obras); não se compara com 2025.", fontsize=12, color="#333333")
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    salvar(fig, "09_obras_paralisadas.png", "TCU (diagnóstico de 2018 e Painel de Obras Paralisadas), Gazeta do Povo")


if __name__ == "__main__":
    notas_por_tema(); criterios(); mercado(); divida(); historicos(); stf(); robustez(); crimes(); obras()
    print(sorted(p.name for p in FIG.glob("*.png")))
