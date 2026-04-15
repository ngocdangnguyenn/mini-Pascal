from enum import Enum

class TokenType(Enum):
    MOTCLE = "motcle"
    IDENT = "ident"
    ENT = "ent"
    CH = "ch"
    VIRG = "virg"
    PTVIRG = "ptvirg"
    POINT = "point"
    DEUXPTS = "deuxpts"
    PAROUV = "parouv"
    PARFER = "parfer"
    INF = "inf"
    SUP = "sup"
    EG = "eg"
    PLUS = "plus"
    MOINS = "moins"
    MULT = "mult"
    DIVI = "divi"
    INFE = "infe"
    SUPE = "supe"
    DIFF = "diff"
    AFF = "aff"

class Token:
    def __init__(self, type, valeur=None):
        self.type = type
        self.valeur = valeur
    
    def __str__(self):
        if self.valeur is not None:
            return f"{self.type.value}: {self.valeur}"
        return self.type.value

LONG_MAX_IDENT = 20
LONG_MAX_CHAINE = 50
NB_MOTS_RESERVES = 14
MAXINT = 32767
