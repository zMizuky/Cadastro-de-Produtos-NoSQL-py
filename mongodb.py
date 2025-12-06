import pymongo
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["database"]
collection = db["store"]

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Produtos")
        self.root.geometry("600x300")

        self.produtos = []

        # Arrays dos dropdown's
        tamanhos = ["", "P", "PP", "M", "G", "GG"]
        tipos = ["Eletrônico", "Alimento", "Roupa", "Livro"]
        cores = ["", "Azul", "Preto", "Vermelho", "Roxo", "Branco"]
        tipos_filtro = ["Todos", "Eletrônico", "Alimento", "Roupa", "Livro"]

        # Elementos da interface
        frame_form = tk.Frame(root, padx=10, pady=10)
        frame_form.pack(side="left", fill="y")

        tk.Label(frame_form, text="Nome do Produto:").pack(anchor="w")
        self.entry_nome = tk.Entry(frame_form, width=25)
        self.entry_nome.pack(anchor="w", pady=3)

        tk.Label(frame_form, text="Preço:").pack(anchor="w")
        self.entry_preco = tk.Entry(frame_form, width=15)
        self.entry_preco.pack(anchor="w", pady=3)

        tk.Label(frame_form, text="Tamanho:").pack(anchor="w")
        self.entry_tamanho = ttk.Combobox(frame_form, values=tamanhos, state="readonly", width=13)
        self.entry_tamanho.pack(anchor="w", pady=3)
        self.entry_tamanho.current(0)

        tk.Label(frame_form, text="Páginas:").pack(anchor="w")
        self.entry_pagina = tk.Entry(frame_form, width=15)
        self.entry_pagina.pack(anchor="w", pady=3)

        tk.Label(frame_form, text="Tipo do Produto:").pack(anchor="w")

        self.combo_tipo = ttk.Combobox(frame_form, values=tipos, state="readonly", width=22)
        self.combo_tipo.pack(anchor="w", pady=3)
        self.combo_tipo.current(0)

        tk.Label(frame_form, text="Cor do Produto:").pack(anchor="w")

        self.combo_cor = ttk.Combobox(frame_form, values=cores, state="readonly", width=22)
        self.combo_cor.pack(anchor="w", pady=3)
        self.combo_cor.current(0)

        tk.Button(frame_form, text="Cadastrar", command=self.cadastrar).pack(anchor="w", pady=10)
        tk.Button(frame_form, text="Limpar dados", command=self.limpar).pack(anchor="w", pady=10)

        frame_lista = tk.Frame(root, padx=10, pady=10)
        frame_lista.pack(side="right", fill="both", expand=True)

        tk.Label(frame_lista, text="Produtos Cadastrados:").pack(anchor="w")

        # Dropdown de filtro
        tk.Label(frame_lista, text="Filtrar por tipo:").pack(anchor="w", pady=(0, 3))

        self.combo_filtro = ttk.Combobox(frame_lista, values=tipos_filtro, state="readonly", width=20)
        self.combo_filtro.pack(anchor="w", pady=(0, 5))
        self.combo_filtro.current(0)
        self.combo_filtro.bind("<<ComboboxSelected>>", self.filtrar_lista)

        self.lista = tk.Text(frame_lista, width=40, height=15, state="disabled")
        self.lista.pack(fill="both", expand=True)

        # Atualizar lista de produtos ao iniciar
        try:
            for item in db.collection.find():
                produto = f'{item["nome"]} | R$ {item["preco"]} | {item["tipo"]}'
                
                paginas = item.get("paginas")
                tamanho = item.get("tamanho")
                if paginas != None:
                    produto += f" | {paginas} páginas"
                if tamanho != None:
                    produto += f" | {tamanho}"
                if cor != None:
                    produto += f" | {cor}"
                self.produtos.append(produto)
                self.atualizar_lista()
        except:
            print("")


    # Cadastro
    def cadastrar(self):
        # Recolhe os input
        nome = self.entry_nome.get().strip()
        preco = self.entry_preco.get().strip()
        tamanho = self.entry_tamanho.get()
        tipo = self.combo_tipo.get()
        cor = self.combo_cor.get()
        paginas = self.entry_pagina.get()

        # Exibe erro na tela se não tiver preço ou nome
        if not nome or not preco:
            messagebox.showinfo("Erro!", "Você esqueceu de inserir os dados!")
            return
        
        # Cria o produto com atributos padrão
        produtoDB = {
            "nome": nome, 
            "preco": preco,
            "tipo": tipo
        }

        # Print dos itens no BD
        for item in db.collection.find():
            print(item)

        # Cria a string para aparecer na lista
        produto = f"{nome} | R$ {preco} | {tipo}"
        
        # Se foi colocado o atributo opcional ele acrescenta na string
        if tamanho != "":
            produtoDB.update({"tamanho": tamanho})
            produto += f" | {tamanho}"

        if paginas != "":
            produtoDB.update({"paginas": paginas})
            produto += f" | {paginas} páginas"

        if cor != "":
            produtoDB.update({"cor": cor})
            produto += f" | {cor}"
        
        # Armazena no DB e na array
        db.collection.insert_one(produtoDB)
        self.produtos.append(produto)

        # Mostra na lista
        self.atualizar_lista()

        # Limpa campos
        self.entry_nome.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        self.entry_tamanho.delete(0, tk.END)
        self.entry_pagina.delete(0, tk.END)

    def filtrar_lista(self, event=None):
        tipo_selecionado = self.combo_filtro.get()
        self.lista.config(state="normal")
        self.lista.delete("1.0", tk.END)

        for p in self.produtos:
            if tipo_selecionado == "Todos" or tipo_selecionado in p:
                self.lista.insert(tk.END, p + "\n") 

        self.lista.config(state="disabled")

    # Atualizar lista
    def atualizar_lista(self):
        self.lista.config(state="normal")
        self.lista.delete("1.0", tk.END)
        
        for p in self.produtos:
            self.lista.insert(tk.END, p + "\n")

        self.lista.config(state="disabled")
    
    # Limpar BD
    def limpar(self):
        db.collection.delete_many({})
        self.lista.config(state="normal")
        self.lista.delete("1.0", tk.END)
        self.produtos = []

root = tk.Tk()
App(root)
root.mainloop()
