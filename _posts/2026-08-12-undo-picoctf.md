---
title: "Undo — picoCTF : remonter une chaîne de transformations Linux"
description: "Writeup du challenge Undo (picoCTF, General Skills) : reconnaissance et inversion successive de Base64, rev, tr et ROT13 via netcat pour reconstituer le flag original."
date: 2026-08-12 04:13:00 +0100
categories: [CTF, picoCTF]
tags: [linux, encodage, base64, rot13, tr]
image:
  path: /assets/img/posts/Undo.png
  alt: Challenge Undo sur picoCTF
---

> Un challenge un peu différent des précédents : ici, pas de fichier à télécharger, mais un **service distant** auquel on se connecte avec `netcat`. Le principe est simple à comprendre mais demande de connaître ses commandes Linux de manipulation de texte : à chaque étape, le serveur affiche une version transformée du flag, donne un **indice** sur la transformation appliquée, et attend qu'on tape la **commande Linux qui l'inverse**. Cinq étapes, cinq transformations à identifier et à défaire dans l'ordre inverse.

## 🎯 En bref

| Infos | Détails |
| ----- | ------- |
| **Catégorie** | General Skills |
| **Difficulté** | 🟢 Facile |
| **Plateforme** | picoCTF 2026 |
| **Auteur du challenge** | Yahaya Meddy |
| **Outils utilisés** | `netcat` (`nc`), `base64`, `rev`, `tr` |
| **Connexion** | `nc foggy-cliff.picoctf.net 62907` |

## 📜 Énoncé

> Can you reverse a series of Linux text transformations to recover the original flag?
>
> **Hint :** For text translation and character replacement, see the `tr` command documentation.

Pas de fichier à télécharger cette fois : on se connecte directement au serveur avec `nc` (netcat), un outil qui ouvre une simple connexion réseau texte — ici, il joue le rôle d'un petit programme interactif qui pose une question à chaque étape.

```bash
┌──(emma_aura㉿kali)-[~]
└─$ nc foggy-cliff.picoctf.net 62907
===Welcome to the Text Transformations Challenge!===
```

## 🔍 Découvertes — les 5 étapes, une par une

### Étape 1 — Base64

```
Current flag: KXA2OTgxcHBxLWZhMDFnQHplMHNmYTRlRy1nazNnLXRhMWZlcmlyRShTR1BicHZj
Hint: Base64 encoded the string.
```

Le **Base64** est un encodage qui transforme n'importe quelle donnée (texte ou binaire) en une chaîne composée uniquement de lettres, chiffres et de `+`, `/`, `=` — pratique pour transporter des données dans des contextes qui n'acceptent que du texte "propre" (URLs, emails, JSON...). Ce n'est **pas du chiffrement** : n'importe qui peut le décoder, il n'y a pas de clé secrète.

On reconnaît du Base64 assez facilement : une chaîne qui ne contient que `A-Z`, `a-z`, `0-9`, `+`, `/`, et parfois un ou plusieurs `=` à la fin (padding). Pour l'inverser, l'outil en ligne de commande `base64` avec l'option `-d` (decode) :

```bash
Enter the Linux command to reverse it: base64 -d
Correct!
```

### Étape 2 — Texte inversé (`rev`)

```
Current flag: )p6981ppq-fa01g@ze0sfa4eG-gk3g-ta1ferirE(SGPbpvc
Hint: Reversed the text.
```

Le résultat de l'étape 1 est une chaîne lisible, mais **à l'envers** — on repère ça facilement en remarquant des fragments qui ressemblent à de l'anglais inversé (`ferirE` → `Erirref`? en fait tout le mot est retourné lettre par lettre). La commande `rev` fait exactement ce que son nom indique : elle inverse l'ordre des caractères d'une ligne.

```bash
Enter the Linux command to reverse it: rev
Correct!
```

### Étape 3 — Tirets et underscores échangés (`tr`)

```
Current flag: cvpbPGS(Eriref1at-g3kg-Ge4afs0ez@g10af-qpp1896p)
Hint: Replaced underscores with dashes.
```

L'indice dit que les **underscores** (`_`) d'origine ont été remplacés par des **tirets** (`-`). On voit effectivement plusieurs `-` dans la chaîne actuelle. Pour inverser ça, on utilise `tr` (translate/transliterate), qui remplace caractère par caractère :

```bash
Enter the Linux command to reverse it: tr '-' '_'
Correct!
```

