# Contributing to Job Salary Estimator

Thank you for your interest in contributing! Here's how to get started.

## Local Setup

1. Clone the repo
```bash
   git clone https://github.com/Ashutosh-Parve/-Job-Salary-Estimator.git
   cd -Job-Salary-Estimator
```

2. Install dependencies
```bash
   pip install -r requirements.txt
```

3. Set up environment variables
```bash
   cp .env.example .env
   # Add your PostgreSQL credentials
```

4. Run the API
```bash
   uvicorn api.main:app --reload
```

5. Run the frontend
```bash
   streamlit run app/streamlit_app.py
```

## Project Structure



## Ways to Contribute

- Improve the ML model accuracy with better features
- Add more job titles, locations, or companies to training data
- Improve the Streamlit UI
- Add unit tests
- Fix bugs or improve error handling

## Commit Style

Follow this pattern:
- `Add` — new feature or file
- `Fix` — bug fix
- `Update` — change to existing feature
- `Remove` — deleted something

Example: `Add experience_years feature to prediction model`