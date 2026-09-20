# Changelog

All notable changes to this project are documented here.

## [1.0.0] - 2026-06-19
### Added
- Live deployment on Render (frontend + API + cloud PostgreSQL)
- Streamlit frontend with dark navy theme and market range visualization
- FastAPI backend with `/predict` endpoint serving predictions in ~80ms
- PostgreSQL `user_queries` table logging every prediction automatically
- Random Forest model achieving R² = 0.83 (83% accuracy)

## [0.3.0] - 2026-06-18
### Added
- FastAPI backend with 5 endpoints
- Swagger UI auto-generated at `/docs`
- Query logging to PostgreSQL on every prediction

## [0.2.0] - 2026-06-17
### Added
- PostgreSQL database schema with `job_listings` and `user_queries` tables
- SQLAlchemy connection via `database/db.py`
- `.env` file for secure credential management

## [0.1.0] - 2026-06-12
### Added
- Web scraper using Requests and BeautifulSoup
- Data cleaner converting messy salary strings to LPA format
- Synthetic dataset with realistic city and company multipliers
- Random Forest model training with Scikit-Learn
- Project folder structure and README