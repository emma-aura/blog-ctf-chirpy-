---
title: ressources
icon: fas fa-bookmark
order: 5
---

> Une collection de ressources soigneusement sélectionnées dans l'univers de la cybersécurité offensive, du CTF et du reverse engineering. Cette page évolue au fil de mes découvertes.
{: .prompt-info }

## 🧭 Comment lire cette page

Chaque ligne suit la même logique : **ce que c'est**, puis **quand / pourquoi l'ouvrir** (avec les commandes ou options clés quand elles existent). Le but n'est pas de tout lire, mais de choisir le bon outil en quelques secondes.
{: .prompt-tip }

| Si je veux... | Commence par |
|---|---|
| Comprendre un binaire ou un malware | Dogbolt, Reverse.zip, MalwareUnicorn, OST2 |
| Reconnaître et cartographier une cible (réseau, web) | Top 1 000 ports Nmap, ffuf, Gobuster, **EyeWitness** |
| Auditer un site WordPress | WPScan |
| Passer d'un shell bancal à un vrai TTY | Reverse Shell Cheat Sheet, ropnop, Spawn TTY (Swissky) |
| Élever mes privilèges sur Linux | LinPEAS, linux-exploit-suggester, linuxprivchecker, LinEnum, lse, pspy, GTFOBins |
| Élever mes privilèges sur Windows | WinPEAS, PrivescCheck, Seatbelt, JAWS, WES-NG |
| Trouver un exploit / un PoC pour une CVE | Exploit-DB, Rapid7 DB, Vulnerability-Lab |
| Monter un C2 / faire du red team | Sliver (+ GUI), Havoc, Empire, Starkiller |
| M'entraîner sur des CTF et des wargames | OverTheWire, UnderTheWire, Hack The Box, TryHackMe, Root-Me, CTFtime |
| Monter un lab vulnérable chez moi | Juice Shop, DVWA, Metasploitable 2 & 3 |
| Suivre des writeups et la veille | 0xdf, IppSec, LiveOverflow, jaxafed, HackTricks, The DFIR Report, ce blog 😉 |
| Me former (cours, certifs) | Grafikart, The CTF Primer, Red Team Leaders |

---

## 🔬 Reverse Engineering & Malware

### 🧩 Décompilateurs & analyse de binaires

