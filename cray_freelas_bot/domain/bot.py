from dataclasses import dataclass
from pathlib import Path


@dataclass
class Bot:
    username: str
    password: str
    report_folder: Path
    category: str
    message: str
    user_data_dir: str
    browser_module: str
    id: int = None
