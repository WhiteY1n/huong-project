#!/bin/bash

# Kiểm tra kết nối mạng bằng cách ping tới Google DNS
LOG_FILE="/home/vu/code/huong-project/shell-system-manager-gui/logs/network_ping.log"
mkdir -p "$(dirname "$LOG_FILE")"

if ping -c 3 8.8.8.8 &> /dev/null; then
    echo "[$(date)] KẾT NỐI MẠNG: OK" >> "$LOG_FILE"
else
    echo "[$(date)] KẾT NỐI MẠNG: LỖI (Không thể ping 8.8.8.8)" >> "$LOG_FILE"
fi
