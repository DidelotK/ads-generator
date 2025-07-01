# Générateur de Prompts d'Images

## Fonctionnalités

- 🎨 **Styles multiples** : Réaliste, photographique, artistique, commercial, lifestyle, dramatique, etc.
- 🤖 **Modèles IA** : Support de GPT-3.5 Turbo et GPT-4
- 📊 **Gestion des coûts** : Calcul automatique des coûts d'API
- 💾 **Sauvegarde automatique** : Les prompts sont sauvegardés en JSON
- 🔧 **Validation robuste** : Parsing Pydantic avec fallback manuel
- 🌍 **Support multilingue** : Génération en français par défaut
- 📝 **Prompts textuels directs** : Format prêt à l'emploi pour les générateurs d'images
- 🛡️ **Contraintes de réalisme** : Évite les anomalies anatomiques et éléments impossibles

## Installation

Le générateur est inclus dans le package principal. Assurez-vous d'avoir configuré votre clé API OpenAI :

```bash
# Dans votre fichier .env
OPENAI_API_KEY=votre_clé_api_openai
```

## Utilisation

### Script principal

```bash
# Génération simple
python prompt_generator.py "Mon hook" "Ma description"

# Avec style spécifique
python prompt_generator.py "Factures en baisse" "Économisez sur vos factures" --style realistic --num 3

# Avec modèle GPT-4
python prompt_generator.py "Technologie révolutionnaire" "Découvrez notre méthode" --style commercial --model gpt-4

# Génération multi-styles
python prompt_generator.py "Secret révélé" "Ce que l'état cache" --multi-style

# Lister les styles disponibles
python prompt_generator.py --list-styles

# Lister les modèles disponibles
python prompt_generator.py --list-models
```

### Utilisation en Python

```python
from src.generators.prompt_generator import PromptGenerator

# Initialiser le générateur
generator = PromptGenerator()

# Générer des prompts
prompts = generator.generate_prompts(
    hook="Factures en baisse, pouvoir d'achat en hausse",
    description="Augmentez votre pouvoir d'achat en adoptant notre méthode révolutionnaire",
    num_prompts=3,
    style="realistic",
    model="gpt-3.5-turbo"
)

# Utiliser directement le prompt pour générer une image
for prompt_data in prompts:
    prompt_text = prompt_data['prompt']  # Prompt textuel direct
    print(f"Prompt: {prompt_text}")
    # Utiliser prompt_text avec DALL-E, Midjourney, etc.

# Générer pour plusieurs styles
all_prompts = generator.generate_multiple_styles(
    hook="Mon hook",
    description="Ma description",
    styles=["realistic", "commercial", "artistic"],
    num_prompts=2
)
```

## Styles disponibles

| Style | Description |
|-------|-------------|
| `realistic` | Style photographique ultra-réaliste, haute qualité, détails nets |
| `photographic` | Photographie professionnelle, éclairage naturel, couleurs authentiques |
| `artistic` | Style artistique créatif, composition unique, couleurs expressives |
| `commercial` | Style publicitaire moderne, composition impactante, couleurs vives |
| `lifestyle` | Style lifestyle authentique, scènes quotidiennes, éclairage doux |
| `dramatic` | Style dramatique, éclairage contrasté, émotions intenses |
| `minimalist` | Style minimaliste, composition épurée, couleurs sobres |
| `vibrant` | Style vibrant, couleurs éclatantes, énergie positive |
| `professional` | Style professionnel, composition équilibrée, couleurs harmonieuses |
| `emotional` | Style émotionnel, éclairage doux, atmosphère chaleureuse |

## Modèles disponibles

| Modèle | Description | Coût entrée | Coût sortie |
|--------|-------------|-------------|-------------|
| `gpt-3.5-turbo` | Modèle rapide et économique | $0.0015/1K tokens | $0.002/1K tokens |
| `gpt-4` | Modèle le plus avancé | $0.030/1K tokens | $0.060/1K tokens |

## Format des prompts générés

### Structure JSON (pour sauvegarde)

```json
{
  "prompt": "Description détaillée pour générer l'image",
  "style": "Style d'image utilisé",
  "elements": ["élément 1", "élément 2", "élément 3"],
  "description": "Description de l'approche visuelle"
}
```

### Prompt textuel direct (pour utilisation)

Le générateur produit des **prompts textuels directs** prêts à être utilisés avec n'importe quel générateur d'images :

```
Une image mettant en scène une famille souriante autour d'une table, en train de regarder des factures d'énergie et des relevés de dépenses. Le père, la mère et l'enfant semblent surpris et heureux en découvrant des économies réalisées. En arrière-plan, des ampoules LED, des panneaux solaires et des appareils électroménagers économes en énergie renforcent le message de réduction des factures. L'ambiance est chaleureuse et conviviale, reflétant le bien-être financier que procure l'adoption de la méthode proposée.
```

## Contraintes de réalisme intégrées

Chaque prompt généré inclut automatiquement des contraintes pour assurer la qualité :

