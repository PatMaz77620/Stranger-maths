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

# --- 2. STYLE CSS UNIFIÉ (FORCE BRUTE) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* TEXTE BLANC GÉNÉRAL */
    .stMarkdown, p, span, label, li { color: #ffffff !important; }

    /* TITRES ROUGES NÉON */
    h1, h2, h3 { 
        color: #ff0000 !important; 
        text-shadow: 2px 2px 10px #ff0000; 
        text-align: center;
    }

    /* 🎯 UNIFORMISATION DES BOUTONS (CARTES) */
    /* On cible le conteneur de la colonne pour forcer le bouton à s'étirer */
    [data-testid="column"] {
        width: 100% !important;
    }

    button[kind="secondary"] {
        width: 100% !important;
        height: 160px !important;
        border-radius: 15px !important;
        border: 2px solid #ff0000 !important;
        background-color: #161b22 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0px 4px 15px rgba(255, 0, 0, 0.2) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* ⚪ FORCE LE TEXTE EN BLANC PUR (ÉLIMINE LE GRIS) */
    button[kind="secondary"] p, 
    button[kind="secondary"] span {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-size: 1.25rem !important;
        font-weight: bold !important;
        text-align: center !important;
    }

    /* 🔴 EFFET AU SURVOL */
    button[kind="secondary"]:hover {
        transform: scale(1.02) !important;
        background-color: #1e2129 !important;
        box-shadow: 0px 0px 25px #ff0000 !important;
    }
    
    button[kind="secondary"]:hover p, 
    button[kind="secondary"]:hover span {
        color: #ff0000 !important;
        -webkit-text-fill-color: #ff0000 !important;
    }

    /* BOUTON RETOUR */
    .btn-retour button {
        height: auto !important;
        width: auto !important;
        min-width: 100px !important;
        padding: 5px 15px !important;
    }
    .btn-retour button p { font-size: 0.9rem !important; }

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
    try:
        img = Image.open(chemin_logo)
        st.image(img, use_container_width=True)
    except:
        st.title("🔦 STRANGER MATHS")

    st.write("### 🎮 Choisissez votre mission :")
    
    # Grille 2x2
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🌀 Fonctions :\nGénéralités", key="c0-btn"):
            st.session_state.page = 'chap0'
            st.rerun()
        if st.button("📈 Suites\nNumériques", key="c2-btn"):
            st.session_state.page = 'chap2'
            st.rerun()

    with c2:
        if st.button("📟 Information\nChiffrée", key="c1-btn"):
            st.session_state.page = 'chap1'
            st.rerun()
        if st.button("🛸 Second\nDegré", key="c3-btn"):
            st.session_state.page = 'chap3'
            st.rerun()

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
