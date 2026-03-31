import sys
import src.lexer as lexer
import src.parser as parser
import src.machine as machine
from src.table_ident import REINITIALISER_TABLE
import src.table_ident as table_ident

def main():
    if len(sys.argv) > 1:
        nom_fichier = sys.argv[1]
    else:
        nom_fichier = "tests/test.pas"
    
    print(f"\n{'='*80}")
    print(f"PHASE 3: PARSING + CODE GENERATION + INTERPRETER")
    print(f"{'='*80}")
    print(f"File: {nom_fichier}\n")
    
    try:
        REINITIALISER_TABLE()
        parser.TABLE_IDENT = table_ident.TABLE_IDENT
        parser.UNILEX = None
        parser.NB_CONST_CHAINE = 0
        parser.VAL_DE_CONST_CHAINE = []
        parser.DERNIERE_ADRESSE_VAR_GLOB = -1
        machine.CO = 0
        machine.SOM_PILEX = -1
        machine.SOM_PILOP = -1
        machine.P_CODE = [0] * machine.TAILLE_MAX_MEM
        machine.MEMVAR = [0] * machine.TAILLE_MAX_MEM
        
        lexer.INITIALISER(nom_fichier)
        parser.UNILEX = lexer.ANALEX()
        ok = parser.PROG()
        lexer.TERMINER()
        if ok:
            machine.CREER_FICHIER_CODE(nom_fichier)
            print("Parsing: OK")
            print(f"Generated code: {machine.CO} instructions")
            print("\nRunning interpreter:")
            print("-" * 80)
            machine.CO = 0
            machine.SOM_PILEX = -1
            machine.SOM_PILOP = -1
            machine.INTERPRETER()
            print("\n" + "-" * 80)
            print("\nExecution completed successfully")
        else:
            if lexer.MESSAGE_ERREUR:
                print(f"Parsing failed: {lexer.MESSAGE_ERREUR}")
            else:
                print("Parsing failed")
    except SystemExit:
        pass
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            lexer.TERMINER()
        except:
            pass

if __name__ == "__main__":
    main()
