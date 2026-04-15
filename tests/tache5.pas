{ Tache 5 : fonctions, passage par valeur, recursivite. }

PROGRAMME tache5;
VAR r;

FONCTION carre(x) : ENTIER;
DEBUT
    carre := x * x
FIN;

FONCTION puissance(b, n) : ENTIER;
DEBUT
    SI n ALORS
        puissance := b * puissance(b, n - 1)
    SINON
        puissance := 1
FIN;

DEBUT
    r := carre(7);
    ECRIRE('carre(7)       = ', r);
    r := puissance(2, 8);
    ECRIRE('puissance(2,8) = ', r)
FIN.
