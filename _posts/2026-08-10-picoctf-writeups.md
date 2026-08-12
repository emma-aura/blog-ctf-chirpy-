---
title: "picoCTF — Récapitulatif & Progression"
description: "Ma progression sur picoCTF : mes challenges résolus classés par catégorie (cryptographie, forensics, web…), chacun avec son writeup complet."
date: 2026-08-10 18:00:00 +0100
categories: [CTF, picoCTF]
tags: [picoctf, ctf, writeup, progression]
pin: true
image:
  path: /assets/img/posts/picoctf.png
  alt: Logo picoCTF
---

> Ce post est **l'index vivant de ma progression sur [picoCTF](https://picoctf.org)**. Chaque challenge résolu s'ajoute ici, **classé par catégorie** (cryptographie, forensics, web…) avec sa difficulté réelle 🟢🟡🔴, et pointe vers son writeup complet.
{: .prompt-tip }

---

## 🎯 En bref

| Infos | Détails |
|---|---|
| **Plateforme** | [picoCTF](https://picoctf.org) |
| **Challenges résolus** | 4 (StegoRSA, Shared Secrets, Undo, MyGit) |
| **Principe** | Chaque challenge = une entrée classée par catégorie |
| **Format** | Résumé + lien vers le writeup complet (avec photos de résolution) |

---

## 🏆 Les challenges résolus

### 🔐 Cryptographie

**StegoRSA** — 🟢 Facile — résolu le 10/08/2026

> [**Writeup complet : StegoRSA — la clé privée RSA cachée dans une image**]({% post_url 2026-08-10-stegorsa-picoctf %})

**Objectif** : un message a été chiffré en RSA, la clé publique a disparu… mais quelqu'un a été négligent avec la clé privée.

| Étape | Ce qu'on fait |
|-------|--------------|
| Découverte | `file image.jpg` + `exiftool image.jpg` → champ **Comment** rempli d'une chaîne hexadécimale |
| Reconnaissance | Détecteur de code de dcode.fr → verdict : de l'**hexadécimal** |
| Extraction | Décodage : `2d 2d 2d` = `---` → `-----BEGIN PRIVATE KEY-----` |
| Reconstitution | `xxd -r -p` → clé privée PEM (`cle.pem`) |
| Décryptage | `openssl pkeyutl -decrypt -in flag.enc -inkey cle.pem` → flag |

**Compétences** : métadonnées (forensics), reconnaissance d'encodage, stéganographie, RSA, OpenSSL.

**Flag** : `picoCTF{rs4_k3y_1n_1mg_4eedd678}`

**Shared Secrets** — 🟢 Facile — résolu le 12/08/2026

> [**Writeup complet : Shared Secrets — quand le secret Diffie-Hellman fuite en clair**]({% post_url 2026-08-12-shared-secrets-picoctf %})

**Objectif** : un message a été chiffré avec un secret partagé (échange Diffie-Hellman)… mais l'une des deux parties a laissé fuiter son secret privé dans le fichier de sortie.

| Étape | Ce qu'on fait |
|-------|--------------|
| Analyse | Lecture du code source `encryption.py` → repérage de la fuite : le secret `b` du client est écrit en clair dans `message.txt` |
| Recalcul | `shared = pow(A, b, p)` → on rejoue le calcul du serveur avec les valeurs fuitées |
| Déchiffrement | XOR répété (`shared % 256`) appliqué à `enc` → flag |

**Compétences** : Diffie-Hellman, arithmétique modulaire (`pow()` à 3 arguments), XOR à clé répétée, lecture de code source.

**Flag** : `picoCTF{dh_s3cr3t_32ec2679}`

### 🛠️ General Skills

**Undo** — 🟢 Facile — résolu le 12/08/2026

> [**Writeup complet : Undo — remonter une chaîne de transformations Linux**]({% post_url 2026-08-12-undo-picoctf %})

**Objectif** : un service distant applique **5 transformations successives** au flag (Base64, `rev`, `tr`, ROT13…) ; à chaque étape, le serveur affiche le flag transformé, donne un indice, et attend la commande Linux qui **inverse** la transformation.

| Étape | Ce qu'on fait |
|-------|--------------|
| Connexion | `nc foggy-cliff.picoctf.net 62907` — un service interactif pose une question à chaque étape |
| Étapes 1-2 | `base64 -d` puis `rev` — décoder le Base64, inverser l'ordre des caractères |
| Étapes 3-4 | `tr '-' '_'` puis `tr '()' '{}'` — remplacer des caractères par paires |
| Étape 5 | ROT13 : `tr 'a-zA-Z' 'n-za-mN-ZA-M'` — le piège : ne pas oublier les **majuscules** |

**Compétences** : netcat, encodage Base64, manipulation de texte (`rev`, `tr`), ROT13, résolution d'une chaîne de transformations dans l'**ordre inverse**.

**Flag** : `picoCTF{Revers1ng_t3xt_Tr4nsf0rm@t10ns_dcc1896c}`

**MyGit** — 🟢 Facile — résolu le 12/08/2026

> [**Writeup complet : MyGit — usurper l'identité root avec un simple commit Git**]({% post_url 2026-08-12-mygit-picoctf %})

**Objectif** : un serveur Git maison ne renvoie le flag que si un `flag.txt` est poussé par un auteur nommé `root` (`root@picoctf`)… or l'identité d'un commit Git est une métadonnée que le client déclare lui-même, sans aucune vérification.

| Étape | Ce qu'on fait |
|-------|--------------|
| Clone | `git clone ssh://git@foggy-cliff.picoctf.net:53071/git/challenge.git` — lecture du `README.md` : la règle exacte est écrite noir sur blanc |
| Imposture | `git config user.name "root"` + `git config user.email "root@picoctf"` — on se déclare root, aucune preuve demandée |
| Push | `touch flag.txt` + `git add .` + `git commit` + `git push` → le serveur croit en l'identité déclarée et renvoie le flag |

**Compétences** : Git (clone, config, commit, push), compréhension du modèle de confiance de l'auteur d'un commit, lecture d'énoncé/README.

**Flag** : `picoCTF{1mp3rs0n4t4_g17_345y_02a39618}`

### 🕵️ Forensics

*(pas encore de challenge résolu — à venir)*

### 🌐 Web

*(pas encore de challenge résolu — à venir)*

### ⚙️ Reverse Engineering

*(pas encore de challenge résolu — à venir)*

### 🔓 Exploitation (Pwn)

*(pas encore de challenge résolu — à venir)*

---

## 🧭 Progression à venir

Chaque nouveau challenge résolu viendra **s'ajouter dans sa catégorie** — pas de montée en difficulté artificielle, juste ma collection qui grandit :

```text
🔐 Cryptographie : StegoRSA ✅, Shared Secrets ✅
🛠️ General Skills : Undo ✅, MyGit ✅
🕵️ Forensics      : à venir ⬜
🌐 Web            : à venir ⬜
⚙️ Reverse        : à venir ⬜
🔓 Pwn            : à venir ⬜
```

---

## 📊 Mon bilan

| Domaine | Ce que j'ai appris |
|---------|---------------------|
| **Métadonnées** | Les métadonnées d'une image (champ Comment) peuvent cacher n'importe quoi — premier réflexe en forensics |
| **Encodages** | Savoir reconnaître l'hexadécimal (et le base64, ROT13…) avant de décoder |
| **Stéganographie** | Cacher ≠ chiffrer : une clé cachée dans une image est récupérable |
| **RSA / OpenSSL** | `openssl pkeyutl -decrypt` pour un déchiffrement RSA brut |
| **Diffie-Hellman** | Si l'une des valeurs privées (`a` ou `b`) fuite, tout l'échange s'effondre : on recalcule le secret partagé sans casser le logarithme discret |
| **XOR / Python** | Le XOR se déchiffre en réappliquant la même clé ; `pow(base, exp, mod)` à 3 arguments pour les grands nombres |
| **netcat** | `nc <host> <port>` ouvre une session texte interactive avec un service distant — le point d'entrée de beaucoup de challenges |
| **Texte Linux** | `rev` inverse une ligne, `tr` remplace caractère par caractère ; une chaîne de transformations se dénoue dans l'**ordre inverse** |
| **ROT13** | Auto-inverse (13 + 13 = 26)… à condition de traiter **minuscules et majuscules** : `tr 'a-zA-Z' 'n-za-mN-ZA-M'` |
| **Git** | L'auteur d'un commit (`user.name`/`user.email`) est une métadonnée **déclarative** : se déclarer `root` suffit — l'authentification réelle (SSH, token) est indépendante de ce champ |
| **Conception serveur** | Ne jamais faire confiance à une donnée fournie par le client (auteur du commit, en-têtes HTTP…) comme source de vérité pour une autorisation |

---

## 📚 Ressources liées

- [picoCTF](https://picoctf.org) — la plateforme de challenges
- [Writeup StegoRSA]({% post_url 2026-08-10-stegorsa-picoctf %}) — la résolution complète en détail
- [Writeup Shared Secrets]({% post_url 2026-08-12-shared-secrets-picoctf %}) — la résolution complète en détail
- [Writeup Undo]({% post_url 2026-08-12-undo-picoctf %}) — la résolution complète en détail
- [Writeup MyGit]({% post_url 2026-08-12-mygit-picoctf %}) — la résolution complète en détail
- [Mon récap OverTheWire]({% post_url 2026-08-03-overthewire-wargames-recapitulatif %}) — la même logique de progression, appliquée aux wargames
- [Ma page Ressources]({% link _tabs/ressources.md %}) — les outils et sites utiles

*Ce post sera mis à jour à chaque nouveau challenge picoCTF résolu — chaque writeup s'ajoute dans sa catégorie. Stay tuned !* 🚀
