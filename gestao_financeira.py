import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import messagebox


class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão de Finanças")

        
        self.gastos_df = pd.DataFrame(columns=["Descrição", "Valor", "Data"])
        self.ganhos_df = pd.DataFrame(columns=["Descrição", "Valor", "Data"])

        
        self.create_widgets()

    def create_widgets(self):
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        
        self.tab_gastos = ttk.Frame(self.notebook, width=400, height=400)
        self.tab_ganhos = ttk.Frame(self.notebook, width=400, height=400)

        self.notebook.add(self.tab_gastos, text='Controle de Gastos')
        self.notebook.add(self.tab_ganhos, text='Controle de Ganhos')

        
        self.label_gastos = tk.Label(self.tab_gastos, text="Adicionar Despesa")
        self.label_gastos.pack(pady=10)

        self.entry_gastos_desc = tk.Entry(self.tab_gastos, width=50)
        self.entry_gastos_desc.pack(pady=5)
        self.entry_gastos_valor = tk.Entry(self.tab_gastos, width=20)
        self.entry_gastos_valor.pack(pady=5)

        self.btn_add_gasto = tk.Button(self.tab_gastos, text="Adicionar Despesa", command=self.add_gasto)
        self.btn_add_gasto.pack(pady=10)

        self.btn_save_gastos = tk.Button(self.tab_gastos, text="Salvar Gastos", command=self.save_gastos)
        self.btn_save_gastos.pack(pady=5)

        
        self.tree_gastos = ttk.Treeview(self.tab_gastos, columns=("Descrição", "Valor", "Data"), show="headings")
        self.tree_gastos.heading("Descrição", text="Descrição")
        self.tree_gastos.heading("Valor", text="Valor")
        self.tree_gastos.heading("Data", text="Data")
        self.tree_gastos.pack(pady=20)

        
        self.label_ganhos = tk.Label(self.tab_ganhos, text="Adicionar Ganho")
        self.label_ganhos.pack(pady=10)

        self.entry_ganhos_desc = tk.Entry(self.tab_ganhos, width=50)
        self.entry_ganhos_desc.pack(pady=5)
        self.entry_ganhos_valor = tk.Entry(self.tab_ganhos, width=20)
        self.entry_ganhos_valor.pack(pady=5)

        self.btn_add_ganho = tk.Button(self.tab_ganhos, text="Adicionar Ganho", command=self.add_ganho)
        self.btn_add_ganho.pack(pady=10)

        self.btn_save_ganhos = tk.Button(self.tab_ganhos, text="Salvar Ganhos", command=self.save_ganhos)
        self.btn_save_ganhos.pack(pady=5)

        
        self.tree_ganhos = ttk.Treeview(self.tab_ganhos, columns=("Descrição", "Valor", "Data"), show="headings")
        self.tree_ganhos.heading("Descrição", text="Descrição")
        self.tree_ganhos.heading("Valor", text="Valor")
        self.tree_ganhos.heading("Data", text="Data")
        self.tree_ganhos.pack(pady=20)

        
        self.entry_gastos_valor.bind('<FocusOut>', self.validate_currency_input)
        self.entry_ganhos_valor.bind('<FocusOut>', self.validate_currency_input)

    def validate_currency_input(self, event):
        """Valida e formata a entrada de valor como moeda brasileira."""
        entry = event.widget
        value = entry.get().replace('R$', '').replace(',', '').strip()
        try:
            formatted_value = f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            entry.delete(0, tk.END)
            entry.insert(0, formatted_value)
        except ValueError:
            entry.delete(0, tk.END)
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")

    def add_gasto(self):
        desc = self.entry_gastos_desc.get()
        valor = self.entry_gastos_valor.get().replace('R$', '').replace('.', '').replace(',', '.').strip()
        if desc and valor:
            try:
                valor = float(valor)
                data = pd.Timestamp.now().strftime('%d/%m/%Y')
                new_row = {"Descrição": desc, "Valor": f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'), "Data": data}
                self.gastos_df = pd.concat([self.gastos_df, pd.DataFrame([new_row])], ignore_index=True)
                self.tree_gastos.insert("", "end", values=(desc, new_row["Valor"], data))
                self.entry_gastos_desc.delete(0, tk.END)
                self.entry_gastos_valor.delete(0, tk.END)
                messagebox.showinfo("Sucesso", "Despesa adicionada com sucesso!")
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def add_ganho(self):
        desc = self.entry_ganhos_desc.get()
        valor = self.entry_ganhos_valor.get().replace('R$', '').replace('.', '').replace(',', '.').strip()
        if desc and valor:
            try:
                valor = float(valor)
                data = pd.Timestamp.now().strftime('%d/%m/%Y')
                new_row = {"Descrição": desc, "Valor": f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'), "Data": data}
                self.ganhos_df = pd.concat([self.ganhos_df, pd.DataFrame([new_row])], ignore_index=True)
                self.tree_ganhos.insert("", "end", values=(desc, new_row["Valor"], data))
                self.entry_ganhos_desc.delete(0, tk.END)
                self.entry_ganhos_valor.delete(0, tk.END)
                messagebox.showinfo("Sucesso", "Ganho adicionado com sucesso!")
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def save_gastos(self):
        self.gastos_df.to_csv("gastos.csv", index=False)
        messagebox.showinfo("Sucesso", "Gastos salvos com sucesso!")

    def save_ganhos(self):
        self.ganhos_df.to_csv("ganhos.csv", index=False)
        messagebox.showinfo("Sucesso", "Ganhos salvos com sucesso!")


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
