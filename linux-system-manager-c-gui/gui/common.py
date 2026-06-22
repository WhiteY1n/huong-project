import tkinter as tk
from tkinter import ttk

class OutputBox(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.text = tk.Text(self, wrap="word", height=22)
        scrollbar = ttk.Scrollbar(self, command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)

        self.text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def set_text(self, content: str):
        self.text.config(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content)
        self.text.config(state="disabled")
