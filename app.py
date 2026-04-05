import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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

# --- 2. STYLE CSS UNIFIÉ ET ROBUSTE ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stMarkdown, p, span, label, li { color: #ffffff !important; }
    h1, h2, h3 { color: #ff0000 !important; text-shadow: 2px 2px 10px #ff0000; text-align: center; }

    /* Forçage de la grille d'accueil */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 0% !important;
        min-width: 0 !important;
    }

    /* Design des boutons (Cartes) */
    button[kind="secondary"] {
        width: 100% !important;
        background-color: #161b22 !important;
        border: 2px solid #ff0000 !important;
        border-radius: 15px !important;
        transition: all 0.3s ease !important;
        height: 160px !important;
        box-shadow: 0px 4px 15px rgba(255, 0, 0, 0.2) !important;
    }

    button[kind="secondary"] p {
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        text-align: center !important;
    }

    /* Survol */
    button[kind="secondary"]:hover {
        transform: scale(1.02) !important;
        box-shadow: 0px 0px 25px #ff0000 !important;
        background-color: #1e2129 !important;
    }
    button[kind="secondary"]:hover p { color: #ff0000 !important; }

    /* Bouton Retour */
    .btn-retour button {
        height: auto !important;
        width: auto !important;
        padding: 8px 25px !important;
    }

    /* Centrage Tableaux Ch4 */
    div[data-testid="stTable"] table { margin: auto !important; }
    div[data-testid="stTable"] td, div[data-testid="stTable"] th { text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FONCTIONS ---
def formater_fr(valeur, decimales=2):
    if valeur is None: return "0"
    s = f"{valeur:.{decimales}f}".replace('.', ',').rstrip('0').rstrip(',')
    return s if s != "" and s != "0," else "0"

def aller_a_home():
    st.session_state.clear()
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
    
    # Utilisation d'un container pour forcer le comportement CSS
    with st.container():
        st.markdown('<div class="grille-accueil">', unsafe_allow_html=True)
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            if st.button("🌀 Fonctions :\nGénéralités", key="btn_c0"):
                st.session_state.page = 'chap0'
                st.rerun()
            if st.button("📈 Suites\nNumériques\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0", key="btn_c2"):
                st.session_state.page = 'chap2'
                st.rerun()
            if st.button("📊 Stats :\nProbabilités\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0", key="btn_c4"):
                st.session_state.page = 'chap4'
                st.rerun()

        with col2:
            if st.button("📟 Information\nChiffrée\u00A0\u00A0\u00A0", key="btn_c1"):
                st.session_state.page = 'chap1'
                st.rerun()
            if st.button("🛸 Second\nDegré\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0", key="btn_c3"):
                st.session_state.page = 'chap3'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# =================================================================
# CHAPITRE 0 : FONCTIONS (GÉNÉRALITÉS)
# =================================================================
elif st.session_state.page == 'chap0':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Retour au QG", on_click=aller_a_home)
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
            st.markdown("""
            **Mémo technique :**
            - **x** est l'ANTÉCÉDENT (il vient AVANT).
            - **f(x)** est l'IMAGE (c'est le RÉSULTAT).
            """)

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
        st.subheader("📍 Cohérence Graphique")
        limite = 6
        x_p = np.linspace(-limite, limite, 400)
        y_p = -0.05 * (x_p + 5) * (x_p + 1) * (x_p - 4) 
        fig, (ax_graph, ax_tab) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})
        fig.patch.set_facecolor('#0e1117')
        ax_graph.set_facecolor('#161b22')
        ax_graph.plot(x_p, y_p, color='#ff0000', lw=4)
        ax_graph.axhline(0, color='white', lw=1.5); ax_graph.axvline(0, color='white', lw=1.5)
        ax_graph.tick_params(colors='white'); ax_graph.grid(color='#333333', linestyle='--')
        ax_tab.set_facecolor('#161b22'); ax_tab.axis('off')
        
        # Annotation manuelle asymétrique
        ax_tab.axhline(0.8, color='white', lw=1)
        ax_tab.text(-5.8, 0.9, "-6", color='white', ha='center')
        ax_tab.text(-3.2, 0.9, "-3.2", color='white', ha='center')
        ax_tab.text(1.8, 0.9, "1.8", color='white', ha='center')
        ax_tab.text(5.8, 0.9, "6", color='white', ha='center')
        ax_tab.annotate('', xy=(-3.4, 0.2), xytext=(-5.6, 0.7), arrowprops=dict(arrowstyle='->', color='#ff0000', lw=2))
        ax_tab.annotate('', xy=(1.6, 0.7), xytext=(-3.0, 0.2), arrowprops=dict(arrowstyle='->', color='#ff0000', lw=2))
        ax_tab.annotate('', xy=(5.6, 0.2), xytext=(2.0, 0.7), arrowprops=dict(arrowstyle='->', color='#ff0000', lw=2))

        st.pyplot(fig)
        st.success("✅ f(x) = 0,1(4 - x)(x + 1)(x + 5)")

