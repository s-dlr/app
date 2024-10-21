from typing import List
import pandas as pd

import streamlit as st
from sqlalchemy.sql import text


class ClientSQL:

    def __init__(self, connection_name: str, equipe: str) -> None:
        self.connection = st.connection(connection_name, autocommit=True, ttl=1)
        self.equipe = equipe

    def check_team_exists(self):
        """
        Teste si une équipe existe déjà dans la base SQL
        """
        return self.get_table("Etat").shape[0] > 0

    def get_table(self, table):
        query = f'SELECT * FROM `{table}` WHERE `equipe` = "{self.equipe}";'
        df_results = self.connection.query(query, ttl=1)
        return df_results.drop(columns="equipe")

    def get_custom_query(self, query, ttl=1):
        df_results = self.connection.query(query, ttl=ttl)
        return df_results.drop(columns="equipe")

    def get_running_rows(self, table, min_annee: int, max_annee: int) -> pd.DataFrame:
        """
        Récupération des lignes en cours
        """
        query = f'SELECT * FROM `{table}` WHERE `equipe` = "{self.equipe}" AND `debut` >= {max_annee} AND `fin` >= {min_annee-1};'
        return self.connection.query(query, ttl=1).drop(columns="equipe")

    def get_last_value(self, table):
        """
        Récupère la valeur la plus à jour d'une table (date la plus récente)
        """
        query_max_annee = (
            f'SELECT MAX(y.annee) FROM `{table}` y WHERE y.equipe = "{self.equipe}"'
        )
        query = f'SELECT x.* FROM `{table}` x WHERE x.annee = ({query_max_annee}) AND x.equipe = "{self.equipe}";'
        return self.connection.query(query, ttl=1).drop(columns="equipe")

    def execute_query(self, queries: List[str]):
        with self.connection.session as session:
            for query in queries:
                session.execute(text(query))
            session.commit()

    def delete_row(self, table: str):
        """
        Efface les lignes associées à l'équipe dans la table
        """
        query = f'DELETE FROM `{table}` WHERE equipe = "{self.equipe}";'
        self.execute_query([query])

    def insert_row(self, table: str, value_dict: dict, replace: bool = True):
        """
        Ecrit les indicateurs dans la base SQL
        """
        if replace:
            command = "REPLACE"
        else:
            command = "INSERT"
        columns_list_str = ", ".join([f"`{k}`" for k in value_dict.keys()])
        values_list_str = ", ".join([f'"{v}"' for v in value_dict.values()])
        query = f'{command} INTO `{table}`(`equipe`, {columns_list_str}) VALUES ("{self.equipe}", {values_list_str});'
        self.execute_query([query])
