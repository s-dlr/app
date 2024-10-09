import streamlit as st

from src.data.objet import Objet
from src.data.indicateurs import *

class ClientSQL:

    def __init__(self, connection_name: str, equipe: str) -> None:
        # TODO
        self.connection = st.connection(connection_name, autocommit=False)
        self.equipe = equipe

    def get_objet(self, objet: str):
        """
        Récupère un objet à partir de son nom dans la base sql
        """
        # requete SQL
        # Objet depuis la requete
        return Objet(objet)

    def insert_row(self, table: str, value_dict: dict):
        """
        Ecrit les indicateurs dans la base SQL
        """
        columns_list_str = ", ".join([f"`{k}`" for k in value_dict.keys()])
        values_list_str = ", ".join([f"'{v}'" for v in value_dict.values()])
        query = f"INSERT INTO `{table}`(`equipe`, {columns_list_str}) VALUES ('{self.equipe}', {values_list_str})"
        with self.connection.session as session:
            session.execute(str(query))
            session.commit()

    def update_sql_objet(self, objet: Objet) -> None:
        """
        Efface la ligne correspondant à l'ancien objet dans la base SQL (si elle existe)
        Ajoute le nouvel objet
        """
        # delete old objet
        # add new objet
        pass
