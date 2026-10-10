import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "allsarkarijobs.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Crawler settings
REQUEST_TIMEOUT = 15
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36 (AllSarkariJobs Crawler/1.0; +https://allsarkarijobs.com)"
)
