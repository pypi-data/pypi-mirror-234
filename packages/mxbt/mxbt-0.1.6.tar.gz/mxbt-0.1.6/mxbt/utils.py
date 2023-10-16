
from datetime import datetime

def log(text: str) -> None:
    date = datetime.now().strftime("%H:%M:%S %d.%m.%Y")
    message = f"{date} -> {text}"
    print(message)

def info(text: str) -> None:
    log(f"INFO: {text}")

def error(text: str) -> None:
    log(f"ERROR: {text}")

