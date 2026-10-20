# Pré-registro: temas, critérios, pesos e régua, escritos antes das notas

**Escrito em:** 20/out/2026, em commit antes de qualquer nota. O hash deste commit entra no relatório. Critério mudado depois entra na §12, dizendo se foi antes ou depois de ver a nota.

---

## 0. O que já foi visto antes deste registro (declaração)

Um pré-registro não consegue ser cego à manchete. O que ele garante é que **os temas, os critérios, os pesos e a régua de cada nota estão escritos antes de qualquer nota**. Já foi visto e se declara:

- as pesquisas de "principal problema do país" usadas na §1 (Datafolha 13 e 14/out, Quaest 30/ago a 1º/set e 12 a 15/set, BTG/Nexus 10 a 12/jul, Paraná Pesquisas fev, Ipsos jul);
- a manchete de mercado do dia seguinte ao 1º turno (Ibovespa +7,70% e dólar −4,12% em 05/out, CNN Brasil), ainda sem conferência em série oficial e sem comparação com o mercado de fora;
- a dívida bruta do governo geral de dez/2018 (75,27% do PIB) e de ago/2026 (82,87%), na sonda da API do Banco Central;
- os balanços de promessas do g1 (Bolsonaro, 19 de 58 cumpridas integralmente até 31/12/2022; Lula, 26 de 36 até 30/06/2026), de segunda mão;
- tudo o que os projetos `congresso-e-governos-eleicoes-2026` (Congresso de 2027), `presidente-primeiro-turno-2026` (economia do bolso) e `analise-debates-eleicoes-2026` (propostas do debate da Band, com a régua de exequibilidade) já publicaram;
- manchetes de 15/out de que a PEC do fim da escala 6x1 foi aprovada e de que o Senado aprovou calendário especial para a PEC da Segurança Pública, ainda sem conferência.

**Não foi visto:** nenhuma série dos indicadores da §3 por mandato, nenhuma avaliação de impacto das propostas, nenhum texto dos planos de governo de 2026 além de manchetes, nenhuma nota.

---

## 1. Os temas (regra de entrada)

**Regra:** entra o tema citado por **5% ou mais** como principal problema do país na pesquisa nacional mais recente de 2026 de **pelo menos 3** destes 5 levantamentos de resposta espontânea: Datafolha (13 e 14/out), Quaest/Globo (30/ago a 1º/set), Quaest/Pax (12 a 15/set), BTG/Nexus (10 a 12/jul, soma da 1ª e da 2ª menção) e Paraná Pesquisas (fev). Subtemas de economia (economia, inflação, custo de vida, desemprego, emprego e renda, impostos) somam-se em **Economia**. Pobreza, fome, miséria, desigualdade, problemas sociais e assistência social somam-se em **Pobreza, fome e desigualdade**. A Ipsos (lista estimulada, até 3 escolhas) fica como conferência, fora da regra.

| Tema | Datafolha | Quaest/Globo | Quaest/Pax | Nexus | Paraná | Entra? |
|---|---:|---:|---:|---:|---:|---|
| Segurança e violência | 20 | 31 | 28 | 29 | 22,2 | ✅ 5 de 5 |
| Saúde | 18 | 14 | 15 | 26 | 20,1 | ✅ 5 de 5 |
| Economia (com inflação, desemprego e impostos) | 15+4+3 | 16 | 19+5 | 11+11 | 15,9+9,4 | ✅ 5 de 5 |
| Corrupção | 7 | 14 | 22 | 26 | não listada | ✅ 4 de 5 |
| Educação | 6 | 7 | 5 | 14 | 13,8 | ✅ 5 de 5 |
| Pobreza, fome e desigualdade | 3 | 13 | não listada | 10 | 6,0 | ✅ 3 de 5 |

**Seis temas.** Fontes: capturas `P01` a `P09` em `dados/capturas/`.

---

## 2. Quem é comparado com o quê

