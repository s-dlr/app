from dataclasses import dataclass

from src.data.abstract_class import AbstractClass


@dataclass
class Objet:

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

    @staticmethod
    def get_table():
        return "Objets"
