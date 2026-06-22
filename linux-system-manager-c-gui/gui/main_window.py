import tkinter as tk
from tkinter import ttk
from gui.process_tab import ProcessTab
from gui.file_tab import FileTab
from gui.socket_tab import SocketTab
from gui.network_tab import NetworkTab

class LinuxSystemManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Linux System Manager C - Python GUI")
        self.geometry("950x650")
        self.minsize(850, 560)

        title = ttk.Label(
            self,
            text="LINUX SYSTEM MANAGER C",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        subtitle = ttk.Label(
            self,
            text="Quản lý tiến trình, file, socket và network trong Ubuntu"
        )
        subtitle.pack(pady=2)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        notebook.add(ProcessTab(notebook), text="Tiến trình")
        notebook.add(FileTab(notebook), text="File")
        notebook.add(SocketTab(notebook), text="Socket")
        notebook.add(NetworkTab(notebook), text="Network")
