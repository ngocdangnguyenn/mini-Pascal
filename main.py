import sys
import io
import src.lexer as lexer
from src.token import TokenType
import src.parser as parser
import src.machine as machine
from src.table_ident import REINITIALISER_TABLE, AFFICHE_TABLE_IDENT
import src.table_ident as table_ident


def _reset():
    REINITIALISER_TABLE()
    parser.TABLE_IDENT = table_ident.TABLE_IDENT
    parser.UNILEX = None
    parser.NB_CONST_CHAINE = 0
    parser.VAL_DE_CONST_CHAINE = []
    parser.DERNIERE_ADRESSE_VAR_GLOB = -1
    machine.CO = 0
    machine.SOM_PILEX = -1
    machine.SOM_PILOP = -1
    machine.PB = 0
    machine.P_CODE = [0] * machine.TAILLE_MAX_MEM
    machine.MEMVAR = [0] * machine.TAILLE_MAX_MEM
    parser.FONCTION_COURANTE = None


def compile_and_run(nom_fichier, entree=None):
    print(f"\n{'='*60}")
    print(f"Fichier : {nom_fichier}")
    if entree is not None:
        print(f"Entrée  : {entree.strip()}")
    print('='*60)

    stdin_original = sys.stdin
    if entree is not None:
        sys.stdin = io.StringIO(entree)

    try:
        _reset()
        lexer.INITIALISER(nom_fichier)
        parser.UNILEX = lexer.ANALEX()
        ok = parser.PROG()
        lexer.TERMINER()

        if ok:
            machine.CREER_FICHIER_CODE(nom_fichier)
            print(f"Compilation OK — {machine.CO} instructions générées")
            print("-" * 60)
            machine.CO = 0
            machine.SOM_PILEX = -1
            machine.SOM_PILOP = -1
            machine.PB = 0
            machine.INTERPRETER()
            print("-" * 60)
            print("Exécution terminée")
        else:
            msg = lexer.MESSAGE_ERREUR or "erreur de syntaxe"
            print(f"Echec de la compilation : {msg}")

    except SystemExit:
        pass
    except Exception:
        import traceback
        traceback.print_exc()
    finally:
        sys.stdin = stdin_original
        try:
            lexer.TERMINER()
        except Exception:
            pass


def tests_tache12(nom_fichier="tests/tache12.pas"):
    print(f"\n{'='*62}")
    print(f"  TÂCHE 1-2 — Phase A : flux de tokens")
    print(f"  Fichier : {nom_fichier}")
    print(f"{'='*62}")
    print(f"  {'#':<4}  {'Type':<12}  Valeur")
    print(f"  {'-'*56}")
    n = 0
    try:
        lexer.INITIALISER(nom_fichier)
        tok = lexer.ANALEX()
        while tok is not None:
            n += 1
            if tok == TokenType.MOTCLE:
                print(f"  [{n:<3}]  {'mot-cle':<12}  {lexer.CHAINE}")
            elif tok == TokenType.IDENT:
                print(f"  [{n:<3}]  {'ident':<12}  {lexer.CHAINE}")
            elif tok == TokenType.ENT:
                print(f"  [{n:<3}]  {'entier':<12}  {lexer.NOMBRE}")
            elif tok == TokenType.CH:
                print(f"  [{n:<3}]  {'chaine':<12}  '{lexer.CHAINE}'")
            else:
                SYM = {
                    'ptvirg': ';', 'point': '.', 'virg': ',', 'deuxpts': ':',
                    'parouv': '(', 'parfer': ')', 'plus': '+', 'moins': '-',
                    'mult': '*', 'divi': '/', 'eg': '=', 'inf': '<', 'sup': '>',
                    'infe': '<=', 'supe': '>=', 'diff': '<>', 'aff': ':=',
                }
                print(f"  [{n:<3}]  {tok.value:<12}  {SYM.get(tok.value, tok.value)}")
            if tok == TokenType.POINT:
                break
            tok = lexer.ANALEX()
        lexer.TERMINER()
        print(f"  {'-'*56}")
        print(f"  Total : {n} token(s)")
    except SystemExit:
        pass

    print(f"\n{'='*62}")
    print(f"  TÂCHE 1-2 — Phase B : table des identificateurs")
    print(f"{'='*62}")
    try:
        _reset()
        lexer.INITIALISER(nom_fichier)
        parser.UNILEX = lexer.ANALEX()
        ok = parser.PROG()
        lexer.TERMINER()
        if ok:
            AFFICHE_TABLE_IDENT()
        else:
            print(f"  Echec parsing : {lexer.MESSAGE_ERREUR or 'erreur syntaxe'}")
    except SystemExit:
        pass


def tests_tache3():
    compile_and_run("tests/tache3.pas", entree="5\n")


def tests_tache4():
    compile_and_run("tests/tache4.pas")


def tests_tache5():
    compile_and_run("tests/tache5.pas")


def tests_complet():
    compile_and_run("tests/complet.pas", entree="5\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        compile_and_run(sys.argv[1])
    else:
        # tests_tache12()
        # tests_tache3()
        # tests_tache4()
        # tests_tache5()
        # tests_complet()
        print("Usage : python main.py <fichier.pas>")
