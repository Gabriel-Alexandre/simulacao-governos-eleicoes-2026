# CLAUDE.md: como operar neste repositório

As regras moram em `.cursor/rules/simulacao-fundamentos.mdc`, que o Cursor carrega sozinho e o Claude Code não. Este arquivo é roteador.

| Ordem | Arquivo | Para quê |
|---|---|---|
| 1 | `ESTADO.md` | onde o trabalho parou |
| 2 | `.cursor/rules/simulacao-fundamentos.mdc` | a doutrina, sempre |
| 3 | `docs/PRE_REGISTRO.md` | temas, critérios, pesos, régua e emendas; critério novo só pela §12 |
| 4 | `docs/LIMITE_ELEITORAL.md` | ⛔ a IA não soma temas nem diz quem é melhor |
| 5 | `RELATORIO.md` e `docs/LEITURA_DA_IA.md` | o resultado |
| 6 | `docs/HISTORIA_DO_PROJETO.md` e `docs/METODO.md` | a ordem dos fatos, quem fez o quê, os erros, e a origem de cada método |

## O que nunca fazer

- Número que não saiu de série com hash ou de trecho conferido (`ferramentas/conferir-trechos.py` precisa passar).
- Número escrito à mão no relatório (ele sai de `ferramentas/gerar-relatorio.py`).
- Mudar critério, peso ou régua sem emenda datada na §12, dizendo se foi antes ou depois de ver nota.
- Somar temas num placar, dizer quem é melhor para o país ou recomendar voto.
- Commit ou push sem o autor confirmar (o autor pediu o repositório público e o push desta execução em 20/out/2026).
