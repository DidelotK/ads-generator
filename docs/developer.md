# 👨‍💻 Guide Développeur

Guide complet pour les développeurs souhaitant contribuer au projet ou comprendre son architecture.

## 🚀 Installation

### Prérequis
- **Python 3.13+** : Le projet nécessite Python 3.13 ou supérieur
- **uv** : Gestionnaire de paquets Python moderne
- **Git** : Pour la gestion de version

### Installation de uv
```bash
# Installation sur Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Installation sur Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Vérifier l'installation
uv --version
```

### Configuration du projet
```bash
# Cloner le repository
git clone <repository-url>
cd ads-generator

# Installer les dépendances
uv sync

# Configurer l'environnement
cp .env.example .env
# Éditer .env avec votre clé API OpenAI
```

### Variables d'environnement
Créez un fichier `.env` à la racine du projet :

```env
# Clé API OpenAI (requise)
OPENAI_API_KEY=sk-your-api-key-here

# Configuration optionnelle
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7

# Configuration des logs
LOG_LEVEL=INFO
DEBUG_MODE=false
```

### Architecture des modules

#### `src/generators/`
- **hook_generator.py** : Classe `HookGenerator` pour la génération d'accroches
- **image_generator.py** : Classe `ImageGenerator` pour la génération d'images

#### `src/marketing_config.py`
- Configuration des styles d'accroches
- Configuration des modèles d'images
- Gestion des prompts et templates

#### Scripts principaux
- **hook_generator.py** : Interface CLI pour les accroches
- **image_generator.py** : Interface CLI pour les images

## 🛠️ Commandes Utiles

### Gestion des dépendances avec uv

```bash
# Installer toutes les dépendances
uv sync

# Ajouter une nouvelle dépendance
uv add package-name

# Ajouter une dépendance de développement
uv add --dev package-name

# Supprimer une dépendance
uv remove package-name

# Mettre à jour les dépendances
uv sync --upgrade

# Voir l'arbre des dépendances
uv tree

# Voir les dépendances obsolètes
uv tree --outdated
```

### Environnement virtuel

```bash
# Activer l'environnement virtuel
uv shell

# Exécuter une commande dans l'environnement
uv run python script.py

# Exécuter avec des variables d'environnement
uv run --env-file .env python script.py
```

### Tests

```bash
# Exécuter tous les tests
uv run python -m pytest tests/

# Exécuter un test spécifique
uv run python -m pytest tests/test_hook_generator.py

# Exécuter avec couverture
uv run python -m pytest tests/ --cov=src

# Exécuter en mode verbose
uv run python -m pytest tests/ -v
```

### Linting et formatage

```bash
# Vérifier le style du code
uv run ruff check .

# Formater le code
uv run ruff format .

# Vérifier les types
uv run mypy src/
```

### Développement

```bash
# Lancer en mode debug
uv run python -m pdb script.py

# Profiler le code
uv run python -m cProfile -o profile.stats script.py

# Analyser la mémoire
uv run python -m memory_profiler script.py
```

### Build et distribution

```bash
# Construire le package
uv run python -m build

# Publier sur PyPI (si configuré)
uv run python -m twine upload dist/*
```

## 🔧 Configuration du développement

### IDE recommandé
- **VS Code** avec les extensions Python
- **PyCharm** pour un environnement complet
- **Vim/Neovim** avec des plugins Python

### Extensions VS Code recommandées
```json
{
  "extensions": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.ruff",
    "ms-python.mypy-type-checker",
    "ms-python.pylint"
  ]
}
```

### Configuration Python
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"]
}
```

## 🧪 Tests

### Structure des tests
```
tests/
├── test_hook_generator.py        # Tests du générateur d'accroches
├── test_improvements.py          # Tests des améliorations
└── test_marketing_resources.py   # Tests des ressources marketing
```

### Exécution des tests
```bash
# Tests unitaires
uv run python -m pytest

# Tests avec couverture
uv run python -m pytest --cov=src --cov-report=html

# Tests en parallèle
uv run python -m pytest -n auto

# Tests d'intégration
uv run python -m pytest tests/ -m integration
```

### Écriture de tests
```python
import pytest
from src.generators.hook_generator import HookGenerator

class TestHookGenerator:
    def test_generate_hook_basic(self):
        generator = HookGenerator()
        result = generator.generate_hook("Test subject")
        assert result is not None
        assert len(result) > 0

    def test_generate_hook_with_style(self):
        generator = HookGenerator()
        result = generator.generate_hook("Test subject", style="urgent")
        assert "urgent" in result.lower() or "limited" in result.lower()
```

## 📦 Gestion des versions

### Versioning sémantique
Le projet suit le versioning sémantique (SemVer) :
- **MAJOR** : Changements incompatibles
- **MINOR** : Nouvelles fonctionnalités compatibles
- **PATCH** : Corrections de bugs compatibles

### Mise à jour de la version
```bash
# Mise à jour automatique avec bump2version
uv run bump2version patch  # 1.0.0 → 1.0.1
uv run bump2version minor  # 1.0.1 → 1.1.0
uv run bump2version major  # 1.1.0 → 2.0.0
```

## 🚀 Déploiement

### Environnements
- **Development** : Environnement local pour le développement
- **Staging** : Environnement de test avant production
- **Production** : Environnement de production

### Variables d'environnement par environnement
```bash
# Development
cp .env.example .env.development

# Staging
cp .env.example .env.staging

# Production
cp .env.example .env.production
```

## 🐛 Debugging

### Logs
```python
import logging

# Configuration des logs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.debug("Message de debug")
logger.info("Message d'information")
logger.warning("Avertissement")
logger.error("Erreur")
```

### Debug avec pdb
```python
import pdb

def fonction_complexe():
    # Code complexe...
    pdb.set_trace()  # Point d'arrêt
    # Suite du code...
```

### Debug avec ipdb (plus avancé)
```bash
# Installer ipdb
uv add --dev ipdb

# Utilisation
import ipdb; ipdb.set_trace()
```

## �� Ressources supplémentaires

- [Documentation Python](https://docs.python.org/)
- [Documentation uv](https://docs.astral.sh/uv/)
- [Documentation pytest](https://docs.pytest.org/)
- [Documentation OpenAI API](https://platform.openai.com/docs)
- [Guide de style Python (PEP 8)](https://peps.python.org/pep-0008/)
