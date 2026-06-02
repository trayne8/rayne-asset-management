"""Rayne Asset Management Streamlit Launcher

This app embeds the existing HTML dashboard in a Streamlit page so the
project can be deployed directly as a public Streamlit app.
"""

from pathlib import Path
import json
import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(
    page_title="Rayne Asset Management Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("# Rayne Asset Management — Hedge Fund Dashboard")
st.markdown(
    "This repository includes the main dashboard as a standalone HTML file. "
    "Streamlit embeds it directly so the original HTML styling and charts are preserved."
)

html_file = Path("Rayne Hedge Fund.html")

if html_file.exists():
    dashboard_html = html_file.read_text(encoding="utf-8")
    default_csv_path = Path("CSV data files/MES_15min_Stitched_Jul2022_May2026.csv")
    if default_csv_path.exists():
        default_csv = default_csv_path.read_text(encoding="utf-8")
        default_payload = json.dumps({
            "id": "default-mes-15m",
            "name": "MES_15min_Stitched_Jul2022_May2026",
            "csv": default_csv,
        })
        dashboard_html = dashboard_html.replace(
            "</head>",
            f'<script>window.DEFAULT_DATASET = {default_payload};</script></head>'
        )
    html(dashboard_html, height=1200, scrolling=True)
    st.markdown("---")
    st.markdown(
        "### Notes\n"
        "- The dashboard is rendered from `Rayne Hedge Fund.html`.\n"
        "- If you want the original layout, styles, and chart behavior, this HTML asset is preserved exactly.\n"
        "- The dashboard uses Chart.js via CDN, so it should render in Streamlit Cloud without additional packages."
    )
else:
    st.error("Could not find `Rayne Hedge Fund.html` in the repository root.")
    st.stop()
