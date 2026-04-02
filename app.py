import io
import base64
from datetime import datetime
from pathlib import Path

import pandas as pd
import qrcode
import streamlit as st

try:
    from PIL import Image
except Exception:
    Image = None

APP_TITLE = "Ψηφιακό Διαβατήριο Οσπρίων"
BASE_URL_PLACEHOLDER = "https://your-app-name.streamlit.app"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def greek_date(value):
    months = {
        1: "Ιανουαρίου", 2: "Φεβρουαρίου", 3: "Μαρτίου", 4: "Απριλίου",
        5: "Μαΐου", 6: "Ιουνίου", 7: "Ιουλίου", 8: "Αυγούστου",
        9: "Σεπτεμβρίου", 10: "Οκτωβρίου", 11: "Νοεμβρίου", 12: "Δεκεμβρίου"
    }
    if value is None or str(value).strip() == "":
        return "-"
    try:
        dt = pd.to_datetime(value)
        return f"{dt.day} {months[dt.month]} {dt.year}"
    except Exception:
        return str(value)


def inject_css():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #edf5ec 0%, #f8fbf8 100%);
        }
        .block-container {
            max-width: 470px;
            padding-top: 1rem;
            padding-bottom: 6rem;
        }
        .app-shell {
            background: #f7fbf4;
            border-radius: 28px;
            padding: 0.85rem;
            box-shadow: 0 16px 40px rgba(0,0,0,0.08);
            border: 1px solid #dce9d7;
        }
        .topbar {
            background: linear-gradient(135deg, #2d7d32, #3f9d45);
            border-radius: 20px;
            padding: 0.9rem 1rem;
            color: white;
            font-weight: 800;
            font-size: 1.15rem;
            display: flex;
            align-items: center;
            gap: 0.55rem;
        }
        .subline {
            background: #eef5e8;
            border: 1px solid #d9e7d2;
            color: #244d27;
            border-radius: 14px;
            padding: 0.65rem 0.8rem;
            margin-top: 0.65rem;
            font-weight: 700;
        }
        .section-card {
            background: white;
            border: 1px solid #dce6d8;
            border-radius: 18px;
            overflow: hidden;
            box-shadow: 0 8px 24px rgba(0,0,0,0.05);
            margi
