# 🚀 Workflow CI/CD - GitHub Actions

## 📋 Vue d'ensemble

Le projet `ads-generator` utilise GitHub Actions avec une **architecture modulaire et réutilisable** pour automatiser l'exécution des tests à chaque push de commit. 

### 🏗️ Architecture modulaire

L'architecture suit le principe **DRY (Don't Repeat Yourself)** avec :

- **🔧 Action composite** (`.github/actions/setup-env/`) : Configuration réutilisable de l'environnement
- **🧪 Workflow réutilisable** (`.github/workflows/run-tests.yml`) : Template pour l'exécution de tests
- **📋 Workflows spécialisés** : `tests.yml` et `ci.yml` qui utilisent les composants réutilisables

### 🎯 Composants disponibles

## 🔧 Action composite : Setup Environment

**Fichier** : `.github/actions/setup-env/action.yml`

### Fonctionnalités
- ** Configuration Python** (version paramétrable, défaut 3.13)
- **⚡ Installation uv** avec cache intelligent
- **📦 Installation Just** (task runner)
- **🔧 Installation dépendances** avec `uv sync --dev`

### Paramètres
```yaml
inputs:
  python-version: '3.13'    # Version Python
  cache-key-suffix: 'default'  # Suffixe pour le cache
```

## 🧪 Workflow réutilisable : Run Tests

**Fichier** : `.github/workflows/run-tests.yml`

### Paramètres configurables
```yaml
inputs:
  test-command: "just check"      # Commande à exécuter
  job-name: "Tests"               # Nom du job
  python-version: "3.13"         # Version Python
  upload-coverage: false         # Upload couverture
  continue-on-error: false       # Continuer si erreur
```

### Utilisation
```yaml
jobs:
  my-tests:
    uses: ./.github/workflows/run-tests.yml
    with:
      test-command: "just check"
      job-name: "Tests principaux"
      upload-coverage: true
```

## 📋 Workflow principal : Tests (`tests.yml`)

### Déclenchement
- ✅ **Push sur toutes les branches** (`"**"`)
- ✅ **Pull requests** vers `main`, `master`, `develop`

### Configuration
```yaml
jobs:
  tests:
    uses: ./.github/workflows/run-tests.yml
    with:
      test-command: "just check"
      job-name: "Tests principaux"
      upload-coverage: true
```

## 🔧 Workflow complet : CI (`ci.yml`)

### Jobs parallèles
1. **🧪 Tests principaux** - `just check` avec couverture
2. **⚡ Tests rapides** - `just test-ultra` sans couverture
3. **🔍 Qualité du code** - `just format && just lint && just typecheck`

### Configuration
```yaml
jobs:
  tests:
    uses: ./.github/workflows/run-tests.yml
    with:
      test-command: "just check"
      upload-coverage: true
      
  tests-rapides:
    uses: ./.github/workflows/run-tests.yml
    with:
      test-command: "just test-ultra"
      upload-coverage: false
      
  qualite-code:
    uses: ./.github/workflows/run-tests.yml
    with:
      test-command: "just format && just lint && just typecheck"
      continue-on-error: true
```

## ✨ Avantages de l'architecture modulaire

### � DRY (Don't Repeat Yourself)
- **Zéro duplication** : Le code de configuration n'est écrit qu'une fois
- **Maintenance facilitée** : Un seul endroit à modifier pour tous les workflows
- **Cohérence garantie** : Tous les jobs utilisent la même configuration

### 🚀 Performance optimisée
- **Cache intelligent** : Cache différencié par job avec `cache-key-suffix`
- **Parallélisation maximale** : Jobs indépendants s'exécutent en parallèle
- **Réutilisation des layers** : Docker layers et dépendances mises en cache

### 🔧 Flexibilité maximale
- **Paramètres configurables** : Chaque workflow peut adapter les paramètres
- **Réutilisabilité** : Facile d'ajouter de nouveaux types de tests
- **Extensibilité** : Nouveaux workflows en quelques lignes

### 📊 Exemple d'ajout d'un nouveau test
```yaml
# Dans n'importe quel workflow
new-test:
  uses: ./.github/workflows/run-tests.yml
  with:
    test-command: "just mon-nouveau-test"
    job-name: "Mon nouveau test"
    python-version: "3.12"  # Version différente si besoin
```

## �🛠️ Configuration technique

### Environnement
- **OS** : Ubuntu Latest
- **Python** : 3.13 (configurable par workflow)
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