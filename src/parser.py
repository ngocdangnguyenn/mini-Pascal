from src.token import TokenType
import src.lexer as lexer
from src.table_ident import CHERCHER, INSERER, T_IDENT, TABLE_IDENT
import src.machine as machine

UNILEX = None
NB_CONST_CHAINE = 0
VAL_DE_CONST_CHAINE = []
DERNIERE_ADRESSE_VAR_GLOB = -1

def ANASYNT():
    global UNILEX
    UNILEX = lexer.ANALEX()
    if PROG():
        print("Le programme source est syntaxiquement correct.")
    else:
        lexer.ERREUR(3)

def PROG():
    global UNILEX
    if (UNILEX == TokenType.MOTCLE) and (lexer.CHAINE == 'PROGRAMME'):
        UNILEX = lexer.ANALEX()
        if UNILEX == TokenType.IDENT:
            UNILEX = lexer.ANALEX()
            if UNILEX == TokenType.PTVIRG:
                UNILEX = lexer.ANALEX()
                if (UNILEX == TokenType.MOTCLE) and (lexer.CHAINE == 'CONST'):
                    if not DECL_CONST():
                        return False
                if (UNILEX == TokenType.MOTCLE) and (lexer.CHAINE == 'VAR'):
                    if not DECL_VAR():
                        return False
                if BLOC():
                    machine.P_CODE[machine.CO] = machine.STOP
                    machine.CO += 1
                    if UNILEX == TokenType.POINT:
                        UNILEX = lexer.ANALEX()
                        return True
                    else:
                        lexer.MESSAGE_ERREUR = f"Attendu '.', trouvé {lexer.CHAINE if lexer.CHAINE else 'EOF'}"
                        lexer.ERREUR(3)
                else:
                    return False
            else:
                lexer.MESSAGE_ERREUR = f"Attendu ';' après nom du programme, trouvé {lexer.CHAINE if lexer.CHAINE else 'EOF'}"
                lexer.ERREUR(3)
        else:
            lexer.MESSAGE_ERREUR = f"Attendu nom du programme après PROGRAMME, trouvé {lexer.CHAINE if lexer.CHAINE else 'EOF'}"
            lexer.ERREUR(3)
    else:
        lexer.MESSAGE_ERREUR = "Programme doit commencer par 'PROGRAMME'"
        lexer.ERREUR(3)
    return False
                
def DEFINIR_CONSTANTE(nom, ul):
    global NB_CONST_CHAINE, VAL_DE_CONST_CHAINE
    if CHERCHER(nom) != -1:
        return False
    indice = INSERER(nom, T_IDENT.CONSTANTE)
    if ul == TokenType.ENT:
        TABLE_IDENT[indice].typc = 0
        TABLE_IDENT[indice].val = lexer.NOMBRE
    else:
        TABLE_IDENT[indice].typc = 1
        NB_CONST_CHAINE += 1
        VAL_DE_CONST_CHAINE.append(lexer.CHAINE)
        TABLE_IDENT[indice].val = NB_CONST_CHAINE
    return True

