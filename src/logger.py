import inspect
from pathlib import Path
from datetime import datetime, timezone

def log(msg, level="INFO", source=None):
    """Logs to terminal and logs file
    Valid level values: INFO, WARN, ERROR, DEBUG"""
    formatted_time = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
    formatted_time = formatted_time.replace("+00:00", "Z")

    if source is None:
        caller_frame = inspect.stack()[1]
        source = Path(caller_frame.filename).name

    message = f"{formatted_time} [{level.upper()}] [{source}] {msg}"

    print(message)

log("idk")