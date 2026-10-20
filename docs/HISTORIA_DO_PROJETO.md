# A história do projeto: como cada resultado foi construído

**Escrita em 20/out/2026, no fim da rodada 2.** Este arquivo conta, na ordem em que aconteceu, o que o autor pediu, o que a IA fez, o que deu errado, o que mudou e por quê. As horas são de Brasília e saem do `git log` e do registro da conversa. O que é regra está no [`PRE_REGISTRO.md`](PRE_REGISTRO.md); o que é método, no [`METODO.md`](METODO.md); o resultado, no [`RELATORIO.md`](../RELATORIO.md).

> **Quem fez o quê, em uma linha.** O autor, Gabriel Alexandre, pediu o projeto, definiu o objetivo (um resultado por tema, sem ficar em cima do muro e sem vencedor geral), reprovou a rodada 1 e disse o que faltava. O Claude, modelo de IA da Anthropic, escreveu as regras, coletou os dados, deu as notas, escreveu o código e o relatório, e revisou o próprio trabalho.

---

## 1. A linha do tempo

| Hora (20/out) | Quem | O que aconteceu | Prova |
|---|---|---|---|
| 09:00 | autor | Pede o projeto do vídeo longo 13: simular como fica o Brasil com Lula e com Flávio nos principais problemas, com histórico, propostas reais, promessa e entrega, caminho de execução (Congresso de 2027 e STF), fontes cruzadas entre esquerda e direita, um ponto por tema com o motivo, e repositório público | registro da conversa |
| 09:12 | IA | **Pré-registro em commit antes de qualquer nota:** 6 temas pela regra das pesquisas, 6 critérios, pesos, a régua de 5 pontos para veredito, 3 pesos alternativos e o desenho da simulação | `1e73d27` |
| 09:23 | IA | Emendas 1 a 3, antes de qualquer nota: propostas por subtema fixo, índice do Banco Mundial em nota de 0 a 100, roubo de veículo no lugar de "roubos" | `0b3ce1c` |
| 09:23 | IA | Emenda 3 corrigida para declarar que os valores de roubo de veículo e estelionato tinham sido vistos ao localizar as tabelas | `24e3341` |
| 09:30 | IA | Emenda 4 e a seleção das propostas congelada: 46 propostas (24 subtemas, 2 lados, 2 subtemas sem proposta), cada trecho conferido no PDF do plano | `f3701f6` |
| 10:03 | IA | **Rodada 1 completa:** notas, histórico, mercado, simulação da dívida, STF, revisão adversarial em 3 passadas, teste das duas pontas e relatório gerado por script | `c98060a` |
| 10:44 | autor | *"eu tô achando o resultado muito suspeito com esse nível de diferença"*: pede o porquê de Lula ficar na frente em cada tema e uma dupla verificação | registro da conversa |
| 10:44 a 10:56 | IA | Decompõe a nota de cada tema critério por critério e mostra de onde vinha a vantagem (seção 3) | registro da conversa |
| 10:56 | autor | Pede a rodada 2, *"extremamente mais criteriosa"*: os roubos e o feminicídio, promessa igual em todo tema, o caminho de execução não pode favorecer quem governou mais, a pandemia, o tempo de cada governo, as obras inacabadas e os prazos (cita a transposição do São Francisco), as dívidas, as dificuldades e os privilégios de cada um | registro da conversa |
| 11:02 | IA | **Regras da rodada 2 em commit antes das notas:** emendas 6 a 11; a rodada 1 guardada em `resultados/rodada1/` | `902202a` |
| 11:16 | IA | **Rodada 2 completa:** 14 crimes, Ideb sem pandemia, base comum fora da nota, obras do TCU, promessa como informação | `c02fa5c` |
| 11:26 | autor | Aprova (*"agora me parece que ficou um pouco mais adequado com a realidade"*) e pede que a história do projeto fique documentada | registro da conversa |

---

## 2. A rodada 1: o que foi feito

