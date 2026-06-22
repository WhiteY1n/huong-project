from pathlib import Path
import subprocess
import os
import signal

PROJECT_DIR = Path(__file__).resolve().parents[1]
BIN = PROJECT_DIR / "bin" / "linux_manager"
RUNTIME_DIR = PROJECT_DIR / "runtime"
SERVER_PID_FILE = RUNTIME_DIR / "echo_server.pid"
SERVER_LOG_FILE = RUNTIME_DIR / "echo_server.log"

def run_backend(args, timeout=20):
    if not BIN.exists():
        return "Chưa biên dịch C backend. Hãy chạy lệnh: make"

    try:
        result = subprocess.run(
            [str(BIN)] + args,
            cwd=str(PROJECT_DIR),
            capture_output=True,
            text=True,
            timeout=timeout
        )

        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += "\n" + result.stderr

        return output.strip() if output.strip() else "Thao tác đã thực hiện xong."

    except subprocess.TimeoutExpired:
        return "Lệnh chạy quá lâu và đã bị dừng."
    except Exception as e:
        return f"Lỗi khi chạy backend: {e}"

def start_echo_server(port: str):
    if not BIN.exists():
        return "Chưa biên dịch C backend. Hãy chạy lệnh: make"

    if SERVER_PID_FILE.exists():
        pid = SERVER_PID_FILE.read_text().strip()
        return f"Server có vẻ đang chạy, PID={pid}. Hãy dừng server trước."

    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    log = open(SERVER_LOG_FILE, "a", encoding="utf-8")

    proc = subprocess.Popen(
        [str(BIN), "socket", "server", port],
        cwd=str(PROJECT_DIR),
        stdout=log,
        stderr=log,
        text=True
    )

    SERVER_PID_FILE.write_text(str(proc.pid))
    return f"Đã khởi động Echo Server ở port {port}, PID={proc.pid}"

def stop_echo_server():
    if not SERVER_PID_FILE.exists():
        return "Không có server đang chạy."

    try:
        pid = int(SERVER_PID_FILE.read_text().strip())
        os.kill(pid, signal.SIGTERM)
        SERVER_PID_FILE.unlink(missing_ok=True)
        return f"Đã dừng server PID={pid}"
    except Exception as e:
        return f"Dừng server thất bại: {e}"

def server_status():
    if not SERVER_PID_FILE.exists():
        return "Chưa chạy"

    try:
        pid = int(SERVER_PID_FILE.read_text().strip())
        os.kill(pid, 0)
        return f"Đang chạy, PID={pid}"
    except Exception:
        SERVER_PID_FILE.unlink(missing_ok=True)
        return "Chưa chạy"
