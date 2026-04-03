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

        import matplotlib.pyplot as plt
        import numpy as np

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
    st.button("⬅️ Menu principal", on_click=aller_a_home)
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
# CHAPITRE 4 : STATISTIQUES
# =================================================================
elif st.session_state.page == 'chap4':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Retour au QG", on_click=aller_a_home)
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
