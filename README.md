# Sistema de Estoque

Aplicação de desktop (Tkinter) para cadastrar produtos, registrar vendas e
consultar o estoque de um mercado. Os dados são persistidos em `data/estoque.json`.

## Estrutura

```
src/estoque.py    -> lógica de negócio (carregar, salvar, cadastrar, vender)
src/interface.py  -> janelas e botões (Tkinter), chama as funções de estoque.py
src/main.py       -> ponto de entrada
data/estoque.json -> dados persistidos
```

## Como rodar

```bash
python -m src.main
```

## Origem

Refatorado a partir de `Dicionarios6.45.py` (Módulo 01, exercício 2 do curso) —
mesmo comportamento, agora separado por responsabilidade.
