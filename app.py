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
# CHAPITRE 0 : FONCTIONS (GÉNÉRALITÉS)
# =================================================================
if st.session_state.page == 'chap0':
    if st.button("⬅️ Retour au QG"):
        st.session_state.page = 'home'
        st.rerun()

    st.title("🌀 Fonctions : Généralités")
    st.write("---")

    tab1, tab2, tab3 = st.tabs([
        "🚪 Portail (Images/Antécédents)", 
        "🗺️ Territoire (Domaine)", 
        "📍 Lecture de Carte"
    ])

    # --- SOUS-CHAPITRE 1 : IMAGES ET ANTÉCÉDENTS ---
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
            *Un antécédent n'a qu'une seule image, mais une image peut avoir plusieurs antécédents !*
            """)

    # --- SOUS-CHAPITRE 2 : DOMAINE DE DÉFINITION ---
    with tab2:
        st.subheader("🚧 Le Territoire de la fonction")
        st.write("Certaines fonctions ont des 'zones interdites' (valeurs de x pour lesquelles le calcul est impossible).")
        c1, c2 = st.columns(2)
        with c1:
            st.error("🚫 **La Division par Zéro**")
            st.latex(r"g(x) = \frac{5}{x - 4}")
            st.write("Ici, $x$ ne peut pas être égal à **4** (le dénominateur serait nul).")
            st.write("**Domaine :** $\mathbb{R} \setminus \{4\}$")
        with c2:
            st.error("🚫 **La Racine Négative**")
            st.latex(r"h(x) = \sqrt{x + 2}")
            st.write("Sous une racine, le résultat doit être $\geq 0$.")
            st.write("**Domaine :** $[-2 \ ; \ +\infty[$")

    # --- SOUS-CHAPITRE 3 : LECTURE DE CARTE (VERSION ASYMÉTRIQUE FINALE) ---
    with tab3:
        st.subheader("📍 Cohérence Graphique : Du Squelette au Dessin")
        st.write("""
        Ici, pas de piège : la courbe rouge (le dessin) suit **strictement** le mouvement des flèches du tableau (le schéma). 
        Observe bien les valeurs de $x$ où la courbe change de direction.
        """)


        # 1. CRÉATION D'UNE FONCTION ASYMÉTRIQUE
        # On définit les points de rupture (x) pour le tableau
        x_min_local = -3  # Le creux
        x_max_local = 1   # La bosse
        limite = 6
        x_p = np.linspace(-limite, limite, 400)
        # Fonction f(x) asymétrique : f(x) = 0.1 * (x+4)(x-1)(x-5) - ajustée
        # Pour garantir la forme : Descend -> Monte -> Descend
        y_p = -0.05 * (x_p + 5) * (x_p + 1) * (x_p - 4) 

        # 2. CRÉATION DE LA FIGURE
        fig, (ax_graph, ax_tab) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})
        fig.patch.set_facecolor('#0e1117')

        # --- PARTIE HAUTE : LE GRAPH (DESSIN PRÉCIS) ---
        ax_graph.set_facecolor('#161b22')
        ax_graph.plot(x_p, y_p, color='#ff0000', lw=4)

        # Axes et Grille
        ax_graph.axhline(0, color='white', lw=1.5)
        ax_graph.axvline(0, color='white', lw=1.5)
        ax_graph.set_title("1. REPRÉSENTATION GRAPHIQUE", color='white', pad=15, fontweight='bold')
        ax_graph.tick_params(colors='white')
        ax_graph.set_xlim(-limite, limite)
        ax_graph.grid(color='#333333', linestyle='--')

        # --- PARTIE BASSE : LE TABLEAU (SQUELETTE ASYMÉTRIQUE) ---
        ax_tab.set_facecolor('#161b22')
        ax_tab.set_title("2. TABLEAU DE VARIATIONS", color='white', pad=10, fontweight='bold')

        # Structure du tableau (Lignes blanches)
        ax_tab.axhline(0.8, color='white', lw=1)
        ax_tab.axvline(-5.8, color='white', lw=1) # Bord gauche
        ax_tab.axvline(-3.2, color='white', lw=1) # Min à x ≈ -3.2
        ax_tab.axvline(1.8, color='white', lw=1)  # Max à x ≈ 1.8
        ax_tab.axvline(5.8, color='white', lw=1)  # Bord droit

        # Valeurs de x (alignées avec les sommets de la courbe)
        ax_tab.text(-5.8, 0.9, "-6", color='white', ha='center')
        ax_tab.text(-3.2, 0.9, "-3.2", color='white', ha='center')
        ax_tab.text(1.8, 0.9, "1.8", color='white', ha='center')
        ax_tab.text(5.8, 0.9, "6", color='white', ha='center')
        
        # Flèches (Même rouge que la courbe)
        # 1. Descente de -6 à -3.2
        ax_tab.annotate('', xy=(-3.4, 0.2), xytext=(-5.6, 0.7), arrowprops=dict(arrowstyle='->', color='#ff0000', lw=2))
        # 2. Montée de -3.2 à 1.8
        ax_tab.annotate('', xy=(1.6, 0.7), xytext=(-3.0, 0.2), arrowprops=dict(arrowstyle='->', color='#ff0000', lw=2))
        # 3. Descente de 1.8 à 6
        ax_tab.annotate('', xy=(5.6, 0.2), xytext=(2.0, 0.7), arrowprops=dict(arrowstyle='->', color='#ff0000', lw=2))
        
        # Valeurs f(x) qualitatives
        ax_tab.text(-3.2, 0.1, "Min", color='white', ha='center', fontsize=10)
        ax_tab.text(1.8, 0.75, "Max", color='white', ha='center', fontsize=10)
        ax_tab.axis('off')

        st.pyplot(fig)
        st.success("✅ Cette fois c'est la bonne : l'asymétrie est respectée et la courbe suit strictement le tableau !")

# =================================================================
# CHAPITRE 1 : INFORMATION CHIFFRÉE
# =================================================================
elif st.session_state.page == 'chap1':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Retour au QG", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.title("📟 Information Chiffrée")
    
    tab1, tab2, tab3 = st.tabs([
        "🔢 Coeff. Multiplicateur", 
        "📈 Taux d'évolution", 
        "🔄 Évolutions Successives"
    ])

    with tab1:
        st.subheader("🎯 Le Multiplicateur Magique")
        st.info("""
        **Concept :** Pour passer d'une valeur à une autre après une hausse ou une baisse, on utilise le **Coefficient Multiplicateur (CM)**.
        - **Hausse de t% :** $CM = 1 + \\frac{t}{100}$
        - **Baisse de t% :** $CM = 1 - \\frac{t}{100}$
        """)
        
        col_input, col_res = st.columns(2)
        with col_input:
            t_in = st.number_input("Entrez le taux en % (ex: 20 ou -15)", value=20.0, step=0.1, key="input_c1_t1")
        with col_res:
            res_cm = 1 + t_in / 100
            st.metric("Résultat du CM", formater_fr(res_cm))
            
        st.write("👉 *Exemple : Une hausse de 20% revient à multiplier par 1,20.*")

    with tab2:
        st.subheader("📊 Calculer une Variation")
        st.warning("""
        **Formule :** Pour trouver le taux d'évolution ($t$) entre une valeur de départ ($V_D$) et une valeur d'arrivée ($V_A$) :
        $$t = \\frac{V_A - V_D}{V_D}$$
        *(Multiplier par 100 pour obtenir le pourcentage)*
        """)
        
        c1, c2 = st.columns(2)
        v_d = c1.number_input("Valeur de Départ ($V_D$)", value=100.0, key="input_c1_vd")
        v_a = c2.number_input("Valeur d'Arrivée ($V_A$)", value=125.0, key="input_c1_va")
        
        if v_d != 0:
            taux_calc = ((v_a - v_d) / v_d) * 100
            st.success(f"Le taux d'évolution est de **{formater_fr(taux_calc)} %**")

    with tab3:
        st.subheader("🔄 Évolutions Successives")
        st.error("⚠️ **Attention :** On n'additionne JAMAIS les pourcentages entre eux !")
        st.info("""
        **Règle :** Pour trouver l'évolution globale, on multiplie les coefficients multiplicateurs entre eux.
        $$CM_{Global} = CM_1 \\times CM_2$$
        """)
        
        col_ev1, col_ev2 = st.columns(2)
        with col_ev1:
            ev1 = st.number_input("Hausse/Baisse 1 (%)", value=10.0, key="input_c1_ev1")
            cm1 = 1 + ev1/100
            st.caption(f"CM1 = {formater_fr(cm1)}")
        with col_ev2:
            ev2 = st.number_input("Hausse/Baisse 2 (%)", value=-10.0, key="input_c1_ev2")
            cm2 = 1 + ev2/100
            st.caption(f"CM2 = {formater_fr(cm2)}")
        
        cm_g = cm1 * cm2
        taux_g = (cm_g - 1) * 100
        
        st.divider()
        st.metric("Taux d'évolution global", f"{formater_fr(taux_g)} %")
        st.write(f"Calcul : ${formater_fr(cm1)} \\times {formater_fr(cm2)} = {formater_fr(cm_g)}$")

    # --- PETIT DÉFI POUR FINIR ---
    st.divider()
    if 'vd_quiz' not in st.session_state:
        st.session_state.vd_quiz = random.randint(50, 200)
        st.session_state.tx_quiz = random.choice([5, 10, 20, 25, 50])

    st.write(f"### ❓ Mission Flash :")
    st.write(f"Un objet coûte **{st.session_state.vd_quiz} €**. Son prix augmente de **{st.session_state.tx_quiz} %**.")
    rep_eleve = st.number_input("Quel est le nouveau prix ?", value=0.0, key="input_c1_quiz")
    
    if st.button("Vérifier la réponse"):
        correction = st.session_state.vd_quiz * (1 + st.session_state.tx_quiz / 100)
        if abs(rep_eleve - correction) < 0.1:
            st.balloons()
            st.success(f"Bravo ! C'est exactement {formater_fr(correction)} €.")
        else:
            st.error(f"Pas tout à fait. Le calcul était : {st.session_state.vd_quiz} × {formater_fr(1+st.session_state.tx_quiz/100)}.")

# =================================================================
# CHAPITRE 2 : SUITES NUMÉRIQUES
# =================================================================
elif st.session_state.page == 'chap2':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Retour au QG", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)

    st.title("📈 Chapitre 2 : Suites Numériques")
    
    t_gen, t_ari, t_geo = st.tabs(["📚 Généralités", "➕ Arithmétiques", "✖️ Géométriques"])

    # --- ONGLET 1 : GÉNÉRALITÉS ---
    with t_gen:
        st.subheader("📚 Guide de survie : Les Bases")
        
        with st.expander("🤔 Forme Explicite vs Récurrence"):
            st.write("#### 1️⃣ Forme Explicite (Le calcul direct)")
            st.write("On calcule n'importe quel terme directement avec **n**.")
            st.latex(r"u_n = f(n)")
            st.info("👉 *Exemple :* $u_n = 3n + 2$. Pour $u_{100}$, on fait $3 \times 100 + 2$. Rapide !")
            
            st.divider()
            
            st.write("#### 2️⃣ Forme Récurrence (L'escalier)")
            st.write("On a besoin du terme d'avant pour calculer le suivant. Il y a **toujours 2 lignes**.")
            st.latex(r"\begin{cases} u_0 = 5 \\ u_{n+1} = u_n + 3 \end{cases}")
            st.warning("⚠️ *Ici, pour avoir $u_{10}$, il faut d'abord calculer $u_1, u_2, u_3...$ jusqu'à 9. C'est long !*")

        with st.expander("📉 La Monotonie (Sens de variation)"):
            st.write("Pour savoir si une suite monte ou descend, on calcule :")
            st.latex(r"u_{n+1} - u_n")
            st.success("✅ Résultat > 0 : La suite est **Croissante**.")
            st.error("❌ Résultat < 0 : La suite est **Décroissante**.")

    # --- ONGLET 2 : ARITHMÉTIQUES ---
    with t_ari:
        st.subheader("🪜 Suites Arithmétiques (Addition)")
        st.info("""
        **Règle :** On passe d'un terme au suivant en **ajoutant** toujours le même nombre $r$ (la raison).
        - **Récurrence :** $u_{n+1} = u_n + r$
        - **Explicite :** $u_n = u_0 + n \times r$
        """)
        
        col_p, col_g = st.columns([1, 2])
        with col_p:
            u0_a = st.number_input("Premier terme $u_0$", value=10.0, key="ari_u0")
            r_a = st.number_input("Raison $r$", value=2.0, key="ari_r")
        
        with col_g:
            data_ari = [u0_a + (i * r_a) for i in range(11)]
            st.line_chart(data_ari)
            st.caption("Évolution des 10 premiers termes (Progression linéaire)")

    # --- ONGLET 3 : GÉOMÉTRIQUES ---
    with t_geo:
        st.subheader("🚀 Suites Géométriques (Multiplication)")
        st.warning("""
        **Règle :** On passe d'un terme au suivant en **multipliant** toujours par le même nombre $q$ (la raison).
        - **Récurrence :** $u_{n+1} = u_n \times q$
        - **Explicite :** $u_n = u_0 \times q^n$
        """)
        
        col_p2, col_g2 = st.columns([1, 2])
        with col_p2:
            u0_g = st.number_input("Premier terme $u_0$", value=1.0, key="geo_u0")
            q_g = st.number_input("Raison $q$", value=2.0, step=0.1, key="geo_q")
        
        with col_g2:
            data_geo = [u0_g * (q_g ** i) for i in range(11)]
            st.area_chart(data_geo)
            st.caption("Évolution des 10 premiers termes (Progression exponentielle)")

    # --- DÉFI DES SUITES ---
    st.divider()
    if 'suite_type' not in st.session_state:
        st.session_state.suite_type = random.choice(["Arithmétique", "Géométrique"])
        st.session_state.s_u0 = random.randint(2, 10)
        st.session_state.s_r = random.randint(2, 5)
        st.session_state.s_n = random.randint(2, 4)

    st.write(f"### ❓ Défi Mission :")
    if st.session_state.suite_type == "Arithmétique":
        st.write(f"Soit une suite **Arithmétique** de premier terme $u_0 = {st.session_state.s_u0}$ et de raison $r = {st.session_state.s_r}$.")
        sol_suite = st.session_state.s_u0 + (st.session_state.s_n * st.session_state.s_r)
    else:
        st.write(f"Soit une suite **Géométrique** de premier terme $u_0 = {st.session_state.s_u0}$ et de raison $q = {st.session_state.s_r}$.")
        sol_suite = st.session_state.s_u0 * (st.session_state.s_r ** st.session_state.s_n)

    rep_suite = st.number_input(f"Calculez la valeur de $u_{st.session_state.s_n}$ :", value=0.0, key="quiz_suite")
    
    if st.button("Vérifier le résultat", key="btn_quiz_suite"):
        if abs(rep_suite - sol_suite) < 0.1:
            st.balloons()
            st.success(f"Félicitations ! $u_{st.session_state.s_n}$ vaut bien {formater_fr(sol_suite)}.")
        else:
            st.error(f"Oups ! Revois ta formule. Le résultat attendu était {formater_fr(sol_suite)}.")

# =================================================================
# CHAPITRE 3 : POLYNÔMES DU 2ND DEGRÉ
# =================================================================
elif st.session_state.page == 'chap3':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Retour au QG", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)

    st.title("🛸 Chapitre 3 : Second Degré")
    
    t_cours, t_galerie, t_calc = st.tabs(["📚 Les 3 Formes (Cours)", "🖼️ Galerie de Paraboles", "📈 Simulateur"])

    # --- ONGLET 1 : LES FORMES (COURS) ---
    with t_cours:
        st.subheader("🧬 Les 3 visages d'une même fonction")
        st.write("Exemple unique pour tout le cours : $f(x) = 2x^2 + 4x - 6$")

        with st.expander("1. Forme Développée : $f(x) = ax^2 + bx + c$"):
            st.info("**Interprétation :** Le nombre **c = -6** est l'ordonnée à l'origine (coupe l'axe vertical).")
            st.latex(r"f(0) = c = -6")
            
        with st.expander("2. Forme Canonique : $f(x) = a(x - \\alpha)^2 + \\beta$"):
            st.success(r"""
            **🎯 Le Sommet $S(\alpha ; \beta)$ :**
            - $\alpha = \frac{-b}{2a} = \frac{-4}{2 \times 2} = \mathbf{-1}$
            - $\beta = f(\alpha) = 2(-1)^2 + 4(-1) - 6 = \mathbf{-8}$
            """)
            st.write("👉 *Le sommet de cette parabole est le point $S(-1 ; -8)$.*")
            

        with st.expander("3. Forme Factorisée : $f(x) = a(x - x_1)(x - x_2)$"):
            st.warning("**Interprétation :** $x_1$ et $x_2$ sont les **racines** (là où la courbe coupe l'axe horizontal).")
            st.latex(r"f(x) = 2(x - 1)(x + 3) \rightarrow x_1 = 1, x_2 = -3")

# --- ONGLET 2 : GALERIE (STYLE UNIFIÉ CH0) ---
    with t_galerie:

        st.write("### 🖼️ Analyse Graphique : $f(x) = 2x^2 + 4x - 6$")
        
        # 1. PRÉPARATION DES DONNÉES
        limite_x = 6
        limite_y = 10
        x_p = np.linspace(-limite_x, limite_x, 400)
        y_p = 2*x_p**2 + 4*x_p - 6

        # 2. CRÉATION DE LA FIGURE
        fig, ax = plt.subplots(figsize=(10, 7))
        fig.patch.set_facecolor('#0e1117') # Fond sombre App
        ax.set_facecolor('#161b22')        # Fond graphique

        # Grille et Axes (Style blanc discret)
        ax.grid(color='#333333', linestyle='--', lw=0.5)
        ax.axhline(0, color='white', lw=1.5)
        ax.axvline(0, color='white', lw=1.5)

        # La Courbe ROUGE NÉON
        ax.plot(x_p, y_p, color='#ff0000', lw=4, label='f(x) = 2x² + 4x - 6')

        # Points Singuliers en CYAN
        # Sommet S(-1, -8) | Racines (1,0) et (-3,0) | Ordonnée origine (0,-6)
        pts_x = [-1, 1, -3, 0]
        pts_y = [-8, 0, 0, -6]
        labels = ['S(-1;-8)', 'x1=1', 'x2=-3', 'c=-6']

        ax.scatter(pts_x, pts_y, color='#00d4ff', s=100, zorder=5, edgecolors='white')
        
        # Annotations Cyan
        for i, txt in enumerate(labels):
            ax.annotate(txt, (pts_x[i], pts_y[i]), xytext=(10, 10), 
                        textcoords='offset points', color='#00d4ff', fontweight='bold')

        # Graduations
        ax.set_xlim(-limite_x, limite_x)
        ax.set_ylim(-limite_y, limite_y)
        ax.tick_params(colors='white')
        
        st.pyplot(fig)
        st.success("✅ **Lecture :** La courbe coupe l'axe horizontal aux racines (Cyan) et atteint son minimum au sommet S.")

    # --- ONGLET 3 : SIMULATEUR (STYLE INTERACTIF) ---
    with t_calc:
        st.write("### 🕹️ Le Labo des Paraboles")
        
        col_p, col_v = st.columns([1, 2])
        
        with col_p:
            st.write("**Paramètres (Forme Canonique) :**")
            sa = st.slider("Coefficient a (Ouverture)", -4.0, 4.0, 1.0, step=0.5)
            s_alpha = st.number_input("Alpha (Position x)", value=0.0)
            s_beta = st.number_input("Beta (Hauteur y)", value=0.0)
        
        with col_v:
            # Création du graphique dynamique
            x_sim = np.linspace(s_alpha - 10, s_alpha + 10, 400)
            y_sim = sa * (x_sim - s_alpha)**2 + s_beta
            
            fig2, ax2 = plt.subplots()
            fig2.patch.set_facecolor('#0e1117')
            ax2.set_facecolor('#161b22')
            
            # Axes et Grille
            ax2.grid(color='#333333', linestyle='--', lw=0.5)
            ax2.axhline(0, color='white', lw=1)
            ax2.axvline(0, color='white', lw=1)
            
            # Courbe dynamique
            couleur_courbe = '#ff0000' if sa != 0 else '#ffffff'
            ax2.plot(x_sim, y_sim, color=couleur_courbe, lw=3)
            
            # Point du sommet (Cyan)
            ax2.scatter([s_alpha], [s_beta], color='#00d4ff', s=100, zorder=5)
            
            # Fixer les limites pour que le mouvement soit visible
            ax2.set_xlim(s_alpha - 10, s_alpha + 10)
            ax2.set_ylim(s_beta - 10, s_beta + 10)
            ax2.tick_params(colors='white')
            
            st.pyplot(fig2)

        # Analyse dynamique sous le graphique
        if sa > 0:
            st.info(f"🔼 **a > 0** : Parabole 'souriante'. Minimum en $y = {s_beta}$")
        elif sa < 0:
            st.error(f"🔽 **a < 0** : Parabole 'triste'. Maximum en $y = {s_beta}$")
        else:
            st.warning("📏 **a = 0** : C'est une droite horizontale !")

    # --- DÉFI ---
    st.divider()
    st.write("### ❓ Défi Sommet")
    if 'q3_val' not in st.session_state:
        st.session_state.q3_val = random.randint(-5, 5)

    st.write(f"Dans la forme $f(x) = 3(x - 2)^2 + ({st.session_state.q3_val})$, quelle est l'ordonnée du sommet ($\\beta$) ?")
    ans3 = st.number_input("Votre réponse :", value=0, key="quiz_c3")
    
    if st.button("Vérifier"):
        if ans3 == st.session_state.q3_val:
            st.balloons(); st.success("Bravo ! C'est le nombre seul à la fin de la forme canonique.")
        else:
            st.error(f"Faux. La réponse était {st.session_state.q3_val}.")

# =================================================================
# CHAPITRE 4 : PROBABILITÉS
# =================================================================
elif st.session_state.page == 'chap4':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Retour au QG", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)

    st.title("🎲 Chapitre 4 : Probabilités")

    tab_cours, tab_tab, tab_arbre = st.tabs(["📚 Rappels de Cours", "📊 Tableau Croisé", "🌳 Arbre de Choix"])

    # --- 1. RAPPELS DE COURS ---
    with tab_cours:
        st.subheader("🧠 Fondamentaux des Probabilités")
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.info("""
            **🔹 Probabilité simple ou marginale :**
            $$P(A) = \\frac{\\text{Nombre de cas favorables}}{\\text{Nombre total de cas}}$$
            """)
            st.write("Exemple : Tirer un As dans un jeu de 32 cartes $\\rightarrow 4/32 = 0,125$ (ou 12,5%).")
        
        with col_c2:
            st.warning("""
            **🔹 Événement contraire :**
            L'événement $\\bar{A}$ (non A) est :
            $$P(\\bar{A}) = 1 - P(A)$$
            """)
            st.write("Si $P(A)=0,3$ ou 30%, alors $P(\\bar{A})=0,7$ ou 70%.")

        st.write("")
        st.write("🤔 La probabilité te dit ce qui devrait arriver en théorie (dans le futur), et la fréquence te dit ce qui est arrivé (dans le passé) sur un échantillon donné. Mais les formules pour les calculer sont les mêmes !")
        
        st.divider()
        st.subheader("📡 Probabilités Conditionnelles")
        st.error("""
        **La formule clé :** La probabilité de B sachant que A est réalisé :
        $$P_A(B) = \\frac{P(A \\cap B)}{P(A)}$$
        *Note : $P(A \\cap B)$ représente 'A et B en même temps'.*
        """)

# --- 2. TABLEAU CROISÉ ---
    with tab_tab:
        st.subheader("📊 Analyse de données (Tableau à double entrée)")
        
        st.write("""
        👉 **Méthode :** Ce tableau est un exemple complet. Dans un exercice, certaines cases seront **vides**. 
        Vous devrez les retrouver en sachant que la somme des cases d'une ligne (ou d'une colonne) est égale à son **Total**.
        """)
        
        # Données
        data = {
            "Garçons": [12, 8, 20],
            "Filles": [15, 5, 20],
            "Total": [27, 13, 40]
        }
        df_prob = pd.DataFrame(data, index=["Sportifs", "Non Sportifs", "Total"])
        
        # Affichage avec CSS pour centrer tout le contenu du tableau
        st.markdown("""
        <style>
            .centered-table div[data-testid="stTable"] table {
                margin-left: auto;
                margin-right: auto;
            }
            .centered-table td, .centered-table th {
                text-align: center !important;
            }
        </style>
        <div class="centered-table">
        """, unsafe_allow_html=True)
        st.table(df_prob)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.divider()

        st.write("#### ❓ Question d'entraînement")
        st.write("D'après le tableau ci-dessus, quelle est la **fréquence** (en %) de **filles sportives** parmi le total des élèves ?")
        st.caption("💡 Rappel : Fréquence % = (Valeur de la case / Total général) × 100")

        # Entrée de l'élève
        ans_pct = st.number_input("Réponse en % (arrondir à 1 chiffre après la virgule) :", value=0.0, step=0.1)
        
        if st.button("Vérifier le pourcentage"):
            # Calcul réel : (15 / 40) * 100 = 37.5
            bonne_reponse = 37.5
            
            # On utilise abs(reponse - bonne_reponse) < 0.1 pour accepter les petits écarts d'arrondi
            if abs(ans_pct - bonne_reponse) < 0.1:
                st.balloons()
                st.success(f"Bravo ! Le calcul est : (15 / 40) × 100 = **{bonne_reponse}%**")
            else:
                st.error(f"Pas tout à fait. Cherchez la case 'Filles' + 'Sportifs' (15) et divisez par le Total (40).")

    # --- 3. ARBRE DE CHOIX (STYLE GRAPHIQUE NOIR/CYAN/ROUGE) ---
    with tab_arbre:
        st.subheader("🌳 Arbre de Probabilités")
        st.write("Visualisation des chemins possibles :")


        # Configuration du graphique identique au Ch0/Ch3
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#161b22')

        # Construction de l'arbre
        # Coordonnées des nœuds
        nodes = {
            'Départ': (0, 0),
            'A': (1, 1),
            'nonA': (1, -1),
            'B_sachant_A': (2, 1.5),
            'nonB_sachant_A': (2, 0.5),
            'B_sachant_nonA': (2, -0.5),
            'nonB_sachant_nonA': (2, -1.5)
        }

        # Dessiner les branches (Lignes Rouges)
        def draw_branch(p1, p2, label):
            ax.plot([nodes[p1][0], nodes[p2][0]], [nodes[p1][1], nodes[p2][1]], 
                    color='#ff0000', lw=3, zorder=1)
            # Label de probabilité au milieu de la branche
            mid_x = (nodes[p1][0] + nodes[p2][0]) / 2
            mid_y = (nodes[p1][1] + nodes[p2][1]) / 2
            ax.text(mid_x, mid_y + 0.1, label, color='white', fontweight='bold', ha='center')

        draw_branch('Départ', 'A', 'P(A)')
        draw_branch('Départ', 'nonA', 'P(nonA)')
        draw_branch('A', 'B_sachant_A', 'P_A(B)')
        draw_branch('A', 'nonB_sachant_A', 'P_A(nonB)')
        draw_branch('nonA', 'B_sachant_nonA', 'P_nonA(B)')
        draw_branch('nonA', 'nonB_sachant_nonA', 'P_nonA(nonB)')

        # Dessiner les nœuds (Points Cyan)
        for name, pos in nodes.items():
            ax.scatter(pos[0], pos[1], color='#00d4ff', s=200, zorder=2, edgecolors='white')
            ax.text(pos[0], pos[1]-0.3, name, color='#00d4ff', fontsize=10, ha='center', fontweight='bold')

        # Nettoyage du graphique
        ax.set_xlim(-0.5, 2.5)
        ax.set_ylim(-2, 2)
        ax.axis('off') # On cache les axes pour l'arbre

        st.pyplot(fig)

        st.info("""
        **📏 Règle d'or de l'arbre :**
        1. La somme des branches partant d'un même nœud vaut toujours **1**.
        2. Pour calculer la probabilité d'un chemin complet, on **multiplie** les probabilités.
        3. La somme des fleurs de l'arbre (les probabilités à droite) fait 1 ou 100%.
        """)

