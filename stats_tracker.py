"""
stats_tracker.py
Module de tracking des statistiques d'utilisation vers Google Sheets.
Enregistre les sessions et les quiz lancés.
"""

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from zoneinfo import ZoneInfo
import traceback

# Fuseau horaire France
TZ_PARIS = ZoneInfo("Europe/Paris")

def now_paris():
    """Retourne l'heure actuelle en heure de Paris."""
    return datetime.now(TZ_PARIS)

# ID du Google Sheet
SHEET_ID = "1uxpMlwvShuO_uxAePYpnmFz5CRKnLkgnIQ6oVL6OviA"

# Scopes nécessaires
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Noms des onglets
ONGLET_SESSIONS = "Sessions"
ONGLET_QUIZ     = "Quiz"


def get_client():
    """
    Crée et retourne un client gspread authentifié.
    Utilise les secrets Streamlit.
    """
    try:
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=SCOPES
        )
        return gspread.authorize(creds)
    except Exception as e:
        # On ne bloque pas l'app si Google Sheets est indisponible
        return None


def get_sheet(client, nom_onglet):
    """Retourne un onglet du Google Sheet."""
    try:
        spreadsheet = client.open_by_key(SHEET_ID)
        return spreadsheet.worksheet(nom_onglet)
    except Exception:
        return None


# ================================================================
# TRACKING DES SESSIONS
# ================================================================

def enregistrer_debut_session():
    """
    Enregistre le début d'une session.
    Appelé une seule fois à l'ouverture de l'app.
    """
    if 'session_debut' in st.session_state:
        return  # Déjà enregistré

    now = now_paris()
    st.session_state.session_debut = now
    st.session_state.session_pages = []
    st.session_state.session_row = None  # ligne dans Google Sheets

    try:
        client = get_client()
        if client is None:
            return

        sheet = get_sheet(client, ONGLET_SESSIONS)
        if sheet is None:
            return

        # Ajouter une nouvelle ligne
        nouvelle_ligne = [
            now.strftime("%d/%m/%Y"),    # Date
            now.strftime("%H:%M:%S"),    # Heure début
            "",                           # Dernière action (sera mise à jour)
            "",                           # Durée (sera calculée)
            ""                            # Pages visitées
        ]
        sheet.append_row(nouvelle_ligne)

        # Mémoriser le numéro de ligne pour la mettre à jour plus tard
        toutes_lignes = sheet.get_all_values()
        st.session_state.session_row = len(toutes_lignes)

    except Exception:
        pass  # On ne bloque pas l'app


def mettre_a_jour_session(page_visitee=None):
    """
    Met à jour la session en cours :
    - Dernière action = maintenant
    - Durée estimée
    - Pages visitées
    Appelé à chaque navigation/action.
    """
    if 'session_debut' not in st.session_state:
        return

    now = now_paris()
    debut = st.session_state.session_debut

    # Calculer la durée en minutes
    duree = round((now - debut).total_seconds() / 60, 1)

    # Ajouter la page si nouvelle
    if page_visitee and page_visitee not in st.session_state.session_pages:
        st.session_state.session_pages.append(page_visitee)

    pages_str = ", ".join(st.session_state.session_pages)

    try:
        client = get_client()
        if client is None:
            return

        sheet = get_sheet(client, ONGLET_SESSIONS)
        if sheet is None or not st.session_state.session_row:
            return

        row = st.session_state.session_row

        # Mettre à jour les colonnes C, D, E
        sheet.update_cell(row, 3, now.strftime("%H:%M:%S"))  # Dernière action
        sheet.update_cell(row, 4, duree)                      # Durée en minutes
        sheet.update_cell(row, 5, pages_str)                  # Pages visitées

    except Exception:
        pass


# ================================================================
# TRACKING DES QUIZ
# ================================================================

NOMS_CHAPITRES = {
    "chap0": "Fonctions",
    "chap1": "Info Chiffrée",
    "chap2": "Suites",
    "chap3": "Second Degré",
    "chap4": "Probabilités",
    "chap5": "Dérivation",
    "automatismes_stmg": "Automatismes STMG",
    "automatismes_generale": "Automatismes Générale"
}


def enregistrer_lancement_quiz(chapitre, difficulte, nb_questions):
    """
    Enregistre le lancement d'un quiz.
    Appelé quand l'élève clique sur "Lancer la Mission Eleven".
    """
    now = now_paris()
    nom_chapitre = NOMS_CHAPITRES.get(chapitre, chapitre)

    # Stocker dans session_state pour mise à jour du score plus tard
    st.session_state.quiz_log = {
        "row": None,
        "chapitre": nom_chapitre,
        "difficulte": difficulte,
        "nb_questions": nb_questions,
        "heure": now
    }

    try:
        client = get_client()
        if client is None:
            return

        sheet = get_sheet(client, ONGLET_QUIZ)
        if sheet is None:
            return

        nouvelle_ligne = [
            now.strftime("%d/%m/%Y"),   # Date
            now.strftime("%H:%M:%S"),   # Heure
            nom_chapitre,               # Chapitre
            difficulte,                 # Difficulté
            "",                         # Score (mis à jour à la fin)
            nb_questions                # Nb questions
        ]
        sheet.append_row(nouvelle_ligne)

        # Mémoriser le numéro de ligne
        toutes_lignes = sheet.get_all_values()
        st.session_state.quiz_log["row"] = len(toutes_lignes)

        # Mettre à jour la session
        mettre_a_jour_session(page_visitee=nom_chapitre)

    except Exception:
        pass


def enregistrer_fin_quiz(score):
    """
    Met à jour le score à la fin d'un quiz.
    Appelé quand l'élève termine toutes les questions.
    """
    if 'quiz_log' not in st.session_state:
        return
    if not st.session_state.quiz_log.get("row"):
        return

    nb_questions = st.session_state.quiz_log.get("nb_questions", 11)
    score_str = f"{score}/{nb_questions}"

    try:
        client = get_client()
        if client is None:
            return

        sheet = get_sheet(client, ONGLET_QUIZ)
        if sheet is None:
            return

        row = st.session_state.quiz_log["row"]
        sheet.update_cell(row, 5, score_str)  # Colonne E = Score

    except Exception:
        pass
