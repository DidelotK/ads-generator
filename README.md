# Générateur d'Images avec l'API OpenAI

Ce script Python génère des images en utilisant l'API OpenAI (DALL-E 2 et DALL-E 3). Il peut générer différents types d'images : chats, chiens, paysages, portraits, etc.

## 🚀 Installation

### Option 1: Configuration automatique
```bash
./setup.sh
```

### Option 2: Configuration manuelle

1. **Installer uv** (si pas déjà installé) :
   ```bash
   # macOS avec Homebrew
   brew install uv
   
   # Ou avec curl
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Installer les dépendances** :
   ```bash
   uv sync
   ```

3. **Configurer l'API OpenAI** :
   - Créez un fichier `.env` à la racine du projet
   - Ajoutez votre clé API OpenAI :
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```
   - Obtenez votre clé sur [OpenAI Platform](https://platform.openai.com/api-keys)

## 🤖 Modèles disponibles

### Afficher les modèles et leurs tarifs
```bash
uv run python image_generator.py --list-models
```

### DALL-E 3 (par défaut)
- **Description** : Modèle le plus récent et avancé d'OpenAI
- **Tailles** : 1024x1024, 1792x1024, 1024x1792
- **Qualités** : standard, hd
- **Tarifs** : $0.040-$0.120 USD par image

### DALL-E 2 (économique)
- **Description** : Modèle précédent d'OpenAI, moins cher
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
# Avec DALL-E 3 (haute qualité)
uv run python image_generator.py --model dall-e-3 --quality hd

# Avec DALL-E 2 (économique)
uv run python image_generator.py --model dall-e-2 --size 512x512
```

### Génération d'un type spécifique
```bash
uv run python image_generator.py --subject chien --prompt "Un golden retriever joueur"
uv run python image_generator.py --subject paysage --prompt "Une montagne enneigée"
uv run python image_generator.py --subject portrait --prompt "Une femme élégante"
```

### Génération avec un prompt personnalisé
```bash
uv run python image_generator.py --prompt "Un chat noir assis sur un coussin rouge"
```

### Génération dans un style spécifique
```bash
uv run python image_generator.py --style cartoon --prompt "Un chaton joueur"
```

### Génération en haute qualité
```bash
uv run python image_generator.py --quality hd --size 1792x1024
```

### Génération dans plusieurs styles
```bash
uv run python image_generator.py --multiple --prompt "Un chat élégant"
```

### Exemple d'utilisation programmatique
```bash
uv run python example_usage.py
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

### DALL-E 3
- `1024x1024` : Carré (par défaut)
- `1792x1024` : Paysage
- `1024x1792` : Portrait

### DALL-E 2
- `256x256` : Petit carré
- `512x512` : Carré moyen
- `1024x1024` : Grand carré

## 🎯 Qualités disponibles

### DALL-E 3
- `standard` : Qualité standard (par défaut)
- `hd` : Haute définition

### DALL-E 2
- `standard` : Qualité standard uniquement

## 📁 Structure des fichiers

```
ads-generator/
├── image_generator.py    # Script principal
├── example_usage.py           # Exemple d'utilisation
├── pyproject.toml            # Configuration uv
├── uv.lock                   # Verrouillage des dépendances
├── setup.sh                  # Script de configuration automatique
├── env_example.txt           # Exemple de configuration
├── README.md                 # Ce fichier
├── src/
│   └── generators/
│       ├── __init__.py
│       └── image_generator.py # Module principal
└── generated_images/         # Dossier des images générées (créé automatiquement)
```

## 🔧 Options de ligne de commande

| Option | Description | Exemple |
|--------|-------------|---------|
| `--subject, -t` | Type de sujet à générer | `--subject chien` |
| `--prompt, -p` | Description personnalisée | `--prompt "Un chat dans un jardin"` |
| `--style, -s` | Style de l'image | `--style cartoon` |
| `--size` | Taille de l'image | `--size 1792x1024` |
| `--quality` | Qualité de l'image | `--quality hd` |
| `--model, -m` | Modèle à utiliser | `--model dall-e-2` |
| `--multiple` | Générer dans plusieurs styles | `--multiple` |
| `--list-models` | Afficher les modèles disponibles | `--list-models` |
| `--api-key` | Clé API (optionnel si dans .env) | `--api-key sk-...` |

## 💡 Exemples d'utilisation

### Chat réaliste avec DALL-E 3
```bash
uv run python image_generator.py --style realistic --model dall-e-3
```

### Chat économique avec DALL-E 2
```bash
uv run python image_generator.py --model dall-e-2 --size 512x512
```

### Chien en cartoon haute qualité
```bash
uv run python image_generator.py --subject chien --style cartoon --prompt "Un golden retriever joueur" --quality hd
```

### Paysage artistique
```bash
uv run python image_generator.py --subject paysage --style artistic --prompt "Une montagne enneigée"
```

### Portrait vintage
```bash
uv run python image_generator.py --subject portrait --style vintage --prompt "Une femme des années 1920"
```

### Génération multiple économique
```bash
uv run python image_generator.py --multiple --subject chat --prompt "Un chat élégant dans un salon" --model dall-e-2
```

## 🛠️ Utilisation programmatique

```python
from src.generators.image_generator import ImageGenerator

# Initialiser le générateur
generator = ImageGenerator()

# Afficher les modèles disponibles
models = generator.get_available_models()
print(models)

# Générer une image avec DALL-E 3
filename = generator.generate_image(
    subject_type="chat",
    prompt="Un chat noir élégant",
    style="realistic",
    model="dall-e-3",
    quality="hd"
)

# Générer une image économique avec DALL-E 2
filename = generator.generate_image(
    subject_type="chien",
    prompt="Un golden retriever dans un parc",
    style="cartoon",
    model="dall-e-2",
    size="512x512"
)

# Générer plusieurs styles avec un modèle spécifique
results = generator.generate_multiple_styles(
    subject_type="paysage",
    prompt="Une montagne enneigée",
    styles=["realistic", "artistic", "watercolor"],
    model="dall-e-3",
    quality="standard"
)
```

## ⏱️ Statistiques et monitoring

L'application affiche automatiquement :
- **Temps de génération** : Durée de la requête API
- **Temps de téléchargement** : Durée du téléchargement de l'image
- **Temps total** : Somme des deux temps
- **Coût estimé** : Basé sur les tarifs officiels du modèle utilisé
- **Taille du prompt** : Nombre de caractères
- **Statistiques globales** : Pour les générations multiples

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

## ⚠️ Notes importantes

- **Coût** : L'utilisation de DALL-E 3 engendre des coûts selon votre plan OpenAI
- **Limites** : Respectez les limites d'utilisation de l'API OpenAI
- **Clé API** : Gardez votre clé API secrète et ne la partagez jamais
- **Python 3.13+** : Le projet nécessite Python 3.13 ou supérieur

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