# =================================================================
# CHAPITRE 1 : INFORMATION CHIFFRÉE
# =================================================================
elif st.session_state.page == 'chap1':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Retour au QG", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("📟 Information Chiffrée")
    tab1, tab2, tab3 = st.tabs(["🔢 Coeff. Multiplicateur", "📈 Taux d'évolution", "🔄 Évolutions Successives"])
    with tab1:
        st.subheader("🎯 Le Multiplicateur Magique")
        st.info("Hausse de t% : $CM = 1 + t/100$ | Baisse de t% : $CM = 1 - t/100$")
        t_in = st.number_input("Taux en %", value=20.0, step=0.1, key="c1t")
        st.metric("Résultat du CM", formater_fr(1 + t_in/100))
    with tab2:
        v_d = st.number_input("Départ (VD)", value=100.0, key="c1vd")
        v_a = st.number_input("Arrivée (VA)", value=125.0, key="c1va")
        if v_d != 0: st.success(f"Taux = {formater_fr(((v_a-v_d)/v_d)*100)} %")
    with tab3:
        ev1 = st.number_input("Hausse/Baisse 1 (%)", value=10.0, key="c1ev1")
        ev2 = st.number_input("Hausse/Baisse 2 (%)", value=-10.0, key="c1ev2")
        cm_g = (1 + ev1/100) * (1 + ev2/100)
        st.metric("Taux global", f"{formater_fr((cm_g-1)*100)} %")

# =================================================================
# CHAPITRE 2 : SUITES NUMÉRIQUES
# =================================================================
elif st.session_state.page == 'chap2':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Retour au QG", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("📈 Chapitre 2 : Suites Numériques")
    t_gen, t_ari, t_geo = st.tabs(["📚 Généralités", "➕ Arithmétiques", "✖️ Géométriques"])
    with t_gen:
        st.subheader("📚 Guide de survie")
        with st.expander("Explicite vs Récurrence"):
            st.latex(r"u_n = f(n) \text{ vs } u_{n+1} = u_n + r")
    with t_ari:
        u0_a = st.number_input("u0", value=10.0, key="ari_u0")
        r_a = st.number_input("r", value=2.0, key="ari_r")
        st.line_chart([u0_a + (i * r_a) for i in range(11)])
    with t_geo:
        u0_g = st.number_input("u0", value=1.0, key="geo_u0")
        q_g = st.number_input("q", value=2.0, key="geo_q")
        st.area_chart([u0_g * (q_g ** i) for i in range(11)])

# =================================================================
# CHAPITRE 3 : POLYNÔMES DU 2ND DEGRÉ
# =================================================================
elif st.session_state.page == 'chap3':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Retour au QG", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("🛸 Chapitre 3 : Second Degré")
    t_cours, t_galerie, t_calc = st.tabs(["📚 Les 3 Formes", "🖼️ Galerie", "📈 Simulateur"])
    with t_cours:
        st.latex(r"ax^2 + bx + c")
    with t_galerie:
        x_p = np.linspace(-6, 6, 400); y_p = 2*x_p**2 + 4*x_p - 6
        fig, ax = plt.subplots(); fig.patch.set_facecolor('#0e1117'); ax.set_facecolor('#161b22')
        ax.plot(x_p, y_p, color='#ff0000', lw=4); ax.grid(color='#333333'); ax.tick_params(colors='white')
        st.pyplot(fig)
    with t_calc:
        sa = st.slider("a", -4.0, 4.0, 1.0); s_alpha = st.number_input("Alpha", value=0.0)
        s_beta = st.number_input("Beta", value=0.0)
        x_sim = np.linspace(s_alpha-10, s_alpha+10, 100); y_sim = sa*(x_sim-s_alpha)**2 + s_beta
        st.line_chart(pd.DataFrame({'y': y_sim}, index=x_sim))

# =================================================================
# CHAPITRE 4 : PROBABILITÉS
# =================================================================
elif st.session_state.page == 'chap4':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Retour au QG", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("🎲 Chapitre 4 : Probabilités")
    tab_cours, tab_tab, tab_arbre = st.tabs(["📚 Rappels", "📊 Tableau", "🌳 Arbre"])
    with tab_tab:
        df_prob = pd.DataFrame({"Garçons": [12, 8, 20], "Filles": [15, 5, 20], "Total": [27, 13, 40]}, index=["Sport", "Non Sport", "Total"])
        st.table(df_prob)
    with tab_arbre:
        fig, ax = plt.subplots(figsize=(10, 5)); fig.patch.set_facecolor('#0e1117'); ax.set_facecolor('#161b22')
        ax.plot([0, 1], [0, 1], color='#ff0000', lw=3); ax.plot([0, 1], [0, -1], color='#ff0000', lw=3)
        ax.scatter([0, 1, 1], [0, 1, -1], color='#00d4ff', s=200); ax.axis('off')
        st.pyplot(fig)
