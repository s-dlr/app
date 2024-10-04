"""
Module option
"""

from dataclasses import dataclass

import streamlit as st

from src.data.prerequis import Prerequis
from src.data.modification import Modification


class Option:
    """
    La classe option modélise un choix possible de l'arborescence.

    Args:
        numero_option: Numéro de l'option
        texte_option: Texte décrivant l'option
        prochaine_question: Numéro de la priochaine question
        prerequis: Prérequis pour que l'option soit disponible
        effet_immediat: Effet immédiat de l'option. \
            Cette modification est immédiatement appliquée aux compteurs de l'équipe
        modification_objet: Modification de l'objet \
            Cette modification est appliquée à l'objet concerné par l'option
        modification_programme: Modification de l'objet \
            Cette modification est appliquée au programme courant de l'arborescence
        objet: Nom de l'objet concerné par l'option
    """

    def __init__(
        self,
        numero_option: str,
        texte_option: str,
        prochaine_question: int,
        prerequis: str,
        effet_immediat: str,
        modification_objet: str,
        modification_programme: str,
        objet: str,
    ):
        self.numero_option = numero_option
        self.texte_option = texte_option
        self.prochaine_question = prochaine_question
        self.objet = objet
        self.prerequis = Prerequis(prerequis)
        self.modification_objet = Modification(modification_objet)
        self.modification_programme = Modification(modification_programme)
        self.effet_immediat = Modification(effet_immediat)

    def check_prerequis(self, europeanisation: float = 0., niveau_techno: float = 0.):
        """
        Vérifie si les niveaux d'auropéanisation et de technologie du pays \
        permettent d'accéder à l'option
        """
        # return (self.prerequis.europeanisation <= europeanisation) and (
        #     self.prerequis.niveau_techno <= niveau_techno
        # )
        return True
