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
| **Challenge résolu** | 1 (StegoRSA) |
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
🔐 Cryptographie : StegoRSA ✅
🕵️ Forensics      : à venir ⬜
🌐 Web            : à venir ⬜
⚙️ Reverse        : à venir ⬜
🔓 Pwn            : à venir ⬜
```

---

## 📊 Mon bilan après ce premier challenge

| Domaine | Ce que j'ai appris |
|---------|---------------------|
| **Métadonnées** | Les métadonnées d'une image (champ Comment) peuvent cacher n'importe quoi — premier réflexe en forensics |
| **Encodages** | Savoir reconnaître l'hexadécimal (et le base64, ROT13…) avant de décoder |
| **Stéganographie** | Cacher ≠ chiffrer : une clé cachée dans une image est récupérable |
| **RSA / OpenSSL** | `openssl pkeyutl -decrypt` pour un déchiffrement RSA brut |

---

## 📚 Ressources liées

- [picoCTF](https://picoctf.org) — la plateforme de challenges
- [Writeup StegoRSA]({% post_url 2026-08-10-stegorsa-picoctf %}) — la résolution complète en détail
- [Mon récap OverTheWire]({% post_url 2026-08-03-overthewire-wargames-recapitulatif %}) — la même logique de progression, appliquée aux wargames
- [Ma page Ressources]({% link _tabs/ressources.md %}) — les outils et sites utiles

*Ce post sera mis à jour à chaque nouveau challenge picoCTF résolu — chaque writeup s'ajoute dans sa catégorie. Stay tuned !* 🚀