1. **Os temas não foram escolhidos pela IA nem pelo autor.** Entrou o tema citado por 5% ou mais como principal problema do país em pelo menos 3 de 5 pesquisas de 2026 (Datafolha, duas da Quaest, Nexus e Paraná Pesquisas). Saíram 6: segurança, saúde, economia, corrupção, educação e pobreza, fome e desigualdade.
2. **As propostas saíram dos planos registrados no TSE**, por 4 subtemas fixos por tema, iguais para os dois lados (emenda 1), para que os dois fossem medidos nas mesmas perguntas. Em cada subtema, a primeira ação concreta do plano. Cada trecho foi conferido letra por letra no PDF capturado.
3. **O histórico de cada um** foi medido pela variação por ano no mandato: o atual de Lula (2023 até o dado mais recente) e o governo Jair Bolsonaro (2019 a 2022) para Flávio, que nunca governou e apresenta aquele governo como referência. Quando havia série de fora, a variação foi descontada dos vizinhos (América Latina) ou dos emergentes, para tirar o que aconteceu no mundo inteiro.
4. **Seis critérios por tema:** histórico (C1), promessa e entrega pelo g1 (C2), caminho de execução com o Congresso de 2027 (C3), maturidade e evidência (C4), dinheiro (C5) e, na economia, o mercado no dia seguinte ao 1º turno (C6).
5. **Resultado da rodada 1:** Lula na frente em segurança (61,2 × 42,7), saúde (76,1 × 55,0), economia (58,5 × 51,6), educação (74,7 × 47,5) e pobreza (74,8 × 50,3); corrupção empatada (51,8 × 54,5). O relatório da rodada 1 está em [`resultados/rodada1/RELATORIO_RODADA1.md`](../resultados/rodada1/RELATORIO_RODADA1.md).

---

## 3. Por que a rodada 1 favorecia quem já governava (a decomposição pedida pelo autor)

Quando o autor achou a diferença suspeita, a IA abriu a nota de cada tema critério por critério. O que apareceu:

| O que a decomposição mostrou | Por que isso era um defeito de desenho |
|---|---|
| **A continuidade contava em 4 critérios.** O pedido original dizia que *"aquilo que já está em andamento é a favor do Lula"*, e a IA aplicou isso no caminho de execução (manter o que existe valia 100), na maturidade (programa funcionando valia mais que proposta nova), no dinheiro (programa com orçamento) e, por tabela, na promessa | a mesma vantagem entrava 4 vezes na mesma nota |
| **O mesmo programa tinha nota diferente conforme o verbo.** Saúde da Família e prontuário único apareciam nos dois planos; quem escrevia *manter* tirava 100, quem escrevia *ampliar* tirava menos | a régua dependia da redação do plano, não do programa |
| **A promessa e entrega (C2) era o mesmo número em todos os temas** (o g1 não separa por tema), e dava a Lula cerca de 5,5 pontos na nota de cada tema (3,6 na economia, onde pesava menos) | um número geral decidindo 6 vereditos |
| **A segurança tinha só 3 indicadores** (mortes violentas, roubo de veículo e estelionato) e o estelionato tinha subido muito no período Bolsonaro, em parte por mudança de registro | faltavam feminicídio, roubos e crimes contra a pessoa |
| **O Ideb da janela de Lula começava em 2021**, ano medido com as escolas na pandemia, então media a recuperação | a pandemia pesava diferente para cada governo |
| **Não havia nada sobre obras e prazos** | o autor citou a transposição do São Francisco |

O autor também trouxe uma premissa: *"o roubo e a taxa de feminicídio cresceu de 2022 para cá"*. A rodada 2 pôs os 14 crimes do Anuário na régua, a favor e contra cada lado, e mostrou o que os dados dizem (seção 5).

---

## 4. A rodada 2: o que mudou, com as regras escritas antes das notas

