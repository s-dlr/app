"""
Module décrivant un choix d'achat
"""

from dataclasses import dataclass


@dataclass
class NumberUnits:

    objet: str
    min_nb_unit: int = 0
    max_nb_unit: int = 1
