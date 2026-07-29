---
title: "Solution du Wargame Bandit - OverTheWire"
date: 2026-07-25 12:00:00 +0100
categories: [CTF, Wargame]
tags: [bandit, ssh, linux, overthewire]
image:
  path: /assets/img/posts/bandit-cover.png
  alt: Terminal OverTheWire Bandit
---



## Level 0

**Objectif** : Se connecter en SSH sur le serveur avec les identifiants fournis par défaut (`bandit0`/`bandit0`).

```bash
ssh -p 2220 bandit0@bandit.labs.overthewire.org
```

### 🔍 Découvertes

- Bandit utilise systématiquement le **port 2220** au lieu du port SSH standard (22) — une pratique courante pour limiter le bruit des scans automatiques sur le port par défaut
- Une fois connecté, un `ls -la` révèle un fichier `readme` dans le répertoire personnel :

```bash
bandit0@bandit:~$ ls -la
-rw-r----- 1 bandit1 bandit0  438 Jun 24 14:58 readme
```

- Chaque niveau possède également un fichier de mot de passe dédié dans `/etc/bandit_pass/`, en lecture seule et accessible uniquement par l'utilisateur concerné — une bonne illustration du principe du **moindre privilège**
- Un simple `cat readme` suffit à récupérer le mot de passe nécessaire pour passer au niveau suivant :

```bash
bandit0@bandit:~$ cat readme
6y2kwnwK6grgvwvpvLaa2T1cpFEKOhNR
```

### 🛠️ Commandes clés
`ssh`, `ls -la`, `cat`

---
## Level 1 → Level 2

**Objectif** : Le mot de passe est stocké dans un fichier nommé `-` (juste un tiret), situé dans le répertoire personnel.

```bash
bandit1@bandit:~$ ls -la
-rw-r-----   1 bandit2 bandit1   33 Jun 24 14:59 -
```

Un simple `cat -` échoue silencieusement ou se comporte de façon inattendue, car le shell interprète `-` comme une référence à l'entrée standard plutôt que comme un nom de fichier littéral.

### 🔍 Découvertes

- Un fichier nommé uniquement `-` piège les commandes shell classiques : `cat -` par exemple attend une entrée depuis le clavier au lieu de lire le fichier
- Solution : préfixer explicitement le chemin avec `./` pour forcer le shell à traiter `-` comme un chemin relatif et non comme une option ou un symbole spécial :

```bash
bandit1@bandit:~$ cat ./-
PK8fYLZg2hnHSz83plBL1iEPKdD3QToB
```

- Ce niveau illustre un piège classique de sécurité : le nommage ambigu de fichiers peut perturber ou détourner le comportement attendu d'une commande — un principe qu'on retrouve aussi dans certaines techniques d'injection d'arguments

### 🛠️ Commandes clés
`ls -la`, `cat ./-`

---
## Level 2 → Level 3

**Objectif** : Le mot de passe est stocké dans un fichier dont le nom contient des espaces.

```bash
bandit2@bandit:~$ ls -la
-rw-r-----   1 bandit3 bandit2   33 Jun 24 14:59 --spaces in this filename--
```

### 🔍 Découvertes

- Un nom de fichier contenant des espaces pose un problème similaire au niveau précédent : le shell découpe naturellement une commande selon les espaces, donc il interprète chaque mot du nom comme un argument séparé plutôt qu'un seul nom de fichier
- Deux solutions possibles pour gérer ça :
  - **Échapper chaque espace** avec un backslash :
```bash
    cat ./--spaces\ in\ this\ filename--
```
  - Ou **entourer le nom entier de guillemets** :
```bash
    cat "./--spaces in this filename--"
```

Et voici le mot de passe récupéré :

```bash
bandit2@bandit:~$ cat ./--spaces\ in\ this\ filename--
7ZZ2LFrykP2zEyvBl4m3clcL7tGYJPME
```

- Ce niveau renforce un réflexe essentiel en administration système et en sécurité : toujours anticiper les caractères spéciaux (espaces, tirets, guillemets) dans les noms de fichiers, que ce soit pour éviter des erreurs ou pour repérer des tentatives de dissimulation

### 🛠️ Commandes clés
`ls -la`, échappement avec `\ ` ou guillemets `"..."`

---
## Level 3 → Level 4

**Objectif** : Le mot de passe est stocké dans un fichier caché, quelque part dans le répertoire `inhere`.

```bash
bandit3@bandit:~$ ls -la
drwxr-xr-x   2 root root 4096 Jun 24 14:59 inhere

bandit3@bandit:~$ cd inhere/
bandit3@bandit:~/inhere$ ls -la
-rw-r----- 1 bandit4 bandit3   33 Jun 24 14:59 ...Hiding-From-You
```

### 🔍 Découvertes

- Un `ls` classique (sans option) ne montre que les fichiers "visibles" — sous Linux, tout fichier dont le nom commence par un point (`.`) est considéré comme **caché** par convention
- L'option `-a` (déjà utilisée depuis le début avec `ls -la`) est indispensable pour révéler ces fichiers cachés
- Ici, le nom du fichier (`...Hiding-From-You`) est volontairement trompeur : il commence par plusieurs points pour bien insister sur le concept de fichier caché, mais reste un nom de fichier valide comme un autre une fois qu'on sait qu'il existe
- Ce niveau rappelle un réflexe de base en investigation/pentest : ne jamais se fier à un simple `ls` sans vérifier aussi les fichiers cachés, que ce soit pour explorer un système ou auditer une configuration

```bash
bandit3@bandit:~/inhere$ cat ...Hiding-From-You
xzTXq1rDJQVVAzdv5cHq1TQytTWufAMq
```

### 🛠️ Commandes clés
`ls -la`, `cd`, `cat`

---
## Level 4 → Level 5

**Objectif** : Un des 10 fichiers du dossier `inhere` contient le mot de passe, mais tous n'ont pas la même nature — un seul est un fichier texte ASCII lisible.

```bash
bandit4@bandit:~/inhere$ ls -la
-rw-r----- 1 bandit5 bandit4   33 Jun 24 14:59 -file00
-rw-r----- 1 bandit5 bandit4   33 Jun 24 14:59 -file01
...
-rw-r----- 1 bandit5 bandit4   33 Jun 24 14:59 -file09
```

### 🔍 Découvertes

- Plutôt que d'ouvrir chaque fichier un par un, la commande `file` permet d'identifier le **type réel** de chaque fichier, indépendamment de son extension ou de son nom :

```bash
bandit4@bandit:~/inhere$ file ./*
./-file00: data
./-file01: data
...
./-file06: OpenPGP Public Key
./-file07: ASCII text
./-file08: data
./-file09: Motorola S-Record; binary data in text format
```

- Cette analyse révèle immédiatement que seul `-file07` est du texte ASCII lisible — les autres sont soit des données binaires brutes, soit des formats spécifiques (clé OpenPGP, encodage Motorola S-Record)
- Comme les noms de fichiers commencent tous par un tiret (piège déjà rencontré au Level 1), le préfixe `./` reste indispensable pour que le shell les traite correctement

```bash
bandit4@bandit:~/inhere$ cat ./-file07
6C7h9GD8M6ai5nr7wo1RonrzFjj9yIrG
```

### 🛠️ Commandes clés
`ls -la`, `file ./*`, `cat`

---
## Level 5 → Level 6

**Objectif** : Le mot de passe se trouve dans un fichier caché parmi 20 sous-dossiers (`maybehere00` à `maybehere19`), avec des critères précis : le fichier fait exactement 1033 octets.

```bash
bandit5@bandit:~/inhere$ ls -la
drwxr-x---  2 root bandit5 4096 Jun 24 14:59 maybehere00
drwxr-x---  2 root bandit5 4096 Jun 24 14:59 maybehere01
...
drwxr-x---  2 root bandit5 4096 Jun 24 14:59 maybehere19
```

### 🔍 Découvertes

- Chercher fichier par fichier dans 20 sous-dossiers à la main serait beaucoup trop long — c'est typiquement le genre de situation où `find` devient indispensable, en combinant plusieurs critères de recherche à la fois
- La commande `find` permet de filtrer par **type** (`-type f` pour ne cibler que les fichiers, pas les dossiers) et par **taille exacte** (`-size 1033c`, le `c` signifiant "en octets") :

```bash
bandit5@bandit:~/inhere$ find ./* -type f -size 1033c
./maybehere07/.file2
```

- Cette seule commande balaie récursivement toute l'arborescence et isole immédiatement le fichier correspondant, même s'il est caché (nom commençant par un point) et enfoui dans un sous-dossier
- Ce niveau illustre la puissance de `find` face à une exploration manuelle : dès qu'on connaît un ou plusieurs attributs distinctifs d'un fichier (taille, type, date de modification, permissions...), `find` permet de le localiser en une seule commande, quelle que soit la profondeur de l'arborescence

```bash
bandit5@bandit:~/inhere$ cat ./maybehere07/.file2
pXa26xhMWaC2SvDotA4r9EgZkulOeSBW
```

