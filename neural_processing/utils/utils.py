import os
from datetime import datetime


def delete_file(file_path: str) -> bool:
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    else:
        return False


def delete_old_zip_logs(date: datetime):
    log_directory = "path/to/log/directory"
    for filename in os.listdir(log_directory):
        file_path = os.path.join(log_directory, filename)
        if os.path.isfile(file_path) and filename.endswith(".zip"):
            modification_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if modification_time < date and "workers" in filename:
                os.remove(file_path)


def file_exists(file_path: str):
    return os.path.exists(file_path)
