---
title: "Solution du Wargame Leviathan - OverTheWire"
date: 2026-08-01 12:00:00 +0100
categories: [CTF, Wargame]
tags: [leviathan, reverse, ltrace, linux, overthewire]
---

## Level 0

**Objectif** : Se connecter en SSH sur le serveur avec les identifiants fournis par défaut (`leviathan0`/`leviathan0`), puis trouver le mot de passe du niveau suivant.

```bash
ssh -p 2223 leviathan0@leviathan.labs.overthewire.org
```

### 🔍 Découvertes

- Leviathan utilise le **port 2223** — pas le 2220 de Bandit ni le 22 standard
- Un `ls -la` dans le répertoire personnel ne montre qu'un seul élément digne d'intérêt : un dossier `.backup` (donc invisible avec un simple `ls` sans l'option `-a`) :

```bash
leviathan0@leviathan:~$ ls -la
drwxr-x---   2 leviathan1 leviathan0 4096 Jun 24 15:01 .backup
```

- Détail intéressant dans les permissions : le dossier appartient à `leviathan1` mais est lisible par le **groupe** `leviathan0` — donc par nous. Même logique pour le fichier qu'il contient
- Le dossier `.backup` ne renferme qu'un seul fichier : `bookmarks.html` (133 Ko), un export de signets de navigateur :

```bash
leviathan0@leviathan:~/.backup$ ls -la
-rw-r----- 1 leviathan1 leviathan0 133259 Jun 24 15:01 bookmarks.html
```

- L'idée du niveau : un export de favoris peut contenir des informations sensibles (URLs avec identifiants, notes, mots de passe stockés en dur...). Pour éviter de lire les 133 Ko à la main, on filtre les lignes contenant « leviathan » avec `grep` :

```bash
leviathan0@leviathan:~/.backup$ cat bookmarks.html | grep leviathan
<DT><A HREF="http://leviathan.labs.overthewire.org/passwordus.html | This will be fixed later, the password for leviathan1 is PiXaSWQqHq" ...>
```

- Le signet contient le mot de passe **en clair** dans le texte du lien : `PiXaSWQqHq` — un rappel que les sauvegardes (`backup`) et les exports de navigateur sont des cibles de choix en investigation, car les gens y laissent souvent traîner des secrets « en attendant de corriger plus tard »

### 🛠️ Commandes clés
`ssh -p 2223`, `ls -la`, `cd`, `cat fichier | grep`

---
## Level 1 → Level 2

**Objectif** : Le répertoire personnel contient un programme `check` avec le bit **setuid** activé. Il demande un mot de passe — il faut le découvrir pour obtenir un shell en tant que `leviathan2`.

```bash
leviathan1@leviathan:~$ ls -la
-r-sr-x---   1 leviathan2 leviathan1 15080 Jun 24 15:01 check
```

### 🔍 Découvertes

- La permission `r-s` à la place de `r-x` pour le propriétaire révèle le **bit setuid** : le programme s'exécute avec les privilèges de son **propriétaire** (`leviathan2`), quel que soit l'utilisateur qui le lance — le même mécanisme que `bandit20-do` dans Bandit, mais cette fois sans béquille : il faut trouver le mot de passe soi-même
- Lancer le programme affiche un prompt et refuse les mauvais mots de passe :

```bash
leviathan1@leviathan:~$ ./check
password: 123
Wrong password, Good Bye ...
```

- Plutôt que de deviner, on va **observer** ce que fait le programme : `ltrace` intercepte et affiche tous les appels aux **bibliothèques dynamiques** — c'est-à-dire les morceaux de code partagés que le programme emprunte au système (comme `printf`, qui affiche du texte, ou `strcmp`, qui compare deux chaînes) au lieu de les contenir lui-même. C'est analyser un programme de l'extérieur sans avoir son code source — le cœur du **reverse engineering** :

```bash
leviathan1@leviathan:~$ ltrace ./check
__libc_start_main(["./check"] <unfinished ...>
printf("password: ")                                      = 10
getchar(0xf7fc5310, 0xf7fc3000, 0x786573, 0x646f67)       = 49   # '1'
getchar(0xf7fc5310, 0xf7fc3031, 0x786573, 0x646f67)       = 50   # '2'
getchar(0xf7fc5310, 0xf7fc3231, 0x786573, 0x646f67)       = 51   # '3'
strcmp("123", "sex")                                      = -1
puts("Wrong password, Good Bye ...")                      = 29
```

*Note : dans ta session réelle, la trace et l'affichage du programme s'entremêlaient (`ltrace` écrit sur `stderr`, le programme sur `stdout`) ; j'ai nettoyé ça pour la lisibilité. Les valeurs `0x786573` et `0x646f67` sont bien celles qu'affichait `ltrace`.*

- Le résultat parle de lui-même : le programme compare notre saisie avec la chaîne **`"sex"`** via `strcmp`. Le mot de passe est stocké **en clair** dans le binaire — une très mauvaise pratique de sécurité, mais une aubaine pour nous

- 💡 **Petit rappel : pourquoi `getchar` renvoie des nombres ?** Un ordinateur ne connaît pas les lettres : il ne manipule que des **nombres**. Chaque caractère du clavier a donc un numéro officiel, défini par une table standard appelée **ASCII** (`'0'` = 48, `'1'` = 49, `'2'` = 50, `'3'` = 51, `'A'` = 65, `'a'` = 97...). La fonction `getchar` fait exactement une seule chose : elle lit **un caractère** de l'entrée standard et renvoie son **code ASCII** (le numéro). En pratique, dans un terminal, les caractères que tu tapes sont envoyés au programme au moment où tu appuies sur **Entrée**. C'est pour ça qu'on voit **trois appels** `getchar` dans la trace : le programme lit les trois caractères de `123` un par un, et `ltrace` nous montre le numéro renvoyé à chaque fois :
  - `getchar(...) = 49` → le programme a lu le caractère `'1'`
  - `getchar(...) = 50` → il a lu le caractère `'2'`
  - `getchar(...) = 51` → il a lu le caractère `'3'`
  Ces trois caractères sont ensuite assemblés en la chaîne `"123"`, celle qu'on retrouve dans `strcmp("123", "sex")`. La ligne `strcmp` est d'ailleurs la **seule** qui compte pour nous : `getchar` décrit *comment* le programme lit ta saisie, `strcmp` révèle *avec quoi* il la compare — c'est son argument `"sex"` qui est la vraie information, pas le retour `-1`.

- 🕵️ **Et les valeurs hexadécimales à côté de `getchar` (`0x786573`, `0x646f67`...) ?** Elles ne sont pas des arguments : `getchar` n'en prend aucun. Ce sont des **valeurs de registres** — les registres sont les cases de stockage ultra-rapides situées à l'intérieur du processeur, et `ltrace` affiche leur contenu « par-dessus » faute de connaître la signature exacte de la fonction. Mais l'une d'elles est un joli easter egg : sur un processeur x86 (petit-boutiste / little-endian), charger les octets `'s' 'e' 'x'` (73 65 78 en hexa) comme un entier 32 bits donne exactement `0x786573` — le mot de passe est donc littéralement visible en hexadécimal aussi !
- `strcmp` renvoie `-1` ici (les chaînes diffèrent) ; il renverrait `0` si elles étaient identiques — c'est cette valeur que le programme teste pour accepter ou refuser le mot de passe
- En entrant le bon mot de passe, le programme (setuid) nous donne un shell **en tant que `leviathan2`**, ce qui permet de lire le fichier de mot de passe dédié :

```bash
leviathan1@leviathan:~$ ./check
password: sex
$ cat /etc/leviathan_pass/leviathan2
ERJ9jTYWXE
```

- Comme pour Bandit, les mots de passe sont stockés dans `/etc/leviathan_pass/` (l'équivalent de `/etc/bandit_pass/`) et ne sont lisibles que par l'utilisateur concerné — ici c'est possible parce que le shell obtenu a les droits de `leviathan2`
- Ce niveau est une première vraie initiation au **reverse engineering** : analyser un programme sans son code source. `ltrace` (et son cousin `strace`, qui trace les **appels système** au lieu des appels de bibliothèque) sont les premiers outils à essayer face à un binaire inconnu, avant même d'ouvrir un désassembleur comme `objdump` ou `gdb`

### 🛠️ Commandes clés
`ls -la`, `./check`, `ltrace`, `cat /etc/leviathan_pass/...`

---

## 🔬 Pour aller plus loin : registres, little-endian, ltrace & strace

Trois notions techniques croisées dans ce niveau méritent qu'on s'y attarde : pourquoi `ltrace` affichait ces valeurs hexadécimales bizarres, pourquoi `0x786573` vaut `"sex"`, et ce que `strace` — mentionné plus haut — aurait montré à la place.

### 🗂️ Les registres : le bureau du processeur

Le **CPU** (processeur) est le cerveau de l'ordinateur. Pour calculer, il doit poser ses nombres quelque part. Il a deux options :

- La **RAM** : immense (des Go), mais relativement lente à atteindre → c'est l'entrepôt
- Les **registres** : une poignée de cases situées **à l'intérieur même du CPU**, minuscules (32 ou 64 bits chacune) mais **instantanées** → c'est le bureau, tout ce qui est en cours de calcul

```
        ┌──────────────────────────┐
        │        LE CPU            │
        │  ┌─────┐ ┌─────┐         │
        │  │EAX  │ │EBX  │   ...   │
        │  │0x78…│ │0xf7…│         │
        │  └─────┘ └─────┘         │
        │  Registres = le BUREAU   │
        │  (ultra-rapide)          │
        └───────────┬──────────────┘
                    │
        ┌───────────▼──────────────┐
        │   RAM = l'ENTREPÔT       │
        │   (des Go, plus lent)    │
        └──────────────────────────┘
```

Quand un programme appelle une fonction, les valeurs en cours circulent dans les registres. `ltrace` connaît la signature de certaines fonctions et peut afficher leurs arguments proprement ; pour `getchar`, qui n'en prend aucun, il se contente d'afficher **le contenu brut des registres** à cet instant — c'est l'origine des `0x786573` et `0x646f67` de la trace.

### 🔀 Le little-endian : dans quel ordre range-t-on les octets ?

Un octet (byte) ne peut contenir qu'un nombre entre `0x00` et `0xFF` (0 à 255). Une valeur comme `0x786573` est plus grande qu'un octet → elle est découpée en plusieurs octets :

```
0x786573  =  0x78  |  0x65  |  0x73
              │       │        │
          le + fort  milieu  le - faible
```

Question : dans quel ordre stocker ces octets en mémoire ? Deux écoles :

| Convention | Ordre des octets | Exemple pour `0x786573` |
|---|---|---|
| **Big-endian** | Le plus fort d'abord (comme on écrit `123` : 1 puis 2 puis 3) | `78 65 73` |
| **Little-endian** | Le plus faible d'abord (à l'envers : `123` → 3, 2, 1) | `73 65 78` |

Les processeurs **x86 (Intel/AMD)** — ton PC comme le serveur Leviathan — utilisent le **little-endian**. C'est une simple convention, mais elle a une conséquence savoureuse :

### 🍬 Le schéma qui relie tout : pourquoi `0x786573` = `"sex"`

La chaîne `"sex"` en mémoire, ce sont les octets ASCII dans l'ordre :

```
Adresse :   …  0x100   0x101   0x102   0x103 …
            …   0x73    0x65    0x78    0x00 …
                's'     'e'     'x'     (fin de chaîne)
```

Si le CPU charge ces octets comme un entier 32 bits, en little-endian le premier octet lu est le **poids faible** :

```
Lecture little-endian (x86) :
  0x73  (poids faible)   → 0x73
  0x65  (× 256)          → 0x6500
  0x78  (× 65536)        → 0x780000
                              ────────
  Total                   = 0x786573   ← EXACTEMENT la valeur de ltrace !
```

En big-endian, on aurait obtenu `0x73×65536 + 0x65×256 + 0x78 = 0x736578` — un autre nombre. Le `0x786573` que `ltrace` affichait « par hasard » est donc littéralement le mot `"sex"` relu comme un nombre : le mot de passe était visible *deux fois* dans la trace — en clair dans `strcmp("123", "sex")` et en easter egg dans le registre. 🥚

Bonus : l'autre valeur de la trace, `0x646f67`, relue en little-endian donne les octets `67 6f 64` = `"god"` — sans doute un simple hasard de valeur de registre, mais amusant !

### 🎯 `ltrace` vs `strace` : deux étages d'observation

Ces deux outils tracent un programme, mais pas au même étage :

- **`ltrace`** trace les appels aux **fonctions de bibliothèque** (libc : `printf`, `strcmp`, `getchar`, `fopen`…) — la *façade* que le programme utilise
- **`strace`** trace les **appels système** — les demandes directes au **noyau Linux** (`open`, `read`, `write`, `execve`, `socket`…) — le *moteur* qui fait vraiment le travail

**L'analogie du restaurant** : `ltrace` voit ce que le client commande au comptoir (« un café »), `strace` voit ce qui se passe en cuisine (moudre le café, verser l'eau...). Un appel de bibliothèque englobe souvent plusieurs appels système : `printf` finit par faire un `write`, `getchar` un `read`, `fopen` un `open`.

