from dataclasses import dataclass

from src.data.modification import Modification


@dataclass
class Objet:

    nom: str = "default_objet"  # un nom unique par objet
    cout_unitaire: float = 0.0
    std_cout: float = 0.0
    cout_fixe: float = 0.0
    bonus_terre: int = 0
    bonus_mer: int = 0
    bonus_air: int = 0
    bonus_rens: int = 0
    max_nb_utile: int = 0
    unite_par_an: float = 0.0
    budget: float = 0.0
    dependance_export: str = ""  # virgule entre pays
    niveau_techno: float = 0.0

    def to_dict(self):
        return self.__dict__

    def to_str(self):
        return str(self.to_dict())

    def from_str(self, serialized_objet: str = "{}"):
        """
        Crée l'objet depuis sa valeur sérialisée
        """
        self.__init__(*eval(serialized_objet))

    def apply_modification(self, modification: Modification) -> None:
        """
        Applique une modification définie par un objet modification
        """
        self.update_from_dict(modification.to_dict())

    def update(self, attribute_name, increment):
        """
        incrémente la valeur d'un attribut de l'objet
        """
        if attribute_name == "dependance_export":
            self.dependance_export = ",".join([self.dependance_export, increment])
        elif current_value in self.__dataclass_fields__.keys():
            current_value = getattr(self, attribute_name)
            setattr(self, attribute_name, current_value + increment)

    def update_from_dict(self, modification_dict):
        """
        Change les valeurs de l'objet depuis un dict de modification
        Par exemple si le dictionnaire est {'cout_fixe' : +1}, le coût fixe est incrémeté de 1
        """
        for key, value in modification_dict.items():
            self.update(key, value)
