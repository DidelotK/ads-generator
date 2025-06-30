# Générateur d'Accroches avec l'API OpenAI

Ce script Python génère des accroches marketing percutantes en utilisant l'API OpenAI (GPT-4 et GPT-3.5 Turbo). Il peut créer différents types d'accroches selon le style demandé et le sujet fourni.

**🎯 GPT-3.5 Turbo** est le modèle par défaut pour une génération rapide et économique !

## 🚀 Installation

Pour installer et configurer le projet, consultez notre [guide d'installation complet](installation.md).

## 🤖 Modèles disponibles

### Afficher les modèles et leurs tarifs
```bash
uv run python hook_generator.py --list-models
```

### 🚀 GPT-3.5 Turbo (par défaut - économique)
- **Description** : Modèle rapide et économique pour la génération de contenu
- **Type** : Génération de texte
- **Coût entrée** : $0.0015 USD par 1K tokens
- **Coût sortie** : $0.002 USD par 1K tokens
- **Tokens max** : 4096
- **Avantages** : Rapide, économique, idéal pour les tests

### 🧠 GPT-4 (haute qualité)
- **Description** : Modèle le plus avancé pour la génération de contenu créatif
- **Type** : Génération de texte
- **Coût entrée** : $0.030 USD par 1K tokens
- **Coût sortie** : $0.060 USD par 1K tokens
- **Tokens max** : 4096
- **Avantages** : Qualité supérieure, créativité élevée

## 📖 Utilisation

### Génération d'accroches simple
```bash
uv run python hook_generator.py --subject "Application mobile de fitness"
```

### Génération avec un modèle spécifique
```bash
# Avec GPT-3.5 Turbo (économique - par défaut)
uv run python hook_generator.py --subject "Restaurant gastronomique" --model gpt-3.5-turbo

# Avec GPT-4 (haute qualité)
uv run python hook_generator.py --subject "Formation en ligne" --model gpt-4
```

### Génération avec un style spécifique
```bash
uv run python hook_generator.py --subject "Produit tech" --style engaging
uv run python hook_generator.py --subject "Service B2B" --style professional
uv run python hook_generator.py --subject "Restaurant" --style creative
```

### Génération avec plusieurs accroches
```bash
uv run python hook_generator.py --subject "Application mobile" --num-hooks 10
```

### Génération dans plusieurs styles
```bash
uv run python hook_generator.py --subject "Formation marketing" --multiple-styles
```

### Exemple d'utilisation programmatique
```bash
uv run python examples/example_hooks.py
```

## 🎨 Styles disponibles

- `engaging` : Accrocheuses et engageantes qui captent immédiatement l'attention (par défaut)
- `professional` : Professionnelles et sérieuses, adaptées à un public business
- `creative` : Créatives et originales, avec un angle unique et surprenant
- `emotional` : Émotionnelles et touchantes, qui suscitent des sentiments
- `humorous` : Humoristiques et amusantes, avec une touche d'humour
- `urgent` : Qui créent un sentiment d'urgence et d'action immédiate
- `curiosity` : Qui éveillent la curiosité et poussent à en savoir plus
- `benefit` : Qui mettent l'accent sur les bénéfices et avantages
- `story` : Narratives, qui racontent une histoire ou utilisent une anecdote
- `question` : Qui posent des questions pertinentes et provocantes

## 🌍 Langues disponibles

Le générateur supporte toutes les langues. Par défaut, il génère en français :
```bash
uv run python hook_generator.py --subject "Product" --language "english"
```

## 📏 Format des accroches

### Règles de génération
- **Hooks** : Maximum 60 caractères, phrases courtes et impactantes
- **Descriptions** : Maximum 120 caractères, explications concises
- **Variété** : Les accroches sont variées et non répétitives
- **Direct** : Privilégier les phrases courtes et directes

### Exemple de sortie
```json
{
  "hooks": [
    {
      "hook": "Transformez votre corps en 30 jours",
      "description": "Accroche engageante avec promesse de résultat rapide"
    },
    {
      "hook": "Fitness sans effort, résultats garantis",
      "description": "Accent sur la facilité et les garanties"
    }
  ]
}
```

## 💡 Conseils pour des accroches efficaces

### Sujets optimaux
- **Produits/Services** : Décrivez clairement ce que vous vendez
- **Audience cible** : Mentionnez votre public si pertinent
- **Bénéfices** : Incluez les avantages principaux
- **Contexte** : Ajoutez du contexte si nécessaire

### Exemples de sujets
```
"Application mobile de fitness pour débutants"
"Formation en ligne de marketing digital pour entrepreneurs"
"Restaurant gastronomique fusion asiatique à Paris"
"Service de nettoyage écologique pour entreprises"
"Formation en ligne de yoga pour seniors"
```

## 🔧 Options de ligne de commande

| Option | Description | Exemple |
|--------|-------------|---------|
| `--subject, -s` | Sujet pour lequel générer les accroches | `--subject "Application mobile"` |
| `--num-hooks, -n` | Nombre d'accroches à générer | `--num-hooks 10` |
| `--style` | Style des accroches | `--style professional` |
| `--model, -m` | Modèle à utiliser | `--model gpt-4` |
| `--language, -l` | Langue de génération | `--language english` |
| `--multiple-styles` | Générer dans plusieurs styles | `--multiple-styles` |
| `--list-models` | Afficher les modèles disponibles | `--list-models` |
| `--api-key` | Clé API (optionnel si dans .env) | `--api-key sk-...` |

## 💡 Exemples d'utilisation

### Accroches engageantes pour un produit tech
```bash
uv run python hook_generator.py --subject "Application mobile de fitness" --style engaging --num-hooks 5
```

### Accroches professionnelles pour un service B2B
```bash
uv run python hook_generator.py --subject "Solution de gestion de projet pour entreprises" --style professional --model gpt-4
```

### Accroches créatives pour un restaurant
```bash
uv run python hook_generator.py --subject "Restaurant gastronomique fusion asiatique" --style creative
```

### Génération multiple de styles
```bash
uv run python hook_generator.py --subject "Formation en ligne de marketing digital" --multiple-styles --num-hooks 3
```

### Accroches émotionnelles en anglais
```bash
uv run python hook_generator.py --subject "Online yoga course for seniors" --style emotional --language english
```

## 🔄 Comparaison des modèles

| Modèle | Qualité | Coût | Vitesse | Idéal pour |
|--------|---------|------|---------|------------|
| **GPT-3.5 Turbo** | ⭐⭐⭐ | $ | ⚡⚡⚡ | Tests, génération rapide |
| **GPT-4** | ⭐⭐⭐⭐⭐ | $$$ | ⚡⚡ | Qualité maximale |

## ⏱️ Statistiques et monitoring

L'application affiche automatiquement :
- **Temps de génération** : Durée de la requête API
- **Coût estimé** : Basé sur les tarifs officiels du modèle utilisé
- **Nombre d'accroches** : Accroches générées avec succès
- **Statistiques globales** : Pour les générations multiples

## 📁 Structure des fichiers

```
ads-generator/
├── hook_generator.py              # Script principal
├── examples/
│   └── example_hooks.py           # Exemple d'utilisation
├── src/
│   └── generators/
│       └── hook_generator.py      # Module principal
└── generated/
    └── hooks/                     # Dossier des accroches générées
```

## 🛠️ Utilisation programmatique

```python
from src.generators.hook_generator import HookGenerator

# Initialiser le générateur
generator = HookGenerator()

# Générer des accroches
hooks = generator.generate_hooks(
    subject="Application mobile de fitness",
    num_hooks=5,
    style="engaging",
    model="gpt-3.5-turbo",
    language="français"
)

# Générer dans plusieurs styles
results = generator.generate_multiple_styles(
    subject="Formation marketing",
    styles=["engaging", "professional", "emotional"],
    num_hooks=3
)
```

## ⚠️ Notes importantes

- **Coût** : L'utilisation des modèles engendre des coûts selon votre plan OpenAI
- **Limites** : Respectez les limites d'utilisation de l'API OpenAI
- **Clé API** : Gardez votre clé API secrète et ne la partagez jamais
- **Python 3.13+** : Le projet nécessite Python 3.13 ou supérieur

## 🐛 Dépannage

### Erreur "Clé API requise"
- Vérifiez que votre fichier `.env` contient `OPENAI_API_KEY=sk-...`
- Ou passez la clé directement : `--api-key sk-...`

### Erreur "L'argument --subject/-s est requis"
- Ajoutez le sujet : `--subject "Votre sujet ici"`

### Erreur de connexion
- Vérifiez votre connexion internet
- Vérifiez que votre clé API est valide

### Erreur de quota
- Vérifiez votre quota OpenAI sur le dashboard

### Problèmes avec uv
- Vérifiez que uv est installé : `uv --version`
- Réinstallez les dépendances : `uv sync --reinstall` 