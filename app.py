import streamlit as st
from PIL import Image
import random

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Stranger Maths",
    page_icon="🔦",
    layout="centered",
    initial_sidebar_state="collapsed" # Sidebar cachée pour le look "Cards"
)

# --- 2. STYLE CSS AMÉLIORÉ (CARTES CLIQUABLES) ---
st.markdown("""
    <style>
    /* FOND GÉNÉRAL */
    .stApp { background-color: #0e1117; }
    
    /* TEXTE BLANC PUR pour la lisibilité */
    .stMarkdown, p, span, label, li, .stExpander p { 
        color: #ffffff !important; 
    }
    
    /* TITRES ROUGES NÉON CENTRÉS */
    h1, h2, h3 { 
        color: #ff0000 !important; 
        font-family: 'Helvetica', sans-serif; 
        text-shadow: 2px 2px 10px #ff0000; 
        text-align: center;
        margin-top: 0px;
    }

    /* 🎯 --- STYLISATION DES CARTES COMME BOUTONS --- 🎯 */
    /* On cible les boutons Streamlit spécifiques pour les transformer en cartes */
    div.stButton > button.css-1x8cf1d, div.stButton > button {
        background-color: #1e2129 !important;
        border: 2px solid #ff0000 !important;
        border-radius: 20px !important;
        padding: 40px 20px !important; /* Plus grand pour le look carte */
        text-align: center !important;
        width: 100% !important;
        height: 200px !important; /* Hauteur fixe pour les cartes */
        transition: 0.3s !important;
        margin-bottom: 20px !important;
        display: block !important;
    }

    /* Contenu à l'intérieur du bouton (Titre et icône) */
    div.stButton > button p {
        color: #ff0000 !important; /* Titre en rouge néon */
        font-size: 1.5rem !important;
        font-weight: bold !important;
        font-family: 'Helvetica', sans-serif;
        text-shadow: 1px 1px 5px #ff0000;
        margin: 0 !important;
    }
    
    /* Icône plus grande au-dessus du texte */
    div.stButton > button::before {
        font-size: 3rem !important;
        display: block;
        margin-bottom: 10px;
    }
    
    /* Spécifique pour l'icône de la carte 1 */
    key-c1-btn::before { content: "📟"; }
    /* Spécifique pour l'icône de la carte 2 */
    key-c2-btn::before { content: "📈"; }

    /* EFFET AU SURVOL (HOVER) */
    div.stButton > button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0px 0px 20px #ff0000 !important;
        background-color: #2a2e38 !important; /* Un peu plus clair au survol */
    }

    /* BOUTON RETOUR (plus petit et discret) */
    .btn-retour div.stButton > button {
        height: auto !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        width: auto !important;
        margin-bottom: 0px !important;
    }

    /* FIX EXPANDERS & TABS */
    .streamlit-expanderHeader { 
        background-color: #1e2129 !important; 
        border: 1px solid #ff0000 !important; 
        color: white !important;
    }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; }
    .stTabs [aria-selected="true"] { color: #ff0000 !important; font-weight: bold; }

    </style>
    """, unsafe_allow_html=True)

# Initialisation de la navigation dans le session_state
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
# PAGE D'ACCUEIL (MENU PAR CARTES CLIQUABLES)
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
        # 🎯 LA CARTE EST LE BOUTON 🎯
        # Le CSS transforme ce bouton en carte avec l'icône 📟
        if st.button("Information Chiffrée", key="c1-btn"):
            st.session_state.page = 'chap1'
            st.rerun()

    with col2:
        # 🎯 LA CARTE EST LE BOUTON 🎯
        # Le CSS transforme ce bouton en carte avec l'icône 📈
        if st.button("Suites Numériques", key="c2-btn"):
            st.session_state.page = 'chap2'
            st.rerun()

