import io
import re
import requests
from typing import Dict, Any, Optional
from pypdf import PdfReader
from backend.config import REQUEST_TIMEOUT, DEFAULT_USER_AGENT

class PDFNoticeParser:
    @staticmethod
    def extract_text_from_url(pdf_url: str) -> Optional[str]:
        headers = {"User-Agent": DEFAULT_USER_AGENT}
        try:
            resp = requests.get(pdf_url, headers=headers, timeout=REQUEST_TIMEOUT, verify=False)
            if resp.status_code == 200:
                stream = io.BytesIO(resp.content)
                reader = PdfReader(stream)
                text = ""
                # Parse first 5 pages (where 95% of job summary and criteria appear)
                max_pages = min(5, len(reader.pages))
                for i in range(max_pages):
                    page_text = reader.pages[i].extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text
        except Exception as e:
            print(f"[PDFParser] Error reading {pdf_url}: {e}")
        return None

    @classmethod
    def parse_notice_text(cls, text: str) -> Dict[str, Any]:
        result = {
            "vacancies": None,
            "age_limit": None,
            "last_date": None,
            "fee": None,
            "education": None
        }

        if not text:
            return result

        # 1. Total Vacancies
        vac_match = re.search(r'(?:total\s*(?:of\s*)?vacanc(?:y|ies)|posts|no\.?\s*of\s*posts)\s*[:=-]?\s*(\d[\d,]*)', text, re.I)
        if not vac_match:
            vac_match = re.search(r'(\d[\d,]*)\s*(?:vacancies|posts)', text, re.I)
        if vac_match:
            result["vacancies"] = vac_match.group(1).replace(",", "")

        # 2. Age Limit
        age_match = re.search(r'(?:age\s*limit|minimum\s*age|age\s*as\s*on).*?(\d{2}\s*(?:to|-)\s*\d{2}\s*years?)', text, re.I)
        if age_match:
            result["age_limit"] = age_match.group(1).strip()

        # 3. Last Date
        date_match = re.search(r'(?:last\s*date|closing\s*date).*?(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})', text, re.I)
        if date_match:
            result["last_date"] = date_match.group(1).strip()

        # 4. Application Fee
        fee_match = re.search(r'(?:application\s*fee|fee\s*payable).*?(?:₹|rs\.?)\s*(\d+)', text, re.I)
        if fee_match:
            result["fee"] = f"₹{fee_match.group(1)}"

        # 5. Qualification keywords
        edu_keywords = ["10th", "12th", "Intermediate", "Matric", "Graduation", "Bachelor", "Master", "Diploma", "B.Tech", "ITI"]
        found_edu = [kw for kw in edu_keywords if re.search(rf'\b{kw}\b', text, re.I)]
        if found_edu:
            result["education"] = ", ".join(found_edu)

        return result
