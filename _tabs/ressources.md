---
title: ressources
icon: fas fa-bookmark
order: 5
---

> Une collection de ressources soigneusement sélectionnées dans l'univers de la cybersécurité offensive, du CTF et du reverse engineering. Cette page évolue au fil de mes découvertes.
{: .prompt-info }

---

## 🔬 Reverse Engineering & Malware

| Ressource | Lien | Description |
|---|---|---|
| Reverse.zip | [https://reverse.zip/](https://reverse.zip/) | Plateforme complète de reverse engineering |
| Dogbolt | [https://dogbolt.org/](https://dogbolt.org/) | Compare plusieurs décompilateurs (Ghidra, IDA, Binary Ninja...) sur un même binaire |
| MalwareUnicorn Workshops | [https://malwareunicorn.org/#/workshops](https://malwareunicorn.org/#/workshops) | Ateliers de reverse engineering et d'analyse de malware par Amanda Rousseau (MalwareUnicorn), dont le célèbre « Reverse Engineering Malware 101 » |
| OpenSecurityTraining2 | [https://p.ost2.fyi/courses](https://p.ost2.fyi/courses) | Formations gratuites en sécurité : reverse engineering, exploitation binaire, architecture CPU... |

## 🏴 CTF & Wargames

| Ressource | Lien | Description |
|---|---|---|
| OverTheWire - Bandit | [https://overthewire.org/wargames/bandit/](https://overthewire.org/wargames/bandit/) | Wargame Linux pour apprendre la sécurité UNIX |
| OverTheWire - Leviathan | [https://overthewire.org/wargames/leviathan/](https://overthewire.org/wargames/leviathan/) | Wargame orienté reverse engineering et binaires setuid |
| 📌 Mon récap OverTheWire | [{% post_url 2026-08-03-overthewire-wargames-recapitulatif %}]({% post_url 2026-08-03-overthewire-wargames-recapitulatif %}) | Index de ma progression sur les wargames OverTheWire : Bandit & Leviathan complets, roadmap et compétences acquises |
| Writeup Leviathan (hrbrtschmu1l) | [https://hrbrtschmu1l.medium.com/leviathan-overthewire-wargame-writeup-dd3378a6136a](https://hrbrtschmu1l.medium.com/leviathan-overthewire-wargame-writeup-dd3378a6136a) | Writeup détaillé du wargame Leviathan (0→7) : SUID, ltrace, access() vs cat, bruteforce — source d'inspiration pour mes propres writeups |
| CTFtime | [https://ctftime.org/](https://ctftime.org/) | Calendrier mondial des CTF, classements d'équipes et archives de write-ups |
| Hack The Box | [https://www.hackthebox.com/](https://www.hackthebox.com/) | Plateforme de pentest avec machines et challenges variés |
| TryHackMe | [https://tryhackme.com/](https://tryhackme.com/) | Apprentissage guidé en cybersécurité, du débutant à l'avancé |
| picoCTF | [https://picoctf.org/](https://picoctf.org/) | CTF éducatif organisé par Carnegie Mellon University, idéal pour débuter |
| Root-Me | [https://www.root-me.org/](https://www.root-me.org/) | Plateforme francophone de challenges en sécurité offensive |

## 📖 Documentation & Cheatsheets

| Ressource | Lien | Description |
|---|---|---|
| HackTricks (FR) | [https://hacktricks.wiki/fr/index.html](https://hacktricks.wiki/fr/index.html) | La bible du pentest en français : base de connaissances couvrant reconnaissance, web, cloud, Active Directory, exploitation binaire, privilege escalation, red team... Des centaines de pages de techniques pratiques avec commandes prêtes à l'emploi, également disponible hors-ligne via le dépôt GitHub (branche `fr`) et Docker |
| PayloadsAllTheThings (Swissky) | [https://github.com/swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) | Le recueil de payloads et bypass de référence pour la sécurité web et le pentest/CTF : un chapitre par vulnérabilité (XSS, SQLi, SSRF, LFI/RFI, command injection, upload, SSTI, JWT...) avec description, techniques d'exploitation, fichiers prêts pour Burp Intruder et wordlists (ffuf) — versions web sur payloadsallthethings.com et projets frères InternalAllTheThings / HardwareAllTheThings |
| InternalAllTheThings - Reverse Shell | [https://swisskyrepo.github.io/InternalAllTheThings/cheatsheets/shell-reverse-cheatsheet/](https://swisskyrepo.github.io/InternalAllTheThings/cheatsheets/shell-reverse-cheatsheet/) | Cheatsheet exhaustif sur les reverse shells |
| SQL Injection Cheat Sheets (pentestmonkey) | [https://pentestmonkey.net/category/cheat-sheet/sql-injection](https://pentestmonkey.net/category/cheat-sheet/sql-injection) | Série complète de cheatsheets SQLi par moteur : MSSQL, MySQL, Oracle, PostgreSQL, DB2, Informix et Ingres — syntaxe pour version, current user, users/hashes, privileges, filesystem et command execution |
| MySQL SQL Injection Cheat Sheet (pentestmonkey) | [https://pentestmonkey.net/cheat-sheet/sql-injection/mysql-sql-injection-cheat-sheet](https://pentestmonkey.net/cheat-sheet/sql-injection/mysql-sql-injection-cheat-sheet) | Cheatsheet dédiée MySQL : `@@version`, `user()`, `mysql.user`, `information_schema`, lecture de fichiers via `LOAD_FILE()`/`INTO OUTFILE`, execution via UDF et techniques de bypass |
| Reverse Shell Cheat Sheet (pentestmonkey) | [https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet](https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet) | Le classique des one-liners de reverse shell : Bash, Perl, Python, PHP, Ruby, Netcat, Java, socat... à copier-coller dès qu'on a une exécution de commande. (Pour les Windows, remplacer `/bin/sh -i` par `cmd.exe`) |
| Upgrading Simple Shells to Fully Interactive TTYs (ropnop) | [https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/) | Passer d'un shell netcat « dumb » à un vrai TTY : module `pty` de Python, `script`, socat, stty + job control, et les raccourcis clavier pour survivre à un Ctrl-C |
| Spawn TTY Shell (PayloadsAllTheThings) | [https://swisskyrepo.github.io/InternalAllTheThings/cheatsheets/shell-reverse-cheatsheet/#spawn-tty-shell](https://swisskyrepo.github.io/InternalAllTheThings/cheatsheets/shell-reverse-cheatsheet/#spawn-tty-shell) | Section « Spawn TTY Shell » de Swissky : `rlwrap` au catch, `stty raw -echo; fg` (bash) ou `stty raw -echo ; fg` (zsh), `reset`, `export TERM=xterm-256color` et gestion des rows/columns |
| Tmux Cheat Sheet (tmuxcheatsheet.com) | [https://tmuxcheatsheet.com/](https://tmuxcheatsheet.com/) | Référence rapide tmux (dispo en français) : sessions, fenêtres, panes, copier/coller, raccourcis avec le préfixe `Ctrl-b`, plus un générateur de `~/.tmux.conf` et des guides ciblés — l'indispensable quand on fait tourner plusieurs shells dans un même terminal |
| Pwntools | [https://docs.pwntools.com/en/stable/](https://docs.pwntools.com/en/stable/) | Documentation officielle de la librairie Python pour l'exploitation binaire |
| smbclient - man page | [https://www.samba.org/samba/docs/current/man-html/smbclient.1.html](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html) | Documentation officielle de `smbclient` (Samba) : syntaxe, options d'authentification (`-U`, `-W`, `-N`, `-k`), mode interactif et commandes internes (`ls`, `get`, `put`, `recurse`, `mask`, `prompt`, `mget`...) pour énumérer et manipuler des partages SMB depuis un shell |
| Common Ports Cheatsheet (PacketLife) | [PDF (archive)](https://web.archive.org/web/20240315102711/https://packetlife.net/media/library/23/common-ports.pdf) | Cheatsheet PDF des ports TCP/UDP les plus courants : table de référence rapide pour identifier les services lors d'un scan |
| OWASP Top 10:2025 | [https://top10.owasp.org/2025/](https://top10.owasp.org/2025/) | Référentiel des 10 risques majeurs des applications web (édition 2025), avec CWE associés, statistiques et contre-mesures. A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures, A10 Mishandling of Exceptional Conditions |
| Liste des codes HTTP (Wikipédia) | [https://en.wikipedia.org/wiki/List_of_HTTP_status_codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) | Référence complète des codes de statut HTTP (1xx à 5xx, plus les codes non standard des serveurs comme nginx ou Cloudflare) avec leur signification : indispensable pour interpréter un scan, filtrer les faux positifs en fuzzing (`-fc`, `-fs`...) et comprendre les réponses d'une webapp |
| Notes personnelles | [https://docs.google.com/document/d/1sAR8k_5TjMAmf-2dx3XhnY2zeDsvvAyxplw8o4RMXw4/edit?tab=t.0](https://docs.google.com/document/d/1sAR8k_5TjMAmf-2dx3XhnY2zeDsvvAyxplw8o4RMXw4/edit?tab=t.0) | Mes notes de travail et ressources compilées |

## 🛠️ Outils & Scripts

| Ressource | Lien | Description |
|---|---|---|
| ffuf | [https://github.com/ffuf/ffuf](https://github.com/ffuf/ffuf) | Fuzzer web ultra-rapide écrit en Go : découverte de contenu/dossiers, de paramètres GET/POST, de vhosts (`-H "Host: FUZZ."`) et de valeurs, avec filtres de taille/mots/lignes (`-fs`, `-fw`, `-fl`), export JSON/HTML (`-of`), recursion, rate limiting et modes multi-wordlists — le compagnon de choix des wordlists SecLists |
| Gobuster | [https://github.com/OJ/gobuster](https://github.com/OJ/gobuster) | Outil de brute force écrit en Go avec plusieurs modes : `dir` (dossiers/fichiers, extensions via `-x`), `dns` (sous-domaines), `vhost` (virtual hosts) et `fuzz`, plus la découverte de buckets cloud (S3, GCS) — options utiles : `-t` pour les threads, `-b`/`-s` pour filtrer les codes de statut, cookies et headers custom (`-c`, `-H`) |
| LinPEAS (PEASS-ng) | [https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS](https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS) | Script d'énumération pour l'élévation de privilèges sur Linux/Unix/macOS : recherche de SUID, capabilities, cron, credentials, kernel exploits... Version allégée (`linpeas_small.sh`) et build custom possibles — le passage obligé sur les machines HTB/THM |
| WinPEAS (PEASS-ng) | [https://github.com/peass-ng/PEASS-ng/tree/master/winPEAS](https://github.com/peass-ng/PEASS-ng/tree/master/winPEAS) | Équivalent Windows de linPEAS : énumération des mauvaises configurations (services, permissions, credentials, tokens, Autologon...) pour l'élévation de privilèges. Dispo en .exe C#, .ps1 et .bat, exécutable depuis la mémoire |
| PrivescCheck | [https://github.com/itm4n/PrivescCheck](https://github.com/itm4n/PrivescCheck) | Script PowerShell d'énumération des vulnérabilités et mauvaises configurations Windows : `Invoke-PrivescCheck` avec modes -Extended, -Audit, -Risky et rapports TXT/HTML |
| WES-NG | [https://github.com/bitsadmin/wesng](https://github.com/bitsadmin/wesng) | Windows Exploit Suggester - Next Generation : à partir d'un `systeminfo` (ou des KB manquants), liste les vulnérabilités applicables à l'OS et les exploits publics correspondants — couvre Windows XP à Windows 11 et Server |
| linux-exploit-suggester (LES) | [https://github.com/The-Z-Labs/linux-exploit-suggester](https://github.com/The-Z-Labs/linux-exploit-suggester) | Outil d'audit pour l'élévation de privilèges Linux : croise le kernel et les protections (ASLR, SMEP/SMAP...) avec une base de CVE/exploits publics pour suggérer les pistes exploitables |
| linux-smart-enumeration (lse) | [https://github.com/diego-treitos/linux-smart-enumeration](https://github.com/diego-treitos/linux-smart-enumeration) | Script d'énumération Linux inspiré de LinEnum mais progressif : 3 niveaux de verbosité, tests POSIX/shellcheck, et monitoring de processus (`-p`) pour repérer les exécutions récurrentes. One-liner `lse.sh` |
| LinEnum | [https://github.com/rebootuser/LinEnum](https://github.com/rebootuser/LinEnum) | Le classique « Scripted Local Linux Enumeration & Privilege Escalation Checks » : kernel/distro, users, sudo, SUID, cron, réseau, fichiers intéressants — options `-t` (tests approfondis), `-k` (keyword), `-r`/`-e` (rapport) |
| Top 1 000 ports TCP & UDP (Nmap) | [https://nullsec.us/top-1-000-tcp-and-udp-ports-nmap-default/](https://nullsec.us/top-1-000-tcp-and-udp-ports-nmap-default/) | Référence des ports scannés par défaut par Nmap, avec les commandes `--top-ports 1000` et les listes prêtes à copier (format `-p` avec ranges) pour cibler rapidement les ports les plus fréquents |
| onesixtyone | [https://github.com/trailofbits/onesixtyone](https://github.com/trailofbits/onesixtyone) | Scanner SNMP rapide (Trail of Bits) : bruteforce des community strings à partir d'une wordlist, lancement multi-threadé et découverte des agents SNMP sur un réseau — `onesixtyone -c dict.txt -i hosts.txt -o results.txt` |
| Empire (BC-Security) | [https://github.com/BC-SECURITY/Empire](https://github.com/BC-SECURITY/Empire) | Framework de post-exploitation et d'adversary emulation pour le red team : architecture serveur/client, listeners HTTP/S, SMB, pivoting, agents PowerShell/C#/Go/Python et 400+ modules (Mimikatz, Rubeus, Seatbelt, BOF...) |
| Sliver (BishopFox) | [https://github.com/BishopFox/sliver](https://github.com/BishopFox/sliver) | Framework C2 open-source cross-platform : implants en mTLS, WireGuard, HTTP(S) et DNS, compilation dynamique avec clés uniques, payloads natifs/shellcode et exécution BOF/COFF sur Windows, Linux et macOS |
| Havoc | [https://github.com/HavocFramework/Havoc](https://github.com/HavocFramework/Havoc) | Framework C2 post-exploitation moderne et malléable : teamserver en Go, client Qt cross-platform, agent « Demon » (C/ASM) avec sleep obfuscation, indirect syscalls, spoofing d'adresses de retour et profiles C2 personnalisables |
| Starkiller | [https://github.com/BC-SECURITY/Starkiller](https://github.com/BC-SECURITY/Starkiller) | Frontend web (VueJS) pour PowerShell Empire : gestion des agents, listeners, modules et stagers depuis une interface. Depuis Empire 5.0, Starkiller est prépackagé et servi directement par l'API d'Empire |
| Sliver GUI | [https://github.com/sliverarmory/sliver-gui](https://github.com/sliverarmory/sliver-gui) | Application desktop Electron (cross-platform) pour le C2 Sliver : sessions/beacons, fichiers, processus, génération d'implants et profils, listeners, loot et credentials — avec console Sliver et terminaux intégrés |
| revshells.com | [https://www.revshells.com/](https://www.revshells.com/) | Générateur de reverse/bind shells en ligne : IP/port + choix de l'OS et du langage (bash, nc, python, powershell, php...), listener prêt à l'emploi, encodage Base64/URI, mode MSFVenom et HoaxShell — idéal en CTF |
| pspy | [https://github.com/DominicBreuker/pspy](https://github.com/DominicBreuker/pspy) | Monitoring de processus Linux **sans root** : voit les commandes des autres utilisateurs, les cron jobs et les scripts éphémères (scan procfs + inotify). Binaires statiques pspy32/64 et versions « small » ~1 MB |
| Process Monitor (Procmon) | [https://learn.microsoft.com/en-us/sysinternals/downloads/procmon](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon) | Sysinternals : monitoring temps réel Windows du filesystem, du registre et de l'activité process/thread/DLL, avec filtres puissants et stack traces — l'outil de référence pour le debug et la chasse au malware |
| UnPacker (JS) | [https://matthewfl.com/unPacker.html](https://matthewfl.com/unPacker.html) | Déobfuscateur JavaScript en ligne : colle du code packé (p.a.c.k.e.r de Dean Edwards, `eval(function(p,a,c,k,e,r)...)`) et récupère la version lisible — pratique en CTF web et pour analyser du JS suspect |

## 🎓 Formations & Tutoriels

| Ressource | Lien | Description |
|---|---|---|
| Grafikart | [https://grafikart.fr/formations](https://grafikart.fr/formations) | Formations complètes en programmation (PHP, Python, JS, etc.) |
| The CTF Primer | [https://primer.picoctf.org/#_assembly](https://primer.picoctf.org/#_assembly) | Guide d'introduction au CTF (picoCTF) : shell, assembleur, exploitation binaire, crypto... |
| CJCA : everything I wish someone told me (The Pensieve) | [https://www.thepensieve.in/Blogs/cjca](https://www.thepensieve.in/Blogs/cjca) | Retour d'expérience honnête sur la certif HTB CJCA (5 jours, 5 machines user+root, 80/100 min côté red, rapport éliminatoire) : prep, gestion du temps, SysReptor et partie blue team / Kibana |
| Red Team Leaders | [Accueil](https://courses.redteamleaders.com/) · [Catalogue](https://courses.redteamleaders.com/catalog) | Catalogue de formations, examens et labs en cybersécurité (offensif, défensif, GRC, cloud, AppSec, sécurité IA) proposés à prix réduit par une plateforme « AI-first » entièrement textuelle : plus de 100 cours dont plusieurs gratuits (AV/EDR Evasion, Foundations of Log Analysis, Introduction to Bug Bounty), des certifications (CASP, CAIPJ, CAISR...) et un abonnement aux labs hands-on |

## 🌐 Blogs & Veille

| Ressource | Lien | Description |
|---|---|---|
| ØSecurity (nullsec.us) | [https://nullsec.us/](https://nullsec.us/) | Blog de forensics numérique, réponse à incident et cybersécurité, avec des références techniques très détaillées (dont les listes de ports Nmap par défaut) |
| ropnop blog | [https://blog.ropnop.com/](https://blog.ropnop.com/) | Blog de référence de Ronnie Flathers (ropnop) : post-exploitation Windows, active directory, Kerberos, upgrade de shells en TTY — très orienté pentest / red team |
| 0xdf hacks stuff | [https://0xdf.gitlab.io/](https://0xdf.gitlab.io/) | Le blog de référence pour les writeups HTB : solutions détaillées pas à pas (AD, Windows, Linux, web), analyse de malware et home lab — souvent plusieurs chemins d'exploitation par machine |
| IppSec | [https://ippsec.rocks/](https://ippsec.rocks/) | Moteur de recherche dans les vidéos YouTube d'IppSec : tape une commande, un outil ou un concept et retrouve le timestamp exact dans ses walkthroughs HTB (chaîne : youtube.com/@ippsec) |
| H4ckYou Blog | [https://h4ckyou.github.io/](https://h4ckyou.github.io/) | Blog CTF & cybersécurité offensive |
| FoundHack | [https://foundhack.github.io/](https://foundhack.github.io/) | Blog CTF & hacking |
| Stéphane Robert | [https://blog.stephane-robert.info/](https://blog.stephane-robert.info/) | Blog technique sur l'infrastructure, le cloud et la sécurité |
| Writeup - Web Showcase | [https://web-showcase-inky.vercel.app/](https://web-showcase-inky.vercel.app/) | Writeup d'un aîné, ressource précieuse à conserver |
| devl00p's infosec stuff | [https://devl00p.github.io/](https://devl00p.github.io/) | Blog de writeups CTF et exploitation binaire, source d'inspiration pour ce blog |
| Kur0sh1r0's Portfolio | [https://kur0sh1r0.tech/](https://kur0sh1r0.tech/) | Portfolio de Fredmark Ivan "Kur0sh1ro" Dizon : security researcher, CTF player et bug bounty hunter, certifié HTB CPTS et membre d'A1SBERG — writeups CTF, projets offensive security et blog |

## 🤖 AI & Assistants

| Ressource | Lien | Description |
|---|---|---|
| Freebuff - Buffy | [https://freebuff.com](https://freebuff.com) | Assistant IA pour coder avec l'aide d'une IA généreuse |



## 🤝 Communautés & Événements

| Ressource | Lien | Description |
|---|---|---|
| Meetup | [https://www.meetup.com/home/](https://www.meetup.com/home/) | Trouver des meetups et événements tech dans sa région |

---

*D'autres ressources seront ajoutées prochainement.*
