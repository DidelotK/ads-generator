# Générateur d'Images avec l'API OpenAI

Ce module génère des images en utilisant l'API OpenAI (GPT-Image-1, DALL-E 2 et DALL-E 3). Il peut générer différents types d'images selon la description fournie dans le prompt.

**🎨 GPT-Image-1** est maintenant le modèle par défaut pour une qualité d'image supérieure !

## 🚀 Installation

Pour installer et configurer le projet, consultez notre [guide d'installation complet](installation.md).

## 🤖 Modèles disponibles

### Afficher les modèles et leurs tarifs
```bash
uv run python image_generator.py --list-models
```

### 🎨 GPT-Image-1 (par défaut - qualité supérieure)
- **Description** : Modèle d'image le plus récent d'OpenAI (remplace DALL-E)
- **Type** : Génération d'image directe
- **Tailles** : 1024x1024, 1024x1536, 1536x1024, auto
- **Qualités** : standard, hd
- **Tarifs** : $0.040-$0.120 USD par image
- **Avantages** : Qualité supérieure, meilleure résolution, prompts détaillés

### DALL-E 3 (haute qualité)
- **Description** : Modèle précédent d'OpenAI pour l'image
- **Type** : Génération d'image directe
- **Tailles** : 1024x1024, 1792x1024, 1024x1792
- **Qualités** : standard, hd
- **Tarifs** : $0.040-$0.120 USD par image

### DALL-E 2 (économique)
- **Description** : Ancien modèle d'OpenAI, moins cher
- **Type** : Génération d'image directe
- **Tailles** : 256x256, 512x512, 1024x1024
- **Qualités** : standard uniquement
- **Tarifs** : $0.016-$0.020 USD par image

## 📖 Utilisation

### Génération d'une image simple (chat par défaut)
```bash
uv run python image_generator.py
# ou
uv run chat-image-generator
```

### Génération avec un modèle spécifique
```bash
# Avec GPT-Image-1 (qualité supérieure - par défaut)
uv run python image_generator.py --model gpt-image-1 --quality hd

# Avec DALL-E 3 (haute qualité)
uv run python image_generator.py --model dall-e-3 --quality hd

# Avec DALL-E 2 (économique)
uv run python image_generator.py --model dall-e-2 --size 512x512
```

### Génération avec un prompt personnalisé
```bash
uv run python image_generator.py --prompt "Un golden retriever joueur dans un parc"
uv run python image_generator.py --prompt "Une montagne enneigée au coucher du soleil"
uv run python image_generator.py --prompt "Une femme élégante dans un jardin"
```

### Génération dans un style spécifique
```bash
uv run python image_generator.py --style cartoon --prompt "Un chaton joueur"
```

### Génération en haute qualité
```bash
uv run python image_generator.py --quality hd --size 1024x1536
```

### Génération dans plusieurs styles
```bash
uv run python image_generator.py --multiple --prompt "Un chat élégant"
```

### Exemple d'utilisation programmatique
```bash
uv run python examples/example_usage.py
```

### Exemple spécifique avec GPT-Image-1
```bash
uv run python examples/example_gpt_image_usage.py
```

## 🎨 Styles disponibles

- `realistic` : Style réaliste (par défaut)
- `cartoon` : Style cartoon/manga
- `artistic` : Style artistique/peinture
- `anime` : Style anime japonais
- `watercolor` : Style aquarelle
- `sketch` : Style croquis au crayon
- `cute` : Style mignon/adorable
- `majestic` : Style majestueux/royal
- `minimalist` : Style minimaliste/épuré
- `vintage` : Style vintage/rétro

## 📏 Tailles disponibles

### GPT-Image-1 (qualité supérieure)
- `1024x1024` : Carré
- `1024x1536` : Portrait
- `1536x1024` : Paysage
- `auto` : Taille automatique

### DALL-E 3
- `1024x1024` : Carré (par défaut)
- `1792x1024` : Paysage
- `1024x1792` : Portrait

### DALL-E 2
- `256x256` : Petit carré
- `512x512` : Carré moyen
- `1024x1024` : Grand carré

## 🎯 Qualités disponibles

### GPT-Image-1 et DALL-E 3
- `standard` : Qualité standard (par défaut)
- `hd` : Haute définition

### DALL-E 2
- `standard` : Qualité standard uniquement

## 💡 Conseils pour GPT-Image-1

GPT-Image-1 excelle particulièrement dans :
- **Prompts détaillés** : Utilisez des descriptions précises
- **Éclairage et composition** : Mentionnez l'éclairage, l'ambiance
- **Résolutions élevées** : 1024x1536 et 1536x1024 pour la meilleure qualité
- **Styles réalistes** : Photographies, portraits, paysages

Exemples de prompts optimisés pour GPT-Image-1 :
```
"Un chat persan blanc assis sur un coussin rouge, éclairage doux et chaleureux, composition professionnelle"
"Portrait d'une femme avec des cheveux roux, éclairage dramatique, style photographique professionnel"
"Montagnes enneigées au coucher du soleil, style réaliste, éclairage doré"
```

## 🔧 Options de ligne de commande

| Option | Description | Exemple |
|--------|-------------|---------|
| `--prompt, -p` | Description complète de l'image à générer | `--prompt "Un chat dans un jardin"` |
| `--style, -s` | Style de l'image | `--style cartoon` |
| `--size` | Taille de l'image | `--size 1024x1536` |
| `--quality` | Qualité de l'image | `--quality hd` |
| `--model, -m` | Modèle à utiliser | `--model gpt-image-1` |
| `--multiple` | Générer dans plusieurs styles | `--multiple` |
| `--list-models` | Afficher les modèles disponibles | `--list-models` |
| `--api-key` | Clé API (optionnel si dans .env) | `--api-key sk-...` |

## 💡 Exemples d'utilisation

### Chat réaliste avec GPT-Image-1 (qualité supérieure)
```bash
uv run python image_generator.py --prompt "Un chat persan blanc assis sur un coussin rouge" --style realistic --model gpt-image-1 --quality hd
```

### Chat économique avec DALL-E 2
```bash
uv run python image_generator.py --prompt "Un chat mignon" --model dall-e-2 --size 512x512
```

### Chien en cartoon haute qualité avec GPT-Image-1
```bash
uv run python image_generator.py --prompt "Un golden retriever joueur dans un parc" --style cartoon --quality hd --model gpt-image-1
```

### Paysage artistique avec GPT-Image-1
```bash
uv run python image_generator.py --prompt "Une montagne enneigée au coucher du soleil" --style artistic --model gpt-image-1
```

### Portrait vintage avec GPT-Image-1
```bash
uv run python image_generator.py --prompt "Une femme des années 1920, éclairage dramatique" --style vintage --model gpt-image-1
```

### Génération multiple avec GPT-Image-1
```bash
uv run python image_generator.py --multiple --prompt "Un chat élégant dans un salon" --model gpt-image-1
```

## 🔄 Comparaison des modèles

| Modèle | Qualité | Coût | Résolution max | Type |
|--------|---------|------|----------------|------|
| **GPT-Image-1** | ⭐⭐⭐⭐⭐ | $$ | 1536x1024 | Image directe |
| **DALL-E 3** | ⭐⭐⭐⭐ | $$ | 1792x1024 | Image directe |
| **DALL-E 2** | ⭐⭐⭐ | $ | 1024x1024 | Image directe |

## ⏱️ Statistiques et monitoring

L'application affiche automatiquement :
- **Temps de génération** : Durée de la requête API
- **Temps de téléchargement** : Durée du téléchargement de l'image
- **Temps total** : Somme des deux temps
- **Coût estimé** : Basé sur les tarifs officiels du modèle utilisé
- **Taille du prompt** : Nombre de caractères
- **Statistiques globales** : Pour les générations multiples

## 🛠️ Utilisation programmatique

### Exemple de base
```python
from src.generators.image_generator import ImageGenerator

# Initialiser le générateur
generator = ImageGenerator()

# Générer une image simple
result = generator.generate_image(
    prompt="Un chat mignon dans un jardin",
    style="realistic",
    size="1024x1024"
)
```

### Exemple avec options avancées
```python
from src.generators.image_generator import ImageGenerator

generator = ImageGenerator()

# Générer avec toutes les options
result = generator.generate_image(
    prompt="Un portrait professionnel d'une femme",
    style="realistic",
    size="1024x1536",
    quality="hd",
    model="gpt-image-1"
)
```

### Génération multiple
```python
from src.generators.image_generator import ImageGenerator

generator = ImageGenerator()

# Générer dans plusieurs styles
results = generator.generate_multiple_styles(
    prompt="Un chat élégant",
    styles=["realistic", "cartoon", "artistic"]
)
```

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

### Erreur de taille non supportée
- Vérifiez que la taille est compatible avec le modèle choisi
- Consultez la section "Tailles disponibles" ci-dessus

### Images de mauvaise qualité
- Utilisez `--quality hd` pour une meilleure qualité
- Essayez GPT-Image-1 avec des prompts plus détaillés
- Augmentez la résolution si possible

## 📁 Structure des fichiers

```
ads-generator/
├── image_generator.py    # Script principal
├── examples/
│   ├── example_usage.py           # Exemple d'utilisation général
│   └── example_gpt_image_usage.py # Exemple spécifique GPT-Image-1
├── src/
│   └── generators/
│       └── image_generator.py     # Module principal
└── generated/
    └── images/                    # Dossier des images générées
```

## ⚠️ Notes importantes

- **Coût** : L'utilisation de GPT-Image-1 engendre des coûts selon votre plan OpenAI
- **Limites** : Respectez les limites d'utilisation de l'API OpenAI
- **Clé API** : Gardez votre clé API secrète et ne la partagez jamais
- **Python 3.13+** : Le projet nécessite Python 3.13 ou supérieur
- **Stockage** : Les images sont sauvegardées dans `generated/images/` 