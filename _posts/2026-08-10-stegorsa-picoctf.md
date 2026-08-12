---
title: "StegoRSA — picoCTF : la clé privée RSA cachée dans une image"
description: "Writeup du challenge StegoRSA (picoCTF, Cryptographie, Facile) : inspection des métadonnées JPEG avec file et exiftool, reconnaissance du format hexadécimal avec dCode, reconstitution de la clé privée RSA et déchiffrement du flag avec OpenSSL."
date: 2026-08-11 15:00:00 +0100
categories: [CTF, picoCTF]
tags: [crypto, rsa, steganographie, forensics, exiftool, openssl]
image:
  path: /assets/img/posts/StegoRSA.png
  alt: Challenge StegoRSA sur picoCTF
---

> Après les wargames (Bandit, Leviathan) et le reverse (RE101), voici un nouveau writeup picoCTF ! **StegoRSA** est un challenge de **cryptographie** de niveau **facile** qui mélange deux mondes : la **stéganographie** (dissimuler une information dans un fichier image) et le **RSA** (déchiffrer un message). L'énoncé est un bijou de simplicité : le message est chiffré, la clé publique a disparu… mais quelqu'un a été **négligent avec la clé privée**. À nous de la retrouver et de déchiffrer le message !

## 🎯 En bref

