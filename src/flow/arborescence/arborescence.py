from dataclasses import dataclass

import pandas as pd

from src.flow.arborescence.question import *
from src.variables import *

@dataclass
class Arborescence:
    arborescence: str = "test"

    def __post_init__(self) -> None:
        self.df_arborescence = pd.read_csv(
            ARBORESCENCES[self.arborescence],
            sep=";",
            dtype={
                NUM_QUESTION: int,
                ANNEE: int,
                CONTEXTE_QUESTION: str,
                TEXTE_QUESTION: str,
                IMAGE: str,
                NUMERO_OPTION: str,
                TEXTE_OPTION: str,
                PROCHAINE_QUESTION: int,
                PREREQUIS: str,
                EFFET_IMMEDIAT: str,
                MODIFICATION_OBJET: str,
                MODIFICATION_PROGRAMME: str,
                OBJET: str,
                PROGRAMME: str,
                COMMANDES: str,
            },
        )
        self.arborescence = "Programme test"
        self.df_arborescence.fillna("", inplace=True)
        self.load_data(num_question=1)

    def load_data(self, num_question: int = 1) -> None:
        """
        Instantie l'étape de l'arboarescence correpondant à la question
        """
        data = self.df_arborescence[self.df_arborescence[NUM_QUESTION] == num_question]
        question_data = data.iloc[0][
            [NUM_QUESTION, CONTEXTE_QUESTION, TEXTE_QUESTION, ANNEE, IMAGE]
        ].fillna("")
        option_data = data[
            [
                NUMERO_OPTION,
                TEXTE_OPTION,
                PROCHAINE_QUESTION,
                PREREQUIS,
                EFFET_IMMEDIAT,
                MODIFICATION_OBJET,
                MODIFICATION_PROGRAMME,
                OBJET,
                PROGRAMME,
                COMMANDES,
            ]
        ].fillna("")
        self.question = QuestionOptions(**question_data.to_dict())
        self.question.create_options(option_data)

    def get_next_question(self, select_option: str) -> str:
        return self.question.get_next_question(select_option)
