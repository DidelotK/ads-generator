# 🚀 Workflow CI/CD - GitHub Actions

## 📋 Vue d'ensemble

Le projet `ads-generator` utilise GitHub Actions pour automatiser l'exécution des tests à chaque push de commit. Deux workflows sont disponibles :

## 🧪 Workflow principal : Tests (`tests.yml`)

### Déclenchement
- ✅ **Push sur toutes les branches** (`"**"`)
- ✅ **Pull requests** vers `main`, `master`, `develop`

### Actions réalisées
1. **📥 Checkout** du code source
2. **🐍 Configuration** de Python 3.13
3. **⚡ Installation** de `uv` (gestionnaire de packages)
4. **📦 Installation** de `just` (task runner)
5. **🔧 Installation** des dépendances avec `uv sync --dev`
6. **🧪 Exécution** des tests avec `just check`

### Commande exécutée
```bash
just check
```

Cette commande lance les tests principaux avec coverage selon la configuration du `justfile`.

## 🔧 Workflow complet : CI (`ci.yml`)

### Jobs parallèles
1. **🧪 Tests principaux** - Exécution de `just check`
2. **⚡ Tests rapides** - Exécution de `just test-ultra`
3. **🔍 Qualité du code** - Formatage, linting, vérification des types

### Fonctionnalités avancées
- **📊 Rapport de couverture** avec upload vers Codecov
- **🎨 Vérification du formatage** avec Black
- **🔍 Linting** avec Flake8
- **🔎 Vérification des types** avec MyPy

## 🛠️ Configuration technique

### Environnement
- **OS** : Ubuntu Latest
- **Python** : 3.13
- **Gestionnaire de packages** : `uv`
- **Task runner** : `just`

### Dépendances installées
```bash
uv sync --dev
```

Installe toutes les dépendances définies dans `pyproject.toml`, y compris les dépendances de développement.

## 📊 Tests exécutés

### Tests principaux (`just check`)
Basé sur la configuration du `justfile`, cette commande exécute :
```bash
# Tests principaux avec coverage
pytest tests/test_prompt_generator.py tests/test_image_generator.py --cov=src --cov-report=term-missing --cov-branch -v
```

### Tests rapides (`just test-ultra`)
```bash
# Tests essentiels ultra-rapides
pytest tests/test_fast.py::TestFastMarketingConfig::test_marketing_functions tests/test_fast.py::TestFastHookGenerator::test_hook_generation_fast -v --tb=short --no-cov
```

## 🔍 Surveillance et rapports

### Status badges
Vous pouvez ajouter des badges dans votre README :

```markdown
![Tests](https://github.com/VOTRE_USERNAME/ads-generator/workflows/🧪%20Tests/badge.svg)
![CI](https://github.com/VOTRE_USERNAME/ads-generator/workflows/CI%20-%20Tests%20automatisés/badge.svg)
```

### Logs et debugging
- Les logs sont disponibles dans l'onglet "Actions" de votre repository
- Chaque étape est détaillée avec emojis pour faciliter la lecture
- Les erreurs sont clairement identifiées

## ⚙️ Personnalisation

### Modifier les branches surveillées
Dans `.github/workflows/tests.yml` :
```yaml
on:
  push:
    branches: [ main, develop ]  # Branches spécifiques
```

### Ajouter des tests spécifiques
Dans le workflow, vous pouvez ajouter d'autres commandes `just` :
```yaml
- name: 🧪 Tests spécifiques
  run: |
    just test-prompt
    just test-image
```

### Variables d'environnement
Pour ajouter des variables d'environnement (comme des clés API de test) :
```yaml
env:
  PYTHON_VERSION: "3.13"
  TEST_API_KEY: ${{ secrets.TEST_API_KEY }}
```

## 🚨 Gestion des erreurs

### Échec des tests
- Le workflow s'arrête si `just check` échoue
- Les logs détaillent les tests qui ont échoué
- Le badge GitHub indique l'état (✅ ou ❌)

### Dépendances manquantes
- `uv sync --dev` installe automatiquement toutes les dépendances
- Le cache `uv` accélère les installations répétées

## 📈 Optimisations

### Cache
- **Cache uv** : Accélère l'installation des dépendances
- **Cache Python** : Réutilise l'environnement Python

### Parallélisation
- Les jobs s'exécutent en parallèle quand possible
- Tests rapides et qualité du code en parallèle

## 🔧 Maintenance

### Mise à jour des actions
Vérifiez régulièrement les versions des actions GitHub :
- `actions/checkout@v4`
- `actions/setup-python@v4`
- `astral-sh/setup-uv@v3`
- `extractions/setup-just@v2`

### Mise à jour Python
Pour changer la version Python, modifiez la variable `PYTHON_VERSION` dans les workflows.

## 📚 Ressources

- [Documentation GitHub Actions](https://docs.github.com/en/actions)
- [Documentation uv](https://docs.astral.sh/uv/)
- [Documentation Just](https://github.com/casey/just)
- [Documentation pytest](https://docs.pytest.org/)

## 🎯 Commandes locales équivalentes

Pour reproduire localement ce que fait le CI :

```bash
# Installation des dépendances
uv sync --dev

# Tests principaux
just check

# Tests rapides
just test-ultra

# Qualité du code
just format
just lint
just typecheck
```