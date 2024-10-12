"""
Module indicateurs
"""
from dataclasses import dataclass
import re

from src.data.abstract_class import AbstractClass

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
        if armee_to_update in self.__dataclass_fields__.keys():
            current_value = getattr(self, armee_to_update)
            setattr(self, armee_to_update, current_value + increment)
