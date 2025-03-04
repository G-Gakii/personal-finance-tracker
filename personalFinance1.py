import tkinter as tk
from tkinter import ttk, messagebox

class FinanceTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Personal Finance Tracker")
        self.label=tk.Label(self.root, text="Personal Finance Tracker",font=("Arial",18))
        self.root.geometry("600x400")
        
        # Transactions list
        self.transactions = []
        
        # Input fields
        tk.Label(self.root, text="Category:").grid(row=0, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.root, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self.root, text="Date:").grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Income/Expense selection
        self.type_var = tk.StringVar(value="Income")
        tk.Radiobutton(self.root, text="Income", variable=self.type_var, value="Income").grid(row=3, column=0)
        tk.Radiobutton(self.root, text="Expense", variable=self.type_var, value="Expense").grid(row=3, column=1)
        
        # Buttons
        tk.Button(self.root, text="Add Transaction", command=self.add_transaction).grid(row=4, column=0, columnspan=2, pady=5)
        
        # Filter by category
        tk.Label(self.root, text="Filter by Category:").grid(row=5, column=0, padx=5, pady=5)
        self.filter_entry = tk.Entry(self.root)
        self.filter_entry.grid(row=5, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Filter", command=self.filter_transactions).grid(row=5, column=2, padx=5, pady=5)
        
        # Transactions display 
        columns = ("Category", "Amount", "Type", "Date")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.grid(row=6, column=0, columnspan=3, padx=5, pady=5)
        
        # Delete selected button
        tk.Button(self.root, text="Delete Selected", command=self.delete_selected_transaction).grid(row=7, column=0, columnspan=3, pady=5)
        
        # Summary labels
        self.total_income_label = tk.Label(self.root, text="Total Income: 0")
        self.total_income_label.grid(row=8, column=0, pady=5)
        
        self.total_expense_label = tk.Label(self.root, text="Total Expenses: 0")
        self.total_expense_label.grid(row=8, column=1, pady=5)
        
        self.balance_label = tk.Label(self.root, text="Balance: 0")
        self.balance_label.grid(row=8, column=2, pady=5)
        
        self.root.mainloop()
    
    def add_transaction(self):
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        type_ = self.type_var.get()
        
        if not category or not amount or not date:
            messagebox.showerror("Input Error", "All fields are required!")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number!")
            return
        
        transaction = (category, amount, type_, date)
        self.transactions.append(transaction)
        self.tree.insert("", tk.END, values=transaction)
        
        self.update_summary()
    
    def delete_selected_transaction(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Delete Error", "Please select a transaction to delete!")
            return
        
        values = self.tree.item(selected_item[0], "values")
        self.transactions = [t for t in self.transactions if t != values]
        self.tree.delete(selected_item[0])
        
        self.update_summary()
    
    def update_summary(self):
        total_income = sum(amount for category, amount, type_, date in self.transactions if type_ == "Income")
        total_expense = sum(amount for category, amount, type_, date in self.transactions if type_ == "Expense")
        balance = total_income - total_expense
        
        self.total_income_label.config(text=f"Total Income: {total_income}")
        self.total_expense_label.config(text=f"Total Expenses: {total_expense}")
        self.balance_label.config(text=f"Balance: {balance}")
    
    def filter_transactions(self):
        filter_text = self.filter_entry.get().strip().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for transaction in self.transactions:
            if filter_text in transaction[0].lower():
                self.tree.insert("", tk.END, values=transaction)

FinanceTracker()
