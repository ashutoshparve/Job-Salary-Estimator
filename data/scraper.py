import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
from datetime import datetime
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

JOB_TITLES = [
    "data analyst", "software engineer", "python developer",
    "data scientist", "backend developer", "machine learning engineer"
]

LOCATION = "India"
PAGES_PER_TITLE = 5


def scrape_indeed_jobs(job_title: str, location: str, pages: int) -> list:
    jobs = []
    for page in range(0, pages * 10, 10):
        url = (
            f"https://in.indeed.com/jobs"
            f"?q={job_title.replace(' ', '+')}"
            f"&l={location.replace(' ', '+')}"
            f"&start={page}"
        )
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            cards = soup.find_all("div", class_="job_seen_beacon")
            if not cards:
                logging.warning(f"No cards found on page {page} for '{job_title}'")
                break

            for card in cards:
                job = parse_job_card(card, job_title)
                if job:
                    jobs.append(job)

            logging.info(f"Scraped page {page//10 + 1} for '{job_title}' — {len(cards)} listings")
            time.sleep(random.uniform(2.5, 5.0))

        except requests.RequestException as e:
            logging.error(f"Request failed for '{job_title}' page {page}: {e}")
            break

    return jobs


def parse_job_card(card, search_title: str) -> dict:
    try:
        title = card.find("span", attrs={"id": lambda x: x and x.startswith("jobTitle")})
        company = card.find("span", attrs={"data-testid": "company-name"})
        location = card.find("div", attrs={"data-testid": "text-location"})
        salary = card.find("div", attrs={"data-testid": "attribute_snippet_testid"})

        return {
            "job_title": title.get_text(strip=True) if title else None,
            "company": company.get_text(strip=True) if company else None,
            "location": location.get_text(strip=True) if location else None,
            "salary_raw": salary.get_text(strip=True) if salary else None,
            "search_query": search_title,
            "scraped_at": datetime.now().isoformat(),
        }
    except Exception as e:
        logging.error(f"Failed to parse card: {e}")
        return None


def run_scraper() -> pd.DataFrame:
    all_jobs = []

    for title in JOB_TITLES:
        logging.info(f"Starting scrape for: {title}")
        print(f"Scraping jobs for: {title}...")
        jobs = scrape_indeed_jobs(title, LOCATION, PAGES_PER_TITLE)
        all_jobs.extend(jobs)
        print(f"  Found {len(jobs)} jobs for '{title}'")
        logging.info(f"Finished '{title}' — {len(jobs)} jobs collected")
        time.sleep(random.uniform(3.0, 6.0))

    df = pd.DataFrame(all_jobs)
    df.drop_duplicates(subset=["job_title", "company", "location"], inplace=True)

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/raw_jobs.csv", index=False)

    logging.info(f"Scrape complete. Total unique jobs: {len(df)}")
    print(f"\nDone! Scraped {len(df)} unique job listings → saved to data/raw_jobs.csv")
    return df


if __name__ == "__main__":
    run_scraper()