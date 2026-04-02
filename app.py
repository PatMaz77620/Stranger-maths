import streamlit as st
from PIL import Image
import random

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Stranger Maths",
    page_icon="🔦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 🎯 INITIALISATION CRUCIALE DU STATE ---
# Ce bloc doit être AVANT toute lecture de st.session_state.page
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- 2. STYLE CSS UNIFIÉ (VERSION "FULL WIDTH" GARANTIE) ---
st.markdown("""
    <style>
    /* FOND ET TEXTE GÉNÉRAL */
    .stApp { background-color: #0e1117; }
    .stMarkdown, p, span, label, li { color: #ffffff !important; }
    h1, h2, h3 { color: #ff0000 !important; text-shadow: 2px 2px 10px #ff0000; text-align: center; }

    /* 🎯 --- LA FORCE BRUTE POUR L'UNIFORMISATION --- 🎯 */
    /* On force TOUS les conteneurs de colonnes à laisser leurs enfants prendre 100% */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 0% !important;
        min-width: 0 !important;
    }
    
    [data-testid="column"] > div {
        width: 100% !important;
    }

    /* On force le bouton Streamlit à ignorer la largeur de son texte */
    div.stButton, div.stButton > button {
        width: 100% !important;
        display: block !important;
    }

    /* 🏎️ LE LOOK DES CARTES */
    button[kind="secondary"] {
        height: 160px !important;
        border-radius: 15px !important;
        border: 2px solid #ff0000 !important;
        background-color: #161b22 !important;
        box-shadow: 0px 4px 15px rgba(255, 0, 0, 0.2) !important;
        transition: all 0.3s ease !important;
        margin-bottom: 10px !important;
    }

    /* ⚪ TEXTE BLANC ET CENTRÉ DANS LE BOUTON */
    button[kind="secondary"] p, 
    button[kind="secondary"] span {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        text-align: center !important;
        display: block !important;
        width: 100% !important;
    }

    /* 🔴 SURVOL */
    button[kind="secondary"]:hover {
        transform: scale(1.02) !important;
        box-shadow: 0px 0px 25px #ff0000 !important;
        border-color: #ff0000 !important;
    }
    button[kind="secondary"]:hover p {
        color: #ff0000 !important;
        -webkit-text-fill-color: #ff0000 !important;
    }

    /* BOUTON RETOUR (On le protège de l'étirement) */
    .btn-retour {
        display: inline-block !important;
        width: auto !important;
    }
    .btn-retour button {
        height: auto !important;
        width: auto !important;
        padding: 5px 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FONCTIONS UTILES ---
def formater_fr(valeur, decimales=2):
    if valeur is None: return "0"
    s = f"{valeur:.{decimales}f}".replace('.', ',').rstrip('0').rstrip(',')
    return s if s != "" and s != "0," else "0"

def aller_a_home():
    st.session_state.page = 'home'

# --- GESTION DU LOGO ---
chemin_logo = "Stranger_Maths_Logo.png"

# =================================================================
# PAGE D'ACCUEIL
# =================================================================
if st.session_state.page == 'home':
    # ... ton logo ...

    st.write("### 🎮 Choisissez votre mission :")
    
    # Ligne 1
    c1, c2 = st.columns(2)
    with c1:
        st.button("🌀 Fonctions :\nGénéralités", key="c0-btn")
    with c2:
        st.button("📟 Information\nChiffrée", key="c1-btn")

    # Ligne 2
    c3, c4 = st.columns(2)
    with c3:
        st.button("📈 Suites\nNumériques", key="c2-btn")
    with c4:
        st.button("🛸 Second\nDegré", key="c3-btn")
    
    # Gestion des clics (plus propre)
    if st.session_state["c0-btn"]: st.session_state.page = 'chap0'; st.rerun()
    if st.session_state["c1-btn"]: st.session_state.page = 'chap1'; st.rerun()
    if st.session_state["c2-btn"]: st.session_state.page = 'chap2'; st.rerun()
    if st.session_state["c3-btn"]: st.session_state.page = 'chap3'; st.rerun()

# =================================================================
# LES CHAPITRES (0, 1, 2, 3)
# =================================================================

# --- CHAPITRE 0 ---
elif st.session_state.page == 'chap0':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Retour", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("🌀 Fonctions : Généralités")
    # ... (Reste de ton code pour chap0)

# --- CHAPITRE 1 ---
elif st.session_state.page == 'chap1':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Menu", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("📟 Information Chiffrée")
    # ... (Reste de ton code pour chap1)

# --- CHAPITRE 2 ---
elif st.session_state.page == 'chap2':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Menu", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("📈 Suites Numériques")
    # ... (Reste de ton code pour chap2)

# --- CHAPITRE 3 ---
elif st.session_state.page == 'chap3':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Menu", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("🛸 Second Degré")
    # ... (L'onglet Galerie avec les couleurs synchro va ici)
