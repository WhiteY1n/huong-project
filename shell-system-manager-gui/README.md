# Shell System Manager - Python GUI

## 1. Giới thiệu

Đây là phiên bản giao diện đồ họa của project quản lý hệ thống Linux.  
Chương trình được viết bằng Python Tkinter và sử dụng các lệnh hệ thống Linux phía sau như `ls`, `find`, `crontab`, `timedatectl`, `apt`.

Các chức năng chính:

- Quản lý file/thư mục
- Lập lịch tác vụ bằng cron
- Sao lưu thư mục tự động
- Thiết lập thời gian hệ thống
- Cài đặt/gỡ bỏ chương trình bằng apt

## 2. Cấu trúc thư mục

```text
shell-system-manager-gui/
├── app.py
├── config.py
├── README.md
├── requirements.txt
│
├── gui/
│   ├── main_window.py
│   ├── common.py
│   ├── file_tab.py
│   ├── schedule_tab.py
│   ├── time_tab.py
│   └── package_tab.py
│
├── services/
│   ├── file_service.py
│   ├── cron_service.py
│   ├── time_service.py
│   └── package_service.py
│
├── utils/
│   ├── command_runner.py
│   └── logger.py
│
├── logs/
├── backup/
├── scripts/
└── test/
```

## 3. Cài đặt

Trên Ubuntu, cài Tkinter nếu chưa có:

```bash
sudo apt install python3-tk -y
```

## 4. Chạy chương trình

Đứng trong thư mục project:

```bash
python3 app.py
```

Nếu các chức năng `apt` hoặc `timedatectl` báo cần quyền sudo, chạy trước:

```bash
sudo -v
```

Sau đó quay lại app và chạy lại chức năng.

## 5. Kiểm thử nhanh

### Test cron ghi ngày giờ

Vào tab **Lập lịch cron**.

Nhập:

```text
Phút = */1
Giờ = *
Ngày = *
Tháng = *
Thứ = *
```

Chọn **Nhập lệnh trực tiếp** và nhập:

```bash
/bin/date >> "/đường/dẫn/project/test/cron_test.txt"
```

Sau 1 phút kiểm tra file `test/cron_test.txt`.

### Test backup

Vào tab **Lập lịch cron** → **Thêm lịch backup**.  
Chọn thư mục `test/`, đặt:

```text
Phút = */1
Giờ = *
```

Sau 1–2 phút kiểm tra thư mục `backup/`.

## 6. Lưu ý

- GUI nên chạy trực tiếp trong Ubuntu Desktop/VMware.
- Nếu chạy qua SSH từ Windows, cửa sổ Tkinter thường không hiện nếu chưa cấu hình X11 forwarding.
- Với cron, nên dùng đường dẫn tuyệt đối.
- Sau khi test cron mỗi phút, nên xóa cron để tránh tác vụ chạy liên tục.
