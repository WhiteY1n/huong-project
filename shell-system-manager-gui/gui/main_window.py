import tkinter as tk
from tkinter import ttk
from gui.file_tab import FileTab
from gui.schedule_tab import ScheduleTab
from gui.time_tab import TimeTab
from gui.package_tab import PackageTab

class SystemManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Shell System Manager - Python GUI")
        self.geometry("950x650")
        self.minsize(850, 550)

        title = ttk.Label(
            self,
            text="CHƯƠNG TRÌNH QUẢN LÝ HỆ THỐNG",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        notebook.add(FileTab(notebook), text="Quản lý file")
        notebook.add(ScheduleTab(notebook), text="Lập lịch cron")
        notebook.add(TimeTab(notebook), text="Thời gian hệ thống")
        notebook.add(PackageTab(notebook), text="Cài/Gỡ chương trình")
