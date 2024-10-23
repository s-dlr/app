"""
Mises jour du session state
"""
import pandas as pd
import streamlit as st

from src.data.objet import Objet
from src.data.programme import Programme
from src.data.indicateurs import *
from src.data.modification import Modification
from src.variables import *


def init_objets(fichier_objets) -> None:
    """
    Récupération des objets
    """
    get_objets_from_sql()
    # Objets en local
    df_objets = pd.read_csv(
        fichier_objets,
        sep=";",
        dtype={
            NOM: str,
            COUT_UNITAIRE: float,
            STD_COUT: float,
            COUT_FIXE: float,
            BONUS_TERRE: float,
            BONUS_MER: float,
            BONUS_RENS: float,
            BONUS_AIR: float,
            MAX_NB_UTILE: int,
            UNITE_PAR_AN: float,
            BUDGET: float,
            DEPENDANCE_EXPORT: str,
            NIVEAU_TECHNO: float,
            ANNEE: int,
            MIN_NB_UTILE: int,
        },
    )
    for _, row in df_objets.iterrows():
        new_objet = Objet(**row.to_dict())
        # Save and send to SQL if new objet
        if row[NOM] not in st.session_state:
            st.session_state[row[NOM]] = new_objet
            new_objet.send_to_sql(st.session_state.sql_client)

def init_programmes(
    fichier_programmes,
) -> None:
    """
    Récupération des objets
    """
    # Programmes SQL
    get_programmes_from_sql()
    # Programmes en local
    df_programmes = pd.read_csv(
        fichier_programmes,
        sep=";",
        dtype={
            NOM: str,
            COUT: float,
            STD_COUT: float,
            BONUS_TERRE: float,
            BONUS_MER: float,
            BONUS_RENS: float,
            BONUS_AIR: float,
            BUDGET: float,
            DEPENDANCE_EXPORT: str,
            NIVEAU_TECHNO: float,
            ANNEE: int,
            DUREE: int,
        },
    )
    for _, row in df_programmes.iterrows():
        new_programme = Programme(**row.to_dict())
        # Save and send to SQL if new objet
        if new_programme.nom not in st.session_state:
            st.session_state[new_programme.nom] = new_programme
            new_programme.send_to_sql(st.session_state.sql_client)

def get_programmes_from_sql() -> None:
    """
    Récupère les objets de l'équipe dans la base SQL
    Si l'objet existe déjà dans le sessin_state, il est écrasé
    """
    df_programmes = st.session_state.sql_client.get_table("Programmes")
    for _, row in df_programmes.iterrows():
        row[NOM] = row[NOM].replace("programme ", "")
        new_programme = Programme(**row.to_dict())
        st.session_state[row[NOM]] = new_programme


def get_objets_from_sql() -> None:
    """
    Récupère les objets de l'équipe dans la base SQL
    Si l'objet existe déjà dans le sessin_state, il est écrasé
    """
    df_objets = st.session_state.sql_client.get_table("Objets")
    for _, row in df_objets.iterrows():
        new_objet = Objet(**row.to_dict())
        st.session_state[row[NOM]] = new_objet


def get_indicateurs_from_sql() -> None:
    """
    Mise à jour ou créations des indicateurs à partir de SQL
    """
    df_indicateurs = st.session_state.sql_client.get_last_value("Indicateurs")
    if df_indicateurs.shape[0] > 0:
        st.session_state["indicateurs"] = Indicateurs(
            **df_indicateurs.iloc[0].to_dict()
        )
    df_armee = st.session_state.sql_client.get_last_value("Armee")
    if df_armee.shape[0] > 0:
        st.session_state["armee"] = Armee(**df_armee.iloc[0].to_dict())

