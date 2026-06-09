# Job Salary Estimator

An end-to-end machine learning web application that predicts job salaries based on role, location, and experience — built with real-world scraped data, not a Kaggle CSV.

---

## Live Demo
> Deployment in progress — link will be added after Phase 5

---

## Project Overview

Most salary estimator projects use clean, pre-packaged datasets. This one scrapes **live job listings** from Indeed India, cleans the messy salary data, trains an ML model, and serves predictions through a FastAPI backend connected to a Streamlit frontend.

Every prediction made by a user is logged back into the database — simulating how a real production ML system tracks usage and collects data for future model updates.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Data collection | Python, Requests, BeautifulSoup |
| Data storage | PostgreSQL, SQLAlchemy |
| Data processing | Pandas, NumPy |
| ML model | Scikit-Learn (Random Forest) |
| API backend | FastAPI |
| Frontend | Streamlit |
| Deployment | Render |

---

## Project Structure

```
salary-estimator/
├── data/
│   ├── scraper.py          # scrapes live job listings from Indeed India
│   ├── cleaner.py          # parses salary strings, outputs cleaned CSV
│   ├── raw_jobs.csv        # raw scraped data (gitignored)
│   └── cleaned_jobs.csv    # cleaned data ready for ML (gitignored)
├── database/
│   ├── schema.sql          # table definitions for jobs + user queries
│   └── db.py               # SQLAlchemy connection and helper functions
├── model/
│   ├── train.py            # feature engineering + model training
│   └── model.pkl           # saved trained model (gitignored)
├── api/
│   └── main.py             # FastAPI prediction endpoint + query logging
├── app/
│   └── streamlit_app.py    # Streamlit frontend UI
├── logs/                   # scraper + cleaner logs (gitignored)
├── .env.example            # environment variable template
├── requirements.txt
└── README.md
```

---

## How It Works

```
Indeed job pages → scraper.py → raw_jobs.csv
                                     ↓
                             cleaner.py (parse salary → LPA)
                                     ↓
                             PostgreSQL (job_listings table)
                                     ↓
                             train.py → model.pkl
                                     ↓
              User input → FastAPI /predict → salary estimate
                                     ↓
                         PostgreSQL (user_queries table — logged)
```

---

## Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/your-username/salary-estimator.git
cd salary-estimator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
# Edit .env and add your PostgreSQL credentials
```

### 4. Run the scraper
```bash
python data/scraper.py
python data/cleaner.py
```

### 5. Set up the database
```bash
psql -U your_user -d your_db -f database/schema.sql
```

### 6. Train the model
```bash
python model/train.py
```

### 7. Start the API and frontend
```bash
# Terminal 1
uvicorn api.main:app --reload

# Terminal 2
streamlit run app/streamlit_app.py
```

---

## Current Progress

- [x] Phase 1 — Data collection (scraper + cleaner)
- [ ] Phase 2 — SQL database schema and storage
- [ ] Phase 3 — ML model training and evaluation
- [ ] Phase 4 — FastAPI backend + query logging
- [ ] Phase 5 — Streamlit frontend + deployment

---

## What I Learned

- How to scrape and handle real-world messy data (salary strings in multiple formats)
- How to structure Python projects outside of Jupyter notebooks
- How production ML systems log predictions for future retraining

---

## Author

**Ashutosh** — [GitHub](https://github.com/your-username) · [LinkedIn](https://linkedin.com/in/your-profile)