- **Lula:** proposta de 2026 = plano registrado no TSE (*Diretrizes para o Programa de Transformação do Brasil*) e falas de campanha com 2 fontes. Histórico principal = **mandato atual, 2023 até o dado mais recente**. Sensibilidade = todos os mandatos dele (2003 a 2010 e 2023 em diante); os governos Dilma (2011 a 2016) ficam como segunda sensibilidade ("grupo político"), nunca na nota principal.
- **Flávio Bolsonaro:** proposta de 2026 = plano registrado no TSE (*Para o Brasil Vencer o Atraso*) e falas de campanha com 2 fontes. **Ele nunca governou**; o histórico é o do **governo Jair Bolsonaro, 2019 a 2022**, que ele apresenta como referência (captura obrigatória dessa referência; se não houver, o histórico entra com o aviso de que é do grupo político, não dele).
- **Por que o mandato mais recente é o principal:** é o mais perto das regras, do Congresso e da economia de 2027; os mandatos de 2003 a 2010 viveram outro ciclo de preço de commodities e outra lei fiscal.

---

## 3. Os critérios e a régua de cada um

Cada tema tem notas de 0 a 100 para cada lado em cada critério. A régua é a mesma para os dois.

### C1 · O que o histórico entregou (resultado)

Para cada indicador da tabela da §3.1: a **variação média por ano** no mandato de cada um (do último dado do mandato anterior ao último dado do mandato), e, quando existe série comparável de fora, a mesma variação **descontada da média da América Latina e Caribe** (ou dos emergentes, para PIB e inflação), para tirar do caminho o que aconteceu no mundo inteiro (a pandemia, a guerra, o preço de commodities). O indicador marcado com ★ usa a versão descontada.

- Por indicador: quem teve a variação melhor fica com 2 e o outro com 0; se a diferença for menor que a **diferença mínima** da tabela, 1 para cada.
- **C1 = média dos indicadores do tema, de 0 a 2, vezes 50.**
- **Sensibilidade da pandemia:** o mesmo cálculo sem 2020 e 2021, quando o indicador tiver dado anual. Se a sensibilidade virar o indicador, isso vai para o relatório.

#### 3.1 Indicadores (escolhidos antes de ver as séries por mandato)

| Tema | Indicador | Melhor é | Fonte 1 | Fonte 2 (conferência do valor do Brasil) | Diferença mínima |
|---|---|---|---|---|---|
| Economia | ★ PIB real, crescimento ao ano, Brasil menos emergentes | maior | FMI WEO | IBGE (SIDRA 6784 ou 5932) | 0,3 p.p. |
| Economia | ★ Inflação ao ano, Brasil menos emergentes | menor | FMI WEO | IBGE/BCB (IPCA, SGS 433) | 0,5 p.p. |
| Economia | Desemprego (PNAD Contínua), variação ao ano | menor | IBGE SIDRA 6381 | BCB SGS 24369 | 0,2 p.p. |
| Economia | Dívida bruta do governo geral (% do PIB), variação ao ano | menor | BCB SGS 13762 | Tesouro/IFI | 0,5 p.p. |
| Economia | Rendimento médio real do trabalho, variação ao ano | maior | IBGE SIDRA 5436 | BCB/IPEA | 0,5% |
| Segurança | Mortes violentas intencionais por 100 mil, variação ao ano | menor | Fórum Brasileiro de Segurança Pública (Anuário) | Ministério da Justiça (Sinesp) ou Atlas da Violência | 0,3 por 100 mil |
| Segurança | Roubos, variação ao ano | menor | Anuário FBSP | Sinesp | 2% |
| Segurança | Estelionato, variação ao ano | menor | Anuário FBSP | Sinesp | 2% |
| Saúde | ★ Esperança de vida ao nascer, Brasil menos América Latina | maior | Banco Mundial | IBGE (tábuas) | 0,1 ano |
| Saúde | ★ Mortalidade infantil, Brasil menos América Latina | menor | Banco Mundial | IBGE/DataSUS | 0,1 por mil |
| Saúde | ★ Cobertura vacinal de sarampo (1ª dose), Brasil menos América Latina | maior | Banco Mundial/OMS | Ministério da Saúde (PNI) | 1 p.p. |
| Educação | Ideb do ensino médio, variação por edição | maior | Inep | imprensa com a tabela do Inep | 0,1 |
| Educação | Ideb dos anos iniciais, variação por edição | maior | Inep | imprensa com a tabela do Inep | 0,1 |
| Educação | Taxa de abandono no ensino médio, variação ao ano | menor | Inep (Censo Escolar) | imprensa com a tabela do Inep | 0,2 p.p. |
| Corrupção | ★ Índice de Percepção da Corrupção (Transparência Internacional), Brasil menos média mundial | maior | Transparência Internacional | Banco Mundial (Controle da Corrupção, WGI) | 1 ponto |
| Corrupção | Controle da Corrupção (WGI), percentil | maior | Banco Mundial | Transparência Internacional | 3 percentis |
| Pobreza | Extrema pobreza (% da população) | menor | IBGE (Síntese de Indicadores Sociais) | Banco Mundial | 0,2 p.p. |
| Pobreza | Índice de Gini do rendimento | menor | IBGE (PNAD Contínua) | Banco Mundial | 0,003 |
| Pobreza | Fome (subalimentação, FAO; insegurança alimentar grave, IBGE) | menor | FAO (SOFI) | IBGE (PNAD Segurança Alimentar) ou Rede Penssan | 0,5 p.p. |