### 🛠️ Commandes clés
`ls -la`, `find -type f -size Xc`, `cat`

---
## Level 6 → Level 7

**Objectif** : Le mot de passe du niveau suivant ne se trouve **plus dans le répertoire personnel**, mais quelque part sur le système entier. Trois critères permettent de l'identifier : il appartient à l'utilisateur `bandit7`, au groupe `bandit6`, et fait exactement 33 octets.

### 🔍 Découvertes

**Première tentative (infructueuse)** : chercher uniquement dans le répertoire courant ne donne aucun résultat, ce qui confirme que le fichier n'est pas local :

```bash
bandit6@bandit:~$ find ./ -user bandit7 -group bandit6
(aucun résultat)
```

**Élargir la recherche à tout le système** : en partant de la racine (`/`) plutôt que du répertoire courant, `find` peut explorer l'intégralité de l'arborescence Linux :

```bash
bandit6@bandit:~$ find / -user bandit7 -group bandit6 -size 33c 2>/dev/null
/var/lib/dpkg/info/bandit7.password
```

- Le `2>/dev/null` est essentiel ici : en explorant tout le système depuis `/`, la commande tente d'accéder à des dossiers protégés (`/proc`, `/root`, etc.) et génère énormément d'erreurs "Permission denied". Rediriger le flux d'erreur (`2>`) vers `/dev/null` permet de ne garder que les résultats utiles à l'écran

**Lire directement le résultat avec `xargs`** : plutôt que de copier le chemin renvoyé par `find` puis de faire un `cat` séparé, on peut chaîner les deux étapes en une seule commande :

```bash
bandit6@bandit:~$ find / -user bandit7 -group bandit6 -size 33c 2>/dev/null | xargs cat
Bmnnvf82KzQlfxgAI2d1zYbr1u9pr3E3
```

- `xargs` prend en entrée le résultat texte renvoyé par `find` (ici, le chemin du fichier) et le transforme automatiquement en **argument** pour la commande qui suit — ici `cat`. Concrètement, `find ... | xargs cat` revient à exécuter `cat /var/lib/dpkg/info/bandit7.password` directement, sans avoir à copier-coller le chemin à la main
- C'est particulièrement utile quand `find` renvoie plusieurs résultats à la fois : `xargs` peut alors enchaîner la commande sur chacun d'eux automatiquement, un par un

**Variante utile pour explorer plus largement** : `find / -user bandit7 -ls` (sans filtre de groupe ni de taille) affiche un résultat façon `ls -l` pour chaque fichier trouvé — pratique pour visualiser rapidement les permissions, propriétaire et taille de plusieurs fichiers candidats en une seule commande, avant d'affiner la recherche

- Ce niveau marque une étape importante : il introduit la nécessité d'explorer **tout le système de fichiers**, pas seulement son propre répertoire, et montre comment chaîner des commandes efficacement plutôt que de traiter chaque étape manuellement

### 🛠️ Commandes clés
`find / -user X -group Y -size Zc`, `find / -user X -ls`, `| xargs cat`, redirection d'erreur `2>/dev/null`, `cat`

---
## Level 7 → Level 8

**Objectif** : Le mot de passe se trouve dans le fichier `data.txt`, à côté du mot **"millionth"**.

```bash
bandit7@bandit:~$ ls -la
-rw-r-----   1 bandit8 bandit7 18530 Jun 24 14:59 data.txt
```

### 🔍 Découvertes

- Le fichier `data.txt` contient beaucoup de données, mais le mot de passe est associé au mot-clé "millionth". Il faut donc chercher spécifiquement cette occurrence parmi tout le contenu
- `grep` est l'outil idéal ici : il filtre et n'affiche que les lignes correspondant à un motif

```bash
bandit7@bandit:~$ grep "millionth" data.txt
millionth       VR1ljMayciFxbnUokuQmJFw6QC9VKtub
```

- `grep` cherche un motif texte dans un fichier (ou une entrée standard) et affiche les lignes qui correspondent. C'est un outil fondamental pour l'analyse de logs, la recherche dans des fichiers de configuration, et bien d'autres usages en sécurité
- Contrairement à `find` (qui cherche des fichiers selon leurs attributs comme la taille ou le propriétaire), `grep` cherche **à l'intérieur** du contenu des fichiers — les deux sont complémentaires
- Le résultat montre le mot "millionth" suivi d'une tabulation et du mot de passe — un format clé-valeur classique qu'on retrouve souvent dans les fichiers de configuration

### 🛠️ Commandes clés
`grep "motif" fichier`

---
## Level 8 → Level 9

**Objectif** : Le fichier `data.txt` contient de nombreuses lignes, mais une seule d'entre elles apparaît **une seule fois** — c'est elle qui contient le mot de passe.

```bash
bandit8@bandit:~$ ls -la
-rw-r-----   1 bandit9 bandit8 33033 Jun 24 14:59 data.txt
```

### 🔍 Découvertes

**Première tentative (erreur de syntaxe)** : un tiret placé par erreur devant `uniq` le transforme en option invalide plutôt qu'en nom de commande :

```bash
bandit8@bandit:~$ sort data.txt | -uniq -u
Command '-uniq' not found
```

**Solution — combiner `sort` et `uniq -u`** : la commande `uniq` ne peut détecter des doublons que sur des lignes **déjà côte à côte**, d'où la nécessité de trier le fichier au préalable avec `sort`. L'option `-u` de `uniq` affiche uniquement les lignes qui n'ont **aucun doublon** dans tout le fichier :

```bash
bandit8@bandit:~$ sort data.txt | uniq -u
EjmOSvuAu7sGAHqHVcBDPirRe9T03kxl
```

Cette seule commande isole directement la ligne unique recherchée.

**Vérification/exploration alternative avec comptage** : pour visualiser concrètement combien de fois chaque ligne apparaît (utile pour comprendre le raisonnement avant de foncer sur `-u`), on peut combiner `uniq -c` (compte les occurrences) avec un second `sort -n` (tri numérique croissant sur ce compteur) :

```bash
bandit8@bandit:~$ sort data.txt | uniq -c | sort -n | head
      1 EjmOSvuAu7sGAHqHVcBDPirRe9T03kxl
     10 08Jd2vmb6FjR4zXPteGHhpJm8A0OOA5B
     10 0dEKX1sDwYtc4vyjrKpGu30ecWBsDDa9
     ...
```

Ce résultat confirme visuellement qu'une seule ligne a un compteur à `1` (apparaît une seule fois), pendant que toutes les autres reviennent 10 fois chacune — exactement le résultat qu'on obtient plus directement avec `uniq -u`.

- Ce niveau illustre une combinaison très classique en traitement de texte sous Linux : `sort | uniq` pour dédupliquer, analyser ou isoler des lignes selon leur fréquence d'apparition — une compétence utile aussi bien pour explorer un fichier de logs que pour repérer une anomalie dans un jeu de données

### 🛠️ Commandes clés
`sort data.txt | uniq -u`, `sort data.txt | uniq -c | sort -n`

---
## Level 9 → Level 10

**Objectif** : Le fichier `data.txt` contient majoritairement des données binaires, mais une poignée de chaînes lisibles s'y trouve — le mot de passe est précédé de plusieurs caractères `=`.

```bash
bandit9@bandit:~$ ls -la
-rw-r-----   1 bandit10 bandit9 19382 Jun 24 14:58 data.txt
```

### 🔍 Découvertes

**Première tentative (échec)** : un `grep` classique sur un fichier binaire refuse d'afficher le détail des correspondances :

```bash
bandit9@bandit:~$ cat data.txt | grep =
grep: (standard input): binary file matches
```

`grep` détecte la présence d'octets non-textuels dans le fichier et, par mesure de précaution, se contente d'annoncer qu'une correspondance existe sans l'afficher en détail.

**Solution — forcer le traitement en texte avec `-a`** : cette option indique à `grep` de traiter le fichier comme du texte pur, peu importe son contenu réel, et donc d'afficher les lignes correspondantes normalement :

```bash
bandit9@bandit:~$ grep -a '==.*[a-zA-Z0-9]$' data.txt
========== B0s2khmbT9u0geKuOoVGW3JZKhndE3BG
```

L'expression régulière `==.*[a-zA-Z0-9]$` cible précisément une ligne qui contient une séquence de `=`, suivie de n'importe quels caractères, se terminant par un caractère alphanumérique — exactement le motif attendu autour du mot de passe.

**Approche alternative en Python** : plutôt que de dépendre de `grep` et du symbole `=`, on peut ouvrir le fichier en lecture binaire et chercher directement une séquence de 32 caractères alphanumériques consécutifs (la longueur type des mots de passe Bandit) :

```python
import re

with open("data.txt", "rb") as f:
    buff = f.read()

match = re.search(rb"[a-zA-Z0-9]{32}", buff)
if match:
    print(match.group().decode())
```

Ou directement en une ligne depuis le terminal, sans ouvrir l'interpréteur interactif :