As 6 emendas foram escritas e publicadas às 11:02, antes de qualquer nota da rodada 2 (`902202a`). Cada uma diz que veio depois de ver a rodada 1, a pedido do autor.

| Emenda | O que mudou | O que o autor tinha pedido |
|---|---|---|
| 6 | Promessa e entrega saiu da nota do tema e virou informação geral; os pesos foram redistribuídos | *"deveria ser 0 a 0"* |
| 7 | Caminho, maturidade e dinheiro medem **só o que muda**. Programa que os dois mantêm é **base comum** (continua com qualquer um) e fica fora da média; o mesmo programa tem o mesmo degrau dos dois lados | *"você não pode fazer tudo somar a favor do Lula pelo fato dele ter tido mais tempo de governo"* |
| 8 | Segurança com os **14 crimes** que o Anuário publica com a mesma definição em 2018, 2022 e 2025 | os roubos e o feminicídio |
| 9 | Ideb na janela **sem pandemia** para os dois (2017 a 2019 contra 2023 a 2025), desemprego contra a América Latina, mais vacina, mortalidade materna e pobreza a US$ 8,30 | *"a pandemia [...] deve ser um fator de equilíbrio"* |
| 10 | Critério novo **C7, obras federais paralisadas** (painel do TCU), e as grandes obras com atraso como casos | *"o número de obras incompletas, o número de prazos não concluídos"* |
| 11 | Tabela de **contexto de cada mandato** (juro, desemprego, dívida e inflação no começo; choques) | *"as dificuldades e privilégios que cada governo teve"* |

**Os pesos alternativos da rodada 2** (todos iguais, histórico pesa mais, execução pesa mais) seguem a lógica da §5 do pré-registro, sem o C2 e com o C7. ⚠️ Eles foram escritos no código junto do cálculo (`ferramentas/calcular-rodada2.py`, commit `c02fa5c`), e não no commit das regras; isso está declarado na emenda 12.

**Sobre o tempo de governo:** o autor pediu que *"como ele teve mais tempo de governo [...] deveria ter feito bem mais coisa"*. A régua já mede tudo por ano de mandato (variação anual), o que ajusta o tempo. Os mandatos antigos do PT (2003 a 2010) e as obras que atravessaram governos entram como sensibilidade e como casos, sem nota, porque o pré-registro escolheu o mandato mais recente como o mais perto das regras, do Congresso e da economia de 2027.

---

## 5. O que os dados mostraram nos pontos que o autor levantou

| O autor disse | O dado | Fonte |
|---|---|---|
| o roubo cresceu de 2022 para cá | **caiu**, e mais rápido que no período anterior: roubo a transeunte −18,3% ao ano, a residência −18,8%, a comércio −18,6%, de carga −15,3%, latrocínio −13,1%; o roubo de celular foi de 508.335 em 2022 para 308.723 em 2025 | Anuário FBSP 2023 e 2026 |
| o feminicídio cresceu | **cresceu nos dois governos**: 4,48% ao ano no de Bolsonaro e 3,02% ao ano no atual | Anuário FBSP 2019, 2023 e 2026 |
| (não citado) | **pioraram no período atual:** lesão corporal dolosa (+6,1% ao ano) e tentativa de homicídio (+1,6%) | idem |
| as obras inacabadas | a fatia de obras federais paradas foi de 38,5% (ago/2022) para 50,7% (abr/2025) | painel do TCU |
| a transposição do São Francisco | começou em 2007, no governo Lula, tinha conclusão prevista para 2012, passou por Dilma e Temer, e os eixos Norte e Leste foram dados como concluídos em fevereiro de 2022, no governo Bolsonaro, com partes que já estavam 92,5% prontas desde anos anteriores | capturas O08 e O09 |

---

## 6. Os erros que apareceram no caminho, e quem pegou