# =================================================================
# CHAPITRE 1 : INFORMATION CHIFFRÉE (AVEC COURS)
# =================================================================
elif st.session_state.page == 'chap1':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Menu principal", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.title("📟 Chapitre 1 : Information Chiffrée")
    
    tab1, tab2, tab3 = st.tabs(["🔢 Coeff. Multiplicateur", "📈 Taux d'évolution", "🔄 Évolutions Successives"])

    with tab1:
        st.markdown("### 🎯 Le multiplicateur magique")
        st.info(r"""
        **Concept :** Pour appliquer une évolution, on multiplie par le **CM**.  
        * **Hausse de t% :** $CM = 1 + \frac{t}{100}$  
        * **Baisse de t% :** $CM = 1 - \frac{t}{100}$
        """)
        t_in = st.number_input("Entrez le taux en % (ex: 20 ou -15)", value=20.0, step=0.1, key="c1t")
        res_cm = 1 + t_in / 100
        st.success(f"Le Coefficient Multiplicateur (CM) est de **{formater_fr(res_cm)}**")

    with tab2:
        st.markdown("### 📊 Calculer une variation")
        st.info(r"""
        **Concept :** Mesurer l'écart entre le départ ($V_D$) et l'arrivée ($V_A$).  
        * **Formule :** $t = \frac{V_A - V_D}{V_D}$  
        * Multiplier le résultat par 100 pour avoir le pourcentage.
        """)
        ca, cb = st.columns(2)
        v_d = ca.number_input("Valeur de Départ (VD)", value=100.0, key="c1vd")
        v_a = cb.number_input("Valeur d'Arrivée (VA)", value=125.0, key="c1va")
        if v_d != 0:
            taux_calc = ((v_a - v_d) / v_d) * 100
            st.success(f"Le taux d'évolution est de **{formater_fr(taux_calc)} %**")

    with tab3:
        st.markdown("### 🔄 Enchaîner les évolutions")
        st.warning("⚠️ Attention : On ne s'additionne JAMAIS les pourcentages, on multiplie les CM !")
        st.info(r"**Formule :** $CM_{global} = CM_1 \times CM_2 \times ...$")
        
        st.write("Simulateur : deux évolutions successives")
        col_ev1, col_ev2 = st.columns(2)
        ev1 = col_ev1.number_input("Taux 1 (%)", value=10.0, key="ev1")
        ev2 = col_ev2.number_input("Taux 2 (%)", value=-10.0, key="ev2")
        
        cm_global = (1 + ev1/100) * (1 + ev2/100)
        taux_global = (cm_global - 1) * 100
        st.success(f"Le CM global est **{formater_fr(cm_global, 4)}**, soit une évolution totale de **{formater_fr(taux_global)} %**")

    # DÉFI 1
    st.divider()
    if 'vd1' not in st.session_state:
        st.session_state.vd1 = random.randint(50, 200)
        st.session_state.tx1 = random.choice([5, 10, 15, 20, 25, 50])
        
    st.write(f"### ❓ Défi : Une hausse de {st.session_state.tx1}% sur un prix de {st.session_state.vd1}€")
    rep1 = st.number_input("Quel est le nouveau prix ?", value=0.0, key="r1")
    
    c_res1, c_res2 = st.columns(2)
    if c_res1.button("Vérifier"):
        corr = st.session_state.vd1 * (1 + st.session_state.tx1 / 100)
        if abs(rep1 - corr) < 0.1:
            st.balloons(); st.success(f"Bravo ! C'était bien {formater_fr(corr)} €")
        else:
            st.error(f"Faux ! Le calcul était {st.session_state.vd1} × {formater_fr(1+st.session_state.tx1/100)} = {formater_fr(corr)}")
    
    if c_res2.button("Nouveau défi 🔄", key="reset_c1"):
        del st.session_state.vd1
        st.rerun()

# =================================================================
# CHAPITRE 2 : SUITES NUMÉRIQUES (AVEC COURS)
# =================================================================
elif st.session_state.page == 'chap2':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Menu principal", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)

    st.title("📈 Chapitre 2 : Suites Numériques")
    
    t_gen, t_ari, t_geo = st.tabs(["📚 Généralités", "➕ Arithmétiques", "✖️ Géométriques"])

    # --- ONGLET GÉNÉRALITÉS ---
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

    # --- ONGLET ARITHMÉTIQUES (AVEC RAPPEL) ---
    with t_ari:
        st.markdown("### 🪜 La progression constante")
        st.info(r"""
        **Concept :** On passe d'un terme au suivant en **ajoutant** toujours le même nombre $r$ (la raison).  
        * **Récurrence :** $u_{n+1} = u_n + r$  
        * **Explicite :** $u_n = u_0 + n \times r$
        """)
        
        c1, c2 = st.columns([1, 2])
        with c1:
            st.write("**Paramètres :**")
            u0_a = st.number_input("Premier terme u0", value=10.0, key="u0a_input")
            r_a = st.number_input("Raison r", value=2.0, key="ra_input")
        with c2:
            st.write("**Visualisation :**")
            st.line_chart([u0_a + (i * r_a) for i in range(11)])

    # --- ONGLET GÉOMÉTRIQUES (AVEC RAPPEL) ---
    with t_geo:
        st.markdown("### 🚀 La progression explosive")
        st.info(r"""
        **Concept :** On passe d'un terme au suivant en **multipliant** toujours par le même nombre $q$ (la raison).  
        * **Récurrence :** $u_{n+1} = u_n \times q$  
        * **Explicite :** $u_n = u_0 \times q^n$
        """)
        
        c1, c2 = st.columns([1, 2])
        with c1:
            st.write("**Paramètres :**")
            u0_g = st.number_input("Premier terme u0", value=1000.0, key="u0g_input")
            q_g = st.number_input("Raison q", value=1.03, step=0.01, key="qg_input")
        with c2:
            st.write("**Visualisation :**")
            st.area_chart([u0_g * (q_g ** i) for i in range(11)])

    # --- DÉFI ---
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
            st.balloons(); st.success(f"Bravo ! C'était bien {formater_fr(corr_suite)}")
        else:
            st.error(f"Faux ! Le résultat était {formater_fr(corr_suite)}")

    if col_s2.button("Autre défi 🔄"):
        del st.session_state.suite_type
        st.rerun()
