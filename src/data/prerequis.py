"""
Module prérequis
"""

import numpy as np

class Prerequis:
    """
    Permet de modéliser un prérequis
    Les attributs europeanisation et niveau_techno correspodent
    aux seuils minimaux pour que le prérequis soit vérifié
    """

    europeanisation: float = -np.inf
    niveau_techno: float = -np.inf

    def __init__(self, prerequis_str: str = ""):
        for prerequis in prerequis_str.split("\n"):
            if len(prerequis.split(":")) == 2:
                attr, value = prerequis.split(":")
                setattr(self, attr.strip(), float(value.strip()))
