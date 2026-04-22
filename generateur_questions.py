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
    lettres = ["A", "B", "C", "D"]
    toutes = [bonne_reponse] + mauvaises_reponses[:3]
    random.shuffle(toutes)
    options = [f"{lettres[i]}. {toutes[i]}" for i in range(len(toutes))]
    idx_bonne = toutes.index(bonne_reponse)
    reponse = f"{lettres[idx_bonne]}. {bonne_reponse}"
    return options, reponse

def to_graph_val(val):
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
        produit = f1_val * f2_val
        explication = (
            f"Pour $x={x_test}$ : "
            f"$({x_test} - ({r1_str})) \\times ({x_test} - ({r2_str})) = "
            f"{fmt_latex(f1_val)} \\times {fmt_latex(f2_val)} = {fmt_latex(produit)}$, "
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
    for diff in ["Facile", "Moyen", "Difficile"]:
        print(f"\n--- Difficulté : {diff} ---")
        q = generer_question_produit(difficulte=diff)
        print(f"Question : {q['question']}")
        print(f"Options  : {q['options']}")
        print(f"Réponse  : {q['reponse']}")
        print(f"Explication : {q['explication']}")
        print(f"Graph : {q['graph_data']}")
