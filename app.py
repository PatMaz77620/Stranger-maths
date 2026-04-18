import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import json

from openai import OpenAI

# Initialisation du client OpenAI (beaucoup plus simple)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


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
        /* On enlève width: 100% pour laisser les espaces pousser les bords */
        width: max-content !important; 
        min-width: 300px !important; /* Optionnel : définit une base minimale pour la sécurité */
        background-color: #161b22 !important;
        border: 2px solid #ff0000 !important;
        border-radius: 15px !important;
        transition: all 0.3s ease !important;
        height: 160px !important;
        box-shadow: 0px 4px 15px rgba(255, 0, 0, 0.2) !important;
        margin: auto !important; /* Centre le bouton dans sa colonne */
        display: block !important;
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

    /* Règle spéciale pour le QUIZ : on annule le style "Carte" uniquement ici */
    .stButtonGroup, [data-testid="stVerticalBlock"] .stButton button {
        height: auto !important; /* On laisse le bouton s'adapter au texte */
        min-width: 0px !important; /* On enlève la largeur forcée */
        padding: 10px !important; /* On remet un espacement normal */
    }

    /* Optionnel : si tu veux que les boutons du quiz soient moins épais que les cartes */
    div.stButton > button {
        margin-bottom: 5px !important;
    }
    

    
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

def generer_mission_openai(theme_maths, difficulte):  # Vous pouvez garder le nom ou le changer
    niveaux = {
        "Facile": "Niveau 1 : Applications directes du cours, calculs simples et évidents.",
        "Moyen": "Niveau 2 : Niveau standard STMG, mélanger lecture d'énoncés et calculs à 2 étapes.",
        "Difficile": "Niveau 3 : Questions type Bac, cas particuliers, et raisonnements plus poussés."
    }

    prompt = f"""Génère une LISTE de 11 questions de mathématiques (niveau 1ERE STMG) sur le thème : {theme_maths}.
    Difficulté : {difficulte} ({niveaux[difficulte]}).
     Format JSON strict : une liste d'objets [{{...}}, {{...}}] contenant :
    - 'question': texte de la question
    - 'options': liste de 4 choix
    - 'reponse': la réponse exacte parmi les options
    - 'explication': une courte explication pédagogique
    """

    try:
        # --- CHANGEMENT ICI POUR OPENAI ---
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "Tu es un expert en mathématiques pédagogiques pour le niveau STMG. Tu réponds uniquement en JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        # Extraction du contenu texte
        data = response.choices[0].message.content
        quiz_data = json.loads(data)

        # Sécurité : OpenAI peut parfois encapsuler la liste dans une clé "questions"
        if isinstance(quiz_data, dict) and "questions" in quiz_data:
            return quiz_data["questions"]
        elif isinstance(quiz_data, dict) and not isinstance(quiz_data, list):
            # Si c'est un dictionnaire mais pas une liste, on cherche la première liste dedans
            for val in quiz_data.values():
                if isinstance(val, list): return val

        return quiz_data
    except Exception as e:
        st.error(f"Erreur de connexion avec OpenAI : {e}")
        return None

