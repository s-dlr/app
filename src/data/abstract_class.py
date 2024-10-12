from dataclasses import dataclass

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

    def to_dict(self):
        return self.__dict__

    def apply_modification(self, modification: Modification) -> None:
        """
        Applique une modification définie par un objet modification
        Renvoie un booléen indiquant si une modification a eu lieu
        """
        modification_dict = modification.to_dict()
        if len(modification_dict) == 0:
            return False
        else:    
            for key, value in modification_dict.items():
                self.update(key, value)
            return True

    def update(self, attribute_name, increment):
        """
        incrémente la valeur d'un attribut de l'objet
        """
        if attribute_name == "dependance_export":
            self.dependance_export = ",".join([self.dependance_export, increment])
        elif attribute_name in self.__dataclass_fields__.keys():
            current_value = getattr(self, attribute_name)
            setattr(self, attribute_name, current_value + increment)

    def send_to_sql(self, sql_client: ClientSQL, replace=True):
        sql_client.insert_row(
            table=self.get_table(),
            value_dict=self.to_dict(),
            replace=replace,
        )