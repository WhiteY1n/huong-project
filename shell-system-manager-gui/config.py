from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
LOG_DIR = PROJECT_DIR / "logs"
BACKUP_DIR = PROJECT_DIR / "backup"
SCRIPTS_DIR = PROJECT_DIR / "scripts"
TEST_DIR = PROJECT_DIR / "test"
LOG_FILE = LOG_DIR / "system_manager.log"

for folder in [LOG_DIR, BACKUP_DIR, SCRIPTS_DIR, TEST_DIR]:
    folder.mkdir(parents=True, exist_ok=True)
