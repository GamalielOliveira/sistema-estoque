"""Interface gráfica (Tkinter) do sistema de estoque.

Só cuida de janelas, botões e popups. A lógica de negócio (calcular, validar,
salvar) fica inteira em src/estoque.py — esta classe só chama essas funções.
"""

import random
import tkinter as tk
from tkinter import messagebox, ttk

from src import estoque


class AppEstoque:
    def __init__(self) -> None:
        self.estoque = estoque.carregar_estoque()

        self.janela = tk.Tk()
        self.janela.title("Inventory System - Market")
        self.janela.geometry("520x420")
        self.janela.resizable(False, False)

        self._montar_menu()
        self._montar_abas()
        self._atualizar_consulta()
        self._atualizar_dashboard()

    def _montar_menu(self) -> None:
        barra_menu = tk.Menu(self.janela)
        barra_menu.add_command(label="Cadastrar Produto", command=self._popup_cadastro)
        barra_menu.add_command(label="Vender Produto", command=self._popup_venda)
        barra_menu.add_command(label="Sair", command=self.janela.quit)
        self.janela.config(menu=barra_menu)

    def _montar_abas(self) -> None:
        abas = ttk.Notebook(self.janela)
        abas.pack(fill="both", expand=True, padx=10, pady=10)

        aba1 = tk.Frame(abas)
        abas.add(aba1, text="Consulta Estoque")
        tk.Label(
            aba1, text="Produto      Quantidade     Preço", font=("Arial", 12, "bold")
        ).pack(pady=5)
        self.label_consulta = tk.Label(aba1, text="", font=("Consolas", 11), justify="left")
        self.label_consulta.pack(pady=5)

        aba2 = tk.Frame(abas)
        abas.add(aba2, text="Painel (Dashboard)")
        self.label_dash = tk.Label(aba2, text="", font=("Arial", 12), justify="left")
        self.label_dash.pack(pady=20)

        aba3 = tk.Frame(abas)
        abas.add(aba3, text="Estoque Atualizado")
        self.label_estoque_atualizado = tk.Label(aba3, text="", font=("Arial", 12), justify="left")
        self.label_estoque_atualizado.pack(pady=20)

    def _atualizar_consulta(self) -> None:
        self.label_consulta.config(text=estoque.formatar_consulta(self.estoque))

    def _atualizar_dashboard(self) -> None:
        total_produtos, total_itens = estoque.calcular_totais(self.estoque)
        tempo_espera = random.randint(10, 45)
        self.label_dash.config(
            text=(
                f"Total de produtos: {total_produtos}\n"
                f"Total de itens: {total_itens}\n"
                f"Tempo médio de fila caixa: {tempo_espera} min"
            )
        )

    def _popup_cadastro(self) -> None:
        janela_pop = tk.Toplevel(self.janela)
        janela_pop.title("Cadastro de Produto")
        janela_pop.geometry("320x200")
        janela_pop.resizable(False, False)

        tk.Label(janela_pop, text="Produto:").pack(pady=2)
        e_prod = tk.Entry(janela_pop, width=30)
        e_prod.pack()

        tk.Label(janela_pop, text="Quantidade:").pack(pady=2)
        e_qtd = tk.Entry(janela_pop, width=30)
        e_qtd.pack()

        tk.Label(janela_pop, text="Preço (R$):").pack(pady=2)
        e_pre = tk.Entry(janela_pop, width=30)
        e_pre.pack()

        def confirmar():
            produto = e_prod.get().strip()
            qtd = e_qtd.get().strip()
            pre = e_pre.get().strip()

            if not produto or not qtd or not pre:
                messagebox.showwarning("Aviso", "Preencha todos os campos.")
                return

            estoque.cadastrar_produto(self.estoque, produto, int(qtd), float(pre))
            estoque.salvar_estoque(self.estoque)
            self._atualizar_consulta()
            self._atualizar_dashboard()
            janela_pop.destroy()

        tk.Button(janela_pop, text="Confirmar", width=18, command=confirmar).pack(pady=8)

    def _popup_venda(self) -> None:
        janela_pop = tk.Toplevel(self.janela)
        janela_pop.title("Venda de Produto")
        janela_pop.geometry("300x160")
        janela_pop.resizable(False, False)

        tk.Label(janela_pop, text="Produto:").pack(pady=2)
        e_prod = tk.Entry(janela_pop, width=28)
        e_prod.pack()

        tk.Label(janela_pop, text="Quantidade:").pack(pady=2)
        e_qtd = tk.Entry(janela_pop, width=28)
        e_qtd.pack()

        def confirmar():
            produto = e_prod.get().strip()
            qtd = e_qtd.get().strip()

            if not produto or not qtd:
                messagebox.showwarning("Aviso", "Preencha os campos.")
                return

            sucesso, mensagem = estoque.vender_produto(self.estoque, produto, int(qtd))
            if not sucesso:
                messagebox.showerror("Erro", mensagem)
                return

            estoque.salvar_estoque(self.estoque)
            self._atualizar_consulta()
            self._atualizar_dashboard()
            messagebox.showinfo("Venda", mensagem)
            janela_pop.destroy()

        tk.Button(janela_pop, text="Registrar Venda", width=18, command=confirmar).pack(pady=6)

    def iniciar(self) -> None:
        self.janela.mainloop()
