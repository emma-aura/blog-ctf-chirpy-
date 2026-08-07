---
title: "Solution du Wargame Leviathan - OverTheWire"
date: 2026-08-01 12:00:00 +0100
categories: [CTF, Wargame]
tags: [leviathan, reverse, ltrace, linux, overthewire]
image:
  path: /assets/img/posts/leviathan-cover.png
  alt: Connexion SSH Leviathan OverTheWire
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

- Plutôt que de deviner, on va **observer** : `ltrace` intercepte les appels aux **bibliothèques dynamiques** — les morceaux de code partagés que le programme emprunte au système (`printf`, `strcmp`...) au lieu de les contenir lui-même. C'est analyser un programme de l'extérieur sans son code source — le cœur du **reverse engineering** :

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
- 💡 **Pourquoi `getchar` renvoie des nombres ?** Un ordinateur ne connaît pas les lettres : chaque caractère a un numéro officiel défini par la table **ASCII** (`'1'` = 49, `'2'` = 50, `'3'` = 51...). Les **trois appels** `getchar` de la trace correspondent aux trois caractères de `123`, lus un par un (les caractères tapés ne partent qu'à l'appui sur **Entrée**). La seule ligne qui compte reste `strcmp` : `getchar` décrit *comment* le programme lit, `strcmp` révèle *avec quoi* il compare — l'argument `"sex"` est la vraie information, pas le retour `-1`
- 🕵️ **Et les valeurs hexadécimales (`0x786573`, `0x646f67`) ?** Ce ne sont pas des arguments (`getchar` n'en prend aucun) : ce sont des **valeurs de registres** — les cases de stockage ultra-rapides du CPU — que `ltrace` affiche « par-dessus » faute de connaître la signature exacte. Petit easter egg : sur un processeur x86 (little-endian), charger les octets `'s' 'e' 'x'` comme un entier 32 bits donne exactement `0x786573` — le mot de passe est donc visible *deux fois* dans la trace ! 🥚
- `strcmp` renvoie `-1` ici (les chaînes diffèrent) ; il renverrait `0` si elles étaient identiques — c'est cette valeur que le programme teste pour accepter ou refuser
- En entrant le bon mot de passe, le programme (setuid) nous donne un shell **en tant que `leviathan2`** :

```bash
leviathan1@leviathan:~$ ./check
password: sex
$ cat /etc/leviathan_pass/leviathan2
ERJ9jTYWXE
```

- Comme pour Bandit, les mots de passe sont stockés dans `/etc/leviathan_pass/` (l'équivalent de `/etc/bandit_pass/`) et ne sont lisibles que par l'utilisateur concerné — ici c'est possible parce que le shell obtenu a les droits de `leviathan2`
- Ce niveau est une première vraie initiation au **reverse engineering** : analyser un programme sans son code source. `ltrace` (et son cousin `strace`, qui trace les **appels système** au lieu des appels de bibliothèque) sont les premiers outils à essayer face à un binaire inconnu, avant même d'ouvrir un désassembleur comme `objdump` ou `gdb`

### 🛠️ Commandes clés
`ls -la`, `./check`, `ltrace`, `strace -e trace=read,write`, `cat /etc/leviathan_pass/...`

---

## 🔬 Pour aller plus loin : ltrace vs strace

Deux étages d'observation d'un même programme :

- **`ltrace`** trace les appels aux **fonctions de bibliothèque** (libc : `printf`, `strcmp`, `getchar`, `fopen`…) — la *façade* que le programme utilise
- **`strace`** trace les **appels système** — les demandes directes au **noyau Linux** (`open`, `read`, `write`, `execve`, `socket`…) — le *moteur* qui fait vraiment le travail

**L'analogie du restaurant** : `ltrace` voit ce que le client commande au comptoir (« un café »), `strace` voit ce qui se passe en cuisine (moudre le café, verser l'eau...). Un appel de bibliothèque englobe souvent plusieurs appels système : `printf` finit par faire un `write`, `getchar` un `read`, `fopen` un `open`.

Le même programme `check` vu par les deux outils (`strace` est schématisé : la trace réelle est noyée sous le bruit du chargeur dynamique, voir plus bas) :

| `ltrace` | `strace` |
|---|---|
| `printf("password: ") = 10` | `write(1, "password: ", 10) = 10` |
| `getchar() = 49` | `read(0, "123\n", 1024) = 4` |
| `strcmp("123", "sex") = -1` | *(calcul interne au CPU, rien à tracer)* |
| `puts("Wrong password...") = 29` | `write(1, "Wrong password...\n", 29) = 29` |

- **`strcmp` n'apparaît jamais chez `strace`** : comparer deux chaînes est du pur calcul interne au CPU, aucune demande au noyau → rien à tracer. C'est exactement pourquoi `ltrace` est le bon outil sur ce niveau
- **Quand utiliser lequel ?** `ltrace` d'abord (comparaisons → mot de passe en clair, `fopen`, décodages) ; `strace` ensuite pour les fichiers/le réseau/les erreurs (`strace -e trace=openat,open ./prog`, `-f` pour suivre les processus enfants). Si `ltrace` ne montre rien (binaire statique), passe à `strace` — et inversement si `strace` est trop bavard
- ⚠️ **`strace` brut est bruyant** : avant `main`, le **chargeur dynamique** (chargement de la libc, ASLR…) produit des dizaines d'appels identiques pour *tous* les programmes — du bruit à ignorer. On le coupe avec `strace -e trace=read,write ./check`, on suit les enfants avec `-f` (au niveau 3, le bon mot de passe lance un shell : `strace -f ./level3` révélerait l'`execve("/bin/sh")`), et on peut tout écrire dans un fichier avec `-o trace.log`