def DECL_CONST():
    global UNILEX, NB_CONST_CHAINE, VAL_DE_CONST_CHAINE
    if (UNILEX == TokenType.MOTCLE) and (lexer.CHAINE == 'CONST'):
        UNILEX = lexer.ANALEX()
        if UNILEX == TokenType.IDENT:
            nom_constante = lexer.CHAINE
            UNILEX = lexer.ANALEX()
            if UNILEX == TokenType.EG:
                UNILEX = lexer.ANALEX()
                if (UNILEX == TokenType.ENT) or (UNILEX == TokenType.CH):
                    if DEFINIR_CONSTANTE(nom_constante, UNILEX):
                        UNILEX = lexer.ANALEX()
                        non_fin = True
                        while non_fin:
                            if UNILEX == TokenType.VIRG:
                                UNILEX = lexer.ANALEX()
                                if UNILEX == TokenType.IDENT:
                                    nom_constante = lexer.CHAINE
                                    UNILEX = lexer.ANALEX()
                                    if UNILEX == TokenType.EG:
                                        UNILEX = lexer.ANALEX()
                                        if (UNILEX == TokenType.ENT) or (UNILEX == TokenType.CH):
                                            if DEFINIR_CONSTANTE(nom_constante, UNILEX):
                                                UNILEX = lexer.ANALEX()
                                            else:
                                                lexer.MESSAGE_ERREUR = f"Constante '{nom_constante}' déjà définie"
                                                lexer.ERREUR(3)
                                        else:
                                            lexer.MESSAGE_ERREUR = f"Attendu valeur de constante (nombre ou chaîne), trouvé {lexer.CHAINE}"
                                            lexer.ERREUR(3)
                                    else:
                                        lexer.MESSAGE_ERREUR = f"Attendu '=' dans déclaration de constante, trouvé {lexer.CHAINE}"
                                        lexer.ERREUR(3)
                                else:
                                    lexer.MESSAGE_ERREUR = f"Attendu nom de constante après ',', trouvé {lexer.CHAINE if lexer.CHAINE else 'EOF'}"
                                    lexer.ERREUR(3)
                            else:
                                non_fin = False
                        if UNILEX == TokenType.PTVIRG:
                            UNILEX = lexer.ANALEX()
                            return True
                        else:
                            lexer.MESSAGE_ERREUR = f"Attendu ';' après déclaration de constantes, trouvé {lexer.CHAINE if lexer.CHAINE else 'EOF'}"
                            lexer.ERREUR(3)
                    else:
                        lexer.MESSAGE_ERREUR = f"Constante '{nom_constante}' déjà définie"
                        lexer.ERREUR(3)
                else:
                    lexer.MESSAGE_ERREUR = f"Attendu valeur de constante (nombre ou chaîne), trouvé {lexer.CHAINE}"
                    lexer.ERREUR(3)
            else:
                lexer.MESSAGE_ERREUR = f"Attendu '=' dans déclaration de constante, trouvé {lexer.CHAINE if lexer.CHAINE else 'EOF'}"
                lexer.ERREUR(3)
        else:
            lexer.MESSAGE_ERREUR = f"Attendu nom de constante après CONST, trouvé {lexer.CHAINE if lexer.CHAINE else 'EOF'}"
            lexer.ERREUR(3)
    return False

def DECL_VAR():
    global UNILEX, DERNIERE_ADRESSE_VAR_GLOB
    if (UNILEX == TokenType.MOTCLE) and (lexer.CHAINE == 'VAR'):
        UNILEX = lexer.ANALEX()
        if UNILEX == TokenType.IDENT:
            while True:
                nom_var = lexer.CHAINE
                if CHERCHER(nom_var) != -1:
                    lexer.MESSAGE_ERREUR = f"Variable '{nom_var}' déjà définie"
                    lexer.ERREUR(3)
                DERNIERE_ADRESSE_VAR_GLOB += 1
                indice = INSERER(nom_var, T_IDENT.VARIABLE)
                TABLE_IDENT[indice].typv = 0
                TABLE_IDENT[indice].adrv = DERNIERE_ADRESSE_VAR_GLOB
                UNILEX = lexer.ANALEX()
                if UNILEX == TokenType.VIRG:
                    UNILEX = lexer.ANALEX()
                    if UNILEX != TokenType.IDENT:
                        lexer.MESSAGE_ERREUR = f"Attendu nom de variable après ',', trouvé {lexer.CHAINE if lexer.CHAINE else 'EOF'}"
                        lexer.ERREUR(3)
                else:
                    break
            if UNILEX == TokenType.PTVIRG:
                UNILEX = lexer.ANALEX()
                return True
            else:
                lexer.MESSAGE_ERREUR = f"Attendu ';' après déclaration de variables, trouvé {lexer.CHAINE if lexer.CHAINE else 'EOF'}"
                lexer.ERREUR(3)
        else:
            lexer.MESSAGE_ERREUR = f"Attendu nom de variable après VAR, trouvé {lexer.CHAINE if lexer.CHAINE else 'EOF'}"
            lexer.ERREUR(3)
    return False

