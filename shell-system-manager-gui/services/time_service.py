import subprocess
from utils.command_runner import run_command, q
from utils.logger import write_log

def current_time() -> str:
    write_log("Xem thời gian hiện tại")
    return run_command("date")

def time_info() -> str:
    write_log("Xem thông tin thời gian hệ thống")
    return run_command("timedatectl")

def current_timezone() -> str:
    write_log("Xem múi giờ hiện tại")
    return run_command("timedatectl show --property=Timezone --value")

def search_timezone(keyword: str) -> str:
    result = run_command(f"timedatectl list-timezones | grep -i {q(keyword)}")
    write_log(f"Tìm múi giờ: {keyword}")
    return result if result.strip() else "Không tìm thấy múi giờ phù hợp."

def set_timezone(timezone: str) -> str:
    valid = run_command(f"timedatectl list-timezones | grep -Fx {q(timezone)}")
    if not valid or "Không tìm" in valid:
        return "Múi giờ không hợp lệ."
    write_log(f"Đổi múi giờ: {timezone}")
    return run_command(f"sudo timedatectl set-timezone {q(timezone)}", require_sudo=True)

def set_manual_time(new_time: str) -> str:
    write_log(f"Đặt thời gian thủ công: {new_time}")
    command = f"sudo timedatectl set-ntp false && sudo timedatectl set-time {q(new_time)}"
    return run_command(command, require_sudo=True)

def set_ntp(enable: bool) -> str:
    value = "true" if enable else "false"
    write_log(f"{'Bật' if enable else 'Tắt'} NTP")
    return run_command(f"sudo timedatectl set-ntp {value}", require_sudo=True)
