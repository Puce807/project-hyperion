import inspect
import time
import os
from pathlib import Path
from datetime import datetime, timezone

VERBOSE = True

def log(msg, level="INFO", source=None):
    """Logs to terminal and logs to daily log file.
    Valid level values: INFO, WARN, ERROR, CRITICAL, DEBUG, CLI"""
    formatted_time = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
    formatted_time = formatted_time.replace("+00:00", "Z")

    if source is None:
        caller_frame = inspect.stack()[1]
        source = Path(caller_frame.filename).name

    message = f"{formatted_time} [{level.upper()}] [{source}] {msg}"

    log_folder = Path(__file__).resolve().parent.parent / "logs"
    os.makedirs(log_folder, exist_ok=True)
    log_path = log_folder / f"{time.strftime('%Y-%m-%d')}.log"
    with open(log_path, "a") as file:
        file.write(message + "\n")

    if level.upper() == "CLI":
        print(msg)
        return
    elif VERBOSE:
        print(message)

