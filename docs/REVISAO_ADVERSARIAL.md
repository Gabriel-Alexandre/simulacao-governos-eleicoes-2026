# Revisão adversarial (três passadas, nas duas rodadas)

**Feita pelo Claude em 20/out/2026, depois das notas e antes do texto final, como manda `PRE_REGISTRO.md` §9.** Cada achado diz o que foi feito por causa dele. As três primeiras passadas são da **rodada 1** (números em `resultados/rodada1/RESUMO.json`); a revisão da **rodada 2** está no fim, com os números de `resultados/RESUMO.json`. A ordem dos fatos: [`HISTORIA_DO_PROJETO.md`](HISTORIA_DO_PROJETO.md).

# Rodada 1

## Passada 1 · o leitor que mais desconfiaria de uma conclusão favorável a Lula

| Objeção | Procede? | O que foi feito |
|---|---|---|
| O critério de caminho (C3) dá 100 a quem só "mantém" o que existe, e quem governa tem mais coisa para manter | Procede como desenho, e o desenho foi pedido pelo autor ("aquilo que já está em andamento é a favor do Lula") | A regra vale para os dois: Flávio também recebe 100 quando promete manter (vacinação, Bolsa Família). O relatório diz no topo que C3 mede o que a proposta exige para sair do papel, não o mérito |
| A nota de promessa e entrega (C2) usa o governo do pai para o filho | Procede | Escrito no topo do relatório. Sensibilidade fora do pré-registro: sem C2, a economia empata e a corrupção vai para Flávio |
| O g1 avaliou Lula em 3,5 anos e Bolsonaro em 4, com listas de tamanhos diferentes; outros levantamentos dão números mais próximos (Folha: 28% de 103 em metade do mandato de Lula; Metrópoles: 24,5% de 53 em 3 anos de Bolsonaro) | Procede em parte: o g1 é o único com a mesma metodologia para os dois | Limite escrito no pré-registro (§3, C2) e no relatório; os outros levantamentos ficam como conferência de sentido |
| O estelionato de 2018 a 2022 cresceu também porque mudou o registro (fraude eletrônica virou crime em 2021 e o registro migrou para o digital) | Procede | Sensibilidade sem o indicador: a segurança continua com Lula (57,0 × 46,8) |
| O mandato atual de Lula pega anos de recuperação depois da pandemia | Procede em parte | O histórico desconta os emergentes e a América Latina quando há série; sem 2020 e 2021, nenhum veredito muda |
| Vários fatos de instrumento têm uma fonte só (o próprio plano) | Procede | Marcados como fonte única (emenda 5); nenhum deles decide um veredito sozinho |

## Passada 2 · o leitor que mais desconfiaria de uma conclusão favorável a Flávio

| Objeção | Procede? | O que foi feito |
|---|---|---|
| O critério de mercado (C6) mede o que investidores esperam, não a renda, o emprego ou o bem-estar | Procede | Escrito na régua antes (§3, C6) e repetido no relatório. Sem C6, a economia fica com Lula por mais (68,9 × 43,1) |
| O índice da Transparência Internacional mede percepção; a própria organização chamou o orçamento secreto do governo Bolsonaro de esquema de corrupção institucionalizada | Procede em parte | O histórico de corrupção usa também o índice do Banco Mundial (empate). Casos, de qualquer lado, ficaram fora da nota porque a régua não conta caso sem condenação |
| A queda da dívida de 2018 a 2022 teve ajuda da inflação alta, que infla o PIB nominal | Procede | Escrito na leitura da economia; o indicador é o pré-registrado e fica |
| O Gini caiu em 2022 no ano em que o auxílio foi ampliado | Procede como coincidência | O relatório cita o IBGE (sem os programas sociais, a extrema pobreza de 2022 teria sido 10,6% em vez de 5,9%) sem atribuir causa |
| O prêmio de juros de um único dia (15/10) é frágil para simular quatro anos | Procede | A simulação mostra faixa (1,0 a 2,4 pontos de prêmio; repasse gradual, total e de metade) e diz que o prêmio já mudou em dias |
| A PEC da Segurança passou na Câmara por 487 a 15; tratá-la como "do lado mais longe da maioria" subestima o caminho dela | Procede como limite da régua | A régua foi seguida (degrau 6 mais 1 por já ter passado numa casa); o relatório diz que a votação travou no Senado por causa da emenda da maioridade, não por oposição à PEC |

