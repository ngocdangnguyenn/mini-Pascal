from src.token import Token, TokenType, LONG_MAX_IDENT, LONG_MAX_CHAINE, MAXINT

SOURCE = None
CARLU = ''
NUM_LIGNE = 1
NOMBRE = 0
CHAINE = ""
TABLE_MOTS_RESERVES = []
MESSAGE_ERREUR = ""

def ERREUR(num):
    global MESSAGE_ERREUR
    
    messages = {
        1: "Fin de fichier atteinte",
        2: f"Nombre entier trop grand (maximum: {MAXINT})",
        3: f"Chaine de caracteres trop longue (maximum: {LONG_MAX_CHAINE} caracteres)",
        4: "Symbole non reconnu"
    }
    if num == 3 and MESSAGE_ERREUR:
        print(f"Ligne {NUM_LIGNE}: {MESSAGE_ERREUR}")
    else:
        print(f"Erreur {num} a la ligne {NUM_LIGNE}: {messages.get(num, 'Erreur inconnue')}")
    exit(1)

def LIRE_CAR():
    global CARLU, NUM_LIGNE
    CARLU = SOURCE.read(1)
    if CARLU == '':
        ERREUR(1)
    if CARLU == '\n':
        NUM_LIGNE += 1

def SAUTER_SEPARATEURS():
    global CARLU
    while True : 
        if CARLU.isspace():
            LIRE_CAR()
        elif CARLU == '{':
            LIRE_CAR()
            niveau = 1
            while niveau > 0:
                if CARLU == '{':
                    niveau += 1
                elif CARLU == '}':
                    niveau -= 1
                LIRE_CAR()
        else:
            break

def RECO_ENTIER():
    global CARLU, NOMBRE
    NOMBRE = 0
    while CARLU.isdigit():
        NOMBRE = NOMBRE * 10 + int(CARLU)
        if NOMBRE > MAXINT:
            ERREUR(2)
        LIRE_CAR()
    return TokenType.ENT

def RECO_CHAINE():
    global CARLU, CHAINE
    CHAINE = ""
    LIRE_CAR()
    while True:
        if len(CHAINE) >= LONG_MAX_CHAINE:
            ERREUR(3)
        if CARLU == "'":
            LIRE_CAR()
            if CARLU == "'":
                CHAINE += "'"
                LIRE_CAR()
            else:
                break
        else:
            CHAINE += CARLU
            LIRE_CAR()
    return TokenType.CH

def RECO_IDENT_OU_MOT_RESERVE():
    global CARLU, CHAINE
    CHAINE = ""
    longueur = 0
    while CARLU.isalnum() or CARLU == '_':
        if longueur < LONG_MAX_IDENT:
            CHAINE += CARLU.upper()
            longueur += 1
        LIRE_CAR()
    if EST_UN_MOT_RESERVE():
        return TokenType.MOTCLE
    return TokenType.IDENT

def EST_UN_MOT_RESERVE():
    global CHAINE
    i = 0
    j = len(TABLE_MOTS_RESERVES) - 1
    while i <= j:
        k = (i + j) // 2
        if CHAINE < TABLE_MOTS_RESERVES[k]:
            j = k - 1
        elif CHAINE > TABLE_MOTS_RESERVES[k]:
            i = k + 1
        else:
            return True
    return False

def RECO_SYMB():
    global CARLU
    if CARLU == ';':
        LIRE_CAR()
        return TokenType.PTVIRG
    elif CARLU == '.':
        return TokenType.POINT
    elif CARLU == '(':
        LIRE_CAR()
        return TokenType.PAROUV
    elif CARLU == ')':
        LIRE_CAR()
        return TokenType.PARFER
    elif CARLU == '+':
        LIRE_CAR()
        return TokenType.PLUS
    elif CARLU == '-':
        LIRE_CAR()
        return TokenType.MOINS
    elif CARLU == '*':
        LIRE_CAR()
        return TokenType.MULT
    elif CARLU == '/':
        LIRE_CAR()
        return TokenType.DIVI
    elif CARLU == ',':
        LIRE_CAR()
        return TokenType.VIRG
    elif CARLU == '<':
        LIRE_CAR()
        if CARLU == '=':
            LIRE_CAR()
            return TokenType.INFE
        elif CARLU == '>':
            LIRE_CAR()
            return TokenType.DIFF
        else:
            return TokenType.INF
    elif CARLU == '>':
        LIRE_CAR()
        if CARLU == '=':
            LIRE_CAR()
            return TokenType.SUPE
        else:
            return TokenType.SUP
    elif CARLU == '=':
        LIRE_CAR()
        return TokenType.EG
    elif CARLU == ':':
        LIRE_CAR()
        if CARLU == '=':
            LIRE_CAR()
            return TokenType.AFF
        else:
            return TokenType.DEUXPTS
    else:
        ERREUR(4)

def ANALEX():
    global CARLU
    SAUTER_SEPARATEURS()
    if CARLU == '':
        return None
    elif CARLU.isdigit():
        return RECO_ENTIER()
    elif CARLU == "'":
        return RECO_CHAINE()
    elif CARLU.isalpha():
        return RECO_IDENT_OU_MOT_RESERVE()
    else:
        return RECO_SYMB()

def INITIALISER(nom):
    global SOURCE, NUM_LIGNE, TABLE_MOTS_RESERVES, CHAINE, NOMBRE, CARLU, MESSAGE_ERREUR
    SOURCE = open(nom, 'r', encoding='utf-8')
    NUM_LIGNE = 1
    CHAINE = ""
    NOMBRE = 0
    CARLU = ''
    MESSAGE_ERREUR = ""
    TABLE_MOTS_RESERVES = [
        "ALORS", "CONST", "DEBUT", "ECRIRE", "ENTIER",
        "FAIRE", "FIN", "FONCTION",
        "LIRE", "PROGRAMME", "SI", "SINON", "TANTQUE", "VAR"
    ]
    LIRE_CAR()

def TERMINER():
    global SOURCE
    if SOURCE:
        SOURCE.close()
        SOURCE = None