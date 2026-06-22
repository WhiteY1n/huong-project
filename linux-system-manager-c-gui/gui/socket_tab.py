from tkinter import ttk, simpledialog
from gui.common import OutputBox
from gui.backend import run_backend, start_echo_server, stop_echo_server, server_status

class SocketTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        left = ttk.Frame(self)
        left.pack(side="left", fill="y", padx=10, pady=10)

        self.output = OutputBox(self)
        self.output.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.status_label = ttk.Label(left, text=f"Server: {server_status()}", wraplength=260)
        self.status_label.pack(pady=8)

        ttk.Button(left, text="Start Echo Server", width=35, command=self.start_server).pack(pady=5)
        ttk.Button(left, text="Stop Echo Server", width=35, command=self.stop_server).pack(pady=5)
        ttk.Button(left, text="Gửi message bằng Client", width=35, command=self.client_send).pack(pady=5)
        ttk.Button(left, text="Cập nhật trạng thái", width=35, command=self.refresh_status).pack(pady=5)

        self.output.set_text(
            "Luồng test socket:\n"
            "1. Bấm Start Echo Server, nhập port 9000.\n"
            "2. Bấm Gửi message bằng Client.\n"
            "3. Host nhập 127.0.0.1, port 9000.\n"
            "4. Nhập message bất kỳ để kiểm tra phản hồi."
        )

    def refresh_status(self):
        self.status_label.config(text=f"Server: {server_status()}")

    def start_server(self):
        port = simpledialog.askstring("Start Server", "Nhập port:", initialvalue="9000")
        if port:
            self.output.set_text(start_echo_server(port))
            self.refresh_status()

    def stop_server(self):
        self.output.set_text(stop_echo_server())
        self.refresh_status()

    def client_send(self):
        host = simpledialog.askstring("Client", "Nhập host:", initialvalue="127.0.0.1")
        if not host:
            return
        port = simpledialog.askstring("Client", "Nhập port:", initialvalue="9000")
        if not port:
            return
        message = simpledialog.askstring("Client", "Nhập message:", initialvalue="Hello from GUI")
        if message:
            self.output.set_text(run_backend(["socket", "client", host, port, message]))
