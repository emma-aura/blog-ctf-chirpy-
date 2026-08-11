---
title: "StegoRSA — picoCTF : la clé privée RSA cachée dans une image"
description: "Writeup du challenge StegoRSA (picoCTF, Cryptographie, Facile) : inspection des métadonnées JPEG avec file et exiftool, reconnaissance du format hexadécimal grâce au détecteur de code de dcode.fr, reconstitution de la clé privée RSA et décryptage du flag avec OpenSSL."
date: 2026-08-10 15:00:00 +0100
categories: [CTF, Cryptographie]
tags: [picoctf, ctf, crypto, rsa, steganographie, dcode, exiftool, métadonnées, openssl, writeup]
image:
  path: /assets/img/posts/stegorsa-challenge.png
  alt: Challenge StegoRSA sur picoCTF
---

> Après les wargames (Bandit, Leviathan) et le reverse (RE101), voici mon premier **writeup picoCTF** ! **StegoRSA** est un challenge de **cryptographie** de niveau **facile** qui mélange deux mondes : la **stéganographie** (dissimuler une information dans un fichier image) et le **RSA** (déchiffrer un message). L'énoncé est un bijou de simplicité : le message est chiffré, la clé publique a disparu… mais quelqu'un a été **négligent avec la clé privée**. À nous de la retrouver et de déchiffrer le message !
{: .prompt-tip }

---

## 🎯 En bref