def apply_programmes() -> None:
    """
    Mise à jour des indicateurs à partir des programmes en cours
    """
    # Récupération des programmes en cours dans SQL
    df_programmes = st.session_state.sql_client.get_table("Programmes")
    df_running_programmes = df_programmes[
        (df_programmes[DEBUT] != 0) & (df_programmes[FIN] >= st.session_state.indicateurs.annee)
    ]
    # Application des modifications
    for _, modif_per_year in df_running_programmes.iterrows():
        modif_year_dict = modif_per_year.to_dict()
        # Indicateurs
        nb_years = (
            min(st.session_state.annee, modif_per_year[FIN])
            - st.session_state.indicateurs.annee
        )
        modification_indicateurs = {
            key: nb_years * modif_year_dict.get(key, 0)
            for key in [COUT, NIVEAU_TECHNO, EUROPEANISATION]
        }
        # Armées
        nb_years = (
            min(st.session_state.annee, modif_per_year[FIN])
            - st.session_state.armee.annee
        )
        modification_armee = {
            key: nb_years * modif_year_dict.get(key, 0)
            for key in [BONUS_AIR, BONUS_MER, BONUS_TERRE, BONUS_RENS]
        }
        st.session_state.armee.apply_modification_dict(modification_armee)
        st.session_state.indicateurs.apply_modification_dict(modification_indicateurs)


def apply_constructions() -> None:
    """
    Mise à jour des indicateurs à partir des programmes en cours
    """
    # Récupération des constructions en cours dans SQL
    df_constructions = st.session_state.sql_client.get_table("Constructions")
    df_running_constructions = df_constructions[
        (df_constructions[DEBUT] != 0)
        & (df_constructions[FIN] >= st.session_state.indicateurs.annee)
    ]
    def get_nb(annee, modif):
        nb_years = min(st.session_state.annee, modif[FIN]) - annee
        # Prorata
        if modif[FIN] >= st.session_state.annee:
            nb_unites_ajoutes = nb_years * st.session_state[modif[OBJET]].unite_par_an
        # Gestion des arrondis si la construction est finie
        else:
            nb_unites_construites = (
                max(annee - modif[DEBUT], 0) * st.session_state[modif[OBJET]].unite_par_an
            )
            nb_unites_ajoutes = modif[NOMBRE_UNITE] - nb_unites_construites
        return nb_unites_ajoutes

    # Application des modifications
    for _, modif in df_running_constructions.iterrows():
        objet_dict = st.session_state[modif[OBJET]].to_dict()
        # Indicateurs
        nb_unites_ajoutes = get_nb(st.session_state.indicateurs.annee, modif)
        modification_indicateurs = {
            key: nb_unites_ajoutes * objet_dict.get(key, 0)
            for key in [COUT_UNITAIRE, NIVEAU_TECHNO, EUROPEANISATION]
        }
        # Armées
        nb_unites_ajoutes = get_nb(st.session_state.armee.annee, modif)
        modification_armee = {
            key: nb_unites_ajoutes * objet_dict.get(key, 0)
            for key in [BONUS_AIR, BONUS_MER, BONUS_TERRE, BONUS_RENS]
        }
        # Apply modifications
        st.session_state.armee.apply_modification_dict(modification_armee)
        st.session_state.indicateurs.apply_modification_dict(modification_indicateurs)


def update_indicateurs() -> None:
    """
    Mise à jour des indicateurs
    """
    get_indicateurs_from_sql()
    # Appliquer les programmes et les constructions en cours
    if st.session_state.annee > st.session_state.indicateurs.annee:
        # Application des couts des programmes et des constructions
        apply_programmes()
        apply_constructions()
        # Mise à jour dans SQL
        st.session_state.indicateurs.annee = int(st.session_state.annee)
        st.session_state.indicateurs.send_to_sql(st.session_state.sql_client)
        st.session_state.armee.annee = int(st.session_state.annee)
        st.session_state.armee.send_to_sql(st.session_state.sql_client)

def launch_programme(programme) -> None:
    """
    Lance un programme
    """
    st.session_state[programme].create_start_end(st.session_state.annee)
    st.session_state[programme].send_to_sql(st.session_state.sql_client)

def get_objets_disponibles():
    """
    Récupère les noms des objets disponibles à l'achat
    """
    df_objets = st.session_state.sql_client.get_table("Objets")
    df_objets_disponibles = df_objets[df_objets[ANNEE].astype(int) <= st.session_state.annee]
    return list(df_objets_disponibles[NOM].unique())

def push_etat_to_sql(arborescence, question):
    etat_courant = {
        ARBORESCENCE: arborescence,
        QUESTION: question,
    }
    st.session_state.sql_client.insert_row(table=ETAT, value_dict=etat_courant, replace=True)
