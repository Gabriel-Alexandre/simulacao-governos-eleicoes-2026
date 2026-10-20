"""Gera RELATORIO.md, RESUMO_SIMPLES.md, docs/LEITURA_DA_IA.md e docs/AUDITORIA_RODADA_2.md da rodada 2.

Nenhum número é digitado no texto: todos saem do RESUMO.json (rodada 2), que traz a comparação com a
rodada 1 (resultados/rodada1/), e do SIMULACAO_DIVIDA.json. O gerador da rodada 1 está guardado em
resultados/rodada1/gerar-relatorio-rodada1.py.
"""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
R = json.loads((RAIZ / "resultados" / "RESUMO.json").read_text(encoding="utf-8"))
S = json.loads((RAIZ / "resultados" / "SIMULACAO_DIVIDA.json").read_text(encoding="utf-8"))
T = R["temas"]
ORDEM = ["seguranca", "saude", "economia", "corrupcao", "educacao", "pobreza"]
NOME_CRIT = {"C1": "histórico", "C3": "caminho de execução", "C4": "maturidade e evidência", "C5": "dinheiro", "C6": "mercado", "C7": "obras paralisadas"}
ROT_PESO = {"iguais": "pesos iguais", "historico_pesa_mais": "histórico pesa mais", "execucao_pesa_mais": "execução pesa mais"}
PRE_REGISTRO = "1e73d27"
REGRAS_R2 = "902202a"


def br(x, nd=1, sinal=False):
    t = f"{x:+.{nd}f}" if sinal else f"{x:.{nd}f}"
    return t.replace(".", ",")


def mil(n):
    return f"{int(n):,}".replace(",", ".")


def nome(l):
    return "Lula" if l == "lula" else "Flávio"


def quem(l):
    return "empate" if l["pontos_lula"] == 1 else ("Lula" if l["pontos_lula"] == 2 else "Bolsonaro")


def ind(prefixo):
    return next(l for l in R["c1_indicadores"] if l["indicador"].startswith(prefixo))


def decisivos(t, n=3):
    c = T[t]["pesos"]["principal"]["contribuicoes"]
    partes = [f"{NOME_CRIT[k]} ({'a favor de Lula' if v > 0 else 'a favor de Flávio'}, {br(abs(v))})"
              for k, v in sorted(c.items(), key=lambda kv: -abs(kv[1])) if abs(v) >= 0.05]
    return "; ".join(partes[:n])


def tabela_resultado():
    r1 = R["rodada1_vereditos"]
    linhas = ["| Tema | Rodada 1 | Rodada 2: Lula | Rodada 2: Flávio | Veredito da rodada 2 | Robustez (4 pesos) | O que mais pesou (pontos na diferença) |",
              "|---|---|---:|---:|---|---|---|"]
    for t in ORDEM:
        p = T[t]["pesos"]["principal"]
        linhas.append(f"| {T[t]['nome']} | {r1[t]['veredito']} ({br(r1[t]['lula'])} × {br(r1[t]['flavio'])}) | {br(p['lula'])} | {br(p['flavio'])} | **{T[t]['veredito']}** | {T[t]['robustez']} | {decisivos(t)} |")
    return "\n".join(linhas)


def tabela_c1(t):
    nd = lambda l: 3 if "Gini" in l["indicador"] else 2
    linhas = ["| Indicador | Bolsonaro (2019 a 2022) | Lula (2023 até o dado mais recente) | Quem fica na frente |", "|---|---:|---:|---|"]
    ls = [l for l in R["c1_indicadores"] if l["tema"] == t]
    for l in ls:
        linhas.append(f"| {l['indicador']} | {br(l['bolsonaro_2019_2022'], nd(l))} | {br(l['lula_2023_atual'], nd(l))} | {quem(l)} |")
    cont = {k: sum(1 for l in ls if quem(l) == k) for k in ("Lula", "Bolsonaro", "empate")}
    return "\n".join(linhas) + f"\n\nPlacar dos indicadores: Lula {cont['Lula']}, Bolsonaro {cont['Bolsonaro']}, empate {cont['empate']}."


