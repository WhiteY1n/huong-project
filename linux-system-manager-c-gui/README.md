# linux-system-manager-c-gui

## 1. Mục tiêu

Project phục vụ bài:

**Lập trình quản lý tiến trình, file, socket và network trong Ubuntu**

Phần xử lý chính viết bằng **C**.  
Phần giao diện viết bằng **Python Tkinter**, tương tự kiểu giao diện Python của project Shell System Manager.

## 2. Luồng hoạt động

```text
Python Tkinter GUI
    ↓
Gọi chương trình C đã biên dịch: bin/linux_manager
    ↓
C backend xử lý process/file/socket/network
    ↓
Trả kết quả về giao diện
```

## 3. Cấu trúc source code

```text
linux-system-manager-c-gui/
├── src/
│   └── linux_manager.c
│
├── gui/
│   ├── main_window.py
│   ├── backend.py
│   ├── common.py
│   ├── process_tab.py
│   ├── file_tab.py
│   ├── socket_tab.py
│   └── network_tab.py
│
├── bin/
├── logs/
├── runtime/
├── test/
├── reports/
├── app.py
├── Makefile
├── requirements.txt
└── README.md
```

## 4. Cài đặt

Trên Ubuntu Desktop:

```bash
sudo apt update
sudo apt install gcc make python3 python3-tk iproute2 iputils-ping -y
```

## 5. Biên dịch C backend

```bash
make
```

Sau khi biên dịch sẽ có:

```text
bin/linux_manager
```

## 6. Chạy giao diện

```bash
python3 app.py
```

Hoặc:

```bash
make run-gui
```

## 7. Lưu ý quan trọng

Giao diện Tkinter cần môi trường đồ họa.  
Nếu bạn dùng Ubuntu Server không có Desktop, chương trình sẽ lỗi:

```text
no display name and no $DISPLAY environment variable
```

Muốn chạy Tkinter GUI, cần chạy trên Ubuntu Desktop/VMware có giao diện.

Nếu chỉ có Ubuntu Server, nên dùng Web GUI hoặc terminal GUI như `dialog/whiptail`.

## 8. Test backend C trực tiếp

### Process

```bash
./bin/linux_manager process list
./bin/linux_manager process search bash
./bin/linux_manager process detail 1234
./bin/linux_manager process top
```

### File

```bash
./bin/linux_manager file list test
./bin/linux_manager file info test/sample.txt
./bin/linux_manager file create-file test/demo.txt
./bin/linux_manager file create-dir test/demo_folder
./bin/linux_manager file view test/sample.txt
```

### Socket

Terminal 1:

```bash
./bin/linux_manager socket server 9000
```

Terminal 2:

```bash
./bin/linux_manager socket client 127.0.0.1 9000 "Hello Server"
```

### Network

```bash
./bin/linux_manager network interfaces
./bin/linux_manager network routes
./bin/linux_manager network ping 8.8.8.8
./bin/linux_manager network dns google.com
./bin/linux_manager network ports
```
