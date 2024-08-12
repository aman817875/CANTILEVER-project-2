import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        # List to hold expenses
        self.expenses = []

        # StringVars to hold input data
        self.item_name_var = tk.StringVar()  # New variable for Item Name
        self.description_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.date_var = tk.StringVar()

        self.setup_ui()

    def setup_ui(self):
        # Item Name (New Entry)
        tk.Label(self.root, text="Item Name:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.item_name_var).grid(row=0, column=1, padx=10, pady=10)

        # Item Description
        tk.Label(self.root, text="Item Description:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.description_var).grid(row=1, column=1, padx=10, pady=10)

        # Category
        tk.Label(self.root, text="Category:").grid(row=1, column=2, padx=10, pady=10)
        categories = ["Food", "Utilities", "Transportation", "Entertainment", "Miscellaneous"]
        tk.OptionMenu(self.root, self.category_var, *categories).grid(row=1, column=3, padx=10, pady=10)

        # Date
        tk.Label(self.root, text="Date (YYYY-MM-DD):").grid(row=1, column=4, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.date_var).grid(row=1, column=5, padx=10, pady=10)

        # Add Expense Button
        tk.Button(self.root, text="Add Expense", command=self.add_expense).grid(row=1, column=6, padx=10, pady=10)

        # Listbox to display expenses
        self.expense_listbox = tk.Listbox(self.root, width=80, height=10)
        self.expense_listbox.grid(row=2, column=0, columnspan=7, padx=10, pady=10)

        # Edit, Delete, and Save Buttons
        tk.Button(self.root, text="Edit Expense", command=self.edit_expense).grid(row=3, column=2, padx=10, pady=10)
        tk.Button(self.root, text="Delete Expense", command=self.delete_expense).grid(row=3, column=3, padx=10, pady=10)
        tk.Button(self.root, text="Save Expenses", command=self.save_expenses).grid(row=3, column=4, padx=10, pady=10)

        # Total Expenses Label
        self.total_expense_label = tk.Label(self.root, text="Total Expenses: USD 0.00")
        self.total_expense_label.grid(row=4, column=0, columnspan=7, padx=10, pady=10)

        # Show Expenses Chart Button
        tk.Button(self.root, text="Show Expenses Chart", command=self.show_expense_chart).grid(row=5, column=0, columnspan=7, padx=10, pady=10)

    def add_expense(self):
        item_name = self.item_name_var.get()  # Get the item name input
        description = self.description_var.get()
        category = self.category_var.get()
        date = self.date_var.get()
        amount = simpledialog.askfloat("Add Expense", "Enter amount:")
        
        if item_name and description and category and date and amount:
            self.expenses.append({"item_name": item_name, "description": description, "category": category, "date": date, "amount": amount})
            self.update_expense_listbox()
            self.update_total_expense()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields and enter a valid amount.")

    def edit_expense(self):
        selected_expense_index = self.expense_listbox.curselection()
        if selected_expense_index:
            selected_expense = self.expenses[selected_expense_index[0]]
            new_amount = simpledialog.askfloat("Edit Expense", "Enter new amount:", initialvalue=selected_expense["amount"])
            
            if new_amount:
                self.expenses[selected_expense_index[0]]["amount"] = new_amount
                self.update_expense_listbox()
                self.update_total_expense()
        else:
            messagebox.showwarning("Selection Error", "Please select an expense to edit.")

    def delete_expense(self):
        selected_expense_index = self.expense_listbox.curselection()
        if selected_expense_index:
            del self.expenses[selected_expense_index[0]]
            self.update_expense_listbox()
            self.update_total_expense()
        else:
            messagebox.showwarning("Selection Error", "Please select an expense to delete.")

    def save_expenses(self):
        # You can add code here to save the expenses to a file or database
        messagebox.showinfo("Save Expenses", "Expenses have been saved!")

    def show_expense_chart(self):
        if not self.expenses:
            messagebox.showwarning("No Data", "No expenses to show.")
            return

        # Calculate total amount per category
        category_totals = {}
        for expense in self.expenses:
            category = expense["category"]
            amount = expense["amount"]
            if category in category_totals:
                category_totals[category] += amount
            else:
                category_totals[category] = amount

        # Plot the chart using matplotlib
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())

        plt.figure(figsize=(10, 6))
        plt.bar(categories, amounts, color='skyblue')
        plt.xlabel("Category")
        plt.ylabel("Total Amount (USD)")
        plt.title("Total Expenses by Category")
        plt.show()

    def update_expense_listbox(self):
        self.expense_listbox.delete(0, tk.END)
        for expense in self.expenses:
            expense_text = f"{expense['amount']} - {expense['item_name']} - {expense['description']} - {expense['category']} ({expense['date']})"
            self.expense_listbox.insert(tk.END, expense_text)

    def update_total_expense(self):
        total = sum(expense["amount"] for expense in self.expenses)
        self.total_expense_label.config(text=f"Total Expenses: USD {total:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
