# Simulação dos governos 2027 a 2030: Lula ou Flávio Bolsonaro

Projeto aberto que simula como tendem a andar **seis temas** no Brasil de 2027 a 2030 com cada um dos dois candidatos do 2º turno de 2026, a partir de dados, do histórico de cada grupo no governo, das propostas registradas no TSE e do Congresso que toma posse em 2027. Os critérios, os pesos e a régua de cada nota foram escritos e publicados **antes** de qualquer nota (commit `1e73d27`).

> ⛔ **O projeto não diz quem vai ganhar, nem quem deveria ganhar.** A IA dá nota por critério e diz qual caminho fica na frente **em cada tema**; ela não soma os temas e não diz quem é melhor para o país ([`docs/LIMITE_ELEITORAL.md`](docs/LIMITE_ELEITORAL.md), Res. TSE nº 23.755/2026, art. 28, §1º-C). Flávio Bolsonaro nunca governou: o histórico usado para ele é o do governo Jair Bolsonaro, que o plano dele apresenta como referência.

## Por onde começar

| Quero | Leia |
|---|---|
| o resultado em uma página | [`RESUMO_SIMPLES.md`](RESUMO_SIMPLES.md) |
| tudo, com tabelas, fontes e limites | [`RELATORIO.md`](RELATORIO.md) |
| a opinião da IA, tema por tema | [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md) |
| as regras escritas antes e as emendas | [`docs/PRE_REGISTRO.md`](docs/PRE_REGISTRO.md) |
| as objeções de cada lado e o que mudou por causa delas | [`docs/REVISAO_ADVERSARIAL.md`](docs/REVISAO_ADVERSARIAL.md) |
| se a esquerda e a direita contam os mesmos fatos | [`docs/TESTE_DAS_DUAS_PONTAS.md`](docs/TESTE_DAS_DUAS_PONTAS.md) |
| de onde veio cada número | [`docs/FONTES.md`](docs/FONTES.md), [`dados/evidencias/`](dados/evidencias/), [`resultados/TRECHOS_CONFERIDOS.csv`](resultados/TRECHOS_CONFERIDOS.csv) |
| refazer tudo | [`docs/REPLICAR.md`](docs/REPLICAR.md) |
| os gráficos (1920x1080) | [`resultados/figuras/`](resultados/figuras/) |

## O método em seis linhas

1. **Temas** escolhidos pelas pesquisas de "principal problema do país" de 2026: segurança, saúde, economia, corrupção, educação e pobreza, fome e desigualdade.
2. **Quatro subtemas fixos por tema**, iguais para os dois lados, e a primeira ação concreta de cada plano registrado no TSE em cada subtema (46 propostas, trecho literal conferido no PDF).
3. **Seis critérios:** histórico (indicadores do mandato, descontado o mundo quando há série), promessa e entrega (g1, mesma metodologia), caminho de execução (o instrumento que a proposta exige e o Congresso de 2027), maturidade e evidência, dinheiro e, na economia, o que o mercado precificou.
4. **Veredito por tema** com diferença de 5 pontos ou mais, refeito com quatro pesos; abaixo disso, empate.
5. **Simulação:** a dívida bruta até 2030 pela equação da dívida, sobre a base da Instituição Fiscal Independente, com o prêmio de juros medido no mercado e o superávit prometido; nos outros temas, o que tem caminho provável e com que faixa de incerteza.
6. **Validação:** todo trecho conferido na página capturada, toda série com hash, revisão em três passadas e teste das duas pontas.

## Estrutura

```
docs/            pré-registro, limite eleitoral, leitura da IA, revisão, fontes, replicar
dados/capturas/  texto extraído de cada página e PDF (no git)
dados/series/    séries numéricas (Banco Central, IBGE, FMI, Banco Mundial, mercado)
dados/evidencias/ propostas, notas, evidências e valores, com o trecho e a fonte
ferramentas/     capturar, coletar, conferir, calcular, simular, gráficos, relatório
resultados/      RESUMO.json, SIMULACAO_DIVIDA.json, TRECHOS_CONFERIDOS.csv, figuras/
```

Análise feita pelo Claude, modelo de IA da Anthropic, com o processo montado e dirigido pelo autor, Gabriel Alexandre.
