from dataclasses import dataclass

import pandas as pd

from src.flow.arborescence.option import Option
from src.variables import *

@dataclass
class AbstractQuestion:
    contexte_question: str
    num_question: int
    texte_question: str

@dataclass
class QuestionAchat(AbstractQuestion):
    objet: str
    min_nb_unit: int = 0
    max_nb_unit: int = 1
    prochaine_question: int = 0

@dataclass
class QuestionOptions(AbstractQuestion):
    contexte_question: str
    num_question: str
    texte_question: str

    def create_options(self, options_df: pd.DataFrame):
        self.options = []
        for _, option_data in options_df.iterrows():
            option = Option(**option_data.to_dict())
            if option.check_prerequis():
                # TODO récupérer les seuils via l'API
                self.options.append(option)

    def get_option_by_text(self, texte_option: str) -> Option:
        for opt in self.options:
            if opt.texte_option == texte_option:
                return opt

    def get_next_question(self, texte_option: str) -> Option:
        return self.get_option_by_text(texte_option).prochaine_question
