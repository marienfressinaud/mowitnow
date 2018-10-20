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
1 3 N
5 1 E
```

Le programme retourne les positions finales des différentes tondeuses qui
auront été initialisées dans le fichier en entrée, en fonction des instructions
qui leur seront données.

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

Les lignes qui suivent sont spécifiques aux tondeuses et vont par paire. Une
paire correspond aux instructions pour une tondeuse.

La première ligne de chaque paire correspond à l'emplacement initiale de la
tondeuse ainsi que sa direction. Elle doit contenir 2 nombres supérieurs ou
égals à 0, et inférieurs ou égals aux dimensions de la pelouse. La direction
est une lettre parmis `N` (nord), `E` (est), `W` (ouest) et `S` (sud). Exemples
pour une pelouse de taille 5x5 :

```raw
# Valeurs correctes

1 2 N
5 5 S
0 0 W

# Valeurs incorrectes

1
1 N 2
1 2 N S
1 2 A
-1 2 N
6 2 N
```

La deuxième ligne de la paire correspond aux instructions envoyées à la
tondeuse. Il s'agit d'une suite de caractères sans limite fixe. Les caractères
possibles sont `D` (tourne de 90° vers la droite), `G` (tourne de 90° vers la
gauche) et `A` (avance dans la direction actuelle). Exemples :

```raw
# Valeurs correctes

GAGAGAGAA
AADAADADDA

# Valeurs incorrectes

GAGAGAP
AZERTY
```

Contrairement aux autres données, si des valeurs incorrectes sont entrées sur
cette ligne, aucune erreur n'est levée. La tondeuse ne bougera tout simplement
pas.

## Tests

Les tests sont écrits avec [doctest](https://docs.python.org/3/library/doctest.html).
Voici la commande pour les exécuter :

```console
$ python3 -m doctest -v mowitnow.py
```
