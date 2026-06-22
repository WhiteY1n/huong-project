from tkinter import ttk, filedialog, simpledialog, messagebox
from gui.common import OutputBox
from gui.backend import run_backend, PROJECT_DIR

class FileTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        left = ttk.Frame(self)
        left.pack(side="left", fill="y", padx=10, pady=10)

        self.output = OutputBox(self)
        self.output.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ttk.Button(left, text="Xem danh sách thư mục", width=35, command=self.list_dir).pack(pady=5)
        ttk.Button(left, text="Xem thông tin file/thư mục", width=35, command=self.info_path).pack(pady=5)
        ttk.Button(left, text="Tạo file", width=35, command=self.create_file).pack(pady=5)
        ttk.Button(left, text="Tạo thư mục", width=35, command=self.create_dir).pack(pady=5)
        ttk.Button(left, text="Sao chép", width=35, command=self.copy_item).pack(pady=5)
        ttk.Button(left, text="Di chuyển/đổi tên", width=35, command=self.move_item).pack(pady=5)
        ttk.Button(left, text="Xem nội dung file", width=35, command=self.view_file).pack(pady=5)
        ttk.Button(left, text="Xóa file/thư mục", width=35, command=self.delete_item).pack(pady=5)

        self.output.set_text(
            "Gợi ý test:\n"
            f"Project dir: {PROJECT_DIR}\n"
            f"File mẫu: {PROJECT_DIR}/test/sample.txt"
        )

    def list_dir(self):
        path = filedialog.askdirectory(title="Chọn thư mục cần xem")
        if path:
            self.output.set_text(run_backend(["file", "list", path]))

    def info_path(self):
        path = filedialog.askopenfilename(title="Chọn file cần xem thông tin")
        if not path:
            path = filedialog.askdirectory(title="Hoặc chọn thư mục")
        if path:
            self.output.set_text(run_backend(["file", "info", path]))

    def create_file(self):
        path = simpledialog.askstring("Tạo file", "Nhập đường dẫn file cần tạo:")
        if path:
            self.output.set_text(run_backend(["file", "create-file", path]))

    def create_dir(self):
        path = simpledialog.askstring("Tạo thư mục", "Nhập đường dẫn thư mục cần tạo:")
        if path:
            self.output.set_text(run_backend(["file", "create-dir", path]))

    def copy_item(self):
        src = filedialog.askopenfilename(title="Chọn file nguồn")
        if not src:
            src = filedialog.askdirectory(title="Hoặc chọn thư mục nguồn")
        if not src:
            return
        dst = simpledialog.askstring("Đường dẫn đích", "Nhập đường dẫn đích:")
        if dst:
            self.output.set_text(run_backend(["file", "copy", src, dst]))

    def move_item(self):
        src = filedialog.askopenfilename(title="Chọn file nguồn")
        if not src:
            src = filedialog.askdirectory(title="Hoặc chọn thư mục nguồn")
        if not src:
            return
        dst = simpledialog.askstring("Đường dẫn mới", "Nhập đường dẫn mới hoặc tên mới:")
        if dst:
            self.output.set_text(run_backend(["file", "move", src, dst]))

    def view_file(self):
        path = filedialog.askopenfilename(title="Chọn file cần xem")
        if path:
            self.output.set_text(run_backend(["file", "view", path]))

    def delete_item(self):
        path = filedialog.askopenfilename(title="Chọn file cần xóa")
        if not path:
            path = filedialog.askdirectory(title="Hoặc chọn thư mục cần xóa")
        if path and messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa?\n{path}"):
            self.output.set_text(run_backend(["file", "delete", path]))