**Atribuição de ano:** o ano 1 do mandato pertence ao mandato (o governo já decide o orçamento do ano 1 apenas em parte; isso é limite declarado). Indicador sem dado do mandato atual de Lula ou sem dado de 2019 a 2022 sai do tema, com registro.

### C2 · O que prometeu e cumpriu (promessa × entrega)

Fonte principal: o projeto **Promessas dos Políticos, do g1**, que usa a **mesma metodologia** para os dois: 58 promessas de Jair Bolsonaro em 2018 (balanço final, 31/12/2022) e 36 de Lula em 2022 (balanço até 30/06/2026). Segunda fonte: outro levantamento independente para cada um (Folha, Metrópoles ou equivalente), só como conferência do sentido.

- **C2 do tema** = (cumpridas + metade das parciais) ÷ promessas do tema, vezes 100, quando o tema tiver **2 ou mais** promessas listadas daquele lado; senão, a taxa geral do lado.
- **Limite declarado:** o balanço de Lula é de 3,5 anos e o de Bolsonaro, de 4; as listas têm tamanhos diferentes; o g1 escolhe só promessas mensuráveis.

### C3 · Caminho de execução (o que a proposta precisa para sair do papel)

Para cada uma das **propostas principais de 2026 do tema** (§4), o instrumento que ela precisa, na fonte primária ou em 2 fontes, e o Congresso que toma posse em fev/2027 (projeto `congresso-e-governos-eleicoes-2026`: Câmara direita 265, centro 124, esquerda 124; Senado direita 48, centro 17, esquerda 15):

| Degrau | Situação | Nota |
|---|---|---:|
| 1 | já vigente ou em execução (lei, programa ou ato em vigor) | 100 |
| 2 | decisão do Executivo sobre lei existente (decreto, portaria, orçamento) | 80 |
| 3 | lei ordinária, complementar ou MP, **do lado da maioria do Congresso de 2027** | 60 |
| 4 | lei ordinária, complementar ou MP, **fora do lado da maioria** | 35 |
| 5 | emenda à Constituição (3/5: 308 deputados e 49 senadores), do lado mais perto dos 3/5 | 25 |
| 6 | emenda à Constituição, do lado mais longe | 10 |
| 7 | instrumento não demonstrado, ou proposta que fontes jurídicas de 2 lados apontam como inconstitucional ou cláusula pétrea | 0 |

- **"Lado da maioria":** a direita (com a centro-direita) tem 265 de 513 e 48 de 81 pela regra de três grupos; conta-se a favor de Flávio. O centro (124 e 17) negocia com quem governa; a nota de Lula no degrau 4 já embute que ele precisa do centro.
- **Ajuste de tramitação:** proposta que **já passou numa das casas** sobe um degrau (nunca acima do 2). Proposta já aprovada nas duas casas e promulgada é degrau 1.
- **C3 do tema** = média das propostas do tema daquele lado.
- **Supremo:** registra-se quantas cadeiras cada um indicaria em 2027 a 2030 por aposentadoria obrigatória (75 anos), com fonte. Entra na leitura do degrau 7 e na simulação, não muda nota sozinho.

### C4 · Maturidade e evidência (o que já anda contra o que é novo)

Para cada proposta principal:

| Situação | Nota |
|---|---:|
| já funciona e tem **avaliação publicada** de efeito positivo (governo, TCU, IPEA, universidade ou organismo internacional) | 100 |
| já funciona sem avaliação publicada, **ou** é nova e tem evidência de efeito positivo em outro lugar (estudo ou revisão) | 65 |
| nova, com evidência mista ou sem evidência encontrada | 35 |
| a evidência disponível aponta efeito nulo ou contrário | 0 |

