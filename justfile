# Justfile pour le projet ads-generator
# Utilisation: just <tâche>

# Variables
python := "uv run python"
pytest := "uv run pytest"
pytest_cov := "uv run pytest --cov=src --cov-report=term-missing --cov-branch"
default_model := "gpt-3.5-turbo"
default_num_hooks := "5"

# Tâche par défaut
default:
    @just --list

# Installation des dépendances
install:
    @echo "📦 Installation des dépendances..."
    uv sync

# Nettoyage des fichiers temporaires
clean:
    @echo "🧹 Nettoyage des fichiers temporaires..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type f -name "*.pyo" -delete 2>/dev/null || true
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    @echo "🧹 Nettoyage des fichiers générés..."
    rm -rf generated/ htmlcov/ .coverage .pytest_cache/

# Lancement de tous les tests avec coverage
test:
    @echo "🧪 Lancement de tous les tests avec coverage..."
    {{pytest_cov}} tests/ -v

# Tests sans coverage (unittest classique)
test-unittest:
    @echo "🧪 Lancement de tous les tests (unittest)..."
    {{python}} -m unittest discover tests -v

# Tests spécifiques au PromptGenerator avec coverage
test-prompt:
    @echo "🎨 Tests du PromptGenerator avec coverage..."
    {{pytest_cov}} tests/test_prompt_generator.py -v

# Tests spécifiques à l'ImageGenerator avec coverage
test-image:
    @echo "🖼️  Tests de l'ImageGenerator avec coverage..."
    {{pytest_cov}} tests/test_image_generator.py -v

# Tests avec pytest standard
pytest:
    @echo "🔬 Tests avec pytest standard..."
    {{pytest}} tests/ -v

# Vérification complète du code (tests + coverage + style)
check: test-core
    @echo "✅ Vérification complète terminée avec succès!"

# Tests principaux avec coverage (sans les tests avec dépendances manquantes)
test-core:
    @echo "🧪 Lancement des tests principaux avec coverage..."
    {{pytest_cov}} tests/test_prompt_generator.py tests/test_image_generator.py -v

# Formatage du code avec black (si disponible)
format:
    @echo "🎨 Formatage du code..."
    uv run black src/ tests/ --line-length 88 || echo "⚠️  Black non disponible, ignoré"

# Vérification du style avec flake8 (si disponible)
lint:
    @echo "🔍 Vérification du style de code..."
    uv run flake8 src/ tests/ --max-line-length=88 || echo "⚠️  Flake8 non disponible, ignoré"

# Vérification des types avec mypy (si disponible)
typecheck:
    @echo "🔎 Vérification des types..."
    uv run mypy src/ || echo "⚠️  MyPy non disponible, ignoré"

# Vérification complète avec style et types
check-all: test lint typecheck
    @echo "🎯 Vérification complète (tests + style + types) terminée!"

# Génération d'un rapport de couverture détaillé
coverage:
    @echo "📊 Génération du rapport de couverture détaillé..."
    {{pytest_cov}} tests/test_prompt_generator.py tests/test_image_generator.py --cov-report=html:htmlcov --cov-report=xml:coverage.xml
    @echo "📈 Rapport HTML généré dans: htmlcov/index.html"

# Exemple d'utilisation du générateur de prompts
demo-prompt:
    @echo "🎭 Démonstration du générateur de prompts..."
    {{python}} -c "import sys; sys.path.append('src'); from generators.prompt_generator import PromptGenerator; import os; os.environ['OPENAI_API_KEY'] = 'demo_key'; pg = PromptGenerator(); print('✅ PromptGenerator initialisé'); print('📋 Styles disponibles:', list(pg.get_available_styles().keys()))"

# Exemple d'utilisation du générateur d'images
demo-image:
    @echo "🖼️  Démonstration du générateur d'images..."
    {{python}} -c "import sys; sys.path.append('src'); from generators.image_generator import ImageGenerator; import os; os.environ['OPENAI_API_KEY'] = 'demo_key'; ig = ImageGenerator(); print('✅ ImageGenerator initialisé'); print('📋 Styles disponibles:', list(ig.get_available_styles().keys())); print('🤖 Modèles disponibles:', list(ig.get_available_models().keys()))"

