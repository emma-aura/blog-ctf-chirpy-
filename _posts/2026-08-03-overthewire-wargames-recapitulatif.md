---
title: "Wargames OverTheWire — Récapitulatif & Progression"
date: 2026-08-03 00:00:00 +0100
categories: [CTF, Wargame]
tags: [overthewire, wargame, linux, bandit, leviathan, reverse, progression]
pin: true
image:
  path: /assets/img/posts/domokitten.png
  alt: Domokitten
---

> Ce post est un index vivant de ma progression sur les **wargames OverTheWire** — une suite de challenges Linux qui couvre tout, de la prise en main du shell jusqu'au reverse engineering et à l'exploitation binaire. Chaque ligne ci-dessous pointe vers le writeup complet correspondant.
{: .prompt-tip }

---

## 🏰 Qu'est-ce qu'OverTheWire ?

[OverTheWire](https://overthewire.org/wargames/) est un ensemble de **wargames** — des jeux de guerre, version cybersécurité — accessibles en SSH, où chaque niveau donne accès au suivant une fois résolu. Contrairement aux CTF ponctuels, on y progresse à son rythme, et chaque wargame a sa thématique :

| Wargame | Thématique | Difficulté |
|---------|-----------|------------|
| **Bandit** | Fondamentaux Linux & commandes | Débutant |
| **Leviathan** | Reverse engineering & binaires setuid | Intermédiaire |
| **Natas** | Web (inspiré de l'ancien HackThisSite) | Intermédiaire |
| **Narnia** | Exploitation binaire (buffer overflow) | Avancé |
| **Behemoth** | Exploitation binaire + scripting | Avancé |
| **Krypton** | Cryptographie | Intermédiaire |
| **Utumno** | Exploitation binaire (très corsé) | Expert |
| **Maze** | Exploitation binaire (le plus dur) | Expert |

---

## ✅ Wargames couverts sur ce blog

### 🐚 Bandit — Complet (niveaux 0 → 33) 🏆

> [**Solution du Wargame Bandit**]({% post_url 2026-07-25-bandit-overthewire %}) — publié le 25/07/2026

Le point de départ idéal : **34 niveaux** (de 0 à 33) qui balaient les fondamentaux de Linux.

**Connexion** : `ssh -p 2220 bandit0@bandit.labs.overthewire.org` (mot de passe : `bandit0`)

| Bloc de niveaux | Compétences acquises |
|-----------------|----------------------|
| 0 → 6 | SSH, `ls`, `cat`, fichiers cachés, `file`, `find` |
| 7 → 13 | `grep`, `sort`/`uniq`, regex, base64, ROT13, compression |
| 13 → 18 | Clés SSH, `nc`, TLS/`openssl`, `nmap`, `diff` |
| 19 → 26 | Binaires SUID, client-serveur, cron, bruteforce, shell escapes |
| 27 → 33 | Git (objet, historique, branches, tags, hooks), expansion du shell |

**Leçons marquantes** : magic bytes, cryptographie asymétrique, escalade de privilèges, et le fameux *uppercase shell* du boss final.

---

### 🐉 Leviathan — Complet (niveaux 0 → 7) 🏆

> [**Solution du Wargame Leviathan**]({% post_url 2026-08-01-leviathan-overthewire %}) — publié le 01/08/2026

8 niveaux orientés **reverse engineering** : chaque niveau repose sur un binaire setuid à comprendre avant de le casser.

**Connexion** : `ssh -p 2223 leviathan0@leviathan.labs.overthewire.org` (mot de passe : `leviathan0`)

| Niveau | Compétence clé |
|--------|----------------|
| 0 → 1 | Fouille de fichiers & `grep` |
| 1 → 2 | Reverse : `ltrace` / mot de passe en clair |
| 2 → 3 | TOCTOU : `access()` vs `cat`, symlink + espace |
| 3 → 4 | Leurres & comparaison |
| 4 → 5 | Encodage binaire → ASCII |
| 5 → 6 | Symlink & lecture arbitraire |
| 6 → 7 | Bruteforce + rate-limiting |

**Leçons marquantes** : UID réel vs effectif, little-endian, `ltrace` vs `strace`, registres CPU — le pont parfait entre Bandit et les vrais challenges de pwn.

---

## 🧭 Progression conseillée

Pour les nouveaux arrivants, voici l'ordre que je recommande — c'est aussi ma propre roadmap :

```text
1. Bandit        ✅ (fait)
2. Leviathan     ✅ (fait)
3. Natas         ⬜ (web — à venir)
4. Krypton       ⬜ (crypto — à venir)
5. Narnia        ⬜ (exploitation binaire — à venir)
6. Behemoth      ⬜ (scripting + exploitation — à venir)
7. Utumno / Maze ⬜ (le graal — plus tard !)
```

---

## 📊 Mon bilan après Bandit + Leviathan

| Domaine | Ce que je maîtrise maintenant |
|---------|-------------------------------|
| **Shell & Linux** | Navigation, permissions, redirections, pipelines, `find`/`grep`/`xargs` |
| **Reverse engineering** | `ltrace`, `strace`, `strings`, magic bytes, little-endian |
| **Sécurité système** | SUID, cron, symlinks, TOCTOU, escalade de privilèges |
| **Réseau** | `nc`, TLS, `nmap`, sockets TCP |
| **Git** | Objets, historique, reflog, branches, tags, hooks |
| **Python** | Scripts de décodage, regex, exploitation rapide |

Les wargames OverTheWire sont la meilleure école que je connaisse : **on apprend en cassant**, et chaque niveau résolu devient un réflexe de plus pour les CTF réels.

---

## 📚 Ressources liées

- [OverTheWire — Wargames](https://overthewire.org/wargames/) — le site officiel
- [Writeup Leviathan (hrbrtschmu1l)](https://hrbrtschmu1l.medium.com/leviathan-overthewire-wargame-writeup-dd3378a6136a) — la source d'inspiration de mon writeup Leviathan
- [Page Ressources du blog]({% link _tabs/ressources.md %}) — mes ressources soigneusement sélectionnées

*Ce post sera mis à jour à chaque nouveau wargame terminé — reste connecté !* 🚀
