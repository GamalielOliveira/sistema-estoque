"""Lógica de negócio do estoque: carregar, salvar, cadastrar e vender produtos.

Nenhuma linha aqui sabe que existe uma janela — por isso essa lógica poderia ser
reaproveitada em outro contexto (uma API, um bot, um teste) sem depender do Tkinter.
"""

import json
from pathlib import Path

ARQUIVO_PADRAO = Path(__file__).resolve().parent.parent / "data" / "estoque.json"


def carregar_estoque(caminho: Path = ARQUIVO_PADRAO) -> dict:
    if caminho.exists():
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return {}


def salvar_estoque(estoque: dict, caminho: Path = ARQUIVO_PADRAO) -> None:
    caminho.parent.mkdir(exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(estoque, arquivo, ensure_ascii=False, indent=2)


def cadastrar_produto(estoque: dict, produto: str, quantidade: int, preco: float) -> None:
    estoque[produto.strip().lower()] = [quantidade, preco]


def vender_produto(estoque: dict, produto: str, quantidade: int) -> tuple[bool, str]:
    produto = produto.strip().lower()

    if produto not in estoque:
        return False, "Produto não encontrado."

    estoque[produto][0] -= quantidade
    if estoque[produto][0] < 0:
        estoque[produto][0] = 0

    return True, f"{quantidade} unidades vendidas."


def formatar_consulta(estoque: dict) -> str:
    if not estoque:
        return "Sem produtos cadastrados."

    linhas = [
        f"{produto.title():<12} {quantidade:>6} un  |  R$ {preco:>6.2f}"
        for produto, (quantidade, preco) in estoque.items()
    ]
    return "\n".join(linhas)


def calcular_totais(estoque: dict) -> tuple[int, int]:
    total_produtos = len(estoque)
    total_itens = sum(quantidade for quantidade, _ in estoque.values())
    return total_produtos, total_itens