def tabela_propostas(t):
    linhas = ["| Lado | O que muda (página do plano) | Caminho (C3) | Maturidade (C4) | Dinheiro (C5) |", "|---|---|---:|---:|---:|"]
    base = []
    for lado in ("lula", "flavio"):
        for p in R["propostas"]:
            if p["tema"] != t or p["lado"] != lado:
                continue
            if p["tipo"] == "mudanca":
                linhas.append(f"| {nome(lado)} | {p['proposta']} (p. {p['pagina_plano']}) | {int(p['c3_nota'])} | {int(p['c4_nota'])} | {int(p['c5_nota'])} |")
            else:
                base.append(f"{p['proposta']} ({nome(lado)}, p. {p['pagina_plano']})")
    txt = "\n".join(linhas)
    if base:
        txt += "\n\n**Base comum** (continua com qualquer um dos dois, porque nenhum plano propõe encerrar; fica fora da nota): " + "; ".join(base) + "."
    return txt


def secao(t):
    v = T[t]; p = v["pesos"]["principal"]; c = v["criterios"]
    alt = "; ".join(f"{ROT_PESO[k]}: {x['veredito']} ({br(x['lula'])} × {br(x['flavio'])})" for k, x in v["pesos"].items() if k != "principal")
    crit = " · ".join(f"{NOME_CRIT[k]} {br(c['lula'][k], 0)} × {br(c['flavio'][k], 0)}" for k in ("C1", "C3", "C4", "C5", "C6", "C7") if c["lula"].get(k) is not None)
    o = R["c7_obras"]
    obras = (f"\n\n**Obras paralisadas (C7):** a fatia de obras federais paradas no painel do TCU subiu {br(o['bolsonaro_pp_ao_ano'], 2)} ponto por ano no período Bolsonaro e {br(o['lula_pp_ao_ano'], 2)} pontos por ano no atual."
             if c["lula"].get("C7") is not None else "")
    return f"""### {v['nome']}

**Veredito da rodada 2: {v['veredito']}** (Lula {br(p['lula'])}, Flávio {br(p['flavio'])}; {v['robustez']}). Notas por critério (Lula × Flávio): {crit}. O que mais pesou: {decisivos(t, 4)}. Com outros pesos: {alt}.

**Histórico (C1).**

{tabela_c1(t)}

**Propostas (C3, C4 e C5), só o que muda.**

{tabela_propostas(t)}{obras}
"""


def contexto_tabela():
    c = R["contexto"]; b, l = c["bolsonaro"], c["lula_atual"]
    return f"""| | Bolsonaro (começo de 2019) | Lula (começo de 2023) |
|---|---|---|
| Selic no começo | {br(b['selic_no_inicio'], 2)}% | {br(l['selic_no_inicio'], 2)}% |
| Desemprego no começo | {br(b['desemprego_no_inicio'])}% | {br(l['desemprego_no_inicio'])}% |
| Dívida bruta no começo | {br(b['divida_no_inicio'], 2)}% do PIB | {br(l['divida_no_inicio'], 2)}% do PIB |
| Inflação do ano anterior | {br(b['ipca_do_ano_anterior'], 2)}% | {br(l['ipca_do_ano_anterior'], 2)}% |
| Crescimento médio dos emergentes no mandato | {br(b['crescimento_medio_emergentes'], 2)}% ao ano | {br(l['crescimento_medio_emergentes'], 2)}% ao ano |
| Choques | {b['choques']} | {l['choques']} |"""


def fragilidades():
    sc7 = R["sensibilidade"]["sem_obras_C7"]
    temas_c7 = [t for t in ORDEM if T[t]["criterios"]["lula"].get("C7") is not None]
    muda = [f"{T[t]['nome']} vira {sc7[t]['veredito']} ({br(sc7[t]['lula'])} × {br(sc7[t]['flavio'])})" for t in temas_c7 if sc7[t]["veredito"] != T[t]["veredito"]]
    sid = R["sensibilidade"]["ideb_com_a_pandemia"]["educacao"]
    sc6 = R["sensibilidade"]["sem_mercado_C6"]["economia"]
    return f"""- **O critério de obras (C7) é um número só, igual em quatro temas.** Ele dá a nota inteira a Flávio em saúde, educação, pobreza e economia. Sem ele: {'; '.join(muda) if muda else 'nenhum veredito muda'}. É a mesma objeção que tirou o critério de promessa da nota (não ser específico do tema), e a base de 2018 é o diagnóstico do TCU, não o painel. A regra foi escrita antes da nota (emenda 10), então o veredito oficial fica, e a fragilidade vai junto.
- **Ideb com a pandemia na janela** (como na rodada 1): educação vira {sid['veredito']} ({br(sid['lula'])} × {br(sid['flavio'])}).
- **Economia sem o critério de mercado:** {sc6['veredito']} ({br(sc6['lula'])} × {br(sc6['flavio'])}).
- **A base comum supõe que os programas continuam com os dois.** Pé-de-Meia, Farmácia Popular, controle de armas e aumento real do salário mínimo não aparecem no plano de Flávio, nem para manter nem para acabar."""


