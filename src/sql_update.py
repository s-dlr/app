import pandas as pd
import streamlit as st

from src.data.object import MyObject


def update_sql_object(conn: st.connection, object: MyObject) -> None:
    """
    Efface la ligne correspondant à l'ancien objet dans la base SQL (si elle existe)
    Ajoute le nouvel objet
    """
    # delete old object
    # add new object
    pass
