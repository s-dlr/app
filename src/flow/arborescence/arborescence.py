from dataclasses import dataclass

import pandas as pd

from src.flow.arborescence.question import *
from src.variables import *

@dataclass
class Arborescence:
    arborescence: str

    def __post_init__(self) -> None:
        self.df_arborescence = pd.read_csv(ARBORESCENCES[self.arborescence], sep=";")
        self.load_data(num_question=1)

    def load_data(self, num_question: int = 1) -> None:
        """
        Instantie l'étape de l'arboarescence correpondant à la question
        """
        data = self.df_arborescence[self.df_arborescence[NUM_QUESTION] == num_question]
        question_data = data.iloc[0][[NUM_QUESTION, CONTEXTE_QUESTION, TEXTE_QUESTION]]
        if data.iloc[0][NUMERO_OPTION] == NOMBRE_UNITE:
            option_data = data.iloc[0]
            self.question = QuestionAchat(
                contexte_question=question_data[CONTEXTE_QUESTION],
                num_question=question_data[NUM_QUESTION],
                texte_question=question_data[TEXTE_QUESTION],
                objet=option_data[OBJET],
                min_nb_unit=int(option_data[TEXTE_OPTION].split("a")[0]),
                max_nb_unit=int(option_data[TEXTE_OPTION].split("a")[1]),
                prochaine_question=int(option_data[PROCHAINE_QUESTION]),
            )
            self.type_question = CHOIX_NOMBRE_UNITE
        else:
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
                ]
            ].fillna("")
            self.question = QuestionOptions(**question_data.to_dict())
            self.question.create_options(option_data)
            self.type_question = CHOIX_OPTION

    def get_next_question(self) -> str:
        if self.type_question == CHOIX_OPTION:
            num_next_question = self.question.prochaine_question
        else:
            num_next_question = self.question.get_next_question(st.session_state.option)

    def get_next_question_type(self) -> str:
        next_question = self.get_next_question_type()
        data = self.df_arborescence[self.df_arborescence[NUM_QUESTION] == next_question]
        if data.iloc[0][NUMERO_OPTION] == NOMBRE_UNITE:
            return CHOIX_NOMBRE_UNITE
        else:
            return CHOIX_OPTION
