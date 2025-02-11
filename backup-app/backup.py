import shutil
import os
from datetime import datetime
def backup_files(source_dir, backup_dir):
    """Backup files from source_dir to backup_dir with timestamp."""
    if not os.path.exists(source_dir):
        return "Source directory does not exist."
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_path = os.path.join(backup_dir, f'backup_{timestamp}')
    try:
        shutil.copytree(source_dir, backup_path)
        return f"Backup successful! Files copied to {backup_path}"
    except Exception as e:
        return f"Backup failed: {e}"