```bash
bandit9@bandit:~$ python3 -c "import re; print(re.search(rb'[a-zA-Z0-9]{32}', open('data.txt','rb').read()).group().decode())"
```

**Explication du script :**
- `open("data.txt", "rb")` : ouverture en mode **binaire** (`rb` = read binary), indispensable puisque le fichier contient des octets non-textuels que Python ne saurait pas décoder proprement en mode texte classique
- `re.search(rb"[a-zA-Z0-9]{32}", buff)` : recherche la première séquence de **32 caractères alphanumériques consécutifs** dans le buffer binaire — le préfixe `rb` devant le motif indique qu'il s'agit d'une regex appliquée à des données binaires (bytes), pas à une chaîne de caractères classique
- `.group()` : récupère la correspondance trouvée (sous forme de bytes)
- `.decode()` : convertit ces bytes en chaîne de caractères lisible pour l'affichage final

Cette méthode Python est plus robuste que le `grep`, car elle ne dépend pas d'un indice visuel comme les `=` : elle se base uniquement sur la structure attendue du mot de passe (32 caractères alphanumériques), ce qui fonctionnerait même si le format d'affichage du fichier changeait.

- Ce niveau illustre une limite importante de `grep` : par défaut, il n'affiche pas le contenu des fichiers qu'il détecte comme binaires. L'option `-a` permet de contourner cette limite, tandis que Python offre une alternative plus flexible pour des recherches basées sur un pattern structurel plutôt que sur un simple mot-clé

### 🛠️ Commandes clés
`grep -a 'motif' fichier`, expressions régulières, `python3 -c`, module `re` (`re.search`, `rb"..."`)

---
## Level 10 → Level 11

**Objectif** : Le mot de passe est encodé en base64 dans le fichier `data.txt`.

```bash
bandit10@bandit:~$ ls -la
-rw-r-----   1 bandit11 bandit10   69 Jun 24 14:58 data.txt

bandit10@bandit:~$ cat data.txt
VGhlIHBhc3N3b3JkIGlzIHBZZk9ZNkh3VXNEajVyTDlVdnloVTdNQ212OHZONVJvCg==
```

### 🔍 Découvertes

- Le contenu affiché ne ressemble à aucun texte lisible directement, mais sa structure — uniquement des lettres, chiffres, et un padding `==` à la fin — est caractéristique de l'encodage **base64**, une méthode qui convertit des données binaires en texte ASCII imprimable
- La commande `base64` avec l'option `-d` (decode) permet de décoder ce type de contenu instantanément :

```bash
bandit10@bandit:~$ cat data.txt | base64 -d
The password is pYfOY6HwUsDj5rL9UvyhU7MCmv8vN5Ro
```

- Le base64 n'est **pas un chiffrement** — c'est un simple encodage, réversible sans clé ni mot de passe. Il est couramment utilisé pour transporter des données binaires dans des contextes texte (emails, URLs, tokens) mais n'offre aucune confidentialité en soi. En sécurité offensive, reconnaître visuellement une chaîne encodée en base64 (souvent terminée par `=` ou `==`) est un réflexe important, car ce type d'encodage cache parfois des informations sensibles (identifiants, tokens, payloads) juste devant les yeux
- Ce niveau initie à la reconnaissance des formats d'encodage courants, une compétence qui reviendra régulièrement en CTF (base64, hex, URL encoding, ROT13...)

### 🛠️ Commandes clés
`cat fichier | base64 -d`

---
## Level 11 → Level 12

**Objectif** : Le mot de passe est chiffré avec ROT13 dans le fichier `data.txt`.

```bash
bandit11@bandit:~$ ls -la
-rw-r-----   1 bandit12 bandit11   49 Jun 24 14:58 data.txt

bandit11@bandit:~$ cat data.txt
Gur cnffjbeq vf TEBbmJCB8DlA0zTewHxVQ0JPLxMvDkeA
```

### 🔍 Découvertes

- Le texte affiché ressemble à du texte normal (mots, espaces, structure de phrase), mais illisible tel quel — signe caractéristique d'un **chiffrement par substitution** plutôt que d'un encodage comme le base64 vu au niveau précédent
- **ROT13** est un chiffrement de César simplifié : chaque lettre est décalée de 13 positions dans l'alphabet. Comme l'alphabet compte 26 lettres, appliquer ROT13 une seconde fois annule le chiffrement — c'est une transformation symétrique
- La commande `tr` (translate) permet de substituer un jeu de caractères par un autre, caractère par caractère :

```bash
bandit11@bandit:~$ echo "Gur cnffjbeq vf TEBbmJCB8DlA0zTewHxVQ0JPLxMvDkeA" | tr 'N-ZA-Mn-za-m' 'A-Za-z'
The password is GROozWPO8QyN0mGrjUkID0WCYkZiQxrN
```

- Le principe de `tr 'N-ZA-Mn-za-m' 'A-Za-z'` : chaque lettre du premier jeu de caractères (`N-ZA-Mn-za-m`, soit l'alphabet décalé de 13 positions) est remplacée par la lettre correspondante du second jeu (`A-Za-z`, l'alphabet standard) — ce qui revient exactement à appliquer un décalage ROT13
- Ce niveau illustre un autre type de transformation réversible à reconnaître rapidement : contrairement au base64 (encodage de données binaires en texte), ROT13 est historiquement utilisé pour masquer un texte de façon très légère (spoilers, blagues, contenu sensible non critique) — jamais pour une réelle sécurité, sa "clé" étant fixe et connue de tous

### 🛠️ Commandes clés
`cat`, `tr 'N-ZA-Mn-za-m' 'A-Za-z'` (ou tout outil dédié type `rot13`)

---
## Level 12 → Level 13

**Objectif** : Le fichier `data.txt` contient un dump hexadécimal (format `xxd`) d'une archive compressée plusieurs fois de suite — il faut décompresser couche par couche jusqu'à atteindre le mot de passe en clair.

### 🔍 Découvertes

**Étape 1 — Travailler dans `/tmp`**

Le répertoire personnel de Bandit est en écriture désactivée ; il faut donc créer un espace de travail temporaire dans `/tmp` pour manipuler les fichiers extraits :

```bash
bandit12@bandit:~$ mkdir /tmp/out
bandit12@bandit:~$ cp data.txt /tmp/out
bandit12@bandit:~$ cd /tmp/out
```

**Étape 2 — Reconstituer le binaire à partir du dump hexadécimal**

Le contenu de `data.txt` n'est pas directement un fichier compressé : c'est sa représentation en hexadécimal (générée par `xxd`), reconnaissable au format `adresse: octets  texte` :

```bash
bandit12@bandit:/tmp/out$ cat data.txt
00000000: 1f8b 0808 b2f0 3b6a 0203 6461 7461 322e  ......;j..data2.
00000010: 6269 6e00 0142 02bd fd42 5a68 3931 4159  bin..B...BZh91AY
...
```

L'option `-r` de `xxd` permet de faire l'opération **inverse** : reconvertir ce dump hexadécimal en données binaires réelles :

```bash
bandit12@bandit:/tmp/out$ cat data.txt | xxd -r > out
bandit12@bandit:/tmp/out$ file out
out: gzip compressed data, was "data2.bin"...
```

**Étape 3 — Décompresser couche par couche**

La commande `file` révèle à chaque étape le type réel du fichier obtenu, indépendamment de son nom. Il a fallu enchaîner plusieurs décompressions successives, chaque étape produisant un nouveau format à identifier :

```bash
# Couche 1 : gzip
bandit12@bandit:/tmp/out$ mv out out.gz
bandit12@bandit:/tmp/out$ gzip -d out.gz
bandit12@bandit:/tmp/out$ file out
out: bzip2 compressed data, block size = 900k

# Couche 2 : bzip2
bandit12@bandit:/tmp/out$ mv out out.bz2
bandit12@bandit:/tmp/out$ bzip2 -d out.bz2
bandit12@bandit:/tmp/out$ file out
out: gzip compressed data, was "data4.bin"...

# Couche 3 : gzip
bandit12@bandit:/tmp/out$ mv out out.gz
bandit12@bandit:/tmp/out$ gzip -d out.gz
bandit12@bandit:/tmp/out$ file out
out: POSIX tar archive (GNU)

# Couche 4 : tar
bandit12@bandit:/tmp/out$ tar xvf out
data5.bin
bandit12@bandit:/tmp/out$ file data5.bin
data5.bin: POSIX tar archive (GNU)

# Couche 5 : tar (encore)
bandit12@bandit:/tmp/out$ tar xvf data5.bin
data6.bin
bandit12@bandit:/tmp/out$ file data6.bin
data6.bin: bzip2 compressed data, block size = 900k

# Couche 6 : bzip2
bandit12@bandit:/tmp/out$ mv data6.bin data.bz2
bandit12@bandit:/tmp/out$ bzip2 -d data.bz2
bandit12@bandit:/tmp/out$ file data
data: POSIX tar archive (GNU)

# Couche 7 : tar
bandit12@bandit:/tmp/out$ tar xvf data
data8.bin
bandit12@bandit:/tmp/out$ file data8.bin
data8.bin: gzip compressed data, was "data9.bin"...

# Couche 8 : gzip (la dernière)
bandit12@bandit:/tmp/out$ mv data8.bin data.gz
bandit12@bandit:/tmp/out$ gzip -d data.gz
bandit12@bandit:/tmp/out$ file data
data: ASCII text
bandit12@bandit:/tmp/out$ cat data
The password is qQYQiHOBPR8zR61qxYqX45quvihF2uzk
```

