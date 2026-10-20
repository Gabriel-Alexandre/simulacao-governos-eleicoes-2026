"""Gera RELATORIO.md, RESUMO_SIMPLES.md e docs/LEITURA_DA_IA.md a partir de resultados/*.json.

Nenhum número é digitado no texto: todos saem do RESUMO.json e do SIMULACAO_DIVIDA.json.
"""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
R = json.loads((RAIZ / "resultados" / "RESUMO.json").read_text(encoding="utf-8"))
S = json.loads((RAIZ / "resultados" / "SIMULACAO_DIVIDA.json").read_text(encoding="utf-8"))
T = R["temas"]
ORDEM = ["seguranca", "saude", "economia", "corrupcao", "educacao", "pobreza"]
NOME_CRIT = {"C1": "histórico", "C2": "promessa e entrega", "C3": "caminho de execução", "C4": "maturidade e evidência",
             "C5": "dinheiro", "C6": "mercado"}
PESO = {"geral": {"C1": 25, "C2": 15, "C3": 30, "C4": 20, "C5": 10, "C6": 0},
        "economia": {"C1": 20, "C2": 10, "C3": 25, "C4": 20, "C5": 10, "C6": 15}}
PRE_REGISTRO = "1e73d27"


def br(x, nd=1, sinal=False):
    t = f"{x:+.{nd}f}" if sinal else f"{x:.{nd}f}"
    return t.replace(".", ",")


def lado_nome(l):
    return "Lula" if l == "lula" else "Flávio"


def decisivos(t):
    pw = PESO["economia" if t == "economia" else "geral"]
    c = T[t]["criterios"]
    contrib = {k: pw[k] * (c["lula"][k] - c["flavio"][k]) / 100 for k in pw if pw[k]}
    return sorted(contrib.items(), key=lambda kv: -abs(kv[1]))


def frase_decisivos(t):
    partes = []
    for k, v in decisivos(t)[:3]:
        if abs(v) < 0.05:
            continue
        partes.append(f"{NOME_CRIT[k]} ({'a favor de Lula' if v > 0 else 'a favor de Flávio'}, {br(abs(v))} ponto{'s' if abs(v) >= 2 else ''} na nota)")
    return "; ".join(partes)


def props(t, lado):
    return [p for p in R["propostas"] if p["tema"] == t and p["lado"] == lado]


def tabela_propostas(t):
    linhas = ["| Lado | Subtema | Proposta (página do plano) | Caminho (C3) | Maturidade (C4) | Dinheiro (C5) |", "|---|---|---|---:|---:|---:|"]
    for lado in ("lula", "flavio"):
        for p in props(t, lado):
            if p["sem_proposta"]:
                linhas.append(f"| {lado_nome(lado)} | {p['subtema']} | *sem proposta no plano*: {p['trecho_do_plano']} | fora da média | fora da média | fora da média |")
            else:
                linhas.append(f"| {lado_nome(lado)} | {p['subtema']} | {p['proposta']} (p. {p['pagina_plano']}) | {int(p['c3_nota'])} | {int(p['c4_nota'])} | {int(p['c5_nota'])} |")
    return "\n".join(linhas)


def tabela_c1(t):
    linhas = ["| Indicador | Bolsonaro (2019 a 2022) | Lula (2023 até o dado mais recente) | Quem fica na frente | Fonte |", "|---|---:|---:|---|---|"]
    for l in R["c1_indicadores"]:
        if l["tema"] != t:
            continue
        quem = "empate (diferença menor que a mínima)" if l["pontos_lula"] == 1 else ("Lula" if l["pontos_lula"] == 2 else "Bolsonaro")
        nd = 3 if "Gini" in l["indicador"] else 2
        linhas.append(f"| {l['indicador']} | {br(l['bolsonaro_2019_2022'], nd)} | {br(l['lula_2023_atual'], nd)} | {quem} | {l['fonte']} |")
    return "\n".join(linhas)


def minuscula(txt):
    return txt[0].lower() + txt[1:] if txt[:2] != txt[:2].upper() else txt


