# 🚀 Installation

Ce guide vous accompagne dans l'installation et la configuration du générateur d'images avec l'API OpenAI.

## Option 1: Configuration automatique

La méthode la plus simple pour configurer le projet :

```bash
./scripts/setup.sh
```

Ce script automatise l'ensemble du processus d'installation.

## Option 2: Configuration manuelle

Si vous préférez une installation manuelle, suivez ces étapes :

### 1. Installer uv

**macOS avec Homebrew :**
```bash
brew install uv
```

**Ou avec curl :**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Installer les dépendances

```bash
uv sync
```


### 3. Configurer l'API OpenAI

1. **Créer le fichier de configuration :**
   - Créez un fichier `.env` à la racine du projet

2. **Ajouter votre clé API :**
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```

3. **Obtenir votre clé API :**
   - Rendez-vous sur [OpenAI Platform](https://platform.openai.com/api-keys)
   - Créez une nouvelle clé API
   - Copiez-la dans votre fichier `.env`

## 🔧 Vérification de l'installation

Pour vérifier que tout fonctionne correctement :

```bash
# Vérifier que uv est installé
uv --version

# Vérifier que les dépendances sont installées
uv tree

# Tester la génération d'une image simple
uv run python image_generator.py --list-models
```

## 🛠️ Commandes uv utiles

```bash
# Installer les dépendances
uv sync

# Ajouter une nouvelle dépendance
uv add package-name

# Ajouter une dépendance de développement
uv add --dev package-name

# Activer l'environnement virtuel
uv shell

# Exécuter un script
uv run python script.py

# Voir les dépendances installées
uv tree
```

## ⚠️ Prérequis

- **Python 3.13+** : Le projet nécessite Python 3.13 ou supérieur
- **Connexion internet** : Pour télécharger les dépendances et utiliser l'API OpenAI
- **Compte OpenAI** : Avec une clé API valide

## 🐛 Dépannage

### Erreur "Clé API requise"
- Vérifiez que votre fichier `.env` contient `OPENAI_API_KEY=sk-...`
- Ou passez la clé directement : `--api-key sk-...`

### Erreur de connexion
- Vérifiez votre connexion internet
- Vérifiez que votre clé API est valide

### Erreur de quota
- Vérifiez votre quota OpenAI sur le dashboard

### Problèmes avec uv
- Vérifiez que uv est installé : `uv --version`
- Réinstallez les dépendances : `uv sync --reinstall`
- Nettoyez le cache : `uv cache clean`

### Python version
- Vérifiez votre version Python : `python --version`
- Le projet nécessite Python 3.13 ou supérieur 