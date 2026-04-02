import streamlit as st

st.set_page_config(layout="wide")

# ======================
# CUSTOM CSS (το μυστικό για mobile look)
# ======================
st.markdown("""
<style>
body {
    background-color: #f3f7f3;
}

.main-container {
    max-width: 420px;
    margin: auto;
    background: #ffffff;
    border-radius: 25px;
    padding: 15px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
}

/* Header */
.header {
    background: linear-gradient(135deg, #2e7d32, #4caf50);
    padding: 15px;
    border-radius: 20px;
    color: white;
    font-size: 18px;
    font-weight: bold;
}

/* Card */
.card {
    background: #ffffff;
    border-radius: 15px;
    padding: 12px;
    margin-top: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* Title */
.section-title {
    font-weight: bold;
    color: #2e7d32;
    margin-bottom: 5px;
}

/* Small boxes */
.mini-card {
    background: #f3f7f3;
    padding: 10px;
    border-radius: 12px;
    text-align: center;
}

/* Bottom nav */
.bottom-nav {
    display: flex;
    justify-content: space-around;
    margin-top: 15px;
    font-size: 12px;
    color: #2e7d32;
}
</style>
""", unsafe_allow_html=True)

# ======================
# APP UI
# ======================
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
🌱 Ψηφιακό Διαβατήριο Οσπρίων
</div>
""", unsafe_allow_html=True)

# Batch Input
batch = st.text_input("Batch Number", "GR-2023-0578")

# ======================
# ΠΛΗΡΟΦΟΡΙΕΣ ΠΑΡΤΙΔΑΣ
# ======================
st.markdown("""
<div class="card">
<div class="section-title">📦 Πληροφορίες Παρτίδας</div>
Αρ. Παρτίδας: <b>2023-004</b><br>
Έκταση: 12 στρέμματα<br>
Ημερομηνία Σποράς: <b>15 Μαΐου 2023</b><br>
Περιοχή: <b>Λευκωνότοπος</b>
</div>
""", unsafe_allow_html=True)

# ======================
# DRONE
# ======================
st.markdown("""
<div class="card">
<div class="section-title">🚁 Ψεκασμός με Drone</div>
Τελευταίος Ψεκασμός: <b>10 Ιουλίου 2023</b><br>
Σκεύασμα: <b>Βιολογικό Εντομοκτόνο</b>
</div>
""", unsafe_allow_html=True)

# ======================
# ΑΝΑΠΤΥΞΗ
# ======================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🌱 Ανάπτυξη Καλλιέργειας</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="mini-card">🌸<br>Ανθοφορία</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="mini-card">💧<br>26%</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="mini-card">☀️<br>29°C</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ======================
# ΙΧΝΗΛΑΣΙΜΟΤΗΤΑ
# ======================
st.markdown("""
<div class="card">
<div class="section-title">🔎 Ιχνηλασιμότητα</div>
📄 Πιστοποιήσεις<br>
🧪 Αναλύσεις<br>
🚛 Διαδρομή Προϊόντος
</div>
""", unsafe_allow_html=True)

# ======================
# BOTTOM NAV
# ======================
st.markdown("""
<div class="bottom-nav">
🏠 Αρχική  
📊 Παρακολούθηση  
📄 Αναφορές  
👤 Προφίλ
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
