import tkinter as tk
from tkinter import messagebox
import random
import string

# Function to generate password
def generate_password():
    length = int(length_entry.get())

    characters = ""
    if var_uppercase.get():
        characters += string.ascii_uppercase
    if var_numbers.get():
        characters += string.digits
    if var_symbols.get():
        characters += string.punctuation
    # Always include lowercase
    characters += string.ascii_lowercase

    if characters == "":
        messagebox.showwarning("Error", "Please select at least one option!")
        return

    password = "".join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# Function to copy password
def copy_password():
    window.clipboard_clear()
    window.clipboard_append(password_entry.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")

# Create window
window = tk.Tk()
window.title("Random Password Generator")
window.geometry("400x300")

# Password length
tk.Label(window, text="Enter Password Length:").pack(pady=5)
length_entry = tk.Entry(window)
length_entry.insert(0, "12")  # Default length
length_entry.pack(pady=5)

# Options
var_uppercase = tk.BooleanVar()
var_numbers = tk.BooleanVar()
var_symbols = tk.BooleanVar()

tk.Checkbutton(window, text="Include Uppercase", variable=var_uppercase).pack()
tk.Checkbutton(window, text="Include Numbers", variable=var_numbers).pack()
tk.Checkbutton(window, text="Include Symbols", variable=var_symbols).pack()

# Generate button
tk.Button(window, text="Generate Password", command=generate_password, bg="green", fg="white").pack(pady=10)

# Show password
password_entry = tk.Entry(window, width=30, font=("Arial", 12))
password_entry.pack(pady=10)

# Copy button
tk.Button(window, text="Copy to Clipboard", command=copy_password, bg="blue", fg="white").pack(pady=5)

window.mainloop()
