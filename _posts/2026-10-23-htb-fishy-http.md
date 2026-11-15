---
title: "HTB – Fishy HTTP : décoder un canal C2 caché dans du HTML (Forensics / Malware)"
description: "Analyse d'un pcap et d'un exécutable suspect : décoder un canal C2 HTTP caché dans du HTML, puis rejouer le malware contre un faux serveur pour récupérer les deux moitiés du flag."
date: 2026-10-23 01:00:00 +0100
categories: [CTF, HackTheBox]
tags: [htb, forensics, malware, wireshark, tshark, wine, strace, c2, base64, writeup]
---

## Informations sur le challenge

| Élément | Détail |
|---|---|
| Plateforme | Hack The Box (Challenges) |
| Nom | Fishy HTTP |
| Catégorie | Forensics / Malware analysis |
| Difficulté | Débutant |
| Créateur | pakcyberbot |
| Fichier fourni | un `.zip` (~28 Mo) contenant `sustraffic.pcapng` et `smphost.exe` |

**Énoncé (traduit) :** « J'ai trouvé un programme suspect sur mon ordinateur qui fait des requêtes HTTP vers un serveur Web. Merci de consulter la capture de trafic et l'exécutable fournis pour analyse. (Note : le drapeau comporte deux parties) »

> Pense à vérifier que le challenge est bien **retiré** (retired) sur HTB avant de publier ce writeup avec le flag : la plateforme n'autorise pas la publication de solutions de challenges actifs.
{: .prompt-warning }

## Outils utilisés

