{ Tache 4 : instructions de controle SI/SINON et TANTQUE. }

PROGRAMME tache4;
VAR n, s, parite;
DEBUT
    n := 6;
    s := 0;
    parite := 0;   { 0 = pair, 1 = impair }

    { TANTQUE : calcule la somme 1 + 2 + ... + n }
    TANTQUE n FAIRE
        DEBUT
            s := s + n;
            n := n - 1
        FIN;
    ECRIRE('somme(1..6)    = ', s);

    { SI/SINON : verification du resultat (s - 21 = 0 si correct) }
    SI s - 21 ALORS
        ECRIRE('resultat incorrect')
    SINON
        ECRIRE('resultat correct : 21');

    { SI imbrique avec BLOC dans la branche SINON }
    SI parite ALORS
        ECRIRE('impair')
    SINON
        DEBUT
            ECRIRE('pair : parite = 0');
            parite := 1;
            SI parite ALORS
                ECRIRE('parite modifiee a 1')
            SINON
                ECRIRE('parite toujours 0')
        FIN
FIN.
