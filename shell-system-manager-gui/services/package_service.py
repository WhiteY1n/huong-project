import re
from utils.command_runner import run_command, q
from utils.logger import write_log

DANGEROUS_PACKAGES = {
    "bash", "sudo", "apt", "dpkg", "coreutils", "systemd",
    "libc6", "ubuntu-minimal", "ubuntu-standard", "ubuntu-desktop"
}

def valid_package_name(package: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9._+-]+$", package))

def is_dangerous_package(package: str) -> bool:
    return package in DANGEROUS_PACKAGES or package.startswith("linux-image")

def update_package_list() -> str:
    write_log("Cập nhật danh sách gói")
    return run_command("sudo apt update", require_sudo=True)

def search_package(keyword: str) -> str:
    write_log(f"Tìm kiếm gói apt: {keyword}")
    return run_command(f"apt-cache search {q(keyword)} | head -n 50")

def check_package(package: str) -> str:
    if not valid_package_name(package):
        return "Tên gói không hợp lệ."
    write_log(f"Kiểm tra gói: {package}")
    return run_command(f"dpkg -s {q(package)}")

def install_package(package: str) -> str:
    if not valid_package_name(package):
        return "Tên gói không hợp lệ."
    write_log(f"Cài đặt gói: {package}")
    return run_command(f"sudo apt install -y {q(package)}", require_sudo=True)

def installed_packages_by_keyword(keyword: str) -> str:
    write_log(f"Tìm gói đã cài: {keyword}")
    result = run_command(f"dpkg -l | grep -i -- {q(keyword)}")
    return result if result.strip() else "Không tìm thấy gói đã cài phù hợp."

def remove_package(package: str) -> str:
    if not valid_package_name(package):
        return "Tên gói không hợp lệ."
    if is_dangerous_package(package):
        return f"Không cho phép gỡ gói hệ thống quan trọng: {package}"
    write_log(f"Gỡ bỏ gói: {package}")
    return run_command(f"sudo apt remove -y {q(package)}", require_sudo=True)

def purge_package(package: str) -> str:
    if not valid_package_name(package):
        return "Tên gói không hợp lệ."
    if is_dangerous_package(package):
        return f"Không cho phép gỡ gói hệ thống quan trọng: {package}"
    write_log(f"Gỡ bỏ hoàn toàn gói: {package}")
    return run_command(f"sudo apt purge -y {q(package)}", require_sudo=True)

def autoremove() -> str:
    write_log("apt autoremove")
    return run_command("sudo apt autoremove -y", require_sudo=True)
