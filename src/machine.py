ADDI = 0
SOUS = 1
MULT = 2
DIVI = 3
MOIN = 4
AFFE = 5
LIRE = 6
ECRL = 7
ECRE = 8
ECRC = 9
FINC = 10
EMPI = 11
CONT = 12
STOP = 13
ALLE = 14
ALSN = 15
SAVEPB = 16
EMPL = 17
AFFR = 18
APPF = 19
RETN = 20

TAILLE_MAX_MEM = 10000
MEMVAR = [0] * TAILLE_MAX_MEM  
P_CODE = [0] * TAILLE_MAX_MEM  
CO = 0                          
PB = 0

PILEX = [0] * TAILLE_MAX_MEM
SOM_PILEX = -1

PILOP = [0] * 100
SOM_PILOP = -1

def INTERPRETER():
    global CO, SOM_PILEX, PB
    while P_CODE[CO] != STOP:
        if P_CODE[CO] == ADDI:
            PILEX[SOM_PILEX-1] = PILEX[SOM_PILEX-1] + PILEX[SOM_PILEX]
            SOM_PILEX -= 1
            CO += 1
        elif P_CODE[CO] == SOUS:
            PILEX[SOM_PILEX-1] = PILEX[SOM_PILEX-1] - PILEX[SOM_PILEX]
            SOM_PILEX -= 1
            CO += 1
        elif P_CODE[CO] == MULT:
            PILEX[SOM_PILEX-1] = PILEX[SOM_PILEX-1] * PILEX[SOM_PILEX]
            SOM_PILEX -= 1
            CO += 1
        elif P_CODE[CO] == DIVI:
            if PILEX[SOM_PILEX] == 0:
                print("Erreur: division par zéro!")
                break
            PILEX[SOM_PILEX-1] = PILEX[SOM_PILEX-1] // PILEX[SOM_PILEX]
            SOM_PILEX -= 1
            CO += 1
        elif P_CODE[CO] == MOIN:
            PILEX[SOM_PILEX] = -PILEX[SOM_PILEX]
            CO += 1
        elif P_CODE[CO] == AFFE:
            MEMVAR[PILEX[SOM_PILEX-1]] = PILEX[SOM_PILEX]
            SOM_PILEX -= 2
            CO += 1
        elif P_CODE[CO] == LIRE:
            val = int(input("? "))
            addr = PILEX[SOM_PILEX]
            SOM_PILEX -= 1
            MEMVAR[addr] = val
            CO += 1
        elif P_CODE[CO] == ECRL:
            print()
            CO += 1
        elif P_CODE[CO] == ECRE:
            print(PILEX[SOM_PILEX], end='')
            SOM_PILEX -= 1
            CO += 1
        elif P_CODE[CO] == ECRC:
            i = 1
            while P_CODE[CO + i] != FINC:
                print(chr(P_CODE[CO + i]), end='')
                i += 1
            CO += i + 1
        elif P_CODE[CO] == EMPI:
            SOM_PILEX += 1
            PILEX[SOM_PILEX] = P_CODE[CO+1]
            CO += 2
        elif P_CODE[CO] == CONT:
            PILEX[SOM_PILEX] = MEMVAR[PILEX[SOM_PILEX]]
            CO += 1
        elif P_CODE[CO] == ALLE:
            CO = P_CODE[CO + 1]
        elif P_CODE[CO] == ALSN:
            if PILEX[SOM_PILEX] == 0:
                CO = P_CODE[CO + 1]
            else:
                CO += 2
            SOM_PILEX -= 1
        elif P_CODE[CO] == SAVEPB:
            SOM_PILEX += 1
            PILEX[SOM_PILEX] = PB
            CO += 1
        elif P_CODE[CO] == EMPL:
            SOM_PILEX += 1
            PILEX[SOM_PILEX] = PILEX[PB + P_CODE[CO + 1]]
            CO += 2
        elif P_CODE[CO] == AFFR:
            PILEX[PB - 2] = PILEX[SOM_PILEX]
            SOM_PILEX -= 1
            CO += 1
        elif P_CODE[CO] == APPF:
            addr = P_CODE[CO + 1]
            N    = P_CODE[CO + 2]
            SOM_PILEX += 1
            PILEX[SOM_PILEX] = CO + 3
            PB = SOM_PILEX - N
            CO = addr
        elif P_CODE[CO] == RETN:
            N = P_CODE[CO + 1]
            ret_addr = PILEX[PB + N]
            old_PB   = PILEX[PB - 1]
            SOM_PILEX = PB - 2
            PB  = old_PB
            CO  = ret_addr
        elif P_CODE[CO] == STOP:
            break
        else:
            print(f"Opcode inconnu: {P_CODE[CO]}")
            break

def CREER_FICHIER_CODE(nom_fichier_source):
    import os
    base = os.path.splitext(nom_fichier_source)[0]
    cod_dir = 'cod'
    os.makedirs(cod_dir, exist_ok=True)
    nom_fichier_cod = os.path.join(cod_dir, os.path.basename(base) + '.COD')
    with open(nom_fichier_cod, 'w', encoding='utf-8') as f:
        opcodes = {
            ADDI: 'ADDI', SOUS: 'SOUS', MULT: 'MULT', DIVI: 'DIVI', MOIN: 'MOIN',
            AFFE: 'AFFE', LIRE: 'LIRE', ECRL: 'ECRL', ECRE: 'ECRE', ECRC: 'ECRC',
            FINC: 'FINC', EMPI: 'EMPI', CONT: 'CONT', STOP: 'STOP',
            ALLE: 'ALLE', ALSN: 'ALSN',
            SAVEPB: 'SAVEPB', EMPL: 'EMPL', AFFR: 'AFFR', APPF: 'APPF', RETN: 'RETN'
        }
        i = 0
        while i < CO:
            opcode = P_CODE[i]
            op_name = opcodes.get(opcode, f'OP_{opcode}')
            if opcode == EMPI:
                f.write(f'{op_name} {P_CODE[i+1]}\n')
                i += 2
            elif opcode == AFFE:
                f.write(f'{op_name}\n')
                i += 1
            elif opcode == LIRE:
                f.write(f'{op_name}\n')
                i += 1
            elif opcode in (ALLE, ALSN):
                f.write(f'{op_name} {P_CODE[i+1]}\n')
                i += 2
            elif opcode in (EMPL, RETN):
                f.write(f'{op_name} {P_CODE[i+1]}\n')
                i += 2
            elif opcode == APPF:
                f.write(f'{op_name} {P_CODE[i+1]} {P_CODE[i+2]}\n')
                i += 3
            elif opcode in (SAVEPB, AFFR):
                f.write(f'{op_name}\n')
                i += 1
            elif opcode == ECRC:
                s = ''
                j = i + 1
                while P_CODE[j] != FINC:
                    s += chr(P_CODE[j])
                    j += 1
                f.write(f'{op_name} {s} FINC\n')
                i = j + 1
            else:
                f.write(f'{op_name}\n')
                i += 1