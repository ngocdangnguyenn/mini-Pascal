# Compilateur mini-Pascal

**Auteur :** NGUYEN Ngoc Dang Nguyen

Mini-compilateur pour un sous-ensemble du langage Pascal, de l'analyse lexicale jusqu'à l'interprétation du code généré. Écrit en Python 3, sans bibliothèque externe.

---

## Utilisation

```bash
python main.py <fichier.pas>
```

Pour lancer les tests intégrés, décommenter la fonction voulue dans `main.py`. Les fichiers de test disponibles :

| Fichier | Tâche | Entrée |
|---------|-------|--------|
| `tests/tache12.pas` | 1 et 2 — lexer + table des identificateurs | aucune |
| `tests/tache3.pas`  | 3 — arithmétique, LIRE, ECRIRE, BLOC imbriqué | un entier |
| `tests/tache4.pas`  | 4 — SI/ALORS/SINON, TANTQUE/FAIRE | aucune |
| `tests/tache5.pas`  | 5 — fonctions, récursivité | aucune |
| `tests/complet.pas` | toutes les tâches combinées | un entier |

---

## Structure du projet

```
mini-Pascal/
├── main.py               # point d'entrée + fonctions de test par tâche
├── src/
│   ├── token.py          # types de tokens
│   ├── lexer.py          # analyseur lexical
│   ├── table_ident.py    # table des identificateurs (hachage)
│   ├── parser.py         # parseur + génération de code
│   └── machine.py        # machine virtuelle à pile
├── tests/                # programmes de test .pas
└── cod/                  # code intermédiaire généré .COD
```