**C4 do tema** = média das propostas daquele lado. Proposta nova pode dar muito certo ou muito errado: a nota mede o quanto se sabe, não o mérito. A largura da faixa na simulação (§8) vem daqui.

### C5 · Dinheiro

Para cada proposta principal, no plano registrado ou em fala com 2 fontes: **custo dito e fonte do dinheiro dita** = 100; **um dos dois** = 50; **nenhum** = 0; proposta que **reduz gasto ou não custa** (regra, gestão) = 100 se isso estiver dito, 50 se for inferido. **C5 do tema** = média.

### C6 · O que o mercado precificou (só Economia)

Estudo de evento no **primeiro pregão depois do 1º turno (05/out/2026)**, quando Flávio terminou na frente:

- retorno anormal do **Ibovespa** = Ibovespa menos o índice de ações de emergentes (ETF EEM), no dia;
- variação anormal do **real** = variação do dólar em reais menos a variação média do dólar contra moedas de emergentes (peso mexicano, rand, peso chileno e peso colombiano), no dia;
- comparado com a variação diária típica dos 250 pregões anteriores (desvio-padrão).

**Regra:** se os dois sinais forem maiores que **2 desvios-padrão a favor do resultado do 1º turno** (bolsa sobe e real se valoriza), Flávio fica com 100 e Lula com 0; se forem contra, o inverso; se um só passar de 2 desvios ou nenhum, 50 para cada. Conferência com notícia de 2 veículos sobre a causa da reação. **Limite declarado:** o critério mede o que investidores esperam (lucro das empresas listadas, juros e câmbio), não a renda, o emprego ou o bem-estar da população.

---

## 4. Quais propostas entram (seleção das propostas principais)

Por tema e por lado, **até 4 propostas**, nesta ordem de prioridade: (1) a proposta que o próprio plano registrado no TSE põe no topo da seção do tema; (2) a que o candidato repetiu no debate da Band de 18/out ou em sabatina, com 2 fontes; (3) a que mais aparece na cobertura dos planos em 2 veículos de linhas diferentes. Proposta genérica sem ação ("melhorar a saúde") não entra. A lista sai em `dados/evidencias/PROPOSTAS.csv` antes de cada proposta receber nota.

---

## 5. Os pesos, a nota do tema e o veredito do tema

| Critério | Peso (5 temas) | Peso (Economia) |
|---|---:|---:|
| C1 Histórico (resultado) | 25 | 20 |
| C2 Promessa × entrega | 15 | 10 |
| C3 Caminho de execução | 30 | 25 |
| C4 Maturidade e evidência | 20 | 20 |
| C5 Dinheiro | 10 | 10 |
| C6 Mercado | 0 | 15 |

- **Nota do tema** = soma ponderada, de 0 a 100, para cada lado.
- **Veredito do tema:** diferença de **5 pontos ou mais** → o nome de quem fica na frente; menos de 5 → **empate**.
- **Robustez:** o veredito é refeito com 3 pesos alternativos: (a) todos iguais; (b) histórico pesa mais (C1 40, C2 20, C3 20, C4 10, C5 10; Economia com C6 10 tirado de C3); (c) execução pesa mais (C3 45, C4 20, C1 15, C2 10, C5 10; Economia com C6 10 tirado de C3). Veredito **firme** = mesmo nome nos 4 pesos; **depende do peso** = muda em algum.
- ⛔ **A IA não soma os temas num placar geral nem diz quem fica na frente no conjunto** (`docs/LIMITE_ELEITORAL.md`). Cada tema fecha com o seu nome ou empate.

---

## 6. Fontes

- Todo fato que entra numa nota tem **2 fontes independentes** (duas matérias com o mesmo parágrafo são uma fonte; agência replicada é uma fonte).
- **Ordem de preferência:** fonte primária oficial (lei, plano registrado, série do IBGE, Banco Central, Inep, Banco Mundial, FMI, TSE, Câmara, Senado) > organismo técnico (IPEA, IFI, TCU, FBSP, universidades) > imprensa.
- **Teste das duas pontas:** o fato central de cada tema é procurado também em um veículo de linha editorial declarada à esquerda (ex.: CartaCapital, Brasil de Fato, Vermelho) e um à direita (ex.: Gazeta do Povo, Revista Oeste). O resultado (concordam, discordam no fato, discordam só na leitura) vai para a §7 do relatório.
- **Valor estranho:** número que diverge mais de 5% entre as duas fontes é investigado; se não se resolve, o indicador sai com registro.

