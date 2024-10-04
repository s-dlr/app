"""
Module prérequis
"""

import json


class Prerequis:
    """
    Permet de modéliser un prérequis
    Les attributs europeanisation et niveau_techno correspodent
    aux seuils minimaux pour que le prérequi soit vérifié
    """

    europeanisation: float = 0.0
    niveau_techno: float = 0.0

    def __init__(self, prerequis_str: str = ""):
        for prerequis in prerequis_str.split("\n"):
            if len(prerequis.split(":")) == 2:
                attr, value = prerequis.split(":")
                setattr(self, attr.strip(), float(value.strip()))

    def to_str(self):
        return json.dumps(self.__dict__)