- Le principe central de ce niveau : **ne jamais se fier à l'extension attendue**, toujours vérifier avec `file` avant d'agir — chaque type de compression nécessite un outil différent (`gzip -d`, `bzip2 -d`, `tar xvf`), et se tromper d'outil échoue immédiatement
- Renommer chaque fichier intermédiaire avec l'extension correcte (`.gz`, `.bz2`) avant de le décompresser évite les erreurs de certains outils qui exigent une extension cohérente pour fonctionner correctement
- Ce niveau simule une situation réaliste en forensic/reverse engineering : des données peuvent être imbriquées dans plusieurs couches d'encodage ou de compression, et il faut les éplucher méthodiquement, une couche à la fois, jusqu'au contenu final

**Petite variante d'organisation** : plutôt que de renommer manuellement en `out`/`out.gz`/`out.bz2` à chaque étape (source de confusion si on perd le fil), il peut être plus lisible de nommer chaque fichier decompressé avec un numéro de couche croissant (`data1.bin`, `data2.bin`, `data3.bin`...) pour garder une trace claire de la progression.

### 🛠️ Commandes clés
`xxd -r`, `file`, `gzip -d`, `bzip2 -d`, `tar xvf`, `mv`

---
## Level 13 → Level 14

**Objectif** : Une clé SSH privée est fournie directement dans le répertoire personnel — il faut l'utiliser pour s'authentifier sur le compte suivant, sans mot de passe.

```bash
bandit13@bandit:~$ ls -la
-rw-r-----   1 bandit14 bandit13  467 Jun 24 14:59 HINT
-rw-r-----   1 bandit14 bandit13 2602 Jun 24 14:59 sshkey.private
```

### 🔍 Découvertes

- Ce niveau introduit un mode d'authentification différent des précédents : au lieu d'un mot de passe, on utilise une **paire de clés SSH** (ici, seule la clé privée est fournie, à utiliser pour prouver son identité)
- Le fichier `HINT` précise un point clé : les versions récentes d'OverTheWire empêchent de rebondir d'un niveau à l'autre via `localhost` — il faut donc se reconnecter depuis sa propre machine plutôt que de tenter un `ssh` en boucle depuis l'intérieur du serveur

**Méthode 1 — Récupérer la clé avec `scp`**

Plutôt que de copier-coller le contenu affiché par `cat` (source d'erreurs si le formatage est corrompu par le terminal), la commande `scp` (Secure Copy) permet de transférer le fichier proprement depuis le serveur distant vers sa propre machine :

```bash
scp -P 2220 bandit13@bandit.labs.overthewire.org:sshkey.private ~/
```

- `-P 2220` : précise le port SSH non-standard (comme pour toute connexion à Bandit)
- `bandit13@bandit...:sshkey.private` : chemin distant du fichier à récupérer
- `~/` : destination locale (ici, le répertoire personnel)

Le transfert réussi s'affiche avec une barre de progression et le résumé de la vitesse/taille :

```bash
sshkey.private    100% 2602    6.2KB/s   00:00
```

**Méthode 2 — Copier-coller manuel avec `nano` + permissions `chmod`**

Alternative sans `scp` : ouvrir un éditeur en local, coller manuellement le contenu de la clé (récupéré via `cat sshkey.private` sur le serveur), puis sauvegarder :

```bash
nano sshkey.private
# coller le contenu affiché par cat sur le serveur, puis sauvegarder (Ctrl+O, Entrée, Ctrl+X)
```

Cette méthode impose une étape supplémentaire indispensable : SSH **refuse d'utiliser une clé privée dont les permissions sont trop ouvertes** (lisible par d'autres utilisateurs), par mesure de sécurité. Il faut donc restreindre les droits du fichier pour qu'il ne soit accessible qu'à son propriétaire :

```bash
chmod 600 sshkey.private
```

`600` signifie : lecture et écriture uniquement pour le propriétaire du fichier, aucun droit pour le groupe ni les autres utilisateurs. Sans cette commande, `ssh` refuserait la clé avec une erreur du type `UNPROTECTED PRIVATE KEY FILE!`.

**Étape finale — Se connecter avec la clé privée**

L'option `-i` (identity file) de `ssh` permet de spécifier une clé privée à utiliser pour l'authentification, au lieu du mot de passe habituel :

```bash
ssh -i sshkey.private bandit14@bandit.labs.overthewire.org -p 2220
```

- Une fois connecté, le mot de passe du niveau suivant est disponible directement dans `/etc/bandit_pass/bandit14` :

```bash
bandit14@bandit:~$ cat /etc/bandit_pass/bandit14
aaWecNkG4FhxJQxz07uiwzVP6bJiYS65
```

- Ce niveau illustre un mécanisme d'authentification omniprésent en administration système et en sécurité : l'authentification par **clé publique/privée**, bien plus robuste qu'un simple mot de passe car elle repose sur de la cryptographie asymétrique. Il illustre aussi une bonne pratique systématiquement appliquée par SSH : une clé privée mal protégée (permissions trop larges) est refusée par principe, pour éviter qu'elle soit lisible par n'importe quel utilisateur du système

### 🛠️ Commandes clés
`scp -P port user@host:fichier destination`, `nano` (copier-coller manuel), `chmod 600 fichier`, `ssh -i clé_privée user@host -p port`

---
## Level 14 → Level 15

