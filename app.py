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

# --- 🎯 INITIALISATION DU STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- 2. STYLE CSS VERSION GRILLE FORCÉE ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stMarkdown, p, span, label, li { color: #ffffff !important; }
    h1, h2, h3 { 
        color: #ff0000 !important; 
        text-shadow: 2px 2px 10px #ff0000; 
        text-align: center;
    }

    [data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: 1fr 1fr !important;
        gap: 15px !important;
    }

    [data-testid="column"] {
        width: 100% !important;
        max-width: 100% !important;
        flex: none !important;
    }

    div[data-testid="stButton"], div[data-testid="stButton"] button {
        width: 100% !important;
    }

    button[kind="secondary"] {
        width: 100% !important;
        height: 160px !important;
        border-radius: 15px !important;
        border: 2px solid #ff0000 !important;
        background-color: #161b22 !important;
        box-shadow: 0px 4px 15px rgba(255, 0, 0, 0.2) !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }

    button[kind="secondary"] div[data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        text-align: center !important;
    }

    button[kind="secondary"]:hover {
        transform: scale(1.02) !important;
        background-color: #1e2129 !important;
        box-shadow: 0px 0px 25px #ff0000 !important;
    }
    
    button[kind="secondary"]:hover div[data-testid="stMarkdownContainer"] p {
        color: #ff0000 !important;
        -webkit-text-fill-color: #ff0000 !important;
    }

    .btn-retour {
        display: block !important;
        width: fit-content !important;
        margin-bottom: 20px;
    }
    .btn-retour button {
        height: auto !important;
        width: auto !important;
        padding: 5px 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FONCTIONS ---
def formater_fr(valeur, decimales=2):
    if valeur is None: return "0"
    s = f"{valeur:.{decimales}f}".replace('.', ',').rstrip('0').rstrip(',')
    return s if s != "" and s != "0," else "0"

def aller_a_home():
    st.session_state.page = 'home'

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
    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌀 Fonctions :\nGénéralités", key="btn_c0"):
            st.session_state.page = 'chap0'
            st.rerun()
        if st.button("📈 Suites\nNumériques", key="btn_c2"):
            st.session_state.page = 'chap2'
            st.rerun()
        if st.button("📊 Stats :\nProbabilités", key="btn_c4"):
            st.session_state.page = 'chap4'
            st.rerun()

    with col2:
        if st.button("📟 Information\nChiffrée", key="btn_c1"):
            st.session_state.page = 'chap1'
            st.rerun()
        if st.button("🛸 Second\nDegré", key="btn_c3"):
            st.session_state.page = 'chap3'
            st.rerun()

# =================================================================
# CHAPITRE 0
# =================================================================
elif st.session_state.page == 'chap0':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Retour", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("🌀 Fonctions : Généralités")
    st.write("---")
    
    tab1, tab2, tab3 = st.tabs([
        "🚪 Portail (Images/Antécédents)", 
        "🗺️ Territoire (Domaine)", 
        "📍 Lecture de Carte"
    ])

    with tab1:
        st.subheader("⚙️ La Machine à Transformer")
        st.info("Une fonction est un processus. On entre un nombre **x** (antécédent), on applique une règle, et il ressort un nombre **f(x)** (image).")
        col_calc, col_viz = st.columns([1, 1])
        with col_calc:
            st.write("**Exemple : $f(x) = 2x^2 - 3$**")
            input_x = st.number_input("Choisissez un antécédent (x) :", value=3.0)
            result_f = 2*(input_x**2) - 3
            st.success(f"L'image de **{input_x}** est **{result_f}**")
            st.latex(r"f(" + str(input_x) + r") = " + str(result_f))
        with col_viz:
            st.markdown("- **x** est l'ANTÉCÉDENT (avant).\n- **f(x)** est l'IMAGE (résultat).")

    with tab2:
        st.subheader("🚧 Le Territoire de la fonction")
        c1, c2 = st.columns(2)
        with c1:
            st.error("🚫 **La Division par Zéro**")
            st.latex(r"g(x) = \frac{5}{x - 4}")
            st.write("**Domaine :** $\mathbb{R} \setminus \{4\}$")
        with c2:
            st.error("🚫 **La Racine Négative**")
            st.latex(r"h(x) = \sqrt{x + 2}")
            st.write("**Domaine :** $[-2 \ ; \ +\infty[$")

    with tab3:
        st.subheader("📍 Lecture de Carte")
        import matplotlib.pyplot as plt
        import numpy as np
        x_p = np.linspace(-6, 6, 400)
        y_p = -0.05 * (x_p + 5) * (x_p + 1) * (x_p - 4) 
        fig, (ax_graph, ax_tab) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})
        fig.patch.set_facecolor('#0e1117')
        ax_graph.set_facecolor('#161b22')
        ax_graph.plot(x_p, y_p, color='#ff0000', lw=4)
        ax_graph.axhline(0, color='white', lw=1.5); ax_graph.axvline(0, color='white', lw=1.5)
        ax_graph.tick_params(colors='white'); ax_graph.grid(color='#333333', linestyle='--')
        ax_tab.set_facecolor('#161b22')
        ax_tab.axis('off')
        st.pyplot(fig)

# =================================================================
# CHAPITRE 1
# =================================================================
elif st.session_state.page == 'chap1':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Menu", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("📟 Information Chiffrée")
    tab1, tab2, tab3 = st.tabs(["🔢 Coeff. Multiplicateur", "📈 Taux d'évolution", "🔄 Évolutions Successives"])
    with tab1:
        t_in = st.number_input("Taux en %", value=20.0, step=0.1)
        st.success(f"CM = **{formater_fr(1 + t_in / 100)}**")
    with tab2:
        v_d = st.number_input("Valeur de Départ", value=100.0)
        v_a = st.number_input("Valeur d'Arrivée", value=125.0)
        if v_d != 0: st.success(f"Taux = **{formater_fr(((v_a-v_d)/v_d)*100)} %**")
    with tab3:
        ev1 = st.number_input("Taux 1 (%)", value=10.0)
        ev2 = st.number_input("Taux 2 (%)", value=-10.0)
        cm_g = (1+ev1/100)*(1+ev2/100)
        st.success(f"Evolution totale : **{formater_fr((cm_g-1)*100)} %**")

# =================================================================
# CHAPITRE 4 : STATISTIQUES
# =================================================================
elif st.session_state.page == 'chap4':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Menu", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("📊 Statistiques & Arbres")
    t1, t2 = st.tabs(["📋 Tableau Croisé", "🌳 Arbre de Choix"])
    with t1:
        st.markdown("| | Pouvoirs | Pas Pouvoirs | Total |\n|---|---|---|---|\n| Enfant | 2 | 18 | 20 |\n| Adulte | 1 | 29 | 30 |\n| Total | 3 | 47 | 50 |")
        v1 = st.number_input("Valeur case", value=2)
        v2 = st.number_input("Valeur total", value=20)
        if v2 > 0: st.success(f"Fréquence = **{formater_fr((v1/v2)*100)} %**")
    with t2:
        st.code("Départ -> [Choix A] -> Résultat 1\n       -> [Choix B] -> Résultat 2")
