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

# --- 2. STYLE CSS VERSION GRILLE FORCÉE ---
st.markdown("""
    <style>
    /* FOND GÉNÉRAL */
    .stApp { background-color: #0e1117; }
    
    /* TEXTE BLANC GÉNÉRAL */
    .stMarkdown, p, span, label, li { color: #ffffff !important; }

    /* TITRES ROUGES NÉON */
    h1, h2, h3 { 
        color: #ff0000 !important; 
        text-shadow: 2px 2px 10px #ff0000; 
        text-align: center;
    }

    /* 🎯 --- LA GRILLE MAGIQUE --- 🎯 */
    /* On force le conteneur des colonnes à devenir une grille stricte */
    [data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: 1fr 1fr !important; /* Deux colonnes strictement égales */
        gap: 15px !important;
    }

    /* On annule les comportements par défaut des colonnes Streamlit qui cassent tout */
    [data-testid="column"] {
        width: 100% !important;
        max-width: 100% !important;
        flex: none !important;
    }

    /* 🎯 LE BOUTON (CARTE) */
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

    /* ⚪ FORCE LE TEXTE EN BLANC PUR */
    button[kind="secondary"] div[data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-size: 1.25rem !important;
        font-weight: bold !important;
        text-align: center !important;
    }

    /* 🔴 SURVOL */
    button[kind="secondary"]:hover {
        transform: scale(1.02) !important;
        background-color: #1e2129 !important;
        box-shadow: 0px 0px 25px #ff0000 !important;
    }
    
    button[kind="secondary"]:hover div[data-testid="stMarkdownContainer"] p {
        color: #ff0000 !important;
        -webkit-text-fill-color: #ff0000 !important;
    }

    /* BOUTON RETOUR (On désactive la grille pour lui) */
    .btn-retour {
        display: block !important;
        width: fit-content !important;
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
    # Logo
    try:
        img = Image.open(chemin_logo)
        st.image(img, use_container_width=True)
    except:
        st.title("🔦 STRANGER MATHS")

    st.write("### 🎮 Choisissez votre mission :")
    st.write("")

    # ON MET TOUT DANS UNE SEULE LIGNE DE 2 COLONNES
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("🌀 Fonctions :\nGénéralités", key="btn_c0")
        st.button("📈 Suites\nNumériques", key="btn_c2")
        st.button("📊 Stats :\nProbabilités", key="btn_c4")

    with col2:
        st.button("📟 Information\nChiffrée", key="btn_c1")
        st.button("🛸 Second\nDegré", key="btn_c3")
    
    # Clics
    if st.session_state.btn_c0: st.session_state.page = 'chap0'; st.rerun()
    if st.session_state.btn_c1: st.session_state.page = 'chap1'; st.rerun()
    if st.session_state.btn_c2: st.session_state.page = 'chap2'; st.rerun()
    if st.session_state.btn_c3: st.session_state.page = 'chap3'; st.rerun()
    if st.session_state.btn_c4: st.session_state.page = 'chap4'; st.rerun()

# =================================================================
# LES CHAPITRES (0, 1, 2, 3)
# =================================================================

# --- CHAPITRE 0 ---
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

        import matplotlib.pyplot as plt
        import numpy as np
        
        # 1. CRÉATION D'UNE FONCTION ASYMÉTRIQUE
        # On définit les points de rupture (x) pour le tableau
        x_min_local = -3  # Le creux
        x_max_local = 1   # La bosse
        
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
        ax_tab.axvline(1.8, color='white', lw=1)  # Max à x ≈ 1.8
        ax_tab.axvline(5.8, color='white', lw=1)  # Bord droit
        
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
        
# --- CHAPITRE 1 ---
elif st.session_state.page == 'chap1':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Menu", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("📟 Information Chiffrée")
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


# --- CHAPITRE 2 ---
elif st.session_state.page == 'chap2':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Menu", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("📈 Suites Numériques")
    t_gen, t_ari, t_geo = st.tabs(["📚 Généralités", "➕ Arithmétiques", "✖️ Géométriques"])

    # --- ONGLET GÉNÉRALITÉS ---
    with t_gen:
        st.subheader("📚 Guide de survie : Généralités")
        with st.expander("🤔 Comment différencier Explicite et Récurrence ?"):
            st.write("**Tuyau de Dustin :** Regarde bien la structure de l'énoncé.")
            
            st.write("#### 1️⃣ Forme Explicite (Le raccourci)")
            st.write("Il n'y a **qu'une seule ligne**. On calcule n'importe quel terme directement avec **n**.")
            st.latex(r"u_n = 5n - 2")
            st.write("👉 *Exemple : Pour $u_{10}$, on remplace juste n par 10.*")
            
            st.divider()
            
            st.write("#### 2️⃣ Forme Récurrence (L'escalier)")
            st.warning("⚠️ **Attention :** Une suite par récurrence comporte **TOUJOURS 2 lignes** !")
            st.write("Il faut la valeur de départ ET la règle pour monter à la marche suivante.")
            st.latex(r"\begin{cases} u_0 = 3 & \text{(Le premier terme)} \\ u_{n+1} = u_n + 10 & \text{(La relation de récurrence)} \end{cases}")
            st.write("👉 *Ici, on ne peut pas calculer $u_{10}$ sans avoir calculé tous les termes avant.*")

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


# --- CHAPITRE 3 ---
elif st.session_state.page == 'chap3':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Menu", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("🛸 Second Degré")
    t_cours, t_galerie, t_calc = st.tabs(["📚 Les 3 Formes (Cours)", "🖼️ Galerie de Paraboles", "📈 Simulateur"])

 # --- ONGLET COURS (AVEC EXEMPLE UNIQUE) ---
    with t_cours:
        st.write("### 🧬 Les 3 visages d'une même fonction")
        st.write("Pour comprendre les formes, nous allons utiliser un exemple unique :")
        st.latex(r"f(x) = 2x^2 + 4x - 6 \quad \text{(Forme Développée)}")

        with st.expander("1. Forme Développée : f(x) = ax² + bx + c"):
            st.write("**Notre exemple :** $f(x) = 2x^2 + 4x - 6$")
            st.info("**Interprétation :** Le nombre **c = -6** est l'ordonnée à l'origine (là où la courbe coupe l'axe vertical).")
            st.latex(r"f(0) = -6")
            
        with st.expander("2. Forme Canonique : f(x) = a(x - α)² + β"):
            st.write("**Notre exemple :** $f(x) = 2(x + 1)^2 - 8$")
            
            st.success(r"""
            **🎯 Le Sommet $S(\alpha \ ; \ \beta)$ :**
            
            * **Calcul de $\alpha$ :** On utilise la formule $\alpha = \frac{-b}{2a}$
                * *Ici :* $\alpha = \frac{-4}{2 \times 2} = \mathbf{-1}$
            
            * **Calcul de $\beta$ :** C'est l'image de $\alpha$ par la fonction ($f(\alpha)$)
                * *Ici :* $\beta = f(-1) = 2(-1)^2 + 4(-1) - 6 = \mathbf{-8}$
            
            **💡 Interprétation :**
            Le sommet de la parabole est le point **$S(-1 \ ; \ -8)$**.  
            Comme $a > 0$, la valeur **$\beta = -8$** est le **minimum** de la fonction.  
            Il est atteint pour **$x = -1$**.
            """)
            st.latex(r"S = (-1 \ ; \ -8)")
    
        with st.expander("3. Forme Factorisée : f(x) = a(x - x₁)(x - x₂)"):
            st.write("**Notre exemple :** $f(x) = 2(x - 1)(x + 3)$")
            st.warning(r"""
            **Interprétation :** Les nombres **$x_1 = 1$** et **$x_2 = -3$** sont les **racines**.  
            Ce sont les solutions de l'équation **$f(x) = 0$**.  
            Graphiquement, ce sont les points où la courbe coupe l'axe des abscisses (horizontal).
            """)
            st.latex(r"f(1) = 0 \quad \text{et} \quad f(-3) = 0")

    # --- ONGLET GALERIE (QUADRILLAGE MANUEL 1x1 & COULEURS SYNCHRO) ---
    with t_galerie:
        import pandas as pd
        import numpy as np
        import altair as alt

        st.write("### 🖼️ Représentation Graphique (Repère orthonormé)")
        
        # 1. PRÉSENTATION DES FORMES (Plus lisible)
        st.info(r"**Exemple :** $f(x) = 2x^2 + 4x - 6$ | Forme canonique : $2(x+1)^2-8$ | Forme factorisée : $2(x-1)(x+3)$")
        
        # 2. PRÉPARATION DES DONNÉES
        limite = 10
        grid_lines = []
        for i in range(-limite, limite + 1):
            grid_lines.append(pd.DataFrame({'x': [i, i], 'y': [-limite, limite], 'group': f'v{i}'}))
            grid_lines.append(pd.DataFrame({'x': [-limite, limite], 'y': [i, i], 'group': f'h{i}'}))
        df_grid = pd.concat(grid_lines)

        # Points singuliers en CYAN pour se détacher du rouge
        df_pts = pd.DataFrame([
            {'name': 'S (-1 ; -8)', 'x': -1, 'y': -8},
            {'name': 'R1 (1 ; 0)', 'x': 1, 'y': 0},
            {'name': 'R2 (-3 ; 0)', 'x': -3, 'y': 0},
            {'name': 'C (0 ; -6)', 'x': 0, 'y': -6}
        ])
        
        x_p = np.linspace(-limite, limite, 400)
        y_p = 2 * (x_p - 1) * (x_p + 3)
        df_c = pd.DataFrame({'x': x_p, 'y': y_p})

        # 3. CONSTRUCTION DU GRAPHIQUE COUCHE PAR COUCHE
        
        # COUCHE 1 : Grille manuelle discrète
        manual_grid = alt.Chart(df_grid).mark_line(color='#333333', size=1).encode(
            x=alt.X('x', scale=alt.Scale(domain=[-limite, limite]), title="Abscisses (x)"),
            y=alt.Y('y', scale=alt.Scale(domain=[-limite, limite]), title="Ordonnées (y)"),
            detail='group'
        )

        # COUCHE 2 : Axes JAUNES éclatants (comme dans le chapitre généralités)
        axe_h = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='#ffff00', size=3, opacity=0.8).encode(y='y')
        axe_v = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule(color='#ffff00', size=3, opacity=0.8).encode(x='x')

        # COUCHE 3 : La Courbe ROUGE (le sujet principal)
        curve = alt.Chart(df_c).mark_line(color='#ff0000', size=4).encode(
            x='x', y='y'
        ).transform_filter((alt.datum.y <= limite) & (alt.datum.y >= -limite))

        # COUCHE 4 : Points et textes CYAN (les indices)
        points = alt.Chart(df_pts).mark_point(size=220, filled=True, color='#00d4ff', stroke='white').encode(
            x='x', 
            y='y',
            tooltip=['name', 'x', 'y']
        )
        
        text = alt.Chart(df_pts).mark_text(
            align='left', 
            dx=12, 
            dy=-12, 
            fontSize=14, 
            fontWeight='bold', 
            color='#00d4ff'
        ).encode(x='x', y='y', text='name')

        # 4. ASSEMBLAGE ET CONFIGURATION
        final_chart = (manual_grid + axe_h + axe_v + curve + points + text).configure_axis(
            labelColor='white',
            titleColor='white',
            grid=False,
            domain=False,
            labelFontSize=11,
            values=list(range(-limite, limite + 1))
        ).properties(width=600, height=600)

        # Affichage centré
        _, col_c, _ = st.columns([1, 10, 1])
        with col_c:
            st.altair_chart(final_chart, use_container_width=False, theme=None)

# --- SECTION TABLEAUX GRAPHIQUES OPTIMISÉS ---
        st.divider()
        st.write("### 📋 Tableaux de variations et Tableau de signes de f : $f(x) = 2x^2 + 4x - 6$")

        import matplotlib.pyplot as plt

        # On crée une figure avec deux sous-graphiques (1 ligne, 2 colonnes)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        fig.patch.set_facecolor('#0e1117') # Fond sombre comme ton app

        # --- TABLEAU DE VARIATION ---
        ax1.set_facecolor('#161b22')
        ax1.set_title("📈 VARIATIONS", color='#ff0000', fontweight='bold', pad=20)
        # Dessin des flèches
        ax1.annotate('', xy=(0.5, 0.1), xytext=(0.1, 0.9), arrowprops=dict(arrowstyle='->', color='white', lw=2))
        ax1.annotate('', xy=(0.9, 0.9), xytext=(0.5, 0.1), arrowprops=dict(arrowstyle='->', color='white', lw=2))
        # Textes
        ax1.text(0.1, 1.05, "-∞", color='#00d4ff', ha='center')
        ax1.text(0.5, 1.05, "-1", color='#00d4ff', ha='center')
        ax1.text(0.9, 1.05, "+∞", color='#00d4ff', ha='center')
        ax1.text(0.5, -0.1, "-8", color='#ff0000', ha='center', fontsize=14, fontweight='bold')
        ax1.axis('off')

        # --- TABLEAU DE SIGNES ---
        ax2.set_facecolor('#161b22')
        ax2.set_title("✨ SIGNE DE f(x)", color='#00d4ff', fontweight='bold', pad=20)
        # Ligne horizontale
        ax2.axhline(0.7, color='white', lw=1)
        # Textes x
        ax2.text(0.1, 0.85, "-∞", color='white', ha='center')
        ax2.text(0.35, 0.85, "-3", color='white', ha='center')
        ax2.text(0.65, 0.85, "1", color='white', ha='center')
        ax2.text(0.9, 0.85, "+∞", color='white', ha='center')
        # Signes et zéros
        ax2.text(0.2, 0.4, "+", color='white', fontsize=18, ha='center')
        ax2.text(0.5, 0.4, "-", color='white', fontsize=18, ha='center')
        ax2.text(0.8, 0.4, "+", color='white', fontsize=18, ha='center')
        # Barres verticales pour les zéros
        ax2.axvline(0.35, ymin=0.2, ymax=0.7, color='white', lw=1)
        ax2.axvline(0.65, ymin=0.2, ymax=0.7, color='white', lw=1)
        ax2.text(0.35, 0.4, "0", color='#ff0000', fontweight='bold', ha='center', bbox=dict(facecolor='#161b22', edgecolor='none'))
        ax2.text(0.65, 0.4, "0", color='#ff0000', fontweight='bold', ha='center', bbox=dict(facecolor='#161b22', edgecolor='none'))
        ax2.axis('off')

        st.pyplot(fig)
        
        
        st.caption("💡 Le minimum -8 correspond au sommet, qui représente ici le minimum de la fonction. Les '0' correspondent aux intersections avec l'axe jaune (racines ou solutions de l'équation f(x)=0).")
        st.caption("💡 Ici a=2 est positif ; si a avait été négatif, la courbe aurait été inversée et on aurait eu un maximum et non pas un minimum ; de la même façon, le tableau de variations et le tableau de signes auraient été inversés.")

        
    # --- ONGLET SIMULATEUR ---
    with t_calc:
        st.write("### 🕹️ Simulateur Interactif")
        c1, c2, c3 = st.columns(3)
        pa = c1.number_input("Coeff a (forme)", value=1.0, step=0.5)
        p_alpha = c2.number_input("Alpha (position x)", value=0.0)
        p_beta = c3.number_input("Beta (Max/Min y)", value=0.0)

        # Calcul de la courbe
        x_range = [x / 10 for x in range(int((p_alpha-10)*10), int((p_alpha+10)*10))]
        y_vals = [pa * (x - p_alpha)**2 + p_beta for x in x_range]
        st.line_chart(dict(zip(x_range, y_vals)))

        # Affichage dynamique du tableau de variation
        st.divider()
        if pa > 0:
            st.write(f"✅ **Sens de variation :** La fonction décroit puis croît. Le **minimum** est {p_beta} (atteint pour x = {p_alpha}).")
        else:
            st.write(f"❌ **Sens de variation :** La fonction croît puis décroit. Le **maximum** est {p_beta} (atteint pour x = {p_alpha}).")

    # --- DÉFI ---
    st.divider()
    st.write("### ❓ Défi Sommet")
    if 'q3_alpha' not in st.session_state:
        st.session_state.q3_alpha = random.randint(-5, 5)
        st.session_state.q3_beta = random.randint(-5, 5)

    st.write(f"Soit la fonction $f(x) = 2(x - ({st.session_state.q3_alpha}))^2 + ({st.session_state.q3_beta})$")
    ans_beta = st.number_input("Quelle est la valeur de l'extremum (Beta) ?", value=0)
    
    if st.button("Vérifier"):
        if ans_beta == st.session_state.q3_beta:
            st.balloons(); st.success(f"Bravo ! L'extremum est bien {st.session_state.q3_beta}.")
        else:
            st.error(f"Faux ! L'extremum (Beta) est le nombre tout seul à la fin : {st.session_state.q3_beta}")

    
# --- CHAPITRE 4 : STATISTIQUES ---
elif st.session_state.page == 'chap4':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Menu", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.title("📊 Statistiques & Arbres")
    
    tab1, tab2 = st.tabs(["📋 Tableau Croisé", "🌳 Arbre de Choix"])
    
    with tab1:
        st.subheader("Analyse des Fréquences")
        st.write("Imaginez qu'on étudie les habitants de Hawkins selon deux critères :")
        
        # Données fictives pour l'exemple
        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.markdown("""
            | | Possède des Pouvoirs | Pas de Pouvoirs | **Total** |
            |---|---|---|---|
            | **Enfant** | 2 | 18 | **20** |
            | **Adulte** | 1 | 29 | **30** |
            | **Total** | **3** | **47** | **50** |
            """)
        
        st.info("💡 **Marginale** = Regarder les totaux (bords). **Conditionnelle** = Zoomer sur une ligne ou colonne.")
        
        # Petit calculateur interactif
        val_case = st.number_input("Valeur de la case choisie :", value=2)
        val_total = st.number_input("Valeur du total référent (Ligne, Col ou Total) :", value=20)
        
        if val_total > 0:
            frequence = (val_case / val_total) * 100
            st.success(f"La fréquence est de : **{formater_fr(frequence)} %**")

        

    with tab2:
        st.subheader("L'Arbre de Choix")
        st.write("Pour dénombrer les issues d'une expérience (ex: choisir une tenue puis un vélo) :")
        
        st.markdown("""
        1. **Chaque embranchement** représente un choix ou un événement.
        2. **Multipliez** les probabilités le long d'un chemin pour avoir le résultat final.
        3. **Additionnez** les résultats si plusieurs chemins mènent à ce que vous cherchez.
        """)
        
        # Exemple visuel simple en texte (ou tu peux insérer un graphique matplotlib)
        st.code("""
        Départ ---- (VTT) ----> [Glace]  => Chemin 1
               |          |---> [Bonbon] => Chemin 2
               |
               ---- (Route) ---> [Glace]  => Chemin 3
                          |---> [Bonbon] => Chemin 4
        """)


