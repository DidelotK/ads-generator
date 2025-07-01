# 🧪 Guide des Tests - ads-generator

## Vue d'ensemble

Ce projet utilise `pytest` avec des mocks complets pour éviter les appels API réels pendant les tests. Plusieurs commandes sont disponibles selon vos besoins.

## ⚡ Commandes de Test Rapides

### `just test-fast` - Tests Ultra-Rapides (1-2 secondes)
```bash
just test-fast
```
- **Durée** : ~1.5 seconde
- **Couverture** : Désactivée (pour la vitesse)
- **Contenu** : Tests essentiels avec mocks complets
- **Usage** : Développement rapide, vérification avant commit

### `just test-safe` - Tests avec Timeout (max 60s)
```bash
just test-safe
```
- **Durée** : ~1.5 seconde (avec timeout de sécurité à 60s)
- **Couverture** : Désactivée
- **Contenu** : Mêmes tests que test-fast avec protection contre les blocages
- **Usage** : CI/CD, scripts automatisés

## 🔧 Commandes de Test pour le Développement

### `just test-dev` - Tests avec Couverture Minimale
```bash
just test-dev
```
- **Durée** : ~5-10 secondes
- **Couverture** : Activée avec rapport
- **Contenu** : Tests rapides + quelques tests d'intégration
- **Usage** : Vérification de couverture pendant le développement

### `just test-all` - Tests Complets
```bash
just test-all
```
- **Durée** : Variable (peut être long si mal mockés)
- **Couverture** : Complète avec rapport HTML
- **Contenu** : Tous les tests du projet
- **Usage** : Validation finale, release

## 📁 Structure des Tests

### `tests/test_fast.py` - Tests Ultra-Optimisés
- Tests avec mocks complets
- Aucun appel API réel
- Validation des fonctionnalités principales
- Classes testées :
  - `TestFastHookGenerator`
  - `TestFastMarketingConfig`

### `tests/test_marketing_resources.py` - Tests de Configuration
- Tests des fonctions utilitaires
- Pas d'appels API
- Validation des configurations marketing
- Classes testées :
  - `TestMarketingConfig`

### Autres fichiers de test
- `test_hook_generator.py` - Tests complets HookGenerator
- `test_image_generator.py` - Tests complets ImageGenerator  
- `test_prompt_generator.py` - Tests complets PromptGenerator
- `test_improvements.py` - Tests d'amélioration et intégration

## 🎯 Mocking et Performance

### Principes de Mock
```python
@patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
@patch('src.generators.hook_generator.openai.OpenAI')
def test_with_mock(self, mock_openai):
    # Mock complet de l'API OpenAI
    mock_client = Mock()
    mock_openai.return_value = mock_client
    
    # Mock de la réponse
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = '{"result": "test"}'
    mock_client.chat.completions.create.return_value = mock_response
```

### Éviter les Appels API Réels
- ✅ Toujours utiliser `@patch` pour `openai.OpenAI`
- ✅ Mocker `time.sleep()` pour les délais
- ✅ Mocker `requests.get()` pour les téléchargements
- ❌ Jamais d'appels API réels dans les tests

## 📊 Couverture de Code

### Configuration Actuelle
- **Seuil minimum** : 60% (configuration développement)
- **Objectif** : 80%+ (configuration production)
- **Outils** : pytest-cov avec rapports HTML

### Vérifier la Couverture
```bash
# Rapport terminal
just test-dev

# Rapport HTML détaillé
just test-all
open htmlcov/index.html
```

## 🚀 Workflow de Développement Recommandé

### 1. Développement Rapide
```bash
# Pendant le développement
just test-fast

# Vérification occasionnelle
just test-dev
```

### 2. Avant Commit
```bash
# Validation rapide
just test-safe

# Si tout va bien, validation complète
just test-all
```

### 3. CI/CD
```bash
# Tests avec timeout de sécurité
just test-safe
```

## 🔧 Dépannage

### Tests Lents
- **Problème** : Tests prennent plusieurs minutes
- **Cause** : Appels API réels non mockés
- **Solution** : Utiliser `just test-fast` ou ajouter des mocks

### Blocages de Tests
- **Problème** : Tests se bloquent indéfiniment  
- **Cause** : Appels API qui attendent une réponse
- **Solution** : Utiliser `just test-safe` avec timeout

### Couverture Insuffisante
- **Problème** : Couverture < 60%
- **Cause** : Tests ne couvrent pas assez de code
- **Solution** : Ajouter des tests dans `test_fast.py` ou réduire temporairement le seuil

### Erreurs d'Import
- **Problème** : `ModuleNotFoundError`
- **Cause** : Structure de projet ou imports manquants
- **Solution** : Vérifier les imports et la structure dans `src/`

## 📋 Checklist Qualité

### Avant chaque commit
- [ ] `just test-fast` passe en moins de 2 secondes
- [ ] Aucun appel API réel dans les nouveaux tests
- [ ] Mocks appropriés pour toutes les dépendances externes

### Avant chaque release
- [ ] `just test-all` passe avec couverture >= 80%
- [ ] Tous les tests sont rapides (< 30 secondes total)
- [ ] Documentation à jour

## 🎯 Objectifs de Performance

- **Tests ultra-rapides** : < 2 secondes
- **Tests de développement** : < 10 secondes
- **Tests complets** : < 30 secondes
- **Couverture minimum** : 60% (dev) / 80% (prod)

## 🔗 Ressources

- [pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Guide](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-cov Plugin](https://pytest-cov.readthedocs.io/)
- [Just Command Runner](https://just.systems/) 