| Infos | Détails |
|---|---|
| **Challenge** | StegoRSA |
| **Plateforme** | [picoCTF](https://picoctf.org) |
| **Catégorie** | Cryptographie |
| **Difficulté** | Facile |
| **Auteur** | Yahaya Meddy (F3) |
| **Fichiers fournis** | `image.jpg` (l'image piégée) + `flag.enc` (le message chiffré) |
| **Méthode** | Métadonnées (`file` / `exiftool`) → reconnaissance du format (dcode.fr) → hex → clé PEM → `openssl pkeyutl` |

**Ce qu'on apprend ici** : la **stéganographie ≠ le chiffrement**. Cacher une clé dans une image ne la protège pas : dès qu'on pense à regarder — surtout les **métadonnées** — tout tombe. Et que l'**hexadécimal est partout** : il suffit de savoir le reconnaître pour reconstituer un fichier.

---

## 📜 Le challenge

La description officielle :

> *A message has been encrypted using RSA. The public key is gone... but someone might have been careless with the private key. Can you recover it and decrypt the message?*

Deux indices accompagnent le challenge — et ils disent presque tout :

1. **Metadata can tell you more than you expect.** — *Les métadonnées en disent plus qu'on ne le croit.*
2. **Hex can be turned back into a key file.** — *L'hexadécimal peut redevenir un fichier clé.*

Deux fichiers à télécharger :
- `image.jpg` — une image 512×512, à première vue banale
- `flag.enc` — le flag chiffré en RSA

![La page du challenge StegoRSA sur picoCTF](/assets/img/posts/stegorsa-challenge.png){: .shadow .rounded-10 }

---

## 🔍 Étape 1 — La découverte

Premier réflexe : examiner les fichiers fournis. Le nom du challenge est déjà un indice en soi : **Stego**RSA → stéganographie + RSA. L'image est le seul fichier « à inspecter », le `flag.enc` étant le message à déchiffrer une fois la clé retrouvée.

![La découverte : le challenge et ses fichiers](/assets/img/posts/stegorsa-decouverte.png){: .shadow .rounded-10 }

---

## 🕵️ Étape 2 — L'inspection des métadonnées

L'indice 1 parle de **métadonnées** : direction les outils d'analyse de fichiers. `file` donne déjà un premier aperçu, et `exiftool` (l'outil de référence pour lire les métadonnées) révèle un détail intéressant : un champ **Comment** rempli d'une longue chaîne hexadécimale !

```bash
└─$ file image.jpg
image.jpg: JPEG image data, JFIF standard 1.01, ..., comment: "2d2d2d2d2d424547494e2050524956415445204b45592d2d2d2d2d0a4d49494576514942...", baseline, precision 8, 512x512, components 3

└─$ exiftool image.jpg
File Type                       : JPEG
Image Width                     : 512
Image Height                    : 512
Comment                         : 2d2d2d2d2d424547494e2050524956415445204b45592d2d2d2d2d0a4d49494576514942...
```

Un champ `Comment` JPEG rempli de caractères `2d`, `42`, `45`… ce n'est pas anodin : les métadonnées cachent quelque chose.

---

## 🧩 Étape 3 — La reconnaissance du format : le détecteur de code de dcode.fr

Je me retrouve avec une chaîne de caractères inconnue — comment savoir ce que c'est ? C'est là qu'intervient le [détecteur de code (cipher identifier) de dcode.fr](https://www.dcode.fr/cipher-identifier) : on lui colle la chaîne, et il identifie le type de chiffrement/encodage.

![Le détecteur de code de dcode.fr](/assets/img/posts/stegorsa-detecteur.png){: .shadow .rounded-10 }

Verdict : de l'**hexadécimal** ! Et le début de la chaîne vaut le coup d'œil :

```text
2d2d2d2d2d 42 45 47 49 4e 20 50 52 49 56 41 54 45 20 4b 45 59 2d2d2d2d2d 0a
```

En ASCII, `2d` = le tiret `-`, `42` = `B`, `45` = `E`, `47` = `G`, `49` = `I`, `4e` = `N`, `0a` = retour à la ligne… Autrement dit : **`-----BEGIN PRIVATE KEY-----\n`**. La clé privée RSA est là, en clair, juste encodée en hexadécimal !

![Le résultat du détecteur : la chaîne hexadécimale identifiée](/assets/img/posts/stegorsa-resultat.png){: .shadow .rounded-10 }

> 💡 Le décodage des premiers octets suffit presque toujours à deviner le format d'un fichier caché : `2d 2d 2d` = `---`, `50 4b` = `PK` (zip), `1f 8b` = gzip… — le réflexe *magic bytes* qu'on avait déjà vu dans [Bandit]({% post_url 2026-07-25-bandit-overthewire %}).
{: .prompt-info }

---

## 🔑 Étape 4 — De l'hex au fichier clé (PEM)

Deuxième indice : *« Hex can be turned back into a key file. »* Il suffit de convertir l'hexadécimal en binaire pour reconstituer la clé au format PEM :

```bash
echo "2d2d2d2d2d424547494e2050524956415445204b45592d2d2d2d2d0a..." | xxd -r -p > cle.pem
cat cle.pem
```

```text
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCOdn3AYDcumr2w
N/Oo6AOJoESl6RPNyei+zev9CkXAnrvkAaB9ih9Y/93CB8akMbzWVgZ2P7iW0DVc
...
-----END PRIVATE KEY-----
```

> 💡 Équivalent Python, même conversion en une ligne : `bytes.fromhex(hex_data).decode()`.
{: .prompt-info }

---

## 🔓 Étape 5 — Décryptage RSA du flag

Clé privée en main, le déchiffrement de `flag.enc` devient une formalité. `flag.enc` fait ≈ 256 octets (un bloc RSA 2048 bits) : c'est un déchiffrement RSA « brut », parfait pour `openssl pkeyutl` :

```bash
└─$ openssl pkeyutl -decrypt -in flag.enc -inkey cle.pem
picoCTF{rs4_k3y_1n_1mg_4eedd678}
```

> 😄 Petit détail du live : mon fichier clé s'appelait `cle.pivate` (un `r` oublié dans `nano`)… et ça marche quand même !
{: .prompt-info }

Équivalent en Python (bibliothèque `cryptography`) :

```python
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding

with open("cle.pem", "rb") as f:
    key = load_pem_private_key(f.read(), password=None)

with open("flag.enc", "rb") as f:
    ciphertext = f.read()

print(key.decrypt(ciphertext, padding.PKCS1v15()).decode())
```

---

## 🏁 Le flag

```text
picoCTF{rs4_k3y_1n_1mg_4eedd678}
```

Le flag confirme tout le mécanisme : **rs4_k3y_1n_1mg** — *« RSA key in image »*. La clé était bien cachée dans l'image !

---

## 🧠 Ce que j'ai appris

| Leçon | Détail |
|---|---|
| **Les métadonnées sont le premier endroit à regarder** | `file` puis `exiftool` : le champ *Comment* d'un JPEG peut contenir n'importe quoi — en forensics comme en CTF, c'est le tout premier réflexe |
| **Stéganographie ≠ chiffrement** | Cacher une clé dans une image ne la protège pas : la stéganographie **dissimule**, elle ne chiffre pas. Une fois qu'on sait où regarder, le secret tombe |
| **Reconnaître l'encodage avant de décoder** | Face à une chaîne inconnue, le [cipher identifier de dcode.fr](https://www.dcode.fr/cipher-identifier) évite de deviner au hasard : on identifie le format (hex, base64…), puis on décode |
| **Reconstituer un fichier depuis l'hex** | `xxd -r -p` (ou `bytes.fromhex` en Python) : les *magic bytes* décodés en ASCII révèlent le format du fichier caché (`2d 2d 2d` = `---`…) |
| **Le RSA brut se déchiffre avec `openssl pkeyutl`** | Pour un message chiffré « directement » en RSA (pas via un format conteneur), `openssl pkeyutl -decrypt -inkey cle.pem -in flag.enc` est l'outil exact |

### 🔬 Pour aller plus loin : où cache-t-on des données dans une image ?

| Méthode | Principe | Comment la détecter |
|---|---|---|
| **Métadonnées (EXIF / Comment)** | Champ texte libre dans l'en-tête du fichier — *la méthode de ce challenge* | `file`, `exiftool` |
| **LSB** (bits de poids faible) | On modifie le dernier bit de chaque pixel : invisible à l'œil | `zsteg`, analyse statistique des couleurs |
| **Append (fin de fichier)** | On colle des données après la fin de l'image réelle | `binwalk`, comparaison de tailles |
| **Steganography software** | steghide, outguess… (souvent avec passphrase) | `steghide info`, `steghide extract` |

La vraie leçon de sécurité : **ne jamais mettre une clé privée dans un fichier partagé** — même « cachée », elle sera retrouvée par n'importe quel outil d'analyse. Une clé privée ne doit exister que là où personne d'autre ne peut la lire.

---

## 📚 Ressources liées

- [Mon récap picoCTF]({% post_url 2026-08-10-picoctf-writeups %}) — l'index de ma progression picoCTF, classé par catégorie
- [picoCTF](https://picoctf.org) — la plateforme de challenges
- [dcode.fr — cipher identifier (détecteur de code)](https://www.dcode.fr/cipher-identifier) — reconnaître un chiffrement/encodage
- [dcode.fr — déchiffreur RSA](https://www.dcode.fr/rsa-cipher) — alternative en ligne pour le décryptage
- [Mon récap OverTheWire]({% post_url 2026-08-03-overthewire-wargames-recapitulatif %}) — le contexte de ma progression
- [Mon RE101 MalwareUnicorn]({% post_url 2026-08-03-re101-malwareunicorn %}) — la méthode d'analyse, transposable aux fichiers de CTF

*Prochaines étapes : des challenges crypto plus « purs » (attaques RSA — Wiener, petit exposant…), et pourquoi pas d'autres writeups picoCTF. Stay tuned !* 🚀