def BLOC():
    global UNILEX
    if (UNILEX == TokenType.MOTCLE) and (lexer.CHAINE == 'DEBUT'):
        UNILEX = lexer.ANALEX()
        if INSTRUCTION():
            while True:
                if UNILEX == TokenType.PTVIRG:
                    UNILEX = lexer.ANALEX()
                    if (UNILEX == TokenType.MOTCLE) and (lexer.CHAINE == 'FIN'):
                        break
                    elif not INSTRUCTION():
                        lexer.MESSAGE_ERREUR = "Attendu une instruction après ';'"
                        lexer.ERREUR(3)
                elif (UNILEX == TokenType.MOTCLE) and (lexer.CHAINE == 'FIN'):
                    break
                else:
                    lexer.MESSAGE_ERREUR = f"Attendu ';' ou 'FIN', trouvé {lexer.CHAINE}"
                    lexer.ERREUR(3)
            if (UNILEX == TokenType.MOTCLE) and (lexer.CHAINE == 'FIN'):
                UNILEX = lexer.ANALEX()
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def INSTRUCTION():
    return (INST_COND() or INST_NON_COND())

def INST_NON_COND():
    return (AFFECTATION() or LECTURE() or ECRITURE() or BLOC() or INST_REPE())

def INST_REPE():
    global UNILEX
    if (UNILEX == TokenType.MOTCLE) and (lexer.CHAINE == 'TANTQUE'):
        UNILEX = lexer.ANALEX()
        machine.SOM_PILOP += 1
        machine.PILOP[machine.SOM_PILOP] = machine.CO
        if EXP():
            machine.P_CODE[machine.CO] = machine.ALSN
            machine.SOM_PILOP += 1
            machine.PILOP[machine.SOM_PILOP] = machine.CO + 1
            machine.CO += 2
            if (UNILEX == TokenType.MOTCLE) and (lexer.CHAINE == 'FAIRE'):
                UNILEX = lexer.ANALEX()
                if INSTRUCTION():
                    machine.P_CODE[machine.PILOP[machine.SOM_PILOP]] = machine.CO + 2
                    machine.SOM_PILOP -= 1
                    machine.P_CODE[machine.CO] = machine.ALLE
                    machine.P_CODE[machine.CO + 1] = machine.PILOP[machine.SOM_PILOP]
                    machine.SOM_PILOP -= 1
                    machine.CO += 2
                    return True
                else:
                    lexer.MESSAGE_ERREUR = "Instruction attendue après FAIRE"
                    lexer.ERREUR(3)
            else:
                lexer.MESSAGE_ERREUR = f"Attendu 'FAIRE', trouvé {lexer.CHAINE if lexer.CHAINE else 'EOF'}"
                lexer.ERREUR(3)
        else:
            lexer.MESSAGE_ERREUR = "Expression attendue après TANTQUE"
            lexer.ERREUR(3)
    return False

def INST_COND():
    global UNILEX
    if (UNILEX == TokenType.MOTCLE) and (lexer.CHAINE == 'SI'):
        UNILEX = lexer.ANALEX()
        if EXP():
            machine.P_CODE[machine.CO] = machine.ALSN
            machine.SOM_PILOP += 1
            machine.PILOP[machine.SOM_PILOP] = machine.CO + 1  
            machine.CO += 2
            if (UNILEX == TokenType.MOTCLE) and (lexer.CHAINE == 'ALORS'):
                UNILEX = lexer.ANALEX()
                if INST_COND():
                    machine.P_CODE[machine.PILOP[machine.SOM_PILOP]] = machine.CO
                    machine.SOM_PILOP -= 1
                    return True
                elif INST_NON_COND():
                    if (UNILEX == TokenType.MOTCLE) and (lexer.CHAINE == 'SINON'):
                        machine.P_CODE[machine.PILOP[machine.SOM_PILOP]] = machine.CO + 2
                        machine.SOM_PILOP -= 1  
                        machine.P_CODE[machine.CO] = machine.ALLE
                        machine.SOM_PILOP += 1
                        machine.PILOP[machine.SOM_PILOP] = machine.CO + 1  
                        machine.CO += 2
                        UNILEX = lexer.ANALEX()
                        if INSTRUCTION():
                            machine.P_CODE[machine.PILOP[machine.SOM_PILOP]] = machine.CO
                            machine.SOM_PILOP -= 1
                            return True
                        else:
                            lexer.MESSAGE_ERREUR = "Instruction attendue après SINON"
                            lexer.ERREUR(3)
                    else:
                        machine.P_CODE[machine.PILOP[machine.SOM_PILOP]] = machine.CO
                        machine.SOM_PILOP -= 1
                        return True
                else:
                    lexer.MESSAGE_ERREUR = "Instruction attendue après ALORS"
                    lexer.ERREUR(3)
            else:
                lexer.MESSAGE_ERREUR = f"Attendu 'ALORS', trouvé {lexer.CHAINE if lexer.CHAINE else 'EOF'}"
                lexer.ERREUR(3)
        else:
            lexer.MESSAGE_ERREUR = "Expression attendue après SI"
            lexer.ERREUR(3)
    return False


