---
title: "Shared Secrets — picoCTF : quand le secret Diffie-Hellman fuite en clair"
description: "Writeup du challenge Shared Secrets (picoCTF, Cryptographie, Facile) : analyse d'un échange de clé Diffie-Hellman, exploitation d'une fuite du secret privé côté client, recalcul de la clé partagée avec pow() et déchiffrement XOR en Python."
date: 2026-08-12 02:40:00 +0100
categories: [CTF, picoCTF]
tags: [crypto, diffie-hellman, xor, python]
image:
  path: /assets/img/posts/SharedSecrets.png
  alt: Challenge Shared Secrets sur picoCTF
---

> Après **StegoRSA**, on reste en cryptographie avec **Shared Secrets**, un challenge basé sur l'échange de clé **Diffie-Hellman**. L'énoncé donne un indice limpide : *"it looks like one side of the exchange leaked something"* — une des deux parties a été négligente. Pas besoin de casser de maths compliquées ici : il suffit de savoir **lire le code source** fourni pour repérer où se cache la fuite, et rejouer le même calcul que le serveur.

## 🎯 En bref

| Infos | Détails |
| ----- | ------- |
| **Catégorie** | Cryptographie |
| **Difficulté** | 🟢 Facile |
| **Plateforme** | picoCTF 2026 |
| **Auteur du challenge** | Yahaya Meddy |
| **Outils utilisés** | Python 3 (`pow()`, `bytes.fromhex()`, XOR) |
| **Fichiers fournis** | `message.txt`, `encryption.py` |

## 📜 Énoncé

> A message was encrypted using a shared secret... but it looks like one side of the exchange leaked something. Can you piece together the secret and get the flag?
>
> **Hint :** What do you get if you combine a public key with a known private one?

On récupère deux fichiers : le **code source** utilisé pour générer le challenge (`encryption.py`), et le **résultat** de son exécution (`message.txt`), qui contient les valeurs numériques et le message chiffré.

## 🔍 Découvertes

### Étape 1 — Comprendre l'échange Diffie-Hellman

Le code source fourni simule un échange **Diffie-Hellman**, un protocole qui permet à deux parties de se mettre d'accord sur un secret commun sans jamais l'envoyer directement sur le réseau :

```python
from Crypto.Util.number import getPrime
from random import randint

# Public parameters
g = 2
p = getPrime(1048)

# Server's secret
a = randint(2, p-2)
A = pow(g, a, p)

# Client secret
b = '???'  

B = pow(g, b, p)

# Shared key
shared = pow(A, b, p)

# Encrypt flag
flag = b"picoCTF{...}"
enc = bytes([x ^ (shared % 256) for x in flag])

# Write challenge info
with open("file.txt", "w") as f:
    f.write(f"g = {g}\n")
    f.write(f"p = {p}\n")
    f.write(f"A = {A}\n")
    f.write(f"b = {b} \n")
    f.write(f"enc = {enc.hex()}\n")
```

Principe résumé :
- Le **serveur** choisit un secret `a`, et publie seulement `A = g^a mod p`
- Le **client** choisit un secret `b`, et publie seulement `B = g^b mod p`
- Les deux parties peuvent alors calculer le **même** secret partagé (`shared = A^b mod p` côté client, ou `B^a mod p` côté serveur), sans jamais avoir communiqué `a` ni `b` directement

