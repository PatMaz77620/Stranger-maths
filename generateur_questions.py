"""
generateur_questions.py
Générateur de questions paramétrées pour Stranger Maths
Tableaux de signes : affines, produits, second degré
100% fiable mathématiquement, sans appel GPT
"""

import random
from fractions import Fraction

# ================================================================
# UTILITAIRES
# ================================================================

def fmt(val):
    """
    Formate un nombre (entier, float ou Fraction) pour affichage.
    Exemples : 2 -> "2", Fraction(1,2) -> "1/2", -3 -> "-3"
    """
    if isinstance(val, Fraction):
        if val.denominator == 1:
            return str(val.numerator)
        return f"{val.numerator}/{val.denominator}"
    if isinstance(val, float) and val == int(val):
        return str(int(val))
    return str(val)

def fmt_latex(val):
    """
    Formate un nombre pour affichage LaTeX.
    Exemples :
      Fraction(1,2)  -> "\\frac{1}{2}"
      Fraction(-2,3) -> "-\\frac{2}{3}"  (signe devant, pas dans le numérateur)
      2              -> "2"
    """
    if isinstance(val, Fraction):
        if val.denominator == 1:
            return str(val.numerator)
        # Signe séparé du numérateur
        signe = "-" if val < 0 else ""
        num = abs(val.numerator)
        den = val.denominator
        return f"{signe}\\frac{{{num}}}{{{den}}}"
    return fmt(val)

def fmt_facteur(coef, var="x", racine=None):
    """
    Formate un facteur (coef * x - coef * racine) de façon lisible.
    Exemples :
      coef=1, racine=3  -> "(x - 3)"
      coef=2, racine=-1 -> "(2x + 2)"  [car 2*(x-(-1)) = 2x+2]
      coef=1, racine=Fraction(1,2) -> "(x - 1/2)"
    """
    if coef == 1:
        prefix = ""
    elif coef == -1:
        prefix = "-"
    else:
        prefix = fmt(coef)

    if racine == 0:
        return f"({prefix}{var})"
    elif isinstance(racine, Fraction):
        r_latex = fmt_latex(racine)
        signe = "+" if racine < 0 else "-"
        r_abs = Fraction(abs(racine.numerator), racine.denominator)
        return f"({prefix}{var} {signe} {fmt_latex(r_abs)})"
    else:
        signe = "+" if racine < 0 else "-"
        return f"({prefix}{var} {signe} {abs(racine)})"

def fmt_fonction_affine(a, b):
    """
    Formate f(x) = ax + b proprement.
    Evite -1x (→ -x) et 1x (→ x)
    """
    # Coefficient de x
    if a == 1:
        a_str = ""
    elif a == -1:
        a_str = "-"
    else:
        a_str = fmt_latex(a)

    if b == 0:
        return f"f(x) = {a_str}x"
    signe_b = "+" if b > 0 else "-"
    b_abs = abs(b) if not isinstance(b, Fraction) else Fraction(abs(b.numerator), b.denominator)
    return f"f(x) = {a_str}x {signe_b} {fmt_latex(b_abs)}"

def fmt_fonction_produit(a, r1, r2):
    """
    Formate f(x) = a(x-r1)(x-r2) proprement.
    """
    if a == 1:
        a_str = ""
    elif a == -1:
        a_str = "-"
    else:
        a_str = fmt_latex(a)
    f1 = fmt_facteur(1, racine=r1)
    f2 = fmt_facteur(1, racine=r2)
    return f"f(x) = {a_str}{f1}{f2}"

def racine_aleatoire(difficulte, exclude=[]):
    """
    Génère une racine aléatoire selon la difficulté.
    exclude : liste de valeurs à éviter
    """
    fractions_simples = [Fraction(1,2), Fraction(-1,2),
                         Fraction(1,3), Fraction(-1,3),
                         Fraction(3,2), Fraction(-3,2),
                         Fraction(2,3), Fraction(-2,3)]
    entiers = [i for i in range(-5, 6) if i != 0 and i not in exclude]

    if difficulte == "Facile":
        candidats = entiers
    elif difficulte == "Moyen":
        # 1 chance sur 3 d'avoir une fraction
        if random.random() < 1/3:
            candidats = [f for f in fractions_simples if f not in exclude]
        else:
            candidats = entiers
    else:  # Difficile
        # 1 chance sur 2 d'avoir une fraction
        if random.random() < 1/2:
            candidats = [f for f in fractions_simples if f not in exclude]
        else:
            candidats = entiers

    candidats = [c for c in candidats if c not in exclude]
    if not candidats:
        candidats = [i for i in range(-5, 6) if i != 0 and i not in exclude]
    return random.choice(candidats)

def coef_aleatoire(difficulte):
    """
    Génère un coefficient a aléatoire selon la difficulté.
    Toujours non nul.
    """
    entiers = [-3, -2, -1, 1, 2, 3]
    fractions_simples = [Fraction(1,2), Fraction(-1,2),
                         Fraction(3,2), Fraction(-3,2),
                         Fraction(1,3), Fraction(-1,3)]

    if difficulte == "Facile":
        return random.choice(entiers)
    elif difficulte == "Moyen":
        return random.choice(entiers)
    else:  # Difficile
        if random.random() < 1/2:
            return random.choice(fractions_simples)
        return random.choice(entiers)

def melanger_options(bonne_reponse, mauvaises_reponses):
    """
    Mélange les options et retourne (options_formatées, bonne_reponse_formatée).
    """
    def nettoyer(texte):
        """Corrige les doubles backslashes et applique fmt_option."""
        if isinstance(texte, str):
            # Corriger \\\\frac → \frac etc
            texte = texte.replace('\\\\', '\\')
        return fmt_option(texte)

    lettres = ["A", "B", "C", "D"]
    toutes = [bonne_reponse] + mauvaises_reponses[:3]
    random.shuffle(toutes)
    options = [f"{lettres[i]}. {nettoyer(toutes[i])}" for i in range(len(toutes))]
    idx_bonne = toutes.index(bonne_reponse)
    reponse = f"{lettres[idx_bonne]}. {nettoyer(bonne_reponse)}"
    return options, reponse

def to_graph_val(val):
    """
    Convertit une valeur pour graph_data.
    Retourne (valeur_float, label_str).
    """
    if isinstance(val, Fraction):
        return float(val), fmt_latex(val)
    return val, str(val)

def fmt_option(texte):
    """
    S'assure que les fractions LaTeX dans les options sont bien rendues
    par st.markdown en les entourant de $...$.
    Corrige aussi les doubles backslashes \\\\frac → \\frac.
    """
    import re
    if not isinstance(texte, str):
        return str(texte)
    # Corriger les doubles backslashes
    texte = texte.replace('\\\\frac', '\\frac')
    # Si déjà entièrement dans $...$, on ne touche pas
    if texte.startswith('$') and texte.endswith('$'):
        return texte
    # Entoure \frac{}{} de $ si pas déjà dans $
    def entourer(m):
        return f"${m.group(0)}$"
    texte = re.sub(r'(?<!\$)\\frac\{[^}]*\}\{[^}]*\}(?!\$)', entourer, texte)
    return texte

