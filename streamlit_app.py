"""Rayne Asset Management Streamlit Launcher

This app embeds the existing HTML dashboard in a Streamlit page so the
project can be deployed directly as a public Streamlit app.
"""

from pathlib import Path
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
