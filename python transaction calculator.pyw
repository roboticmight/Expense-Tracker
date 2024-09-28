""" The program will ask a user to input the item, amount, and date by using
    GUI interface afterwards it will store it as a file for records for later
    viewing upon the request of the user. User can manually log files with
    the help of the File that is written inside the program.
    Created by Dmitriy Kononenko 08/30/2024
"""
import tkinter as tk
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('expenses.db')
c = conn.cursor()

# Create a table to store expenses
c.execute('''CREATE TABLE IF NOT EXISTS expenses
             (id INTEGER PRIMARY KEY, item TEXT, cost REAL, date TEXT)''')

# Function to add an expense
def add_expense():
    item = item_entry.get()
    cost = float(cost_entry.get())
    date = date_entry.get()
    
    c.execute("INSERT INTO expenses (item, cost, date) VALUES (?, ?, ?)", (item, cost, date))
    conn.commit()
    
    item_entry.delete(0, tk.END)
    cost_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    
    status_label.config(text="Expense added successfully!")
    view_expenses()

# Function to view all expenses with color coding for costs
def view_expenses():
    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()
    
    expenses_list.delete(0, tk.END)  # Clear the listbox
    
    for expense in expenses:
        cost = float(expense[2])  # Convert the cost to a float
        color = "black" if cost <= 50 else "red"
        
        item_text = f"ID: {expense[0]}, Item: {expense[1]}, Cost: {expense[2]}, Date: {expense[3]}"
        
        expenses_list.insert(tk.END, item_text)
        
        item_index = expenses_list.size() - 1  # Get the index of the last inserted item
        expenses_list.itemconfig(item_index, {'fg': color})

# Function to clear all input fields
def clear_inputs():
    item_entry.delete(0, tk.END)
    cost_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    status_label.config(text="Inputs cleared!")

# Function to delete a specific expense by ID
def delete_expense():
    expense_id = int(delete_entry.get())
    c.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    status_label.config(text=f"Expense with ID {expense_id} deleted!")
    view_expenses()

# Create the GUI
root = tk.Tk()
root.title("Expense Tracker")

# Create a frame to hold all the widgets
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=1)

item_label = tk.Label(frame, text="Item:")
item_label.pack()

item_entry = tk.Entry(frame)
item_entry.pack()

cost_label = tk.Label(frame, text="Cost:")
cost_label.pack()

cost_entry = tk.Entry(frame)
cost_entry.pack()

date_label = tk.Label(frame, text="Date (mm-dd-yyyy):")
date_label.pack()

date_entry = tk.Entry(frame)
date_entry.pack()

add_button = tk.Button(frame, text="Add Expense", command=add_expense, bg="green")
add_button.pack()

delete_label = tk.Label(frame, text="Delete Expense by ID:")
delete_label.pack()

delete_entry = tk.Entry(frame)
delete_entry.pack()

delete_button = tk.Button(frame, text="Delete Expense", command=delete_expense, bg="red")
delete_button.pack()

clear_button = tk.Button(frame, text="Clear Inputs", command=clear_inputs, bg="blue")
clear_button.pack()

status_label = tk.Label(frame, text="")
status_label.pack()

expenses_list = tk.Listbox(frame, height=10, width=80)
expenses_list.pack(fill=tk.BOTH, expand=1)

view_expenses()

root.mainloop()

# Close the database connection when done
conn.close()