def AFFECTATION():
    global UNILEX
    if UNILEX == TokenType.IDENT:
        nom_var = lexer.CHAINE
        idx = CHERCHER(nom_var)
        if idx == -1:
            lexer.MESSAGE_ERREUR = f"Variable '{nom_var}' n'a pas été déclarée."
            lexer.ERREUR(3)
        if TABLE_IDENT[idx].typ != T_IDENT.VARIABLE:
            lexer.MESSAGE_ERREUR = f"'{nom_var}' n'est pas une variable."
            lexer.ERREUR(3)
        UNILEX = lexer.ANALEX()
        if UNILEX == TokenType.AFF:
            machine.P_CODE[machine.CO] = machine.EMPI
            machine.P_CODE[machine.CO+1] = TABLE_IDENT[idx].adrv
            machine.CO += 2
            UNILEX = lexer.ANALEX()
            if EXP():
                machine.P_CODE[machine.CO] = machine.AFFE
                machine.CO += 1
                return True
            else:
                lexer.MESSAGE_ERREUR = f"Expression incorrecte dans l'affectation de '{nom_var}'"
                lexer.ERREUR(3)
        else:
            lexer.MESSAGE_ERREUR = f"Attendu ':=', trouvé '{lexer.CHAINE}'"
            lexer.ERREUR(3)
    else:
        return False

def LECTURE():
    global UNILEX
    if (UNILEX == TokenType.MOTCLE) and (lexer.CHAINE == 'LIRE'):
        UNILEX = lexer.ANALEX()
        if UNILEX == TokenType.PAROUV:
            UNILEX = lexer.ANALEX()
            if UNILEX == TokenType.IDENT:
                while True:
                    nom_var = lexer.CHAINE
                    idx = CHERCHER(nom_var)
                    if idx == -1:
                        lexer.MESSAGE_ERREUR = f"Identificateur '{nom_var}' non déclaré."
                        lexer.ERREUR(3)
                    if TABLE_IDENT[idx].typ != T_IDENT.VARIABLE:
                        lexer.MESSAGE_ERREUR = f"'{nom_var}' n'est pas une variable."
                        lexer.ERREUR(3)
                    machine.P_CODE[machine.CO] = machine.EMPI
                    machine.P_CODE[machine.CO+1] = TABLE_IDENT[idx].adrv
                    machine.P_CODE[machine.CO+2] = machine.LIRE
                    machine.CO += 3
                    UNILEX = lexer.ANALEX()
                    if UNILEX == TokenType.VIRG:
                        UNILEX = lexer.ANALEX()
                        if UNILEX != TokenType.IDENT:
                            lexer.MESSAGE_ERREUR = f"Attendu identificateur après ',', trouvé {lexer.CHAINE if lexer.CHAINE else 'EOF'}"
                            lexer.ERREUR(3)
                    else:
                        break
                if UNILEX == TokenType.PARFER:
                    UNILEX = lexer.ANALEX()
                    return True
                else:
                    lexer.MESSAGE_ERREUR = f"Attendu ')', trouvé {lexer.CHAINE if lexer.CHAINE else 'EOF'}"
                    lexer.ERREUR(3)
            else:
                lexer.MESSAGE_ERREUR = f"Attendu identificateur après 'LIRE(', trouvé {lexer.CHAINE if lexer.CHAINE else 'EOF'}"
                lexer.ERREUR(3)
        else:
            lexer.MESSAGE_ERREUR = f"Attendu '(', trouvé {lexer.CHAINE if lexer.CHAINE else 'EOF'}"
            lexer.ERREUR(3)
    else:
        return False
    
