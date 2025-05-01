import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as mat

class app:
    def __init__(self, main):
        self.main = main
        self.tracker = budgetTracker()
        self.main.title("Budget Tracker")
        self.main.geometry("600x600")

        self.widgets()
        self.update()

    def widgtes(self):
        title = tk.Label(self.main, text = "Budget tracking",
                         font = ("Times New Roman", 24, "bold"))
        title.pack()

        frame = tk.Frame(self.main)
        frame.pack(pady = 15)

        tk.Label(self.main, text = "Sum: ").grid(row = 0, column = 0, padx = 5, pady = 5)
        self.sum_entry = tk.Entry(frame)
        self.sum_entry.grid(row = 0, column = 1, padx = 5, pady = 5)

        tk.Label(self.main, text = "Category").grid(row = 1, column = 0, padx = 5, pady = 5)
        self.category_entry = tk.Entry(frame)
        self.category_entry.grid(row = 1, column = 1, padx = 5, pady =5)

        tk.Label(self.main, text = "Type: ").grid(row = 2, column = 0, padx = 5, pady = 5)
        self.variable = tk.StringVar()
        menu = ttk.Combobox(frame, textvariable = variable, values = ["Income", "Expense"])
        menu.grid(row = 2, column = 1, padx = 5, pady = 5)

        button = tk.Button(self.main, text = "Add", command = self.add_transaction,
                            bg = "#4cff57", fg = "white", font = ("Times New Roman",18,"bold"), witdth = 15)
        button.pack(pady = 10)

        self.summary = tk.Label(self.main, text = "", font = ("Times New Roman",16))
        self.summary.pack(pady = 10)

        button_graph = tk.Button(self.main, text = "Show the graph", command = self.plot_data, 
                                 bg = "#6be4ba", fg = "white", width = 15, font = ("Times New Roman", 16))
        button_graph.pack(pady = 10)

    def add_transaction(self):
        try:
            sum = float(self.sum_entry.get())
            category = self.category_entry.get()
            type = self.variable.get()

            if not category:
                raise Valueerror("The category can't be empty!!!")
            if not sum:
                raise ValueError("The amount can't be empty!!!")
            if not type:
                raise ValueError("Choose the type of transaction!!!")
            
            self.tracker.add_transaction(sum, category, type)
            self.sum_entry(0, tk.END)
            self.category_entry(0, tk.END)
            self.update()
            messagebox.showinfo("Succces", "Succesfully added transaction!!!")
        except ValueError as error:
            messagebox.showerror("Error", f"Invalid value: {error}!!!")

    def update(self):
        income, expenses, balance = self.tracker.summary()
        self.summary_label.config(text = f"Income: {income:.2f} RON     Expenses: {expenses:.2f} RON    Balance: {balance:.2f} RON")

    def plot_data(self):
        income, expenses, balance = self.tracker.summary()
        category = self.tracker.get_category_summary()

        if not category:
            messagebox.showwarning("Warning", "No data available for the graph!!!")
        
        fig, axes = mat.subplots(1,2, figsize = (12, 5))

        #grafic pe categorii
        categories = list(category.keys())
        amounts = list(category.values())

        axes[0].pie(amounts, labels = categories, autopct = '%1.1f%%', startangle = 140)
        axes[0].set_title("Expenses by categories")

        #grafic pt venituri vs cheltuieli vs balanta
        axes[1].bar(["Income", "Expenses", "Balance"], [income, expenses, balance], color = ["#3eeb43", "#fa2834", "#1683ca"])
        axes[1].set_title("Financial situation")

        mat.tight_layout()
        mat.show()
        