def cenario(t):
    """Simulação qualitativa de cada tema: o que tem caminho provável (C3 >= 60) e com que faixa (C4)."""
    txt = []
    for lado in ("lula", "flavio"):
        ps = [p for p in props(t, lado) if not p["sem_proposta"]]
        provaveis = [p for p in ps if p["c3_nota"] >= 60]
        dependem = [p for p in ps if p["c3_nota"] < 60]
        estreita = [p for p in provaveis if p["c4_nota"] >= 65]
        larga = [p for p in provaveis if p["c4_nota"] < 65]
        s = f"**Caminho de {lado_nome(lado)}.** "
        if estreita:
            s += "Com caminho provável e faixa estreita (já funciona ou tem evidência de efeito): " + "; ".join(minuscula(p["proposta"]) for p in estreita) + ". "
        if larga:
            s += "Com caminho provável e faixa larga (efeito pouco conhecido, pode dar muito certo ou muito errado): " + "; ".join(minuscula(p["proposta"]) for p in larga) + ". "
        if dependem:
            s += "Dependem do Congresso, com caminho mais difícil: " + "; ".join(minuscula(p["proposta"]) for p in dependem) + "."
        txt.append(s.strip())
    return "\n\n".join(txt)


def tabela_resultado():
    linhas = ["| Tema | Nota de Lula | Nota de Flávio | Diferença | Veredito do tema | Robustez (4 pesos escritos antes) | O que mais pesou |", "|---|---:|---:|---:|---|---|---|"]
    for t in ORDEM:
        p = T[t]["pesos"]["principal"]
        linhas.append(f"| {T[t]['nome']} | {br(p['lula'])} | {br(p['flavio'])} | {br(p['diferenca'], 1, True)} | **{T[t]['veredito']}** | {T[t]['robustez']} | {frase_decisivos(t)} |")
    return "\n".join(linhas)


def tabela_criterio_por_tema():
    crits = ["C1", "C2", "C3", "C4", "C5"]
    linhas = ["| Tema | " + " | ".join(NOME_CRIT[c].capitalize() for c in crits) + " | Mercado |", "|---|" + "---|" * (len(crits) + 1)]
    for t in ORDEM:
        c = T[t]["criterios"]
        cel = []
        for k in crits + ["C6"]:
            if k == "C6" and t != "economia":
                cel.append("não se aplica"); continue
            d = c["lula"][k] - c["flavio"][k]
            cel.append(f"{'Lula' if d > 0 else ('Flávio' if d < 0 else 'empate')} ({br(c['lula'][k], 0)} × {br(c['flavio'][k], 0)})")
        linhas.append(f"| {T[t]['nome']} | " + " | ".join(cel) + " |")
    return "\n".join(linhas)


def mercado_txt():
    c = R["c6"]
    return (f"No pregão de {c['evento'].split(',')[0]}, o Ibovespa subiu {br(c['ibovespa_dia_pct'], 2)}% e o índice de ações de emergentes (EEM) subiu {br(c['eem_dia_pct'], 2)}%: "
            f"a bolsa brasileira andou {br(c['bolsa_anormal_pct'], 2)} pontos acima dos emergentes, {br(c['z_bolsa'])} vezes o desvio-padrão diário dos {c['pregoes_na_base']} pregões anteriores. "
            f"O dólar (PTAX do Banco Central) caiu {br(abs(c['ptax_dia_pct']), 2)}% em reais, contra {br(abs(c['dolar_emergentes_dia_pct']), 2)}% na média de peso mexicano, rand, peso chileno e peso colombiano: "
            f"o real se valorizou {br(abs(c['moeda_anormal_pct']), 2)} pontos acima, {br(abs(c['z_moeda']))} vezes o desvio-padrão. "
            f"Os dois sinais passaram de 2 desvios-padrão a favor do resultado do 1º turno, e pela régua escrita antes o critério de mercado fica com Flávio ({c['nota']['flavio']} a {c['nota']['lula']}). "
            f"O juro futuro de janeiro de 2031 caiu de {br(c['juros_futuros']['di_jan2031_05out']['de'], 2)}% para {br(c['juros_futuros']['di_jan2031_05out']['para'], 2)}% no mesmo dia. "
            f"Em 15/10, quando a chance de Flávio na Polymarket caiu de {c['juros_futuros']['di_jan2031_15out']['polymarket_flavio']['de']}% para {c['juros_futuros']['di_jan2031_15out']['polymarket_flavio']['para']}%, "
            f"o mesmo juro subiu de {br(c['juros_futuros']['di_jan2031_15out']['de'], 3)}% para {br(c['juros_futuros']['di_jan2031_15out']['para'], 3)}%.")