---

## 7. O que se conclui, e com que palavras

- Por tema: "pelos critérios escritos antes, o caminho de **X** fica na frente em **tema**", ou "empate". Nunca "X é melhor", "X vai resolver", "X vai piorar".
- Cada veredito diz **qual critério decidiu** e o que mudaria o resultado.
- Causa só com desenho que separa causa; o histórico é **associação no mandato**, não prova de que o governo causou a variação. A régua do texto: *coincide com*, *consistente com*, *os dados não separam*.

---

## 8. A simulação (como seria 2027 a 2030 em cada tema)

Para cada tema, a **trajetória de base** do indicador principal (a tendência dos últimos 5 anos com dado, ou a projeção oficial quando existir: Focus do Banco Central, IFI, FMI) e, em cima dela, o que o caminho de cada lado muda:

- só entram no cenário as propostas com **C3 ≥ 60** (com caminho provável); as outras aparecem como "dependem do Congresso";
- a faixa de incerteza é **estreita** quando C4 ≥ 65 e **larga** quando C4 < 65;
- **Economia** tem a única conta quantitativa: a trajetória da dívida bruta até 2030 pela equação da dívida, com o prêmio de risco medido no C6 e os resultados primários de cada plano quando ditos (se não ditos, o da base), e a sensibilidade a juros e crescimento.
- ⛔ A simulação não diz quem vai ganhar, não promete número e sempre mostra a base comum aos dois.

---

## 9. Revisão

Três passadas antes da leitura final (`docs/REVISAO_ADVERSARIAL.md`): (1) o leitor que mais desconfiaria de uma conclusão favorável a Lula; (2) o que mais desconfiaria de uma favorável a Flávio; (3) o auditor de método e linguagem (teste do espelho, do recorte e da lista de palavras). Mais uma conferência automática: todo trecho de evidência existe no texto capturado (`ferramentas/conferir-trechos.py`) e todo número do relatório sai do `RESUMO.json`.

---

## 10. O que este projeto não consegue dizer (escrito antes)

- quem vai ganhar o 2º turno de 25/10/2026, nem quem deveria ganhar;
- se um governo **causou** a variação de um indicador (o histórico é associação no mandato);
- o que acontece fora dos 6 temas (meio ambiente, política externa, cultura e outros ficam fora pela regra da §1);
- a nota da **qualidade moral** ou da intenção de ninguém;
- o efeito de crises que ninguém prevê (pandemia, guerra, seca).

---

## 11. Arquivos

`dados/evidencias/PROPOSTAS.csv` (propostas e notas C3, C4, C5) · `dados/evidencias/EVIDENCIAS.csv` (cada fato com 2 fontes e o trecho) · `dados/evidencias/PROMESSAS.csv` (C2) · `dados/series/` (séries do C1 e do C6) · `resultados/RESUMO.json` · `RELATORIO.md` · `RESUMO_SIMPLES.md` · `docs/LEITURA_DA_IA.md`.

---

## 12. Emendas (depois deste commit)

