import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
from gui.common import OutputBox
from services import cron_service
from config import PROJECT_DIR

class ScheduleTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        form = ttk.LabelFrame(self, text="Thêm tác vụ cron")
        form.pack(fill="x", padx=10, pady=10)

        self.minute = tk.StringVar(value="*/1")
        self.hour = tk.StringVar(value="*")
        self.day = tk.StringVar(value="*")
        self.month = tk.StringVar(value="*")
        self.weekday = tk.StringVar(value="*")
        self.command = tk.StringVar()

        fields = [
            ("Phút", self.minute),
            ("Giờ", self.hour),
            ("Ngày", self.day),
            ("Tháng", self.month),
            ("Thứ", self.weekday),
        ]

        for i, (label, var) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=0, column=i, padx=5, pady=5)
            ttk.Entry(form, textvariable=var, width=10).grid(row=1, column=i, padx=5, pady=5)

        ttk.Label(form, text="Lệnh/script cần chạy").grid(row=2, column=0, columnspan=2, sticky="w", padx=5)
        ttk.Entry(form, textvariable=self.command, width=80).grid(row=3, column=0, columnspan=5, padx=5, pady=5, sticky="we")

        ttk.Button(form, text="Nhập lệnh trực tiếp", command=self.direct_command).grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(form, text="Tạo script mới", command=self.create_script).grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(form, text="Chọn script có sẵn", command=self.choose_script).grid(row=4, column=2, padx=5, pady=5)
        ttk.Button(form, text="Thêm cron", command=self.add_cron).grid(row=4, column=3, padx=5, pady=5)

        actions = ttk.Frame(self)
        actions.pack(fill="x", padx=10, pady=5)

        ttk.Button(actions, text="Xem danh sách cron", command=self.view_jobs).pack(side="left", padx=5)
        ttk.Button(actions, text="Thêm lịch backup", command=self.add_backup).pack(side="left", padx=5)
        ttk.Button(actions, text="Xóa cron theo số thứ tự", command=self.delete_by_number).pack(side="left", padx=5)
        ttk.Button(actions, text="Xóa toàn bộ cron", command=self.delete_all).pack(side="left", padx=5)

        self.output = OutputBox(self)
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

        self.output.set_text(
            "Gợi ý test cron:\n"
            "Phút = */1, giờ = *, ngày = *, tháng = *, thứ = *\n"
            f"Lệnh = /bin/date >> \"{PROJECT_DIR}/test/cron_test.txt\""
        )

    def direct_command(self):
        cmd = simpledialog.askstring(
            "Nhập lệnh trực tiếp",
            "Nhập lệnh cron sẽ chạy:",
            initialvalue=f'/bin/date >> "{PROJECT_DIR}/test/cron_test.txt"'
        )
        if cmd:
            self.command.set(cmd)

    def create_script(self):
        name = simpledialog.askstring("Tên script", "Nhập tên script, ví dụ write_time.sh:")
        if not name:
            return

        win = tk.Toplevel(self)
        win.title("Nhập nội dung script")
        win.geometry("700x450")

        text = tk.Text(win, wrap="word")
        text.pack(fill="both", expand=True, padx=10, pady=10)
        text.insert("1.0", f'/bin/date >> "{PROJECT_DIR}/test/cron_test.txt"\n')

        def save():
            content = text.get("1.0", "end").strip()
            ok, path, cmd = cron_service.create_script(name, content)
            if ok:
                self.command.set(cmd)
                self.output.set_text(f"Đã tạo script:\n{path}\n\nCron command:\n{cmd}")
                win.destroy()

        ttk.Button(win, text="Lưu script", command=save).pack(pady=8)

    def choose_script(self):
        path = filedialog.askopenfilename(
            title="Chọn file script",
            filetypes=[("Shell script", "*.sh"), ("All files", "*.*")]
        )
        if path:
            try:
                self.command.set(cron_service.command_from_existing_script(path))
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    def add_cron(self):
        if not self.command.get().strip():
            messagebox.showwarning("Thiếu dữ liệu", "Bạn chưa nhập lệnh/script cần chạy.")
            return
        result = cron_service.add_cron_job(
            self.minute.get(), self.hour.get(), self.day.get(),
            self.month.get(), self.weekday.get(), self.command.get()
        )
        self.output.set_text(result)

    def view_jobs(self):
        self.output.set_text(cron_service.view_cron_jobs())

    def add_backup(self):
        source = filedialog.askdirectory(title="Chọn thư mục cần sao lưu")
        if not source:
            return
        minute = simpledialog.askstring("Phút", "Nhập phút:", initialvalue="*/1")
        if minute is None:
            return
        hour = simpledialog.askstring("Giờ", "Nhập giờ:", initialvalue="*")
        if hour is None:
            return
        self.output.set_text(cron_service.add_backup_schedule(source, minute, hour))

    def delete_by_number(self):
        jobs = cron_service.get_cron_jobs()
        if not jobs:
            self.output.set_text("Chưa có lịch cron nào.")
            return

        list_text = "\n".join(f"{i + 1}. {job}" for i, job in enumerate(jobs))
        number = simpledialog.askinteger(
            "Xóa cron",
            f"Danh sách cron:\n{list_text}\n\nNhập số thứ tự cần xóa:"
        )
        if number is None:
            return
        if messagebox.askyesno("Xác nhận", f"Xóa cron số {number}?"):
            self.output.set_text(cron_service.delete_cron_by_index(number - 1))

    def delete_all(self):
        if messagebox.askyesno("Cảnh báo", "Bạn có chắc muốn xóa toàn bộ lịch cron không?"):
            self.output.set_text(cron_service.delete_all_cron_jobs())
