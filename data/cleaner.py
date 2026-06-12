import pandas as pd
import re
import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/cleaner.log",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)


def parse_salary(raw: str) -> float:
    if not raw or not isinstance(raw, str):
        return None

    raw = raw.lower().replace(",", "")

    monthly = re.search(r"₹?([\d.]+)\s*(lakh|l)?\s*a month", raw)
    if monthly:
        amount = float(monthly.group(1))
        return round((amount * 12) / 100000, 2)

    range_match = re.findall(r"₹?([\d.]+)\s*(lpa|l|lakh)?", raw)
    if len(range_match) >= 2:
        vals = []
        for val, unit in range_match:
            v = float(val)
            if unit in ("lpa", "l", "lakh"):
                vals.append(v)
            else:
                vals.append(v / 100000)
        return round(sum(vals) / len(vals), 2)

    return None


def clean_data(input_path="data/raw_jobs.csv",
               output_path="data/cleaned_jobs.csv") -> pd.DataFrame:

    df = pd.read_csv(input_path)
    logging.info(f"Loaded {len(df)} raw rows")
    print(f"Loaded {len(df)} raw jobs")

    df.dropna(subset=["job_title", "company"], inplace=True)

    df["salary_lpa"] = df["salary_raw"].apply(parse_salary)

    df_with_salary = df.dropna(subset=["salary_lpa"]).copy()

    df_with_salary["job_title"] = df_with_salary["job_title"].str.strip().str.lower()
    df_with_salary["location"] = df_with_salary["location"].str.strip().str.lower()
    df_with_salary["company"] = df_with_salary["company"].str.strip()

    df_with_salary.to_csv(output_path, index=False)

    logging.info(f"Cleaned data: {len(df_with_salary)} rows with valid salary")
    print(f"Cleaned! {len(df_with_salary)} rows with valid salary → saved to data/cleaned_jobs.csv")
    print(f"Salary range: ₹{df_with_salary['salary_lpa'].min()} LPA — ₹{df_with_salary['salary_lpa'].max()} LPA")

    return df_with_salary


if __name__ == "__main__":
    clean_data()