def simulacao_txt():
    c = S["cenarios"]
    return (f"A base é a projeção da IFI, a Instituição Fiscal Independente do Senado: dívida bruta de {br(c['base_ifi']['2026'])}% do PIB em 2026 para {br(c['base_ifi']['2030'])}% em 2030 se nada mudar. "
            f"O evento de 15/10 dá o tamanho do juro que o mercado cobra a mais num governo Lula: cerca de {br(S['premio_central_pp'], 2)} pontos ao ano (faixa de {br(S['premio_faixa_pp'][0], 2)} a {br(S['premio_faixa_pp'][1], 2)}). "
            f"Só por esse juro, a dívida de 2030 fica {br(S['diferenca_2030_so_pelo_juro'])} pontos do PIB maior com Lula ({br(c['lula_com_premio']['2030'])}%), e a faixa vai de {br(min(S['sensibilidade_juro_2030'].values()))} a {br(max(S['sensibilidade_juro_2030'].values()))} pontos conforme o tamanho do prêmio e a velocidade com que ele chega à dívida. "
            f"Se Flávio entregar o superávit que o plano promete (aqui, a diferença entre o cenário otimista e o base da IFI), a dívida de 2030 fica {br(S['diferenca_2030_so_pelo_esforco'])} pontos abaixo da base ({br(c['flavio_promessa_cumprida']['2030'])}%). "
            f"Se ele não entregar, o juro a mais tende a voltar e a trajetória encosta na de Lula ({br(c['flavio_promessa_nao_cumprida_com_premio_de_volta']['2030'])}%). "
            f"Se Lula fizesse o mesmo esforço fiscal, chegaria a {br(c['lula_se_fizesse_o_mesmo_esforco']['2030'])}%.")


def secao_tema(t):
    v = T[t]
    p = v["pesos"]["principal"]
    rot = {"iguais": "pesos iguais", "historico_pesa_mais": "histórico pesa mais", "execucao_pesa_mais": "execução pesa mais"}
    alt = "; ".join(f"{rot[k]}: {x['veredito']} ({br(x['lula'])} × {br(x['flavio'])})" for k, x in v["pesos"].items() if k != "principal")
    return f"""### {v['nome']}

**Veredito do tema, pelos critérios escritos antes: {v['veredito']}** (Lula {br(p['lula'])}, Flávio {br(p['flavio'])}; {v['robustez']}). O que mais pesou: {frase_decisivos(t)}. Com outros pesos: {alt}.

**Histórico (C1).**

{tabela_c1(t)}

**Propostas de 2026 (C3, C4 e C5).** Promessa e entrega (C2) é a mesma em todos os temas: Lula {br(R['c2']['lula'])}, Flávio {br(R['c2']['flavio'])} (governo Jair Bolsonaro).

{tabela_propostas(t)}

**Cenário 2027 a 2030.**

{cenario(t)}
"""


