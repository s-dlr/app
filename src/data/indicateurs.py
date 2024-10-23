"""
Module indicateurs
"""
from dataclasses import dataclass
import re
import typing as T
import streamlit as st

from src.data.abstract_class import AbstractClass
from src.variables import *

@dataclass
class Indicateurs(AbstractClass):
    """
    Indicateurs macro
    """

    budget: float = 0.0
    europeanisation: float = 0.0
    niveau_techno: float = 0.0
    annee: int = 2000

    @staticmethod
    def get_table():
        return "Indicateurs"

    def update(self, attribute_name: str, increment: T.Union[str, float]) -> bool:
        """
        incrémente la valeur d'un attribut de l'objet
        """
        st.success("update " + attribute_name)
        if attribute_name in [COUT_FIXE, COUT_UNITAIRE, COUT]:
            attribute_name = BUDGET
            increment = - increment
        if attribute_name in self.__dataclass_fields__.keys() and increment !=0:
            current_value = getattr(self, attribute_name)
            setattr(self, attribute_name, current_value + increment)
            return True
        return False


@dataclass
class Armee(AbstractClass):
    """
    Indicateurs armées
    """

    terre: float = 0
    mer: float = 0
    air: float = 0
    rens: float = 0
    annee: int = 2000

    @staticmethod
    def get_table():
        return "Armee"

    def update(self, attribute_name: str, increment: float) -> bool:
        """
        incrémente la valeur d'un attribut de l'objet
        """
        armee_to_update = re.findall(r"bonus_([a-zA-Z]*)", attribute_name)
        if len(armee_to_update) != 1:
            return False
        armee = armee_to_update[0]
        if armee in self.__dataclass_fields__.keys() and increment != 0:
            current_value = getattr(self, armee)
            setattr(self, armee, current_value + increment)
            return True
        return False
