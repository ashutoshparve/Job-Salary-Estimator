-- =============================================================
-- Salary Estimator — Database Schema
-- =============================================================
-- Run this file to set up all tables needed for the project.
-- Command: psql -U postgres -d salary_estimator -f database/schema.sql
-- =============================================================


-- -------------------------------------------------------------
-- TABLE 1: job_listings
-- Stores all scraped job data used for ML model training
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS job_listings (
    id              SERIAL PRIMARY KEY,
    job_title       VARCHAR(255)    NOT NULL,
    company         VARCHAR(255),
    location        VARCHAR(255),
    salary_lpa      FLOAT,
    search_query    VARCHAR(100),
    scraped_at      TIMESTAMP,
    created_at      TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);


-- -------------------------------------------------------------
-- TABLE 2: user_queries
-- Logs every prediction request made through the app
-- This is the "engineering touch" — tracks real usage for
-- future model retraining and monitoring
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS user_queries (
    id                  SERIAL PRIMARY KEY,
    job_title           VARCHAR(255),
    location            VARCHAR(255),
    experience_years    FLOAT,
    predicted_salary    FLOAT,
    queried_at          TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);


-- -------------------------------------------------------------
-- INDEXES — speeds up common queries
-- -------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_job_listings_title
    ON job_listings(job_title);

CREATE INDEX IF NOT EXISTS idx_job_listings_location
    ON job_listings(location);

CREATE INDEX IF NOT EXISTS idx_user_queries_title
    ON user_queries(job_title);


-- -------------------------------------------------------------
-- Verify tables were created
-- -------------------------------------------------------------
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
