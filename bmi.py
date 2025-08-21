import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Store BMI history
bmi_history = []

def calculate_bmi():
    try:
        weight = float(entry_weight.get())
        height = float(entry_height.get()) / 100  # cm to meters
        bmi = round(weight / (height ** 2), 2)

        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

        result_label.config(text=f"BMI: {bmi} ({category})")
        
        # Save history
        bmi_history.append(bmi)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

def show_history():
    if not bmi_history:
        messagebox.showinfo("History", "No BMI data yet.")
        return
    
    plt.plot(bmi_history, marker='o')
    plt.title("BMI History")
    plt.xlabel("Check Number")
    plt.ylabel("BMI Value")
    plt.grid()
    plt.show()

# GUI setup
root = tk.Tk()
root.title("Advanced BMI Calculator")

tk.Label(root, text="Weight (kg):").pack()
entry_weight = tk.Entry(root)
entry_weight.pack()

tk.Label(root, text="Height (cm):").pack()
entry_height = tk.Entry(root)
entry_height.pack()

tk.Button(root, text="Calculate BMI", command=calculate_bmi).pack(pady=5)
tk.Button(root, text="Show History", command=show_history).pack(pady=5)

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()

