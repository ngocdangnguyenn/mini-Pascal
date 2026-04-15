from src.token import LONG_MAX_IDENT

class T_IDENT:
    VARIABLE = "variable"
    CONSTANTE = "constante"
    PROGRAMME = "programme"
    FONCTION = "fonction"
    PARAMETRE = "parametre"

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
        elif typ == T_IDENT.FONCTION:
            self.nb_params = 0
            self.adresse = 0
        elif typ == T_IDENT.PARAMETRE:
            self.adrv = None

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

def SUPPRIMER(nom):
    h = FONCTION_HACHAGE(nom)
    courant = TABLE_HACHAGE[h]
    precedent = None
    while courant is not None:
        if TABLE_IDENT[courant.indice].nom == nom:
            if precedent is None:
                TABLE_HACHAGE[h] = courant.suivant
            else:
                precedent.suivant = courant.suivant
            return
        precedent = courant
        courant = courant.suivant

def AFFICHE_TABLE_IDENT():
    import src.parser as _parser
    val_chaines = _parser.VAL_DE_CONST_CHAINE
    print("\n" + "=" * 62)
    print("TABLE DES IDENTIFICATEURS")
    print("=" * 62)
    print(f"  {'#':<4} {'Nom':<16} {'Genre':<12} Détail")
    print("-" * 62)
    for i in range(NB_IDENT):
        enreg = TABLE_IDENT[i]
        if enreg is None:
            continue
        if enreg.typ == T_IDENT.VARIABLE:
            detail = f"adrv = {enreg.adrv}"
        elif enreg.typ == T_IDENT.CONSTANTE:
            if enreg.typc == 0:
                detail = f"entier, val = {enreg.val}"
            else:
                s = val_chaines[enreg.val - 1] if enreg.val <= len(val_chaines) else f"chaine#{enreg.val}"
                detail = f"chaine, val = '{s}'"
        elif enreg.typ == T_IDENT.FONCTION:
            detail = f"nb_params = {enreg.nb_params}, adresse = {enreg.adresse}"
        elif enreg.typ == T_IDENT.PARAMETRE:
            detail = f"adrv = {enreg.adrv}  (position dans le cadre)"
        else:
            detail = ""
        print(f"  [{i}] {enreg.nom:<16} {enreg.typ:<12} {detail}")
    print("=" * 62)
    print(f"Total : {NB_IDENT} identificateur(s)")

def REINITIALISER_TABLE():
    global NB_IDENT, TABLE_IDENT, TABLE_HACHAGE
    NB_IDENT = 0
    TABLE_IDENT = [None] * NB_IDENT_MAX
    TABLE_HACHAGE = [None] * TAILLE_TABLE_HACHAGE
