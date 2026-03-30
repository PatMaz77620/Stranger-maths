import streamlit as st
from PIL import Image
import random
import os

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Stranger Maths",
    page_icon="🔦",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. STYLE CSS (CORRECTION FINALE DU MENU) ---
st.markdown("""
    <style>
    /* 1. FOND ET TEXTE GENERAUX */
    .stApp { background-color: #0e1117; }
    .stMarkdown, p, span, label, li, .stExpander p { color: #ffffff !important; }
    h1, h2, h3 { color: #ff0000 !important; font-family: 'Helvetica'; text-shadow: 2px 2px 8px #ff0000; }

    /* 2. SIDEBAR */
    [data-testid="collapsedControl"] { display: none !important; }
    section[data-testid="stSidebar"] { background-color: #12151d !important; border-right: 2px solid #ff0000; }

    /* 3. 🎯 FIX ULTIME DU MENU DÉROULANT (LA PARTIE BLANCHE) */

    /* On force le conteneur du menu fermé en noir/rouge */
    div[data-baseweb="select"] > div {
        background-color: #1e2129 !important;
        color: white !important;
        border: 1px solid #ff0000 !important;
    }

    /* ICI LE FIX POUR LA PARTIE DÉROULANTE (POPOVER) */
    /* On cible globalement toutes les listes de sélection du site */
    [data-baseweb="popover"] div, [role="listbox"] {
        background-color: #1e2129 !important; /* Fond sombre */
    }

    [data-baseweb="popover"] li, [role="option"] {
        color: white !important; /* Texte blanc pour chaque ligne */
        background-color: #1e2129 !important;
    }

    /* Effet quand on passe la souris sur une ligne de la liste */
    [data-baseweb="popover"] li:hover, [role="option"]:hover {
        background-color: #ff0000 !important; /* Devient rouge */
        color: white !important;
    }

    /* --- EXPANDERS & TABS --- */
    .streamlit-expanderHeader { background-color: #1e2129 !important; border: 1px solid #ff0000 !important; }
    button[data-baseweb="tab"] p { color: #ffffff !important; }
    button[aria-selected="true"] p { color: #ff0000 !important; font-weight: bold; }

    /* BOUTONS */
    div.stButton > button {
        background-color: #0e1117 !important;
        color: #ff0000 !important;
        border: 2px solid #ff0000 !important;
        border-radius: 10px;
    }
    div.stButton > button:hover { background-color: #ff0000 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

def formater_fr(valeur, decimales=2):
    if valeur is None: return "0"
    s = f"{valeur:.{decimales}f}".replace('.', ',').rstrip('0').rstrip(',')
    return s if s != "" and s != "0," else "0"


# --- 3. SIDEBAR & LOGO ---
chemin_logo = "Stranger_Maths_Logo.png"
try:
    img = Image.open(chemin_logo)
    logo = img.resize((220, int(220 * img.size[1] / img.size[0])), Image.LANCZOS)
    st.sidebar.image(logo)
except:
    st.sidebar.title("🔦 STRANGER MATHS")

st.sidebar.title("🎮 Chapitres")
chapitre = st.sidebar.selectbox("Navigation :", ["Information Chiffrée", "Suites Numériques"])

# =================================================================
# CHAPITRE 1 : INFORMATION CHIFFRÉE
# =================================================================
if chapitre == "Information Chiffrée":
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
else:
    st.title("📈 Chapitre 2 : Suites Numériques")
    t_gen, t_ari, t_geo = st.tabs(["📚 Généralités", "➕ Arithmétiques", "✖️ Géométriques"])

    with t_gen:
        st.subheader("📚 Guide de survie : Généralités")

        # --- BLOC 1 : RECONNAISSANCE ---
        with st.expander("🤔 Comment différencier Explicite et Récurrence ?"):
            st.write("**Tuyau de Dustin :** Regarde ce qu'il y a après le signe égal.")
            st.write("- Si tu vois un **n** seul : c'est **Explicite**. Tu calcules ce que tu veux tout de suite.")
            st.latex(r"u_n = 5n - 2 \rightarrow u_{10} = 5(10)-2 = 48")
            st.write("- Si tu vois un **u_n** : c'est **Récurrence**. Tu es bloqué, il te faut le terme d'avant.")
            st.latex(r"u_{n+1} = u_n + 10")

        # --- BLOC 2 : DÉMONSTRATION DU TYPE ---
        with st.expander("🛠️ Comment démontrer le type de suite ?"):
            st.write("### ➕ Arithmétique ?")
            st.info(
                r"Méthode : Calcule la différence $u_{n+1} - u_n$. Si le résultat est un nombre fixe (ex: 5), c'est la raison $r$.")
            st.write("### ✖️ Géométrique ?")
            st.info(
                r"Méthode : Calcule le quotient $u_{n+1} / u_n$. Si le résultat est un nombre fixe (ex: 1,02), c'est la raison $q$.")

        # --- BLOC 3 : MONOTONIE ---
        with st.expander("📉 Comment démontrer la Monotonie ?"):
            st.write(r"**Tuyau de Lucas :** Calcule $u_{n+1} - u_n$ et regarde son signe.")
            # Utilisation du 'r' pour corriger les flèches
            st.success(r"Signe Positif (+) $\rightarrow$ La suite est **Croissante**.")
            st.warning(r"Signe Négatif (-) $\rightarrow$ La suite est **Décroissante**.")
            st.divider()
            st.write("⚠️ **Cas particulier : Ni l'un ni l'autre**")
            st.write("Si le signe change tout le temps (ex: suite alternée), la suite n'est **pas monotone**.")
            st.latex(r"u_n = (-1)^n \rightarrow \{1; -1; 1; -1...\}")

    with t_ari:
        u0_a = st.number_input("u0", value=10.0, key="u0a_input")
        r_a = st.number_input("Raison r", value=2.0, key="ra_input")
        st.line_chart([u0_a + (i * r_a) for i in range(11)])

    with t_geo:
        u0_g = st.number_input("Capital (€)", value=1000.0, key="u0g_input")
        q_g = st.number_input("Raison q", value=1.03, step=0.01, key="qg_input")
        st.area_chart([u0_g * (q_g ** i) for i in range(11)])

    # --- NOUVEAU SYSTÈME DE DÉFI POUR LES SUITES ---
    st.divider()
    st.write("### ❓ Défi des Suites")

    # Initialisation du défi si non présent
    if 'suite_type' not in st.session_state:
        st.session_state.suite_type = random.choice(["Arithmétique", "Géométrique"])
        st.session_state.s_u0 = random.randint(2, 10)
        st.session_state.s_raison = random.randint(2,
                                                   5) if st.session_state.suite_type == "Arithmétique" else random.choice(
            [2, 3])
        st.session_state.s_n = random.randint(2, 4)  # On demande u2, u3 ou u4

    st.write(f"Soit une suite **{st.session_state.suite_type}**.")
    st.write(f"Premier terme **u0 = {st.session_state.s_u0}**.")

    if st.session_state.suite_type == "Arithmétique":
        st.write(f"Raison **r = {st.session_state.s_raison}**.")
        corr_suite = st.session_state.s_u0 + (st.session_state.s_n * st.session_state.s_raison)
    else:
        st.write(f"Raison **q = {st.session_state.s_raison}**.")
        corr_suite = st.session_state.s_u0 * (st.session_state.s_raison ** st.session_state.s_n)

    rep_suite = st.number_input(f"Calcule la valeur de u{st.session_state.s_n} :", value=0.0, key="rep_suite")

    col_s1, col_s2 = st.columns(2)
    if col_s1.button("Vérifier"):
        if abs(rep_suite - corr_suite) < 0.01:
            st.balloons()
            st.success(f"Bravo ! u{st.session_state.s_n} était bien égal à {corr_suite}")
        else:
            st.error(f"Faux ! Le résultat était {corr_suite}")

    if col_s2.button("Autre défi 🔄", key="reset_suite"):
        # On supprime les variables pour forcer la création d'un nouveau défi au prochain passage
        del st.session_state.suite_type
        st.rerun()
