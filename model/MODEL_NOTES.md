# Model Notes

## Algorithm
Random Forest Regressor (Scikit-Learn)

## Performance
| Metric | Value |
|---|---|
| R² Score | 0.83 |
| Mean Absolute Error | ±₹1.10 LPA |
| Training Records | 1,000 |
| Test Split | 80/20 |

## Features Used
- `job_title` — role category
- `location` — city in India
- `company` — employer name

## Why Random Forest?
- Handles non-linear relationships well (e.g. Google pays 1.5x more than TCS)
- No need to scale features
- Resistant to overfitting with enough trees
- Fast prediction time (~80ms)

## Improvement Ideas
- Add `experience_years` as a feature
- Scrape real data to replace synthetic dataset
- Try XGBoost or LightGBM for comparison
- Add cross-validation for more reliable accuracy score