def afficher_interface_quiz():
    # 1. Initialisation des variables de session si elles n'existent pas
    if 'index_question' not in st.session_state:
        st.session_state.index_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'repondu' not in st.session_state:
        st.session_state.repondu = False

    # CAS A : La mission est en cours
    if 'quiz_dynamique' in st.session_state and st.session_state.quiz_dynamique:
        questions = st.session_state.quiz_dynamique
        idx = st.session_state.index_question

        # A.1. Il reste des questions à poser
        if idx < len(questions):
            q = questions[idx]
            
            # Barre de progression visuelle
            progress = idx / len(questions)
            st.progress(progress)
            st.write(f"### 🛰️ Mission Eleven : Question {idx + 1} / {len(questions)}")
            
            st.markdown(f"**{q['question']}**")
            st.write("") # Petit espace

            # --- AFFICHAGE DES RÉPONSES (LISTE DE BOUTONS SIMPLE) ---
            if not st.session_state.repondu:
                # On affiche simplement les boutons les uns sous les autres
                for option in q['options']:
                    if st.button(option, key=f"opt_{idx}_{option}", use_container_width=True):
                        st.session_state.dernière_reponse = option
                        st.session_state.repondu = True
                        if option == q['reponse']:
                            st.session_state.score += 1
                        st.rerun()
            else:
                # Affichage après la sélection
                st.write(f"Ton choix : **{st.session_state.dernière_reponse}**")
                
                if st.session_state.dernière_reponse == q['reponse']:
                    st.success(f"✅ Bravo ! {q['explication']}")
                else:
                    st.error(f"❌ Erreur. La réponse était : {q['reponse']}")
                    st.info(f"💡 **Explication :** {q['explication']}")
                
                st.write("")
                if st.button("Question suivante ➡️", use_container_width=True):
                    st.session_state.index_question += 1
                    st.session_state.repondu = False
                    st.rerun()

        # A.2. Fin de la mission (Score final)
        else:
            st.balloons()
            st.title("🏆 Mission Accomplie !")
            
            # Récupération des infos
            score_final = st.session_state.score
            total_q = len(st.session_state.quiz_dynamique)
            diff = st.session_state.get('difficulte_active', 'Moyen')
            
            # Affichage du score
            st.metric(f"Score Final (Niveau {diff})", f"{score_final} / {total_q}")
            
            # --- LOGIQUE DES MESSAGES PERSONNALISÉS ---
            if score_final == total_q:
                st.success(f"🔥 **INCROYABLE !** Un sans-faute en mode **{diff}**. Tes pouvoirs dépassent ceux d'Eleven !")
            
            elif score_final >= 7:
                if diff == "Difficile":
                    st.success("💪 **Expert confirmé !** Tu as terrassé le Demogorgon au niveau maximum. Les maths n'ont plus de secrets pour toi.")
                else:
                    st.success(f"👏 **Bravo !** Tu maîtrises le niveau **{diff}**. Prêt pour le niveau supérieur ?")
            
            elif score_final >= 5:
                st.warning(f"🥉 **Moyenne atteinte.** Le niveau **{diff}** est en cours d'acquisition, mais attention aux pièges de l'Upside Down.")
            
            else:
                st.error(f"🛸 **Mission périlleuse...** Le niveau **{diff}** était peut-être un peu haut. Reprends tes forces et réessaie !")

            # --- BOUTON DE RELANCE ---
            if st.button("🔄 Lancer une nouvelle série", use_container_width=True):
                # Nettoyage complet pour la prochaine mission
                del st.session_state.quiz_dynamique
                st.session_state.index_question = 0
                st.session_state.score = 0
                st.session_state.repondu = False
                # On ne supprime pas difficulte_active pour qu'elle serve par défaut au prochain coup
                st.rerun()

    # CAS B : Écran de lancement
    else:
        themes = {
            "chap0": "Fonctions (Généralités)",
            "chap1": "Information chiffrée",
            "chap2": "Suites numériques",
            "chap3": "Polynômes du 2nd degré",
            "chap4": "Probabilités",
            "chap5": "Dérivation (Nombre dérivé, tangentes, variations)"
        }
        theme_actuel = themes.get(st.session_state.page, "Mathématiques")
        
        st.markdown("---")
        st.write(f"Prêt pour une série de **Eleven questions** sur le thème :")

        st.subheader(f"🌀 {theme_actuel}")

        # Choix de la difficulté
        difficulte_choisie = st.select_slider(
            "Sélectionnez le niveau de menace dans l'Upside Down :",
            options=["Facile", "Moyen", "Difficile"],
            value="Moyen"
        )

        
        if st.button("🔦 Lancer la Mission Eleven", use_container_width=True):
            with st.spinner(f"Eleven scanne l'Upside Down pour préparer tes 11 défis (Niveau {difficulte_choisie})..."):
                quiz = generer_mission_openai(theme_actuel, difficulte_choisie)
                if quiz:
                    st.session_state.quiz_dynamique = quiz
                    st.session_state.index_question = 0
                    st.session_state.score = 0
                    st.session_state.repondu = False
                    # On stocke la difficulté pour le message final
                    st.session_state.difficulte_active = difficulte_choisie
                    st.rerun()

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
            if st.button("📊 Stats :\nProbabilités\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0", key="btn_c4"):
                st.session_state.page = 'chap4'
                st.rerun()

        with col2:
            if st.button("📟 Information\nChiffrée\u00A0\u00A0\u00A0", key="btn_c1"):
                st.session_state.page = 'chap1'
                st.rerun()
            if st.button("🛸 Second\nDegré\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0", key="btn_c3"):
                st.session_state.page = 'chap3'
                st.rerun()
            # --- NOUVEAU BOUTON DÉRIVÉES ---
            if st.button("📉 Dérivation \u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0", key="btn_c5"):
                st.session_state.page = 'chap5'
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
        
        # --- SECTION PUB : LE PHARE ---
        st.write("---")
        st.markdown("""
            <div style="background-color: #161b22; border: 1px solid #00d4ff; border-radius: 10px; padding: 20px; text-align: center;">
                <h3 style="color: #00d4ff; margin-top: 0;">🔦 Besoin d'un guide ?</h3>
                <p style="color: white; font-size: 1.1rem;">
                    Besoin d'aide pour tes devoirs ou tes révisions ? <br>
                    Découvre <b>Le Phare</b>, l'association qui t'accompagne vers la réussite.
                </p>
                <a href="https://www.association-le-phare.com/" target="_blank" 
                   style="display: inline-block; background-color: #00d4ff; color: #0e1117; padding: 10px 20px; 
                   border-radius: 5px; text-decoration: none; font-weight: bold; transition: 0.3s;">
                   ⚓ Visiter le Phare
                </a>
            </div>
        """, unsafe_allow_html=True)

