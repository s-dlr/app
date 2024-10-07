import sys

import pandas as pd
import streamlit as st

sys.path.append(".")

from src.sql_client import *
from src.variables import *
from src.flow.arborescence.arborescence import Arborescence
from src.flow.views.options_view import OptionsView
from src.flow.views.buy_view import BuyView
from src.data.objet import MyObjet


def create_objets(arborescence: str) -> None:
    df_objets = pd.read_csv(FICHIER_OBJETS[arborescence], sep=";")
    for _, row in df_objets.iterrows():
        new_objet = MyObjet(**row.to_dict())
        st.session_state[row[NOM]] = new_objet


if __name__ == "__main__":
    # TODO page accueil
    st.session_state["sql_client"] = ClientSQL(
        connection_name="sql", equipe=st.session_state.equipe
    )
    st.session_state["arborescence"] = Arborescence(arborescence="Programme exemple")
    create_objets(arborescence="Programme exemple")

    pages = [
        st.Page("login.py", title="Create your account"),
        st.Page("page_arborescence.py", title="Create your account"),
    ]

    pg = st.navigation(pages)
    pg.run()
