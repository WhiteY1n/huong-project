from tkinter import ttk, simpledialog, messagebox
from gui.common import OutputBox
from gui.backend import run_backend

class ProcessTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        left = ttk.Frame(self)
        left.pack(side="left", fill="y", padx=10, pady=10)

        self.output = OutputBox(self)
        self.output.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ttk.Button(left, text="Xem danh sách tiến trình", width=35, command=self.list_process).pack(pady=5)
        ttk.Button(left, text="Top tiến trình CPU cao", width=35, command=self.top_process).pack(pady=5)
        ttk.Button(left, text="Tìm tiến trình theo từ khóa", width=35, command=self.search_process).pack(pady=5)
        ttk.Button(left, text="Xem chi tiết PID", width=35, command=self.detail_process).pack(pady=5)
        ttk.Button(left, text="Kill tiến trình", width=35, command=self.kill_process).pack(pady=5)

    def list_process(self):
        self.output.set_text(run_backend(["process", "list"]))

    def top_process(self):
        self.output.set_text(run_backend(["process", "top"]))

    def search_process(self):
        keyword = simpledialog.askstring("Tìm tiến trình", "Nhập từ khóa, ví dụ: bash, ssh, python")
        if keyword:
            self.output.set_text(run_backend(["process", "search", keyword]))

    def detail_process(self):
        pid = simpledialog.askstring("Chi tiết PID", "Nhập PID:")
        if pid:
            self.output.set_text(run_backend(["process", "detail", pid]))

    def kill_process(self):
        pid = simpledialog.askstring("Kill PID", "Nhập PID cần kill:")
        if pid and messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn gửi SIGTERM tới PID {pid}?"):
            self.output.set_text(run_backend(["process", "kill", pid]))
