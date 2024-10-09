from typing import List

import streamlit as st
from sqlalchemy.sql import text

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

    def get_table(self, table):
        query = f"SELECT * FROM `{table}` WHERE `equipe` = '{self.equipe}'"
        return self.connection.query(query).delete(columns=["equipe"])

    def get_last_value(self, table):
        query = f"SELECT x.* FROM `{table}` x WHERE x.annee = (SELECT MAX(y.annee) FROM `{table}` y) AND x.equipe = '{self.equipe}'"
        return self.connection.query(query).delete(columns=["equipe"])

    def execute_query(self, queries: List[str]):
        with self.connection.session as session:
            for query in queries:
                session.execute(text(query))
            session.commit()

    def delete_row(self, table: str):
        """
        Efface les lignes associées à l'équipe dans la table
        """
        query = f"DELETE FROM `{table}` WHERE equipe = '{self.equipe}'"
        self.execute_query([query])

    def insert_row(self, table: str, value_dict: dict, replace: bool = False):
        """
        Ecrit les indicateurs dans la base SQL
        """
        if replace:
            self.delete_row(table)
        columns_list_str = ", ".join([f"`{k}`" for k in value_dict.keys()])
        values_list_str = ", ".join([f"'{v}'" for v in value_dict.values()])
        query = f"INSERT INTO `{table}`(`equipe`, {columns_list_str}) VALUES ('{self.equipe}', {values_list_str})"
        self.execute_query([query])

    def update_sql_objet(self, objet: Objet) -> None:
        """
        Efface la ligne correspondant à l'ancien objet dans la base SQL (si elle existe)
        Ajoute le nouvel objet
        """
        # delete old objet
        # add new objet
        pass
