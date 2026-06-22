#!/bin/bash

LOG_FILE="/home/vu/code/huong-project/shell-system-manager-gui/logs/system_health.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "======================================" >> "$LOG_FILE"
echo "Thời gian: $(date)" >> "$LOG_FILE"
echo "--- Bộ nhớ (RAM) ---" >> "$LOG_FILE"
free -h >> "$LOG_FILE"
echo "--- Dung lượng ổ cứng ---" >> "$LOG_FILE"
df -h / >> "$LOG_FILE"
echo "--- Tải CPU (Load Average) ---" >> "$LOG_FILE"
uptime >> "$LOG_FILE"
echo "======================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