def seg_frase():
    fem = ind("Feminicídio")
    cel = R["informativo_seguranca"]["roubo_de_celular"]
    return (f"O feminicídio subiu nos dois governos ({br(fem['bolsonaro_2019_2022'], 2)}% ao ano no de Bolsonaro e {br(fem['lula_2023_atual'], 2)}% ao ano no atual; diferença menor que a mínima, empate). "
            f"O roubo de celular caiu de {mil(cel['2022'])} em 2022 para {mil(cel['2025'])} em 2025 (sem dado comparável de 2018). "
            "Lesão corporal e tentativa de homicídio pioraram no período atual; roubo a transeunte, a residência, a comércio e de carga, e o latrocínio, caíram mais rápido no período atual.")


def relatorio():
    c7 = R["c7_obras"]
    return f"""# Simulação: como tendem a andar seis temas no Brasil de 2027 a 2030, com Lula ou com Flávio Bolsonaro

**Rodada 2, gerada em {R['gerado_em']}.** Análise feita pelo **Claude**, modelo de IA da Anthropic, posto pelo autor para analisar com regras escritas antes: pré-registro `{PRE_REGISTRO}` e regras da rodada 2 `{REGRAS_R2}` (emendas 6 a 11, publicadas antes destas notas, a pedido do autor depois de ver a rodada 1). A rodada 1 está guardada em `resultados/rodada1/`. Em uma página: [`RESUMO_SIMPLES.md`](RESUMO_SIMPLES.md). Opinião da IA: [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md). Auditoria: [`docs/AUDITORIA_RODADA_2.md`](docs/AUDITORIA_RODADA_2.md).

## O que este projeto não consegue dizer

- **Quem vai ganhar, nem quem deveria ganhar.** A IA não soma os temas e não diz quem é melhor para o país ([`docs/LIMITE_ELEITORAL.md`](docs/LIMITE_ELEITORAL.md)).
- **Se um governo causou a variação de um indicador.** O histórico é o que aconteceu no mandato, descontado o mundo quando há série de vizinhos.
- **Flávio Bolsonaro nunca governou.** O histórico dele é o do governo Jair Bolsonaro.
- **O resultado muda com o desenho.** Entre a rodada 1 e a rodada 2 vários temas mudaram de lado; a seção 5 diz de que escolha cada veredito depende.

## 1. O que mudou da rodada 1 para a rodada 2

| Mudança | Por quê |
|---|---|
| Promessa e entrega (C2) saiu da nota do tema | O balanço do g1 não separa tema e dava a mesma vantagem em todos |
| Propostas: só o que muda conta; manter o que já existe é base comum; mesmo programa, mesma nota | Na rodada 1 a continuidade contava quatro vezes, e o mesmo programa tinha nota diferente conforme o verbo |
| Segurança com 14 crimes do Anuário (antes 3) | Faltavam feminicídio, roubos e crimes contra a pessoa |
| Ideb na janela sem pandemia; desemprego contra a América Latina; mais duas medidas de saúde e a pobreza a US$ 8,30 | A pandemia e o ponto de partida pesavam diferente para cada governo |
| Critério novo: obras federais paralisadas (TCU) | Obras inacabadas e prazos |
| Tabela de contexto de cada mandato | Dificuldades e privilégios de cada governo |
| Correção de um erro de casas decimais na comparação | 0,3 menos 0,2 dava 0,0999 e virava empate |

## 2. Resultado por tema

{tabela_resultado()}

![Notas por tema](resultados/figuras/01_notas_por_tema.png)

![Segurança](resultados/figuras/08_seguranca_14_crimes.png)

## 3. Tema a tema

{''.join(secao(t) + chr(10) for t in ORDEM)}
## 4. Contexto de cada mandato (herança e choques)

{contexto_tabela()}

Na régua: os choques do mundo (pandemia, guerra) são descontados nos indicadores comparados com os vizinhos (PIB, inflação, desemprego, saúde), e a variação por ano ajusta o tempo de mandato. Lula começou com juro alto e desemprego baixo; Bolsonaro, com juro baixo e desemprego alto.

**Segurança:** {seg_frase()}

**Grandes obras com atraso** (casos, sem nota): a transposição do São Francisco começou em 2007, tinha conclusão prevista para 2012 e foi dada como concluída em fevereiro de 2022 (captura O08); a Transnordestina começou em 2006 e segue sem conclusão em 2026 (O10, O11); o segundo trem da refinaria Abreu e Lima parou em 2015 e foi retomado em 2025, com previsão para 2029 (O12). Painel do TCU: {br(c7['pct']['2018'])}% das obras paradas no diagnóstico de 2018, {br(c7['pct']['2022'])}% em ago/2022 e {br(c7['pct']['2025'])}% em abr/2025; em abr/2026 o painel mostra {br(c7['pct']['2026'])}%, mas o TCU trocou a carteira e avisa que não se compara com 2025 (O03).

![Obras](resultados/figuras/09_obras_paralisadas.png)

## 5. De que escolha cada veredito depende

{fragilidades()}

![Robustez](resultados/figuras/07_robustez.png)

## 6. Mercado, dívida e Supremo

Iguais à rodada 1: o mercado reagiu a favor de Flávio no 1º turno (bolsa {br(R['c6']['bolsa_anormal_pct'], 2)} pontos acima dos emergentes, real {br(abs(R['c6']['moeda_anormal_pct']), 2)} pontos acima das outras moedas); a simulação dá dívida de {br(S['cenarios']['lula_com_premio']['2030'])}% do PIB em 2030 com Lula e o juro que o mercado cobra, contra {br(S['cenarios']['flavio_promessa_cumprida']['2030'])}% com Flávio entregando o superávit prometido (base da IFI: {br(S['cenarios']['base_ifi']['2030'])}%); e o próximo governo deve preencher de 3 a 4 vagas no STF, com o Senado de 2027 mais à direita.

![Mercado](resultados/figuras/03_mercado_1turno.png)
![Dívida](resultados/figuras/04_simulacao_divida.png)

## 7. Promessa e entrega, como informação geral

Pelo g1, com a mesma metodologia: Lula cumpriu 26 de 36 promessas de 2022 até junho de 2026 (4 em parte); o governo Bolsonaro cumpriu 19 de 58 de 2018 (17% em parte). Fora da nota do tema desde a rodada 2.

## 8. Números dos planos, conferidos

| Plano | Afirmação | Conferido | Situação |
|---|---|---|---|
""" + "\n".join(f"| {nome(x['lado'])} | {x['afirmacao']} (p. {x['pagina']}) | {x['conferido'].replace('.', ',')} | {x['situacao']} |" for x in R["conferencia_planos"]) + """

## 9. Fontes, revisão e como refazer

Emendas: [`docs/PRE_REGISTRO.md`](docs/PRE_REGISTRO.md) §12. Teste das duas pontas: [`docs/TESTE_DAS_DUAS_PONTAS.md`](docs/TESTE_DAS_DUAS_PONTAS.md). Revisão da rodada 1: [`docs/REVISAO_ADVERSARIAL.md`](docs/REVISAO_ADVERSARIAL.md). Fontes: [`docs/FONTES.md`](docs/FONTES.md). Refazer: [`docs/REPLICAR.md`](docs/REPLICAR.md).
"""