**Objectif** : Le mot de passe du niveau suivant est déjà connu (celui du niveau 14, obtenu à l'étape précédente), mais il faut l'envoyer à un service en écoute sur le **port 30000** en local, pour recevoir en retour le mot de passe du niveau 15.

### 🔍 Découvertes

**Première tentative (erreur de syntaxe)** : coller le port directement après `localhost` avec `:` ne fonctionne pas avec `nc` (contrairement à la syntaxe d'une URL classique) :

```bash
bandit14@bandit:~$ echo "motdepasse" | nc localhost:30000
nc: missing port number
```

**Solution — séparer l'hôte et le port par un espace** : `netcat` (`nc`) attend l'adresse et le port comme deux arguments distincts, pas comme une seule chaîne concaténée :

```bash
bandit14@bandit:~$ echo "motdepasse" | nc localhost 30000
Correct!
pbLYuZtTg4MgaqfJx8jbA9gKKGqM68A7
```

- `netcat` est un outil polyvalent permettant d'établir des connexions réseau brutes en TCP/UDP — ici, il ouvre une connexion vers `localhost` sur le port `30000`, envoie le contenu reçu via le pipe (`echo | nc`), puis affiche la réponse du service distant
- Ce service local semble donc valider le mot de passe transmis, et renvoie automatiquement le mot de passe du niveau suivant en cas de succès
- Ce niveau constitue une première approche des **communications réseau par socket** : envoyer des données brutes à un port ouvert et interpréter la réponse — une compétence essentielle en exploitation de services réseau, qu'on retrouve constamment en CTF (interaction avec des ports web, des services custom, etc.)

### 🛠️ Commandes clés
`echo "texte" | nc host port`

---
## Level 15 → Level 16

**Objectif** : Le port `30001` attend une connexion, mais cette fois en **TLS/SSL** plutôt qu'en clair — il faut envoyer le mot de passe du niveau 15 via une connexion chiffrée pour recevoir le mot de passe suivant.

### 🔍 Découvertes

- Une simple connexion `nc` classique (comme au niveau précédent) échouerait ici : le service exige un handshake TLS avant d'accepter la moindre donnée
- La commande `openssl s_client` permet d'établir une connexion chiffrée en imitant un client SSL/TLS, exactement comme le ferait un navigateur avec un site HTTPS :

```bash
bandit15@bandit:~$ openssl s_client -connect localhost:30001
```

- Le certificat présenté par le serveur est **auto-signé** (`self-signed certificate`), ce qui déclenche un avertissement de vérification (`verify error:num=18`) — normal dans ce contexte d'entraînement où le serveur n'a pas de certificat validé par une autorité de certification reconnue. En usage réel, ce type d'avertissement serait un signal d'alerte à ne jamais ignorer, mais ici il n'empêche pas la connexion de s'établir
- Une fois le handshake TLS terminé, la connexion se comporte comme un terminal interactif classique : on peut taper le mot de passe du niveau précédent directement, et le service répond en clair (à travers le tunnel chiffré) :

```bash
[handshake TLS...]
pbLYuZtTg4MgaqfJx8jbA9gKKGqM68A7
Correct!
kS0Hf0u5HiXFwKMKFqXvPdOTNGGa0X8V
```

- Ce niveau introduit un principe fondamental de sécurité réseau : la différence entre une **connexion en clair** (comme `nc` au niveau précédent, où les données transitent sans protection) et une **connexion chiffrée** (TLS/SSL, où le contenu est protégé contre l'interception). C'est le même principe qui distingue HTTP de HTTPS sur le web
- `openssl s_client` est un outil précieux en sécurité offensive/défensive : il permet d'inspecter manuellement un certificat serveur, tester une configuration TLS, ou interagir avec n'importe quel service chiffré sans avoir besoin d'un client dédié

### 🛠️ Commandes clés
`openssl s_client -connect host:port`

---
## Level 16 → Level 17

**Objectif** : Le mot de passe précédent doit être envoyé au bon port parmi une plage de 1000 ports (31000-32000), en trouvant lequel accepte une connexion SSL et renvoie une clé privée SSH en récompense.

### 🔍 Découvertes

**Étape 1 — Scanner la plage de ports avec Nmap**

Plutôt que de tester port par port à la main, `nmap` permet de scanner toute la plage en une seule commande et d'identifier automatiquement quels ports sont ouverts et quel type de service y tourne :

```bash
bandit16@bandit:~$ nmap -sV -p31000-32000 --open -T5 localhost
```

- `-sV` : détection de version de service (essaie d'identifier ce qui tourne sur chaque port)
- `-p31000-32000` : restreint le scan à la plage de ports pertinente pour ce niveau
- `--open` : n'affiche que les ports réellement ouverts (filtre le bruit)
- `-T5` : vitesse de scan maximale, pour accélérer l'exploration d'une plage de 1000 ports

Résultat :
```
PORT STATE SERVICE VERSION
31046/tcp open echo
31518/tcp open ssl/echo
31691/tcp open echo
31790/tcp open ssl/unknown
31960/tcp open echo
```
Sur les 5 ports ouverts, seuls deux utilisent SSL (`31518` et `31790`). Le port `31790` est identifié comme `ssl/unknown` — un service chiffré dont Nmap ne reconnaît pas précisément la nature, ce qui en fait le candidat le plus probable pour ce niveau (les simples `echo` renvoient juste ce qu'on leur envoie, sans logique d'authentification).

**Étape 2 — Première tentative avec `openssl s_client` (échec)**

En envoyant le mot de passe directement dans une session interactive `openssl s_client`, la réponse du serveur indique un échec :

```bash
bandit16@bandit:~$ openssl s_client -connect localhost:31790
[handshake TLS...]
kS0Hf0u5HiXFwKMKFqXvPdOTNGGa0X8V
KEYUPDATE

Wrong! Please enter the correct current password.
```

Le problème ici n'est pas le mot de passe (qui est correct), mais la façon dont `openssl s_client` gère la fin de la connexion en mode interactif : sans configuration particulière, la commande peut fermer prématurément le flux ou mal transmettre les données selon le contexte.

**Étape 3 — Solution : ajouter l'option `-ign_eof`**

L'option `-ign_eof` indique à `openssl s_client` de ne pas fermer la connexion à la fin de l'entrée standard (EOF), ce qui laisse le temps au serveur de traiter correctement les données envoyées :

```bash
bandit16@bandit:~$ echo "kS0Hf0u5HiXFwKMKFqXvPdOTNGGa0X8V" | openssl s_client -connect localhost:31790 -ign_eof
[handshake TLS...]
Correct!
-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----
```

Cette fois, le serveur valide le mot de passe et renvoie directement une **clé privée SSH complète**, à utiliser pour se connecter au niveau suivant.

**Alternative plus simple — `ncat --ssl`**

`ncat` (version améliorée de `netcat`, incluse avec Nmap) gère nativement les connexions SSL sans nécessiter d'options supplémentaires comme `-ign_eof` :

```bash
bandit16@bandit:~$ ncat --ssl localhost 31790
motdepasse
Correct!
-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----
```

`ncat --ssl` établit directement une connexion chiffrée, sans afficher tous les détails du handshake TLS comme le fait `openssl s_client` — plus direct pour ce genre d'interaction simple.

**Étape 4 — Récupérer et utiliser la clé privée**

Une fois la clé copiée dans un fichier local (via `scp`, ou copier-coller dans `nano` comme vu au Level 13), il faut lui appliquer les permissions strictes attendues par SSH avant de pouvoir l'utiliser :

```bash
chmod 600 sshkey_bandit17.private
ssh -i sshkey_bandit17.private bandit17@bandit.labs.overthewire.org -p 2220
```

- Ce niveau combine plusieurs compétences déjà vues (scan réseau, connexions SSL, authentification par clé) dans un scénario plus complet : il faut d'abord **découvrir** le bon service parmi plusieurs candidats avant de pouvoir l'exploiter — une démarche très proche de la reconnaissance réseau en pentest réel
- La différence entre `openssl s_client` et `ncat --ssl` illustre aussi qu'il existe souvent plusieurs outils pour une même tâche (ici, établir une connexion TLS), chacun avec ses subtilités de comportement — savoir en connaître plusieurs permet de contourner les blocages spécifiques à un outil

### 🛠️ Commandes clés
`nmap -sV -p<plage> --open -T5 host`, `openssl s_client -connect host:port -ign_eof`, `ncat --ssl host port`, `chmod 600`, `ssh -i`

---
## Level 17 → Level 18

**Objectif** : Dans le répertoire personnel, deux fichiers sont présents : `passwords.old` et `passwords.new`. La ligne qui **a changé** entre les deux dans `passwords.new` est le mot de passe du niveau suivant.

### 🔍 Découvertes

- Ouvrir chaque fichier à la main pour repérer la différence serait fastidieux — `diff` est conçu exactement pour ça

```bash
bandit17@bandit:~$ diff passwords.old passwords.new
42c42
< 09LJK5b0qSg3lyERWxQ9bX54xM5o5Umk
---
> OQxXZjELndr90zuhOTDYBEomI0SZITXI
```

- `diff` compare deux fichiers ligne par ligne et affiche leurs différences. Le symbole `<` indique le contenu du premier fichier, `>` celui du second. La ligne qui apparaît après `>` dans `passwords.new` est celle qui a été **rajoutée ou modifiée** — c'est le mot de passe
- Ce niveau introduit `diff`, un outil incontournable pour comparer des fichiers de configuration, repérer des modifications non autorisées dans des fichiers système, ou simplement identifier visuellement ce qui a changé entre deux versions d'un même fichier

### 🛠️ Commandes clés
`diff fichier1 fichier2`

---
## Level 18 → Level 19

**Objectif** : En se connectant en SSH, la session se ferme immédiatement avec le message "ByeBye !". Il faut trouver un moyen d'exécuter une commande avant que la session ne soit coupée.

```bash
ssh -p 2220 bandit18@bandit.labs.overthewire.org
...
ByeBye !
Connection to bandit.labs.overthewire.org closed.
```

### 🔍 Découvertes

- Le shell de connexion (défini dans `/etc/passwd` ou le fichier `.bashrc`) est configuré pour se fermer immédiatement — normalement, impossible d'avoir un shell interactif
- Solution : SSH permet de passer **une commande directement en argument**, qui sera exécutée avant que le shell ne se ferme, et le résultat sera renvoyé :

```bash
ssh -p 2220 bandit18@bandit.labs.overthewire.org "cat ~/readme"
KpsOfPkcP7i1FlIExk2QEjyt6dw8dxZI
```

- En passant la commande directement dans l'invocation SSH (entre guillemets), le shell distant exécute `cat ~/readme` et affiche son contenu **avant** que la connexion ne soit interrompue
- Une autre approche possible : `ssh -t` force l'allocation d'un pseudo-terminal, ce qui peut parfois contourner ce genre de restriction pour obtenir un shell interactif :

```bash
ssh -t -p 2220 bandit18@bandit.labs.overthewire.org /bin/bash
```

- Ce niveau illustre une technique defensive simple mais efficace : modifier le shell de connexion pour empêcher tout accès interactif. En pentest, ce type de restriction se contourne souvent en passant directement la commande souhaitée dans l'appel SSH

### 🛠️ Commandes clés
`ssh user@host "commande"`, `ssh -t user@host /bin/bash`

---
## Level 19 → Level 20

**Objectif** : Un binaire setuid nommé `bandit20-do` est présent dans le répertoire personnel. Il permet d'exécuter des commandes **en tant que l'utilisateur bandit20**.

```bash
bandit19@bandit:~$ ls -la
-rwsr-x---   1 bandit20 bandit19 14880 Jun 24 14:58 bandit20-do
```

### 🔍 Découvertes

- Le `s` à la place du `x` dans les permissions (`rws` au lieu de `rwx`) indique que le bit **setuid** (SUID) est activé. Cela signifie que le programme s'exécute avec les privilèges de son **propriétaire** (`bandit20`), quel que soit l'utilisateur qui le lance
- Ce binaire fonctionne comme un `sudo` simplifié : on lui passe une commande en argument, et il l'exécute en tant que `bandit20` :

```bash
bandit19@bandit:~$ ./bandit20-do whoami
bandit20

bandit19@bandit:~$ ./bandit20-do cat /etc/bandit_pass/bandit20
4pIjcunZ0fK2vmp3IwfG8Vf7VhxD6pOA
```

- Les binaires SUID sont un mécanisme puissant mais risqué : un programme setuid mal configuré ou vulnérable peut permettre une **escalade de privilèges**, l'un des enjeux les plus importants en sécurité offensive
- Ce niveau introduit un concept qui reviendra très souvent en CTF et en pentest : repérer les binaires setuid (`find / -perm -4000`) et les exploiter pour gagner les droits d'un autre utilisateur

### 🛠️ Commandes clés
`./binaire commande`, `find / -perm -4000`

---
## Level 20 → Level 21

**Objectif** : Un binaire setuid `suconnect` se connecte à un port donné, envoie le mot de passe du niveau actuel, et reçoit le mot de passe du niveau suivant s'il est correct.

### 🔍 Découvertes

- Il faut d'abord lancer un **serveur d'écoute** avec `nc` sur un port choisi, en lui passant notre mot de passe actuel via un `echo` en pipe :

```bash
# Terminal 1 : lancer l'écoute avec le mot de passe
bandit20@bandit:~$ echo "4pIjcunZ0fK2vmp3IwfG8Vf7VhxD6pOA" | nc -l -p 1234 &
```

- Puis lancer `suconnect` dans le même terminal (ou un autre) en le connectant au même port :

```bash
bandit20@bandit:~$ ./suconnect 1234
Read: 4pIjcunZ0fK2vmp3IwfG8Vf7VhxD6pOA
Password matches, sending next password
bW9kBv5WC3P4yoDyf12LSdGuNz5ka6hY
```

- `nc -l -p PORT` : `nc` en mode **écoute** (`-l`) sur un port donné (`-p`). Il attend une connexion entrante, puis envoie les données qu'on lui a passées via le pipe, avant d'afficher la réponse reçue
- `./suconnect PORT` : le binaire setuid se connecte au port spécifié, lit les données, les compare avec le mot de passe stocké, et si c'est correct, envoie le mot de passe du niveau suivant en retour
- Ce niveau combine serveur (`nc -l`) et client (`suconnect`) pour reproduire un échange réseau simple — exactement le même principe qu'une communication client-serveur en TCP

### 🛠️ Commandes clés
`echo "data" | nc -l -p port`, background (`&`)

---
## Level 21 → Level 22

**Objectif** : Un cron job s'exécute régulièrement. En examinant la configuration cron dans `/etc/cron.d/`, on peut identifier le script exécuté et comprendre son fonctionnement.

### 🔍 Découvertes

- Les tâches planifiées cron sont configurables dans `/etc/cron.d/` :

```bash
bandit21@bandit:~$ ls -la /etc/cron.d/
total 36
drwxr-xr-x   2 root root 4096 Jun 24 14:59 .
...
-rw-r--r--   1 root root  120 Jun 24 14:53 cronjob_bandit22
```

- Afficher le contenu de ce fichier révèle la configuration :

```bash
bandit21@bandit:~$ cat /etc/cron.d/cronjob_bandit22
@reboot bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
```

- Le script s'exécute toutes les minutes (`* * * * *`) en tant que `bandit22`. Examinons-le :

```bash
bandit21@bandit:~$ cat /usr/bin/cronjob_bandit22.sh
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```

- Le script écrit le mot de passe de `bandit22` dans un fichier temporaire (`/tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv`), et le rend lisible par tous (`chmod 644`) :

```bash
bandit21@bandit:~$ cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
RYVux2rHEm9tiXHmLFzuR7Vhx6AZQMEz
```

- Ce niveau illustre un problème de sécurité classique : stocker des mots de passe ou des tokens dans des fichiers temporaires avec des permissions trop ouvertes. En pentest, vérifier les scripts cron et les fichiers temporaires est une technique d'énumération courante

### 🛠️ Commandes clés
`cat /etc/cron.d/*`, `cat /usr/bin/cronjob_*.sh`

---
## Level 22 → Level 23

**Objectif** : Un autre cron job, cette fois pour `bandit23`. Le script utilise le nom d'utilisateur pour générer un nom de fichier temporaire via un hash MD5 (faible).

### 🔍 Découvertes

- Même principe que le niveau précédent : on examine le cron job, puis le script :

```bash
bandit22@bandit:~$ cat /etc/cron.d/cronjob_bandit23
@reboot bandit23 /usr/bin/cronjob_bandit23.sh &> /dev/null
* * * * * bandit23 /usr/bin/cronjob_bandit23.sh &> /dev/null

bandit22@bandit:~$ cat /usr/bin/cronjob_bandit23.sh
#!/bin/bash
myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)
chmod 644 /tmp/$mytarget
cat /etc/bandit_pass/$myname > /tmp/$mytarget
```

- Le script utilise `md5sum` et `cut` pour générer un nom de fichier basé sur le nom d'utilisateur. Le calcul est déterministe : si on remplace `whoami` par `bandit23`, on obtient le même nom de fichier :

```bash
bandit22@bandit:~$ echo "I am user bandit23" | md5sum | cut -d ' ' -f 1
8ca319486bfbbc3663ea0fbe81326349
```

- Il suffit ensuite de lire ce fichier temporaire :

```bash
bandit22@bandit:~$ cat /tmp/8ca319486bfbbc3663ea0fbe81326349
gKXDTAXnIz3OBxiPjRZ2uqutUlPZrBsw
```

- Ce niveau illustre un défaut de conception : utiliser un hash MD5 prévisible pour "cacher" le nom d'un fichier. La sécurité par l'obscurité (cacher plutôt que protéger) est inefficace quand l'algorithme est connu et reproductible

### 🛠️ Commandes clés
`md5sum`, `cut -d ' ' -f 1`, `echo texte | md5sum`

---
## Level 23 → Level 24

**Objectif** : Un cron job exécute **tous les scripts** présents dans `/var/spool/bandit24/`. En écrivant un script dans ce dossier, on peut le faire exécuter automatiquement pour récupérer le mot de passe de `bandit24`.

### 🔍 Découvertes

- On examine d'abord la configuration cron :

```bash
bandit23@bandit:~$ cat /etc/cron.d/cronjob_bandit24
@reboot bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
* * * * * bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
```

- Le script exécute tout script `.sh` présent dans `/var/spool/bandit24/` :

```bash
bandit23@bandit:~$ cat /usr/bin/cronjob_bandit24.sh
#!/bin/bash
cd /var/spool/bandit24
for i in * .*; do
    if [ -f "$i" ]; then
        owner=$(stat -c "%U" "$i")
        if [ "$owner" = "bandit23" ]; then
            timeout -s 9 60 "./$i"
        fi
    fi
done
```

- Le script vérifie que le fichier appartient à `bandit23` avant de l'exécuter. On va donc créer un script qui copie le mot de passe de `bandit24` dans `/tmp` :

```bash
bandit23@bandit:~$ cat > /var/spool/bandit24/script.sh << 'EOF'
#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/bandit24_pwd
chmod 644 /tmp/bandit24_pwd
EOF
bandit23@bandit:~$ chmod +x /var/spool/bandit24/script.sh
```

- Après une minute (le temps que cron exécute le script), on peut lire le fichier créé :

```bash
bandit23@bandit:~$ cat /tmp/bandit24_pwd
hVQMk3lJNsmQ7VF3ubyrNNBom7BOgVXv
```

- Ce niveau illustre un scénario d'escalade de privilèges très réaliste : un script cron qui exécute du contenu potentiellement contrôlé par un utilisateur moins privilégié. C'est un vecteur d'attaque classique qu'on retrouve dans les audits de configuration système

### 🛠️ Commandes clés
`cat > fichier << 'EOF'`, `chmod +x`, `stat -c "%U"`

---
## Level 24 → Level 25

**Objectif** : Un service écoute sur le port 30002. Quand on lui envoie le mot de passe actuel suivi d'un code PIN à 4 chiffres, il répond avec le mot de passe de `bandit25` si le code est correct.

### 🔍 Découvertes

- Une première connexion révèle le format attendu :

```bash
bandit24@bandit:~$ nc localhost 30002
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
```

- Tester manuellement tous les codes de 0000 à 9999 est impossible. On écrit un script bash pour automatiser le **bruteforce** :

```bash
bandit24@bandit:~$ for i in {0000..9999}; do
  echo "hVQMk3lJNsmQ7VF3ubyrNNBom7BOgVXv $i"
done | nc localhost 30002 | grep -v "Wrong"
```

- En une seule commande, le script génère 10 000 combinaisons, les envoie en continu via `nc` au service, et filtre les réponses pour n'afficher que le succès :

```bash
Correct!
The password of user bandit25 is SoHfqMOEqIX2IYKVciZxvgpR9a2Djx4P
```

- L'expansion d'accolades `{0000..9999}` de bash génère automatiquement toutes les combinaisons de 0000 à 9999, qui sont ensuite envoyées via `echo` et pipe à `nc`. Le `grep -v "Wrong"` filtre les réponses négatives pour ne garder que le résultat positif
- Ce niveau illustre l'attaque par **bruteforce** sur un code PIN court : avec seulement 10 000 combinaisons possibles, un script bash simple peut toutes les tester en quelques secondes contre un service local

### 🛠️ Commandes clés
`nc host port`, `for i in {0000..9999}`, `| grep -v "motif"`

---
## Level 25 → Level 26

**Objectif** : En se connectant en SSH avec la clé privée de `bandit26`, la session se ferme immédiatement ou affiche un contenu figé — le shell de `bandit26` est configuré pour utiliser `/usr/bin/showtext` au lieu d'un shell classique.

### 🔍 Découvertes

- D'abord, vérifier quel shell est configuré pour `bandit26` :

```bash
bandit25@bandit:~$ cat /etc/passwd | grep bandit26
bandit26:x:11026:11026:bandit26:/home/bandit26:/usr/bin/showtext
```

- Le fichier `/usr/bin/showtext` est un script tout simple :

```bash
bandit25@bandit:~$ cat /usr/bin/showtext
#!/bin/bash
export TERM=linux
more ~/text.txt
exit 0
```

- Il lance `more` sur un fichier texte, puis quitte immédiatement — on n'obtient donc pas de shell interactif
- La clé est que `more` permet de naviguer dans le contenu si celui-ci est plus grand que la taille du terminal. En **réduisant la fenêtre du terminal** (ou en utilisant `ssh` avec une option de redimensionnement), on force `more` à rester en mode interactif
- Une fois dans `more`, on peut utiliser `v` pour ouvrir l'éditeur `vi`, qui permet à son tour d'exécuter des commandes shell :

```bash
# Depuis more, taper :
v
# Depuis vi, taper :
:set shell=/bin/bash
:shell
```

- On obtient alors un shell en tant que `bandit26`, et on peut lire le mot de passe :

```bash
cat /etc/bandit_pass/bandit26
jHdv2ELQhT22BkprMNDjybZDAkw1zeBJ
```

- Ce niveau illustre comment un shell non-standard peut être contourné en exploitant les fonctionnalités des programmes qu'il utilise — ici, `more` et `vi`. Ce type de technique (shell escape via pager) est un classique de l'escalade de privilèges

### 🛠️ Commandes clés
`more`, `v` (pour ouvrir vi), `:set shell=/bin/bash`, `:shell`

---
## Level 26 → Level 27

**Objectif** : Une fois connecté en tant que `bandit26` (via l'exploit `more`/`vi` du niveau précédent), un binaire setuid `bandit27-do` permet d'exécuter des commandes en tant que `bandit27` — exactement comme au Level 19→20.

### 🔍 Découvertes

- Depuis le shell obtenu dans le niveau précédent :

```bash
bandit26@bandit:~$ ls -la
-rwsr-x---   1 bandit27 bandit26 14880 Jun 24 14:58 bandit27-do
```

- Même principe que `bandit20-do` :

```bash
bandit26@bandit:~$ ./bandit27-do cat /etc/bandit_pass/bandit27
STJLJBRRphMxKB392CT4iOr5CbzPU9ER
```

- Ce niveau conclut la séquence commencée au Level 19 : une fois qu'on a réussi à obtenir un shell via l'exploit `more`/`vi`, la suite est une simple exécution de commande via setuid, comme déjà vu

### 🛠️ Commandes clés
`./bandit27-do commande`

---
## Level 27 → Level 28

**Objectif** : Un dépôt Git est présent dans le dossier personnel (`/home/bandit27-repo/`). Il faut le cloner pour examiner son historique et trouver le mot de passe.

### 🔍 Découvertes

- On commence par cloner le dépôt qui écoute sur le port local :

```bash
bandit27@bandit:~$ git clone ssh://bandit27-git@localhost:2220/home/bandit27-git/repo
```

- Une fois cloné, on explore le dépôt :

```bash
bandit27@bandit:~$ cd repo
bandit27@bandit:~/repo$ ls
README
bandit27@bandit:~/repo$ cat README
The password to the next level is: y8Yd2ssKcpHpud7UvOSOxwamRMzIGIeQ
```

- Simple : le mot de passe est directement dans le fichier README du dépôt
- Ce niveau introduit `git` et le clonage de dépôts, une compétence essentielle en développement mais aussi en CTF — les dépôts Git contiennent souvent des informations sensibles dans leur historique, même après avoir été "nettoyés"

### 🛠️ Commandes clés
`git clone`, `ls`, `cat`

---
## Level 28 → Level 29

**Objectif** : Un dépôt Git contient un README qui semble cacher le mot de passe. En inspectant l'historique des commits, on découvre que le mot de passe était présent dans une version antérieure et a été supprimé ensuite — mais Git garde tout.

### 🔍 Découvertes

- Cloner le dépôt et lire le README :

```bash
bandit28@bandit:~$ git clone ssh://bandit28-git@localhost:2220/home/bandit28-git/repo
bandit28@bandit:~/repo$ cat README.md
# Bandit Notes
Some notes for level29

**credentials**

username: bandit29
password: xxxxxxxxxx
```

- Le mot de passe a été masqué (`xxxxxxxxxx`), mais Git conserve chaque version du fichier. On utilise `git log` pour voir l'historique :

```bash
bandit28@bandit:~/repo$ git log
commit edd935d60906b33f0619605abd1689808ccdd5ee
Author: Morla Porla <morla@overthewire.org>
Date:   ...
    fix info leak

commit c086d11a00c0648d095d04c089786efef5e01264
Author: Morla Porla <morla@overthewire.org>
Date:   ...
    add missing data

commit 5f110f1cf22460b4c5b00b72b7c2728c8e374162
Author: Morla Porla <morla@overthewire.org>
Date:   ...
    initial commit
```

- On voit le message "fix info leak" sur le commit le plus récent — un indice que le mot de passe a été retiré. On compare les versions du fichier avec `git diff` :

```bash
bandit28@bandit:~/repo$ git diff c086d11a00c0648d095d04c089786efef5e01264
```

- Ou on affiche directement le contenu du fichier dans sa version antérieure :

```bash
bandit28@bandit:~/repo$ git show c086d11a00c0648d095d04c089786efef5e01264:README.md
# Bandit Notes
Some notes for level29

**credentials**

username: bandit29
password: Em7eGtqaMySwNFjCpwzzHhLhospOcdt0
```

- `git show commit:chemin/fichier` permet de visualiser le contenu d'un fichier tel qu'il était dans un commit spécifique, sans avoir à faire de checkout ou de manipulation complexe — même si le mot de passe a été "nettoyé" dans la version actuelle, il reste accessible dans l'historique
- Ce niveau illustre un point crucial en sécurité : **Git ne supprime jamais rien**. Supprimer un mot de passe d'un fichier dans un nouveau commit ne l'efface pas — il reste à jamais dans l'historique du dépôt. C'est pour ça qu'il faut utiliser des outils spécialisés (comme `git filter-branch` ou `BFG Repo-Cleaner`) pour purger rétroactivement des informations sensibles

### 🛠️ Commandes clés
`git log`, `git diff commit`, `git show commit:chemin`

---
## Level 29 → Level 30

**Objectif** : Le dépôt Git contient plusieurs branches. Le mot de passe est caché dans une autre branche que `master`.

### 🔍 Découvertes

- Cloner le dépôt et examiner les branches :

```bash
bandit29@bandit:~$ git clone ssh://bandit29-git@localhost:2220/home/bandit29-git/repo
bandit29@bandit:~/repo$ git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/dev
  remotes/origin/master
  remotes/origin/sploits-dev
```

- La branche `dev` est suspecte — on bascule dessus :

```bash
bandit29@bandit:~/repo$ git checkout dev
bandit29@bandit:~/repo$ cat README.md
# Bandit Notes
Some notes for bandit30

**credentials**

username: bandit30
password: jq9Dfg2rXsfYsWMgFuKlXhphjdH7USgX
```

- Le mot de passe apparaît directement dans la branche `dev` — il a été laissé là alors que la branche `master` ne le contient pas
- `git branch -a` liste toutes les branches (locales et distantes), `git checkout nom` permet de basculer entre elles. Ce niveau montre qu'il faut toujours regarder au-delà de la branche par défaut — les branches de développement, de test ou de fonctionnalité contiennent souvent des informations que la branche principale a volontairement exclues

### 🛠️ Commandes clés
`git branch -a`, `git checkout branche`

---
## Level 30 → Level 31

**Objectif** : Le dépôt Git contient des **tags**. L'un d'eux révèle le mot de passe.

### 🔍 Découvertes

- Cloner le dépôt et lister les tags :

```bash
bandit30@bandit:~$ git clone ssh://bandit30-git@localhost:2220/home/bandit30-git/repo
bandit30@bandit:~/repo$ git tag
secret
```

- Il y a un tag nommé `secret`. On affiche son contenu :

```bash
bandit30@bandit:~/repo$ git show secret
82NkymblpGBYmIXG6ZQ8YldBYstHpfUf
```

- `git tag` liste les tags d'un dépôt, qui sont des étiquettes pointant vers un commit spécifique. `git show tag` affiche ce que contient ce tag — ici, directement le mot de passe
- Les tags Git sont souvent utilisés pour marquer des versions de release, mais peuvent aussi servir à stocker n'importe quelle information annexe (notes, signatures, clés...). En CTF, ne pas oublier de vérifier les tags d'un dépôt !

### 🛠️ Commandes clés
`git tag`, `git show tag`

---
## Level 31 → Level 32

**Objectif** : Le dépôt Git contient un fichier `.gitignore` qui exclut les fichiers `.txt`. En créant un fichier `.txt` avec le bon contenu et en forçant son ajout via `git add -f`, le commit déclenche un hook qui révèle le mot de passe.

### 🔍 Découvertes

- Cloner le dépôt et examiner le `.gitignore` :

```bash
bandit31@bandit:~$ git clone ssh://bandit31-git@localhost:2220/home/bandit31-git/repo
bandit31@bandit:~/repo$ cat .gitignore
*.txt
```

- Le fichier README.md explique ce qu'il faut faire :

```bash
bandit31@bandit:~/repo$ cat README.md
This time your task is to push a file to the remote repository.

Details:
    File name: key.txt
    Content: 'May I come in?'
    Branch: master
```

- On crée le fichier demandé, on l'ajoute en **forçant** son inclusion (pour contourner `.gitignore`), on commit et on push :

```bash
bandit31@bandit:~/repo$ echo "May I come in?" > key.txt
bandit31@bandit:~/repo$ git add -f key.txt
bandit31@bandit:~/repo$ git commit -m "push"
bandit31@bandit:~/repo$ git push
```

- Le push déclenche un **hook côté serveur** (un script exécuté automatiquement par Git) qui valide le contenu et renvoie le mot de passe :

```bash
remote: ### Attempting to validate files...
remote: 
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote: 
remote: Well done! Here is the password for the next level:
remote: pWuj5jBQ6IgV0NXwiH6g1pXRF8S1YvbT
remote: 
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
```

- Ce niveau introduit les **hooks Git**, des scripts qui s'exécutent automatiquement à certaines actions (commit, push, merge...). C'est un mécanisme utile pour l'intégration continue et la validation de code, mais aussi une surface d'attaque potentielle en sécurité

### 🛠️ Commandes clés
`git add -f`, `git commit -m`, `git push`, hooks Git

---
## Level 32 → Level 33

**Objectif** : Après s'être connecté en tant que `bandit32`, le shell est un interpréteur spécial qui transforme **tout en majuscules** (UPPERCASE SHELL). Impossible d'exécuter des commandes normalement, car le shell les convertit en MAJUSCULES avant de les interpréter.

### 🔍 Découvertes

- En se connectant, on est accueilli par un shell qui écrit tout ce qu'on tape en majuscules :

```bash
WELCOME TO THE UPPERCASE SHELL
>> ls
SH: LS: COMMAND NOT FOUND
```

- `ls` est devenu `LS`, qui n'existe pas. L'astuce : utiliser des alias de commandes ou des variables qui restent en minuscules. La variable `$0` (qui contient le nom du shell) fonctionne :

```bash
>> $0
$  id
uid=11033( bandit33 ) gid=11033( bandit33 ) groups=11033( bandit33 )
$  cat /etc/bandit_pass/bandit33
u4P2CyPOwPGLe94RdD9Uo2FxFwvnFswM
```

- `$0` est une variable spéciale qui contient le nom du programme en cours d'exécution — ici, `/bin/sh`. Le shell en majuscules lit `$0`, les variables étant interprétées avant la conversion en uppercase, donc `$0` reste `$0` et donne accès à un shell normal
- Ce niveau final est un "boss fight" : un shell qui transforme toute commande en majuscules, ce qui bloque la quasi-totalité des commandes système. L'exploitation passe par une **variable shell** (`$0`) qui contourne la contrainte
- C'est aussi la fin du jeu — le dernier mot de passe (`u4P2CyPOwPGLe94RdD9Uo2FxFwvnFswM`) ne donne accès à aucun niveau suivant ; c'est le trophée final !

### 🛠️ Commandes clés

---

## 📋 Tableau récapitulatif des mots de passe

| Niveau | Compétence | Mot de passe |
|--------|------------|-------------|
| Level 0→1 | Connexion SSH | `6y2kwnwK6grgvwvpvLaa2T1cpFEKOhNR` |
| Level 1→2 | Fichier nommé `-` | `PK8fYLZg2hnHSz83plBL1iEPKdD3QToB` |
| Level 2→3 | Espaces dans les noms | `7ZZ2LFrykP2zEyvBl4m3clcL7tGYJPME` |
| Level 3→4 | Fichiers cachés | `xzTXq1rDJQVVAzdv5cHq1TQytTWufAMq` |
| Level 4→5 | Identification de types (`file`) | `6C7h9GD8M6ai5nr7wo1RonrzFjj9yIrG` |
| Level 5→6 | Recherche par taille (`find -size`) | `pXa26xhMWaC2SvDotA4r9EgZkulOeSBW` |
| Level 6→7 | `find` multi-critères | `Bmnnvf82KzQlfxgAI2d1zYbr1u9pr3E3` |
| Level 7→8 | `grep` / Filtrage texte | `VR1ljMayciFxbnUokuQmJFw6QC9VKtub` |
| Level 8→9 | `sort` + `uniq -u` | `EjmOSvuAu7sGAHqHVcBDPirRe9T03kxl` |
| Level 9→10 | `grep -a` + Regex / Python | `B0s2khmbT9u0geKuOoVGW3JZKhndE3BG` |
| Level 10→11 | Base64 | `pYfOY6HwUsDj5rL9UvyhU7MCmv8vN5Ro` |
| Level 11→12 | ROT13 / `tr` | `GROozWPO8QyN0mGrjUkID0WCYkZiQxrN` |
| Level 12→13 | `xxd` + décompression (gzip/bzip2/tar) | `qQYQiHOBPR8zR61qxYqX45quvihF2uzk` |
| Level 13→14 | Clé SSH (`ssh -i`) | `aaWecNkG4FhxJQxz07uiwzVP6bJiYS65` |
| Level 14→15 | Netcat (`nc`) | `pbLYuZtTg4MgaqfJx8jbA9gKKGqM68A7` |
| Level 15→16 | `openssl s_client` | `kS0Hf0u5HiXFwKMKFqXvPdOTNGGa0X8V` |
| Level 16→17 | Nmap + `ncat --ssl` | `pWXMAZoxGC8JmDMfmT5MGEsobMM3vnj2` |
| Level 17→18 | `diff` | `OQxXZjELndr90zuhOTDYBEomI0SZITXI` |
| Level 18→19 | SSH avec commande | `KpsOfPkcP7i1FlIExk2QEjyt6dw8dxZI` |
| Level 19→20 | Binaire SUID | `4pIjcunZ0fK2vmp3IwfG8Vf7VhxD6pOA` |
| Level 20→21 | `suconnect` + `nc -l` | `bW9kBv5WC3P4yoDyf12LSdGuNz5ka6hY` |
| Level 21→22 | Cron job | `RYVux2rHEm9tiXHmLFzuR7Vhx6AZQMEz` |
| Level 22→23 | `md5sum` / hash | `gKXDTAXnIz3OBxiPjRZ2uqutUlPZrBsw` |
| Level 23→24 | Injection script cron | `hVQMk3lJNsmQ7VF3ubyrNNBom7BOgVXv` |
| Level 24→25 | Bruteforce PIN | `SoHfqMOEqIX2IYKVciZxvgpR9a2Djx4P` |
| Level 25→26 | `more` / `vi` escape | `jHdv2ELQhT22BkprMNDjybZDAkw1zeBJ` |
| Level 26→27 | SUID ×2 | `STJLJBRRphMxKB392CT4iOr5CbzPU9ER` |
| Level 27→28 | `git clone` | `y8Yd2ssKcpHpud7UvOSOxwamRMzIGIeQ` |
| Level 28→29 | `git log` / `git show` | `Em7eGtqaMySwNFjCpwzzHhLhospOcdt0` |
| Level 29→30 | `git checkout` (branche) | `jq9Dfg2rXsfYsWMgFuKlXhphjdH7USgX` |
| Level 30→31 | `git tag` | `82NkymblpGBYmIXG6ZQ8YldBYstHpfUf` |
| Level 31→32 | `git push` + hook | `pWuj5jBQ6IgV0NXwiH6g1pXRF8S1YvbT` |
| Level 32→33 🏆 | Uppercase shell / `$0` | `u4P2CyPOwPGLe94RdD9Uo2FxFwvnFswM` |
