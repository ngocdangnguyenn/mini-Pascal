from src.token import LONG_MAX_IDENT

class T_IDENT:
    VARIABLE = "variable"
    CONSTANTE = "constante"
    PROGRAMME = "programme"

class T_ENREG_IDENT:
    def __init__(self, nom, typ):
        self.nom = nom
        self.typ = typ
        if typ == T_IDENT.VARIABLE:
            self.typv = None
            self.adrv = None
        elif typ == T_IDENT.CONSTANTE:
            self.typc = None
            self.val = None

NB_IDENT_MAX = 100
TAILLE_TABLE_HACHAGE = 211

TABLE_IDENT = [None] * NB_IDENT_MAX
TABLE_HACHAGE = [None] * TAILLE_TABLE_HACHAGE
NB_IDENT = 0

class Noeud:
    def __init__(self, indice):
        self.indice = indice
        self.suivant = None

def FONCTION_HACHAGE(nom):
    p = 0
    alpha = 31
    for c in nom:
        p = alpha * p + ord(c)
    return p % TAILLE_TABLE_HACHAGE

def CHERCHER(nom):
    h = FONCTION_HACHAGE(nom)
    courant = TABLE_HACHAGE[h]
    
    while courant is not None:
        if TABLE_IDENT[courant.indice].nom == nom:
            return courant.indice
        courant = courant.suivant
    
    return -1

def INSERER(nom, genre):
    global NB_IDENT
    
    if NB_IDENT >= NB_IDENT_MAX:
        print(f"Erreur: Table des identificateurs pleine (maximum: {NB_IDENT_MAX})")
        exit(1)
    
    indice = CHERCHER(nom)
    if indice != -1:
        return indice
    
    nouvel_enreg = T_ENREG_IDENT(nom, genre)
    TABLE_IDENT[NB_IDENT] = nouvel_enreg
    indice = NB_IDENT
    NB_IDENT += 1
    
    h = FONCTION_HACHAGE(nom)
    nouveau_noeud = Noeud(indice)
    nouveau_noeud.suivant = TABLE_HACHAGE[h]
    TABLE_HACHAGE[h] = nouveau_noeud
    
    return indice

def AFFICHE_TABLE_IDENT():
    print("\n" + "=" * 80)
    print("TABLE DES IDENTIFICATEURS")
    print("=" * 80)
    print(f"| {'Indice':<8} | {'Nom':<20} | {'Genre':<15} | {'Hash':<8} |")
    print("=" * 80)
    
    for i in range(NB_IDENT):
        if TABLE_IDENT[i] is not None:
            enreg = TABLE_IDENT[i]
            h = FONCTION_HACHAGE(enreg.nom)
            print(f"| {i:<8} | {enreg.nom:<20} | {enreg.typ:<15} | {h:<8} |")
    
    print("=" * 80)
    print(f"Total: {NB_IDENT} identificateurs\n")

def REINITIALISER_TABLE():
    global NB_IDENT, TABLE_IDENT, TABLE_HACHAGE
    NB_IDENT = 0
    TABLE_IDENT = [None] * NB_IDENT_MAX
    TABLE_HACHAGE = [None] * TAILLE_TABLE_HACHAGE