- ✅ **Pas de texte** sur l'image (titre/description déjà affichés sur Facebook)
- ✅ **Pas d'anomalies anatomiques** (humains avec 3 mains, etc.)
- ✅ **Pas d'éléments flottants** ou impossibles
- ✅ **Composition équilibrée** et professionnelle
- ✅ **Éclairage naturel** et cohérent
- ✅ **Couleurs harmonieuses** et réalistes
- ✅ **Détails nets** et précis
- ✅ **Qualité photographique** professionnelle

## Fichiers de sortie

Les prompts sont sauvegardés dans `generated/prompts/` avec le format :
```
prompts_YYYYMMDD_HHMMSS_style_model.json
```

Exemple de contenu :
```json
{
  "metadata": {
    "hook": "Factures en baisse, pouvoir d'achat en hausse",
    "style": "realistic",
    "model": "gpt-3.5-turbo",
    "generated_at": "2024-01-15T10:30:00",
    "num_prompts": 3
  },
  "prompts": [
    {
      "prompt": "Une image mettant en scène une famille souriante...",
      "style": "realistic",
      "elements": ["facture", "table", "ampoule", "énergie", "panneau"],
      "description": "Prompt 1 généré automatiquement"
    }
  ]
}
```

## Exemples d'utilisation

### Exemple 1 : Génération simple

```python
from src.generators.prompt_generator import PromptGenerator

generator = PromptGenerator()

prompts = generator.generate_prompts(
    hook="Factures en baisse, pouvoir d'achat en hausse",
    description="Augmentez votre pouvoir d'achat en adoptant notre méthode révolutionnaire pour diminuer vos factures énergétique et dépenser moins au quotidien.",
    num_prompts=2,
    style="realistic"
)

for i, prompt in enumerate(prompts, 1):
    print(f"Prompt {i}:")
    print(f"  Style: {prompt['style']}")
    print(f"  Prompt: {prompt['prompt']}")  # Prompt textuel direct
    print(f"  Éléments: {', '.join(prompt['elements'])}")
    print(f"  Description: {prompt['description']}")
    print()
```

### Exemple 2 : Utilisation directe avec DALL-E

```python
from src.generators.prompt_generator import PromptGenerator
from src.generators.image_generator import ImageGenerator

# Générer les prompts
prompt_gen = PromptGenerator()
prompts = prompt_gen.generate_prompts(hook, description, style="realistic")

# Générer les images
image_gen = ImageGenerator()
for prompt_data in prompts:
    # Utiliser directement le prompt textuel
    image_path = image_gen.generate_image(prompt_data['prompt'])
    print(f"Image générée: {image_path}")
```

### Exemple 3 : Utilisation avec Midjourney

```python
prompts = generator.generate_prompts(hook, description, style="artistic")

for prompt_data in prompts:
    # Format pour Midjourney
    midjourney_prompt = f"{prompt_data['prompt']} --ar 1:1 --v 6"
    print(f"Midjourney: /imagine {midjourney_prompt}")
```

## Tests

Exécutez les tests avec :

```bash
python -m unittest tests/test_prompt_generator.py
```

## Intégration avec le générateur d'images

Les prompts générés peuvent être utilisés directement avec le générateur d'images existant :

```python
from src.generators.prompt_generator import PromptGenerator
from src.generators.image_generator import ImageGenerator

# Générer les prompts
prompt_gen = PromptGenerator()
prompts = prompt_gen.generate_prompts(hook, description, style="realistic")

# Générer les images
image_gen = ImageGenerator()
for prompt in prompts:
    # Utiliser le prompt textuel directement
    image = image_gen.generate_image(prompt["prompt"])
    # Sauvegarder ou utiliser l'image
```

## Personnalisation

### Ajouter un nouveau style

1. Ajoutez le style dans l'énumération `PromptStyle`
2. Ajoutez la description dans `get_style_prompts()`
3. Mettez à jour `get_default_styles()` si nécessaire

### Modifier le template de base

Éditez le fichier `prompts/energy.md` pour modifier le template utilisé par défaut.

### Modifier les contraintes de réalisme

Les contraintes sont définies dans la méthode `generate_prompts()`. Vous pouvez les personnaliser selon vos besoins.

## Dépannage

### Erreur de clé API
```
❌ Erreur de configuration: Clé API OpenAI requise
```
**Solution** : Définissez `OPENAI_API_KEY` dans votre fichier `.env`

### Erreur de parsing
```
⚠️  Erreur de validation Pydantic, tentative de parsing manuel...
```
**Solution** : Le générateur utilise automatiquement un fallback de parsing manuel

### Style non supporté
```
⚠️  Style 'invalid_style' non supporté. Utilisation du style par défaut: realistic
```
**Solution** : Utilisez un style valide de la liste des styles disponibles

### Prompt trop générique
**Solution** : Utilisez un style plus spécifique ou modifiez le template de base dans `prompts/energy.md` 