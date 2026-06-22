import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from gui.common import OutputBox
from services import time_service

class TimeTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        left = ttk.Frame(self)
        left.pack(side="left", fill="y", padx=10, pady=10)

        self.output = OutputBox(self)
        self.output.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        buttons = [
            ("Xem thời gian hiện tại", self.current_time),
            ("Xem thông tin thời gian hệ thống", self.time_info),
            ("Xem múi giờ hiện tại", self.current_timezone),
            ("Tìm kiếm múi giờ", self.search_timezone),
            ("Đổi múi giờ", self.set_timezone),
            ("Đặt thời gian thủ công", self.set_manual_time),
            ("Bật NTP", lambda: self.set_ntp(True)),
            ("Tắt NTP", lambda: self.set_ntp(False)),
        ]

        for text, command in buttons:
            ttk.Button(left, text=text, width=35, command=command).pack(pady=5)

    def current_time(self):
        self.output.set_text(time_service.current_time())

    def time_info(self):
        self.output.set_text(time_service.time_info())

    def current_timezone(self):
        self.output.set_text(time_service.current_timezone())

    def search_timezone(self):
        keyword = simpledialog.askstring("Tìm múi giờ", "Nhập từ khóa, ví dụ Ho_Chi_Minh:")
        if keyword:
            self.output.set_text(time_service.search_timezone(keyword))

    def set_timezone(self):
        timezone = simpledialog.askstring("Đổi múi giờ", "Nhập múi giờ, ví dụ Asia/Ho_Chi_Minh:")
        if timezone and messagebox.askyesno("Xác nhận", f"Đổi múi giờ thành {timezone}?"):
            self.output.set_text(time_service.set_timezone(timezone))

    def set_manual_time(self):
        value = simpledialog.askstring(
            "Đặt thời gian",
            "Nhập thời gian dạng YYYY-MM-DD HH:MM:SS"
        )
        if value and messagebox.askyesno("Xác nhận", f"Đặt thời gian thành {value}?"):
            self.output.set_text(time_service.set_manual_time(value))

    def set_ntp(self, enable: bool):
        action = "bật" if enable else "tắt"
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn {action} NTP không?"):
            self.output.set_text(time_service.set_ntp(enable))
