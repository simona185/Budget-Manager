import tkinter as tk

from gui import BudgetApp  

def main():
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
