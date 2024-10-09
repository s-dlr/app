DATA_DIR = "src/flow/files"

EQUIPE = "equipe"

# Colonnes arborescence
NUM_QUESTION = "num_question"
ANNEE = "annee" 
CONTEXTE_QUESTION = "contexte_question"
TEXTE_QUESTION = "texte_question"
NUMERO_OPTION = "numero_option"
TEXTE_OPTION = "texte_option"
PROCHAINE_QUESTION = "prochaine_question"
PREREQUIS = "prerequis"
EFFET_IMMEDIAT = "effet_immediat"
MODIFICATION_OBJET = "modification_objet"
MODIFICATION_PROGRAMME = "modification_programme"
OBJET = "objet"  # objet concerné par l'option. Un des objet de l'arbrescence

# Attributs objets
NOM = "nom"
COUT_UNITAIRE = "cout_unitaire"
STD_COUT = "std_cout"
COUT_FIXE = "cout_fixe"
BONUS_TERRE = "bonus_terre"
BONUS_MER = "bonus_mer"
BONUS_AIR = "bonus_air"
BONUS_RENS = "bonus_rens"
MAX_NB_UTILE = "max_nb_utile"
UNITE_PAR_AN = "unite_par_an"
DEPENDANCE_EXPORT = "dependance_export"

# Compteurs
EUROPEANISATION = "europeanisation"
BUDGET = "budget"
NIVEAU_TECHNO = "niveau_techno"

# Variable
NOMBRE_UNITE = "nombre_unites"

# Types de question
CHOIX_OPTION = "choix_option"
CHOIX_NOMBRE_UNITE = "choix_nombre_unites"

# Arborescences
ARBORESCENCES = {
    "Programme exemple": f"{DATA_DIR}/arborescence_exemple/arborescence.csv"
}
FICHIER_OBJETS = f"{DATA_DIR}/arborescence_exemple/objets.csv"
