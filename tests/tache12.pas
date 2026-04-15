{ Taches 1 et 2 : jeu d'essai pour l'analyseur lexical et la table des identificateurs. }

PROGRAMME myApp;
CONST
	x = 'a',
	b = 2;
VAR
	z, t;
DEBUT
	ECRIRE('Type a number: ');
	LIRE(t);
	z := t * b * 2;
	ECRIRE('Your number multiplied by 4 is: ', z)
FIN.