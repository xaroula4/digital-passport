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
            margin-top: 0.8rem;
        }
        .section-head {
            background: linear-gradient(135deg, #2d7d32, #4a9c45);
            color: white;
            padding: 0.7rem 1rem;
            font-weight: 800;
            font-size: 1rem;
        }
        .section-body {
            padding: 0.9rem 1rem;
        }
        .kv-row {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            padding: 0.45rem 0;
            border-bottom: 1px solid #edf3ea;
        }
        .kv-row:last-child {
            border-bottom: none;
        }
        .k {
            color: #5f745f;
            font-weight: 700;
        }
        .v {
            color: #214a26;
            font-weight: 800;
            text-align: right;
        }
        .mini-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.7rem;
            margin-top: 0.8rem;
        }
        .mini-card {
            background: white;
            border: 1px solid #dce6d8;
            border-radius: 16px;
            padding: 0.8rem;
            text-align: center;
            box-shadow: 0 8px 18px rgba(0,0,0,0.04);
        }
        .mini-label {
            color: #547054;
            font-size: 0.82rem;
            font-weight: 700;
        }
        .mini-value {
            color: #1f4824;
            font-size: 1.35rem;
            font-weight: 900;
            line-height: 1.1;
            margin-top: 0.25rem;
        }
        .story-box {
            background: #fcfffb;
            border: 1px solid #dce6d8;
            border-radius: 18px;
            padding: 1rem;
            line-height: 1.6;
            color: #355338;
        }
        .bottom-nav {
            position: fixed;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(12px);
            border-top: 1px solid #dbe7d8;
            z-index: 999;
            padding: 0.45rem 0.6rem calc(0.45rem + env(safe-area-inset-bottom));
        }
        .bottom-nav-inner {
            max-width: 470px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 0.35rem;
        }
        .nav-item {
            text-align: center;
            padding: 0.45rem 0.2rem;
            border-radius: 14px;
            color: #456746;
            font-size: 0.78rem;
            font-weight: 700;
            background: #f6faf3;
            border: 1px solid #e2ecde;
        }
        .hero-note {
            font-size: 0.9rem;
            color: #5b755d;
            margin-top: 0.35rem;
        }
        .stButton > button {
            width: 100%;
            border-radius: 14px;
            min-height: 48px;
            font-weight: 800;
            border: 1px solid #d6e3d1;
            background: white;
            color: #245128;
        }
        .stButton > button:hover {
            border-color: #3d8a42;
            color: #1e4422;
        }
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {
            border-radius: 14px !important;
        }
        @media (max-width: 380px) {
            .mini-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def default_data():
    return pd.DataFrame([
        {
            "batch_number": "GR-2023-0578",
            "passport_id": "GR-2023-0578",
            "product": "Φασόλια Πρεσπών",
            "location": "Καστοριά, Ελλάδα",
            "region": "Λευκωνότοπος",
            "area_stremmata": 12,
            "sowing_date": "2023-05-15",
            "last_spray_date": "2023-07-10",
            "spray_product": "Βιολογικό Εντομοκτόνο",
            "phase": "Ανθοφορία",
            "soil_moisture_pct": 26,
            "temperature_c": 29,
            "lat": 40.5193,
            "lon": 21.2687,
            "family_story": "Η οικογένεια καλλιεργεί όσπρια εδώ και τρεις γενιές, συνδυάζοντας παραδοσιακή γνώση, φροντίδα του τόπου και σύγχρονα εργαλεία ακριβείας.",
            "certifications": "AGRO 2|Εσωτερική ιχνηλασιμότητα|Ημερολόγιο καλλιέργειας",
            "analyses": "Υγρασία 12.8%|Υπολείμματα εντός ορίων|Ξένες ύλες <0.5%",
            "route": "Σπορά|Καλλιέργεια|Συγκομιδή|Καθαρισμός|Συσκευασία|Διανομή",
        },
        {
            "batch_number": "OX-2024",
            "passport_id": "OX-2024",
            "product": "Φασόλια Χασίων",
            "location": "Χάσια, Ελλάδα",
            "region": "Χάσια",
            "area_stremmata": 250,
            "sowing_date": "2024-03-18",
            "last_spray_date": "2024-05-10",
            "spray_product": "Βιοδιεγέρτης φυλλώματος",
            "phase": "Βλαστικό στάδιο",
            "soil_moisture_pct": 31,
            "temperature_c": 24,
            "lat": 39.935,
            "lon": 21.512,
            "family_story": "Στα 250 στρέμματα της εκμετάλλευσης, η παραγωγή συνδέεται με τον τόπο, την οικογένεια και την ιδέα ότι κάθε παρτίδα έχει τη δική της ιστορία.",
            "certifications": "ΟΣΔΕ|Ημερολόγιο καλλιέργειας|Εσωτερικός έλεγχος",
            "analyses": "Υγρασία 13.1%|Πρωτεΐνη 24%|Ξένες ύλες <0.5%",
            "route": "Σπορά|UAV παρακολούθηση|Συγκομιδή|Αποθήκευση|Συσκευασία",
        },
    ])


def load_data():
    df = default_data()
    with st.expander("📂 Φόρτωση δικών σου δεδομένων από Excel ή CSV"):
        uploaded = st.file_uploader(
            "Ανέβασε αρχείο .csv ή .xlsx",
            type=["csv", "xlsx"],
            help="Αν δεν ανεβάσεις αρχείο, η εφαρμογή θα δουλέψει με τα demo δεδομένα."
        )
        if uploaded is not None:
            if uploaded.name.lower().endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            st.success(f"Φορτώθηκαν {len(df)} εγγραφές.")
    return df


def qr_image_for_link(link: str):
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


def first_value(series, default=""):
    if len(series) == 0:
        return default
    v = series.iloc[0]
    if pd.isna(v):
        return default
    return v


def batch_lookup(df, batch_number):
    m = df[df["batch_number"].astype(str).str.upper() == str(batch_number).strip().upper()]
    return m


def render_info_card(batch):
    st.markdown('<div class="section-card"><div class="section-head">Πληροφορίες Παρτίδας</div><div class="section-body">', unsafe_allow_html=True)
    rows = [
        ("Αρ. Παρτίδας", first_value(batch["batch_number"])),
        ("Έκταση", f"{first_value(batch['area_stremmata'])} στρέμματα"),
        ("Ημερομηνία Σποράς", greek_date(first_value(batch["sowing_date"]))),
        ("Περιοχή", first_value(batch["region"])),
    ]
    for k, v in rows:
        st.markdown(f'<div class="kv-row"><div class="k">{k}:</div><div class="v">{v}</div></div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


def render_drone_card(batch):
    st.markdown('<div class="section-card"><div class="section-head">Ψεκασμός με Drone</div><div class="section-body">', unsafe_allow_html=True)
    rows = [
        ("Τελευταίος Ψεκασμός", greek_date(first_value(batch["last_spray_date"]))),
        ("Σκεύασμα", first_value(batch["spray_product"])),
    ]
    for k, v in rows:
        st.markdown(f'<div class="kv-row"><div class="k">{k}:</div><div class="v">{v}</div></div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


def render_growth(batch):
    phase = first_value(batch["phase"])
    moisture = first_value(batch["soil_moisture_pct"])
    temp = first_value(batch["temperature_c"])
    st.markdown('<div class="section-card"><div class="section-head">Ανάπτυξη Καλλιέργειας</div><div class="section-body">', unsafe_allow_html=True)
    st.markdown(
        f'''<div class="mini-grid">
            <div class="mini-card"><div class="mini-label">🌱 Φάση</div><div class="mini-value">{phase}</div></div>
            <div class="mini-card"><div class="mini-label">💧 Υγρασία Εδάφους</div><div class="mini-value">{moisture}%</div></div>
            <div class="mini-card"><div class="mini-label">☀️ Θερμοκρασία</div><div class="mini-value">{temp}°C</div></div>
        </div>''',
        unsafe_allow_html=True,
    )
    st.markdown('</div></div>', unsafe_allow_html=True)


def render_traceability(batch):
    certifications = str(first_value(batch["certifications"], "")).split("|")
    analyses = str(first_value(batch["analyses"], "")).split("|")
    route = str(first_value(batch["route"], "")).split("|")

    st.markdown('<div class="section-card"><div class="section-head">Ιχνηλασιμότητα</div><div class="section-body">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.popover("📄 Πιστοποιήσεις"):
            for item in certifications:
                if item.strip():
                    st.write("•", item.strip())
    with c2:
        with st.popover("🧪 Αναλύσεις"):
            for item in analyses:
                if item.strip():
                    st.write("•", item.strip())
    with c3:
        with st.popover("🚛 Διαδρομή Προϊόντος"):
            for item in route:
                if item.strip():
                    st.write("•", item.strip())
    st.markdown('</div></div>', unsafe_allow_html=True)


def render_story(batch):
    story = first_value(batch["family_story"], "")
    st.markdown('<div class="section-card"><div class="section-head">Digital Storytelling</div><div class="section-body">', unsafe_allow_html=True)
    st.markdown(f'<div class="story-box">{story}</div>', unsafe_allow_html=True)
    photos = st.file_uploader(
        "Πρόσθεσε φωτογραφίες της οικογένειας ή των χωραφιών",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="story_images",
    )
    if photos:
        for photo in photos[:6]:
            st.image(photo, width="stretch")
    else:
        st.caption("Μπορείς να ανεβάσεις 2 έως 6 φωτογραφίες για να γεμίσει αυτή η ενότητα.")
    st.markdown('</div></div>', unsafe_allow_html=True)


def render_map(batch):
    lat = pd.to_numeric(first_value(batch["lat"], None), errors="coerce")
    lon = pd.to_numeric(first_value(batch["lon"], None), errors="coerce")
    st.markdown('<div class="section-card"><div class="section-head">Χάρτης Αγροτεμαχίου</div><div class="section-body">', unsafe_allow_html=True)
    if pd.notna(lat) and pd.notna(lon):
        map_df = pd.DataFrame({"lat": [lat], "lon": [lon]})
        st.map(map_df, use_container_width=True)
    else:
        st.info("Δεν υπάρχουν συντεταγμένες για αυτή την παρτίδα.")
    st.markdown('</div></div>', unsafe_allow_html=True)


def render_dashboard(df):
    st.markdown('<div class="section-card"><div class="section-head">Dashboard Παρακολούθησης</div><div class="section-body">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Παρτίδες", len(df))
    with c2:
        st.metric("Μέση υγρασία", f"{round(pd.to_numeric(df['soil_moisture_pct'], errors='coerce').mean(), 1)}%")
    with c3:
        st.metric("Μέση θερμοκρασία", f"{round(pd.to_numeric(df['temperature_c'], errors='coerce').mean(), 1)}°C")

    chart_df = df[["batch_number", "soil_moisture_pct", "temperature_c"]].copy()
    chart_df["soil_moisture_pct"] = pd.to_numeric(chart_df["soil_moisture_pct"], errors="coerce")
    chart_df["temperature_c"] = pd.to_numeric(chart_df["temperature_c"], errors="coerce")
    st.bar_chart(chart_df.set_index("batch_number")[["soil_moisture_pct", "temperature_c"]], width="stretch")
    st.dataframe(df, width="stretch", hide_index=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


def render_qr(batch_number):
    link = f"{BASE_URL_PLACEHOLDER}/?batch={batch_number}"
    qr_img = qr_image_for_link(link)
    st.markdown('<div class="section-card"><div class="section-head">QR Code Παρτίδας</div><div class="section-body">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.image(qr_img, width="stretch")
    with c2:
        st.write("Σκάναρε ή εκτύπωσέ το στη συσκευασία.")
        st.code(link)
        buffer = io.BytesIO()
        qr_img.save(buffer, format="PNG")
        st.download_button(
            "Λήψη QR PNG",
            data=buffer.getvalue(),
            file_name=f"qr_{batch_number}.png",
            mime="image/png",
            width="stretch",
        )
    st.markdown('</div></div>', unsafe_allow_html=True)


def main():
    inject_css()
    df = load_data()

    required = [
        "batch_number", "passport_id", "product", "location", "region",
        "area_stremmata", "sowing_date", "last_spray_date", "spray_product",
        "phase", "soil_moisture_pct", "temperature_c"
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error("Λείπουν στήλες από τα δεδομένα: " + ", ".join(missing))
        st.stop()

    if "batch" in st.query_params:
        initial_batch = st.query_params.get("batch", "GR-2023-0578")
    else:
        initial_batch = "GR-2023-0578"

    st.markdown('<div class="app-shell">', unsafe_allow_html=True)
    st.markdown('<div class="topbar">🌱 Ψηφιακό Διαβατήριο Οσπρίων</div>', unsafe_allow_html=True)

    products = sorted(df["product"].dropna().astype(str).unique().tolist())
    selected_product = st.selectbox("Προϊόν", products, label_visibility="collapsed")
    filtered = df[df["product"].astype(str) == selected_product].copy()

    batch_options = filtered["batch_number"].astype(str).tolist()
    default_index = batch_options.index(initial_batch) if initial_batch in batch_options else 0
    selected_batch = st.selectbox("Batch", batch_options, index=default_index, label_visibility="collapsed")
    st.query_params["batch"] = selected_batch

    batch = batch_lookup(filtered, selected_batch)

    if batch.empty:
        st.warning("Δεν βρέθηκε η παρτίδα. Δοκίμασε άλλη επιλογή.")
        st.stop()

    location = first_value(batch["location"])
    passport_id = first_value(batch["passport_id"])
    st.markdown(f'<div class="subline">📍 {location}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subline">✅ Διαβατήριο: #{passport_id}</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-note">Παρακάτω βλέπεις πλήρη εικόνα παρτίδας, ψεκασμών, χάρτη, ιστορίας και αναφορών.</div>', unsafe_allow_html=True)

    render_info_card(batch)
    render_drone_card(batch)
    render_growth(batch)
    render_traceability(batch)
    render_map(batch)
    render_qr(selected_batch)
    render_story(batch)
    render_dashboard(filtered)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '''<div class="bottom-nav"><div class="bottom-nav-inner">
        <div class="nav-item">🏠<br>Αρχική</div>
        <div class="nav-item">📡<br>Παρακολούθηση</div>
        <div class="nav-item">📄<br>Αναφορές</div>
        <div class="nav-item">👤<br>Προφίλ</div>
        </div></div>''',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