def fmt_calcul_facteur(x_test, racine):
    """
    Formate (x_test - racine) proprement pour les explications.
    Evite x - (-1) → écrit x + 1 directement.
    """
    resultat = x_test - racine
    if isinstance(racine, Fraction) or (not isinstance(racine, Fraction) and racine < 0):
        r_abs = abs(racine) if not isinstance(racine, Fraction) else Fraction(abs(racine.numerator), racine.denominator)
        return f"({fmt_latex(x_test)} + {fmt_latex(r_abs)})", fmt_latex(resultat)
    elif racine == 0:
        return f"({fmt_latex(x_test)})", fmt_latex(resultat)
    else:
        return f"({fmt_latex(x_test)} - {fmt_latex(racine)})", fmt_latex(resultat)
    """
    Formate (x_test - racine) proprement pour les explications.
    Evite x - (-1) → écrit x + 1 directement.
    Ex: x_test=−7, racine=−1 → "−7 + 1 = −6"
    Ex: x_test=−7, racine=3  → "−7 − 3 = −10"
    """
    resultat = x_test - racine
    if isinstance(racine, Fraction) or racine < 0:
        # racine négative → signe +
        r_abs = abs(racine) if not isinstance(racine, Fraction) else Fraction(abs(racine.numerator), racine.denominator)
        return f"({fmt_latex(x_test)} + {fmt_latex(r_abs)})", fmt_latex(resultat)
    elif racine == 0:
        return f"({fmt_latex(x_test)})", fmt_latex(resultat)
    else:
        return f"({fmt_latex(x_test)} - {fmt_latex(racine)})", fmt_latex(resultat)
    """
    Convertit une valeur pour graph_data.
    Les fractions sont converties en float pour matplotlib,
    mais affichées en LaTeX dans les labels.
    Retourne (valeur_float, label_str).
    """
    if isinstance(val, Fraction):
        return float(val), fmt_latex(val)
    return val, str(val)


# ================================================================
# GÉNÉRATEUR : FONCTIONS AFFINES
# ================================================================

def generer_question_affine(difficulte="Moyen", type_question=None):
    """
    Génère une question sur le tableau de signes d'une fonction affine.
    f(x) = a*x + b, racine en x0 = -b/a

    type_question : "T1", "T2", "T3", "T5" ou None (aléatoire)
    """
    if type_question is None:
        type_question = random.choice(["T1", "T2", "T3", "T5"])

    # Génération des paramètres
    a = coef_aleatoire(difficulte)
    x0 = racine_aleatoire(difficulte)  # racine de f

    # b = -a * x0 pour que f(x0) = 0
    b = -a * x0
    if isinstance(b, Fraction) and b.denominator == 1:
        b = b.numerator

    # Signes du tableau
    if a > 0:
        signes = ["-", "+"]
    else:
        signes = ["+", "-"]

    # Formatage
    f_str = fmt_fonction_affine(a, b)
    x0_str = fmt_latex(x0)

    # graph_data pour le tableau de signes
    x0_float, x0_label = to_graph_val(x0)
    graph_data = {
        "type": "signes",
        "fonction": "f(x)",
        "racines": [x0_float],
        "racines_labels": [x0_label],
        "signes": signes
    }

    # ---- TYPE T1 : Retrouver la fonction ----
    if type_question == "T1":
        question = "D'après le tableau de signes ci-contre, quelle fonction lui correspond ?"

        # Mauvaises réponses : changer le signe de a ou de b
        a2 = -a
        b2 = -a2 * x0
        if isinstance(b2, Fraction) and b2.denominator == 1:
            b2 = b2.numerator

        a3 = a
        x0_faux = racine_aleatoire(difficulte, exclude=[x0])
        b3 = -a3 * x0_faux
        if isinstance(b3, Fraction) and b3.denominator == 1:
            b3 = b3.numerator

        a4 = -a
        b4 = -a4 * x0_faux
        if isinstance(b4, Fraction) and b4.denominator == 1:
            b4 = b4.numerator

        bonne = f_str
        mauvaises = [
            fmt_fonction_affine(a2, b2),
            fmt_fonction_affine(a3, b3),
            fmt_fonction_affine(a4, b4)
        ]
        options, reponse = melanger_options(bonne, mauvaises)

        explication = (
            f"La racine est $x={x0_str}$ et le signe passe de "
            f"{'$-$ à $+$' if a > 0 else '$+$ à $-$'}, "
            f"donc $a {'>' if a > 0 else '<'} 0$. "
            f"La fonction est $\\{f_str}$."
        )

    # ---- TYPE T2 : Retrouver la racine ----
    elif type_question == "T2":
        question = f"D'après le tableau de signes de $f(x) = {fmt_fonction_affine(a, b).replace('f(x) = ', '')}$, quelle est la racine de $f$ ?"

        x0_faux1 = racine_aleatoire(difficulte, exclude=[x0])
        x0_faux2 = racine_aleatoire(difficulte, exclude=[x0, x0_faux1])
        x0_faux3 = racine_aleatoire(difficulte, exclude=[x0, x0_faux1, x0_faux2])

        bonne = f"$x = {x0_str}$"
        mauvaises = [
            f"$x = {fmt_latex(x0_faux1)}$",
            f"$x = {fmt_latex(x0_faux2)}$",
            f"$x = {fmt_latex(x0_faux3)}$"
        ]
        options, reponse = melanger_options(bonne, mauvaises)

        explication = (
            f"On résout $f(x) = 0$ : "
            f"${fmt_latex(a)}x {'+' if b >= 0 else ''} {fmt_latex(b)} = 0$ "
            f"donc $x = {x0_str}$."
        )

    # ---- TYPE T3 : Lire le signe d'une valeur ----
    elif type_question == "T3":
        # Choisir une valeur de test différente de la racine
        if isinstance(x0, Fraction):
            x_test_pool = [i for i in range(-6, 7) if Fraction(i) != x0]
        else:
            x_test_pool = [i for i in range(-6, 7) if i != x0]
        x_test = random.choice(x_test_pool)

        # Calculer le signe réel
        val = a * x_test + b
        if isinstance(val, Fraction):
            signe_reel = "Positif" if val > 0 else "Négatif"
        else:
            signe_reel = "Positif" if val > 0 else "Négatif"

        signe_oppose = "Négatif" if signe_reel == "Positif" else "Positif"

        question = f"D'après le tableau de signes ci-contre, quel est le signe de $f({x_test})$ ?"

        bonne = signe_reel
        mauvaises = [signe_oppose, "Nul", "Impossible à déterminer"]
        options, reponse = melanger_options(bonne, mauvaises)

        zone = "à gauche" if (a > 0 and x_test < x0) or (a < 0 and x_test > x0) else "à droite"
        explication = (
            f"$x={x_test}$ est {zone} de la racine $x={x0_str}$, "
            f"donc dans la zone de signe ${'+'  if signe_reel == 'Positif' else '-'}$."
        )

    # ---- TYPE T5 : Identifier le signe de a ----
    else:  # T5
        question = (
            f"Le tableau de signes ci-contre montre un signe "
            f"${'+'  if signes[0] == '+' else '-'}$ à gauche de la racine "
            f"et ${'+'  if signes[1] == '+' else '-'}$ à droite. "
            f"Que peut-on dire du coefficient $a$ ?"
        )

        if a > 0:
            bonne = "$a > 0$ : la fonction est croissante"
            mauvaises = [
                "$a < 0$ : la fonction est décroissante",
                "$a = 0$ : la fonction est constante",
                "Impossible à déterminer"
            ]
            explication = (
                "Le signe passe de $-$ à $+$ : la fonction est croissante, "
                "donc $a > 0$."
            )
        else:
            bonne = "$a < 0$ : la fonction est décroissante"
            mauvaises = [
                "$a > 0$ : la fonction est croissante",
                "$a = 0$ : la fonction est constante",
                "Impossible à déterminer"
            ]
            explication = (
                "Le signe passe de $+$ à $-$ : la fonction est décroissante, "
                "donc $a < 0$."
            )

        options, reponse = melanger_options(bonne, mauvaises)

    return {
        "question": question,
        "options": options,
        "reponse": reponse,
        "explication": explication,
        "has_graph": True,
        "graph_data": graph_data,
        "type_question": type_question,
        "theme": "affine"
    }


