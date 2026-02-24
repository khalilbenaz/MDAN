# MDAN — Référence CLI

> Documentation complète des commandes de l'interface en ligne de commande MDAN v2.2.0

---

## Installation

### Option 1 : npm (Recommandé)

```bash
npm install -g mdan
```

**Avantages:**
- Mise à jour facile (`npm update -g mdan`)
- Fonctionne sur tous les OS (macOS, Linux, Windows)
- Gestion automatique du PATH

### Option 2 : npx (Sans installation)

```bash
npx mdan init mon-projet
```

**Avantages:**
- Pas d'installation globale
- Toujours la dernière version
- Idéal pour usage ponctuel

### Option 3 : Script d'installation

```bash
curl -fsSL https://raw.githubusercontent.com/khalilbenaz/MDAN/main/install.sh | bash
```

**Ce que fait le script:**
1. Crée `~/.mdan/` avec tous les fichiers MDAN
2. Crée `~/.local/bin/mdan` (exécutable)
3. Affiche les instructions pour ajouter au PATH

**Après installation, ajoutez au PATH:**
```bash
# Pour Bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Pour Zsh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Option 4 : Installation manuelle

```bash
git clone https://github.com/khalilbenaz/MDAN.git
cd MDAN
bash install.sh
```

---

## Commandes

### `mdan init [nom]`

Crée un nouveau projet MDAN.

**Usage:**
```bash
mdan init mon-projet
mdan init          # nom par défaut: "my-project"
```

**Fichiers créés:**
```
mon-projet/
├── .mdan/
│   ├── orchestrator.md         # System prompt MDAN Core
│   ├── universal-envelope.md   # Format standard des agents
│   ├── agents/                 # Prompts des 9 agents
│   │   ├── product.md
│   │   ├── architect.md
│   │   ├── ux.md
│   │   ├── dev.md
│   │   ├── security.md
│   │   ├── test.md
│   │   ├── devops.md
│   │   ├── doc.md
│   │   └── learn.md
│   └── skills/                 # Skills disponibles
│
├── docs/
│   ├── PRD.md                  # Template PRD
│   ├── ARCHITECTURE.md         # Template architecture
│   ├── SECURITY-REVIEW.md      # Template revue sécurité
│   ├── TEST-PLAN.md            # Template plan de test
│   └── CHANGELOG.md            # Template changelog
│
├── .claude/
│   └── skills/                 # Pour Claude Code
│
├── .github/
│   └── copilot-instructions.md # Pour GitHub Copilot
│
├── .cursorrules                # Pour Cursor IDE
├── .windsurfrules              # Pour Windsurf IDE
└── README.md                   # README initial
```

**Après création:**
```bash
cursor mon-projet    # Ouvrir dans Cursor
# ou
windsurf mon-projet  # Ouvrir dans Windsurf
```

---

### `mdan attach [--rebuild]`

Ajoute MDAN à un projet existant.

**Usage:**
```bash
cd mon-projet-existant
mdan attach
```

**Mode Rebuild:**
```bash
cd mon-projet-existant
mdan attach --rebuild
```

Le mode `--rebuild` ajoute des instructions pour analyser le code existant et proposer une réécriture from scratch.

**Fichiers créés/mis à jour:**
```
.mdan/
├── orchestrator.md
├── universal-envelope.md
├── agents/
└── skills/

.cursorrules        # Créé ou écrasé
.windsurfrules      # Créé ou écrasé
.claude/skills/     # Créé
.github/copilot-instructions.md
```

**Après attach:**
```bash
cursor .    # Ouvrir le projet dans Cursor
```

Puis dans l'IDE, utiliser le prompt:
```
MDAN: Analyse ce projet et propose des améliorations.
```

Ou en mode rebuild:
```
MDAN REBUILD: Analyse tout le code existant, documente 
chaque feature, et propose une architecture moderne.
```

---

### `mdan status`

Affiche le statut du projet courant.

**Usage:**
```bash
cd mon-projet
mdan status
```

**Sortie si MDAN actif:**
```
✅ MDAN is active in this project

[Contenu de .mdan/STATUS.md si existant]
```

**Sortie si MDAN non installé:**
```
No MDAN project here.
  Run: mdan init [name]  or  mdan attach
```

---

### `mdan phase [1-5]`

Affiche le guide détaillé d'une phase.

**Usage:**
```bash
mdan phase 1    # DISCOVER
mdan phase 2    # DESIGN
mdan phase 3    # BUILD
mdan phase 4    # VERIFY
mdan phase 5    # SHIP
```

**Exemple de sortie (Phase 1):**
```
# MDAN Phase 1 — DISCOVER

> Goal: Deeply understand the user's need before touching any solution.
> Agents: Product Agent
> Output: Validated PRD

## The 5 Essential Discovery Questions
[...]
```

---

### `mdan agent [nom]`

Affiche le prompt complet d'un agent.

**Usage:**
```bash
mdan agent product    # Agent Product
mdan agent architect  # Agent Architect
mdan agent ux         # Agent UX
mdan agent dev        # Agent Dev
mdan agent security   # Agent Security
mdan agent test       # Agent Test
mdan agent devops     # Agent DevOps
mdan agent doc        # Agent Doc
mdan agent learn      # Agent Learn
```

**Exemple de sortie:**
```
[MDAN-AGENT]
NAME: Dev Agent
VERSION: 2.0.0
ROLE: Senior Full-Stack Developer...
[...]
```

**Utilisation:**
- Copier le prompt pour l'utiliser dans un autre LLM
- Comprendre le rôle et les contraintes d'un agent
- Déboguer le comportement d'un agent

---

### `mdan skills`

Liste les skills disponibles.

**Usage:**
```bash
mdan skills
```

**Sortie:**
```
Skills:
  find-skills
  [... autres skills installés]