En théorie, un attaquant qui intercepte uniquement `g`, `p`, `A` et `B` ne peut pas retrouver `shared` facilement (c'est le fameux problème du logarithme discret).

### Étape 2 — Repérer la fuite

En comparant ce que le script est censé garder secret et ce qu'il écrit réellement dans le fichier de sortie :

```python
f.write(f"g = {g}\n")
f.write(f"p = {p}\n")
f.write(f"A = {A}\n")
f.write(f"b = {b} \n")     # ⚠️ le secret du CLIENT est écrit en clair !
f.write(f"enc = {enc.hex()}\n")
```

Le secret `a` du serveur n'apparaît nulle part — logique, il doit rester privé. **Mais le secret `b` du client, lui, est écrit en toutes lettres.** C'est exactement la négligence annoncée dans l'énoncé ("*one side of the exchange leaked something*"). Avec `A`, `b` et `p` en main, plus besoin de casser quoi que ce soit : il suffit de rejouer la même formule que le serveur utilise pour calculer `shared`.

Voici les valeurs récupérées dans `message.txt` :

```
g = 2
p = 2132004026303109138960419370582104845382939159231816273620696701294630284403386465532863373769144582236949856392667504369986764250039517010152815931140874682590496582913679422125500008296870534246366594745735993256988714723377030293374496770744770410547817411606458596058022709758993968788819254528632650187419776389
A = 1141933368749651547285106584770022946598556294532255484018234071279017284493261458304303078441814350280055235938839850330392924394827971935746684756724106154783529866206686364342391780819577389806835022154187096665229978275413748714049243740736779489018438278478708068573511338451873371736513057724525994219285563327
b = 738623211561746372624170944030870485944978187433844583412325760777341380867104112487743286812112394661187612902430214202202766378016375904891604068375412515990443266634874912487423407082997026224391496763715710675145163967715339675283689424507137408425143581496186446869723885557865390662886201409684909929549168034
enc = 928b818da1b6a499868abd91d18190d196bdd1d08781d0d4d5db9f
```

### Étape 3 — Recalculer le secret partagé

En Python, `pow(base, exposant, modulo)` calcule une puissance modulaire en une seule fonction optimisée (indispensable ici : `A ** b` seul donnerait un nombre à des milliers de chiffres, impossible à manipuler efficacement). On applique donc exactement la ligne du serveur `shared = pow(A, b, p)`, mais nous-mêmes, côté attaquant :

```python
shared = pow(A, b, p)
```

### Étape 4 — Déchiffrer avec le même XOR

Le chiffrement du flag se fait avec un XOR répété, un octet de clé (`shared % 256`) appliqué à chaque octet du flag :

```python
enc = bytes([x ^ (shared % 256) for x in flag])
```

Le XOR ayant la propriété d'être **réversible avec la même clé**, il suffit d'appliquer exactement la même opération, mais sur `enc` (converti depuis l'hexadécimal) au lieu de `flag` :

```python
enc_bytes = bytes.fromhex(enc_hex)
flag_bytes = bytes([x ^ (shared % 256) for x in enc_bytes])
```

## 🛠️ Script de résolution

```python
# --- Valeurs récupérées dans message.txt ---
A = 1141933368749651547285106584770022946598556294532255484018234071279017284493261458304303078441814350280055235938839850330392924394827971935746684756724106154783529866206686364342391780819577389806835022154187096665229978275413748714049243740736779489018438278478708068573511338451873371736513057724525994219285563327
b = 738623211561746372624170944030870485944978187433844583412325760777341380867104112487743286812112394661187612902430214202202766378016375904891604068375412515990443266634874912487423407082997026224391496763715710675145163967715339675283689424507137408425143581496186446869723885557865390662886201409684909929549168034
p = 2132004026303109138960419370582104845382939159231816273620696701294630284403386465532863373769144582236949856392667504369986764250039517010152815931140874682590496582913679422125500008296870534246366594745735993256988714723377030293374496770744770410547817411606458596058022709758993968788819254528632650187419776389
enc_hex = "928b818da1b6a499868abd91d18190d196bdd1d08781d0d4d5db9f"

# 1) On recalcule le secret partagé exactement comme le fait le serveur
shared = pow(A, b, p)

# 2) On convertit le message chiffré (texte hexadécimal) en octets bruts
enc_bytes = bytes.fromhex(enc_hex)

# 3) On applique le même XOR pour déchiffrer
flag_bytes = bytes([x ^ (shared % 256) for x in enc_bytes])

print(flag_bytes)
```

```bash
┌──(emma_aura㉿kali)-[~/Téléchargements]
└─$ nano solve.py
┌──(emma_aura㉿kali)-[~/Téléchargements]
└─$ python3 solve.py
b'picoCTF{dh_s3cr3t_32ec2679}'
```

🏁 **Flag obtenu : `picoCTF{dh_s3cr3t_32ec2679}`**

## 🧠 Ce que je retiens

- Dans un échange **Diffie-Hellman**, si l'une des deux valeurs privées (`a` ou `b`) fuite quelque part — même par erreur dans un fichier de debug — tout l'échange s'effondre : on peut recalculer le secret partagé sans avoir besoin de résoudre le problème du logarithme discret.
- Quand un challenge fournit le **code source** de chiffrement, il ne faut pas chercher à "deviner" une formule : il suffit de lire précisément quelle ligne calcule quoi, et de rejouer les mêmes opérations avec les valeurs qu'on possède.
- Un chiffrement par **XOR à clé répétée** se déchiffre en réappliquant exactement la même opération — c'est la propriété la plus utile (et la plus dangereuse si mal utilisée) du XOR en crypto.
- Toujours utiliser `pow(base, exposant, modulo)` avec les 3 arguments plutôt que `(base ** exposant) % modulo` : avec des nombres de centaines de chiffres, la version à 3 arguments reste rapide, l'autre peut littéralement bloquer le script.

---

*Prochain writeup bientôt — la suite de la progression picoCTF arrive !*
