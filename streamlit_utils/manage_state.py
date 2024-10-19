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


def init_objets(fichier_objets=FICHIERS_OBJETS["Programme exemple"]) -> None:
    """
    Récupération des objets
    """
    # Objets en local
    df_objets = pd.read_csv(
        fichier_objets,
        sep=";",
        dtype={  
            NOM: str,
            COUT_UNITAIRE: float,
            STD_COUT: float,
            COUT_FIXE: float,
            BONUS_TERRE: int,
            BONUS_MER: int,
            BONUS_RENS: int,
            BONUS_AIR: int,
            MAX_NB_UTILE: int,
            UNITE_PAR_AN: float,
            BUDGET: float,
            DEPENDANCE_EXPORT: str,
            NIVEAU_TECHNO: float,
            ANNEE: int,
            DEMANDE_ARMEE: int
        }
    )
    for _, row in df_objets.iterrows():
        new_objet = Objet(**row.to_dict())
        # Save and send to SQL if new objet
        if row[NOM] not in st.session_state:
            st.session_state[row[NOM]] = new_objet
            new_objet.send_to_sql(st.session_state.sql_client)

def init_programmes(
    fichier_programmes=FICHIERS_PROGRAMMES["Programme exemple"],
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
            BONUS_TERRE: int,
            BONUS_MER: int,
            BONUS_RENS: int,
            BONUS_AIR: int,
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
        if "programme " + row[NOM] not in st.session_state:
            st.session_state["programme " + row[NOM]] = new_programme
            new_programme.send_to_sql(st.session_state.sql_client)

def get_programmes_from_sql() -> None:
    """
    Récupère les objets de l'équipe dans la base SQL
    Si l'objet existe déjà dans le sessin_state, il est écrasé
    """
    df_objets = st.session_state.sql_client.get_table("Programmes")
    for _, row in df_objets.iterrows():
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
    df_programmes = st.session_state.sql_client.get_running_rows(
        "Programmes", annee=st.session_state.annee
    )
    # Application des modifications
    for _, modif in df_programmes.iterrows():
        nb_years = st.session_state.annee - st.session_state.indicateurs.annee
        modification_indicateurs = Modification()
        modification_indicateurs.europeanisation = nb_years * modif.get(
            EUROPEANISATION, 0
        )
        modification_indicateurs.niveau_techno = nb_years * modif.get(
            NIVEAU_TECHNO, 0
        )
        nb_years = st.session_state.annee - st.session_state.armee.annee
        modification_armee = Modification()
        modification_armee.bonus_mer = nb_years * modif.get(BONUS_MER, 0)
        modification_armee.bonus_air = nb_years * modif.get(BONUS_AIR, 0)
        modification_armee.bonus_rens = nb_years * modif.get(BONUS_RENS, 0)
        modification_armee.bonus_terre = nb_years * modif.get(BONUS_TERRE, 0)
        st.session_state.armee.apply_modification(modification_armee)
        st.session_state.indicateurs.apply_modification(modification_indicateurs)


def apply_constructions() -> None:
    """
    Mise à jour des indicateurs à partir des programmes en cours
    """
    # Récupération des programmes en cours dans SQL
    df_constructions = st.session_state.sql_client.get_table("Constructions")
    df_constructions_en_cours = df_constructions[
        (df_constructions[DEBUT] <= st.session_state.annee)
        & (df_constructions[FIN] + 1 >= st.session_state.annee)
    ]
    """
    SELECT * FROM `Constructions`
    INNER JOIN (
        SELECT * FROM Objets
        ON Objets.equipe = Constructions.equipe AND Objets.nom = Constructions.objet
    )
    """
    # Application des modifications
    for _, modif in df_constructions_en_cours.iterrows():
        # nb_years = st.session_state.annee - st.session_state.indicateurs.annee
        # modification_indicateurs = Modification()
        # modification_indicateurs.europeanisation = nb_years * modif.get(
        #     EUROPEANISATION, 0
        # )
        # modification_indicateurs.niveau_techno = nb_years * modif.get(NIVEAU_TECHNO, 0)
        # nb_years = st.session_state.annee - st.session_state.armee.annee
        # modification_armee = Modification()
        # modification_armee.bonus_mer = nb_years * modif.get(BONUS_MER, 0)
        # modification_armee.bonus_air = nb_years * modif.get(BONUS_AIR, 0)
        # modification_armee.bonus_rens = nb_years * modif.get(BONUS_RENS, 0)
        # modification_armee.bonus_terre = nb_years * modif.get(BONUS_TERRE, 0)
        # st.session_state.armee.apply_modification(modification_armee)
        # st.session_state.indicateurs.apply_modification(modification_indicateurs)

        # TODO
        pass


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
    df_objets_disponibles = df_objets[df_objets[ANNEE] <= st.session_state.annee]
    return list(df_objets_disponibles[NOM].unique())
