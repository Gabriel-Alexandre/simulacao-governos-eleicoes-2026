# Revisão adversarial (três passadas)

**Feita pelo Claude em 20/out/2026, depois das notas e antes do texto final, como manda `PRE_REGISTRO.md` §9.** Cada achado diz o que foi feito por causa dele. Os números citados estão em `resultados/RESUMO.json`.

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
