import streamlit as st
from PIL import Image
import random

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Stranger Maths",
    page_icon="🔦",
    layout="centered",
    initial_sidebar_state="collapsed" # On cache la sidebar par défaut
)

# --- 2. STYLE CSS AMÉLIORÉ ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* Force le texte en BLANC PUR pour la lisibilité */
    .stMarkdown, p, span, label, li, .stExpander p { 
        color: #ffffff !important; 
    }
    
    /* TITRES ROUGES NÉON */
    h1, h2, h3 { 
        color: #ff0000 !important; 
        font-family: 'Helvetica', sans-serif; 
        text-shadow: 2px 2px 10px #ff0000; 
        text-align: center;
    }

    /* CARTES DE SÉLECTION (HOME) */
    .menu-card {
        background-color: #1e2129;
        border: 2px solid #ff0000;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: 0.3s;
        cursor: pointer;
        margin-bottom: 10px;
    }
    .menu-card:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 15px #ff0000;
    }

    /* FIX EXPANDERS & TABS */
    .streamlit-expanderHeader { 
        background-color: #1e2129 !important; 
        border: 1px solid #ff0000 !important; 
        color: white !important;
    }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; }
    .stTabs [aria-selected="true"] { color: #ff0000 !important; font-weight: bold; }

    /* BOUTONS */
    div.stButton > button {
        background-color: #0e1117 !important;
        color: #ff0000 !important;
        border: 2px solid #ff0000 !important;
        border-radius: 10px;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #ff0000 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialisation de la navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def formater_fr(valeur, decimales=2):
    if valeur is None: return "0"
    s = f"{valeur:.{decimales}f}".replace('.', ',').rstrip('0').rstrip(',')
    return s if s != "" and s != "0," else "0"

# --- 3. GESTION DU LOGO ---
chemin_logo = "Stranger_Maths_Logo.png"

# --- FONCTION RETOUR ---
def aller_a_home():
    st.session_state.page = 'home'

# =================================================================
# PAGE D'ACCUEIL (MENU PAR CARTES)
# =================================================================
if st.session_state.page == 'home':
    # Logo central
    try:
        img = Image.open(chemin_logo)
        st.image(img, use_container_width=True)
    except:
        st.title("🔦 STRANGER MATHS")

    st.write("### 🎮 Choisissez votre mission :")
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="menu-card"><h3>📟</h3><p>Information Chiffrée</p></div>', unsafe_allow_html=True)
        if st.button("Accéder au Chapitre 1"):
            st.session_state.page = 'chap1'
            st.rerun()

    with col2:
        st.markdown('<div class="menu-card"><h3>📈</h3><p>Suites Numériques</p></div>', unsafe_allow_html=True)
        if st.button("Accéder au Chapitre 2"):
            st.session_state.page = 'chap2'
            st.rerun()

# =================================================================
# CHAPITRE 1 : INFORMATION CHIFFRÉE
# =================================================================
elif st.session_state.page == 'chap1':
    st.button("⬅️ Retour au menu principal", on_click=aller_a_home)
    st.title("📟 Chapitre 1 : Information Chiffrée")
    
    tab1, tab2, tab3 = st.tabs(["🔢 Coeff. Multiplicateur", "📈 Taux d'évolution", "🔄 Évolutions Successives"])

    with tab1:
        st.info("💡 $CM = 1 + t/100$ (hausse) ou $1 - t/100$ (baisse)")
        t_in = st.number_input("Taux (%)", value=20.0, step=0.1, key="c1t")
        st.success(f"Le CM est de **{formater_fr(1 + t_in / 100)}**")

    with tab2:
        ca, cb = st.columns(2)
        v_d = ca.number_input("Départ (VD)", value=100.0, key="c1vd")
        v_a = cb.number_input("Arrivée (VA)", value=125.0, key="c1va")
        if v_d != 0:
            st.info(f"Taux : **{formater_fr(((v_a - v_d) / v_d) * 100)} %**")

    # DÉFI 1
    st.divider()
    if 'vd1' not in st.session_state:
        st.session_state.vd1, st.session_state.tx1 = 100, 20
    st.write(f"### ❓ Défi : Hausse de {st.session_state.tx1}% sur {st.session_state.vd1}")
    rep1 = st.number_input("Réponse ?", value=0.0, key="r1")
    if st.button("Vérifier"):
        corr = st.session_state.vd1 * (1 + st.session_state.tx1 / 100)
        if abs(rep1 - corr) < 0.1:
            st.balloons(); st.success("Bravo !")
        else:
            st.error(f"Faux, c'était {formater_fr(corr)}")

# =================================================================
# CHAPITRE 2 : SUITES NUMÉRIQUES
# =================================================================
elif st.session_state.page == 'chap2':
    st.button("⬅️ Retour au menu principal", on_click=aller_a_home)
    st.title("📈 Chapitre 2 : Suites Numériques")
    
    t_gen, t_ari, t_geo = st.tabs(["📚 Généralités", "➕ Arithmétiques", "✖️ Géométriques"])

    with t_gen:
        st.subheader("📚 Guide de survie : Généralités")
        with st.expander("🤔 Comment différencier Explicite et Récurrence ?"):
            st.write("**Tuyau de Dustin :** Regarde ce qu'il y a après le signe égal.")
            st.write("- Si tu vois un **n** seul : c'est **Explicite**.")
            st.latex(r"u_n = 5n - 2 \rightarrow u_{10} = 48")
            st.write("- Si tu vois un **u_n** : c'est **Récurrence**.")
            st.latex(r"u_{n+1} = u_n + 10")

        with st.expander("🛠️ Comment démontrer le type de suite ?"):
            st.write("### ➕ Arithmétique ?")
            st.info(r"Méthode : Calcule $u_{n+1} - u_n$. Si c'est un nombre fixe $r$, c'est arithmétique.")
            st.write("### ✖️ Géométrique ?")
            st.info(r"Méthode : Calcule $u_{n+1} / u_n$. Si c'est un nombre fixe $q$, c'est géométrique.")

        with st.expander("📉 Comment démontrer la Monotonie ?"):
            st.write(r"**Tuyau de Lucas :** Calcule $u_{n+1} - u_n$ et regarde son signe.")
            st.success(r"Signe Positif (+) $\rightarrow$ La suite est **Croissante**.")
            st.warning(r"Signe Négatif (-) $\rightarrow$ La suite est **Décroissante**.")

    with t_ari:
        u0_a = st.number_input("u0", value=10.0, key="u0a_input")
        r_a = st.number_input("Raison r", value=2.0, key="ra_input")
        st.line_chart([u0_a + (i * r_a) for i in range(11)])

    with t_geo:
        u0_g = st.number_input("Capital (€)", value=1000.0, key="u0g_input")
        q_g = st.number_input("Raison q", value=1.03, step=0.01, key="qg_input")
        st.area_chart([u0_g * (q_g ** i) for i in range(11)])

    st.divider()
    st.write("### ❓ Défi des Suites")

    if 'suite_type' not in st.session_state:
        st.session_state.suite_type = random.choice(["Arithmétique", "Géométrique"])
        st.session_state.s_u0 = random.randint(2, 10)
        st.session_state.s_raison = random.randint(2, 5) if st.session_state.suite_type == "Arithmétique" else random.choice([2, 3])
        st.session_state.s_n = random.randint(2, 4)

    st.write(f"Soit une suite **{st.session_state.suite_type}**.")
    st.write(f"Premier terme **u0 = {st.session_state.s_u0}**.")

    if st.session_state.suite_type == "Arithmétique":
        st.write(f"Raison **r = {st.session_state.s_raison}**.")
        corr_suite = st.session_state.s_u0 + (st.session_state.s_n * st.session_state.s_raison)
    else:
        st.write(f"Raison **q = {st.session_state.s_raison}**.")
        corr_suite = st.session_state.s_u0 * (st.session_state.s_raison ** st.session_state.s_n)

    rep_suite = st.number_input(f"Calcule u{st.session_state.s_n} :", value=0.0, key="rep_suite")

    col_s1, col_s2 = st.columns(2)
    if col_s1.button("Vérifier"):
        if abs(rep_suite - corr_suite) < 0.01:
            st.balloons(); st.success(f"Bravo ! C'était {corr_suite}")
        else:
            st.error(f"Faux ! Le résultat était {corr_suite}")

    if col_s2.button("Autre défi 🔄"):
        del st.session_state.suite_type
        st.rerun()
