from dataclasses import dataclass
import typing as T

from src.data.modification import Modification
from src.sql_client import ClientSQL

@dataclass
class AbstractClass:
    """
    Classe de donnéee abstraite
    """
    @staticmethod
    def get_table():
        pass

    def to_dict(self) -> dict:
        return self.__dict__

    def apply_modification(self, modification: Modification) -> bool:
        """
        Applique une modification définie par un objet modification
        Renvoie un booléen indiquant si une modification a eu lieu
        """
        modification_dict = modification.to_dict()
        return self.apply_modification_dict(modification_dict)

    def apply_modification_dict(self, modification_dict: dict) -> bool:
        """
        Applique une modification définie par un objet modification
        Renvoie un booléen indiquant si une modification a eu lieu
        """
        if len(modification_dict) == 0:
            return False
        else:
            updated = False
            for key, value in modification_dict.items():
                updated = updated | self.update(key, value)
            return updated

    def update(self, attribute_name: str, increment: T.Union[str, float]) -> bool:
        """
        incrémente la valeur d'un attribut de l'objet
        """
        if attribute_name == "dependance_export":
            self.dependance_export = ",".join([self.dependance_export, increment])
            return True
        elif attribute_name in self.__dataclass_fields__.keys() and increment != 0:
            current_value = getattr(self, attribute_name)
            setattr(self, attribute_name, current_value + increment)
            return True
        return False

    def send_to_sql(self, sql_client: ClientSQL, replace=True) -> None:
        sql_client.insert_row(
            table=self.get_table(),
            value_dict=self.to_dict(),
            replace=replace,
        )
