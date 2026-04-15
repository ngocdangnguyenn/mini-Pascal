PROGRAMME complet;
CONST MAX = 10;
VAR n, res, i;

FONCTION fact(k) : ENTIER;
DEBUT
    SI k ALORS
        fact := k * fact(k - 1)
    SINON
        fact := 1
FIN;

DEBUT
    ECRIRE('Entrez n : ');
    LIRE(n);
    res := fact(n);
    ECRIRE('fact(', n, ') = ', res);
    i := 1;
    TANTQUE i - MAX FAIRE
        DEBUT
            i := i + 1
        FIN;
    ECRIRE('i final = ', i)
FIN.