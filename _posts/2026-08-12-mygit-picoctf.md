---
title: "MyGit — picoCTF : usurper l'identité root avec un simple commit Git"
description: "Writeup du challenge MyGit (picoCTF, General Skills) : exploitation d'un serveur Git qui valide le flag uniquement sur la base de l'auteur du commit (git config user.name/user.email), sans aucune authentification réelle."
date: 2026-08-12 05:30:00 +0100
categories: [CTF, picoCTF]
tags: [git, linux, general-skills]
image:
  path: /assets/img/posts/MyGit.png
  alt: Challenge MyGit sur picoCTF
---

> Un challenge **General Skills** qui ne demande aucune connaissance en crypto ou en reverse — juste de comprendre comment Git identifie l'auteur d'un commit, et de réaliser qu'il n'y a **aucune vérification réelle** derrière cette identité. Le serveur "fait confiance" à ce que le client déclare lui-même. Autrement dit : on peut littéralement se déclarer `root` sans prouver quoi que ce soit.

## 🎯 En bref

| Infos | Détails |
| ----- | ------- |
| **Catégorie** | General Skills |
| **Difficulté** | 🟢 Facile |
| **Plateforme** | picoCTF 2026 |
| **Auteur du challenge** | Darkraicg492 |
| **Outils utilisés** | `git` (clone, config, add, commit, push) |

## 📜 Énoncé

> I have built my own Git server with my own rules!
>
> You can clone the challenge repo using the command below.
>
> `git clone ssh://git@foggy-cliff.picoctf.net:53071/git/challenge.git`
>
> Here's the password: `e38a0906`
>
> Check the README to get your flag!
>
> **Hint :** How do you specify your Git username and email?

_Le challenge sur la plateforme picoCTF_

L'indice est presque une réponse déguisée : le challenge tourne clairement autour de la façon dont on **déclare son identité** sur un commit Git — pas autour d'une faille technique complexe.

## 🔍 Découvertes

### Étape 1 — Cloner le dépôt

On récupère le dépôt Git distant avec le mot de passe fourni dans l'énoncé :

```bash
┌──(emma_aura㉿kali)-[~/Téléchargements]
└─$ git clone ssh://git@foggy-cliff.picoctf.net:53071/git/challenge.git
Clonage dans 'challenge'...
...
git@foggy-cliff.picoctf.net's password: 
remote: Enumerating objects: 3, done.
...
Réception d'objets: 100% (3/3), fait.
```

### Étape 2 — Lire le README, comprendre la règle du jeu

```bash
┌──(emma_aura㉿kali)-[~/Téléchargements/challenge]
└─$ cat README.md 
# MyGit

### If you want the flag, make sure to push the flag!

Only flag.txt pushed by root:root@picoctf will be updated with the flag.

GOOD LUCK!
```

La règle est écrite noir sur blanc : le serveur ne renverra le flag **que** si un fichier nommé `flag.txt` est poussé (`push`) par un auteur identifié comme `root`, avec l'adresse `root@picoctf`.

**Le point clé à comprendre** : dans Git, l'identité de l'auteur d'un commit (nom + email) n'est **pas** liée à un vrai compte utilisateur vérifié ni à une authentification — c'est juste une information que le client déclare lui-même localement, via `git config`. Le serveur du challenge se base uniquement sur cette métadonnée déclarative pour décider s'il "croit" que c'est root ou non. Il n'y a donc rien à casser techniquement : il suffit de **se présenter comme root**.

### Étape 3 — Se déclarer "root"

On configure localement (pour ce dépôt uniquement, sans `--global`) le nom et l'email attendus par le serveur :

```bash
┌──(emma_aura㉿kali)-[~/Téléchargements/challenge]
└─$ git config user.name "root"
┌──(emma_aura㉿kali)-[~/Téléchargements/challenge]
└─$ git config user.email "root@picoctf"
```

Ces deux commandes n'ont besoin d'aucune preuve d'identité : elles écrivent simplement ces valeurs dans le fichier `.git/config` du dépôt local, et c'est ce que Git utilisera pour signer les prochains commits localement.

### Étape 4 — Créer et pousser flag.txt

On crée le fichier vide attendu, puis on l'ajoute et on le commit avec l'identité qu'on vient de configurer :

```bash
┌──(emma_aura㉿kali)-[~/Téléchargements/challenge]
└─$ touch flag.txt
┌──(emma_aura㉿kali)-[~/Téléchargements/challenge]
└─$ git add .
┌──(emma_aura㉿kali)-[~/Téléchargements/challenge]
└─$ git commit -m "flag"
[master f9bbe98] flag
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 flag.txt
```

Puis on pousse le commit vers le serveur distant :

```bash
┌──(emma_aura㉿kali)-[~/Téléchargements/challenge]
└─$ git push
...
git@foggy-cliff.picoctf.net's password: 
Énumération des objets: 4, fait.
...
remote: Author matched and flag.txt found in commit...
remote: Congratulations! You have successfully impersonated the root user
remote: Here's your flag: picoCTF{1mp3rs0n4t4_g17_345y_02a39618}
To ssh://foggy-cliff.picoctf.net:53071/git/challenge.git
   b4b49f2..f9bbe98  master -> master
```

Le serveur confirme lui-même la logique du challenge dans sa réponse : `Author matched and flag.txt found in commit` — il n'a vérifié que deux choses, la présence du fichier `flag.txt`, et la correspondance entre le nom/email déclaré et `root:root@picoctf`.

🏁 **Flag obtenu : `picoCTF{1mp3rs0n4t4_g17_345y_02a39618}`**

## 🛠️ Commandes clés

| Commande | Rôle |
| -------- | ---- |
| `git clone ssh://...` | Récupérer une copie locale du dépôt distant via SSH |
| `git config user.name "..."` | Déclarer localement le nom d'auteur utilisé pour les prochains commits (aucune vérification d'identité) |
| `git config user.email "..."` | Déclarer localement l'email d'auteur associé aux commits |
| `git add .` | Ajouter les fichiers modifiés/créés à l'index (préparation du prochain commit) |
| `git commit -m "..."` | Créer un commit avec l'identité actuellement configurée |
| `git push` | Envoyer les commits locaux vers le dépôt distant |

## 🧠 Ce que je retiens

- L'identité d'auteur dans Git (`user.name` / `user.email`) est une **métadonnée déclarative locale**, pas un mécanisme d'authentification — n'importe qui peut s'attribuer n'importe quel nom ou email sans preuve. L'authentification réelle sur un dépôt se fait à un tout autre niveau (clé SSH, mot de passe, jeton d'accès), complètement indépendant de ce champ.
- Ce challenge illustre un vrai piège de conception côté serveur : **faire confiance à une donnée fournie par le client** (ici, l'auteur du commit) pour prendre une décision de sécurité (donner un flag/accès) est une mauvaise pratique — la même logique s'applique à d'autres contextes (en-têtes HTTP, champs de formulaire, etc., qui ne doivent jamais être la seule source de vérité pour une autorisation).
- Réflexe utile pour tout challenge "General Skills" impliquant Git : toujours commencer par lire attentivement le `README.md` du dépôt, il contient très souvent la règle exacte que le serveur applique côté vérification.

---

*Prochain writeup bientôt — la suite de la progression picoCTF arrive !*