# ================================================================
# GÉNÉRATEUR : PRODUIT DE DEUX FACTEURS
# ================================================================

def generer_question_produit(difficulte="Moyen", type_question=None):
    """
    Génère une question sur le tableau de signes d'un produit (x-r1)(x-r2).
    """
    if type_question is None:
        type_question = random.choice(["T1", "T2", "T3", "T5", "calcul"])

    # Génération des paramètres
    a = coef_aleatoire(difficulte)
    r1 = racine_aleatoire(difficulte)
    r2 = racine_aleatoire(difficulte, exclude=[r1])

    # On s'assure que r1 < r2
    if r1 > r2:
        r1, r2 = r2, r1

    # Signes du tableau selon le signe de a
    if a > 0:
        signes = ["+", "-", "+"]
    else:
        signes = ["-", "+", "-"]

    # Formatage
    f_str = fmt_fonction_produit(a, r1, r2)
    r1_str = fmt_latex(r1)
    r2_str = fmt_latex(r2)

    # graph_data
    r1_float, r1_label = to_graph_val(r1)
    r2_float, r2_label = to_graph_val(r2)
    graph_data = {
        "type": "signes",
        "fonction": "f(x)",
        "racines": [r1_float, r2_float],
        "racines_labels": [r1_label, r2_label],
        "signes": signes
    }

    # ---- TYPE calcul : question sans tableau ----
    if type_question == "calcul":
        # Choisir une valeur de test
        x_test_pool = [i for i in range(-7, 8) if i != r1 and i != r2]
        x_test = random.choice(x_test_pool)

        val = a * (x_test - r1) * (x_test - r2)
        if isinstance(val, Fraction):
            signe_reel = "Positif" if val > 0 else "Négatif"
        else:
            signe_reel = "Positif" if val > 0 else "Négatif"
        signe_oppose = "Négatif" if signe_reel == "Positif" else "Positif"

        question = f"Quel est le signe de $f({x_test})$ pour $f(x) = {f_str.replace('f(x) = ', '')}$ ?"
        bonne = signe_reel
        mauvaises = [signe_oppose, "Nul", "Impossible à déterminer"]
        options, reponse = melanger_options(bonne, mauvaises)

        f1_val = x_test - r1
        f2_val = x_test - r2
        produit_sans_a = f1_val * f2_val
        produit = a * produit_sans_a
        f1_str, f1_res = fmt_calcul_facteur(x_test, r1)
        f2_str, f2_res = fmt_calcul_facteur(x_test, r2)
        a_str = fmt_latex(a)

        if a == 1:
            explication = (
                f"Pour $x={x_test}$ : "
                f"${f1_str} \\times {f2_str} = "
                f"{f1_res} \\times {f2_res} = {fmt_latex(produit)}$, "
                f"ce qui est {signe_reel.lower()}."
            )
        else:
            explication = (
                f"Pour $x={x_test}$ : "
                f"${a_str} \\times {f1_str} \\times {f2_str} = "
                f"{a_str} \\times {f1_res} \\times {f2_res} = {fmt_latex(produit)}$, "
                f"ce qui est {signe_reel.lower()}."
            )
        graph_data = None
        has_graph = False

    # ---- TYPE T1 : Retrouver la fonction ----
    elif type_question == "T1":
        question = "D'après le tableau de signes ci-contre, quelle fonction lui correspond ?"

        # Mauvaises réponses
        a2 = -a
        r1_faux = racine_aleatoire(difficulte, exclude=[r1, r2])
        r2_faux = racine_aleatoire(difficulte, exclude=[r1, r2, r1_faux])
        if r1_faux > r2_faux:
            r1_faux, r2_faux = r2_faux, r1_faux

        bonne = f_str
        mauvaises = [
            fmt_fonction_produit(a2, r1, r2),
            fmt_fonction_produit(a, r1_faux, r2_faux),
            fmt_fonction_produit(a2, r1_faux, r2_faux)
        ]
        options, reponse = melanger_options(bonne, mauvaises)

        explication = (
            f"Racines $x={r1_str}$ et $x={r2_str}$, "
            f"signes {'$+/-/+$' if a > 0 else '$-/+/-$'} donc "
            f"$a {'>' if a > 0 else '<'} 0$, parabole tournée vers "
            f"{'le haut' if a > 0 else 'le bas'}."
        )

    # ---- TYPE T2 : Retrouver les racines ----
    elif type_question == "T2":
        question = (
            f"Le tableau de signes ci-contre correspond à "
            f"$f(x) = {fmt_latex(a)}(x-a)(x-b)$ avec $a < b$. "
            f"Quelles sont les valeurs de $a$ et $b$ ?"
        )

        r1_faux = racine_aleatoire(difficulte, exclude=[r1, r2])
        r2_faux = racine_aleatoire(difficulte, exclude=[r1, r2, r1_faux])

        bonne = f"$a={r1_str}$ et $b={r2_str}$"
        mauvaises = [
            f"$a={fmt_latex(-r1)}$ et $b={fmt_latex(-r2)}$",
            f"$a={fmt_latex(r1_faux)}$ et $b={fmt_latex(r2_faux)}$",
            f"$a={r2_str}$ et $b={r1_str}$"
        ]
        options, reponse = melanger_options(bonne, mauvaises)

        explication = (
            f"Les racines se lisent directement sur le tableau : "
            f"$x={r1_str}$ et $x={r2_str}$. "
            f"Comme $a < b$, on a $a={r1_str}$ et $b={r2_str}$."
        )

    # ---- TYPE T3 : Lire le signe d'une valeur ----
    elif type_question == "T3":
        x_test_pool = [i for i in range(-7, 8) if i != r1 and i != r2]
        x_test = random.choice(x_test_pool)

        val = a * (x_test - r1) * (x_test - r2)
        signe_reel = "Positif" if val > 0 else "Négatif"
        signe_oppose = "Négatif" if signe_reel == "Positif" else "Positif"

        question = f"D'après le tableau de signes ci-contre, quel est le signe de $f({x_test})$ ?"
        bonne = signe_reel
        mauvaises = [signe_oppose, "Nul", "Impossible à déterminer"]
        options, reponse = melanger_options(bonne, mauvaises)

        if r1 < x_test < r2:
            zone = f"entre les racines $x={r1_str}$ et $x={r2_str}$"
        elif x_test < r1:
            zone = f"à gauche de la racine $x={r1_str}$"
        else:
            zone = f"à droite de la racine $x={r2_str}$"

        explication = (
            f"$x={x_test}$ est {zone}, "
            f"donc dans la zone de signe "
            f"${'+'  if signe_reel == 'Positif' else '-'}$."
        )

    # ---- TYPE T5 : Identifier le signe de a ----
    else:  # T5
        question = (
            f"Le tableau de signes ci-contre montre les signes "
            f"${'+'  if signes[0] == '+' else '-'}$ | $0$ | "
            f"${'+'  if signes[1] == '+' else '-'}$ | $0$ | "
            f"${'+'  if signes[2] == '+' else '-'}$. "
            f"Que peut-on dire du coefficient $a$ ?"
        )

        if a > 0:
            bonne = "$a > 0$ : parabole tournée vers le haut"
            mauvaises = [
                "$a < 0$ : parabole tournée vers le bas",
                "$a = 0$ : la fonction s'annule partout",
                "Impossible à déterminer"
            ]
            explication = (
                "Le signe est $+$ à l'extérieur des racines et $-$ entre elles : "
                "la parabole est tournée vers le haut, donc $a > 0$."
            )
        else:
            bonne = "$a < 0$ : parabole tournée vers le bas"
            mauvaises = [
                "$a > 0$ : parabole tournée vers le haut",
                "$a = 0$ : la fonction s'annule partout",
                "Impossible à déterminer"
            ]
            explication = (
                "Le signe est $-$ à l'extérieur des racines et $+$ entre elles : "
                "la parabole est tournée vers le bas, donc $a < 0$."
            )

        options, reponse = melanger_options(bonne, mauvaises)

    return {
        "question": question,
        "options": options,
        "reponse": reponse,
        "explication": explication,
        "has_graph": True if type_question != "calcul" else False,
        "graph_data": graph_data,
        "type_question": type_question,
        "theme": "produit"
    }


