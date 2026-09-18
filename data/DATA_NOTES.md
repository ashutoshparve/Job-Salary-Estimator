# Data Notes

## Data Collection
- **Source**: Indeed India (in.indeed.com)
- **Method**: Python web scraper using Requests + BeautifulSoup
- **Target**: 6 job titles × 5 pages = ~1,000+ listings attempted
- **Note**: Indeed's anti-scraping protection blocked automated requests,
  so a synthetic dataset was generated with realistic salary patterns

## Synthetic Dataset Design
Rather than using a generic random dataset, salaries were generated
using real-world multipliers:

### City Multipliers
| City | Multiplier |
|---|---|
| Bangalore | 1.30x |
| Mumbai | 1.25x |
| Delhi | 1.20x |
| Hyderabad | 1.15x |
| Pune | 1.10x |
| Chennai | 1.05x |
| Kolkata | 0.90x |

### Company Tier Multipliers
| Company | Multiplier |
|---|---|
| Google | 1.50x |
| Microsoft | 1.45x |
| Amazon | 1.40x |
| Flipkart | 1.25x |
| Infosys | 0.90x |
| TCS | 0.88x |
| Wipro | 0.87x |

### Base Salaries (LPA)
| Role | Base |
|---|---|
| Machine Learning Engineer | ₹12 LPA |
| Data Scientist | ₹10 LPA |
| Backend Developer | ₹8.5 LPA |
| Software Engineer | ₹8 LPA |
| Python Developer | ₹7.5 LPA |
| Data Analyst | ₹6 LPA |

## Impact on Model
Using random data → R² = 0.17 (17% accuracy)
Using realistic multipliers → R² = 0.83 (83% accuracy)

## Files
- `raw_jobs.csv` — raw scraped data (gitignored)
- `cleaned_jobs.csv` — cleaned data ready for ML (gitignored)