Le même programme `check` vu par les deux outils — `ltrace`, la couche *programme* :

```bash
printf("password: ")                        = 10
getchar()                                   = 49
strcmp("123", "sex")                        = -1
puts("Wrong password, Good Bye ...")        = 29
```

Et `strace`, la couche *noyau* (schématique) :

```bash
write(1, "password: ", 10)                   = 10   # écrire sur l'écran (fd 1 = stdout)
read(0, "123\n", 1024)                      = 4    # lire au clavier (fd 0 = stdin)
write(1, "Wrong password, Good Bye ...\n", 29) = 29 # 28 caractères + le saut de ligne
exit_group(0)                                         # quitter le programme
```

Le `strcmp` n'apparaît pas chez `strace` : c'est du calcul interne au programme, pas une demande au noyau. À l'inverse, `ltrace` ne montre pas les numéros de **descripteurs de fichiers** (`fd 0`, `fd 1`...) — la spécialité de `strace`, qui permet de savoir *quel fichier est ouvert par quoi*.

Autre exemple parlant, `cat fichier.txt` :

| `ltrace` | `strace` |
|---|---|
| `fopen("fichier.txt", "r")` | `openat(AT_FDCWD, "fichier.txt", O_RDONLY) = 3` |
| `fread(…, 4096, 1, …)` | `read(3, "Bonjour le monde\n", 4096) = 17` |
| `fwrite(…, 1, 17, …)` | `write(1, "Bonjour le monde\n", 17) = 17` |
| `fclose(...)` | `close(3)` |