# ================================================================
# GÉNÉRATEUR : SECOND DEGRÉ (FORME FACTORISÉE)
# ================================================================

def generer_question_second_degre(difficulte="Moyen", type_question=None):
    """
    Génère une question sur le signe d'un trinôme du second degré
    donné sous forme factorisée ou carrée.
    Adapté au programme 1ère STMG (sans discriminant).
    """
    if type_question is None:
        type_question = random.choice(["forme_factorisee", "carre", "T1", "T3"])

    a = coef_aleatoire(difficulte)
    r1 = racine_aleatoire(difficulte)
    r2 = racine_aleatoire(difficulte, exclude=[r1])
    if r1 > r2:
        r1, r2 = r2, r1

    r1_str = fmt_latex(r1)
    r2_str = fmt_latex(r2)

    if a > 0:
        signes = ["+", "-", "+"]
    else:
        signes = ["-", "+", "-"]

    r1_float, r1_label = to_graph_val(r1)
    r2_float, r2_label = to_graph_val(r2)
    graph_data = {
        "type": "signes",
        "fonction": "f(x)",
        "racines": [r1_float, r2_float],
        "racines_labels": [r1_label, r2_label],
        "signes": signes
    }

    f_str = fmt_fonction_produit(a, r1, r2)

    # ---- Forme factorisée : signe de f ----
    if type_question == "forme_factorisee":
        signe_question = random.choice(["strictement négatif", "strictement positif",
                                        "négatif ou nul", "positif ou nul"])

        if signe_question == "strictement négatif":
            if a > 0:
                bonne = f"$x \\in ]{r1_str} ; {r2_str}[$"
                expl_zone = "entre les racines"
            else:
                bonne = f"$x \\in ]-\\infty ; {r1_str}[ \\cup ]{r2_str} ; +\\infty[$"
                expl_zone = "à l'extérieur des racines"
        elif signe_question == "strictement positif":
            if a > 0:
                bonne = f"$x \\in ]-\\infty ; {r1_str}[ \\cup ]{r2_str} ; +\\infty[$"
                expl_zone = "à l'extérieur des racines"
            else:
                bonne = f"$x \\in ]{r1_str} ; {r2_str}[$"
                expl_zone = "entre les racines"
        elif signe_question == "négatif ou nul":
            if a > 0:
                bonne = f"$x \\in [{r1_str} ; {r2_str}]$"
                expl_zone = "entre les racines (crochets fermés)"
            else:
                bonne = f"$x \\in ]-\\infty ; {r1_str}] \\cup [{r2_str} ; +\\infty[$"
                expl_zone = "à l'extérieur des racines (crochets fermés)"
        else:  # positif ou nul
            if a > 0:
                bonne = f"$x \\in ]-\\infty ; {r1_str}] \\cup [{r2_str} ; +\\infty[$"
                expl_zone = "à l'extérieur des racines (crochets fermés)"
            else:
                bonne = f"$x \\in [{r1_str} ; {r2_str}]$"
                expl_zone = "entre les racines (crochets fermés)"

        question = f"On donne $f(x) = {f_str.replace('f(x) = ', '')}$. Pour quelles valeurs de $x$ a-t-on $f(x)$ {signe_question} ?"

        # Mauvaises réponses : inverser intérieur/extérieur, changer les crochets
        if "extérieur" in expl_zone:
            m1 = f"$x \\in ]{r1_str} ; {r2_str}[$"
            m2 = f"$x \\in [{r1_str} ; {r2_str}]$"
        else:
            m1 = f"$x \\in ]-\\infty ; {r1_str}[ \\cup ]{r2_str} ; +\\infty[$"
            m2 = f"$x \\in ]-\\infty ; {r1_str}] \\cup [{r2_str} ; +\\infty[$"

        r1_faux = racine_aleatoire(difficulte, exclude=[r1, r2])
        r2_faux = racine_aleatoire(difficulte, exclude=[r1, r2, r1_faux])
        if r1_faux > r2_faux:
            r1_faux, r2_faux = r2_faux, r1_faux
        m3 = f"$x \\in ]{fmt_latex(r1_faux)} ; {fmt_latex(r2_faux)}[$"

        options, reponse = melanger_options(bonne, [m1, m2, m3])

        explication = (
            f"Racines : $x={r1_str}$ et $x={r2_str}$. "
            f"Le coefficient $a={'>' if a > 0 else '<'} 0$ donc parabole "
            f"tournée vers {'le haut' if a > 0 else 'le bas'} : "
            f"$f(x)$ est {signe_question} {expl_zone}."
        )
        has_graph = False
        graph_data = None

    # ---- Carré parfait ----
    elif type_question == "carre":
        r0 = racine_aleatoire(difficulte)
        r0_str = fmt_latex(r0)
        a_carre = coef_aleatoire(difficulte)

        if a_carre > 0:
            question = f"On donne $f(x) = {fmt_latex(a_carre)}(x - {r0_str})^2$. Quel est le signe de $f(x)$ ?"
            bonne = f"Toujours positif ou nul, nul uniquement en $x={r0_str}$"
            mauvaises = [
                "Toujours strictement positif",
                f"Positif pour $x > {r0_str}$, négatif pour $x < {r0_str}$",
                "Toujours négatif ou nul"
            ]
            explication = (
                f"$(x-{r0_str})^2 \\geq 0$ toujours. "
                f"Multiplié par $a={fmt_latex(a_carre)} > 0$, reste $\\geq 0$. "
                f"Nul uniquement en $x={r0_str}$."
            )
        else:
            question = f"On donne $f(x) = {fmt_latex(a_carre)}(x - {r0_str})^2$. Quel est le signe de $f(x)$ ?"
            bonne = f"Toujours négatif ou nul, nul uniquement en $x={r0_str}$"
            mauvaises = [
                "Toujours strictement négatif",
                f"Négatif pour $x > {r0_str}$, positif pour $x < {r0_str}$",
                "Toujours positif ou nul"
            ]
            explication = (
                f"$(x-{r0_str})^2 \\geq 0$ toujours. "
                f"Multiplié par $a={fmt_latex(a_carre)} < 0$, devient $\\leq 0$. "
                f"Nul uniquement en $x={r0_str}$."
            )

        options, reponse = melanger_options(bonne, mauvaises)
        has_graph = False
        graph_data = None

    # ---- T1 : Retrouver la fonction depuis le tableau ----
    elif type_question == "T1":
        question = "D'après le tableau de signes ci-contre, quelle fonction lui correspond ?"

        a2 = -a
        r1_faux = racine_aleatoire(difficulte, exclude=[r1, r2])
        r2_faux = racine_aleatoire(difficulte, exclude=[r1, r2, r1_faux])
        if r1_faux > r2_faux:
            r1_faux, r2_faux = r2_faux, r1_faux

        bonne = f_str
        mauvaises = [
            fmt_fonction_produit(a2, r1, r2),
            fmt_fonction_produit(a, r1_faux, r2_faux),
            fmt_fonction_produit(a2, r1_faux, r2_faux)
        ]
        options, reponse = melanger_options(bonne, mauvaises)

        explication = (
            f"Racines $x={r1_str}$ et $x={r2_str}$, "
            f"signes {'$+/-/+$' if a > 0 else '$-/+/-$'} donc "
            f"$a {'>' if a > 0 else '<'} 0$, parabole tournée vers "
            f"{'le haut' if a > 0 else 'le bas'}."
        )
        has_graph = True

    # ---- T3 : Lire le signe d'une valeur ----
    else:  # T3
        x_test_pool = [i for i in range(-7, 8) if i != r1 and i != r2]
        x_test = random.choice(x_test_pool)

        val = a * (x_test - r1) * (x_test - r2)
        signe_reel = "Positif" if val > 0 else "Négatif"
        signe_oppose = "Négatif" if signe_reel == "Positif" else "Positif"

        question = f"D'après le tableau de signes ci-contre, quel est le signe de $f({x_test})$ ?"
        bonne = signe_reel
        mauvaises = [signe_oppose, "Nul", "Impossible à déterminer"]
        options, reponse = melanger_options(bonne, mauvaises)

        if r1 < x_test < r2:
            zone = f"entre les racines $x={r1_str}$ et $x={r2_str}$"
        elif x_test < r1:
            zone = f"à gauche de la racine $x={r1_str}$"
        else:
            zone = f"à droite de la racine $x={r2_str}$"

        explication = (
            f"$x={x_test}$ est {zone}, "
            f"donc dans la zone de signe "
            f"${'+'  if signe_reel == 'Positif' else '-'}$."
        )
        has_graph = True

    return {
        "question": question,
        "options": options,
        "reponse": reponse,
        "explication": explication,
        "has_graph": has_graph,
        "graph_data": graph_data if has_graph else None,
        "type_question": type_question,
        "theme": "second_degre"
    }


