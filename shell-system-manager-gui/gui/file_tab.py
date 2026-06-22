import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
from gui.common import OutputBox
from services import file_service

class FileTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        left = ttk.Frame(self)
        left.pack(side="left", fill="y", padx=10, pady=10)

        self.output = OutputBox(self)
        self.output.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        buttons = [
            ("Xem danh sách file/thư mục", self.list_items),
            ("Tạo file mới", self.create_file),
            ("Tạo thư mục mới", self.create_folder),
            ("Sao chép file/thư mục", self.copy_item),
            ("Di chuyển hoặc đổi tên", self.move_item),
            ("Xóa file/thư mục", self.delete_item),
            ("Tìm kiếm file", self.search_file),
            ("Xem nội dung file", self.read_file),
        ]

        for text, command in buttons:
            ttk.Button(left, text=text, width=30, command=command).pack(pady=5)

    def list_items(self):
        folder = filedialog.askdirectory(title="Chọn thư mục cần xem")
        if folder:
            self.output.set_text(file_service.list_items(folder))

    def create_file(self):
        path = simpledialog.askstring("Tạo file", "Nhập đường dẫn file cần tạo:")
        if path:
            self.output.set_text(file_service.create_file(path))

    def create_folder(self):
        path = simpledialog.askstring("Tạo thư mục", "Nhập đường dẫn thư mục cần tạo:")
        if path:
            self.output.set_text(file_service.create_folder(path))

    def copy_item(self):
        source = filedialog.askopenfilename(title="Chọn file nguồn")
        if not source:
            source = filedialog.askdirectory(title="Hoặc chọn thư mục nguồn")
        if not source:
            return
        destination = filedialog.askdirectory(title="Chọn thư mục đích")
        if destination:
            self.output.set_text(file_service.copy_item(source, destination))

    def move_item(self):
        source = filedialog.askopenfilename(title="Chọn file/thư mục nguồn")
        if not source:
            source = filedialog.askdirectory(title="Hoặc chọn thư mục nguồn")
        if not source:
            return
        destination = simpledialog.askstring(
            "Di chuyển/đổi tên",
            "Nhập đường dẫn mới hoặc tên mới:"
        )
        if destination:
            self.output.set_text(file_service.move_item(source, destination))

    def delete_item(self):
        target = filedialog.askopenfilename(title="Chọn file cần xóa")
        if not target:
            target = filedialog.askdirectory(title="Hoặc chọn thư mục cần xóa")
        if not target:
            return
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa?\n{target}"):
            self.output.set_text(file_service.delete_item(target))

    def search_file(self):
        folder = filedialog.askdirectory(title="Chọn thư mục tìm kiếm")
        if not folder:
            return
        keyword = simpledialog.askstring("Tìm kiếm", "Nhập từ khóa tên file:")
        if keyword:
            self.output.set_text(file_service.search_file(folder, keyword))

    def read_file(self):
        path = filedialog.askopenfilename(title="Chọn file cần xem")
        if path:
            self.output.set_text(file_service.read_file(path))
