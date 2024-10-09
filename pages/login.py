import pandas as pd
import streamlit as st

from src.data.indicateurs import *
from src.data.objet import Objet
from src.variables import *
from src.sql_client import ClientSQL
from src.flow.navigation import *

def init_session_state() -> None:
    # Objets
    df_objets = pd.read_csv(FICHIER_OBJETS, sep=";")
    for _, row in df_objets.iterrows():
        new_objet = Objet(**row.to_dict())
        st.session_state[row[NOM]] = new_objet
    # Indicateurs initiaux
    st.session_state["indicateurs"] = Indicateurs()
    st.session_state["armee"] = Armee()


def init_team_in_db() -> None:
    """
    Créatoin de l'équipe dans la base de données
    """
    st.session_state["sql_client"] = ClientSQL(
        connection_name="astrolabedb", equipe=st.session_state.equipe
    )
    # Push indicateurs to SQL
    st.session_state.sql_client.insert_row(
        table="Indicateurs",
        value_dict=st.session_state.indicateurs.to_dict(),
        replace=True,
    )
    st.session_state.sql_client.insert_row(
        table="Armee", value_dict=st.session_state.armee.to_dict(), replace=True
    )

st.set_page_config(
    page_title="Login",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialisation objets et arborescence
init_session_state()

# Affichage
st.header("Choix du nom de l'équipe")
team = st.text_input("équipe", "astrolabe")
if st.button("Log in"):
    st.session_state["equipe"] = team
    init_team_in_db()
    go_to_next_question()
