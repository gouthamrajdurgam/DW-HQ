# DW-HQ

Automated property recommendation bot for ImmoScout24 and eBay Kleinanzeigen.

This project is meant to be a practical MVP for a daily shortlist workflow:
- scrape listings from major property portals
- normalize them into a shared schema
- expand searches slightly when results are thin
- rank listings based on user preferences
- learn from likes/dislikes over time
- send the top 3 offers daily

The repository intentionally uses a hybrid approach:
- rule-based filtering first
- machine learning ranking on top of your actual feedback

This keeps the system explainable and easier to debug while still learning.

## Features
- Playwright-based scraping for ImmoScout24 and eBay Kleinanzeigen
- Shared listing schema
- Search expansion logic
- SQLite-backed storage for listings and feedback
- Scoring and ranking engine
- Daily shortlist sending via SMTP email
- GitHub Actions cron schedule

## Tech stack
- Python 3.11+
- Playwright
- BeautifulSoup
- scikit-learn
- SQLite
- GitHub Actions

## Folder layout

```text
DW-HQ/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   ├── utils.py
│   ├── main.py
│   ├── feedback/
│   │   ├── __init__.py
│   │   └── feedback_store.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── feature_builder.py
│   │   ├── ranking_model.py
│   │   └── trainer.py
│   ├── notifications/
│   │   ├── __init__.py
│   │   └── emailer.py
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── immoscout.py
│   │   ├── kleinanzeigen.py
│   │   └── normalize.py
│   └── search/
│       ├── __init__.py
│       ├── expand.py
│       └── filter.py
├── .github/
│   └── workflows/
│       └── daily_shortlist.yml
├── data/
│   ├── listings.db
│   └── feedback.csv
├── requirements.txt
├── preferences.yaml
├── .gitignore
└── README.md
```

## Setup

1. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
python -m playwright install --with-deps chromium
```

3. Update `preferences.yaml`

4. Run the app
```bash
python -m app.main
```

## Notes

This project is intentionally a strong starter, not a fully production-grade browser scraper. German real estate portals frequently change structure and add anti-bot protections, so a browser automation route is the safest baseline.

## Security

Do not commit personal email credentials or secrets. Use GitHub repository secrets for SMTP credentials when running through GitHub Actions.