# ================================================================
# GÉNÉRATEUR : SUITES NUMÉRIQUES
# ================================================================

def _params_suite(difficulte):
    """
    Génère des paramètres aléatoires pour une suite.
    Retourne (u0, nature, r_ou_q) où nature = 'arithmetique' ou 'geometrique'.
    """
    # Valeur initiale u0
    if difficulte == "Facile":
        u0 = random.choice([1, 2, 3, 4, 5, 10])
    elif difficulte == "Moyen":
        u0 = random.choice([1, 2, 3, 5, 10, 20, -1, -2])
    else:
        u0 = random.choice([1, 2, 3, 5, 10, -1, -2, -5,
                            Fraction(1,2), Fraction(3,2)])

    nature = random.choice(["arithmetique", "geometrique"])

    if nature == "arithmetique":
        if difficulte == "Facile":
            r = random.choice([1, 2, 3, 5, -1, -2])
        elif difficulte == "Moyen":
            r = random.choice([1, 2, 3, 5, -1, -2, -3, 10])
        else:
            r = random.choice([1, 2, 3, -1, -2, -3,
                               Fraction(1,2), Fraction(-1,2), Fraction(3,2)])
        return u0, nature, r
    else:
        if difficulte == "Facile":
            q = random.choice([2, 3, -1])
        elif difficulte == "Moyen":
            q = random.choice([2, 3, -2, -1, 10])
        else:
            q = random.choice([2, 3, -2, -1,
                               Fraction(1,2), Fraction(1,3), Fraction(-1,2)])
        return u0, nature, q

def _calculer_termes(u0, nature, r_ou_q, n=5):
    """Calcule les n+1 premiers termes de la suite."""
    termes = [u0]
    for _ in range(n):
        if nature == "arithmetique":
            termes.append(termes[-1] + r_ou_q)
        else:
            termes.append(termes[-1] * r_ou_q)
    return termes

def _fmt_relation_recurrence(u0, nature, r_ou_q):
    """
    Formate la relation de récurrence en LaTeX.
    Ex: u0=2, arithmetique, r=3 → "$u_0 = 2$ et $u_{n+1} = u_n + 3$"
    """
    u0_str = fmt_latex(u0)
    r_str = fmt_latex(r_ou_q)

    if nature == "arithmetique":
        if r_ou_q >= 0:
            rel = f"$u_{{n+1}} = u_n + {r_str}$"
        else:
            r_abs = abs(r_ou_q) if not isinstance(r_ou_q, Fraction) else Fraction(abs(r_ou_q.numerator), r_ou_q.denominator)
            rel = f"$u_{{n+1}} = u_n - {fmt_latex(r_abs)}$"
    else:
        rel = f"$u_{{n+1}} = {r_str} \\times u_n$"

    return f"$u_0 = {u0_str}$ et {rel} pour tout $n \\geq 0$"

def _fmt_forme_explicite(u0, nature, r_ou_q):
    """
    Formate la forme explicite en LaTeX.
    Arithmétique : u_n = u0 + n*r
    Géométrique  : u_n = u0 * q^n
    """
    u0_str = fmt_latex(u0)
    r_str = fmt_latex(r_ou_q)

    if nature == "arithmetique":
        if r_ou_q == 0:
            return f"$u_n = {u0_str}$"
        elif r_ou_q == 1:
            return f"$u_n = {u0_str} + n$"
        elif r_ou_q == -1:
            return f"$u_n = {u0_str} - n$"
        elif r_ou_q > 0:
            return f"$u_n = {u0_str} + {r_str} \\times n$"
        else:
            r_abs = abs(r_ou_q) if not isinstance(r_ou_q, Fraction) else Fraction(abs(r_ou_q.numerator), r_ou_q.denominator)
            return f"$u_n = {u0_str} - {fmt_latex(r_abs)} \\times n$"
    else:
        if r_ou_q == 1:
            return f"$u_n = {u0_str}$"
        # Parenthèses autour des raisons négatives ou fractionnaires
        if isinstance(r_ou_q, Fraction) or r_ou_q < 0:
            q_str = f"\\left({fmt_latex(r_ou_q)}\\right)"
        else:
            q_str = r_str
        return f"$u_n = {u0_str} \\times {q_str}^n$"


# ---- TYPE A : Identifier la nature ----

def generer_question_suite_nature(difficulte="Moyen"):
    """
    Donne une relation de récurrence → l'élève identifie arithmétique / géométrique / ni l'un ni l'autre.
    """
    # On choisit aléatoirement entre les 3 cas
    cas = random.choice(["arithmetique", "geometrique", "autre"])

    if cas == "arithmetique":
        u0, _, r = _params_suite(difficulte)
        while _ != "arithmetique":
            u0, _, r = _params_suite(difficulte)
        u0, nature, r_ou_q = u0, "arithmetique", r
        recurrence = _fmt_relation_recurrence(u0, nature, r_ou_q)
        bonne = "Arithmétique"
        explication = (
            f"On calcule $u_{{n+1}} - u_n = {fmt_latex(r_ou_q)}$ : "
            f"c'est constant, donc la suite est **arithmétique** de raison $r = {fmt_latex(r_ou_q)}$."
        )

    elif cas == "geometrique":
        u0, _, q = _params_suite(difficulte)
        while _ != "geometrique":
            u0, _, q = _params_suite(difficulte)
        u0, nature, r_ou_q = u0, "geometrique", q
        recurrence = _fmt_relation_recurrence(u0, nature, r_ou_q)
        bonne = "Géométrique"
        explication = (
            f"On calcule $\\frac{{u_{{n+1}}}}{{u_n}} = {fmt_latex(r_ou_q)}$ : "
            f"c'est constant, donc la suite est **géométrique** de raison $q = {fmt_latex(r_ou_q)}$."
        )

    else:  # ni arithmétique ni géométrique → on utilise (-1)^n
        u0 = random.choice([1, 2, 3])
        u0_str = fmt_latex(u0)
        recurrence = f"$u_0 = {u0_str}$ et $u_{{n+1}} = (-1) \\times u_n + 1$ pour tout $n \\geq 0$"
        bonne = "Ni arithmétique ni géométrique"
        explication = (
            "La différence $u_{n+1} - u_n$ n'est pas constante et "
            "le rapport $\\frac{u_{n+1}}{u_n}$ n'est pas constant non plus : "
            "la suite n'est ni arithmétique ni géométrique."
        )

    question = f"La suite $(u_n)$ est définie par {recurrence}. Quelle est la nature de cette suite ?"

    bonne_rep = bonne
    mauvaises = [r for r in ["Arithmétique", "Géométrique", "Ni arithmétique ni géométrique"] if r != bonne]
    mauvaises.append("Constante")
    mauvaises = mauvaises[:3]

    options, reponse = melanger_options(bonne_rep, mauvaises)

    return {
        "question": question,
        "options": options,
        "reponse": reponse,
        "explication": explication,
        "has_graph": False,
        "graph_data": None,
        "type_question": "nature",
        "theme": "suites"
    }


