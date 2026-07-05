import inspect
import time
import os
from pathlib import Path
from datetime import datetime, timezone

VERBOSE = True
LOG_BUFFER = []

def log(msg, level="INFO", source=None):
    """Logs to terminal and logs to daily log file.
    Valid level values: INFO, WARN, ERROR, CRITICAL, DEBUG, CLI"""
    formatted_time = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
    formatted_time = formatted_time.replace("+00:00", "Z")

    if source is None:
        caller_frame = inspect.stack()[1]
        source = Path(caller_frame.filename).name

    message = f"{formatted_time} [{level.upper()}] [{source}] {msg}"
    level_upper = level.upper()

    if level_upper == "CLI":
        print(msg)
    elif level_upper in ("ERROR", "CRITICAL", "WARN"):
        print(f"[{level_upper}] {msg}")
    elif VERBOSE:
        print(message)

    write_to_disk([message])


def write_to_disk(lines):
    """Internal helper to write an array of strings to disk in a single batch operation."""
    log_folder = Path(__file__).resolve().parent.parent / "logs"
    os.makedirs(log_folder, exist_ok=True)
    log_path = log_folder / f"{time.strftime('%Y-%m-%d')}.log"

    with open(log_path, "a") as file:
        file.write("\n".join(lines) + "\n")