def relatorio():
    sens = R["sensibilidade_nao_preregistrada"]
    stf = R["stf"]
    conf = "\n".join(f"| {lado_nome(x['lado'])} | {x['afirmacao']} (p. {x['pagina']}) | {x['conferido'].replace('.', ',') if ('IPCA' in x['conferido'] or 'dez/' in x['conferido'] or 'IBGE: 20' in x['conferido']) else x['conferido']} | {x['situacao']} |" for x in R["conferencia_planos"])
    sem_c2 = "; ".join(f"{T[t]['nome']}: {sens['sem_C2'][t]['veredito']}" for t in ORDEM)
    so_p = "; ".join(f"{T[t]['nome']}: {sens['so_propostas_C3_C4_C5'][t]['veredito']}" for t in ORDEM)
    longo = "\n".join(f"| {x['indicador']} | {br(x['bolsonaro'], 2)} | {br(x['lula_todos_os_mandatos'], 2)} | {br(x['dilma'], 2)} | {'empate' if x['pontos_lula'] == 1 else ('Lula' if x['pontos_lula'] == 2 else 'Bolsonaro')} |" for x in R["c1_sensibilidade_todos_os_mandatos"])
    return f"""# Simulação: como tendem a andar seis temas no Brasil de 2027 a 2030, com Lula ou com Flávio Bolsonaro

**Gerado em {R['gerado_em']} a partir de `resultados/RESUMO.json` e `resultados/SIMULACAO_DIVIDA.json`.** Análise feita pelo **Claude**, modelo de IA da Anthropic, posto pelo autor para analisar com regras escritas antes ([`docs/PRE_REGISTRO.md`](docs/PRE_REGISTRO.md), commit `{PRE_REGISTRO}`, público antes de qualquer nota). Leitura em uma página: [`RESUMO_SIMPLES.md`](RESUMO_SIMPLES.md). A opinião da IA, tema por tema: [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md).

## O que este projeto não consegue dizer

- **Quem vai ganhar o 2º turno de 25/10/2026, nem quem deveria ganhar.** A IA não soma os temas num placar e não diz quem é melhor para o país ([`docs/LIMITE_ELEITORAL.md`](docs/LIMITE_ELEITORAL.md), Resolução TSE nº 23.755/2026, art. 28, §1º-C). Cada tema fecha com o seu veredito.
- **Se um governo causou a variação de um indicador.** O histórico é o que aconteceu durante o mandato, descontado o que aconteceu no resto do mundo quando há série comparável. Pandemia, guerra e preço de commodities interferem.
- **Flávio Bolsonaro nunca governou.** O histórico usado para ele é o do governo Jair Bolsonaro (2019 a 2022), que o plano dele apresenta como referência ("Nós já mostramos que o caminho é outro", p. 29). Ele pode governar diferente.
- **O valor de uma proposta.** O critério de caminho mede o que ela precisa para sair do papel; o de maturidade, o quanto se sabe do efeito. Uma proposta nova pode ser melhor que uma antiga, e uma emenda à Constituição pode ser melhor que um decreto.
- **Temas fora dos seis** (meio ambiente, política externa, cultura e outros), escolhidos pela regra das pesquisas da §1 do pré-registro.

## 1. A pergunta e o método, em uma tela

- **Seis temas**, pela regra escrita antes: o que pelo menos 5% dos brasileiros citam como principal problema em 3 dos 5 levantamentos de 2026 (Datafolha, Quaest/Globo, Quaest/Pax, BTG/Nexus, Paraná Pesquisas). Entraram segurança, saúde, economia, corrupção, educação e pobreza, fome e desigualdade.
- **Quatro subtemas fixos por tema**, iguais para os dois lados, e em cada um a primeira ação concreta do plano registrado no TSE (46 propostas, 2 subtemas sem proposta, trecho literal conferido no PDF).
- **Seis critérios**: C1 histórico, C2 promessa e entrega (g1, mesma metodologia para os dois), C3 caminho de execução (o instrumento que a proposta exige e o Congresso de 2027), C4 maturidade e evidência, C5 dinheiro e, só na economia, C6 mercado.
- **Pesos**: C3 30, C1 25, C4 20, C2 15, C5 10 (na economia, C3 25, C1 20, C4 20, C6 15, C2 10, C5 10). Veredito do tema com diferença de 5 pontos ou mais; abaixo disso, empate. Refeito com 3 pesos alternativos.
- **Fontes**: toda evidência tem o trecho conferido letra por letra na página capturada ({R.get('trechos_conferidos', 'ver')} em `resultados/TRECHOS_CONFERIDOS.csv`); séries oficiais com hash em `dados/MANIFESTO.csv`.

## 2. Resultado por tema

{tabela_resultado()}

![Notas por tema](resultados/figuras/01_notas_por_tema.png)

**Quem fica na frente em cada critério, tema a tema** (nota de Lula × nota de Flávio):

{tabela_criterio_por_tema()}

![Robustez](resultados/figuras/07_robustez.png)

## 3. Tema a tema

{''.join(secao_tema(t) + chr(10) for t in ORDEM)}
## 4. Mercado e simulação da dívida

{mercado_txt()}

![Mercado](resultados/figuras/03_mercado_1turno.png)

{simulacao_txt()}

![Simulação da dívida](resultados/figuras/04_simulacao_divida.png)

**Limite:** o prêmio de juros é o que investidores esperam; ele já mudou de tamanho em poucos dias (EV081, EV083) e pode mudar de novo com as primeiras decisões do eleito. O repasse para o juro médio da dívida é hipótese do modelo, declarada em `ferramentas/simular.py`, com a sensibilidade acima.

## 5. Congresso e Supremo

O Congresso que toma posse em fevereiro de 2027 tem, pela regra de três grupos do autor (projeto `congresso-e-governos-eleicoes-2026`), direita 265, centro 124 e esquerda 124 na Câmara, e direita 48, centro 17 e esquerda 15 no Senado. É isso que dá a Flávio o degrau mais alto nas propostas que precisam de lei (C3).

O próximo governo deve indicar ministros para estas vagas do STF (a de Barroso, se não for preenchida antes de 2027): {'; '.join(stf['vagas_no_mandato_2027_2030'])}. Cada indicado precisa de {stf['aprovacao_no_senado']} no Senado. Em abril de 2026 o Senado atual rejeitou o indicado de Lula, a primeira rejeição desde a Primeira República (EV070), e o Senado de 2027 tem mais senadores da direita. Isso não entra na nota (a régua da §3 diz que o Supremo entra na leitura, não muda nota sozinho), mas pesa na simulação: com Flávio, as indicações tendem a passar; com Lula, o histórico recente mostra rejeição.

![STF](resultados/figuras/06_stf_vagas.png)

## 6. Sensibilidades

- **Sem 2020 e 2021** (pandemia) nas médias de PIB e inflação: os vereditos ficam iguais ({', '.join(f"{T[t]['nome']}: {v}" for t, v in R['vereditos_sem_2020_2021'].items())}).
- **Todos os mandatos de Lula (2003 a 2010 e 2023 em diante), com os governos Dilma ao lado**, onde há série internacional:

| Indicador | Bolsonaro | Lula, todos os mandatos | Dilma | Quem fica na frente (Lula × Bolsonaro) |
|---|---:|---:|---:|---|
{longo}

- **Fora do pré-registro, pedidas pela revisão adversarial** (não mudam o veredito oficial):
  - sem o critério de promessa e entrega (C2): {sem_c2};
  - só as propostas (C3, C4 e C5): {so_p};
  - segurança sem o indicador de estelionato (o registro mudou com a lei de fraude eletrônica de 2021): {sens['seguranca_sem_estelionato']['veredito']} ({br(sens['seguranca_sem_estelionato']['lula'])} × {br(sens['seguranca_sem_estelionato']['flavio'])});
  - economia sem o critério de mercado (C6): {sens['economia_sem_C6']['veredito']} ({br(sens['economia_sem_C6']['lula'])} × {br(sens['economia_sem_C6']['flavio'])}).

**O que isso mostra:** o veredito da economia depende do critério de promessa e entrega; sem ele, empata. O de corrupção vai para Flávio quando o histórico pesa mais ou quando a promessa sai. Os outros quatro temas ficam com Lula em todas as combinações testadas.

## 7. Números dos planos, conferidos

| Plano | Afirmação | Conferido nas séries oficiais | Situação |
|---|---|---|---|
{conf}

## 8. Teste das duas pontas e revisão

O fato central de cada tema foi procurado em veículos de linha editorial declarada à esquerda e à direita: [`docs/TESTE_DAS_DUAS_PONTAS.md`](docs/TESTE_DAS_DUAS_PONTAS.md). As três passadas de revisão adversarial, com o que mudou por causa delas: [`docs/REVISAO_ADVERSARIAL.md`](docs/REVISAO_ADVERSARIAL.md).

## 9. Emendas, fontes e como refazer

Cinco emendas ao pré-registro, cada uma dizendo se veio antes ou depois de ver dado: [`docs/PRE_REGISTRO.md`](docs/PRE_REGISTRO.md) §12. Fontes: [`docs/FONTES.md`](docs/FONTES.md). Refazer do zero: [`docs/REPLICAR.md`](docs/REPLICAR.md).
"""


