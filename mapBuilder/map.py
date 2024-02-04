import tkinter as tk
import tk_tools

window = tk.Tk()

for i in range(3):
    for j in range(3):
        frame = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=1
        )
        frame.grid(row=i, column=j, padx=5, pady=5)
        label = tk.Button(master=frame, text=f"Row {i}\nColumn {j}")
        label.pack()

window.mainloop()