## Passada 3 · o auditor de método e linguagem

| Teste | Resultado |
|---|---|
| Espelho (com os nomes trocados, a frase seria escrita igual?) | As frases de veredito usam a mesma forma para os dois ("o caminho de X fica na frente em tal tema, pelos critérios escritos antes") |
| Recorte (a frase, recortada, vira anúncio de alguém?) | ⛔ Nenhuma frase soma temas ("fica na frente em N de 6"); a tabela mostra tema por tema e a nota de cada critério. Retirada uma frase do rascunho do resumo que contava temas |
| Lista de palavras proibidas e travessão | conferido por `ferramentas/conferir-linguagem.py` |
| Trechos citados | 100% conferidos na captura por `ferramentas/conferir-trechos.py` |
| Número escrito à mão no relatório | nenhum: o texto sai de `ferramentas/gerar-relatorio.py` |
| Afirmação causal | a régua do texto é "coincide com", "fica na frente pelos critérios"; nenhuma frase diz que um governo causou um indicador |

## O que esta revisão não fez

Não houve leitura humana independente nem as "cinco leituras" separadas (cientista político, economista, estatístico, um leitor de cada lado). Se o autor pedir, o mesmo `RESUMO.json` pode ser lido assim.

# Rodada 2

A rodada 1 passou nas três passadas e mesmo assim o autor achou o resultado suspeito, com razão: a continuidade contava em quatro critérios ([`HISTORIA_DO_PROJETO.md`](HISTORIA_DO_PROJETO.md) §3). A lição para a revisão é que as três passadas olharam frase e fonte, e não a estrutura dos pesos. Na rodada 2, a primeira passada abriu a nota de cada tema critério por critério.

## Passada 1 · o leitor que mais desconfiaria de uma conclusão favorável a Lula

| Objeção | Procede? | O que foi feito |
|---|---|---|
| A maturidade (C4) ainda dá 65 a programa que funciona e 35 a proposta nova, e quem governa tem mais programa funcionando | Procede em parte: é a distinção que o autor pediu (*"aquilo que é extremamente novo ainda é uma possibilidade"*) | Ela conta uma vez só, e só para o que muda; o mesmo programa tem a mesma nota dos dois lados (emenda 7) |
| A queda dos roubos é nacional, começou antes de 2023 e não prova ação do governo federal | Procede | O relatório não atribui causa; a régua é *coincide com*. Os 14 crimes entram a favor e contra os dois |
| A pobreza do período atual herda o benefício ampliado em 2022 (o mesmo ponto da passada 2 da rodada 1) | Procede como contexto | A janela de Bolsonaro termina em 2022 e já contém a ampliação; a régua não atribui causa |

## Passada 2 · o leitor que mais desconfiaria de uma conclusão favorável a Flávio

| Objeção | Procede? | O que foi feito |
|---|---|---|
| O critério de obras (C7) é um número só, igual em quatro temas, como era o C2 que saiu | Procede | Dito no topo do resumo, no relatório e na leitura da IA, com o resultado sem ele (saúde, educação e pobreza vão para Lula, economia empata). O veredito oficial fica, porque a regra foi escrita antes da nota |
| A base de 2018 do C7 é o diagnóstico do TCU (contratos), não o painel | Procede | Escrito junto do número; o ponto de 2026 ficou fora porque o TCU trocou a carteira |
| A base comum supõe que Flávio mantém Pé-de-Meia, Farmácia Popular, controle de armas e o aumento real do salário mínimo, que não estão no plano dele | Procede | Escrito como fragilidade; nenhum dos planos propõe acabar com eles |
| O mercado (C6) mede expectativa de investidor | Procede, como na rodada 1 | Sem o C6, a economia vai para Lula (57,6 × 47,6), escrito no relatório |

## Passada 3 · o auditor de método e linguagem

| Teste | Resultado |
|---|---|
| Erro de conta | 0,3 menos 0,2 dava 0,0999 e virava empate no Ideb; corrigido antes de publicar |
| Os pesos alternativos | escritos no código junto do cálculo, não no commit das regras; declarado na emenda 12 |
| Espelho, recorte, palavras proibidas, travessão, trechos | `conferir-linguagem.py` e `conferir-trechos.py` sem falha; nenhuma frase soma temas |
