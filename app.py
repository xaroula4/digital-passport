import io
import pandas as pd
import qrcode
import streamlit as st

# ======================
# SETTINGS
# ======================
st.set_page_config(page_title="Ψηφιακό Διαβατήριο Οσπρίων", layout="wide")

BASE_URL = "https://your-app-name.streamlit.app"

# ======================
# DEMO DATA
# ======================
def load_demo():
    return pd.DataFrame([
        {
            "batch_number": "GR-2023-0578",
            "product": "Φασόλια Πρεσπών",
            "location": "Καστοριά, Ελλάδα",
            "region": "Λευκωνότοπος",
            "area": 12,
            "sowing_date": "2023-05-15",
            "spray_date": "2023-07-10",
            "spray": "Βιολογικό Εντομοκτόνο",
            "phase": "Ανθοφορία",
            "moisture": 26,
            "temp": 29,
            "lat": 40.51,
            "lon": 21.26,
            "story": "Η οικογένεια καλλιεργεί όσπρια εδώ και γενιές."
        }
    ])

df = load_demo()

# ======================
# QR FUNCTION
# ======================
def generate_qr(link):
    qr = qrcode.make(link)
    return qr

# ======================
# UI STYLE
# ======================
st.markdown("""
<style>
.main {
    max-width: 420px;
    margin: auto;
}
.card {
    background: white;
    padding: 12px;
    border-radius: 15px;
    margin-top: 10px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.title {
    font-weight: bold;
    color: green;
}
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
st.title("🌱 Ψηφιακό Διαβατήριο Οσπρίων")

# ======================
# INPUT
# ======================
batch = st.text_input("Batch Number", "GR-2023-0578")

data = df[df["batch_number"] == batch]

if data.empty:
    st.error("Δεν βρέθηκε παρτίδα")
    st.stop()

row = data.iloc[0]

# ======================
# INFO CARD
# ======================
st.markdown(f"""
<div class="card">
<div class="title">Πληροφορίες Παρτίδας</div>
Αρ. Παρτίδας: <b>{row['batch_number']}</b><br>
Έκταση: {row['area']} στρέμματα<br>
Σπορά: <b>{row['sowing_date']}</b><br>
Περιοχή: <b>{row['region']}</b>
</div>
""", unsafe_allow_html=True)

# ======================
# DRONE
# ======================
st.markdown(f"""
<div class="card">
<div class="title">Ψεκασμός με Drone</div>
Ημερομηνία: <b>{row['spray_date']}</b><br>
Σκεύασμα: <b>{row['spray']}</b>
</div>
""", unsafe_allow_html=True)

# ======================
# GROWTH
# ======================
col1, col2, col3 = st.columns(3)

col1.metric("Φάση", row["phase"])
col2.metric("Υγρασία", f"{row['moisture']}%")
col3.metric("Θερμοκρασία", f"{row['temp']}°C")

# ======================
# MAP
# ======================
st.map(pd.DataFrame({"lat":[row["lat"]],"lon":[row["lon"]]}))

# ======================
# QR
# ======================
link = f"{BASE_URL}/?batch={row['batch_number']}"
qr_img = generate_qr(link)

st.image(qr_img, use_container_width=True)

buf = io.BytesIO()
qr_img.save(buf, format="PNG")

st.download_button(
    "Κατέβασε QR",
    data=buf.getvalue(),
    file_name="qr.png",
    mime="image/png"
)

# ======================
# STORY
# ======================
st.markdown(f"""
<div class="card">
<div class="title">Digital Story</div>
{row['story']}
</div>
""", unsafe_allow_html=True)
