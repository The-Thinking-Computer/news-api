import os
from datetime import datetime
def get_most_recent_file(relative_path):
    folder_path = os.path.abspath(relative_path)
    files = os.listdir(folder_path)
    files = [file for file in files if file.startswith("data__") and file.endswith(".json")]

    if not files:
        return None 
    file_timestamps = [datetime.strptime(file.split("__")[1].split(".json")[0], "%Y-%m-%d_%H-%M-%S") for file in files]

    most_recent_timestamp = max(file_timestamps)
    most_recent_index = file_timestamps.index(most_recent_timestamp)
    return os.path.join(folder_path, files[most_recent_index])