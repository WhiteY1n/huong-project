from pathlib import Path
import subprocess
import tempfile
from config import BACKUP_DIR, SCRIPTS_DIR
from utils.logger import write_log
from utils.command_runner import q

def get_cron_jobs() -> list[str]:
    result = subprocess.run("crontab -l", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]

def view_cron_jobs() -> str:
    jobs = get_cron_jobs()
    write_log("Xem danh sách cron")
    if not jobs:
        return "Chưa có lịch cron nào."
    return "\n".join(f"{i + 1}. {job}" for i, job in enumerate(jobs))

def set_cron_jobs(jobs: list[str]) -> bool:
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as f:
        for job in jobs:
            f.write(job + "\n")
        temp_name = f.name
    result = subprocess.run(f"crontab {q(temp_name)}", shell=True, capture_output=True, text=True)
    Path(temp_name).unlink(missing_ok=True)
    return result.returncode == 0

def add_cron_job(minute: str, hour: str, day: str, month: str, weekday: str, command: str) -> str:
    cron_line = f"{minute} {hour} {day} {month} {weekday} {command}"
    jobs = get_cron_jobs()
    jobs.append(cron_line)
    if set_cron_jobs(jobs):
        write_log(f"Thêm cron: {cron_line}")
        return f"Đã thêm cron thành công:\n{cron_line}"
    return "Thêm cron thất bại."

def create_script(script_name: str, content: str) -> tuple[bool, str, str]:
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    if not script_name.endswith(".sh"):
        script_name += ".sh"

    safe_name = Path(script_name).name
    script_path = SCRIPTS_DIR / safe_name

    if not content.startswith("#!/bin/bash"):
        content = "#!/bin/bash\n" + content

    script_path.write_text(content, encoding="utf-8")
    script_path.chmod(0o755)

    write_log(f"Tạo script mới: {script_path}")
    command = f"/bin/bash {q(str(script_path))}"
    return True, str(script_path), command

def command_from_existing_script(script_path: str) -> str:
    path = Path(script_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError("File script không tồn tại.")
    path.chmod(0o755)
    write_log(f"Chọn script có sẵn: {path}")
    return f"/bin/bash {q(str(path))}"

def add_backup_schedule(source_dir: str, minute: str, hour: str) -> str:
    source = Path(source_dir).expanduser().resolve()
    if not source.is_dir():
        return "Thư mục cần sao lưu không tồn tại."

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    command = (
        f'/bin/tar -czf "{BACKUP_DIR}/backup_$(date +\\%Y\\%m\\%d_\\%H\\%M\\%S).tar.gz" '
        f'"{source}"'
    )
    cron_line = f"{minute} {hour} * * * {command}"

    jobs = get_cron_jobs()
    jobs.append(cron_line)

    if set_cron_jobs(jobs):
        write_log(f"Thêm lịch backup: {source}")
        return f"Đã thêm lịch backup:\n{cron_line}"
    return "Thêm lịch backup thất bại."

def delete_cron_by_index(index: int) -> str:
    jobs = get_cron_jobs()
    if not jobs:
        return "Chưa có lịch cron nào."
    if index < 0 or index >= len(jobs):
        return "Số thứ tự không hợp lệ."

    deleted = jobs.pop(index)
    if set_cron_jobs(jobs):
        write_log(f"Xóa cron: {deleted}")
        return f"Đã xóa cron:\n{deleted}"
    return "Xóa cron thất bại."

def delete_all_cron_jobs() -> str:
    result = subprocess.run("crontab -r", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        write_log("Xóa toàn bộ cron")
        return "Đã xóa toàn bộ lịch cron."
    return "Không có cron để xóa hoặc thao tác thất bại."
