from src.data.objet import Objet


class ClientSQL:

    def __init__(self, connection_name: str, equipe: str) -> None:
        # TODO
        # self.connection = st.connection(connection_name)
        self.equipe = equipe

    def get_objet(self, objet: str):
        """
        Récupère un objet à partir de son nom dans la base sql
        """
        # requete SQL
        # Objet depuis la requete
        return Objet(objet)

    def update_sql_objet(self, objet: Objet) -> None:
        """
        Efface la ligne correspondant à l'ancien objet dans la base SQL (si elle existe)
        Ajoute le nouvel objet
        """
        # delete old objet
        # add new objet
        pass