**Quand utiliser lequel ?**

- **`ltrace` d'abord** sur un binaire inconnu : on cherche les comparaisons (`strcmp` → mot de passe en clair), les décodages (`strtol`, base64), les ouvertures de fichiers (`fopen`). Rapide à lire, orienté logique du programme
- **`strace` ensuite** pour creuser le système : « quels fichiers ce programme ouvre-t-il ? » (`strace -e trace=openat,open ./prog`), « pourquoi il échoue ? » (`Permission denied` sur un `open` = problème de droits), « il contacte un serveur ? » (`connect`, `socket`, `sendto`). `strace -f` suit les processus enfants (fork), `-e trace=` filtre les appels
- **Astuce** : si `ltrace` ne montre rien d'intéressant (binaire statique ou sans libc), passe à `strace`. L'inverse : un programme très lié à libc produit des tonnes de syscalls avec `strace` (bruit) alors que `ltrace` reste lisible

### 📌 À retenir

- **Registre** = case de travail ultra-rapide dans le CPU (le « bureau »), par opposition à la RAM (l'« entrepôt »)
- **Little-endian** = convention x86 où le poids faible est stocké en premier (à l'envers de notre écriture)
- Conséquence : une chaîne de caractères et un nombre peuvent être **la même chose**, juste lus dans des sens différents
- **`ltrace`** = l'étage bibliothèque (logique du programme : `printf`, `strcmp`, `fopen`) ; **`strace`** = l'étage noyau (fichiers, descripteurs, réseau, erreurs) — un appel de bibliothèque englobe souvent plusieurs appels système

---

## Level 2 → Level 3

**Objectif** : Le répertoire personnel contient un programme `printfile` avec le bit **setuid** activé, appartenant à `leviathan3`. Il permet de lire des fichiers — mais refuse de nous laisser lire les mots de passe. Il faut contourner sa vérification de permissions.

```bash
leviathan2@leviathan:~$ ls -la
-r-sr-x---   1 leviathan3 leviathan2 7792 Jun 24 15:01 printfile
```

### 🔍 Découvertes

- En testant le programme, il se comporte comme `cat` : il affiche le contenu du fichier passé en argument… sauf si c'est un mot de passe :

```bash
leviathan2@leviathan:~$ ./printfile /etc/leviathan_pass/leviathan3
You cant have that file...
```

- L'erreur vient d'un **contrôle de permissions** intégré au programme : il appelle la fonction `access()` *avant* de lire le fichier avec `cat`. `ltrace` nous le montre :

```bash
leviathan2@leviathan:~$ ltrace ./printfile /etc/leviathan_pass/leviathan3
access("/etc/leviathan_pass/leviathan3", R_OK)   = -1
puts("You cant have that file...")               = 24
```

- 💡 **Le piège (et l'opportunité)** : `access()` vérifie les permissions de l'utilisateur **réel** (celui qui a lancé le programme, nous), alors que `cat` — appelé *ensuite* par le programme — s'exécute avec l'utilisateur **effectif** (celui du setuid, `leviathan3`). L'utilisateur réel n'a pas accès au fichier → `access()` renvoie `-1` → le programme refuse. Mais si on fait passer la vérification, `cat` lira le fichier avec les droits de `leviathan3` !
- **L'astuce** : `access()` prend **un seul** chemin (la chaîne entière), alors que `cat` accepte **plusieurs arguments séparés par des espaces**. On crée donc un fichier dont le *nom* contient un espace : `access()` valide le nom complet `a b` (qu'on possède → OK), mais `cat` reçoit deux arguments `a` et `b` — dont `a` est un **lien symbolique** vers le fichier convoité !

```bash
leviathan2@leviathan:~$ mkdir /tmp/hs && cd /tmp/hs
leviathan2@leviathan:/tmp/hs$ ln -s /etc/leviathan_pass/leviathan3 a
leviathan2@leviathan:/tmp/hs$ touch 'a b'
leviathan2@leviathan:/tmp/hs$ ~/printfile 'a b'
<mot de passe de leviathan3>
cat: b: No such file or directory
```

- Le `cat: b: No such file or directory` est une erreur **bénigne** : `b` n'existe pas, mais `a` (le lien) a déjà été lu et son contenu affiché. 💪

### 🛠️ Commandes clés
`ln -s`, `touch 'a b'`, `~/printfile 'a b'`, `ltrace`

---

## 🔬 Pour aller plus loin : access(), UID réel vs effectif, et le bug d'argument

C'est LE niveau le plus intéressant du wargame (l'auteur de l'article source le confirme). Il mêle trois notions :

### 👤 UID réel vs UID effectif

| | Définition | Exemple |
|---|---|---|
| **UID réel (RUID)** | L'utilisateur qui a *lancé* le processus | `leviathan2` (nous) |
| **UID effectif (EUID)** | L'utilisateur dont le processus a *les droits* | `leviathan3` (grâce au setuid) |

Normalement RUID = EUID. Le bit **setuid** décale l'EUID : le programme tourne avec les droits de son **propriétaire**, pas de celui qui l'exécute. C'est exactement le mécanisme de `sudo`, de `passwd` (qui doit pouvoir modifier `/etc/shadow`)… et de nos binaires `check`, `printfile` et autres.

### ⚠️ Pourquoi `access()` est-il dangereux ?

`access()` répond à la question : « *l'utilisateur réel peut-il lire ce fichier ?* ». Mais elle **ne vérifie pas** si l'utilisateur *effectif* le peut. Utiliser `access()` pour *autoriser* puis `cat` pour *lire* crée un écart entre **la vérification** (RUID) et **l'action** (EUID) — c'est une faille classique. Le manuel Linux (`man 2 access`) le dit noir sur blanc : utiliser `access()` pour décider d'un accès ultérieur est **une faille de sécurité** (catégorie CWE-367 TOCTOU — *Time Of Check To Time Of Use*, l'écart entre le moment où l'on vérifie et le moment où l'on utilise).

### 🪞 Le bug d'argument : deux lecteurs, deux grammaires

Le même argument `a b` est interprété différemment par les deux fonctions :

```
            "a b"
               │
   ┌───────────┴───────────┐
access("a b")          cat a b
   UN SEUL chemin       DEUX fichiers
   → vérifie "a b"      → lit "a" PUIS "b"
   (existe, OK)         → "a" = lien → mot de passe !
```

`access()` traite l'argument comme une **chaîne unique** ; `cat` le découpe aux **espaces**. L'écart de grammaire = la faille. On retrouve ce genre de « deux interprétations d'un même input » (parsing confusion) aussi bien en web qu'en binaire.

### 📌 À retenir

- **UID réel** = qui je suis ; **UID effectif** = pour qui j'agis (setuid)
- `access()` vérifie le **RUID** → à ne jamais utiliser comme garde-fou avant une action
- Un **espace dans un nom de fichier** permet de tromper `access()` tout en laissant `cat` lire deux fichiers
- Un **lien symbolique** redirige une lecture vers n'importe quel fichier

---

## Level 3 → Level 4

**Objectif** : Encore un binaire setuid, cette fois `level3`, qui demande un mot de passe. Même réflexe que le niveau 1 : on ne devine pas, on **observe**.

### 🔍 Découvertes

- Un `ls -la` montre le binaire setuid appartenant à `leviathan4` ; le lancer affiche un message bizarre avant de demander le mot de passe :

```bash
leviathan3@leviathan:~$ ls -la
-r-sr-x---   1 leviathan4 leviathan3 10123 Jun 24 15:01 level3
leviathan3@leviathan:~$ ./level3
[You've got shell]!
password:
```

- On trace avec `ltrace` — la réponse est immédiate :

```bash
leviathan3@leviathan:~$ ltrace ./level3
printf("[You've got shell]!\n")                = 21
strcmp("123", "snlprintf")                     = -1
```

- Le mot de passe est encore **en clair** dans le binaire : **`snlprintf`**. (Le message `[You've got shell]!` affiché dès le lancement est un **leurre** : il s'affiche avant même de vérifier le mot de passe !)

```bash
leviathan3@leviathan:~$ ./level3
[You've got shell]!
password: snlprintf
$ cat /etc/leviathan_pass/leviathan4
<mot de passe de leviathan4>
```

### 🛠️ Commandes clés
`ls -la`, `./level3`, `ltrace`, `cat /etc/leviathan_pass/...`

---

## 🔬 Pour aller plus loin : les leurres en reverse

- Ce niveau rappelle que l'**affichage** d'un programme ne reflète pas sa **logique** : ici, « You've got shell » s'affiche *avant* toute vérification — une simple fonction `puts` au début du code, pas une vraie réussite
- Le **leurre** (décoy) est une technique de protection naïve : mettre de fausses chaînes ou de faux messages pour égarer celui qui lit le binaire avec `strings`. Elle ne résiste pas à `ltrace`/`strace`, qui montrent les *vrais* appels
- Réflexe à garder : face à un binaire qui « semble » faire quelque chose, toujours vérifier avec `ltrace` ce qu'il fait **réellement**

---

## Level 4 → Level 5

**Objectif** : Un répertoire `.trash` (corbeille) contient un binaire `bin`. Il affiche… des nombres binaires. Il faut les décoder.

### 🔍 Découvertes

```bash
leviathan4@leviathan:~$ ls -la
drwxr-x---   2 leviathan5 leviathan4 4096 Jun 24 15:01 .trash
leviathan4@leviathan:~$ cd .trash && ls -la
-r-sr-x---   1 leviathan5 leviathan4 1900 Jun 24 15:01 bin
```

- En lançant `./bin`, on obtient une série de nombres en **binaire** (0 et 1) :

```bash
leviathan4@leviathan:~/.trash$ ./bin
01000101 01010010 01001010 ... (etc.)
```

- 💡 Chaque groupe de 8 bits est un **octet** = un **code ASCII** : `01000101` = 69 = `'E'`, `01010010` = 82 = `'R'`… Le programme nous affiche le mot de passe… encodé en binaire ! C'est du **chiffrement de pacotille** : une simple transformation, pas un vrai secret.
- Plutôt que de décoder à la main, on écrit un petit **script Python** (le même que l'auteur de l'article source) :

```python
nums = open('nums.txt', 'r').read().split()
for i in range(len(nums)):
    nums[i] = chr(int(nums[i], 2))
password = ""
print(password.join(nums))
```

*(Raccourci : rediriger la sortie — `./bin > nums.txt` — puis lancer le script.)*

- Le résultat est le mot de passe du niveau suivant.

### 🛠️ Commandes clés
`cd .trash`, `./bin`, `./bin > nums.txt`, script Python (`int(x, 2)` + `chr()`)

---

## 🔬 Pour aller plus loin : binaire, octets et ASCII

### 🧮 Comprendre `int(x, 2)` et `chr()`

- Le binaire est une **base 2** : chaque chiffre est un bit, et sa valeur dépend de sa position (puissance de 2) :

```
01000101
│││││││└─ 2⁰ = 1        → 0
││││││└── 2¹ = 2        → 0
│││││└─── 2² = 4        → 1  → 4
││││└──── 2³ = 8        → 0
│││└───── 2⁴ = 16       → 1  → 16
││└────── 2⁵ = 32       → 0
│└─────── 2⁶ = 64       → 0
└──────── 2⁷ = 128      → 0
Total : 4 + 16 + 64 = 69 = 'E'  (en ASCII)
```

- `int("01000101", 2)` → 69 : conversion **binaire → entier**
- `chr(69)` → `'E'` : conversion **entier → caractère ASCII**
- C'est exactement ce que fait le script ligne par ligne, en une boucle

### 🔤 Pourquoi 8 bits ?

8 bits = 2⁸ = 256 valeurs possibles (0 à 255) — de quoi coder les 128 caractères ASCII de base. Un **octet** est l'unité de base de la mémoire moderne. Décoder des octets, c'est le B.A.-BA du forensics et du reverse : `xxd`, `hexdump`, `strings` ne font que relire ces octets autrement.

### 📌 À retenir

- Binaire (base 2) → entier → caractère : la chaîne de conversion universelle
- Un « chiffrement » qui se contente de changer de base n'en est **pas un** : c'est de l'**encodage**
- Python : `int(x, 2)`, `chr()`, `ord()` (l'inverse de `chr`) — à connaître par cœur

---

## Level 5 → Level 6

**Objectif** : Le binaire `leviathan5` (setuid) lit un fichier bien précis… et le **supprime** ensuite. Un lien symbolique suffit.

### 🔍 Découvertes

- En lançant `./leviathan5`, on obtient une erreur : le programme cherche `/tmp/file.log`, qui n'existe pas :

```bash
leviathan5@leviathan:~$ ./leviathan5
Cannot find /tmp/file.log
```

- `strace` (ou `ltrace`) montre ce que fait le programme : il **ouvre** `/tmp/file.log`, affiche son contenu, puis le **supprime** (`unlink`) :

```bash
leviathan5@leviathan:~$ strace ./leviathan5
open("/tmp/file.log", O_RDONLY)      = 3
read(3, "...", 4096)                 = 11
unlink("/tmp/file.log")              = 0
```

- 💡 **L'astuce** : `/tmp` est un dossier **partagé et inscriptible par tous**. On y crée un **lien symbolique** `file.log` pointant vers le fichier de mot de passe : quand le programme (setuid, donc avec les droits de `leviathan6`) ouvrira `/tmp/file.log`, le noyau suivra le lien et lui donnera le contenu du fichier protégé !

```bash
leviathan5@leviathan:~$ ln -s /etc/leviathan_pass/leviathan6 /tmp/file.log
leviathan5@leviathan:~$ ./leviathan5
<mot de passe de leviathan6>
```

- C'est le même principe que le niveau 2 (utiliser un setuid pour lire un fichier qu'on ne peut pas lire directement), mais en beaucoup plus simple : ici, **aucune vérification** n'est faite, le programme lit directement le chemin — et un lien symbolique détourne cette lecture.

### 🛠️ Commandes clés
`strace`, `ln -s cible lien`, `./leviathan5`

---

## 🔬 Pour aller plus loin : les liens symboliques

- Un **lien symbolique** (symlink) est un *raccourci* : un fichier spécial qui ne contient qu'un **chemin** vers un autre fichier. Ouvrir le lien = ouvrir la cible.
- `ln -s CIBLE LIEN` crée le lien. `readlink` affiche la cible, `ls -l` la montre avec une flèche : `file.log -> /etc/leviathan_pass/leviathan6`
- ⚠️ Pourquoi le programme **supprime** le fichier après lecture ? Probablement pour « nettoyer » son fichier de log après usage — mais c'est un comportement dangereux combiné au setuid : un attaquant peut faire lire *n'importe quel* fichier lisible par `leviathan6` en plaçant un lien.
- En sécurité, les symlinks sont à la fois une **arme** (détournement de lecture/écriture) et une **cible** (protéger ses scripts contre `O_NOFOLLOW`). C'est une des causes classiques de **CWE-59** (lien vers un fichier hors périmètre).

### 📌 À retenir

- `ln -s` crée un raccourci ; le noyau suit le lien à l'ouverture
- Un programme setuid qui lit un chemin **non protégé** dans `/tmp` = lecture arbitraire possible
- Toujours se demander : « ce chemin, peut-il être remplacé par un lien ? »

---

## Level 6 → Level 7

**Objectif** : `leviathan6` prend un argument : un **code à 4 chiffres**. Si on ne l'a pas, on peut le **bruteforcer** — il n'y a que 10 000 possibilités.

### 🔍 Découvertes

```bash
leviathan6@leviathan:~$ ls -la
-r-sr-x---   1 leviathan7 leviathan6 19598 Jun 24 15:01 leviathan6
leviathan6@leviathan:~$ ./leviathan6 1234
Wrong
```

- 4 chiffres → 10 000 combinaisons possibles (0000 à 9999). L'auteur de l'article source propose une boucle `for` : tester chaque code, filtrer la sortie pour ne garder que ce qui n'est pas « Wrong », et **espacer les essais** pour ne pas épuiser les ressources du serveur :

```bash
leviathan6@leviathan:~$ for i in {0..10000}; do echo "trying $i"; ./leviathan6 $i | grep -v "Wrong"; sleep 0.005; done
```

- 🐌 Le `sleep 0.005` n'est pas une option : sans lui, la boucle lance des milliers de processus à la seconde et le serveur finit par refuser (`fork: retry: No child processes`) — l'expérience de l'auteur. À ~5 ms par essai, la boucle entière prend environ une minute.
- Le bon code est **`7123`** : la boucle s'arrête sur un **shell en tant que `leviathan7`** !

```bash
leviathan6@leviathan:~$ ./leviathan6 7123
$ cat /etc/leviathan_pass/leviathan7
<mot de passe de leviathan7>
```

### 🛠️ Commandes clés
Boucle `for`, `grep -v`, `sleep 0.005`, `cat /etc/leviathan_pass/...`

---

## 🔬 Pour aller plus loin : bruteforce & gestion des ressources

### 🧮 L'espace de recherche

10 000 combinaisons, c'est **trivial** pour une machine — mais c'est le principe d'un **bruteforce** : essayer toutes les valeurs possibles. La leçon inverse en sécurité : un code à 4 chiffres n'est **jamais** un bon secret (10 000 essais ≈ 1 minute). C'est pourquoi on voit des verrouillages après N essais, ou des codes à 6+ chiffres + TOTP.

### 🐌 Pourquoi `sleep 0.005` ?

Chaque itération lance un **processus** `./leviathan6` (un `fork` + `exec`). Linux limite le nombre de processus et la vitesse de fork ; sans pause, on sature → `fork: retry: No child processes`, la boucle meurt. Le `sleep` **rate-limite** nos propres requêtes : l'attaque ne doit pas détruire la victime (ici, le serveur) avant d'avoir fini.

### 🎯 `grep -v "Wrong"`

Le programme affiche `Wrong` pour les mauvais codes et lance un shell pour le bon. `grep -v "Wrong"` **inverse** le filtre : il ne garde que les lignes qui ne contiennent pas `Wrong` — donc uniquement la sortie du bon code (le prompt `$`). La boucle continue ensuite mais on a ce qu'on veut.

### 📌 À retenir

- Bruteforce = essayer tout l'espace de recherche ; ici 10⁴ = 10 000 essais, ~1 min avec `sleep`
- Toujours **rate-limiter** ses propres boucles (`sleep`) pour ne pas saturer la cible
- `grep -v` inverse un filtre : pratique pour isoler un résultat rare dans un flux bruyant

---

## 🏁 Conclusion

Leviathan est un excellent wargame d'introduction au **reverse engineering** et aux **binaires setuid** :

| Niveau | Compétence clé | Outil principal |
|--------|---------------|-----------------|
| 0 → 1 | Fouille de fichiers & `grep` | `cat` \| `grep` |
| 1 → 2 | Reverse : mot de passe en clair | `ltrace` / `strings` |
| 2 → 3 | TOCTOU : `access()` vs `cat`, symlink + espace | `ltrace` |
| 3 → 4 | Leurre & comparaison | `ltrace` |
| 4 → 5 | Encodage binaire → ASCII | Python |
| 5 → 6 | Symlink & lecture arbitraire | `ln -s` |
| 6 → 7 | Bruteforce + rate-limiting | Boucle `for` |

Le fil rouge : **un binaire setuid fait des choses avec les droits de son propriétaire — et c'est précisément là qu'on attaque.** Entre Bandit (découverte de Linux) et les vrais challenges de pwn, c'est le pont idéal.

> 📌 **Voir aussi** : le [récapitulatif de ma progression sur les wargames OverTheWire]({% post_url 2026-08-03-overthewire-wargames-recapitulatif %}), avec le [writeup Bandit complet]({% post_url 2026-07-25-bandit-overthewire %}) et la roadmap des prochains wargames.
{: .prompt-tip }

---

## 📚 Sources & références

- **hrbrtschmu1l — Leviathan OverTheWire Wargame Writeup** : [https://hrbrtschmu1l.medium.com/leviathan-overthewire-wargame-writeup-dd3378a6136a](https://hrbrtschmu1l.medium.com/leviathan-overthewire-wargame-writeup-dd3378a6136a) — la base de ce writeup (solutions des niveaux 2→7, astuces `access()`/`cat`, bruteforce avec `sleep`)
- **OverTheWire — Leviathan** : [https://overthewire.org/wargames/leviathan/](https://overthewire.org/wargames/leviathan/) — le wargame officiel
- `man 2 access`, `man 2 symlink`, `man ltrace`, `man strace` — pour approfondir
