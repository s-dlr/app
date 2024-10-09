"""
Module indicateurs
"""
from dataclasses import dataclass

@dataclass
class Indicateurs:
    """
    Indicateurs macro
    """

    budget: float = 0.0
    europeanisation: float = 0.0
    niveau_techno: float = 0.0

    def to_dict(self):
        return self.__dict__

    def to_str(self):
        return str(self.to_dict())

@dataclass
class Armee:
    """
    Indicateurs armées
    """

    bonus_terre: int = 0
    bonus_mer: int = 0
    bonus_air: int = 0
    bonus_rens: int = 0

    def to_dict(self):
        return self.__dict__

    def to_str(self):
        return str(self.to_dict())
