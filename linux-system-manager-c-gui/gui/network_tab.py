from tkinter import ttk, simpledialog
from gui.common import OutputBox
from gui.backend import run_backend

class NetworkTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        left = ttk.Frame(self)
        left.pack(side="left", fill="y", padx=10, pady=10)

        self.output = OutputBox(self)
        self.output.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ttk.Button(left, text="Xem interfaces", width=35, command=self.interfaces).pack(pady=5)
        ttk.Button(left, text="Xem routes", width=35, command=self.routes).pack(pady=5)
        ttk.Button(left, text="Ping host", width=35, command=self.ping).pack(pady=5)
        ttk.Button(left, text="DNS lookup", width=35, command=self.dns).pack(pady=5)
        ttk.Button(left, text="Xem listening ports", width=35, command=self.ports).pack(pady=5)

    def interfaces(self):
        self.output.set_text(run_backend(["network", "interfaces"]))

    def routes(self):
        self.output.set_text(run_backend(["network", "routes"]))

    def ping(self):
        host = simpledialog.askstring("Ping", "Nhập host/IP:", initialvalue="8.8.8.8")
        if host:
            self.output.set_text(run_backend(["network", "ping", host], timeout=30))

    def dns(self):
        host = simpledialog.askstring("DNS lookup", "Nhập domain:", initialvalue="google.com")
        if host:
            self.output.set_text(run_backend(["network", "dns", host]))

    def ports(self):
        self.output.set_text(run_backend(["network", "ports"]))
