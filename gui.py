import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as mat
from buget import Budget  # Import the correct Budget class

class BudgetApp:
    def __init__(self, main):
        self.main = main
        self.tracker = Budget()  # Use the Budget class
        self.main.title("Budget Tracker")
        self.main.geometry("900x500")

        self.widgets()
        self.update()

    def widgets(self):
        title = tk.Label(self.main, text="Budget Tracking",
                         font=("Times New Roman", 24, "bold"))
        title.pack()

        frame = tk.Frame(self.main)
        frame.pack(pady=15)

        tk.Label(frame, text="Amount: ").grid(row=0, column=0, padx=5, pady=5)
        self.sum_entry = tk.Entry(frame)
        self.sum_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Description: ").grid(row=1, column=0, padx=5, pady=5)
        self.description_entry = tk.Entry(frame)  # Renamed to description
        self.description_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Type: ").grid(row=2, column=0, padx=5, pady=5)
        self.variable = tk.StringVar()
        self.variable.set("Expense")
        menu = ttk.Combobox(frame, textvariable=self.variable, values=["Income", "Expense"])
        menu.grid(row=2, column=1, padx=5, pady=5)

        add_button = tk.Button(self.main, text="Add", command=self.add_transaction,
                               bg="#4cff57", fg="white", font=("Times New Roman", 18, "bold"), width=10)
        add_button.pack(pady=10)

        self.summary_label = tk.Label(self.main, text="", font=("Times New Roman", 16, "bold"))
        self.summary_label.pack(pady=10)

        graph_button = tk.Button(self.main, text="Show Graphs", command=self.plot_data,
                                 bg="#6be4ba", fg="white", width=15, font=("Times New Roman", 16))
        graph_button.pack(pady=10)

    def add_transaction(self):
        try:
            amount = float(self.sum_entry.get())
            description = self.description_entry.get().strip()
            var_type = self.variable.get().lower()  # Convert type to lowercase to match Budget class

            if not description:
                raise ValueError("The description cannot be empty.")
            if var_type not in ["income", "expense"]:
                raise ValueError("Invalid transaction type selected.")
            
            # Add transaction to the tracker
            success = self.tracker.add_transaction(var_type, amount, description)
            if not success:
                raise ValueError("Failed to add transaction. Please check the input values.")

            # Clear input fields and update the summary
            self.sum_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.update()

            messagebox.showinfo("Success", "Transaction added successfully!")
        except ValueError as error:
            messagebox.showerror("Error", f"Invalid input: {error}")

    def update(self):
        income = self.tracker.income()
        expenses = self.tracker.expense()
        balance = self.tracker.available_budget()
        self.summary_label.config(
            text=f"Income: {income:.2f} RON     Expenses: {expenses:.2f} RON     Balance: {balance:.2f} RON"
        )

    def plot_data(self):
        income = self.tracker.income()
        expenses = self.tracker.expense()
        balance = self.tracker.available_budget()
        transactions = self.tracker.get_transactions()

        # Group expenses by description
        category_summary = {}
        for transaction in transactions:
            if transaction["type"] == "expense":
                description = transaction["description"]
                amount = transaction["amount"]
                if description not in category_summary:
                    category_summary[description] = 0
                category_summary[description] += amount

        if not category_summary:
            messagebox.showwarning("Warning", "No data available for graphs.")
            return

        fig, axes = mat.subplots(1, 2, figsize=(12, 5))

        # Pie chart for expenses by description
        categories = list(category_summary.keys())
        amounts = list(category_summary.values())
        axes[0].pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        axes[0].set_title("Expenses by Description")

        # Bar chart for income, expenses, and balance
        axes[1].bar(["Income", "Expenses", "Balance"], [income, expenses, balance],
                    color=["#3eeb43", "#fa2834", "#1683ca"])
        axes[1].set_title("Financial Overview")
        axes[1].set_ylabel("Amount (RON)")
        axes[1].set_xlabel("Type")

        mat.tight_layout()
        mat.show()