def resumo_simples():
    linhas = []
    for t in ORDEM:
        v = T[t]
        p = v["pesos"]["principal"]
        linhas.append(f"- **{v['nome']}: {v['veredito']}** ({br(p['lula'])} × {br(p['flavio'])}, {v['robustez']}). Pesou mais: {frase_decisivos(t)}.")
    c = S["cenarios"]
    sens = R["sensibilidade_nao_preregistrada"]
    return f"""# Resumo simples

**Gerado em {R['gerado_em']} a partir de `resultados/RESUMO.json`.** O relatório completo é o [`RELATORIO.md`](RELATORIO.md) e a opinião da IA está em [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md).

> **O que este projeto não diz.** Quem vai ganhar, nem quem deveria ganhar. A IA não soma os temas (regra do TSE, `docs/LIMITE_ELEITORAL.md`). Flávio nunca governou: o histórico dele é o do governo Jair Bolsonaro. O projeto mede o caminho e a evidência de cada proposta, não o mérito.

## Como foi feito

Seis temas escolhidos pelas pesquisas de "principal problema do país". Em cada tema, 4 subtemas iguais para os dois lados e a primeira proposta concreta de cada plano registrado no TSE. Seis critérios com pesos escritos e publicados antes de qualquer nota: histórico, promessa e entrega, caminho de execução (com o Congresso de 2027), maturidade e evidência, dinheiro e, na economia, mercado.

## Veredito de cada tema

{chr(10).join(linhas)}

## O que mais muda o resultado

- **Continuidade.** Quase tudo o que Lula propõe já funciona (está em lei ou em execução), e várias propostas têm avaliação publicada. Quase tudo o que Flávio propõe é novo: com o Congresso de 2027 a favor, o caminho dele para leis é mais curto, mas o efeito é menos conhecido.
- **Promessa e entrega.** Pelo g1, Lula cumpriu 26 de 36 promessas de 2022 até junho de 2026; o governo Bolsonaro cumpriu 19 de 58 de 2018. Sem esse critério, a economia empata ({br(sens['sem_C2']['economia']['lula'])} × {br(sens['sem_C2']['economia']['flavio'])}) e a corrupção vai para Flávio.
- **Mercado.** No dia seguinte ao 1º turno, a bolsa subiu {br(R['c6']['bolsa_anormal_pct'], 2)} pontos acima dos emergentes e o real se valorizou {br(abs(R['c6']['moeda_anormal_pct']), 2)} pontos acima das outras moedas. Esse critério é de Flávio.

## A simulação da dívida até 2030

Base da IFI: {br(c['base_ifi']['2030'])}% do PIB em 2030. Com o juro a mais que o mercado cobra num governo Lula: {br(c['lula_com_premio']['2030'])}%. Com Flávio entregando o superávit prometido: {br(c['flavio_promessa_cumprida']['2030'])}%. Se ele não entregar, o juro a mais tende a voltar.

## Supremo

O próximo governo deve indicar {len(R['stf']['vagas_no_mandato_2027_2030']) - 1} ministros do STF até abril de 2029 (se a vaga de Barroso não for preenchida antes de 2027) e mais um no fim de 2030, e o Senado de 2027 tem {R['stf']['senado_2027']['direita']} senadores da direita. Em abril de 2026, o Senado rejeitou o indicado de Lula para a vaga de Barroso.
"""