| Erro | Quem pegou | Como foi resolvido |
|---|---|---|
| A rodada 1 contava a continuidade 4 vezes | **o autor**, pelo resultado (*"muito suspeito"*); a IA achou a causa ao decompor | rodada 2, emendas 6 e 7 |
| A emenda 3 não dizia que os valores de roubo de veículo e estelionato tinham sido vistos | a IA, relendo | commit `24e3341`, 12 segundos depois do commit das emendas |
| A API do FMI recusava o pedido com o cabeçalho de navegador | a IA, no erro 403 | pedido sem cabeçalho para o FMI |
| Páginas do Planalto saíam com acento quebrado | a IA | detecção da codificação da página |
| As datas das moedas de fora no Yahoo vinham desalinhadas | a IA, no estudo de evento | o real pela PTAX do Banco Central e as outras moedas pela última cotação |
| Na rodada 2, 0,3 menos 0,2 dava 0,0999 e virava empate no Ideb dos anos finais | a IA, conferindo a tabela antes de publicar | arredondamento na comparação; a educação foi de Flávio para empate |
| O relatório dizia que o 2º trem da refinaria Abreu e Lima foi retomado em 2025 com previsão para 2029; a captura O12 diz que a Petrobras decidiu retomar em 2023, com operação prevista na época para 2027 | a IA, relendo as capturas para o roteiro do vídeo, depois da rodada 2 | frase corrigida no gerador do relatório; o caso não tinha nota |

---

## 7. O resultado de cada rodada

| Tema | Rodada 1 | Rodada 2 (vigente) | Firmeza na rodada 2 |
|---|---|---|---|
| Segurança | Lula | empate (45,7 × 45,4) | depende do peso |
| Saúde | Lula | empate (65,5 × 63,3) | depende do peso |
| Economia | Lula | **Flávio** (49,0 × 55,5) | firme |
| Corrupção | empate | **Flávio** (49,5 × 56,8) | depende do peso |
| Educação | Lula | empate (64,7 × 61,3) | firme |
| Pobreza, fome e desigualdade | Lula | empate (61,8 × 58,2) | firme |

**O que "firme" quer dizer.** O veredito foi refeito com 4 jeitos de pesar os critérios: os pesos escritos antes, todos iguais, o histórico pesando mais e a execução pesando mais. *Firme* é quando o resultado dá o mesmo nos 4; *depende do peso* é quando muda em pelo menos um. Exemplo: a segurança empata com os pesos escritos antes, vai para Lula quando o histórico pesa mais e para Flávio quando a execução pesa mais. A firmeza mede só os pesos: a fragilidade do critério de obras (seção 8) é outra coisa e está ao lado.

---

## 8. O que ainda é frágil, e fica dito

- **O critério de obras é um número só, igual em quatro temas.** Sem ele, saúde, educação e pobreza vão para Lula e a economia empata. É a mesma objeção que tirou a promessa da nota. O veredito oficial fica, porque a regra foi escrita antes da nota, e a fragilidade vai junto.
- **Com o Ideb dos anos de pandemia**, a educação iria para Flávio.
- **Sem o critério de mercado**, a economia iria para Lula.
- **A base comum supõe que os programas continuam com os dois.** Pé-de-Meia, Farmácia Popular, controle de armas e aumento real do salário mínimo não aparecem no plano de Flávio, nem para manter nem para acabar.

A revisão das duas rodadas está em [`REVISAO_ADVERSARIAL.md`](REVISAO_ADVERSARIAL.md) e [`AUDITORIA_RODADA_2.md`](AUDITORIA_RODADA_2.md).

---

## 9. O que não mudou entre as rodadas

O mercado e a dívida apontam para Flávio; a percepção de corrupção foi melhor no período Bolsonaro; vacinas, mortalidade materna e pobreza melhoraram mais no período atual; a violência letal caiu nos dois; e a fatia de obras federais paradas subiu no período atual. Nas duas rodadas, a IA não somou os temas (Res. TSE 23.755/2026, art. 28, §1º-C; [`LIMITE_ELEITORAL.md`](LIMITE_ELEITORAL.md)).
