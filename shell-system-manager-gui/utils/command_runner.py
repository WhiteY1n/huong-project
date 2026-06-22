import subprocess
import shlex

def run_command(command: str, require_sudo: bool = False) -> str:
    """
    Chạy lệnh Linux và trả về stdout/stderr để hiển thị lên GUI.
    Với lệnh cần sudo, nên chạy trước trong terminal:
        sudo -v
    rồi mở lại/chạy lại chức năng trong app.
    """
    if require_sudo:
        check = subprocess.run(
            "sudo -n true",
            shell=True,
            capture_output=True,
            text=True
        )
        if check.returncode != 0:
            return (
                "Chức năng này cần quyền sudo.\n\n"
                "Cách xử lý:\n"
                "1. Mở Terminal trong Ubuntu.\n"
                "2. Chạy lệnh: sudo -v\n"
                "3. Nhập mật khẩu Ubuntu.\n"
                "4. Quay lại app và thực hiện lại chức năng.\n\n"
                "Hoặc chạy app bằng terminal sau khi đã sudo -v."
            )

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    output = ""
    if result.stdout:
        output += result.stdout
    if result.stderr:
        output += ("\n" + result.stderr)

    if not output.strip():
        output = "Thao tác đã thực hiện xong."

    return output.strip()

def q(value: str) -> str:
    """Quote chuỗi để dùng an toàn trong shell command."""
    return shlex.quote(str(value))