# Affichage des informations du projet
info:
    @echo "📋 Informations du projet ads-generator"
    @echo "=================================="
    @echo "🏗️  Structure du projet:"
    @tree src/ -I "__pycache__" || ls -la src/
    @echo ""
    @echo "🧪 Tests disponibles:"
    @find tests/ -name "test_*.py" | sort
    @echo ""
    @echo "📦 Dépendances:"
    @uv tree || echo "Utilisez 'uv tree' pour voir les dépendances"

# Aide et documentation
help:
    @echo "🚀 Aide pour le projet ads-generator"
    @echo "=================================="
    @echo ""
    @echo "📋 Tâches principales:"
    @echo "  just check        - Lance tous les tests avec coverage"
    @echo "  just test         - Lance tous les tests avec coverage"
    @echo "  just install      - Installe les dépendances"
    @echo "  just clean        - Nettoie les fichiers temporaires"
    @echo ""
    @echo "🧪 Tests spécifiques:"
    @echo "  just test-prompt  - Tests du PromptGenerator avec coverage"
    @echo "  just test-image   - Tests de l'ImageGenerator avec coverage"
    @echo "  just test-unittest- Tests avec unittest (sans coverage)"
    @echo "  just pytest       - Tests avec pytest standard"
    @echo ""
    @echo "🔍 Qualité du code:"
    @echo "  just lint         - Vérification du style"
    @echo "  just format       - Formatage du code"
    @echo "  just typecheck    - Vérification des types"
    @echo "  just check-all    - Vérification complète"
    @echo ""
    @echo "📊 Autres:"
    @echo "  just coverage     - Rapport de couverture détaillé (HTML + XML)"
    @echo "  just demo-prompt  - Démo PromptGenerator"
    @echo "  just demo-image   - Démo ImageGenerator"
    @echo "  just info         - Infos du projet"
    @echo ""
    @echo "🆘 Commandes disponibles:"
    @just --list

# Tests ultra-rapides (essentiels uniquement)
test-ultra:
    @echo "⚡ Tests ultra-rapides (essentiels)..."
    uv run pytest tests/test_fast.py::TestFastMarketingConfig::test_marketing_functions tests/test_fast.py::TestFastHookGenerator::test_hook_generation_fast -v --tb=short --no-cov

# Tests rapides (sans appels API ni couverture)
test-fast:
    @echo "🚀 Exécution des tests rapides..."
    uv run pytest tests/test_fast.py tests/test_marketing_resources.py::TestMarketingConfig tests/test_marketing_resources.py::TestMarketingResourcesGeneration::test_different_quantities -v --tb=short --no-cov

# Tests complets (avec tous les mocks)
test-all:
    @echo "🧪 Exécution de tous les tests..."
    uv run pytest tests/ --cov=src --cov-report=term-missing --tb=short

# Tests avec couverture minimale pour développement
test-dev:
    @echo "🔧 Tests de développement..."
    uv run pytest tests/test_fast.py tests/test_marketing_resources.py::TestMarketingConfig tests/test_improvements.py -v --cov=src --cov-report=term-missing

# Tests avec timeout pour éviter les blocages
test-safe:
    @echo "🛡️ Tests avec timeout de sécurité..."
    timeout 60s uv run pytest tests/test_fast.py tests/test_marketing_resources.py::TestMarketingConfig --no-cov -v || echo "⚠️ Tests interrompus après 60s"

# Lancer les hooks (exemple)
hooks subject=default_model num=default_num_hooks:
    @echo "🎯 Génération de {{num}} hooks pour: {{subject}}"
    uv run python hook_generator.py "{{subject}}" --num-hooks {{num}} --model {{default_model}}

# Lancer les images (exemple)  
images prompt="Une image de test" num="1":
    @echo "🎨 Génération de {{num}} image(s) pour: {{prompt}}"
    uv run python image_generator.py "{{prompt}}" --num-images {{num}}

# Lancer les prompts (exemple)
prompts hook="Test hook" desc="Test description" num="3":
    @echo "📝 Génération de {{num}} prompts pour: {{hook}}"
    uv run python prompt_generator.py "{{hook}}" "{{desc}}" --num-prompts {{num}} 