# ---- TYPE B : Sens de variation ----

def generer_question_suite_variation(difficulte="Moyen"):
    """
    Donne une relation de récurrence → l'élève identifie croissante / décroissante / ni l'un ni l'autre.
    """
    cas = random.choice(["croissante", "decroissante", "alternee"])

    if cas == "croissante":
        # Suite arithmétique r > 0 ou géométrique q > 1
        choix = random.choice(["arithmetique", "geometrique"])
        if choix == "arithmetique":
            u0 = random.choice([1, 2, 3, 5])
            r = random.choice([1, 2, 3])
            recurrence = _fmt_relation_recurrence(u0, "arithmetique", r)
            explication = (
                f"La raison $r = {fmt_latex(r)} > 0$ donc chaque terme est plus grand que le précédent : "
                f"la suite est **croissante**."
            )
        else:
            u0 = random.choice([1, 2, 3])
            q = random.choice([2, 3])
            recurrence = _fmt_relation_recurrence(u0, "geometrique", q)
            explication = (
                f"$u_0 = {fmt_latex(u0)} > 0$ et $q = {fmt_latex(q)} > 1$ donc "
                f"chaque terme est multiplié par {fmt_latex(q)} : la suite est **croissante**."
            )
        bonne = "Croissante"

    elif cas == "decroissante":
        choix = random.choice(["arithmetique", "geometrique"])
        if choix == "arithmetique":
            u0 = random.choice([10, 20, 100])
            r = random.choice([-1, -2, -3])
            recurrence = _fmt_relation_recurrence(u0, "arithmetique", r)
            explication = (
                f"La raison $r = {fmt_latex(r)} < 0$ donc chaque terme est plus petit que le précédent : "
                f"la suite est **décroissante**."
            )
        else:
            u0 = random.choice([10, 20, 100])
            q = Fraction(1, 2)
            recurrence = _fmt_relation_recurrence(u0, "geometrique", q)
            explication = (
                f"$u_0 = {fmt_latex(u0)} > 0$ et $0 < q = {fmt_latex(q)} < 1$ donc "
                f"chaque terme est multiplié par $\\frac{{1}}{{2}}$ : la suite est **décroissante**."
            )
        bonne = "Décroissante"

    else:  # alternée → (-1)^n classique
        u0 = random.choice([1, 2, 3])
        recurrence = f"$u_0 = {fmt_latex(u0)}$ et $u_{{n+1}} = -u_n$ pour tout $n \\geq 0$"
        explication = (
            f"Les termes alternent entre ${fmt_latex(u0)}$ et $-{fmt_latex(u0)}$ : "
            f"la suite est **ni croissante ni décroissante**."
        )
        bonne = "Ni croissante ni décroissante"

    question = f"La suite $(u_n)$ est définie par {recurrence}. Cette suite est :"

    mauvaises = [r for r in ["Croissante", "Décroissante", "Ni croissante ni décroissante"] if r != bonne]
    mauvaises.append("Constante")
    mauvaises = mauvaises[:3]

    options, reponse = melanger_options(bonne, mauvaises)

    return {
        "question": question,
        "options": options,
        "reponse": reponse,
        "explication": explication,
        "has_graph": False,
        "graph_data": None,
        "type_question": "variation",
        "theme": "suites"
    }


# ---- TYPE C : Forme explicite ----

def generer_question_suite_explicite(difficulte="Moyen"):
    """
    Donne une relation de récurrence → l'élève trouve la forme explicite u_n = ...
    Toujours avec u_0 comme indice de départ.
    """
    u0, nature, r_ou_q = _params_suite(difficulte)
    # On force une suite arithmétique ou géométrique (pas "autre")
    while True:
        u0, nature, r_ou_q = _params_suite(difficulte)
        if nature in ["arithmetique", "geometrique"]:
            break

    recurrence = _fmt_relation_recurrence(u0, nature, r_ou_q)
    bonne = _fmt_forme_explicite(u0, nature, r_ou_q)

    # Mauvaises réponses : erreurs classiques
    # 1. Mauvais u0
    u0_faux = u0 + random.choice([1, 2, -1, -2])
    mauvaise_1 = _fmt_forme_explicite(u0_faux, nature, r_ou_q)

    # 2. Mauvaise raison
    if nature == "arithmetique":
        r_faux = r_ou_q + random.choice([1, 2, -1])
        mauvaise_2 = _fmt_forme_explicite(u0, nature, r_faux)
        # 3. Confondre arithmétique et géométrique
        mauvaise_3 = _fmt_forme_explicite(u0, "geometrique", r_ou_q)
    else:
        q_faux = r_ou_q + random.choice([1, -1])
        if q_faux == 0:
            q_faux = 2
        mauvaise_2 = _fmt_forme_explicite(u0, nature, q_faux)
        # 3. Confondre géométrique et arithmétique
        mauvaise_3 = _fmt_forme_explicite(u0, "arithmetique", r_ou_q)

    question = (
        f"La suite $(u_n)$ est définie par {recurrence}. "
        f"Quelle est la forme explicite de $u_n$ ?"
    )

    if nature == "arithmetique":
        explicite = _fmt_forme_explicite(u0, nature, r_ou_q)
        # On extrait la partie droite de u_n = ...
        partie_droite = explicite.replace("$u_n = ", "").replace("$", "")
        explication = (
            f"Suite arithmétique de premier terme $u_0 = {fmt_latex(u0)}$ "
            f"et de raison $r = {fmt_latex(r_ou_q)}$. "
            f"Formule : $u_n = u_0 + n \\times r = {partie_droite}$."
        )
    else:
        explicite = _fmt_forme_explicite(u0, nature, r_ou_q)
        partie_droite = explicite.replace("$u_n = ", "").replace("$", "")
        explication = (
            f"Suite géométrique de premier terme $u_0 = {fmt_latex(u0)}$ "
            f"et de raison $q = {fmt_latex(r_ou_q)}$. "
            f"Formule : $u_n = u_0 \\times q^n = {partie_droite}$."
        )

    options, reponse = melanger_options(bonne, [mauvaise_1, mauvaise_2, mauvaise_3])

    return {
        "question": question,
        "options": options,
        "reponse": reponse,
        "explication": explication,
        "has_graph": False,
        "graph_data": None,
        "type_question": "explicite",
        "theme": "suites"
    }


# ---- FONCTION PRINCIPALE SUITES ----

