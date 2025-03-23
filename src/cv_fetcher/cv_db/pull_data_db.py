import requests
import re
from io import BytesIO
from lxml import etree
from lxml import html
from fastapi import HTTPException

from cv_fetcher.config import LIMIT
from cv_fetcher.cv_db.models import Candidates
from cv_fetcher.cv_db.db import CandidatestDB
from cv_fetcher.utils.logging import get_logger

logger = get_logger(__name__)


def clean_html(raw_html: str) -> str:
    tree = html.fromstring(raw_html)
    return tree.text_content().strip()


def extract_experience(text: str) -> str | None:
    patterns = [
        r"(\d+)\+?\s*(?:years?|роки|років|рік|річний|річні|річного)",  # 3+ роки, 2 years, 1 рік
        r"від\s+(\d+)\s*(?:років|роки|рік|years?)",  # від 2 років
        r"більше\s+(\d+)\s*(?:років|роки|рік|years?)",  # більше 3 років
        r"мінімум\s+(\d+)\s*(?:років|роки|рік|years?)\s+досвіду",  # мінімум 2 роки досвіду
        r"(\d+)\s+years?\s+of\s+experience",  # 3 years of experience
        r"досвід\s+(\d+)\s*(?:років|роки|рік|years?)",  # досвід 3 роки
        r"(\d+)\s*-\s*(\d+)\s*(?:років|роки|рік|years?)\s+досвіду",  # 2-3 роки досвіду
        r"досвід\s+роботи\s+від\s+(\d+)\s*до\s*(\d+)\s*(?:років|роки|рік|years?)",  # досвід роботи від 2 до 5 років
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return f"{match.group(1)} years"

    return None

class SimpleHttpClient:
    def fetch(self, url: str) -> bytes:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
        try:
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()
            return resp.content
        except requests.exceptions.HTTPError as http_err:
            status_code = http_err.response.status_code
            detail = f"HTTP error {status_code}: {http_err.response.reason}"
            raise HTTPException(status_code=status_code, detail=detail)
        except requests.exceptions.RequestException as err:
            raise HTTPException(status_code=500, detail=f"Request failed: {err}")

def parse_and_store(fetch_url):
    logger.info("Get fresh data from https://jobs.dou.ua/vacancies/feeds/?category=Python")
    db = CandidatestDB()
    client = SimpleHttpClient()
    data = client.fetch(fetch_url)
    count = 0
    for event, elem in etree.iterparse(BytesIO(data), events=("end",), tag="item"):
        title = elem.findtext("title") or ""
        description_html = elem.findtext("description") or ""
        description = clean_html(description_html)

        name = title
        skills = description
        experience = extract_experience(description)

        candidate = Candidates(name=name, skills=skills, experience=experience)
        db.save(candidate)

        elem.clear()
        count += 1
        if count >= LIMIT:
            break
    logger.info("Data has fetched")