- Kali Linux
- `tshark` / Wireshark (analyse du pcap)
- `strings`, `file` (premier regard sur l'exécutable)
- Python 3 (décodage, faux serveur)
- Wine (exécuter le `.exe` Windows sous Linux)
- `strace` (observer les processus créés)

> ⚠️ **Sécurité** : exécuter un malware, même sous Wine, n'est **pas** sans risque. Wine n'est pas une sandbox : le programme tourne avec tes droits et voit tout ton disque (le lecteur `Z:` correspond à `/`). Ici, les commandes qu'il exécute sont inoffensives (on le vérifiera), mais le bon réflexe est de le faire dans une **VM jetable**.
{: .prompt-danger }

## Étape 1 – Vue d'ensemble du trafic

On commence par lister les échanges HTTP du pcap :

```bash
tshark -r sustraffic.pcapng -Y http -T fields \
  -e frame.number -e ip.src -e ip.dst -e http.request.method -e http.request.uri
```

Résultat (extrait) :

```
4    10.142.0.4  10.142.0.3  GET   /
9    10.142.0.3  10.142.0.4        /
16   10.142.0.4  10.142.0.3  POST  /submit_feedback
19   10.142.0.3  10.142.0.4        /submit_feedback
26   10.142.0.4  10.142.0.3  GET   /
...
```

On comprend déjà la structure :

- `10.142.0.4` est la **machine infectée** (le client, qui exécute `smphost.exe`).
- `10.142.0.3` est le **serveur C2** de l'attaquant.
- Le schéma se répète **4 fois** : `GET /` → réponse HTML → `POST /submit_feedback` → réponse.

Rappel HTTP : le client envoie les requêtes, le serveur ne fait que répondre. Ici, c'est donc le **malware** qui fait le `GET` (« as-tu une commande pour moi ? ») et le `POST` (« voici le résultat »).

| Message | Émetteur | Contenu |
|---|---|---|
| `GET /` | malware | demande une commande |
| Réponse au GET | serveur C2 | la commande, cachée dans une page HTML |
| `POST /submit_feedback` | malware | le résultat de la commande, caché dans des mots |
| Réponse au POST | serveur C2 | simple accusé de réception |

## Étape 2 – Les pages HTML et les POST

### Les réponses du serveur (les « commandes »)

Une première extraction avec `tshark -Y http.response -T fields -e text` montre des pages HTML qui ne servent visiblement à rien : des dizaines de balises (`<button>`, `<ol><li>`, `<img src=…>`, `<p>`, `<cite>`…) remplies de **mots anglais aléatoires** (`leaf tree glasses uniform guitar…`).

### Les POST du malware

Dans le corps des `POST`, on trouve :

```
Name=Test+User&feedback=duck+2+lock+unicorn+Zebra+Ghost+9+3+car+yak+1+...
```

Ce `feedback` est lui aussi une suite de mots, mais avec des **chiffres** et des **majuscules** mélangés, et il se termine par `=`. Ce signe `=` à la fin est un réflexe à retenir : c'est le *padding* typique du **base64**.

> Attention : `tshark -e text` **tronque** les longues lignes (on voit des `[…]` et des mots coupés comme `Compu`). Pour avoir le contenu complet, il faut utiliser `-e http.file_data` (en hexadécimal) ou `--export-objects http,dossier`.
{: .prompt-tip }

## Étape 3 – Décoder les POST

L'hypothèse : **la première lettre de chaque mot** (en gardant la casse) forme une chaîne base64. Sur la première ligne :

```
duck 2 lock unicorn Zebra Ghost 9 3 car yak 1 ...
 d    2   l     u      Z     G    9 3  c   y   1 ...  →  d2luZG93cy1...
```

`d2luZG93cy1...` est du base64 qui décode en `windows-instanc...`. L'hypothèse est bonne.

Script de décodage complet (lit tous les POST du pcap) :

```python
import subprocess, base64
from urllib.parse import parse_qs

out = subprocess.run(
    ["tshark", "-r", "sustraffic.pcapng", "-Y", "http.request.method==POST",
     "-T", "fields", "-e", "http.file_data"],
    capture_output=True, text=True).stdout

for line in out.split():
    data = bytes.fromhex(line).decode()
    fb = parse_qs(data)["feedback"][0]        # le '+' devient un espace
    s = ''.join(w[0] for w in fb.split())     # première lettre de chaque mot
    s = s.rstrip('=')
    s += '=' * (-len(s) % 4)                  # remet le padding base64
    print(base64.b64decode(s).decode(errors="replace"))
    print("-" * 40)
```

### Résultat : 4 sorties de commandes

1. `windows-instanc\pakcyberbot` → sortie de **`whoami`**.
2. Un long bloc `Host Name: WINDOWS-INSTANC / OS Name: Microsoft Windows Server 2016 Datacenter / …` → sortie de **`systeminfo`** (machine hébergée sur Google Compute Engine, IP `10.142.0.4`). C'est de la reconnaissance, rien pour le flag.
3. Un `dir C:\Temp` qui montre `smphost.exe` (67 515 744 octets), **suivi d'une ligne bizarre** :

   ```
   'h77P_s73417hy_revSHELL}'
   ```

4. Un second `dir C:\Temp`, identique.

La ligne du point 3 se termine par `}` : c'est très probablement la **fin du flag**, donc la **partie 2**. En leetspeak, ça se lit *« http stealthy revshell »*. (Les apostrophes autour font penser à un message d'erreur de `cmd.exe` à propos d'un fichier introuvable : on y revient plus bas.)

On a donc la fin du flag, mais pas le début. Il est probablement caché du côté **commandes reçues** (les pages HTML) ou dans l'exécutable.

## Étape 4 – Premier regard sur `smphost.exe`

```bash
file smphost.exe
strings -a smphost.exe | less
```

> Erreur à éviter : `head -n 3 smphost.exe | strings` ne lit que le tout début du binaire et n'apprend rien d'utile.
{: .prompt-tip }

Observations :

- Le nom `smphost.exe` imite un composant Windows légitime (usurpation de nom).
- On voit des noms de sections comme `.CLR_UEF`, qui évoquent le **runtime .NET (CLR)**. Cela s'est révélé cohérent avec la lecture du flag (« dot net »), mais je ne l'ai pas confirmé par un désassemblage.
- Le fichier est énorme (≈ 67 Mo) pour un si petit malware, ce qui suggère qu'il embarque son propre runtime.

Exécuté sans argument sous Wine, il affiche son usage :

```
Usage: program.exe <IPAddress> <Port>
```

Point clé : **l'adresse du serveur n'est pas codée en dur**. On peut donc le faire parler à notre propre serveur local.

## Étape 5 – Rejouer le malware contre un faux serveur C2

Idée classique en analyse dynamique : jouer le rôle de l'attaquant.

1. On extrait les 4 pages de commandes (réponses aux `GET`, trames 9, 31, 60 et 84) :

   ```bash
   for n in 9 31 60 84; do
     tshark -r sustraffic.pcapng -Y "frame.number==$n" -T fields -e http.file_data \
       | xxd -r -p > page_$n.html
   done
   ```

2. On écrit un petit serveur HTTP (`fake_c2.py`) qui sert une de ces pages à chaque `GET /` et qui **décode le POST** qu'il reçoit :

   ```python
   import sys, base64
   from http.server import BaseHTTPRequestHandler, HTTPServer
   from urllib.parse import parse_qs

   page = open(sys.argv[1], "rb").read()

   class H(BaseHTTPRequestHandler):
       def do_GET(self):
           self.send_response(200)
           self.send_header("Content-Length", str(len(page)))
           self.end_headers()
           self.wfile.write(page)

       def do_POST(self):
           n = int(self.headers.get("Content-Length", 0))
           body = self.rfile.read(n).decode()
           fb = parse_qs(body).get("feedback", [""])[0]
           s = "".join(w[0] for w in fb.split()).rstrip("=")
           s += "=" * (-len(s) % 4)
           print("RÉSULTAT :", base64.b64decode(s).decode(errors="replace"))
           self.send_response(200)
           self.send_header("Content-Length", "0")
           self.end_headers()

   HTTPServer(("127.0.0.1", 8080), H).serve_forever()
   ```

3. Dans un terminal : `python3 fake_c2.py page_9.html` ; dans un autre : `wine smphost.exe 127.0.0.1 8080`.

Résultat, page par page :

| Page | Taille | Commande exécutée |
|---|---|---|
| `page_9.html` | 871 o | `whoami` (affiche `KALI\emma_aura`, ma propre machine) |
| `page_31.html` | 1277 o | `systeminfo` |
| `page_60.html` | 7338 o | `dir` |
| `page_84.html` | 6734 o | `dir` |

Le malware **boucle en permanence** (il redemande une commande sans pause), d'où le flot de résultats identiques. On l'arrête avec `Ctrl+C`, puis `pkill -f smphost.exe` ou `wineserver -k` si besoin.

Ça confirme le fonctionnement : **les pages HTML n'exécutent rien elles-mêmes**. C'est le malware qui lit les mots, les décode en une commande, la passe à `cmd.exe`, puis renvoie le résultat encodé en mots dans le `POST`. Mais j'ai remarqué un détail troublant : sur la machine d'origine, la 3ᵉ commande renvoyait aussi `'h77P_s73417hy_revSHELL}'`, alors que chez moi, la page 60 ne produisait qu'un `dir`. La page cache donc **plus qu'un `dir`**.

> Je n'ai pas cherché à reverse-engineer l'algorithme de décodage des pages HTML. On a contourné le problème : au lieu de comprendre comment le malware lit la page, on l'a laissé la lire pour nous et on a observé ce qu'il exécute.
{: .prompt-info }

## Étape 6 – Voir la vraie commande avec `strace`

Pour voir la commande exacte lancée à partir de la page 60 (le serveur tourne dans un autre terminal avec `python3 fake_c2.py page_60.html`) :

```bash
strace -f -s 2000 -e trace=execve -o trace.txt wine smphost.exe 127.0.0.1 8080
grep -i -E "cmd|/c" trace.txt | head -20
```

Sortie :

```
execve("/usr/lib/wine/wine64", ["/usr/lib/wine/wine64", "cmd.exe", "/c", "dir", "&&",
  "cd", "\\Users\\pakcyberbot\\Documents\\", "&&", "type", "HTB{Th4ts_d07n37_"], ...)
```

La commande complète est donc :

```
cmd.exe /c dir && cd \Users\pakcyberbot\Documents\ && type HTB{Th4ts_d07n37_ ...
```

Elle fait trois choses : liste le dossier courant, change de répertoire vers `\Users\pakcyberbot\Documents\`, puis exécute `type` (qui affiche le contenu d'un fichier) avec, comme « nom de fichier », **le début du flag**. L'attaquant a donc caché la partie 1 dans l'argument de `type`.

Pourquoi ne la voit-on jamais dans le résultat sous Wine ? Mon explication (probable, non prouvée) : sous Wine, le `cd \Users\pakcyberbot\Documents\` échoue puisque ce dossier n'existe pas sur ma machine, et comme les commandes sont chaînées avec `&&`, `type` n'est **jamais exécuté**. Sur la machine Windows d'origine, le `cd` réussit, `type` s'exécute sur des fichiers qui n'existent pas, et `cmd.exe` renvoie une erreur qui contient le nom fautif : c'est ce que le malware a envoyé dans le `POST` (la chaîne entre apostrophes `'h77P_s73417hy_revSHELL}'`).

L'argument de `type` contient un espace entre les deux morceaux, ce qui explique qu'on retrouve la fin du flag dans le `POST` et le début dans la ligne de commande. Remarque : la trace `strace` montre seulement `HTB{Th4ts_d07n37_` comme dernier argument ; la suite de l'argument provient du `POST` décodé à l'étape 3.

## Flag

| Partie | Source | Valeur |
|---|---|---|
| 1 | commande `cmd.exe` observée avec `strace` | `HTB{Th4ts_d07n37_` |
| 2 | `POST` décodé dans le pcap | `h77P_s73417hy_revSHELL}` |

```
HTB{Th4ts_d07n37_h77P_s73417hy_revSHELL}
```

Lecture en leetspeak : *« That's dot net HTTP stealthy revshell »*.

## Ce que j'ai appris

1. **Reconnaître un canal C2** : un schéma `GET` (récupérer une commande) puis `POST` (renvoyer le résultat) répété en boucle, le tout caché dans du trafic HTTP banal.
2. **Reconnaître le base64** : un `=` en fin de chaîne est un indice fort. Ici, l'encodage « première lettre de chaque mot » est une forme de stéganographie par mots, puis du base64.
3. **Attention aux outils qui tronquent** : `tshark -e text` coupe les longues lignes. Pour des données complètes, passer par `http.file_data` ou `--export-objects`.
4. **Analyse dynamique avant le reverse** : quand l'exécutable accepte l'IP du serveur en argument, un faux serveur local permet de l'observer sans le désassembler. C'est souvent plus rapide que de lire le code.
5. **`strace -e trace=execve`** montre la ligne de commande réelle des processus lancés, très utile pour voir ce qu'un malware exécute.
6. **Prudence** : Wine n'isole rien. Toujours analyser un malware dans une VM jetable, et ne lui servir que des commandes dont on a vérifié l'effet.

## Pistes pour aller plus loin

- Décompiler `smphost.exe` (par exemple avec Detect It Easy puis un décompilateur .NET si c'est bien du .NET) pour retrouver l'algorithme qui transforme les mots des pages HTML en commande.
- Écrire un script qui décode directement les pages `GET`, sans exécuter le malware.
- Écrire des règles de détection (réseau) pour ce type de C2 : même requête `GET /` répétée, `POST /submit_feedback` avec un champ `feedback` fait de mots.
