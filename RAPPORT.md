# Compte rendu — Mini-compilateur Pascal

**Auteur :** NGUYEN Ngoc Dang Nguyen

---

## Présentation générale

Ce projet implémente un mini-compilateur pour un sous-ensemble du langage Pascal, de l'analyse lexicale jusqu'à l'interprétation du code généré. Il est entièrement écrit en Python 3, sans bibliothèque externe, et s'organise en cinq modules sources indépendants. La chaîne de traitement suit les étapes classiques : le lexer tokenise le source, le parseur vérifie la syntaxe et génère du code intermédiaire, puis une machine virtuelle à pile exécute ce code. Chaque étape est couverte par un fichier de test dédié dans le dossier `tests/`.

---

## Parties réalisées

**Parties 1 et 2 — Analyse lexicale et table des identificateurs**

L'analyseur lexical reconnaît tous les éléments du langage : mots-clés, identificateurs, entiers (max 32 767), chaînes de caractères (apostrophe doublée `''` supportée, longueur max 50), et tous les symboles simples et composés. Les commentaires entre accolades `{ }` sont ignorés, avec support de l'imbrication. La recherche des mots réservés utilise une recherche dichotomique sur une table triée, ce qui garantit un temps logarithmique. La table des identificateurs est implémentée comme une table de hachage à chaînage qui stocke les variables, constantes, fonctions et paramètres avec leurs attributs respectifs.

**Partie 3 — Analyse syntaxique, sémantique, génération et interprétation du code**

Le parseur est un analyseur descendant récursif qui effectue simultanément la vérification syntaxique, les contrôles sémantiques (identificateur déclaré, type correct, absence de redéclaration) et la génération de code à la volée dans un tableau d'instructions, sans construire d'arbre syntaxique intermédiaire. La machine virtuelle à pile exécute ce tableau : elle dispose d'une pile d'exécution et d'une mémoire linéaire pour les variables globales. Le code intermédiaire généré est également sauvegardé dans un fichier `.COD`.

**Partie 4 — Instructions de contrôle (`SI/ALORS/SINON` et `TANTQUE/FAIRE`)**

Les structures conditionnelles et la boucle sont implémentées avec la technique du backpatching : les adresses de saut sont réservées dans le code puis corrigées une fois la destination connue. La branche `SINON` optionnelle ainsi que l'imbrication des structures de contrôle sont correctement gérées.

**Partie 5 (bonus) — Traitement des fonctions**

Les fonctions à valeur de retour entière avec passage de paramètres par valeur et récursivité sont entièrement implémentées. La convention d'appel est basée sur une pile de cadres : slot de retour, sauvegarde du pointeur de base, arguments, puis retour propre à la fin de la fonction. La portée des paramètres est gérée explicitement : ils sont supprimés de la table des identificateurs à la fin de chaque définition de fonction.

---

## Parties non réalisées

Aucune.