def ECRITURE():
    global UNILEX
    if (UNILEX == TokenType.MOTCLE) and (lexer.CHAINE == 'ECRIRE'):
        UNILEX = lexer.ANALEX()
        if UNILEX == TokenType.PAROUV:
            UNILEX = lexer.ANALEX()
            if UNILEX == TokenType.PARFER:
                machine.P_CODE[machine.CO] = machine.ECRL
                machine.CO += 1
                UNILEX = lexer.ANALEX()
                return True
            if ECR_EXP():
                fin = False
                while not fin:
                    if UNILEX == TokenType.VIRG:
                        UNILEX = lexer.ANALEX()
                        if not ECR_EXP():
                            lexer.MESSAGE_ERREUR = "Expression incorrecte dans ECRIRE"
                            lexer.ERREUR(3)
                    else:
                        fin = True
                if UNILEX == TokenType.PARFER:
                    UNILEX = lexer.ANALEX()
                    machine.P_CODE[machine.CO] = machine.ECRL
                    machine.CO += 1
                    return True
                else:
                    lexer.MESSAGE_ERREUR = f"Attendu ')', trouvé {lexer.CHAINE if lexer.CHAINE else 'EOF'}"
                    lexer.ERREUR(3)
            else:
                return False
        else:
            lexer.MESSAGE_ERREUR = f"Attendu '(', trouvé {lexer.CHAINE if lexer.CHAINE else 'EOF'}"
            lexer.ERREUR(3)
    else:
        return False
    
def ECR_EXP():
    global UNILEX
    if UNILEX == TokenType.CH:
        chaine = lexer.CHAINE
        machine.P_CODE[machine.CO] = machine.ECRC
        machine.CO += 1
        for c in chaine:
            machine.P_CODE[machine.CO] = ord(c)
            machine.CO += 1
        machine.P_CODE[machine.CO] = machine.FINC
        machine.CO += 1
        UNILEX = lexer.ANALEX()
        return True
    elif EXP():
        machine.P_CODE[machine.CO] = machine.ECRE
        machine.CO += 1
        return True
    return False

def EXP():
    if TERME():
        if SUITE_TERME():
            return True
    return False

def TERME():
    global UNILEX
    if UNILEX == TokenType.ENT:
        valeur = lexer.NOMBRE
        machine.P_CODE[machine.CO] = machine.EMPI
        machine.P_CODE[machine.CO+1] = valeur
        machine.CO += 2
        UNILEX = lexer.ANALEX()
        return True
    elif UNILEX == TokenType.IDENT:
        nom_var = lexer.CHAINE
        idx = CHERCHER(nom_var)
        if idx == -1:
            lexer.MESSAGE_ERREUR = f"Identificateur '{nom_var}' non déclaré."
            lexer.ERREUR(3)
        if TABLE_IDENT[idx].typ == T_IDENT.VARIABLE:
            machine.P_CODE[machine.CO] = machine.EMPI
            machine.P_CODE[machine.CO+1] = TABLE_IDENT[idx].adrv
            machine.CO += 2
            machine.P_CODE[machine.CO] = machine.CONT
            machine.CO += 1
        elif TABLE_IDENT[idx].typ == T_IDENT.CONSTANTE:
            if TABLE_IDENT[idx].typc != 0:
                lexer.MESSAGE_ERREUR = f"Constante '{nom_var}' doit être de type entier dans une expression."
                lexer.ERREUR(3)
            machine.P_CODE[machine.CO] = machine.EMPI
            machine.P_CODE[machine.CO+1] = TABLE_IDENT[idx].val
            machine.CO += 2
        else:
            lexer.MESSAGE_ERREUR = f"'{nom_var}' n'est pas une constante ou variable."
            lexer.ERREUR(3)
        UNILEX = lexer.ANALEX()
        return True
    elif UNILEX == TokenType.PAROUV:
        UNILEX = lexer.ANALEX()
        if EXP():
            if UNILEX == TokenType.PARFER:
                UNILEX = lexer.ANALEX()
                return True
            else:
                lexer.MESSAGE_ERREUR = f"Attendu ')' après expression, trouvé '{lexer.CHAINE}'"
                lexer.ERREUR(3)
        else:
            lexer.MESSAGE_ERREUR = "Expression attendue après '('"
            lexer.ERREUR(3)
    elif UNILEX == TokenType.MOINS:
        UNILEX = lexer.ANALEX()
        if TERME():
            machine.P_CODE[machine.CO] = machine.MOIN
            machine.CO += 1
            return True
        else:
            lexer.MESSAGE_ERREUR = "Terme attendu après '-'"
            lexer.ERREUR(3)
    return False

