import sys

import pandas as pd
import streamlit as st

sys.path.append(".")

from src.sql_client import *
from src.variables import *
from src.flow.arborescence.arborescence import Arborescence
from src.data.objet import Objet

def start_game():
    st.session_state["sql_client"] = ClientSQL(
        connection_name="sql", equipe=st.session_state.equipe
    )
    st.session_state["arborescence"] = Arborescence(arborescence="Programme exemple")
    create_objets()
    # st.switch_page("pages/page_arborescence.py")


def create_objets() -> None:
    df_objets = pd.read_csv(FICHIER_OBJETS, sep=";")
    for _, row in df_objets.iterrows():
        new_objet = Objet(**row.to_dict())
        st.session_state[row[NOM]] = new_objet


# page_dict = [
#     st.Page("pages/page_arborescence.py"),
#     st.Page("pages/page_arborescence.py"),
# ]
# pg = st.navigation(page_dict, position="hidden")
# pg.run()

if "equipe" not in st.session_state:
    st.switch_page("pages/page_login.py")
else:
    st.switch_page("pages/page_arborescence.py")

start_game()
#     page_dict.append(st.Page("streamlit_pages/page_arborescence.py"))
#     pg = st.navigation(page_dict)
# pg.run()