| Ressource | Lien | Description |
|---|---|---|
| Reverse.zip | [https://reverse.zip/](https://reverse.zip/) | Plateforme complète de reverse engineering : cours, challenges et outils pour progresser du désassemblage à l'exploitation |
| Dogbolt | [https://dogbolt.org/](https://dogbolt.org/) | Compare plusieurs décompilateurs (Ghidra, IDA, Binary Ninja...) sur un même binaire |
| Binary Ninja | [https://binary.ninja/](https://binary.ninja/) | Suite de reverse engineering (décompilateur, désassembleur, débogueur) pensée pour l'automatisation : API C++/Python/Rust, plugins, visualisation du control flow et des piles, Time Travel Debugging, triage rapide — essai gratuit et édition Cloud |
| REA — Reverse Engineer Anything (sgunin) | [https://github.com/sgunin/ReverseEngineerAnything](https://github.com/sgunin/ReverseEngineerAnything) | Reverse engineering assisté par agents, du comportement d'une app jusqu'aux binaires natifs : REA branche les outils d'analyse (Hopper, Ghidra en lecture seule sur Linux/macOS, inspection JavaScript/Electron, assemblies .NET, observation de pages via Chrome CDP) sur un agent par CLI et serveur MCP. Démarrage : `npx -y rea-agents@latest doctor` puis `npx -y rea-agents@latest analyze /chemin/app`, ou configuration MCP manuelle (`npx -y rea-agents@3.2.1 mcp`). Commandes utiles : `analyze`, `inspect`, `search`, `function`, `xrefs`, `trace`, `capabilities`, `providers`. L'analyse tourne en local, et chaque conclusion arrive avec ses preuves, sa confiance et ses limites |

### 🧪 Apprendre le reverse

| Ressource | Lien | Description |
|---|---|---|
| MalwareUnicorn Workshops | [https://malwareunicorn.org/#/workshops](https://malwareunicorn.org/#/workshops) | Ateliers de reverse engineering et d'analyse de malware par Amanda Rousseau (MalwareUnicorn), dont le célèbre « Reverse Engineering Malware 101 » |
| OpenSecurityTraining2 | [https://p.ost2.fyi/courses](https://p.ost2.fyi/courses) | Formations gratuites en sécurité : reverse engineering, exploitation binaire, architecture CPU... |

## 🏴 CTF & Wargames

### 🎮 Plateformes & wargames

| Ressource | Lien | Description |
|---|---|---|
| OverTheWire — Wargames | [https://overthewire.org/wargames/](https://overthewire.org/wargames/) | L'index de tous les wargames OverTheWire : Bandit (bases shell), Leviathan (SUID/binaires), Natas (web), Narnia, Behemoth, Utumno (exploitation binaire), Maze, Vortex, Semtex, Manpage, Krypton... Chaque jeu est accessible en SSH et se débloque niveau par niveau |
| OverTheWire - Bandit | [https://overthewire.org/wargames/bandit/](https://overthewire.org/wargames/bandit/) | Wargame Linux pour apprendre la sécurité UNIX |
| OverTheWire - Leviathan | [https://overthewire.org/wargames/leviathan/](https://overthewire.org/wargames/leviathan/) | Wargame orienté reverse engineering et binaires setuid |
| UnderTheWire | [https://underthewire.tech/wargames](https://underthewire.tech/wargames) | Les wargames PowerShell, l'équivalent OverTheWire côté Windows : cinq jeux de 15 niveaux (Century pour les bases, Cyborg et Groot en intermédiaire, Oracle et Trebek en avancé) accessibles en SSH sur `*.underthewire.tech`, avec les identifiants de départ via leur Slack. Enumerate, filter, verify — chaque niveau est un petit puzzle d'incident response |
| Hack The Box | [https://www.hackthebox.com/](https://www.hackthebox.com/) | Plateforme de pentest avec machines et challenges variés |
| TryHackMe | [https://tryhackme.com/](https://tryhackme.com/) | Apprentissage guidé en cybersécurité, du niveau débutant au niveau avancé |
| picoCTF | [https://picoctf.org/](https://picoctf.org/) | CTF éducatif organisé par Carnegie Mellon University, idéal pour débuter |
| Root-Me | [https://www.root-me.org/](https://www.root-me.org/) | Plateforme francophone de challenges en sécurité offensive |
| CTF Armée de l'Air et de l'Espace (Root-Me) | [https://armee-air-espace.challenges.root-me.pro/](https://armee-air-espace.challenges.root-me.pro/) | CTF officiel de l'Armée de l'Air et de l'Espace : deux missions (Opération AEGIS, douze étapes) autour d'une liaison de drone compromise et d'une chaîne de mise à jour satellite vérolée — catégories réseau, forensic, radiofréquence, reverse engineering et pentest |
| CTFtime | [https://ctftime.org/](https://ctftime.org/) | Calendrier mondial des CTF, classements d'équipes et archives de write-ups |

### 🧪 Labs vulnérables (à héberger soi-même)

| Ressource | Lien | Description |
|---|---|---|
| OWASP Juice Shop | [https://owasp.org/projects/juice-shop](https://owasp.org/projects/juice-shop) | Application web volontairement vulnérable (Node.js/Express/Angular) couvrant tout l'OWASP Top 10, avec des dizaines de challenges de difficulté croissante — se lance en une commande Docker (`docker run -p 3000:3000 bkimminich/juice-shop`) ou via `npm start`, et sert aussi de cobaye pour tester un scanner |
| DVWA — Damn Vulnerable Web Application | [https://github.com/digininja/DVWA](https://github.com/digininja/DVWA) | Application PHP/MariaDB concentrée sur les vulnérabilités web classiques (SQLi, XSS, LFI, upload, CSRF, command injection, brute force), avec 4 niveaux de difficulté (low → impossible) pour voir l'impact des protections et des contournements. **À ne jamais exposer sur Internet** : à faire tourner en VM ou en conteneur local |
| Metasploitable 2 — guide d'exploitabilité (Rapid7) | [https://docs.rapid7.com/metasploit/metasploitable-2-exploitability-guide/](https://docs.rapid7.com/metasploit/metasploitable-2-exploitability-guide/) | Le guide officiel de la VM Metasploitable 2 : service par service, la vulnérabilité présente, comment la détecter avec Nmap/Metasploit et quel module utiliser — la carte du terrain avant de lancer un scan sur la machine |
| Metasploitable 3 | [https://github.com/rapid7/metasploitable3](https://github.com/rapid7/metasploitable3) | Successeur de Metasploitable 2 : des VM Windows Server 2008 et Ubuntu 14.04 construites avec Packer/Vagrant, bourrées de vulnérabilités modernes. Images prêtes à l'emploi sur Vagrant Cloud, ou build maison depuis le dépôt |

### 📝 Writeups & retours d'expérience

| Ressource | Lien | Description |
|---|---|---|
| 📌 Mon récap OverTheWire | [{% post_url 2026-08-03-overthewire-wargames-recapitulatif %}]({% post_url 2026-08-03-overthewire-wargames-recapitulatif %}) | Index de ma progression sur les wargames OverTheWire : Bandit & Leviathan complets, roadmap et compétences acquises |
| Writeup Leviathan (hrbrtschmu1l) | [https://hrbrtschmu1l.medium.com/leviathan-overthewire-wargame-writeup-dd3378a6136a](https://hrbrtschmu1l.medium.com/leviathan-overthewire-wargame-writeup-dd3378a6136a) | Writeup détaillé du wargame Leviathan (0→7) : SUID, ltrace, access() vs cat, bruteforce — source d'inspiration pour mes propres writeups |
| HackerLab Bénin 2026 — writeups (DazBot13-boopt) | [https://github.com/DazBot13-boopt/hackerlab-benin-2026-wu](https://github.com/DazBot13-boopt/hackerlab-benin-2026-wu) | Writeups du CTF HackerLab Bénin 2026 (format `HLB2026{...}`) rangés par épreuve : forensics Windows (ransomware XTEA-CTR, webshell + logs Apache, SAM/TS, prefetch + PowerShell history, USN journal), web (SSRF + bypass d'IP décimale), OSINT, stégo, AD/pentest (constrained delegation S4U, RBCD + MachineAccountQuota) et ICS (XXE, Modbus TCP) |
| HackerLab Bénin 2026 finale — writeups (achbelsdn) | [https://github.com/achbelsdn/hackerlab-2026-finale/blob/main/jeopardy/kiss-of-death.md](https://github.com/achbelsdn/hackerlab-2026-finale/blob/main/jeopardy/kiss-of-death.md) | Writeups de la finale HackerLab Bénin 2026 (équipe DIVISION_0), avec la mission « Kiss of Death » : extraction ADB d'un téléphone Android (`gesture.key`, `locksettings.db`), enquête OSINT sur six incidents attribués à un APT, décodage des *tracking dots* d'une imprimante avec `libdeda` — et la leçon sur le gabarit exact des flags |

## 📖 Documentation & Cheatsheets

### 📚 Références générales

| Ressource | Lien | Description |
|---|---|---|
| HackTricks (FR) | [https://hacktricks.wiki/fr/index.html](https://hacktricks.wiki/fr/index.html) | La bible du pentest en français : base de connaissances couvrant reconnaissance, web, cloud, Active Directory, exploitation binaire, privilege escalation, red team... Des centaines de pages de techniques pratiques avec commandes prêtes à l'emploi, également disponible hors-ligne via le dépôt GitHub (branche `fr`) et Docker |
| GitHub Topics — penetration-testing | [https://github.com/topics/penetration-testing](https://github.com/topics/penetration-testing) | L'index GitHub des dépôts taggés `penetration-testing`, classés par popularité : frameworks, scanners, scripts d'énumération, listes de skills pour agents IA... — le bon réflexe pour découvrir un projet avant de chercher ailleurs |
| PayloadsAllTheThings (Swissky) | [https://github.com/swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) | Le recueil de payloads et bypass de référence pour la sécurité web et le pentest/CTF : un chapitre par vulnérabilité (XSS, SQLi, SSRF, LFI/RFI, command injection, upload, SSTI, JWT...) avec description, techniques d'exploitation, fichiers prêts pour Burp Intruder et wordlists (ffuf) — versions web sur payloadsallthethings.com et projets frères InternalAllTheThings / HardwareAllTheThings |

### 🐚 Shells, TTY & terminaux

| Ressource | Lien | Description |
|---|---|---|
| InternalAllTheThings — Reverse Shell (Swissky) | [https://swisskyrepo.github.io/InternalAllTheThings/cheatsheets/shell-reverse-cheatsheet/](https://swisskyrepo.github.io/InternalAllTheThings/cheatsheets/shell-reverse-cheatsheet/) | Cheatsheet exhaustif sur les reverse shells : un payload par langage (bash, Python, PHP, nc, socat, PowerShell...), plus la section [`#spawn-tty-shell`](https://swisskyrepo.github.io/InternalAllTheThings/cheatsheets/shell-reverse-cheatsheet/#spawn-tty-shell) pour passer d'un shell « dumb » à un vrai TTY (`rlwrap` au catch, `stty raw -echo; fg`, `reset`, `export TERM=xterm-256color`) |
| Reverse Shell Cheat Sheet (pentestmonkey) | [https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet](https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet) | Le classique des one-liners de reverse shell : Bash, Perl, Python, PHP, Ruby, Netcat, Java, socat... à copier-coller dès qu'on a une exécution de commande. (Pour les Windows, remplacer `/bin/sh -i` par `cmd.exe`) |
| Reverse Shell Cheat Sheet (HighOn.Coffee) | [https://highon.coffee/blog/reverse-shell-cheat-sheet/](https://highon.coffee/blog/reverse-shell-cheat-sheet/) | Cheatsheet de secours quand pentestmonkey ne suffit pas : onelines Bash, Perl, Python, PHP, Ruby, Java, Netcat et PowerShell (dont la version encodée en Base64), la technique du `mkfifo` (backpipe dans `/tmp/f`, relu par `cat` et réinjecté dans `nc`) pour un netcat compilé sans `-e`, des payloads `msfvenom` prêts pour Linux, Windows et macOS, et une section « spawning a TTY » avec `python -c 'import pty;pty.spawn("/bin/bash")'`, `script -qc /bin/bash /dev/null` et `socat`. Pratique aussi pour les cibles où l'egress filtering impose de changer de port ou de protocole |
| Reverse Shell Cheatsheet (PayloadsAllTheThings) | [https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md) | La version Markdown de la cheatsheet reverse shell de Swissky (la même que sur `swisskyrepo.github.io`, mais en clair dans le dépôt) : payloads classés par langage — bash `bash -i >& /dev/tcp/...`, netcat (avec et sans `-e`), socat, Python, Perl, PHP, Ruby, Node.js, Java, PowerShell, awk et telnet — plus les `msfvenom` pour Linux/Windows/macOS, les techniques de contournement (`/dev/tcp`, `nc.openbsd`, encodage, obfuscation) et la section « spawn TTY » (`python -c`, `script`, `stty raw -echo` et `socat`). Utile pour copier les payloads directement depuis le dépôt ou pour faire un `curl` ciblé quand on n'a pas de navigateur sur la cible |
| Upgrading Simple Shells to Fully Interactive TTYs (ropnop) | [https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/) | Passer d'un shell netcat « dumb » à un vrai TTY : module `pty` de Python, `script`, socat, stty + job control, et les raccourcis clavier pour survivre à un Ctrl-C |
| Tmux Cheat Sheet (tmuxcheatsheet.com) | [https://tmuxcheatsheet.com/](https://tmuxcheatsheet.com/) | Référence rapide tmux (dispo en français) : sessions, fenêtres, panes, copier/coller, raccourcis avec le préfixe `Ctrl-b`, plus un générateur de `~/.tmux.conf` et des guides ciblés — l'indispensable quand on fait tourner plusieurs shells dans un même terminal |
| Pwntools | [https://docs.pwntools.com/en/stable/](https://docs.pwntools.com/en/stable/) | Documentation officielle de la librairie Python pour l'exploitation binaire |

### 💉 Web & injection

| Ressource | Lien | Description |
|---|---|---|
| SQL Injection Cheat Sheets (pentestmonkey) | [https://pentestmonkey.net/category/cheat-sheet/sql-injection](https://pentestmonkey.net/category/cheat-sheet/sql-injection) | Série complète de cheatsheets SQLi par moteur : MSSQL, MySQL, Oracle, PostgreSQL, DB2, Informix et Ingres — syntaxe pour version, current user, users/hashes, privileges, filesystem et command execution |
| MySQL SQL Injection Cheat Sheet (pentestmonkey) | [https://pentestmonkey.net/cheat-sheet/sql-injection/mysql-sql-injection-cheat-sheet](https://pentestmonkey.net/cheat-sheet/sql-injection/mysql-sql-injection-cheat-sheet) | Cheatsheet dédiée MySQL : `@@version`, `user()`, `mysql.user`, `information_schema`, lecture de fichiers via `LOAD_FILE()`/`INTO OUTFILE`, execution via UDF et techniques de bypass |
| OWASP Top 10:2025 | [https://top10.owasp.org/2025/](https://top10.owasp.org/2025/) | Référentiel des 10 risques majeurs des applications web (édition 2025), avec CWE associés, statistiques et contre-mesures. A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures, A10 Mishandling of Exceptional Conditions |
| Set up a local testing server (MDN) | [https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Tools_and_setup/set_up_a_local_testing_server](https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Tools_and_setup/set_up_a_local_testing_server) | Comment servir un dossier en HTTP en local, avec `python3 -m http.server`, `php -S localhost:8000` ou Node : indispensable quand une page chargée en `file://` refuse de fonctionner (CORS, modules ES, `fetch`), et pratique pour héberger un payload ou un fichier à faire télécharger sur une cible |
| Liste des codes HTTP (Wikipédia) | [https://en.wikipedia.org/wiki/List_of_HTTP_status_codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) | Référence complète des codes de statut HTTP (1xx à 5xx, plus les codes non standard des serveurs comme nginx ou Cloudflare) avec leur signification : indispensable pour interpréter un scan, filtrer les faux positifs en fuzzing (`-fc`, `-fs`...) et comprendre les réponses d'une webapp |

### 🖧 Systèmes, réseau & services

| Ressource | Lien | Description |
|---|---|---|
| GTFOBins | [https://gtfobins.org/](https://gtfobins.org/) | La référence des binaires Unix détournables sur un système mal configuré (SUID, sudo, capabilities, cron) : pour chacun, la technique qui permet de s'échapper d'un shell restreint, d'élever ou maintenir ses privilèges, de lire/écrire un fichier ou de lancer un bind/reverse shell — avec API JSON. Pour les binaires Windows, voir son équivalent LOLBAS |
| LOLBAS Project | [https://lolbas-project.github.io/](https://lolbas-project.github.io/) | Équivalent Windows de GTFOBins : le catalogue des *Living Off The Land Binaries, Scripts and Libraries* — binaires signés Microsoft (certutil, regsvr32, mshta, rundll32...) avec, pour chacun, les fonctions détournables (exécution, téléchargement, contournement d'AppLocker, persistance...), le type (binaries, scripts, libraries) et le mapping ATT&CK. Voir aussi LOLDrivers pour les pilotes |
| smbclient - man page | [https://www.samba.org/samba/docs/current/man-html/smbclient.1.html](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html) | Documentation officielle de `smbclient` (Samba) : syntaxe, options d'authentification (`-U`, `-W`, `-N`, `-k`), mode interactif et commandes internes (`ls`, `get`, `put`, `recurse`, `mask`, `prompt`, `mget`...) pour énumérer et manipuler des partages SMB depuis un shell |
| Top 1 000 ports TCP & UDP (Nmap) | [https://nullsec.us/top-1-000-tcp-and-udp-ports-nmap-default/](https://nullsec.us/top-1-000-tcp-and-udp-ports-nmap-default/) | Référence des ports scannés par défaut par Nmap, avec les commandes `--top-ports 1000` et les listes prêtes à copier (format `-p` avec ranges) pour cibler rapidement les ports les plus fréquents |
| Common Ports Cheatsheet (PacketLife) | [PDF](https://web.archive.org/web/20240315102711/https://packetlife.net/media/library/23/common-ports.pdf) | Cheatsheet PDF des ports TCP/UDP les plus courants : table de référence rapide pour identifier les services lors d'un scan |

## 🛠️ Outils & Scripts

### 🔎 Reconnaissance réseau & web

| Ressource | Lien | Description |
|---|---|---|
| ffuf | [https://github.com/ffuf/ffuf](https://github.com/ffuf/ffuf) | Fuzzer web ultra-rapide écrit en Go : découverte de contenu/dossiers, de paramètres GET/POST, de vhosts (`-H "Host: FUZZ."`) et de valeurs, avec filtres de taille/mots/lignes (`-fs`, `-fw`, `-fl`), export JSON/HTML (`-of`), recursion, rate limiting et modes multi-wordlists — le compagnon de choix des wordlists SecLists |
| Gobuster | [https://github.com/OJ/gobuster](https://github.com/OJ/gobuster) | Outil de brute force écrit en Go avec plusieurs modes : `dir` (dossiers/fichiers, extensions via `-x`), `dns` (sous-domaines), `vhost` (virtual hosts) et `fuzz`, plus la découverte de buckets cloud (S3, GCS) — options utiles : `-t` pour les threads, `-b`/`-s` pour filtrer les codes de statut, cookies et headers custom (`-c`, `-H`) |
| THC-Hydra | [https://github.com/vanhauser-thc/thc-hydra](https://github.com/vanhauser-thc/thc-hydra) | Le bruteforceur de logins de référence (50+ protocoles : SSH, FTP, HTTP GET/POST, SMB, RDP, MySQL, LDAP, VNC, telnet, SNMP...). Syntaxe : `hydra -l admin -P rockyou.txt ssh://10.10.10.10 -t 4 -f -V`. Options clés : `-l`/`-L` (un login ou une liste), `-p`/`-P` (un mot de passe ou une wordlist), `-s` (port), `-t` (tâches parallèles, baisser à 4 sur SSH/RDP sinon Hydra se fait jeter), `-f` (stop au premier succès), `-e nsr` (teste aussi mot de passe vide, login = mot de passe et login inversé), `-V` (affiche chaque tentative), `-o` (fichier de sortie), `-M` (fichier de cibles) et `-x min:max:charset` (génération à la volée au lieu d'une wordlist). Modules HTTP avec `http-get-form` / `http-post-form` : `hydra -l admin -P pass.txt 10.10.10.10 http-post-form "/login.php:user=^USER^&pass=^PASS^:F=incorrect"` (`F` = texte d'échec, `S` = texte de succès). Un Ctrl-C laisse un `hydra.restore`, reprendre avec `-R` (ou l'ignorer avec `-I`). À garder pour un périmètre autorisé : le bruit est énorme et le compte se verrouille vite |
| CeWL (Custom Word List) | [https://github.com/digininja/CeWL](https://github.com/digininja/CeWL) | Générateur de wordlists ciblées (Ruby, par Robin Wood / digininja) : il crawle un site jusqu'à la profondeur demandée et récupère les mots réellement présents dans les pages — parfait pour un `hydra`, un `ffuf`/`wpscan -P` ou un `john` quand rockyou est hors sujet. Exemple : `cewl https://cible.com -d 3 -m 5 -w mots.txt --lowercase`. Options : `-d` (profondeur du crawl, 2 par défaut), `-m`/`-x` (longueur min/max des mots, 3 min par défaut), `-w` (fichier de sortie), `-c` (nombre d'occurrences par mot), `-e` (extraire aussi les adresses e-mail), `-a` (métadonnées : auteur, etc.), `-o` (suivre aussi les liens hors du site), `-p` (proxy) et `-u` (User-Agent). Déjà préinstallé sur Kali, sinon `gem install cewl`. Le même dépôt fournit aussi les scripts de fingerprinting `CeWL`/`FAB` et un mode « metadata » pratique pour récupérer des noms d'utilisateurs avant de bruteforcer |
| WPScan | [https://github.com/wpscanteam/wpscan/](https://github.com/wpscanteam/wpscan/) | Scanner de vulnérabilités WordPress (Ruby) : détection de version, thèmes et plugins installés avec leurs CVE (alimentées par la base WPScan), énumération des utilisateurs (`-e u`), des plugins vulnérables (`-e vp`, `-e ap`), bruteforce de mots de passe (`-P`) et de XML-RPC, détection de `wp-config` backups et de fichiers sensibles — `wpscan --url https://cible --enumerate vp,u --api-token XXX` |
| EyeWitness (RedSiege) | [https://github.com/RedSiege/EyeWitness](https://github.com/RedSiege/EyeWitness) | Captures d'écran en masse de dizaines/centaines de services web (liste d'URLs `-f`, XML Nmap `-x`, Nessus, ou cible unique `--single`), avec les headers serveur et une détection de credentials par défaut — puis un `report.html` cherchable et catégorisé, à ouvrir juste après un `nmap` ou un `ffuf` qui a révélé beaucoup de ports web. Installation : `sudo ./setup/setup.sh`, `source eyewitness-venv/bin/activate`, puis `python Python/EyeWitness.py -x nmap.xml -d sessions/` (`--threads`, `--timeout`, `--proxy-ip`, `--resume`) |
| onesixtyone | [https://github.com/trailofbits/onesixtyone](https://github.com/trailofbits/onesixtyone) | Scanner SNMP rapide (Trail of Bits) : bruteforce des community strings à partir d'une wordlist, lancement multi-threadé et découverte des agents SNMP sur un réseau — `onesixtyone -c dict.txt -i hosts.txt -o results.txt` |
| Nmap — script `http-enum` | [https://nmap.org/nsedoc/scripts/http-enum.html](https://nmap.org/nsedoc/scripts/http-enum.html) | Script NSE qui énumère les répertoires et fichiers des applications web courantes (Citrix, OWA, phpMyAdmin, WordPress, panneaux d'admin...) à partir d'une base de fingerprints façon Nikto, avec détection de versions. Lancement classique : `nmap -sV --script=http-enum <cible>`. Options : `http-enum.displayall` (afficher tous les codes, pas seulement 200/401 — plus de trouvailles, mais beaucoup plus de faux positifs), `http-enum.basepath`, `http-enum.category` (`attacks`, `database`, `general`, `microsoft`, `printer`...), `http-fingerprints.nikto-db-path` (charger la base Nikto à chaud) et `http-enum.fingerprintfile`. À savoir : le script teste deux URL aléatoires pour écarter les serveurs qui renvoient 200 partout, et abandonne si la racine répond 301 ou 401 |

### 🐧 Élévation de privilèges — Linux

| Ressource | Lien | Description |
|---|---|---|
| LinPEAS (PEASS-ng) | [https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS](https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS) | Script d'énumération pour l'élévation de privilèges sur Linux/Unix/macOS : recherche de SUID, capabilities, cron, credentials, kernel exploits... Version allégée (`linpeas_small.sh`) et build custom possibles — le passage obligé sur les machines HTB/THM. Le dépôt parent [peass-ng/PEASS-ng](https://github.com/peass-ng/PEASS-ng) regroupe linPEAS + winPEAS, avec les binaires prêts à l'emploi dans les releases |
| linux-exploit-suggester (LES) | [https://github.com/The-Z-Labs/linux-exploit-suggester](https://github.com/The-Z-Labs/linux-exploit-suggester) | Outil d'audit pour l'élévation de privilèges Linux : croise le kernel et les protections (ASLR, SMEP/SMAP...) avec une base de CVE/exploits publics pour suggérer les pistes exploitables |
| linuxprivchecker | [https://github.com/sleventyeleven/linuxprivchecker](https://github.com/sleventyeleven/linuxprivchecker) | Script Python d'énumération locale (Mike Czumak, maintenu par Sleventyeleven) : infos système, fichiers world-writable, mauvaises configurations, mots de passe en clair et exploits applicables. Pensé pour pointer les pistes à creuser, pas pour exploiter |
| linux-smart-enumeration (lse) | [https://github.com/diego-treitos/linux-smart-enumeration](https://github.com/diego-treitos/linux-smart-enumeration) | Script d'énumération Linux inspiré de LinEnum mais progressif : 3 niveaux de verbosité, tests POSIX/shellcheck, et monitoring de processus (`-p`) pour repérer les exécutions récurrentes. One-liner `lse.sh` |
| LinEnum | [https://github.com/rebootuser/LinEnum](https://github.com/rebootuser/LinEnum) | Le classique « Scripted Local Linux Enumeration & Privilege Escalation Checks » : kernel/distro, users, sudo, SUID, cron, réseau, fichiers intéressants — options `-t` (tests approfondis), `-k` (keyword), `-r`/`-e` (rapport) |

### 🪟 Élévation de privilèges — Windows

| Ressource | Lien | Description |
|---|---|---|
| WinPEAS (PEASS-ng) | [https://github.com/peass-ng/PEASS-ng/tree/master/winPEAS](https://github.com/peass-ng/PEASS-ng/tree/master/winPEAS) | Équivalent Windows de linPEAS : énumération des mauvaises configurations (services, permissions, credentials, tokens, Autologon...) pour l'élévation de privilèges. Dispo en .exe C#, .ps1 et .bat, exécutable depuis la mémoire |
| PrivescCheck | [https://github.com/itm4n/PrivescCheck](https://github.com/itm4n/PrivescCheck) | Script PowerShell d'énumération des vulnérabilités et mauvaises configurations Windows : `Invoke-PrivescCheck` avec modes -Extended, -Audit, -Risky et rapports TXT/HTML |
| Seatbelt (GhostPack) | [https://github.com/GhostPack/Seatbelt](https://github.com/GhostPack/Seatbelt) | Outil de « security-oriented host survey » en C# : collecte d'infos système (utilisateurs, groupes, sessions, AV/EDR, pare-feu, mises à jour, credentials stockés, fichiers récents, mauvaises configurations...) via 80+ checks groupés en catégories (`-group=all`, `-group=user`...). S'utilise aussi en post-exploitation |
| JAWS | [https://github.com/411Hall/JAWS](https://github.com/411Hall/JAWS) | « Just Another Windows (Enum) Script » : script PowerShell 2.0 (compatible Windows 7 → 11) qui passe en revue réseau, pare-feu, processus, fichiers/dossiers modifiables, chemins de service non quotés, `AlwaysInstallElevated`, credentials stockés, tâches planifiées... Sortie écran ou fichier (`-OutputFilename`) |
| WES-NG | [https://github.com/bitsadmin/wesng](https://github.com/bitsadmin/wesng) | Windows Exploit Suggester - Next Generation : à partir d'un `systeminfo` (ou des KB manquants), liste les vulnérabilités applicables à l'OS et les exploits publics correspondants — couvre Windows XP à Windows 11 et Server |

### 🕸️ C2 & red team

| Ressource | Lien | Description |
|---|---|---|
| Sliver (BishopFox) | [https://github.com/BishopFox/sliver](https://github.com/BishopFox/sliver) | Framework C2 open-source cross-platform : implants en mTLS, WireGuard, HTTP(S) et DNS, compilation dynamique avec clés uniques, payloads natifs/shellcode et exécution BOF/COFF sur Windows, Linux et macOS |
| Sliver GUI | [https://github.com/sliverarmory/sliver-gui](https://github.com/sliverarmory/sliver-gui) | Application desktop Electron (cross-platform) pour le C2 Sliver : sessions/beacons, fichiers, processus, génération d'implants et profils, listeners, loot et credentials — avec console Sliver et terminaux intégrés |
| Havoc | [https://github.com/HavocFramework/Havoc](https://github.com/HavocFramework/Havoc) | Framework C2 post-exploitation moderne et malléable : teamserver en Go, client Qt cross-platform, agent « Demon » (C/ASM) avec sleep obfuscation, indirect syscalls, spoofing d'adresses de retour et profiles C2 personnalisables |
| Empire (BC-Security) | [https://github.com/BC-SECURITY/Empire](https://github.com/BC-SECURITY/Empire) | Framework de post-exploitation et d'adversary emulation pour le red team : architecture serveur/client, listeners HTTP/S, SMB, pivoting, agents PowerShell/C#/Go/Python et 400+ modules (Mimikatz, Rubeus, Seatbelt, BOF...) |
| Starkiller | [https://github.com/BC-SECURITY/Starkiller](https://github.com/BC-SECURITY/Starkiller) | Frontend web (VueJS) pour PowerShell Empire : gestion des agents, listeners, modules et stagers depuis une interface. Depuis Empire 5.0, Starkiller est prépackagé et servi directement par l'API d'Empire |

### 👁️ Surveillance & analyse

| Ressource | Lien | Description |
|---|---|---|
| pspy | [https://github.com/DominicBreuker/pspy](https://github.com/DominicBreuker/pspy) | Monitoring de processus Linux **sans root** : voit les commandes des autres utilisateurs, les cron jobs et les scripts éphémères (scan procfs + inotify). Binaires statiques pspy32/64 et versions « small » ~1 MB |
| Process Monitor (Procmon) | [https://learn.microsoft.com/en-us/sysinternals/downloads/procmon](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon) | Sysinternals : monitoring temps réel Windows du filesystem, du registre et de l'activité process/thread/DLL, avec filtres puissants et stack traces — l'outil de référence pour le debug et la chasse au malware |

### 🌐 Outils en ligne

| Ressource | Lien | Description |
|---|---|---|
| revshells.com | [https://www.revshells.com/](https://www.revshells.com/) | Générateur de reverse/bind shells en ligne : IP/port + choix de l'OS et du langage (bash, nc, python, powershell, php...), listener prêt à l'emploi, encodage Base64/URI, mode MSFVenom et HoaxShell — idéal en CTF |
| UnPacker (JS) | [https://matthewfl.com/unPacker.html](https://matthewfl.com/unPacker.html) | Déobfuscateur JavaScript en ligne : colle du code packé (p.a.c.k.e.r de Dean Edwards, `eval(function(p,a,c,k,e,r)...)`) et récupère la version lisible — pratique en CTF web et pour analyser du JS suspect |

## 🗃️ Bases de vulnérabilités & Exploits

| Ressource | Lien | Description |
|---|---|---|
| Exploit-DB | [https://www.exploit-db.com/](https://www.exploit-db.com/) | La référence pour les PoC et exploits publics : base indexée par CVE, par produit/version, par type (web, local, remote, DoS) et par plateforme, avec le code source et les liens vers Metasploit — la première chose à fouiller quand un `searchsploit` remonte une piste |
| Rapid7 Vulnerability & Exploit Database | [https://www.rapid7.com/db/](https://www.rapid7.com/db/) | Base de Rapid7 (éditeur de Metasploit/Nexpose) : fiches CVE détaillées avec CVSS, produits affectés, références et surtout les modules Metasploit associés (`msfconsole` → `search`, `use exploit/...`) — pratique pour passer d'une CVE à un module prêt à l'emploi |
| Vulnerability-Lab | [https://www.vulnerability-lab.com/](https://www.vulnerability-lab.com/) | Archive indépendante de vulnérabilités et d'avis (web, IoT, mobile, logiciels) avec les détails techniques et les PoC, utile pour compléter la veille quand une CVE n'est pas encore publiée ou documentée ailleurs |

## 🎓 Formations & Tutoriels

| Ressource | Lien | Description |
|---|---|---|
| Grafikart | [https://grafikart.fr/formations](https://grafikart.fr/formations) | Formations complètes en programmation (PHP, Python, JS, etc.) |
| The CTF Primer | [https://primer.picoctf.org/#_assembly](https://primer.picoctf.org/#_assembly) | Guide d'introduction au CTF (picoCTF) : shell, assembleur, exploitation binaire, crypto... |
| CJCA : everything I wish someone told me (The Pensieve) | [https://www.thepensieve.in/Blogs/cjca](https://www.thepensieve.in/Blogs/cjca) | Retour d'expérience honnête sur la certif HTB CJCA (5 jours, 5 machines user+root, 80/100 min côté red, rapport éliminatoire) : prep, gestion du temps, SysReptor et partie blue team / Kibana |
| Red Team Leaders | [Accueil](https://courses.redteamleaders.com/) · [Catalogue](https://courses.redteamleaders.com/catalog) | Catalogue de formations, examens et labs en cybersécurité (offensif, défensif, GRC, cloud, AppSec, sécurité IA) proposés à prix réduit par une plateforme « AI-first » entièrement textuelle : plus de 100 cours dont plusieurs gratuits (AV/EDR Evasion, Foundations of Log Analysis, Introduction to Bug Bounty), des certifications (CASP, CAIPJ, CAISR...) et un abonnement aux labs hands-on |

## 🌐 Blogs & Veille

### 📝 Blogs & writeups

| Ressource | Lien | Description |
|---|---|---|
| 0xdf hacks stuff | [https://0xdf.gitlab.io/](https://0xdf.gitlab.io/) | Le blog de référence pour les writeups HTB, mis à jour très régulièrement : solutions détaillées pas à pas (AD, Windows, Linux, web), analyse de malware et home lab, souvent avec plusieurs chemins d'exploitation par machine. Une vraie mine pour l'AD — ESC1/ESC4/ESC13, RBCD, S4U, JEA, domain trusts, tunnels Chisel/SOCKS — chaque article expliquant pourquoi la technique marche et comment elle échoue |
| ropnop blog | [https://blog.ropnop.com/](https://blog.ropnop.com/) | Blog de référence de Ronnie Flathers (ropnop) : post-exploitation Windows, active directory, Kerberos, upgrade de shells en TTY — très orienté pentest / red team |
| jaxafed | [https://jaxafed.github.io/](https://jaxafed.github.io/) | Blog de writeups (TryHackMe, dont l'Advent of Cyber) où chaque room est décortiquée pas à pas, avec les scripts et les commandes utilisés — utile pour réviser une technique ou comparer sa démarche |
| devl00p’s infosec stuff | [https://devl00p.github.io/](https://devl00p.github.io/) | Blog de writeups CTF et exploitation binaire, source d’inspiration pour ce blog |
| H4ckYou Blog | [https://h4ckyou.github.io/](https://h4ckyou.github.io/) | Blog CTF & cybersécurité offensive |
| ka3n1x | [https://ka3n1x.io/](https://ka3n1x.io/) | Blog de recherche en sécurité offensive (« Fear Of Being Average ! ») : analyses de CVE et recherches web détaillées (SPIP, regex, SQLi...), entre veille et writeups |
| FoundHack | [https://foundhack.github.io/](https://foundhack.github.io/) | Blog CTF & hacking |
| Kur0sh1r0’s Portfolio | [https://kur0sh1r0.tech/](https://kur0sh1r0.tech/) | Portfolio de Fredmark Ivan "Kur0sh1ro" Dizon : security researcher, CTF player et bug bounty hunter, certifié HTB CPTS et membre d’A1SBERG — writeups CTF, projets offensive security et blog |
| calif.io - Java4Shell (writeup) | [https://calif.io/java4shell](https://calif.io/java4shell) | Writeup de recherche de Quang Luong sur Java4Shell (CVE-2026-114938) : corruption mémoire dans l'intrinsic Base64 x86-64 d'OpenJDK HotSpot, heap feng shui à distance pour transformer l'écriture hors bornes en fuite de heap puis en RCE — exploitation JVM de bout en bout |
| Writeup - Web Showcase | [https://web-showcase-inky.vercel.app/](https://web-showcase-inky.vercel.app/) | Writeup d'un aîné, ressource précieuse à conserver |

### 🎥 Chaînes YouTube

| Ressource | Lien | Description |
|---|---|---|
| IppSec | [https://www.youtube.com/@IppSec](https://www.youtube.com/@IppSec) | Walkthroughs HTB d'une profondeur rare : chaque machine retirée est résolue de bout en bout, avec les impasses, les alternatives et le raisonnement derrière chaque commande. Le complément indispensable : [ippsec.rocks](https://ippsec.rocks/), qui cherche une commande, un outil ou un concept directement dans l'horodatage de ses vidéos |
| VBScrub | [https://www.youtube.com/@VBScrub](https://www.youtube.com/@VBScrub) | Vidéos HTB et techniques, avec un vrai focus sur l'exploitation d'Active Directory (Kerberos, ACL, délégations, attaques de domaine) — la chaîne à suivre quand on attaque un environnement AD |
| STÖK | [https://www.youtube.com/@STOKfredrik](https://www.youtube.com/@STOKfredrik) | Fredrik Nordberg Almroth (STÖK) : bug bounty et sécurité des applications web, méthodologie de chasse, recon et mindset du hunter — très orienté web et retour d'expérience terrain |
| LiveOverflow | [https://www.youtube.com/@LiveOverflow](https://www.youtube.com/@LiveOverflow) | Chaîne technique très variée : exploitation binaire et heap, reverse engineering, CTF, web, et les formats « how to get into hacking » — excellent pour comprendre *pourquoi* une technique fonctionne, pas juste comment l'exécuter |

### 🛡️ Threat intelligence & recherche

| Ressource | Lien | Description |
|---|---|---|
| The DFIR Report | [https://thedfirreport.com/](https://thedfirreport.com/) | Rapports d'intrusions réelles documentées de bout en bout (accès initial, mouvement latéral, ransomware) avec les artefacts, les commandes et les règles de détection — la référence pour comprendre une attaque réelle côté blue team |
| Cisco Talos | [https://blog.talosintelligence.com/](https://blog.talosintelligence.com/) | Blog de l'équipe threat research de Cisco : avis sur les vulnérabilités critiques, analyses de malwares et de stealers, campagnes APT et infrastructures C2 (blockchain, dead drops...) |
| Unit 42 (Palo Alto Networks) | [https://unit42.paloaltonetworks.com/](https://unit42.paloaltonetworks.com/) | Recherche et threat intelligence de Palo Alto Networks : groupes APT, malwares, ransomware et rapports d'incident détaillés, avec un focus croissant sur les risques liés à l'IA |
| Securelist (Kaspersky) | [https://securelist.com/](https://securelist.com/) | Threat intelligence de Kaspersky : analyses de campagnes et de familles de malwares, rapports APT, statistiques et Kaspersky Security Bulletin |
| Check Point Research | [https://research.checkpoint.com/](https://research.checkpoint.com/) | Recherche de Check Point : campagnes cybercriminelles, ransomware, exploitation de vulnérabilités, recherche IA, plus une encyclopédie publique des techniques d'évasion (anti-debug...) |
| Google Project Zero | [https://projectzero.google/](https://projectzero.google/) | Recherche 0-day de l'équipe Project Zero de Google : exploitation mémoire, fuites d'ASLR, contournement de mitigations et bugs OS/navigateurs — technique et très détaillé |
| PortSwigger Research | [https://portswigger.net/research](https://portswigger.net/research) | Recherche web de l'équipe PortSwigger (James Kettle, Gareth Heyes) : desync, XSS, CSP, SAML, smuggling... à l'origine de nombreuses techniques et du Top 10 des vulnérabilités web |
| Trail of Bits Blog | [https://blog.trailofbits.com/](https://blog.trailofbits.com/) | Blog de la firme d'audit Trail of Bits : sécurité des compilateurs, crypto, fuzzing, analyse statique et recherches sur les protocoles (SAML, OIDC...) |
| Binary Ninja Blog | [https://binary.ninja/blog/](https://binary.ninja/blog/) | Blog de l'équipe Vector 35 (éditeur de Binary Ninja) : techniques de reversing, anti-reverse et obfuscation, analyse de malwares (Cobalt Strike, Flare-On), écriture de plugins et d'architectures, annonces de releases |
| ØSecurity (nullsec.us) | [https://nullsec.us/](https://nullsec.us/) | Blog de forensics numérique, réponse à incident et cybersécurité, avec des références techniques très détaillées (dont les listes de ports Nmap par défaut) |

### 📰 Actualité

| Ressource | Lien | Description |
|---|---|---|
| ZATAZ | [https://www.zataz.com/](https://www.zataz.com/) | Veille cybersécurité francophone depuis 1989 (Damien Bancal) : actualité de la cybercriminalité, fuites de données et alertes, orientée news |
| UnderNews | [https://www.undernews.fr/](https://www.undernews.fr/) | Actualité francophone de la sécurité informatique et du cybercrime : alertes, malwares, phishing, techniques de pirates et veille quotidienne |
| Stéphane Robert | [https://blog.stephane-robert.info/](https://blog.stephane-robert.info/) | Blog technique sur l'infrastructure, le cloud et la sécurité |

## 🤝 Communautés, événements & divers

| Ressource | Lien | Description |
|---|---|---|
| Meetup | [https://www.meetup.com/home/](https://www.meetup.com/home/) | Trouver des meetups et événements tech dans sa région |
| Freebuff - Buffy | [https://freebuff.com](https://freebuff.com) | Assistant IA pour coder avec l'aide d'une IA généreuse |
| Notes personnelles | [Google Docs](https://docs.google.com/document/d/1sAR8k_5TjMAmf-2dx3XhnY2zeDsvvAyxplw8o4RMXw4/edit?tab=t.0) | Mes notes de travail et ressources compilées |

---

*D'autres ressources seront ajoutées prochainement.*