def SUITE_TERME():
    if OP_BIN():
        if EXP():
            opcode = machine.PILOP[machine.SOM_PILOP]
            machine.SOM_PILOP -= 1
            machine.P_CODE[machine.CO] = opcode
            machine.CO += 1
            return True
        lexer.MESSAGE_ERREUR = "Expression attendue après l'opérateur"
        lexer.ERREUR(3)
    return True

def OP_BIN():
    global UNILEX
    if UNILEX == TokenType.PLUS:
        machine.SOM_PILOP += 1
        machine.PILOP[machine.SOM_PILOP] = machine.ADDI
        UNILEX = lexer.ANALEX()
        return True
    elif UNILEX == TokenType.MOINS:
        machine.SOM_PILOP += 1
        machine.PILOP[machine.SOM_PILOP] = machine.SOUS
        UNILEX = lexer.ANALEX()
        return True
    elif UNILEX == TokenType.MULT:
        machine.SOM_PILOP += 1
        machine.PILOP[machine.SOM_PILOP] = machine.MULT
        UNILEX = lexer.ANALEX()
        return True
    elif UNILEX == TokenType.DIVI:
        machine.SOM_PILOP += 1
        machine.PILOP[machine.SOM_PILOP] = machine.DIVI
        UNILEX = lexer.ANALEX()
        return True
    return False

## GENCODE_ FUNCTIONS
def GENCODE_EMPI(valeur):
    machine.P_CODE[machine.CO] = machine.EMPI
    machine.P_CODE[machine.CO+1] = valeur
    machine.CO += 2

def GENCODE_AFFE():
    machine.P_CODE[machine.CO] = machine.AFFE
    machine.CO += 1

def GENCODE_LECTURE(ch):
    machine.P_CODE[machine.CO] = machine.LIRE  
    machine.CO += 1
    idx = CHERCHER(ch)
    if idx == -1:
        raise Exception(f"Identificateur '{ch}' non trouvé pour LIRE.")
    machine.P_CODE[machine.CO] = TABLE_IDENT[idx].adrv
    machine.CO += 1

def GENCODE_ECRL():
    machine.P_CODE[machine.CO] = machine.ECRL
    machine.CO += 1

def GENCODE_ECRE():
    machine.P_CODE[machine.CO] = machine.ECRE
    machine.CO += 1

def GENCODE_ECRC(chaine):
    machine.P_CODE[machine.CO] = machine.ECRC
    machine.CO += 1
    for c in chaine:
        machine.P_CODE[machine.CO] = ord(c)
        machine.CO += 1
    machine.P_CODE[machine.CO] = machine.FINC
    machine.CO += 1

def GENCODE_OPERATION(op):
    if op == '+':
        machine.P_CODE[machine.CO] = machine.ADDI
    elif op == '-':
        machine.P_CODE[machine.CO] = machine.SOUS
    elif op == '*':
        machine.P_CODE[machine.CO] = machine.MULT
    elif op == '/':
        machine.P_CODE[machine.CO] = machine.DIVI
    machine.CO += 1
    
def GENCODE_CONT():
    machine.P_CODE[machine.CO] = machine.CONT
    machine.CO += 1

def GENCODE_STOP():
    machine.P_CODE[machine.CO] = machine.STOP
    machine.CO += 1