def generer_quiz_suites(nb_questions=6, difficulte="Moyen"):
    """
    Génère un quiz sur les suites numériques.
    Mélange les 3 types : nature, variation, explicite.
    """
    questions = []
    types = (
        ["nature"] * 2 +
        ["variation"] * 2 +
        ["explicite"] * 2
    )
    random.shuffle(types)
    types = types[:nb_questions]

    for t in types:
        if t == "nature":
            q = generer_question_suite_nature(difficulte)
        elif t == "variation":
            q = generer_question_suite_variation(difficulte)
        else:
            q = generer_question_suite_explicite(difficulte)
        questions.append(q)

    return questions


# ================================================================
# GÉNÉRATEUR : TABLEAUX DE VARIATIONS + DÉRIVATION
# ================================================================

def _params_variation(difficulte):
    """
    Génère les paramètres d'une fonction du second degré f(x) = a(x-s)² + t
    avec son tableau de variations.
    Retourne (a, sommet_x, sommet_y, x_vals_supplementaires)
    """
    if difficulte == "Facile":
        a = random.choice([1, -1, 2, -2])
        s = random.choice([-2, -1, 0, 1, 2])
        t = random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4])
    elif difficulte == "Moyen":
        a = random.choice([1, -1, 2, -2, 3, -3])
        s = random.choice(range(-3, 4))
        t = random.choice(range(-6, 7))
    else:
        a = random.choice([1, -1, 2, -2, 3, -3,
                           Fraction(1,2), Fraction(-1,2)])
        s = random.choice(range(-3, 4))
        t = random.choice(range(-6, 7))

    return a, s, t

def _generer_tableau_variations_data(a, s, t, x_supplementaires=None):
    """
    Génère le graph_data pour un tableau de variations de f(x) = a(x-s)² + t.
    """
    extremum_type = "min" if a > 0 else "max"
    signes = ["-", "+"] if a > 0 else ["+", "-"]

    return {
        "type": "variations",
        "fonction": "f",
        "derivee": "f'",
        "x_vals": [s],
        "f_vals": [t],
        "signes_deriv": signes,
        "extremums": [extremum_type],
        "a": float(a) if not isinstance(a, Fraction) else float(a),
        "s": s,
        "t": t
    }


# ---- TV1 : Lire la valeur au sommet (visible dans le tableau) ----

def generer_question_tv1_lire_valeur(difficulte="Moyen"):
    """
    Option B : l'élève lit uniquement les valeurs VISIBLES dans le tableau
    → valeur de f au sommet, ou valeur de x au sommet.
    """
    a, s, t = _params_variation(difficulte)
    graph_data = _generer_tableau_variations_data(a, s, t)

    extremum_type = "minimum" if a > 0 else "maximum"
    type_q = random.choice(["lire_f_sommet", "lire_x_sommet"])

    if type_q == "lire_f_sommet":
        question = (
            f"D'après le tableau de variations ci-contre, "
            f"quelle est la valeur du {extremum_type} de $f$ ?"
        )
        bonne = f"${fmt_latex(t)}$"
        mauvaises = [
            f"${fmt_latex(t + random.choice([1, 2, -1, -2]))}$",
            f"${fmt_latex(s)}$",
            f"${fmt_latex(t + random.choice([3, -3, 4, -4]))}$",
        ]
        explication = (
            f"Le {extremum_type} de $f$ se lit directement sur le tableau : "
            f"$f({fmt_latex(s)}) = {fmt_latex(t)}$."
        )
    else:
        question = (
            f"D'après le tableau de variations ci-contre, "
            f"en quelle valeur de $x$ le {extremum_type} de $f$ est-il atteint ?"
        )
        bonne = f"$x = {fmt_latex(s)}$"
        mauvaises = [
            f"$x = {fmt_latex(s + 1)}$",
            f"$x = {fmt_latex(s - 1)}$",
            f"$x = {fmt_latex(t)}$",
        ]
        explication = (
            f"Le {extremum_type} est atteint en $x = {fmt_latex(s)}$ "
            f"(valeur où $f'$ s'annule et change de signe)."
        )

    options, reponse = melanger_options(bonne, mauvaises)

    return {
        "question": question,
        "options": options,
        "reponse": reponse,
        "explication": explication,
        "has_graph": True,
        "graph_data": graph_data,
        "type_question": "TV1",
        "theme": "variations"
    }


# ---- TV2 : Identifier l'extremum ----

def generer_question_tv2_extremum(difficulte="Moyen"):
    """
    Donne un tableau de variations → l'élève identifie le maximum ou minimum.
    """
    a, s, t = _params_variation(difficulte)
    graph_data = _generer_tableau_variations_data(a, s, t)

    extremum_type = "minimum" if a > 0 else "maximum"
    extremum_type_opp = "maximum" if a > 0 else "minimum"

    # Question au choix
    type_q = random.choice(["valeur", "position", "nature"])

    if type_q == "valeur":
        question = f"D'après le tableau de variations ci-contre, quelle est la valeur du {extremum_type} de $f$ ?"
        bonne = f"${fmt_latex(t)}$"
        s_faux = s + random.choice([1, -1, 2])
        t_faux1 = a * (s_faux - s)**2 + t
        mauvaises = [
            f"${fmt_latex(s)}$",
            f"${fmt_latex(t_faux1)}$",
            f"${fmt_latex(t + random.choice([1,-1,2,-2]))}$"
        ]
        explication = (
            f"Le {extremum_type} de $f$ est atteint en $x = {fmt_latex(s)}$ "
            f"et vaut $f({fmt_latex(s)}) = {fmt_latex(t)}$."
        )

    elif type_q == "position":
        question = f"D'après le tableau de variations ci-contre, en quelle valeur de $x$ le {extremum_type} de $f$ est-il atteint ?"
        bonne = f"$x = {fmt_latex(s)}$"
        mauvaises = [
            f"$x = {fmt_latex(s + 1)}$",
            f"$x = {fmt_latex(s - 1)}$",
            f"$x = {fmt_latex(t)}$"
        ]
        explication = (
            f"D'après le tableau, $f'$ s'annule en $x = {fmt_latex(s)}$ "
            f"et change de signe : c'est donc là que $f$ atteint son {extremum_type}."
        )

    else:  # nature
        question = "D'après le tableau de variations ci-contre, la fonction $f$ admet :"
        bonne = f"Un {extremum_type} en $x = {fmt_latex(s)}$"
        mauvaises = [
            f"Un {extremum_type_opp} en $x = {fmt_latex(s)}$",
            f"Un {extremum_type} en $x = {fmt_latex(t)}$",
            f"Ni maximum ni minimum"
        ]
        explication = (
            f"$f'$ change de signe en $x = {fmt_latex(s)}$ : "
            f"de {'$-$ à $+$' if a > 0 else '$+$ à $-$'}, "
            f"donc $f$ admet un {extremum_type} en ce point."
        )

    options, reponse = melanger_options(bonne, mauvaises)

    return {
        "question": question,
        "options": options,
        "reponse": reponse,
        "explication": explication,
        "has_graph": True,
        "graph_data": graph_data,
        "type_question": "TV2",
        "theme": "variations"
    }


# ---- TV3 : Sens de variation sur un intervalle ----

