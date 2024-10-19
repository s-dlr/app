"""
Module indicateurs
"""
from dataclasses import dataclass
import re

from src.data.abstract_class import AbstractClass
from src.variables import *

@dataclass
class Indicateurs(AbstractClass):
    """
    Indicateurs macro
    """

    budget: float = 0.0
    europeanisation: float = 0.0
    niveau_techno: float = 10.0
    annee: int = 2000

    @staticmethod
    def get_table():
        return "Indicateurs"

    def update(self, attribute_name: str, increment: T.Union[str, float]) -> None:
        """
        incrémente la valeur d'un attribut de l'objet
        """
        if attribute_name in [COUT_FIXE, COUT_UNITAIRE, COUT]:
            attribute_name = BUDGET
        elif attribute_name in self.__dataclass_fields__.keys():
            current_value = getattr(self, attribute_name)
            setattr(self, attribute_name, current_value + increment)


@dataclass
class Armee(AbstractClass):
    """
    Indicateurs armées
    """

    terre: int = 0
    mer: int = 0
    air: int = 0
    rens: int = 0
    annee: int = 2000

    @staticmethod
    def get_table():
        return "Armee"

    def update(self, attribute_name: str, increment: float):
        """
        incrémente la valeur d'un attribut de l'objet
        """
        armee_to_update = re.findall(r"bonus_([a-zA-Z]*)", attribute_name)
        if len(armee_to_update) != 1:
            return
        armee = armee_to_update[0]
        if armee in self.__dataclass_fields__.keys():
            current_value = getattr(self, armee)
            setattr(self, armee, current_value + increment)
