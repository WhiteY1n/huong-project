from pathlib import Path
import shutil
from utils.command_runner import run_command, q
from utils.logger import write_log

def list_items(folder: str) -> str:
    path = Path(folder).expanduser()
    if not path.is_dir():
        return "Thư mục không tồn tại."
    write_log(f"Xem danh sách thư mục: {path}")
    return run_command(f"ls -lah {q(str(path))}")

def create_file(file_path: str) -> str:
    path = Path(file_path).expanduser()
    if path.exists():
        return "File/thư mục đã tồn tại."
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    write_log(f"Tạo file: {path}")
    return f"Đã tạo file:\n{path}"

def create_folder(folder_path: str) -> str:
    path = Path(folder_path).expanduser()
    if path.exists():
        return "Thư mục/file đã tồn tại."
    path.mkdir(parents=True, exist_ok=True)
    write_log(f"Tạo thư mục: {path}")
    return f"Đã tạo thư mục:\n{path}"

def copy_item(source: str, destination: str) -> str:
    src = Path(source).expanduser()
    dst = Path(destination).expanduser()
    if not src.exists():
        return "Nguồn không tồn tại."

    if src.is_dir():
        if dst.exists():
            dst = dst / src.name
        shutil.copytree(src, dst)
    else:
        if dst.is_dir():
            dst = dst / src.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    write_log(f"Sao chép từ {src} đến {dst}")
    return f"Đã sao chép thành công:\n{src}\n→ {dst}"

def move_item(source: str, destination: str) -> str:
    src = Path(source).expanduser()
    dst = Path(destination).expanduser()
    if not src.exists():
        return "Nguồn không tồn tại."
    if dst.is_dir():
        dst = dst / src.name
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))
    write_log(f"Di chuyển/đổi tên từ {src} thành {dst}")
    return f"Đã di chuyển/đổi tên:\n{src}\n→ {dst}"

def delete_item(target: str) -> str:
    path = Path(target).expanduser()
    if not path.exists():
        return "File/thư mục không tồn tại."
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()
    write_log(f"Xóa file/thư mục: {path}")
    return f"Đã xóa:\n{path}"

def search_file(folder: str, keyword: str) -> str:
    path = Path(folder).expanduser()
    if not path.is_dir():
        return "Thư mục tìm kiếm không tồn tại."
    result = run_command(f"find {q(str(path))} -iname {q('*' + keyword + '*')}")
    write_log(f"Tìm kiếm '{keyword}' trong {path}")
    return result if result.strip() else "Không tìm thấy file phù hợp."

def read_file(file_path: str) -> str:
    path = Path(file_path).expanduser()
    if not path.is_file():
        return "File không tồn tại hoặc không phải file thường."
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = path.read_text(encoding="latin-1", errors="replace")
    write_log(f"Xem nội dung file: {path}")
    return content if content else "File rỗng."
