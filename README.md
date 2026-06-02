# Rayne Asset Management

This repository contains the Rayne Asset Management dashboard and the original HTML dashboard asset.

## Streamlit App

To run the app locally:

```bash
cd '/Users/rayneperekekeme/Documents/Claude/Projects/Trading stratetgies Portfolio/Rayne Asset Management'
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app embeds `Rayne Hedge Fund.html` directly so the dashboard's HTML structure, styling, and charts are preserved.

## Deploying to Streamlit Cloud

1. Push this repository to GitHub.
2. In Streamlit Cloud, create a new app from the repo.
3. Select branch `main` and the file `streamlit_app.py`.
4. Deploy.

## Notes

- The HTML dashboard is preserved in `Rayne Hedge Fund.html`.
- The Streamlit wrapper is intentionally minimal so the original HTML design remains intact.
