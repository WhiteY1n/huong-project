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
        ttk.Button(left, text="Cập nhật trạng thái", width=35, command=self.refresh_status).pack(pady=5)

        ttk.Separator(left, orient='horizontal').pack(fill='x', pady=15)
        ttk.Label(left, text="--- CLIENT ---", font=("", 10, "bold")).pack(pady=5)

        client_frame = ttk.Frame(left)
        client_frame.pack(fill='x', pady=5)
        
        ttk.Label(client_frame, text="Host:").grid(row=0, column=0, sticky='w', pady=2)
        self.host_entry = ttk.Entry(client_frame, width=25)
        self.host_entry.insert(0, "127.0.0.1")
        self.host_entry.grid(row=0, column=1, pady=2, padx=5)

        ttk.Label(client_frame, text="Port:").grid(row=1, column=0, sticky='w', pady=2)
        self.port_entry = ttk.Entry(client_frame, width=25)
        self.port_entry.insert(0, "9000")
        self.port_entry.grid(row=1, column=1, pady=2, padx=5)

        ttk.Label(client_frame, text="Message:").grid(row=2, column=0, sticky='w', pady=2)
        self.msg_entry = ttk.Entry(client_frame, width=25)
        self.msg_entry.insert(0, "Hello Server")
        self.msg_entry.grid(row=2, column=1, pady=2, padx=5)

        ttk.Button(left, text="Gửi message tới Server", width=35, command=self.client_send).pack(pady=10)

        self.output.set_text(
            "Luồng test socket:\n"
            "1. Bấm Start Echo Server, nhập port 9000.\n"
            "2. Nhập Host, Port và Message ở khu vực CLIENT.\n"
            "3. Bấm 'Gửi message tới Server' để kiểm tra kết quả trả về từ Server."
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
        host = self.host_entry.get().strip()
        port = self.port_entry.get().strip()
        message = self.msg_entry.get().strip()
        
        if not host or not port or not message:
            return
            
        self.output.set_text(run_backend(["socket", "client", host, port, message]))