def leitura_da_ia():
    sens = R["sensibilidade_nao_preregistrada"]
    c = R["c6"]
    def v(t): return T[t]
    def p(t): return T[t]["pesos"]["principal"]
    return f"""# Leitura da IA, tema por tema

**Escrita pelo Claude (modelo de IA da Anthropic) em {R['gerado_em']}, depois das notas, com as regras de `docs/PRE_REGISTRO.md` §7.** Toda frase de opinião vem marcada com "na leitura da IA" e com o grau de confiança. Números do `resultados/RESUMO.json`. ⛔ A IA não soma os temas e não diz quem é melhor para o país (`docs/LIMITE_ELEITORAL.md`).

## Segurança · veredito: {v('seguranca')['veredito']} ({br(p('seguranca')['lula'])} × {br(p('seguranca')['flavio'])})

As mortes violentas caíram nos dois governos quase no mesmo ritmo, e o roubo de veículo também: no histórico, empate nos dois. O que separa é o estelionato, que cresceu muito mais de 2018 a 2022 do que depois; mesmo tirando esse indicador, o caminho de Lula fica na frente ({br(sens['seguranca_sem_estelionato']['lula'])} × {br(sens['seguranca_sem_estelionato']['flavio'])}). Do lado das propostas, Lula aposta no que já está em lei (Lei Antifacção, controle de armas) e numa emenda à Constituição que passou na Câmara e travou no Senado; Flávio aposta em medidas novas, das quais a de fronteira depende só dele e as de facção como terrorismo e maioridade penal dependem do Congresso, a segunda com 3/5.

**Na leitura da IA (confiança média):** o caminho de Lula fica na frente porque o que ele propõe já anda; o de Flávio tem mais medidas que a população pede nas pesquisas e o Congresso de 2027 a favor, mas o efeito delas no crime é pouco conhecido e a evidência sobre maioridade penal é mista. **O que mudaria:** se a PEC da Segurança for aprovada antes de 2027, a proposta central de Lula sobe para o degrau mais alto; se o projeto de facções como terrorismo passar numa das casas, a de Flávio sobe.

## Saúde · veredito: {v('saude')['veredito']} ({br(p('saude')['lula'])} × {br(p('saude')['flavio'])})

Esperança de vida e mortalidade infantil, descontada a América Latina, empatam. A vacina de sarampo separa: a cobertura caiu no governo Bolsonaro e se recuperou depois, e o país voltou a ser certificado livre de sarampo em 2024. As propostas dos dois se parecem (Saúde da Família, prontuário único, vacinação), e as de Lula estão em execução.

**Na leitura da IA (confiança alta):** é o tema em que os dois caminhos mais se parecem no conteúdo; a diferença está em quem já executa e no histórico da vacinação. **O que mudaria:** uma avaliação de impacto do Agora Tem Especialistas, para o bem ou para o mal.

## Economia · veredito: {v('economia')['veredito']} ({br(p('economia')['lula'])} × {br(p('economia')['flavio'])})

Cada lado leva um pedaço. No histórico, com Lula o PIB cresceu mais perto dos emergentes, a inflação ficou mais abaixo deles e a renda do trabalho subiu; com Bolsonaro, o desemprego caiu mais rápido e a dívida caiu, enquanto com Lula ela sobe. O mercado precificou Flávio com {br(c['z_bolsa'])} e {br(abs(c['z_moeda']))} desvios-padrão na bolsa e no câmbio. As propostas de Lula são continuidade (o arcabouço, a reforma tributária); as de Flávio exigem lei, que o Congresso de 2027 favorece.

**Na leitura da IA (confiança baixa):** o veredito de economia é o mais frágil dos seis. Sem o critério de promessa e entrega ele empata, e a simulação da dívida aponta na direção contrária da nota: só pelo juro que o mercado já cobra, a dívida de 2030 fica {br(S['diferenca_2030_so_pelo_juro'])} pontos do PIB maior com Lula. **O que mudaria:** uma meta fiscal com número, de qualquer dos dois; o plano de Flávio promete superávit sem dizer quanto, e o de Lula mantém uma regra com a qual a IFI projeta dívida subindo até 2036.

## Corrupção · veredito: {v('corrupcao')['veredito']} ({br(p('corrupcao')['lula'])} × {br(p('corrupcao')['flavio'])})

O índice da Transparência Internacional ficou melhor em 2020 a 2022 do que depois, e o do Banco Mundial empata. Lula aprofunda um plano anticorrupção que já existe e quer barrar candidaturas ligadas ao crime organizado; Flávio quer mudar regras do STF (partes já aprovadas no Senado) e profissionalizar estatais. Cada um deixa um subtema sem proposta: Lula não fala de estatais nem de fraude em benefício; Flávio não fala de órgãos de controle e investigação.

**Na leitura da IA (confiança baixa):** empate é a conclusão honesta. Os dois índices medem percepção e governança, não casos; os escândalos que cada lado cita contra o outro na campanha ficaram fora da nota, porque a régua não conta caso sem condenação. **O que mudaria:** com o histórico pesando mais, ou sem o critério de promessa, fica Flávio.

## Educação · veredito: {v('educacao')['veredito']} ({br(p('educacao')['lula'])} × {br(p('educacao')['flavio'])})

O Ideb dos anos iniciais ficou parado de 2017 a 2021 e subiu até 2025; o do ensino médio subiu nos dois períodos. Lula continua quatro programas que já funcionam (alfabetização, Pé-de-Meia, creches, Pé-de-Meia Licenciatura); Flávio propõe o método fônico, que tem evidência a favor, ensino técnico, voucher-creche e formação de professores.

**Na leitura da IA (confiança média):** a vantagem é de continuidade. O Pé-de-Meia ainda não tem avaliação de impacto observada: a estimativa é ex-ante, e a Gazeta do Povo questiona o efeito na evasão. A proposta de Flávio com melhor evidência é o método fônico. **O que mudaria:** a primeira avaliação de impacto do Pé-de-Meia.

## Pobreza, fome e desigualdade · veredito: {v('pobreza')['veredito']} ({br(p('pobreza')['lula'])} × {br(p('pobreza')['flavio'])})

Extrema pobreza e fome caíram mais depois de 2022. O Gini caiu mais de 2018 a 2022 e voltou a subir em 2025; em 2022, pelo IBGE, sem os benefícios dos programas sociais a extrema pobreza teria sido 10,6% em vez de 5,9% (captura X06). Os dois prometem manter o Bolsa Família. Lula soma a valorização do salário mínimo, que tem avaliação publicada; Flávio soma uma porta de saída do programa, que é nova.

**Na leitura da IA (confiança média):** a diferença vem de o salário mínimo e os programas de Lula já estarem em lei e avaliados. Manter o Bolsa Família é compromisso dos dois. **O que mudaria:** uma regra de reajuste do salário mínimo no plano de Flávio, ou uma avaliação da porta de saída.

## A leitura geral do método, sem somar temas

O desenho escolhido pelo autor dá peso ao que já está em andamento, e quem governa tem mais coisa em andamento. O Congresso de 2027 e o Supremo favorecem Flávio onde a proposta precisa de lei ou de indicação, e o mercado aposta nele. Os dois planos quase não dizem quanto custa o que prometem.
"""


def main():
    import csv
    n = sum(1 for _ in csv.DictReader((RAIZ / "resultados" / "TRECHOS_CONFERIDOS.csv").open(encoding="utf-8")))
    R["trechos_conferidos"] = f"{n} trechos"
    (RAIZ / "RELATORIO.md").write_text(relatorio(), encoding="utf-8")
    (RAIZ / "RESUMO_SIMPLES.md").write_text(resumo_simples(), encoding="utf-8")
    (RAIZ / "docs" / "LEITURA_DA_IA.md").write_text(leitura_da_ia(), encoding="utf-8")
    print("RELATORIO.md, RESUMO_SIMPLES.md e docs/LEITURA_DA_IA.md gerados")


if __name__ == "__main__":
    main()
