"""
Module modification (d'un programme, d'un objet ou des compteurs de l'équipe)
"""


class Modification:
    """
    Modifications possibles
    
    cout_unitaire: float = 0.0
    std_cout: float = 0.0
    cout_fixe: float = 0.0
    cout: float = 0.0
    bonus_terre: int = 0
    bonus_mer: int = 0
    bonus_air: int = 0
    bonus_rens: int = 0
    max_nb_utile: int = 0
    unite_par_an: float = 0.0
    budget: float = 0.0
    dependance_export: str = ""
    europeanisation: float = 0.0
    niveau_techno: float = 0.0
    duree: int = 0
    """
    def __init__(self, modification_str: str = ""):
        for modification in modification_str.split("\n"):
            if len(modification.split(":")) == 2:
                attr, value = modification.split(":")
                setattr(self, attr.strip(), float(value))

    def to_dict(self):
        return self.__dict__
