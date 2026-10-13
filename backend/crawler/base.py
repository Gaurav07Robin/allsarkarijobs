import time
import requests
import urllib3
from typing import Optional
from backend.config import REQUEST_TIMEOUT, DEFAULT_USER_AGENT

# Suppress insecure SSL warnings for government websites with untrusted/expired certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class BaseCrawler:
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
            "Connection": "keep-alive"
        })

    def fetch_page(self, url: Optional[str] = None, retries: int = 3, delay: float = 1.0) -> Optional[str]:
        target_url = url or self.base_url
        for attempt in range(retries):
            try:
                response = self.session.get(
                    target_url,
                    timeout=REQUEST_TIMEOUT,
                    verify=False  # Required for many state NIC portals
                )
                if response.status_code == 200:
                    return response.text
                print(f"[{self.name}] Attempt {attempt+1}: Status {response.status_code} for {target_url}")
            except Exception as e:
                print(f"[{self.name}] Attempt {attempt+1} error fetching {target_url}: {e}")
            time.sleep(delay)
        return None