| Infos | Détails |
| ----- | ------- |
| **Catégorie** | Cryptographie |
| **Difficulté** | 🟢 Facile |
| **Plateforme** | picoCTF 2026 |
| **Auteur du challenge** | Yahaya Meddy |
| **Outils utilisés** | `file`, `exiftool`, [dcode.fr](https://www.dcode.fr/), `openssl` |
| **Fichiers fournis** | `flag.enc`, `image.jpg` |

## 📜 Énoncé

> A message has been encrypted using RSA. The public key is gone… but someone might have been careless with the private key. Can you recover it and decrypt the message?
>
> **Hints :**
> 1. Metadata can tell you more than you expect.
> 2. Hex can be turned back into a key file.

On récupère deux fichiers : un message chiffré `flag.enc`, et une image `image.jpg`. Les indices sont clairs — la solution se cache dans les **métadonnées** de l'image, sous une forme **hexadécimale**.

## 🔍 Découvertes

### Étape 1 — Identifier le type de fichier

Premier réflexe sur un challenge de stégo/forensics : vérifier ce qu'on a vraiment entre les mains avec `file`.

```bash
┌──(emma_aura㉿kali)-[~/Téléchargements]
└─$ file image.jpg
image.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, comment: "2d2d2d2d2d424547494e2050524956415445204b45592d2d2d2d2d0a4d494945765149424144414e42676b71686b6947397730424151454641415343424b63", baseline, precision 8, 512x512, components 3
```

Le champ **`comment`** attire immédiatement l'œil : une longue chaîne hexadécimale est planquée directement dans les métadonnées JPEG. C'est exactement ce que le premier indice ("*metadata can tell you more than you expect*") laissait présager.

### Étape 2 — Extraire la métadonnée complète

Le `comment` renvoyé par `file` est tronqué. Pour récupérer la chaîne hexadécimale en entier, on passe par `exiftool`, plus complet pour l'extraction de métadonnées.

```bash
┌──(emma_aura㉿kali)-[~/Téléchargements]
└─$ exiftool image.jpg
...
Comment                         : 2d2d2d2d2d424547494e2050524956415445204b45592d2d2d2d2d0a4d4949...
Image Width                     : 512
Image Height                    : 512
...
```

Cette fois on récupère la totalité de la chaîne hex, bien plus longue — un signe qu'il s'agit probablement d'un bloc de données structuré plutôt que d'un simple commentaire texte.

### Étape 3 — Convertir l'hexadécimal

Deuxième indice du challenge : "*hex can be turned back into a key file*". Direction [dcode.fr](https://www.dcode.fr/) pour convertir cette chaîne hexadécimale en texte lisible via le **convertisseur ASCII**.

![Conversion de l'hexadécimal en ASCII sur dCode](/assets/img/posts/Decouverte.png)
_La chaîne hexadécimale extraite se décode directement en clé privée PEM_

Le résultat est sans appel : la chaîne hexadécimale n'est autre que l'encodage d'une **clé privée RSA au format PEM**, en clair :

```
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCOdn3AYDcumr2w
N/Oo6AOJoESl6RPNyei+zev9CkXAnrvkAaB9ih9Y/93CB8akMbzWVgZ2P7iW0DVc
dZPY9YVehK3YxEb9mMe1nGGXJkO6enaosnw0D7TMDRzB5xtEF7CirTRJCYv1JUaF
HwSrXA6OVr2IrFQ2r+qw8Co9P0TRSIIV4fVk9XP0Pq3F2tDS8mQVVhC1K//w+lEa
h0UEk7vJvmC6yohDgTVQ4bANfPsTEBLn5EeFJ3p4sz3/I+cCDnryoSrjlLdK2f5x
LOwl2ivzRtTrJX2SWfmaBPgI2YUljBIKQJVBCA9RhuWm/zS9UZCH8rxprF6hhxZz
oq7D1Vq/AgMBAAECggEAFk/IchCfk9T4UFjy+EkeBLftCG7wgxJUOU3W39J0Ci7S
DmuSzxaKwk2QVYsSOTTw9kCS0oI4TqZdNRXVCe2p7Zup/oD+/UioPnE3d4yuns3/
N3x8p0qubia/kj63rnpnV5L41VeBa+timAa7nHrWbMR4+qbCqa3ze7KhauY1yPDu
SC3YBNhtz4XoubwMWg4ViW8KOpf0Lu18DwnJ8qveJm2S0qUptyDn1Xs6It7MTj+4
/k2XJBlh691XZqB4xLcivyyqI8VWLKrwO33sTJSfGpVIaN3iGCv55k42OKOs0VB2
QZRPYkfGBBr0eZrYGkqC3mgLcbiHbbyZFDlr2AKSAQKBgQDJNq5pcr6O4yXOgmSw
0nYx2ZyM+THEEDtLU6Qwmd6zwgPEUn9HxtGFssLXdf1XL1ixAzDIaAmpnBWIIled
ocwUf2d99K3tLklR+j2XijME76RmmCrj1qKDw/bj/C9EFTBJYeL3VdxlDk5PnU8d
Owrs8rFHPg2/giqmaxHterBEXwKBgQC1QKt17jZt8nnWsUjg/zopRDC+WyZcbfk2
JoRG/J6pyy2CqYqYLJvCNuLL3oJBMdUhsXToOaL0DFKa059oLJU4M2O+ey+R/jVd
fSqYyR+T+ovPJLrgN3mNuR6547awR0w7I2nDqlf0MT0pLdH4QPayhmrqDWQhQscE
dwtEJKuFoQKBgQCeBlHoAvPhqEdy7jlCHagx8mPe237YKp9Gw4O5n76lkoP+1YOc
zWqUBBa9vK6goFCZhJX1bq/YAvtuFPqWlBGBL6YJ5/YIxkdTGKLyttjm0YZeBLf6
hADSVz85Qj+kyrdHipcEBOy4eQnLwRH3NP2ZpejQuM13UDVKyeAkkCyLJQKBgHUP
0m11L5QtEcG2eIJQdOjoEK8wwYLayCTQFYifaX3yKm+EPm3wCZ0Sw8G18NxYafW7
3eyKJROHzeYPHZoziSBmGFqSxvN8gkziJRvOceWp4JgleciMK6Z71DtstbX+Jl7f
jVSA9RNSpdStsjmrA2nj5LNLeMr+jPj2RcF6CYlhAoGAcuHCo4anU+DY2eQSTzME
EL+dbsK2IXdp5fGwMKhESvU5PxAJ/jlOU3i53Nmdiow47nsNMFfrdzTk4hIzwZ8V
2CtB4RWMeJOUmZAGWPFnKPYFdsSF0Wi7PLSOACR2N90XPcfcZUDTPJbCr1QoCK1U
sdKl3MsrZH9mq+CYlnU8Ov8=
-----END PRIVATE KEY-----
```

> 💡 Petit aparté sur l'outil utilisé : dCode propose aussi un **détecteur de chiffrement automatique**, capable d'identifier plus de 250 types de chiffrements/encodages à partir d'un texte donné. Pratique quand on n'est pas sûr à 100 % du format en face de soi.

![Page des outils de cryptographie et de reconnaissance de chiffrement sur dCode](/assets/img/posts/Detecteur.png)
_Le détecteur de chiffrement de dCode_

![Résultat du détecteur : le format Hexadécimal (Base 16) est suggéré en priorité](/assets/img/posts/resultat_du_detecteur.png)
_L'analyseur confirme qu'il s'agit bien d'hexadécimal_

### Étape 4 — Reconstituer le fichier de clé

Une fois le contenu PEM récupéré, il ne reste plus qu'à le sauvegarder tel quel dans un fichier local.

```bash
┌──(emma_aura㉿kali)-[~/Téléchargements]
└─$ nano cle.pivate
```

*(on colle le bloc `-----BEGIN PRIVATE KEY----- ... -----END PRIVATE KEY-----` récupéré à l'étape précédente, puis on sauvegarde)*

### Étape 5 — Déchiffrer le message

Il ne reste plus qu'à utiliser cette clé privée fraîchement reconstituée pour déchiffrer `flag.enc` avec `openssl` :

```bash
┌──(emma_aura㉿kali)-[~/Téléchargements]
└─$ openssl pkeyutl -decrypt -in flag.enc -inkey cle.pivate
picoCTF{rs4_k3y_1n_1mg_4eedd678}
```

🏁 **Flag obtenu : `picoCTF{rs4_k3y_1n_1mg_4eedd678}`**

## 🛠️ Commandes clés

| Commande | Rôle |
| -------- | ---- |
| `file image.jpg` | Identifier le type de fichier et repérer un premier indice dans les métadonnées |
| `exiftool image.jpg` | Extraire l'intégralité des métadonnées, y compris les champs tronqués par `file` |
| Convertisseur ASCII / détecteur — [dcode.fr](https://www.dcode.fr/) | Décoder la chaîne hexadécimale et confirmer le format identifié |
| `nano cle.pivate` | Reconstituer le fichier de clé privée PEM à partir du texte décodé |
| `openssl pkeyutl -decrypt -in flag.enc -inkey cle.pivate` | Déchiffrer le message avec la clé privée RSA récupérée |

## 🧠 Ce que je retiens

- Les métadonnées d'un fichier (EXIF, JFIF, PDF, etc.) sont un vecteur de dissimulation d'information classique en stéganographie/forensics — toujours vérifier avec `file` **et** `exiftool`, car `file` tronque parfois les champs longs.
- Une clé RSA (privée ou publique) peut être encodée sous plusieurs formes (hex, base64…) : savoir reconnaître un format à l'œil (ou via un détecteur automatique) fait gagner un temps précieux.
- Une fois la clé privée récupérée, `openssl pkeyutl -decrypt` suffit à déchiffrer un message RSA sans avoir besoin d'écrire la moindre ligne de code.

---

*Prochain writeup bientôt — n'hésite pas à me suivre pour la suite de la progression picoCTF !*