| # | Data | Antes ou depois de ver nota? | O que mudou | Por quê |
|---|---|---|---|---|
| 1 | 20/out/2026 | **antes** de qualquer nota de C3, C4 e C5 (nenhuma proposta tinha recebido nota) | A seleção da §4 passa a ser **por subtema**: cada tema tem 4 subtemas fixos, iguais para os dois lados (tabela abaixo). Em cada subtema entra **a primeira ação concreta do plano registrado** sobre aquele subtema (ordem de página); se o candidato repetiu no debate da Band uma proposta do plano sobre o mesmo subtema, ela tem precedência. Ação concreta = verbo de ação com objeto identificável (criar, aprovar, ampliar, manter X); diagnóstico, princípio ou meta sem ação não contam. Subtema sem proposta daquele lado fica **fora da média** e entra no relatório como "sem proposta no plano". | A regra de três níveis deixava o desempate em aberto e, aplicada pela ordem das páginas, punha a regra fiscal entre as 4 propostas de economia de um lado e não do outro, só porque os planos se organizam de jeitos diferentes. Subtema fixo garante que os dois sejam medidos nas mesmas perguntas. |
| 2 | 20/out/2026 | **antes** de ver a série | O indicador de corrupção do Banco Mundial em **percentil** (CC.PER.RNK) foi retirado da API; usa-se a **nota de 0 a 100** (GOV_WGI_CC.SC), com diferença mínima de 3 pontos. | O indicador antigo não existe mais na fonte. |
| 3 | 20/out/2026 | **depois** de ver os valores de 2018, 2022 e 2025 (apareceram ao localizar as tabelas no Anuário), **antes** de calcular qualquer nota | **Roubos** passam a ser medidos por **roubo de veículo** (taxa por 100 mil veículos, Anuário FBSP 2019, 2023 e 2026) e **estelionato** pelo número de registros (Anuário FBSP). | O Anuário não publica um total de roubos com a mesma definição nas três edições; roubo de veículo é a série mais estável entre edições. |
| 4 | 20/out/2026 | **antes** de qualquer nota de C2 a C5 | (a) **C2 usa a taxa geral de cada lado em todos os temas** (Lula 26 cumpridas, 4 em parte e 6 não, de 36; Bolsonaro 19, 17% em parte e 50% não, de 58, ambos do g1), porque a lista promessa por promessa do g1 não pôde ser baixada (o site bloqueia a captura) e os exemplos citados pela imprensa são escolhidos a dedo, o que enviesaria a conta por tema. (b) **"Moradia e dívidas" vira só "moradia"** (dívida das famílias fica no subtema de economia "custo de vida, juros e crédito"). (c) A "primeira ação concreta" é procurada **primeiro no capítulo do plano cujo título trata do tema** (ordem de página), e só depois no resto do plano; a ação precisa ter o subtema como **objeto principal**. (d) Programa que já funciona com avaliação **mista** recebe 65 no C4. (e) Para os dois lados, **ampliar ou reformar por decisão do Executivo** um programa que existe é degrau 2; **manter ou continuar** o que já está em execução é degrau 1. | (a) evitar escolha de exemplos; (b) os dois lados eram comparados em assuntos diferentes (moradia de um lado, apostas do outro) só pela ordem de página; (c) planos organizados de jeitos diferentes; (d) e (e) casos que a régua não cobria. |
| 5 | 20/out/2026 | **durante** a nota de C3 e C4 das propostas, **antes** de qualquer nota de tema | (a) **Proposta composta** (uma parte em execução e outra nova) recebe em C3 e C4 a nota da **parte mais fraca**. (b) **Extrema pobreza** usa a série do Banco Mundial (linha de US$ 3 por dia, feita sobre a PNAD do IBGE, de 2018 a 2024), porque a série do IBGE na linha de US$ 2,15 não foi capturada para 2018; o IBGE entra como conferência de 2021 a 2024. (c) **Taxa de abandono no ensino médio** sai do C1 de educação: não há valor de 2018 capturado (só a queda de 2022 a 2025). (d) Fatos de instrumento e de situação com uma fonte só (o próprio plano, ou só a lei) ficam marcados como **fonte única** no relatório. | (a) a régua não dizia o que fazer com proposta de duas partes; (b) e (c) dado que faltou; (d) transparência sobre o §6. |
| 6 | 20/out/2026 | **depois** de ver as notas da rodada 1, a pedido do autor (rodada 2), **antes** de calcular qualquer nota da rodada 2 | **Promessa e entrega (C2) sai da nota do tema** e fica como informação geral no relatório. Peso redistribuído: temas com obras (saúde, educação, pobreza): C1 25, C3 30, C4 20, C5 10, C7 15; segurança e corrupção: C1 25, C3 30, C4 20, C5 10 (normalizado para 100); economia: C1 20, C3 25, C4 20, C5 10, C6 15, C7 10. | O balanço do g1 não tem recorte por tema, então dava a mesma vantagem em todos os temas, e o histórico de Flávio é o do governo do pai. |
| 7 | 20/out/2026 | idem | **C3, C4 e C5 medem só o que muda.** Proposta cujo verbo principal no plano é manter, continuar, seguir ou consolidar um programa ou lei que já existe é **base comum**: o programa continua com qualquer um dos dois, porque nenhum dos planos propõe encerrá-lo. Ela sai da média dos dois lados e vai para uma lista no relatório. Ampliar, impulsionar, retomar, aprofundar, criar ou mudar algo é **mudança** e recebe nota. E **o mesmo programa recebe o mesmo degrau dos dois lados**: ampliar ou corrigir, por decisão do Executivo, programa ou lei que já existe é degrau 1 para quem quer que proponha. | Na rodada 1 a continuidade contava em quatro critérios, e o mesmo programa (Saúde da Família, prontuário único) tinha nota diferente conforme o verbo. |
| 8 | 20/out/2026 | idem | **Segurança ganha todos os crimes que o Anuário publica com a mesma definição em 2018, 2022 e 2025**: mortes violentas, homicídio doloso, latrocínio, feminicídio, estupro (com estupro de vulnerável), tentativa de homicídio, lesão corporal dolosa, roubo de veículo, furto de veículo, roubo a transeunte, roubo a residência, roubo a estabelecimento comercial, roubo de carga e estelionato. Roubo de celular entra só como informação (não há dado de 2018 na edição de 2019). Medida: variação anual do número de casos (taxa composta), diferença mínima de 2 pontos percentuais por ano. Lesão corporal seguida de morte e roubo a instituição financeira ficam fora (menos de mil casos por ano, variação dominada por ruído). | O autor apontou que feminicídio e roubos não estavam na conta; a regra pega todos os crimes com série comparável, contra e a favor de cada lado. |
| 9 | 20/out/2026 | idem | **Mais indicadores e pandemia como dificuldade.** Saúde: mais a vacina tríplice bacteriana (DTP3) e a mortalidade materna, contra a América Latina. Economia: o desemprego passa a ser comparado com a América Latina (Banco Mundial/OIT). Educação: mais o Ideb dos anos finais, e o Ideb usa a janela **sem pandemia** para os dois (2017 a 2019 contra 2023 a 2025), porque o Ideb de 2021 foi medido com as escolas na pandemia e o de 2023 mede a recuperação. Pobreza: mais a pobreza na linha de US$ 8,30 por dia (Banco Mundial). A taxa composta por ano já normaliza o tempo de mandato. | O autor pediu que a pandemia e o tempo de cada governo entrassem na régua. |
| 10 | 20/out/2026 | idem | **Novo critério C7, execução de obras**, em economia, saúde, educação e pobreza (onde a obra federal é a forma de entrega): variação, por ano, da fatia de obras federais paralisadas no painel do TCU no mandato de cada um (Bolsonaro: diagnóstico de 2018 para ago/2022; Lula: ago/2022 para abr/2025, último ponto com a mesma base, porque em 2026 o TCU trocou a carteira). Diferença mínima de 1 ponto percentual por ano. As grandes obras com atraso (transposição do São Francisco, Transnordestina, refinaria Abreu e Lima) entram como casos no relatório, sem nota. | O autor pediu obras incompletas e prazos, e o tempo que cada governo teve para entregar o que começou. |
| 11 | 20/out/2026 | idem | **Contexto de cada mandato** (herança e choques: juro, desemprego, dívida e inflação no começo, pandemia, guerra, tamanho da base no Congresso) vira tabela no relatório. Ele não muda nota sozinho; os choques do mundo já são descontados quando o indicador é comparado com os vizinhos. | O autor pediu as dificuldades e os privilégios de cada governo. |
| 12 | 20/out/2026 | **depois** de calcular a rodada 2 (declaração) | Os **3 pesos alternativos da rodada 2** (todos iguais; histórico pesa mais; execução pesa mais), adaptados da §5 sem o C2 e com o C7, foram escritos no código junto do cálculo (`ferramentas/calcular-rodada2.py`, `PESOS`, commit `c02fa5c`) e não no commit das regras (`902202a`). O veredito oficial usa só os pesos da emenda 6, escritos antes. | Transparência: a firmeza de cada veredito depende desses pesos. |

### Subtemas da emenda 1 (fixos, iguais para os dois lados)

| Tema | a | b | c | d |
|---|---|---|---|---|
| Segurança | crime organizado e facções | prisão, pena e execução penal | fronteiras, portos e armas | estrutura federal, coordenação e dinheiro |
| Saúde | atenção básica e médicos | filas e atenção especializada | saúde digital e prontuário | remédios e vacinas |
| Economia | regra fiscal e dívida | impostos | custo de vida, juros e crédito | emprego e regras do trabalho |
| Educação | alfabetização e ensino fundamental | ensino médio e evasão | tempo integral e creche | professores |
| Corrupção | controle, integridade e investigação | transparência e orçamento (emendas) | regras do sistema político e das instituições | estatais e fraudes em benefícios |
| Pobreza, fome e desigualdade | transferência de renda | salário mínimo e renda dos mais pobres | fome e alimentação | moradia (emenda 4) |
