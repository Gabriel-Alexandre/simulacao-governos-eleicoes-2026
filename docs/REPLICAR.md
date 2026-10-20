# Como refazer tudo

Python 3.11 e as bibliotecas de `requirements.txt`.

```bash
pip install -r requirements.txt
```

## 1. Baixar de novo as séries (Banco Central, IBGE, FMI, Banco Mundial, mercado)

```bash
python ferramentas/coletar-series.py
```

## 2. Baixar de novo as páginas e PDFs

Cada linha de `dados/MANIFESTO.csv` tem o `id` e a `url`. Para uma fonte:

```bash
python ferramentas/capturar.py <id> <url> --forcar
```

Páginas mudam com o tempo; o texto que foi usado está em `dados/capturas/<id>.txt`, com o sha256 do bruto no manifesto.

## 3. Conferir, calcular, simular, desenhar e escrever

```bash
python ferramentas/montar-propostas.py
python ferramentas/conferir-trechos.py
python ferramentas/calcular.py            # rodada 1 (resultados/rodada1/)
python ferramentas/calcular-rodada2.py    # rodada 2 (resultados/RESUMO.json)
python ferramentas/simular.py
python ferramentas/graficos.py
python ferramentas/gerar-relatorio.py
python ferramentas/listar-fontes.py
python ferramentas/conferir-linguagem.py
python -m pytest -q
```

## 4. Mudar um peso ou uma nota

- Pesos e régua: `ferramentas/calcular-rodada2.py` (`PESOS`, rodada 2 vigente) segue `docs/PRE_REGISTRO.md` §5 e as emendas 6 e 12; `ferramentas/calcular.py` guarda a rodada 1. Quem quiser outro peso muda ali e roda de novo; o veredito oficial é o dos pesos escritos antes.
- Nota de uma proposta: `dados/evidencias/NOTAS_RODADA2.csv` (rodada 2: base comum ou mudança) e `dados/evidencias/NOTAS_PROPOSTAS.csv` (rodada 1), com o motivo e a evidência. Toda evidência nova entra em `dados/evidencias/EVIDENCIAS.csv` com o trecho literal, e `conferir-trechos.py` precisa passar.
