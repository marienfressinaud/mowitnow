# MowItNow

Un programme de tondeuse à gazon automatique, écrit en Python.

## Usage

Pour exécuter le programme, vous devez vous assurer d'avoir Python 3.6 installé
sur votre PC.

```console
$ python3 --version
Python 3.6.6
```

Ensuite, exécutez le programme avec :

```console
$ ./mowitnow.py instructions.sample.txt
```

Pour le moment, le programme se contente d'afficher la taille du terrain à
tondre ; de nouvelles fonctionnalités devraient arriver très prochainement !

## Format du fichier en entrée

Le fichier en entrée doit suivre un format pré-défini.

La première ligne indique la taille de la pelouse à tondre. Elle se compose de
deux nombres strictement supérieurs à 0. Exemples :

```raw
# Valeurs correctes

5 5
42 666
1 1

# Valeurs incorrectes

0 5
-1 42
foo 5
1
5 5 5
```

## Tests

Les tests sont écrits avec [doctest](https://docs.python.org/3/library/doctest.html).
Voici la commande pour les exécuter :

```console
$ python3 -m doctest -v mowitnow.py
```