`tr '-' '_'` veut dire : "partout où tu vois un `-`, remplace-le par un `_`" — l'inverse exact de la transformation d'origine.

### Étape 4 — Parenthèses ↔ accolades (`tr`)

```
Current flag: cvpbPGS(Eriref1at_g3kg_Ge4afs0ez@g10af_qpp1896p)
Hint: Replaced curly braces with parentheses.
```

Même logique : les **accolades** `{ }` (typiques du format d'un flag `picoCTF{...}`) ont été remplacées par des **parenthèses** `( )`. On inverse avec `tr`, mais cette fois avec deux caractères de chaque côté :

```bash
Enter the Linux command to reverse it: tr '()' '{}'
Correct!
```

`tr '()' '{}'` fait une correspondance position par position : `(` devient `{`, et `)` devient `}`.

### Étape 5 — ROT13 (et un piège à connaître !)

```
Current flag: cvpbPGS{Eriref1at_g3kg_Ge4afs0ez@g10af_qpp1896p}
Hint: Applied ROT13 to letters.
```

Le **ROT13** est un chiffrement par substitution très simple : chaque lettre est décalée de 13 positions dans l'alphabet (A→N, B→O, ... N→A). Comme l'alphabet a 26 lettres, appliquer ROT13 **deux fois de suite** redonne le texte d'origine — c'est un chiffrement "auto-inverse".

Premier réflexe (naturel, mais incomplet) :

```bash
Enter the Linux command to reverse it: tr 'a-z' 'n-za-m'
Incorrect. Try again.
Output: picoPGS{Eevers1ng_t3xt_Gr4nsf0rm@t10ns_dcc1896c}
```

Presque ! On voit bien `picoPGS{Eevers1ng...}` — le début (`pico`) est correct, mais `PGS` reste incohérent. **Le piège** : `tr 'a-z' 'n-za-m'` ne transforme que les lettres **minuscules**. Or la chaîne contient aussi des lettres **majuscules** (`PGS`, `E`, `G`...) qui, elles, ne sont pas touchées par cette commande et restent donc non déchiffrées.

Le serveur donne d'ailleurs l'indice de correction directement :

```bash
Hint: Try reversing: tr 'a-zA-Z' 'n-za-mN-ZA-M'
Enter the Linux command to reverse it: tr 'a-zA-Z' 'n-za-mN-ZA-M'
Correct!
```

Cette version traite **les deux casses en parallèle** : `a-z` vers `n-za-m` pour les minuscules, **et** `A-Z` vers `N-ZA-M` pour les majuscules — chaque bloc gardant sa propre casse (une majuscule reste une majuscule après transformation, une minuscule reste une minuscule).

## 🏁 Résultat final

```
Congratulations! You've recovered the original flag:
>>> picoCTF{Revers1ng_t3xt_Tr4nsf0rm@t10ns_dcc1896c}
```

**Flag obtenu : `picoCTF{Revers1ng_t3xt_Tr4nsf0rm@t10ns_dcc1896c}`**

## 🛠️ Commandes clés

| Commande | Rôle |
| -------- | ---- |
| `nc <host> <port>` | Se connecter à un service réseau distant en mode texte interactif |
| `base64 -d` | Décoder une chaîne encodée en Base64 |
| `rev` | Inverser l'ordre des caractères d'une ligne |
| `tr 'A' 'B'` | Remplacer chaque caractère de l'ensemble A par le caractère correspondant de l'ensemble B |
| `tr 'a-zA-Z' 'n-za-mN-ZA-M'` | Appliquer/inverser un ROT13, en traitant minuscules et majuscules séparément |

## 🧠 Ce que je retiens

- Une chaîne de transformations se résout **dans l'ordre inverse** de son application : la dernière transformation appliquée est la première à inverser.
- `tr` est un couteau suisse pour ce genre de challenge : il remplace des caractères un par un selon deux listes mises en correspondance — mais il faut penser à couvrir **toutes les casses et tous les caractères concernés**, sinon le résultat reste partiellement transformé (comme à l'étape 5).
- Le **ROT13** est un cas particulier amusant : l'appliquer une seconde fois annule la première application, car 13 + 13 = 26 = la taille complète de l'alphabet.
- Reconnaître un encodage à l'œil (Base64 : caractères alphanumériques + `=` en fin de chaîne ; ROT13 : texte "presque lisible" mais décalé) fait gagner beaucoup de temps par rapport à deviner au hasard.

---

*Prochain writeup bientôt — la suite de la progression picoCTF arrive !*
