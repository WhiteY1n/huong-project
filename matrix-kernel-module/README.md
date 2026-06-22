# Matrix Kernel Module

Chương trình mẫu xây dựng một Linux Kernel Module đơn giản và tích hợp vào hệ thống thông qua `/proc`.

Khi nạp module, hệ thống sẽ tạo file:

```bash
/proc/matrix_module
```

Người dùng có thể đọc file này để xem kết quả xử lý ma trận từ kernel module.

## Cấu trúc

```text
matrix-kernel-module/
├── matrix_kmod.c
├── Makefile
└── README.md
```

## Cài công cụ cần thiết

```bash
sudo apt update
sudo apt install build-essential linux-headers-$(uname -r) -y
```

## Biên dịch

```bash
make
```

Sau khi biên dịch thành công sẽ có file:

```text
matrix_kmod.ko
```

## Nạp module vào kernel

```bash
sudo insmod matrix_kmod.ko
```

## Kiểm tra module đã tích hợp vào hệ thống

```bash
cat /proc/matrix_module
```

## Xem log kernel

```bash
sudo dmesg | tail -n 40
```

## Gỡ module

```bash
sudo rmmod matrix_kmod
```

## Dọn file build

```bash
make clean
```

## Tích hợp bằng modprobe

Cách này đưa module vào thư mục module của hệ thống.

```bash
make
make install
sudo modprobe matrix_kmod
cat /proc/matrix_module
sudo modprobe -r matrix_kmod
```

Nếu muốn xóa module khỏi thư mục hệ thống:

```bash
make remove-installed
```
