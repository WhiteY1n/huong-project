import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from gui.common import OutputBox
from services import package_service

class PackageTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        left = ttk.Frame(self)
        left.pack(side="left", fill="y", padx=10, pady=10)

        self.output = OutputBox(self)
        self.output.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        install_label = ttk.Label(left, text="Cài đặt chương trình", font=("Arial", 11, "bold"))
        install_label.pack(pady=5)

        ttk.Button(left, text="Cập nhật danh sách gói", width=35, command=self.update).pack(pady=4)
        ttk.Button(left, text="Tìm kiếm gói", width=35, command=self.search).pack(pady=4)
        ttk.Button(left, text="Kiểm tra gói đã cài", width=35, command=self.check).pack(pady=4)
        ttk.Button(left, text="Cài đặt gói", width=35, command=self.install).pack(pady=4)

        ttk.Separator(left).pack(fill="x", pady=12)

        remove_label = ttk.Label(left, text="Gỡ bỏ chương trình", font=("Arial", 11, "bold"))
        remove_label.pack(pady=5)

        ttk.Button(left, text="Tìm gói đã cài theo từ khóa", width=35, command=self.installed_by_keyword).pack(pady=4)
        ttk.Button(left, text="Gỡ bỏ gói", width=35, command=self.remove).pack(pady=4)
        ttk.Button(left, text="Gỡ bỏ hoàn toàn", width=35, command=self.purge).pack(pady=4)
        ttk.Button(left, text="Autoremove", width=35, command=self.autoremove).pack(pady=4)

    def ask_package(self, title: str) -> str | None:
        return simpledialog.askstring(title, "Nhập tên gói, ví dụ: tree")

    def update(self):
        self.output.set_text(package_service.update_package_list())

    def search(self):
        keyword = simpledialog.askstring("Tìm kiếm", "Nhập từ khóa, ví dụ: tree")
        if keyword:
            self.output.set_text(package_service.search_package(keyword))

    def check(self):
        package = self.ask_package("Kiểm tra gói")
        if package:
            self.output.set_text(package_service.check_package(package))

    def install(self):
        package = self.ask_package("Cài đặt gói")
        if package and messagebox.askyesno("Xác nhận", f"Cài đặt gói {package}?"):
            self.output.set_text(package_service.install_package(package))

    def installed_by_keyword(self):
        keyword = simpledialog.askstring("Tìm gói đã cài", "Nhập từ khóa:")
        if keyword:
            self.output.set_text(package_service.installed_packages_by_keyword(keyword))

    def remove(self):
        package = self.ask_package("Gỡ bỏ gói")
        if package and messagebox.askyesno("Xác nhận", f"Gỡ bỏ gói {package}?"):
            self.output.set_text(package_service.remove_package(package))

    def purge(self):
        package = self.ask_package("Gỡ bỏ hoàn toàn")
        if package and messagebox.askyesno("Xác nhận", f"Gỡ bỏ hoàn toàn gói {package}?"):
            self.output.set_text(package_service.purge_package(package))

    def autoremove(self):
        if messagebox.askyesno("Xác nhận", "Chạy sudo apt autoremove -y?"):
            self.output.set_text(package_service.autoremove())
