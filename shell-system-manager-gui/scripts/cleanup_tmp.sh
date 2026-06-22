#!/bin/bash

# Dọn dẹp các file tạm trong thư mục test
LOG_FILE="/home/vu/code/huong-project/shell-system-manager-gui/logs/cleanup.log"
TARGET_DIR="/home/vu/code/huong-project/shell-system-manager-gui/test"

mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$TARGET_DIR"

# Tạo một vài file tạm để test nếu thư mục trống
touch "$TARGET_DIR/dummy_1.tmp"
touch "$TARGET_DIR/dummy_2.tmp"

echo "[$(date)] Bắt đầu dọn dẹp các file .tmp trong $TARGET_DIR" >> "$LOG_FILE"

# Tìm và xóa các file kết thúc bằng .tmp
find "$TARGET_DIR" -type f -name "*.tmp" -exec rm -f {} \; -exec echo "  Đã xóa: {}" >> "$LOG_FILE" \;

echo "[$(date)] Hoàn thành dọn dẹp" >> "$LOG_FILE"
echo "-----------------------------------" >> "$LOG_FILE"