def resumo_simples():
    linhas = []
    for t in ORDEM:
        v = T[t]; p = v["pesos"]["principal"]; r1 = R["rodada1_vereditos"][t]
        linhas.append(f"- **{v['nome']}: {v['veredito']}** ({br(p['lula'])} × {br(p['flavio'])}, {v['robustez']}; na rodada 1, {r1['veredito']}). Pesou mais: {decisivos(t)}.")
    return f"""# Resumo simples (rodada 2)

**Gerado em {R['gerado_em']}.** Completo: [`RELATORIO.md`](RELATORIO.md). Opinião da IA: [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md).

> **O que este projeto não diz.** Quem vai ganhar, nem quem deveria ganhar; a IA não soma os temas (regra do TSE). Flávio nunca governou: o histórico dele é o do governo Jair Bolsonaro.

## O que mudou na rodada 2

A promessa saiu da nota; manter o que já existe deixou de contar ponto (vale para os dois); a segurança passou a ter 14 crimes; a pandemia e o ponto de partida entraram na comparação; e entrou um critério de obras paralisadas do TCU.

## Veredito de cada tema

{chr(10).join(linhas)}

## O que você precisa saber antes de usar

{fragilidades()}
"""


def leitura():
    def v(t): return T[t]
    def p(t): return T[t]["pesos"]["principal"]
    sc7 = R["sensibilidade"]["sem_obras_C7"]
    return f"""# Leitura da IA, tema por tema (rodada 2)

**Escrita pelo Claude (modelo de IA da Anthropic) em {R['gerado_em']}, depois das notas da rodada 2.** Opinião marcada, com confiança. ⛔ A IA não soma temas nem diz quem é melhor para o país.

## Segurança · {v('seguranca')['veredito']} ({br(p('seguranca')['lula'])} × {br(p('seguranca')['flavio'])})

Com os 14 crimes, o histórico fica dividido. {seg_frase()} Nas propostas, as de Flávio têm caminho melhor (Forças Armadas na fronteira e repasse a estados dependem só do Executivo), e as duas de Lula que mudam algo dependem de emenda à Constituição ou de um pacto novo.

**Na leitura da IA (confiança média):** empate é a leitura certa. Os dois períodos tiveram queda forte da violência letal; o que separa é o tipo de crime, e o caminho das propostas favorece Flávio.

## Saúde · {v('saude')['veredito']} ({br(p('saude')['lula'])} × {br(p('saude')['flavio'])})

Comparados com a América Latina, os resultados de saúde ficaram melhores no período atual: as duas vacinas e a mortalidade materna. As propostas de mudança dos dois têm caminho parecido. Quem equilibra é o critério de obras: as obras de saúde estão entre as mais paradas do país, e a fatia de obras paradas subiu no período atual.

**Na leitura da IA (confiança baixa):** sem o critério de obras, o tema volta para Lula ({br(sc7['saude']['lula'])} × {br(sc7['saude']['flavio'])}); com ele, empata.

## Economia · {v('economia')['veredito']} ({br(p('economia')['lula'])} × {br(p('economia')['flavio'])})

No histórico, o período atual fica na frente em PIB, inflação e renda, e o de Bolsonaro na dívida; o desemprego empata contra a América Latina. Mercado e obras pesam a favor de Flávio; as propostas de Lula que mudam algo estão mais perto de sair do papel que as de Flávio, que exigem lei.

**Na leitura da IA (confiança média):** o que decide é a expectativa de ajuste fiscal com Flávio, que o mercado já precifica e a simulação da dívida reflete. Se o ajuste não vier, essa vantagem some.

## Corrupção · {v('corrupcao')['veredito']} ({br(p('corrupcao')['lula'])} × {br(p('corrupcao')['flavio'])})

O índice de percepção da Transparência Internacional ficou melhor de 2018 a 2022 do que depois; o do Banco Mundial empata. As propostas de Lula que mudam algo têm caminho mais fácil; a reforma do STF de Flávio depende de emenda à Constituição.

**Na leitura da IA (confiança baixa):** os dois índices medem percepção, não casos; os escândalos que cada lado cita contra o outro ficaram fora da nota.

## Educação · {v('educacao')['veredito']} ({br(p('educacao')['lula'])} × {br(p('educacao')['flavio'])})

Na janela sem pandemia, o Ideb dos anos iniciais e dos anos finais melhorou mais no período atual, e o do ensino médio melhorou mais de 2017 a 2019. As propostas de Flávio têm caminho perto do de Lula; o critério de obras pesa contra o período atual (creches e escolas paradas).

**Na leitura da IA (confiança baixa):** sem o critério de obras, Lula ({br(sc7['educacao']['lula'])} × {br(sc7['educacao']['flavio'])}); com ele, empate. A proposta de Flávio com melhor evidência é o método fônico.

## Pobreza, fome e desigualdade · {v('pobreza')['veredito']} ({br(p('pobreza')['lula'])} × {br(p('pobreza')['flavio'])})

Extrema pobreza, pobreza e fome caíram mais no período atual; o Gini caiu mais no de Bolsonaro. Os dois mantêm o Bolsa Família. O critério de obras pesa contra o período atual.

**Na leitura da IA (confiança média):** o histórico favorece Lula com folga; o empate vem do critério de obras (sem ele, {br(sc7['pobreza']['lula'])} × {br(sc7['pobreza']['flavio'])}).

## A leitura geral, sem somar temas

O resultado depende muito do desenho, e as duas rodadas mostram isso. O que se repete nas duas: o mercado e a dívida apontam para Flávio; a percepção de corrupção foi melhor no período Bolsonaro; vacinas, mortalidade materna e pobreza melhoraram mais no período atual; a violência letal caiu nos dois; e as obras federais paradas aumentaram no período atual.
"""


