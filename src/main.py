"""Ponto de entrada do sistema de estoque. Só liga interface + lógica e inicia o app.

Rodar: python -m src.main
"""
# Praticando fluxo de branch e commit - Analista de Automação
# Praticando fluxo visual no VS Code
# treinando pull request

# acabei e selecionar a branch : Testando - nova - brach
# enviando mais uma comentario na branch - Testando


from src.interface import AppEstoque


def main() -> None:
    app = AppEstoque()
    app.iniciar()


if __name__ == "__main__":
    main()