def generer_question_tv3_sens(difficulte="Moyen"):
    """
    Donne un tableau de variations → l'élève lit le sens de variation.
    """
    a, s, t = _params_variation(difficulte)
    graph_data = _generer_tableau_variations_data(a, s, t)

    # Choisir un intervalle
    x1 = s - random.randint(1, 3)
    x2 = s + random.randint(1, 3)
    intervalles = [
        (f"$]-\\infty ; {fmt_latex(s)}[$", "croissante" if a < 0 else "décroissante"),
        (f"$]{fmt_latex(s)} ; +\\infty[$", "décroissante" if a < 0 else "croissante"),
    ]
    intervalle_str, sens_correct = random.choice(intervalles)
    sens_oppose = "décroissante" if sens_correct == "croissante" else "croissante"

    question = (
        f"D'après le tableau de variations ci-contre, "
        f"sur l'intervalle {intervalle_str}, la fonction $f$ est :"
    )
    bonne = sens_correct.capitalize()
    mauvaises = [
        sens_oppose.capitalize(),
        "Constante",
        "Ni croissante ni décroissante"
    ]
    options, reponse = melanger_options(bonne, mauvaises)

    if sens_correct == "croissante":
        explication = f"Sur cet intervalle, $f'(x) > 0$ donc $f$ est **croissante**."
    else:
        explication = f"Sur cet intervalle, $f'(x) < 0$ donc $f$ est **décroissante**."

    return {
        "question": question,
        "options": options,
        "reponse": reponse,
        "explication": explication,
        "has_graph": True,
        "graph_data": graph_data,
        "type_question": "TV3",
        "theme": "variations"
    }


# ---- Dérivation : signe de f' → croissance ----

def generer_question_derivation_signe(difficulte="Moyen"):
    """
    Donne f'(x) = ax + b → l'élève détermine sur quel intervalle f est croissante/décroissante.
    """
    # f'(x) = 2ax (dérivée de ax²+b) ou f'(x) = a (affine)
    type_q = random.choice(["affine_derivee", "second_degre_derivee"])

    if type_q == "affine_derivee":
        # f(x) = ax + b → f'(x) = a
        if difficulte == "Facile":
            a = random.choice([1, 2, 3, -1, -2])
        else:
            a = random.choice([1, 2, 3, -1, -2, -3,
                               Fraction(1,2), Fraction(-1,2)])

        fp_str = fmt_latex(a)
        if a > 0:
            sens = "croissante"
            intervalle = "$\\mathbb{R}$ tout entier"
        else:
            sens = "décroissante"
            intervalle = "$\\mathbb{R}$ tout entier"

        question = (
            f"Soit $f$ une fonction dont la dérivée est $f'(x) = {fp_str}$. "
            f"Sur quel intervalle $f$ est-elle {sens} ?"
        )
        bonne = intervalle
        mauvaises = [
            f"$]-\\infty ; 0[$",
            f"$]0 ; +\\infty[$",
            f"$f$ n'est {'pas ' if a > 0 else ''}croissante sur $\\mathbb{{R}}$"
        ]
        explication = (
            f"$f'(x) = {fp_str}$ {'$> 0$' if a > 0 else '$< 0$'} pour tout $x$, "
            f"donc $f$ est {sens} sur $\\mathbb{{R}}$."
        )

    else:
        # f(x) = ax² + b → f'(x) = 2ax
        if difficulte == "Facile":
            a = random.choice([1, 2, -1, -2])
        else:
            a = random.choice([1, 2, 3, -1, -2, -3])

        deux_a = 2 * a
        fp_str = f"{fmt_latex(deux_a)}x"

        if a > 0:
            sens_pos = "croissante"
            interv_pos = "$]0 ; +\\infty[$"
            sens_neg = "décroissante"
            interv_neg = "$]-\\infty ; 0[$"
        else:
            sens_pos = "décroissante"
            interv_pos = "$]0 ; +\\infty[$"
            sens_neg = "croissante"
            interv_neg = "$]-\\infty ; 0[$"

        choix = random.choice(["pos", "neg"])
        if choix == "pos":
            sens, intervalle = sens_pos, interv_pos
            sens_opp, interv_opp = sens_neg, interv_neg
        else:
            sens, intervalle = sens_neg, interv_neg
            sens_opp, interv_opp = sens_pos, interv_pos

        question = (
            f"Soit $f$ une fonction dont la dérivée est $f'(x) = {fp_str}$. "
            f"Sur quel intervalle $f$ est-elle {sens} ?"
        )
        bonne = intervalle
        mauvaises = [
            interv_opp,
            "$\\mathbb{R}$ tout entier",
            f"$f$ n'est pas {sens} sur ces intervalles"
        ]
        explication = (
            f"$f'(x) = {fp_str}$ : on résout $f'(x) {'>' if choix == 'pos' and a > 0 or choix == 'neg' and a < 0 else '<'} 0$. "
            f"$f$ est {sens} sur {intervalle}."
        )

    options, reponse = melanger_options(bonne, mauvaises)

    return {
        "question": question,
        "options": options,
        "reponse": reponse,
        "explication": explication,
        "has_graph": False,
        "graph_data": None,
        "type_question": "derivation_signe",
        "theme": "derivation"
    }


def generer_quiz_variations(nb_questions=6, difficulte="Moyen"):
    """
    Génère un quiz sur les tableaux de variations et la dérivation.
    Mélange TV1, TV2, TV3 et questions sur le signe de f'.
    """
    questions = []
    types = (
        ["TV1"] * 2 +
        ["TV2"] * 2 +
        ["TV3"] * 1 +
        ["deriv"] * 1
    )
    random.shuffle(types)
    types = types[:nb_questions]

    for t in types:
        if t == "TV1":
            q = generer_question_tv1_lire_valeur(difficulte)
        elif t == "TV2":
            q = generer_question_tv2_extremum(difficulte)
        elif t == "TV3":
            q = generer_question_tv3_sens(difficulte)
        else:
            q = generer_question_derivation_signe(difficulte)
        questions.append(q)

    return questions


# ================================================================
# FONCTION PRINCIPALE : GÉNÉRER UN QUIZ COMPLET
# ================================================================

def generer_quiz_tableaux_signes(nb_questions=11, difficulte="Moyen"):
    """
    Génère un quiz complet sur les tableaux de signes.
    Mélange affines, produits et second degré.
    """
    questions = []

    # Répartition selon le nombre de questions
    themes = (
        ["affine"] * 3 +
        ["produit"] * 4 +
        ["second_degre"] * 4
    )
    random.shuffle(themes)
    themes = themes[:nb_questions]

    for theme in themes:
        if theme == "affine":
            q = generer_question_affine(difficulte)
        elif theme == "produit":
            q = generer_question_produit(difficulte)
        else:
            q = generer_question_second_degre(difficulte)
        questions.append(q)

    return questions


# ================================================================
# TEST LOCAL (à lancer directement : python generateur_questions.py)
# ================================================================

if __name__ == "__main__":
    print("=== TEST DU GÉNÉRATEUR ===\n")

    print("--- Tableaux de signes ---")
    for diff in ["Facile", "Moyen", "Difficile"]:
        print(f"\nDifficulté : {diff}")
        q = generer_question_produit(difficulte=diff)
        print(f"Question : {q['question']}")
        print(f"Réponse  : {q['reponse']}")

    print("\n\n--- Suites : Nature ---")
    for _ in range(3):
        q = generer_question_suite_nature("Moyen")
        print(f"Q : {q['question']}")
        print(f"R : {q['reponse']}")
        print(f"Explication : {q['explication']}\n")

    print("\n--- Suites : Variation ---")
    for _ in range(3):
        q = generer_question_suite_variation("Moyen")
        print(f"Q : {q['question']}")
        print(f"R : {q['reponse']}")
        print(f"Explication : {q['explication']}\n")

    print("\n--- Suites : Forme explicite ---")
    for _ in range(3):
        q = generer_question_suite_explicite("Moyen")
        print(f"Q : {q['question']}")
        print(f"R : {q['reponse']}")
        print(f"Explication : {q['explication']}\n")

# mise à jour