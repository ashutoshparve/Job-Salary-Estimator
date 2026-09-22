# Roadmap

This document outlines planned improvements and future features
for the Job Salary Estimator project.

## Version 1.1 — Model Improvements
- [ ] Add `experience_years` as a feature to improve prediction accuracy
- [ ] Add `skills` field (Python, SQL, AWS etc.) as additional feature
- [ ] Try XGBoost and LightGBM and compare with Random Forest
- [ ] Add cross-validation for more reliable accuracy score
- [ ] Retrain model on real scraped data when scraper is unblocked

## Version 1.2 — Data Pipeline
- [ ] Fix web scraper to handle Indeed's anti-scraping protection
- [ ] Add support for scraping Naukri.com and LinkedIn Jobs
- [ ] Schedule automatic scraping every week using cron jobs
- [ ] Store 10,000+ real job records in PostgreSQL

## Version 1.3 — API Improvements
- [ ] Add `/history` endpoint to show recent predictions
- [ ] Add `/stats` endpoint showing most searched roles and locations
- [ ] Add input validation for unknown job titles and locations
- [ ] Add rate limiting to prevent API abuse

## Version 1.4 — Frontend Improvements
- [ ] Add salary trend chart by location
- [ ] Add comparison mode — compare 2 roles side by side
- [ ] Add experience slider to adjust prediction by years of experience
- [ ] Make frontend fully mobile responsive

## Version 2.0 — Full Product
- [ ] User authentication — save prediction history per user
- [ ] Email alerts — notify users when salary trends change
- [ ] Resume parser — upload resume and auto-fill job title and skills
- [ ] Admin dashboard — monitor model performance and user queries

## Completed
- [x] Web scraper with BeautifulSoup
- [x] Data cleaning pipeline
- [x] PostgreSQL database with 2 tables
- [x] Random Forest model (R² = 0.83)
- [x] FastAPI backend with 5 endpoints
- [x] Streamlit frontend with market range visualization
- [x] Full deployment on Render (frontend + API + database)
- [x] System architecture and API documentation