Autre exemple parlant, `cat fichier.txt` :

| `ltrace` | `strace` |
|---|---|
| `fopen("fichier.txt", "r")` | `openat(AT_FDCWD, "fichier.txt", O_RDONLY) = 3` |
| `fread(…, 4096, 1, …)` | `read(3, "Bonjour le monde\n", 4096) = 17` |
| `fwrite(…, 1, 17, …)` | `write(1, "Bonjour le monde\n", 17) = 17` |
| `fclose(...)` | `close(3)` |

### 📌 À retenir

- **`ltrace`** = l'étage bibliothèque (logique du programme : `printf`, `strcmp`, `fopen`) ; **`strace`** = l'étage noyau (fichiers, descripteurs, réseau, erreurs) — un appel de bibliothèque englobe souvent plusieurs appels système
- **`strace` brut est bruyant** : le chargeur dynamique produit des dizaines d'appels avant `main` → filtrer avec `-e trace=read,write`, suivre les enfants avec `-f`
- Un binaire peut être **32 bits** (`strace` l'annonce : `runs in 32 bit mode`, libc chargée depuis `/usr/lib32/`) — fréquent sur les vieux wargames

---

## 🔬 Pour aller plus loin : méthode face à un binaire inconnu

La règle d'or du niveau 1 — **on ne devine pas, on observe** — et le principe directeur : *toujours commencer par le moins cher*. Un réflexe bonus avant même de tracer : `file ./binaire` — il donne d'un coup l'architecture (32/64 bits), le format (ELF) et la liaison (statique/dynamique), ce qui oriente déjà le choix des outils.

### 🪜 L'échelle des outils, du plus rapide au plus lourd

| Étape | Outil | Type | Ce qu'on cherche | Coût |
|---|---|---|---|---|
| 1 | `ltrace` | dynamique (appels libc) | `strcmp` avec chaîne en dur, `fopen`, `system`, décodages | quasi nul |
| 2 | `strace -e trace=…` | dynamique (noyau) | fichiers ouverts, réseau, erreurs (`ENOENT`, `EACCES`) | faible |
| 3 | `strings` | statique (fouille rapide) | mots de passe, chemins, indices cachés | faible |
| 4 | `objdump` / `readelf` | statique (désassemblage) | le code assembleur, la structure ELF, les sections | moyen |
| 5 | `gdb` | dynamique (pas à pas) | exécution contrôlée, registres, mémoire | élevé |

### 🧭 L'ordre, en une image

```text
 1. ltrace ───────────► trouvé ? ──► OUI : on exploite !
      │
      └── non
           ▼
 2. strace -e trace= ─► trouvé ? ──► OUI : on exploite !
      │
      └── non
           ▼
 3. strings ──────────► trouvé ? ──► OUI : on exploite !
      │                    ⚠️ méfie-toi des LEURRES
      └── non
           ▼
 4. objdump / readelf ─► trouvé ? ──► OUI : on exploite !
      │
      └── non
           ▼
 5. gdb ───────────────► dernier recours : pas à pas
```

### 🎯 L'essentiel de chaque étape

1. **`ltrace` — le réflexe n°1.** On cherche les appels « parlants » : comparaisons de chaînes, ouvertures de fichiers, exécutions de commandes (`system`). Le niveau 1 s'est résolu à cette seule étape
2. **`strace -e trace=…` — creuser le système.** Quels fichiers sont ouverts (`-e trace=openat,open`), quelles erreurs (`ENOENT`, `EACCES`), quelles connexions. ⚠️ **Cas particulier : binaire setuid.** Si `ltrace` échoue — c'est le cas au niveau 4, où `AT_SECURE` bloque `LD_PRELOAD` — passe directement à `strace` : il fonctionne toujours et donne la **cause exacte** (`openat = -1 EACCES`). `ltrace` dit *que* ça échoue, `strace` dit *pourquoi*
3. **`strings` — la fouille statique.** Extrait les chaînes imprimables du binaire *sans l'exécuter*. ⚠️ Attention au **security theater** : un binaire peut contenir de faux secrets pour égarer — le niveau 3 en est l'exemple parfait (`h0no33`, `kakaka` vs `snlprintf`). `strings` seul suggère, il ne prouve pas
4. **`objdump` / `readelf` — le désassemblage.** `objdump -d` montre l'assembleur, `readelf -h`/`-l`/`-x` la structure ELF — la *vraie* logique du programme, mais au prix d'un effort plus élevé. À réserver quand les traces ne suffisent plus
5. **`gdb` — la dernière carte.** Le débogueur : points d'arrêt, registres, mémoire, exécution pas à pas. Le plus puissant… et le plus exigeant

### 📌 À retenir

- **Du moins cher au plus cher** : `ltrace` → `strace -e trace=` → `strings` → `objdump`/`readelf` → `gdb` — dynamique avant statique
- **Croiser les outils** : `ltrace` montre les appels, `strings` montre les données — et `strings` seul peut tomber dans les leurres
- **Binaire setuid ?** `ltrace` peut échouer (`AT_SECURE` bloque `LD_PRELOAD`) — `strace` donne alors la cause exacte (`EACCES`)

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

- L'erreur vient d'un **contrôle de permissions** intégré au programme : il appelle `access()` *avant* de lire le fichier avec `cat` :

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

### 🔗 `ln -s` — le raccourci qui lit pour nous

- **Syntaxe** : `ln -s CIBLE NOM_DU_LIEN` — la **cible** (le fichier visé) en premier, le **nom du raccourci** en second. Piège classique de débutant : si on inverse, on crée un lien qui pointe vers un fichier inexistant
- Résultat : un fichier `a` dans le dossier courant, qui n'est qu'un *raccourci* vers la cible — `ls -l` l'affiche avec une flèche, et `readlink` montre la cible :

```bash
leviathan2@leviathan:/tmp/hs$ ls -l a
lrwxrwxrwx 1 leviathan2 leviathan2 29 Jun 24 15:05 a -> /etc/leviathan_pass/leviathan3
leviathan2@leviathan:/tmp/hs$ readlink a
/etc/leviathan_pass/leviathan3
```

- **Ouvrir le lien = ouvrir la cible** : quand le programme setuid lance `cat a`, le noyau suit le lien et lit le vrai fichier — avec les droits de `leviathan3`. Nous ne pouvons pas lire `/etc/leviathan_pass/leviathan3` directement, mais le programme setuid, lui, le peut, et un simple lien suffit à lui faire lire *notre* cible
- On retrouvera ce réflexe au niveau 5 (`ln -s /etc/leviathan_pass/leviathan6 /tmp/file.log`) : le symlink est l'outil n°1 pour détourner la lecture d'un programme privilégié

### 🛠️ Commandes clés
`ln -s`, `touch 'a b'`, `~/printfile 'a b'`, `ltrace`

---

## 🔬 Pour aller plus loin : access(), UID réel vs effectif, TOCTOU

C'est LE niveau le plus intéressant du wargame. Il mêle trois notions :

### 👤 UID réel vs UID effectif

| | Définition | Exemple |
|---|---|---|
| **UID réel (RUID)** | L'utilisateur qui a *lancé* le processus | `leviathan2` (nous) |
| **UID effectif (EUID)** | L'utilisateur dont le processus a *les droits* | `leviathan3` (grâce au setuid) |

Normalement RUID = EUID. Le bit **setuid** décale l'EUID : le programme tourne avec les droits de son **propriétaire**, pas de celui qui l'exécute. C'est exactement le mécanisme de `sudo`, de `passwd` (qui doit pouvoir modifier `/etc/shadow`)… et de nos binaires `check`, `printfile` et autres.

### ⚠️ Pourquoi `access()` est-il dangereux ?

`access()` répond à la question : « *l'utilisateur réel peut-il lire ce fichier ?* » — mais elle **ne vérifie pas** si l'utilisateur *effectif* le peut. Utiliser `access()` pour *autoriser* puis `cat` pour *lire* crée un écart entre **la vérification** (RUID) et **l'action** (EUID). Le manuel Linux (`man 2 access`) le dit noir sur blanc : c'est **une faille de sécurité** (catégorie **CWE-367 TOCTOU** — *Time Of Check To Time Of Use*, l'écart entre le moment où l'on vérifie et le moment où l'on utilise).

### 🪞 Le bug d'argument : deux lecteurs, deux grammaires

```
            "a b"
               │
   ┌───────────┴───────────┐
access("a b")          cat a b
   UN SEUL chemin       DEUX fichiers
   → vérifie "a b"      → lit "a" PUIS "b"
   (existe, OK)         → "a" = lien → mot de passe !
```

`access()` traite l'argument comme une **chaîne unique** ; `cat` le découpe aux **espaces**. L'écart de grammaire = la faille — un principe de *parsing confusion* qu'on retrouve aussi bien en web qu'en binaire.

### 📌 À retenir

- **UID réel** = qui je suis ; **UID effectif** = pour qui j'agis (setuid)
- `access()` vérifie le **RUID** → à ne jamais utiliser comme garde-fou avant une action
- Un **espace dans un nom de fichier** permet de tromper `access()` tout en laissant `cat` lire deux fichiers
- Un **lien symbolique** redirige une lecture vers n'importe quel fichier

---

## Level 3 → Level 4

**Objectif** : Encore un binaire setuid, cette fois `level3`, appartenant à `leviathan4`. Il demande un mot de passe. Même réflexe que le niveau 1 : on ne devine pas, on **observe**.

### 🔍 Découvertes

- Un `ls -la` montre le binaire setuid ; le lancer affiche un prompt tout simple :

```bash
leviathan3@leviathan:~$ ls -la
-r-sr-x---   1 leviathan4 leviathan3 18164 Jun 24 15:00 level3
leviathan3@leviathan:~$ ./level3
Enter the password> 123
bzzzzzzzzap. WRONG
```

- On trace avec `ltrace` — et cette fois la trace contient une surprise :

```bash
leviathan3@leviathan:~$ ltrace ./level3
__libc_start_main(["./level3"] <unfinished ...>
strcmp("h0no33", "kakaka")      = -1
printf("Enter the password> ")  = 20
fgets("123\n", 256, 0xf7fa85a0) = 0xffffd26c
strcmp("123\n", "snlprintf\n")  = -1
puts("bzzzzzzzzap. WRONG")      = 19
```

*(Comme au niveau 1, la trace de `ltrace` — écrite sur `stderr` — et l'affichage du programme — sur `stdout` — s'entremêlent sur le terminal ; j'ai séparé les deux pour la lisibilité.)*

- La trace se lit comme une recette, dans l'ordre :
  1. **`strcmp("h0no33", "kakaka")`** — une comparaison **factice** : le programme compare deux chaînes codées en dur, et **aucune des deux n'est notre saisie** ! Ce sont des **leurres** (decoys) : de faux mots de passe pour égarer la fouille (détail plus bas)
  2. **`printf("Enter the password> ")`** — l'affichage du prompt
  3. **`fgets("123\n", 256, ...)`** — la lecture de la saisie : `fgets` lit **toute la ligne, y compris le retour à la ligne** (le `\n` du Enter)
  4. **`strcmp("123\n", "snlprintf\n")`** — LA comparaison qui compte : notre saisie est comparée à `snlprintf\n`. Le vrai mot de passe est **`snlprintf`** (le `\n` vient de `fgets`, détail plus bas)
  5. **`puts("bzzzzzzzzap. WRONG")`** — le refus, si la comparaison échoue

- En entrant le bon mot de passe, le programme (setuid) affiche `[You've got shell]!` et lance un shell **en tant que `leviathan4`** :

```bash
leviathan3@leviathan:~$ ./level3
Enter the password> snlprintf
[You've got shell]!
$ id
uid=12004(leviathan4) gid=12003(leviathan3) groups=12003(leviathan3)
$ cat /etc/leviathan_pass/leviathan4
XIyBbRwAPt
$ exit
```

- Détail du `id` : `uid=12004(leviathan4)` confirme que le setuid a fait son travail — le shell a les droits de `leviathan4`, d'où la lecture possible du fichier de mot de passe. Le groupe reste `leviathan3` : normal, le bit setuid ne change que l'**UID effectif**, pas le groupe
- 💡 **Rappel du niveau précédent** : au niveau 2, on avait déjà créé un lien `a` avec `ln -s` pour détourner la lecture du programme setuid. Ici, pas besoin de détournement : le programme nous offre lui-même un shell — mais le mécanisme est le même, un binaire setuid agit avec les droits de son propriétaire (`leviathan4`)

### 🛠️ Commandes clés
`ls -la`, `./level3`, `ltrace`, `strings`, `cat /etc/leviathan_pass/...`

---

## 🔬 Pour aller plus loin : les leurres (decoys) et le `\n` de `fgets`

### 🎭 De faux mots de passe dans le binaire

- Le binaire `level3` contient **trois chaînes** qui ont toutes la tête d'un mot de passe : `h0no33`, `kakaka`… et `snlprintf`. Deux sur trois sont des **leurres** : seul `snlprintf` (avec son `\n`) fonctionne. `strings` permet de les voir d'un coup d'œil, sans exécuter le binaire :

```bash
leviathan3@leviathan:~$ strings ./level3 | grep -E 'h0no33|kakaka|snlprintf'
h0no33
kakaka
snlprintf
```

- Un attaquant pressé fouille le binaire avec `strings`, essaie `h0no33` ou `kakaka`… et obtient `bzzzzzzzzap. WRONG` à chaque fois. La fausse piste fait perdre du temps — une protection « anti-analyste » naïve, du **security theater** : ça ne ralentit que celui qui ne vérifie pas ce que le programme fait *vraiment*
- Le premier `strcmp("h0no33", "kakaka")` de la trace est l'empreinte de ce leurre : un appel **mort** — son résultat est jeté, **notre saisie n'est jamais impliquée**. Il n'existe que pour apparaître dans une trace et faire douter. La parade : `ltrace` montre les **vrais** appels, leurres compris — seule la comparaison avec notre saisie compte

### ⌨️ Pourquoi le `\n` dans `strcmp("123\n", "snlprintf\n")` ?

- Le programme lit la saisie avec `fgets` (pas `getchar` comme au niveau 1) : il lit **toute la ligne**, caractères tapés **plus le retour à la ligne** envoyé par Entrée. La chaîne stockée dans le binaire contient donc elle-même un `\n` final — `"snlprintf\n"` — et c'est ce qui fait partie du secret
- Conséquence amusante : `echo -n snlprintf | ./level3` (sans le saut de ligne) échouerait — le `\n` fait partie du mot de passe à fournir !

### 📌 À retenir

- Un binaire peut contenir de **faux secrets** (decoys) pour égarer `strings` ; seule l'observation des appels (`ltrace`) montre ce qui compte vraiment
- Un appel de fonction **mort** (résultat jeté, saisie jamais impliquée) = probablement un leurre
- `fgets` conserve le `\n` → si `strcmp` compare contre `"xxx\n"`, le saut de ligne fait partie du mot de passe à fournir

---

## Level 4 → Level 5

**Objectif** : Un dossier `.trash` (la corbeille) cache un binaire `bin` avec le bit setuid. Exécuté, il affiche des nombres binaires — le mot de passe de `leviathan5`, simplement encodé.

### 🔍 Découvertes

- Le répertoire personnel ne contient qu'un dossier à l'accès restreint : `.trash`, lisible par notre groupe (`leviathan4`) mais pas par tout le monde :

```bash
leviathan4@leviathan:~$ ls -la
dr-xr-x---   2 root leviathan4 4096 Jun 24 15:01 .trash
```

- On y entre (on est dans le groupe `leviathan4`) et `ls -ls` révèle un unique binaire setuid de 14 Ko :

```bash
leviathan4@leviathan:~$ cd ./.trash/
leviathan4@leviathan:~/.trash$ ls -ls
16 -r-sr-x--- 1 leviathan5 leviathan4 14936 Jun 24 15:01 bin
```

- Réflexe du niveau 1 : on trace avec `ltrace`… et surprise, ça **échoue** :

```bash
leviathan4@leviathan:~/.trash$ ltrace ./bin
fopen("/etc/leviathan_pass/leviathan5", "r")   = nil
+++ exited (status 255) +++
```

- Le programme veut ouvrir le mot de passe de `leviathan5` — mais `fopen` renvoie `nil` (NULL, l'échec) et le programme sort avec le code **255**. Pourquoi échoue-t-il sous `ltrace`, alors que le bit setuid devrait lui donner les droits de `leviathan5` ?
  - `ltrace` intercepte les appels de bibliothèque en injectant sa bibliothèque via la variable d'environnement **`LD_PRELOAD`**
  - Or, pour un binaire **setuid**, le noyau active le *secure-execution mode* (drapeau **`AT_SECURE`**) : le chargeur dynamique `ld.so` **ignore** `LD_PRELOAD`, précisément pour empêcher d'injecter du code dans un programme privilégié
  - `ltrace` retombe alors sur un traçage par `ptrace` dans lequel les privilèges setuid ne sont pas appliqués : le programme tourne avec nos droits (leviathan4), ne peut pas lire le fichier protégé → `fopen = nil` → exit 255

- **Vérification au niveau noyau avec `strace`** — la trace confirme le diagnostic, avec la cause exacte en prime. `strace` n'intercepte aucune bibliothèque (rien à bloquer) : il observe les appels système, et il montre la **preuve** de l'échec :

```bash
leviathan4@leviathan:~/.trash$ strace ./bin
execve("./bin", ["./bin"], 0x7fffffffe360) = 0
[ Process PID=132 runs in 32 bit mode. ]
... (bruit du chargeur identique au niveau 1 : openat de la libc, mmap2, mprotect, getrandom…) ...
openat(AT_FDCWD, "/etc/leviathan_pass/leviathan5", O_RDONLY) = -1 EACCES (Permission denied)
exit_group(-1)                          = ?
+++ exited with 255 +++
```

  - **La ligne qui compte** : `openat(..., "/etc/leviathan_pass/leviathan5", O_RDONLY) = -1 EACCES`. `EACCES` = *Permission denied* : le noyau répond « tu n'as pas le droit ». Or si le setuid avait fonctionné, le processus (EUID = leviathan5) aurait **le droit** de lire ce fichier, propriété de leviathan5 ! L'`EACCES` est donc la preuve irréfutable que le programme tourne avec **nos** droits (leviathan4) pendant le tracing
  - À comparer avec `ltrace` : il montrait `fopen = nil` (la fonction de bibliothèque échoue, sans dire pourquoi) ; `strace` montre l'appel système `openat = -1 EACCES` (le noyau explique *pourquoi*). Deux étages, même échec — mais `strace` donne la raison exacte. C'est exactement la leçon de la section « ltrace vs strace » du niveau 1

- **Mais peu importe !** C'est un cas d'école de la *méthode face à un binaire inconnu* vue au niveau 1 : l'étape 1 (`ltrace`) est bloquée par le setuid, on saute à l'étape 3 — **`strings`** — qui révèle tout, d'autant que le binaire **n'est pas strippé** (sa table de symboles est intacte) :

```bash
leviathan4@leviathan:~/.trash$ strings bin | grep -E 'leviathan_pass|fgets|putchar|fopen|strlen|bin.c'
/etc/leviathan_pass/leviathan5
fgets
putchar
fopen
strlen
bin.c
```

  - Le chemin du fichier visé (`/etc/leviathan_pass/leviathan5`) et les fonctions utilisées : `fopen` (ouvrir), `fgets` (lire une ligne), `strlen` (mesurer), `putchar` (afficher caractère par caractère) — on peut même **reconstituer le code source** : ouvrir le fichier, lire la ligne, et pour chaque caractère imprimer son écriture binaire
  - Bonus forensics : le nom du fichier source (`bin.c`) apparaît, ainsi que `__wrap_main` (le binaire a été compilé avec l'astuce de linker `--wrap=main`) et l'empreinte compilateur `GCC 15.2.0`

- Et effectivement : en lançant simplement `./bin`, le programme fait le travail **pour nous** — il imprime le mot de passe… en binaire :

```bash
leviathan4@leviathan:~/.trash$ ./bin
01000010 01110101 01100010 00111001 01100111 01011010 00110011 01000010 01000111 01010101 00001010
```

- 💡 Chaque groupe de 8 bits est un **octet** = un **code ASCII** : `01000010` = 66 = `'B'`, `01110101` = 117 = `'u'`… Le binaire nous affiche le secret, simplement **encodé** — une transformation de base réversible sans clé, pas un vrai chiffrement
- Pour décoder, deux options : la **one-liner Perl** utilisée dans la session, ou le **script Python** classique :

```bash
leviathan4@leviathan:~/.trash$ echo "01000010 01110101 01100010 00111001 01100111 01011010 00110011 01000010 01000111 01010101" | perl -lape 's/([01]{8})\s*/chr(oct("0b$1"))/eg'
Bub9gZ3BGU
```

```python
nums = open('nums.txt', 'r').read().split()
for i in range(len(nums)):
    nums[i] = chr(int(nums[i], 2))
password = ""
print(password.join(nums))
```

*(Raccourci : rediriger la sortie — `./bin > nums.txt` — puis lancer le script Python.)*

- Résultat : **`Bub9gZ3BGU`**, le mot de passe de `leviathan5`. *(Les mots de passe OverTheWire tournent régulièrement : c'est bien la valeur de la session actuelle, pas celle des vieux writeups.)*

### 🛠️ Commandes clés
`cd .trash`, `ls -ls`, `ltrace`/`strace -e trace=openat` (échouent sur setuid, `AT_SECURE`), `strings bin`, `./bin`, one-liner Perl (`perl -lape`), script Python (`int(x, 2)` + `chr()`)

---

## 🔬 Pour aller plus loin : binaire, octets et ASCII

### 🧮 Comprendre `int(x, 2)` et `chr()`

- Le binaire est une **base 2** : chaque bit vaut une **puissance de 2** selon sa position (`01000101` = 4 + 16 + 64 = 69)
- `int("01000101", 2)` → 69 : conversion **binaire → entier** ; `chr(69)` → `'E'` : conversion **entier → caractère ASCII**. C'est exactement ce que fait le script ligne par ligne, en une boucle
- 8 bits = 2⁸ = 256 valeurs possibles (0 à 255) — de quoi coder les 128 caractères ASCII de base. Un **octet** est l'unité de base de la mémoire : `xxd`, `hexdump`, `strings` ne font que relire ces octets autrement

### 🐪 La one-liner Perl décortiquée

```bash
echo "01000010 01110101 ..." | perl -lape 's/([01]{8})\s*/chr(oct("0b$1"))/eg'
```

Elle fait le même travail que le script Python, mais tout est condensé :

- **`perl -lape`** : `-e` = le programme est passé en argument, `-p` = lire l'entrée ligne par ligne et afficher le résultat, `-l` = gérer les fins de ligne, `-a` = découper chaque ligne en champs (classique)
- **`s/.../.../eg`** : une **substitution** de texte (comme `sed`) — le `e` dit que le remplacement est une *expression* Perl à évaluer, le `g` = *global*, on remplace toutes les occurrences
- **`([01]{8})`** : le motif cherché — un groupe d'exactement **8 bits** (`[01]` = un bit, `{8}` = répété 8 fois), capturé dans `$1`. **`chr(oct("0b$1"))`** préfixe en binaire (`0b...`), convertit en **nombre** (`oct`), puis en **caractère** (`chr`) — exactement `int(x, 2)` puis `chr()` du Python

### ⏎ Et ce `00001010` final ?

La dernière valeur de la sortie de `./bin`, `00001010` = 10, est le code ASCII du **retour à la ligne** (`\n`) ! Parce que `fgets` — on l'a vu au niveau 3 — conserve le `\n` : le programme convertit *chaque* caractère du fichier en binaire, newline comprise. Ce n'est pas un bug : c'est la preuve que le programme traite tout le contenu du fichier. Dans la one-liner Perl de la session, il n'apparaît d'ailleurs pas — l'`echo` ne l'a pas transmis.

### 📌 À retenir

- Binaire (base 2) → entier → caractère : la chaîne de conversion universelle
- Un « chiffrement » qui se contente de changer de base n'en est **pas un** : c'est de l'**encodage**
- Python : `int(x, 2)`, `chr()`, `ord()` (l'inverse de `chr`) — à connaître par cœur ; Perl : `chr(oct("0b$1"))` — la même chose en une ligne
- **`ltrace` échoue sur les binaires setuid** (`AT_SECURE` ignore `LD_PRELOAD`) ; `strace` en montre la cause : `openat = -1 EACCES` → passer directement à `strings` + exécution
- Un binaire **non strippé** (comme `bin`) garde ses symboles : `strings` révèle fonctions, chemins et même le nom du fichier source

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
leviathan5@leviathan:~$ ls -la
total 36
drwxr-xr-x   2 root       root        4096 Jun 24 15:00 .
drwxr-xr-x 150 root       root        4096 Jun 24 15:02 ..
-rw-r--r--   1 root       root         220 Feb 13 12:16 .bash_logout
-rw-r--r--   1 root       root        3851 Jun 24 14:50 .bashrc
-rw-r--r--   1 root       root         807 Feb 13 12:16 .profile
-r-sr-x---   1 leviathan6 leviathan5 15140 Jun 24 15:00 leviathan5
leviathan5@leviathan:~$ ./leviathan5
JRGj9iWNOb
```

- 💪 **Ma session réelle** : le `ls -la` confirme le binaire setuid (`r-s` = bit setuid, propriétaire `leviathan6`, groupe `leviathan5`) — et le programme affiche bien le mot de passe : **`JRGj9iWNOb`**

- C'est le même principe que le niveau 2 (utiliser un setuid pour lire un fichier qu'on ne peut pas lire directement), mais en beaucoup plus simple : ici, **aucune vérification** n'est faite, le programme lit directement le chemin — et un lien symbolique détourne cette lecture.

### 🎯 Pourquoi le symlink fonctionne ? — la logique du programme

La trace révèle un programme sans la moindre vérification — en C, il ressemble à ceci :

```c
FILE *f = fopen("/tmp/file.log", "r");   // 1. chemin codé en dur, AUCUNE vérification
if (f == NULL) {
    puts("Cannot find /tmp/file.log");    // fichier absent → erreur
    exit(1);
}
char buf[4096];
fread(buf, 1, sizeof(buf), f);            // 2. lit le contenu
printf("%s", buf);                        // 3. l'affiche (le mot de passe !)
remove("/tmp/file.log");                  // 4. supprime le fichier de log
```

```bash
leviathan5@leviathan:~$ strace ./leviathan5
open("/tmp/file.log", O_RDONLY)      = 3
read(3, "...", 4096)                 = 11
unlink("/tmp/file.log")              = 0
```

| Ligne de la trace | Ce que ça signifie |
|---|---|
| `open("/tmp/file.log", O_RDONLY) = 3` | Ouvre le chemin `/tmp/file.log`… mais le noyau **suit le lien** et ouvre en réalité `/etc/leviathan_pass/leviathan6`. L'ouverture se fait avec les **droits effectifs** de `leviathan6` (le setuid) → le fichier protégé devient lisible |
| `read(3, "...", 4096) = 11` | Lit le contenu : **11 octets** = les 10 caractères du mot de passe + le `\n` (le `\n` sournois du niveau 3 !) |
| *(l'affichage)* | Le programme imprime ce qu'il a lu → **`JRGj9iWNOb`** |
| `unlink("/tmp/file.log") = 0` | Supprime l'entrée `/tmp/file.log` : c'est le **lien** qui disparaît, **pas la cible** — `/etc/leviathan_pass/leviathan6` reste intact |

Trois raisons pour lesquelles ça marche :

1. **Aucune vérification** : contrairement au niveau 2 (`access()`), le programme ne contrôle ni le propriétaire ni la nature du fichier — il ouvre le chemin, point final
2. **Le noyau suit le lien transparentement** : `open("/tmp/file.log")` devient un `open` de la cible, et le programme ne s'aperçoit même pas qu'il lit un autre fichier
3. **Le setuid fait le reste** : le processus tourne avec l'EUID de `leviathan6`, donc l'ouverture de la cible (propriété de leviathan6) réussit — alors qu'en tant que `leviathan5`, on n'y aurait jamais eu accès

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

- 4 chiffres → 10 000 combinaisons possibles (0000 à 9999). On lance une boucle `for` : tester chaque code, filtrer la sortie pour ne garder que ce qui n'est pas « Wrong », et **espacer les essais** pour ne pas épuiser les ressources du serveur :

```bash
leviathan6@leviathan:~$ for i in {0..10000}; do echo "trying $i"; ./leviathan6 $i | grep -v "Wrong"; sleep 0.005; done
```

- 🐌 Le `sleep 0.005` n'est pas une option : sans lui, la boucle lance des milliers de processus à la seconde et le serveur finit par refuser (`fork: retry: No child processes`). Ma session réelle le confirme : à ~5 ms par essai, la boucle entière prend environ une minute.
- Le bon code est **`7123`** : la boucle s'arrête sur un **shell en tant que `leviathan7`** !

```bash
leviathan6@leviathan:~$ ./leviathan6 7123
$ cat /etc/leviathan_pass/leviathan7
3zrlkaPTfH
$ exit
```

### 🎯 Pourquoi `7123` ? — la logique du programme

💪 **Ma session réelle** : le shell s'est ouvert sur le code `7123` et `cat` a affiché le mot de passe **`3zrlkaPTfH`**. Le `ltrace` du même passage révèle la logique complète du programme — en C, il ressemble à ceci :

```c
if (atoi(argv[1]) == 7123) {          // 1. le code est codé en dur dans le binaire
    setreuid(geteuid(), geteuid());   // 2. devenir définitivement le propriétaire
    system("/bin/sh");                // 3. lancer un shell avec ces droits
} else {
    puts("Wrong");                    // sinon : refus
}
```

```bash
leviathan6@leviathan:~$ ltrace ./leviathan6 7123
atoi(0xffffd607, 0xf7fc3000, 0, 0)        = 7123
geteuid()                                 = 12006
geteuid()                                 = 12006
setreuid(12006, 12006)                    = 0
system("/bin/sh" ...)                     = ?   # la trace s'arrête : le shell a pris la main
```

| Ligne de la trace | Ce que ça signifie |
|---|---|
| `atoi(...) = 7123` | **`atoi`** convertit la chaîne `"7123"` en **entier** — le programme compare des nombres, pas du texte. Avec `1234` : `= 1234` → l'entier ne vaut pas 7123 → `puts("Wrong")` et exit |
| `geteuid()` = 12006 | Lit l'**UID effectif** — l'utilisateur dont le processus a les droits. Appelé **deux fois** : une pour chaque argument de `setreuid` |
| `setreuid(12006, 12006) = 0` | Fixe l'**UID réel** *et* l'**UID effectif** à la même valeur → l'escalade de privilèges devient **permanente** (le processus ne « redescend » pas ensuite). Le `= 0` = succès |
| `system("/bin/sh")` | Lance un **shell** avec ces droits — c'est le `$` qu'on récupère |
| *(tout autre code)* | `puts("Wrong")` : le test `== 7123` a échoué → pas de shell |

⚠️ **Détail important sur le `12006`** : sous `ltrace`, les privilèges setuid ne sont pas appliqués (la leçon du niveau 4) — `geteuid()` renvoie donc 12006 = **leviathan6**, pas leviathan7 (le post établit plus haut que leviathan4 = 12004). En exécution **normale**, le setuid fait de l'UID effectif celui de `leviathan7` (12007) : `setreuid(12007, 12007)` puis le shell gardent ces droits, et c'est pour ça que `cat /etc/leviathan_pass/leviathan7` fonctionne.

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
