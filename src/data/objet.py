from dataclasses import dataclass

from src.data.abstract_class import AbstractClass


@dataclass
class Objet(AbstractClass):

    nom: str = None  # un nom unique par objet
    cout_unitaire: float = 0.0
    std_cout: float = 0.0
    cout_fixe: float = 0.0
    bonus_terre: int = 0
    bonus_mer: int = 0
    bonus_air: int = 0
    bonus_rens: int = 0
    max_nb_utile: int = 0
    unite_par_an: float = 0.0
    budget: float = 0.0
    dependance_export: str = ""  # virgule entre pays
    niveau_techno: float = 0.0
    annee: int = 2000
    demande_armee: int = 0  # Nombre d'unités demandées par l'EM

    @staticmethod
    def get_table():
        return "Objets"


@dataclass
class Construction(AbstractClass):

    objet: str = None  # un nom unique par objet
    debut: int = 2000
    fin: int = 2000
    nombre_unites: int = 0

    @staticmethod
    def get_table():
        return "Constructions"
