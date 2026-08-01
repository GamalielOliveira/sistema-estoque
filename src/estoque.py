"""Lógica de negócio do estoque: carregar, salvar, cadastrar e vender produtos.

Os produtos agora são representados pela dataclass Produto (ou ProdutoPerecivel,
para itens com data de validade) em vez de listas soltas.
"""

import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

ARQUIVO_PADRAO = Path(__file__).resolve().parent.parent / "data" / "estoque.json"


@dataclass
class Produto:
    nome: str
    quantidade: int
    preco: float


@dataclass
class ProdutoPerecivel(Produto):
    validade: date

    def vencido(self) -> bool:
        return date.today() > self.validade


def carregar_estoque(caminho: Path = ARQUIVO_PADRAO) -> dict[str, Produto]:
    if not caminho.exists():
        return {}

    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados_brutos = json.load(arquivo)

    estoque: dict[str, Produto] = {}
    for nome, dados in dados_brutos.items():
        if "validade" in dados:
            dados = {**dados, "validade": date.fromisoformat(dados["validade"])}
            estoque[nome] = ProdutoPerecivel(**dados)
        else:
            estoque[nome] = Produto(**dados)

    return estoque


def salvar_estoque(estoque: dict[str, Produto], caminho: Path = ARQUIVO_PADRAO) -> None:
    caminho.parent.mkdir(exist_ok=True)

    dados_brutos = {}
    for nome, produto in estoque.items():
        dados = asdict(produto)
        if "validade" in dados:
            dados["validade"] = dados["validade"].isoformat()
        dados_brutos[nome] = dados

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados_brutos, arquivo, ensure_ascii=False, indent=2)


def cadastrar_produto(estoque: dict[str, Produto], nome: str, quantidade: int, preco: float) -> None:
    nome = nome.strip().lower()
    estoque[nome] = Produto(nome=nome, quantidade=quantidade, preco=preco)


def cadastrar_produto_perecivel(
    estoque: dict[str, Produto], nome: str, quantidade: int, preco: float, validade: date
) -> None:
    nome = nome.strip().lower()
    estoque[nome] = ProdutoPerecivel(nome=nome, quantidade=quantidade, preco=preco, validade=validade)


def listar_vencidos(estoque: dict[str, Produto]) -> list[Produto]:
    return [p for p in estoque.values() if isinstance(p, ProdutoPerecivel) and p.vencido()]


def vender_produto(estoque: dict[str, Produto], nome: str, quantidade: int) -> tuple[bool, str]:
    nome = nome.strip().lower()

    if nome not in estoque:
        return False, "Produto não encontrado."

    produto = estoque[nome]
    produto.quantidade = max(0, produto.quantidade - quantidade)

    return True, f"{quantidade} unidades vendidas."


def formatar_consulta(estoque: dict[str, Produto]) -> str:
    if not estoque:
        return "Sem produtos cadastrados."

    linhas = [
        f"{produto.nome.title():<12} {produto.quantidade:>6} un  |  R$ {produto.preco:>6.2f}"
        for produto in estoque.values()
    ]
    return "\n".join(linhas)


def calcular_totais(estoque: dict[str, Produto]) -> tuple[int, int]:
    total_produtos = len(estoque)
    total_itens = sum(produto.quantidade for produto in estoque.values())
    return total_produtos, total_itens