```

---

### `mdan version`

Affiche la version de MDAN.

**Usage:**
```bash
mdan version
mdan -v
```

**Sortie:**
```
MDAN v2.2.0
```

---

### `mdan help`

Affiche l'aide complète.

**Usage:**
```bash
mdan help
mdan --help
mdan -h
mdan          # Sans argument = help
```

**Sortie:**
```
  ███╗   ███╗██████╗  █████╗ ███╗   ██╗
  ████╗ ████║██╔══██╗██╔══██╗████╗  ██║
  ██╔████╔██║██║  ██║███████║██╔██╗ ██║
  ██║╚██╔╝██║██║  ██║██╔══██║██║╚██╗██║
  ██║ ╚═╝ ██║██████╔╝██║  ██║██║ ╚████║
  ╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝

  Multi-Agent Development Agentic Network v2.2.0

USAGE
  mdan <command> [options]

COMMANDS
  init [name]              Create a new project
  attach [--rebuild]       Add MDAN to existing project
  status                   Show project status
  phase [1-5]              Show phase guide
  agent [name]             Show agent prompt
  skills                   List available skills
  version                  Show version

EXAMPLES
  mdan init my-app              # New project
  cd my-project && mdan attach  # Existing project
  mdan attach --rebuild         # Rebuild from scratch

AGENTS
  product, architect, ux, dev, test, security, devops, doc
```

---

## Workflows Courants

### Nouveau projet

```bash
# 1. Créer le projet
mdan init mon-app

# 2. Ouvrir dans l'IDE
cursor mon-app

# 3. Dans l'IDE, commencer avec:
MDAN: Je veux créer une app de [description].
Commence par DISCOVER.
```

### Projet existant

```bash
# 1. Aller dans le projet
cd mon-projet

# 2. Attacher MDAN
mdan attach

# 3. Ouvrir dans l'IDE
cursor .

# 4. Dans l'IDE, commencer avec:
MDAN: Analyse ce projet et identifie les améliorations possibles.
```

### Rebuild complet

```bash
# 1. Aller dans le projet
cd mon-projet

# 2. Attacher MDAN en mode rebuild
mdan attach --rebuild

# 3. Ouvrir dans l'IDE
cursor .

# 4. Dans l'IDE, commencer avec:
MDAN REBUILD: Analyse tout le code existant, documente 
chaque feature, et propose une architecture moderne 
pour tout réécrire from scratch.
```

### Consulter une phase

```bash
# Voir le guide de la phase actuelle
mdan phase 3

# Voir le prompt de l'agent actif
mdan agent dev
```

---

## Fichiers de Configuration

### `.cursorrules`

Généré par `mdan init` et `mdan attach`.

Contenu:
- `orchestrator.md` complet
- Instructions spécifiques Cursor
- Chemins vers les agents et skills

### `.windsurfrules`

Identique à `.cursorrules` mais pour Windsurf IDE.

### `.github/copilot-instructions.md`

Instructions pour GitHub Copilot. Copie de `orchestrator.md`.

### `.claude/skills/`

Skills copiés depuis `skills/` pour Claude Code CLI.

---

## Dépannage

### Commande `mdan` non trouvée

**Problème:**
```
bash: mdan: command not found
```

**Solution 1 (npm):**
```bash
npm install -g mdan
```

**Solution 2 (script):**
```bash
# Vérifier le PATH
echo $PATH

# Ajouter si manquant
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Permission refusée

**Problème:**
```
bash: /home/user/.local/bin/mdan: Permission denied
```

**Solution:**
```bash
chmod +x ~/.local/bin/mdan
```

### Version obsolète

**Vérifier la version:**
```bash
mdan version
```

**Mettre à jour (npm):**
```bash
npm update -g mdan
```

**Mettre à jour (script):**
```bash
curl -fsSL https://raw.githubusercontent.com/khalilbenaz/MDAN/main/install.sh | bash
```

### Fichiers non générés

**Problème:** `mdan init` ne crée pas tous les fichiers.

**Diagnostic:**
```bash
ls -la mon-projet/.mdan/
```

**Solution:** Vérifier que le dossier MDAN source existe:
```bash
ls -la ~/.mdan/           # Installation script
ls -la node_modules/mdan/ # Installation npm
```

---

## Variables d'Environnement

| Variable | Défaut | Description |
|----------|--------|-------------|
| `MDAN_DIR` | `~/.mdan` | Dossier d'installation (script) |
| `PATH` | - | Doit inclure `~/.local/bin` |

---

## Alias Utiles

Ajoutez à `~/.bashrc` ou `~/.zshrc`:

```bash
# Raccourcis MDAN
alias mi='mdan init'
alias ma='mdan attach'
alias ms='mdan status'
alias mp='mdan phase'
alias mag='mdan agent'

# Workflow rapide
mdan-new() {
    mdan init "$1" && cursor "$1"
}

mdan-attach() {
    mdan attach && cursor .
}
```

---

## Sortie JSON (Programmatique)

Actuellement, la CLI ne supporte pas la sortie JSON. Pour un usage programmatique:

```bash
# Récupérer la version
mdan version | grep -oP 'v[\d.]+'

# Vérifier si MDAN actif
mdan status | grep -q "active" && echo "OK" || echo "NO"

# Lister les agents
ls ~/.mdan/agents/*.md | xargs -n1 basename | sed 's/.md$//'
```