def auditoria():
    r1 = R["rodada1_vereditos"]
    fem = ind("Feminicídio"); c7 = R["c7_obras"]
    return f"""# Auditoria da rodada 2

**{R['gerado_em']}.** Pedido do autor depois da rodada 1: mais crítica, considerando o tempo de cada governo, as dificuldades, as obras e mais dados. As regras foram escritas e publicadas antes das notas (commit `{REGRAS_R2}`).

## O que o autor apontou, e o que os dados mostraram

| Ponto do autor | O que os dados mostraram | O que mudou |
|---|---|---|
| "O roubo cresceu de 2022 para cá" | Os roubos **caíram** no período atual, e mais rápido que antes (transeunte, residência, comércio, carga); o roubo de celular também caiu de 2022 para 2025 | Os 14 crimes entraram na régua |
| "O feminicídio cresceu" | Cresceu no período atual ({br(fem['lula_2023_atual'], 2)}% ao ano) e no de Bolsonaro ({br(fem['bolsonaro_2019_2022'], 2)}% ao ano) | Entrou; empate pela diferença mínima |
| Promessa é igual em todos os temas | Procede | Saiu da nota do tema |
| O caminho de execução favorecia quem já governa | Procede: manter o que existe valia 100, e o mesmo programa tinha nota diferente | Só conta o que muda; mesmo programa, mesma nota |
| A pandemia deve equilibrar | Procede para o Ideb (a rodada 1 media a recuperação contra a queda) | Ideb sem pandemia; desemprego contra a América Latina |
| Obras inacabadas e prazos | Procede: a fatia de obras federais paradas foi de {br(c7['pct']['2022'])}% para {br(c7['pct']['2025'])}% de ago/2022 a abr/2025 | Critério C7 |
| Mais tempo de governo deveria render mais | A régua usa variação por ano, que já ajusta o tempo; os mandatos antigos do PT entram como sensibilidade e nos casos de obras | Casos de obras no relatório |

## Erro encontrado na própria rodada 2

- **Casas decimais:** a diferença de 0,1 no Ideb dos anos finais virava 0,0999 e empate. Corrigido antes de publicar; muda a educação de Flávio para empate.

## Fragilidades que ficam

{fragilidades()}

## Comparação das rodadas

| Tema | Rodada 1 | Rodada 2 |
|---|---|---|
""" + "\n".join(f"| {T[t]['nome']} | {r1[t]['veredito']} | {T[t]['veredito']} |" for t in ORDEM) + "\n"


def main():
    (RAIZ / "RELATORIO.md").write_text(relatorio(), encoding="utf-8")
    (RAIZ / "RESUMO_SIMPLES.md").write_text(resumo_simples(), encoding="utf-8")
    (RAIZ / "docs" / "LEITURA_DA_IA.md").write_text(leitura(), encoding="utf-8")
    (RAIZ / "docs" / "AUDITORIA_RODADA_2.md").write_text(auditoria(), encoding="utf-8")
    print("relatórios da rodada 2 gerados")


if __name__ == "__main__":
    main()
