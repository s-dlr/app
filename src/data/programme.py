from dataclasses import dataclass

from src.data.abstract_class import AbstractClass


@dataclass
class Programme(AbstractClass):

    nom: str = "default_objet"  # un nom unique par objet
    cout: float = 0.0
    std_cout: float = 0.0
    bonus_terre: float = 0
    bonus_mer: float = 0
    bonus_air: float = 0
    bonus_rens: float = 0
    budget: float = 0.0
    dependance_export: str = ""  # virgule entre pays
    niveau_techno: float = 0.0
    duree: int = 1
    debut: int = 0 # intialisés au lancement
    fin: int = 0 # initialisés au lancement

    def __post_init__(self):
        self.nom = "programme " + self.nom

    @staticmethod
    def get_table():
        return "Programmes"

    def create_start_end(self, start_date):
        """
        Crée les attributs début et fin à partir d'une année de départ
        """
        self.debut = start_date
        self.fin = start_date + self.duree - 1