# =================================================================
# CHAPITRE 0 : FONCTIONS (GÉNÉRALITÉS)
# =================================================================
elif st.session_state.page == 'chap0':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Retour au QG", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)

    st.title("🌀 Fonctions : Généralités")
    st.write("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🚪 Portail (Images/Antécédents)", 
        "🗺️ Territoire (Domaine)", 
        "📍 Lecture de Carte", 
        "🕹️ Mission Eleven"
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

        # --- TON NOUVEAU BLOC PÉDAGOGIQUE ---
        st.write("---")
        st.success(r"""
        **💡 Pourquoi utilise-t-on des formules ?**
        
        La formule $f(x) = 2x^2 - 3$ permet d'écrire de façon ultra compacte ce que l'on dirait en français :  
        *"Prends n'importe quel nombre, multiplie-le par lui-même, multiplie le résultat par 2, et enlève 3 au résultat final."*
        
        **C'est beaucoup plus fastoche à noter sous forme de fonction, non ?** 🚀
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
        st.success("✅ la fonction représentée ci-dessus est la suivante : $$f(x) = 0,1(4 - x)(x + 1)(x + 5)$$. As-tu trouvé les racines de la fonction (les valeurs de $$x$$ qui annulent la fonction) ? Vérifie sur la représentation graphique les valeurs que tu as trouvées par le calcul... Peux-tu en déduire le tableau de signes facilement ?")

    
    # --- SOUS-CHAPITRE 4 : QUIZZ ---
    with tab4:
        # On appelle la fonction de quiz qu'on a créée plus haut
        afficher_interface_quiz()


# =================================================================
# CHAPITRE 1 : INFORMATION CHIFFRÉE
# =================================================================
elif st.session_state.page == 'chap1':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Retour au QG", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("📟 Information Chiffrée")
    tab1, tab2, tab3, tab4 = st.tabs(["🔢 Coeff. Multiplicateur", "📈 Taux d'évolution", "🔄 Évolutions Successives", "🕹️ Mission Eleven"])

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

    # --- SOUS-CHAPITRE 4 : QUIZZ ---
    with tab4:
        # On appelle la fonction de quiz qu'on a créée plus haut
        afficher_interface_quiz()

# =================================================================
# CHAPITRE 2 : SUITES NUMÉRIQUES
# =================================================================
elif st.session_state.page == 'chap2':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Retour au QG", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("📈 Suites Numériques")
    t_gen, t_ari, t_geo, tab4 = st.tabs(["📚 Généralités", "➕ Arithmétiques", "✖️ Géométriques", "🕹️ Mission Eleven"])
    # --- ONGLET 1 : GÉNÉRALITÉS ---
    with t_gen:
        st.subheader("📚 Guide de survie : Les Bases")
        
        with st.expander("🤔 Forme Explicite vs Récurrence"):
            st.write("#### 1️⃣ Forme Explicite (Le calcul direct)")
            st.write("On calcule n'importe quel terme directement avec **n**.")
            st.latex(r"u_n = f(n)")
            st.info(r"👉 *Exemple :* $u_n = 3n + 2$. Pour $u_{100}$, on fait $3 \times 100 + 2$. Rapide !")
            
            st.divider()
            
            st.write("#### 2️⃣ Forme Récurrence (L'escalier)")
            st.write("On a besoin du terme d'avant pour calculer le suivant. Il y a **toujours 2 lignes**.")
            st.latex(r"\begin{cases} u_0 = 5 \\ u_{n+1} = u_n + 3 \end{cases}")
            st.warning("⚠️ *Ici, pour avoir $u_{10}$, il faut d'abord calculer $u_1, u_2, u_3...$ jusqu'à 9. C'est long !*")

        with st.expander("🔄 Sens de variation (Monotonie)"):
            st.write("Pour savoir si une suite monte ou descend, on calcule la différence :")
            st.latex(r"u_{n+1} - u_n")
            
            st.info("⚠️ **Condition :** Le signe doit être le même **quel que soit $n$** (le résultat ne doit pas dépendre de $n$).")
            
            st.success("↗️ **Résultat > 0 :** La suite est **Croissante**.")
            st.error("↘️ **Résultat < 0 :** La suite est **Décroissante**.")
            
            st.warning("""
            **Attention :** Certaines suites ne sont ni l'une ni l'autre !  
            *Exemple :* $u_n = (-1)^n$ donne une suite qui alterne : $1, -1, 1, -1...$  
            On dit qu'elle n'est **pas monotone**.
            """)

    
    # --- ONGLET 2 : ARITHMÉTIQUES ---
    with t_ari:
        st.subheader("🪜 Suites Arithmétiques (Addition)")
        st.info(r"""
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
        st.warning(r"""
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


    # --- SOUS-CHAPITRE 4 : QUIZZ ---
    with tab4:
        # On appelle la fonction de quiz qu'on a créée plus haut
        afficher_interface_quiz()


# =================================================================
# CHAPITRE 3 : POLYNÔMES DU 2ND DEGRÉ
# =================================================================
elif st.session_state.page == 'chap3':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Retour au QG", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("🛸 Polynômes du Second Degré")
    t_cours, t_galerie, t_calc, tab4 = st.tabs(["📚 Les 3 Formes", "🖼️ Galerie", "📈 Simulateur", "🕹️ Mission Eleven"])
    
    # --- ONGLET 1 : LES FORMES (COURS) ---
    with t_cours:
        st.subheader("🧬 Les 3 visages d'une même fonction")
        st.write("Exemple unique pour tout le cours : $f(x) = 2x^2 + 4x - 6$")

        with st.expander("1. Forme Développée : $f(x) = ax^2 + bx + c$"):
            st.info("**Utile :** Le nombre **c = -6** est l'ordonnée à l'origine (coupe l'axe vertical).")
            st.latex(r"f(0) = c = -6")
            st.info("**Utile encore :** Le nombre **a** est ici positif **a = 2** ce qui donne le sens de la courbe (parabole dirigée vers le haut, en forme de cuvette ou de sourire) ; si **a** avait été négatif, la parabole aurait été dirigée vers le bas, en forme de colline ou de tristesse.")
        
        with st.expander("2. Forme Canonique : $f(x) = a(x - \\alpha)^2 + \\beta$"):
            st.success(r"""
            **🎯 Le Sommet $S(\alpha ; \beta)$ :**
            - $\alpha = \frac{-b}{2a} = \frac{-4}{2 \times 2} = \mathbf{-1}$
            - $\beta = f(\alpha) = 2(-1)^2 + 4(-1) - 6 = \mathbf{-8}$
            """)
            st.write("👉 *Le sommet de cette parabole est le point $S(-1 ; -8)$.*")
            
        with st.expander("3. Forme Factorisée : $f(x) = a(x - x_1)(x - x_2)$"):
            st.warning("**Interprétation :** $x_1$ et $x_2$ sont les **racines** (les valeurs de $x$ pour lesquelles la fonction $f$ s'annule, donc là où la courbe coupe l'axe horizontal).")
            st.latex(r"f(x) = 2(x - 1)(x + 3) \rightarrow x_1 = 1, x_2 = -3")
            st.warning("**IMPORTANT :** les **racines** permettent de connaître le signe de la fonction $f$ : je retiens que la fonction $f$ est du signe de **a** à l'extérieur des **racines** $x_1$ et $x_2$")
            st.write(r"👉 dans mon exemple de $f$ : *$f(x)$ est positif jusque -3, négatif entre -3 et 1, puis à nouveau positif à partir de 1*")
            st.write(r"**Version mathématique :**")
            st.info(r"""
            - $f(x) \geqslant 0$ si $x \in ]-\infty ; -3] \cup [1 ; +\infty[$
            - $f(x) \leqslant 0$ si $x \in [-3 ; 1]$
            """)

    
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
            sa = st.slider("Coefficient a (Ouverture et sens)", -4.0, 4.0, 1.0, step=0.5)
            s_alpha = st.number_input("Alpha (abscisse du sommet)", value=2.0)
            s_beta = st.number_input("Beta (ordonnée du sommet)", value=3.0)
        
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


    # --- SOUS-CHAPITRE 4 : QUIZZ ---
    with tab4:
        # On appelle la fonction de quiz qu'on a créée plus haut
        afficher_interface_quiz()



# =================================================================
# CHAPITRE 4 : PROBABILITÉS
# =================================================================
elif st.session_state.page == 'chap4':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Retour au QG", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("🎲 Probabilités")
    tab_cours, tab_tab, tab_arbre, tab4 = st.tabs(["📚 Rappels", "📊 Tableau", "🌳 Arbre", "🕹️ Mission Eleven"])

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
        
        # CSS Ultra-Précis pour le centrage des cellules
        st.markdown("""
        <style>
            /* Centre le tableau dans la page */
            div[data-testid="stTable"] {
                display: flex;
                justify-content: center;
            }
            /* Force le centrage du texte dans TOUTES les cellules du tableau */
            div[data-testid="stTable"] table td, 
            div[data-testid="stTable"] table th {
                text-align: center !important;
                vertical-align: middle !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.table(df_prob)
        
        st.divider()

        st.write("#### ❓ Question d'entraînement")
        st.write("D'après le tableau ci-dessus, quelle est la **fréquence** (en %) de **filles sportives** parmi le total des élèves ?")
        st.caption("💡 Rappel : Fréquence % = (Valeur de la case / Total général) × 100")

        # Entrée de l'élève
        ans_pct = st.number_input("Réponse en % (ex: 37,5) :", value=0.0, step=0.1, key="input_c4_f")
        
        if st.button("Vérifier le pourcentage", key="btn_c4_f"):
            bonne_reponse = 37.5
            if abs(ans_pct - bonne_reponse) == 0:
                st.balloons()
                st.success(f"Bravo ! Le calcul est : (15 / 40) × 100 = **{bonne_reponse}%**")
            else:
                st.error(f"Pas tout à fait. Cherchez la case 'Filles' + 'Sportifs' (15) et divisez par le Total (40).")

    # --- 3. ARBRE DE CHOIX (STYLE GRAPHIQUE ÉPURÉ ET MATHÉMATIQUE) ---
    with tab_arbre:
        st.subheader("🌳 Arbre de Probabilités")
        st.write("Visualisation mathématique des chemins possibles (basée sur les données du tableau) :")

        # Configuration du graphique plus grand pour éviter les chevauchements
        fig, ax = plt.subplots(figsize=(12, 7)) # Taille augmentée
        fig.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#161b22')

        # Définition des événements (pour la clarté pédagogique)
        # A = Fille, B = Sportif
        
        # Coordonnées des nœuds ajustées pour aérer l'affichage
        nodes = {
            'START': (0, 0),
            'A': (1, 1.2),      # Fille
            'nonA': (1, -1.2),  # Garçon (non Fille)
            'B_A': (2.2, 1.8),  # Sportif sachant Fille
            'nonB_A': (2.2, 0.6), # Non Sportif sachant Fille
            'B_nonA': (2.2, -0.6), # Sportif sachant Garçon
            'nonB_nonA': (2.2, -1.8) # Non Sportif sachant Garçon
        }

        # Dessiner les branches (Lignes Rouges fines)
        def draw_branch(p1, p2, label):
            ax.plot([nodes[p1][0], nodes[p2][0]], [nodes[p1][1], nodes[p2][1]], 
                    color='#ff4b4b', lw=2.5, zorder=1) # Rouge plus discret
            # Label de probabilité (notation mathématique)
            mid_x = (nodes[p1][0] + nodes[p2][0]) / 2
            mid_y = (nodes[p1][1] + nodes[p2][1]) / 2
            # Texte blanc, gras, taille raisonnable
            ax.text(mid_x, mid_y + 0.12, label, color='white', fontweight='bold', ha='center', fontsize=11)

        # Dessiner les branches avec les notations mathématiques P(A), P_A(B)
        draw_branch('START', 'A', r'$P(A)$')
        draw_branch('START', 'nonA', r'$P(\bar{A})$')
        draw_branch('A', 'B_A', r'$P_A(B)$')
        draw_branch('A', 'nonB_A', r'$P_A(\bar{B})$')
        draw_branch('nonA', 'B_nonA', r'$P_{\bar{A}}(B)$')
        draw_branch('nonA', 'nonB_nonA', r'$P_{\bar{A}}(\bar{B})$')
        
        # Dessiner les nœuds (Points Cyan plus petits)
        for name, pos in nodes.items():
            ax.scatter(pos[0], pos[1], color='#00d4ff', s=150, zorder=2, edgecolors='white')
            # Label du nœud (simple lettre) placé à droite pour gagner de l'espace
            if name != 'START':
                label_node = name.replace("B_nonA", r"$\bar{A}\cap B$").replace("nonB_nonA", r"$\bar{A}\cap \bar{B}$").replace("B_A", r"$A\cap B$").replace("nonB_A", r"$A\cap \bar{B}$")
                # Cas particuliers pour les noeuds intermédiaires
                if name == 'A': label_node = r'$A$'
                if name == 'nonA': label_node = r'$\bar{A}$'
                
                # Placement stratégique du texte
                ax.text(pos[0] + 0.08, pos[1], label_node, color='#00d4ff', fontsize=12, va='center', fontweight='bold')

        # Nettoyage du graphique
        ax.set_xlim(-0.3, 2.8)
        ax.set_ylim(-2.2, 2.2)
        ax.axis('off') # On cache les axes pour l'arbre

        st.pyplot(fig)

        # --- NOUVEAU BLOC DE CORRESPONDANCE (DISCRET ET CLAIR) ---
        st.write("---")
        st.write("### 📐 Correspondance avec les données du Tableau")
        
        c1, c2 = st.columns(2)
        
        with c1:
            st.info(r"""
            **Événements définis :**
            - $A$ : Choisir une Fille
            - $\bar{A}$ : Choisir un Garçon
            - $B$ : Choisir un(e) Sportif(ve)
            """)
            st.success(r"""
            **Calculs issus du Tableau :**
            - $P(A) = 20 / 40 = 0,5$
            - $P(\bar{A}) = 20 / 40 = 0,5$
            """)

        with c2:
            st.warning(r"""
            **Probabilités Conditionnelles (2nd niveau) :**
            - $P_A(B) = 15 / 20 = 0,75$ (Filles sportives parmi les filles)
            - $P_A(\bar{B}) = 5 / 20 = 0,25$ (Filles non sportives parmi les filles)
            - $P_{\bar{A}}(B) = 12 / 20 = 0,6$ (Garçons sportifs parmi les garçons)
            - $P_{\bar{A}}(\bar{B}) = 8 / 20 = 0,4$ (Garçons non sportifs parmi les garçons)
            """)


    # --- SOUS-CHAPITRE 4 : QUIZZ ---
    with tab4:
        # On appelle la fonction de quiz qu'on a créée plus haut
        afficher_interface_quiz()

# =================================================================
# CHAPITRE 5 : DÉRIVATION
# =================================================================
elif st.session_state.page == 'chap5':
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    st.button("⬅️ Retour au QG", on_click=aller_a_home)
    st.markdown('</div>', unsafe_allow_html=True)

    st.title("📈 Dérivation")
    st.write("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Nombre Dérivé", 
        "🧪 Formules", 
        "⚡ Méthodes", 
        "🏹 Tangentes", 
        "🕹️ Mission Eleven"
    ])

    # --- SOUS-CHAPITRE 1 : LE NOMBRE DÉRIVÉ ---
    with tab1:
        st.subheader("📍 Zoom sur un point : La pente locale")
        st.info("Le nombre dérivé $f'(a)$ est la pente (le coefficient directeur) de la tangente à la courbe au point d'abscisse $a$.")
        
        col_slope, col_viz = st.columns([1, 1])
        with col_slope:
            st.write("**Exploration interactive : $f(x) = x^2$**")
            a_val = st.slider("Choisissez le point a :", -3.0, 3.0, 1.0, step=0.1)
            f_a = a_val**2
            # La dérivée de x² est 2x
            pente = 2 * a_val
            st.metric(label=f"Nombre dérivé f'({a_val})", value=f"{pente:.2f}")
            st.write(f"En ce point, la courbe monte avec une pente de **{pente:.2f}**.")

        with col_viz:
            # Graphique interactif de la tangente
            x_range = np.linspace(-4, 4, 100)
            y_curve = x_range**2
            # Équation de la tangente : y = f'(a)(x-a) + f(a)
            y_tangent = pente * (x_range - a_val) + f_a

            fig, ax = plt.subplots()
            ax.plot(x_range, y_curve, color='white', label="f(x) = x²")
            ax.plot(x_range, y_tangent, color='#ff0000', linestyle='--', label="Tangente")
            ax.scatter([a_val], [f_a], color='#ff0000', zorder=5) # Le point de contact
            
            ax.set_ylim(-1, 10)
            ax.set_facecolor('#0e1117')
            fig.patch.set_facecolor('#0e1117')
            ax.tick_params(colors='white')
            ax.legend()
            st.pyplot(fig)

    # --- SOUS-CHAPITRE 2 : FONCTIONS DÉRIVÉES ---
    with tab2:
        st.subheader("🧪 Formulaire des pouvoirs")
        st.write("Voici les formules pour transformer une fonction en sa dérivée :")

        c1, c2 = st.columns(2)
        with c1:
            st.success("**Constante** \n $f(x) = k \implies f'(x) = 0$")
            st.success("**Carré** \n $f(x) = x^2 \implies f'(x) = 2x$")
            st.success("**Cube** \n $f(x) = x^3 \implies f'(x) = 3x^2$")
            st.success("**Puissance $n$** \n $f(x) = x^n \implies f'(x) = n x^{n-1}$")
        with c2:
            st.success("**Affine** \n $f(x) = ax + b \implies f'(x) = a$")
            st.success("**Inverse** \n $f(x) = \\frac{1}{x} \implies f'(x) = -\\frac{1}{x^2}$")
            st.success("**Racine** \n $f(x) = \sqrt{x} \implies f'(x) = \\frac{1}{2\sqrt{x}}$")
        
        st.markdown("---")
        st.subheader("🧠 Le lien Sacré : Signe ➡️ Variation")
        
        st.warning("""
        **Règle d'or :** Étudier les variations d'une fonction $f$, c'est étudier le **SIGNE** de sa dérivée $f'$.
        - Si $f'(x) > 0$ (positive) : la fonction $f$ est **croissante** (elle monte).
        - Si $f'(x) < 0$ (négative) : la fonction $f$ est **décroissante** (elle descend).
        """)

        # --- EXEMPLE DE TABLEAU DE VARIATION ---
        st.write("---")
        
        # On laisse le titre de l'expander vide de texte pour éviter le bug de couleur
        with st.expander("📝 MÉTHODE : Dresser un tableau de variations", expanded=False):
            # On place le VRAI titre ici : il sera TOUJOURS lisible
            st.markdown("""
                <h5 style='color: #00d4ff;'>📍 MÉTHODE : Dresser un tableau de variations</h5>
                <p style='color: white;'><b>Énoncé :</b> Dresser le tableau de variations de f(x) = x² - 6x</p>
            """, unsafe_allow_html=True)
            
            st.write("1. **Dérivée :** $f'(x) = 2x - 6$ : fonction affine de coefficient a = 2 qui est positif")
            st.write("2. **Racine :** $2x - 6 = 0 \implies 2x = 6 \implies x = 3$")
            st.write("3. **Image du sommet :** $f(3) = 3^2 - 6 \\times 3 = 9 - 18 = -9$")

            # Le tableau avec forçage de couleur blanche ligne par ligne
            st.latex(r"""
            \begin{array}{|c|ccccc|}
            \hline
            \color{white} x & \color{white} -\infty & & \color{white} 3 & & \color{white} +\infty \\
            \hline
            \color{white} \text{Signe de } f'(x) & & \color{white} - & \color{white} 0 & \color{white} + & \\
            \hline
            & \color{white} +\infty & & & & \color{white} +\infty \\
            \color{white} \text{Variations de } f & & \color{white} \searrow & & \color{white} \nearrow & \\
            & & & \color{white} -9 & & \\
            \hline
            \end{array}
            """)
            
            st.info("💡 **Analyse :** Comme a = 2 est positif, la dérivée $2x-6$ est négative pour $x < 3$ (la fonction descend) et positive pour $x > 3$ (la fonction monte).")

    
    
    # --- SOUS-CHAPITRE 3 : MÉTHODES DE CALCUL (LES TUYAUX) ---
    with tab3:
        st.subheader("⚡ Protocoles de Combinaison")
        st.write("Pour dériver les fonctions du programme, Eleven utilise deux règles simples :")

        # Règle 1 : La Somme
        st.info("### 1️⃣ La Règle de la Somme")
        # Note le 'r' avant les guillemets pour éviter le bug "imes"
        st.latex(r"f(x) = u(x) + v(x) \implies f'(x) = u'(x) + v'(x)")
        st.write("**Le tuyau :** On dérive chaque morceau séparément. C'est la règle magique pour les polynômes !")
        st.success("**Exemple :** $f(x) = x^2 + 5x - 3$ \n\n - $x^2$ devient $2x$ \n\n - $5x$ devient $5$ \n\n - $-3$ devient $0$ \n\n **Résultat :** $f'(x) = 2x + 5$")

        # Règle 2 : Constante multiplicatrice
        st.info("### 2️⃣ La Règle du Nombre Collé (Coefficient)")
        st.latex(r"f(x) = k \cdot u(x) \implies f'(x) = k \cdot u'(x)")
        st.write("**Le tuyau :** Si un nombre est multiplié à $x$, il 'survit' et attend que la puissance de $x$ descende.")
        st.success(r"**Exemple :** $g(x) = 4x^3$ : On garde le $4$, on dérive $x^3$ en $3x^2$. **Calcul :** $4 \times 3x^2 = 12x^2$")

        
        # L'AVERTISSEMENT CRUCIAL
        st.error("⚠️ **ALERTE DEMOGORGON : LE PIÈGE DU PRODUIT**")
        st.markdown("""
        En STMG, si tu vois un produit de deux parenthèses, **ne dérive pas chaque parenthèse séparément !** La technique secrète consiste à **développer** l'expression d'abord pour n'avoir que des additions à gérer.
        
        **Exemple :** Soit $f(x) = (x + 3)(x - 2)$
        1. **On développe :** $f(x) = x^2 - 2x + 3x - 6 = x^2 + x - 6$
        2. **Maintenant, on dérive facilement :** $f'(x) = 2x + 1$
        
        *C'est beaucoup plus sûr et c'est ce qui est attendu au Bac !*
        """)

    # --- SOUS-CHAPITRE 4 : ÉQUATION DE TANGENTE ---
    with tab4:
        st.subheader("🏹 L'arme de précision")
        st.write("L'équation de la droite tangente au point d'abscisse $a$ est donnée par la formule :")
        st.latex(r"y = f'(a)(x - a) + f(a)")
        
        st.markdown("""
        **Les 4 étapes pour réussir :**
        1. **Calculer l'image** : $f(a)$
        2. **Calculer la dérivée** : $f'(x)$
        3. **Calculer le nombre dérivé** : $f'(a)$
        4. **Remplacer** les valeurs dans la formule magique.
        """)

        st.write("---")
        # On réutilise l'astuce de l'expander "safe" pour le mode sombre
        with st.expander("📝 EXEMPLE DÉTAILLÉ", expanded=False):
            st.markdown("""
                <h4 style='color: white; margin-top: -10px;'>📝 EXEMPLE DÉTAILLÉ</h4>
                <h5 style='color: #00d4ff;'>📍 Équation de tangente pour f(x) = x² au point a = 3</h5>
                <p style='color: white;'>On veut trouver l'équation de la droite qui "frôle" la parabole au point d'abscisse 3.</p>
            """, unsafe_allow_html=True)

            col_etapes, col_bilan = st.columns([1.5, 1])
            
            with col_etapes:
                st.write("**Étape 1 :** Calcul de l'image")
                st.success("$f(3) = 3^2 = 9$")
                
                st.write("**Étape 2 & 3 :** Dérivée et nombre dérivé")
                st.info("$f'(x) = 2x$ \n\n Donc $f'(3) = 2 \\times 3 = 6$")
            
            with col_bilan:
                st.write("**Étape 4 :** On remplace")
                st.warning("""
                $y = 6(x - 3) + 9$  
                $y = 6x - 18 + 9$  
                **$y = 6x - 9$**
                """)

            st.info("💡 **Interprétation :** La tangente est une droite de pente 6 qui passe par le point (3 ; 9).")

    # --- SOUS-CHAPITRE 5 : MISSION ELEVEN ---
    with tab5:
        # Pense à ajouter 'chap5' dans ton dictionnaire 'themes' de la fonction afficher_interface_quiz
        afficher_interface_quiz()
