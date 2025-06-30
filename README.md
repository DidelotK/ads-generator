# 🚀 Générateur d'Ads - Suite d'Outils IA

Une suite complète d'outils IA pour générer des accroches marketing et des images créatives avec l'API OpenAI.

## 📋 Sommaire

- [🚀 Installation](#-installation)
- [🎯 Générateur d'Accroches](#-générateur-daccroches)
- [🎨 Générateur d'Images](#-générateur-dimages)
- [👨‍💻 Guide Développeur](#️-guide-développeur)
- [🐛 Dépannage](#-dépannage)

## 🚀 Installation

Pour installer et configurer le projet, consultez notre [guide d'installation complet](docs/installation.md).


## 🎯 Générateur d'Accroches

Le générateur d'accroches marketing crée des accroches percutantes pour vos campagnes publicitaires.

### 📖 Documentation complète
Consultez la [documentation détaillée du générateur d'accroches](docs/hook_generator.md).

### 🚀 Utilisation rapide

```bash
# Génération avec un sujet spécifique
uv run python hook_generator.py --subject "Formation en marketing digital"
```

## 🎨 Générateur d'Images

Le générateur d'images crée des visuels créatifs avec l'API OpenAI (GPT-Image-1, DALL-E 2 et DALL-E 3).

### 📖 Documentation complète
Consultez la [documentation détaillée du générateur d'images](docs/image_generator.md).

### 🚀 Utilisation rapide

```bash
uv run python image_generator.py --prompt "Un chat mignon dans un jardin" --model gpt-image-1 --quality hd
```

## 👨‍💻 Guide Développeur

Pour les développeurs souhaitant contribuer au projet ou comprendre son architecture, consultez notre [guide développeur complet](docs/developer.md).

Ce guide inclut :
- **Installation détaillée** et configuration de l'environnement de développement
- **Structure complète du repository** et architecture des modules
- **Commandes utiles** pour le développement, les tests et le déploiement
- **Configuration des IDE** et outils de développement
- **Guide de contribution** et bonnes pratiques

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

### Problèmes techniques avancés
Pour les problèmes techniques plus complexes, consultez la section [Debugging](docs/developer.md#-debugging) du guide développeur.

## ⚠️ Notes importantes

- **Coût** : L'utilisation des API OpenAI engendre des coûts selon votre plan
- **Limites** : Respectez les limites d'utilisation de l'API OpenAI
- **Clé API** : Gardez votre clé API secrète et ne la partagez jamais
- **Python 3.13+** : Le projet nécessite Python 3.13 ou supérieur
- **Stockage** : Les fichiers générés sont sauvegardés dans `generated/`

## 📚 Ressources supplémentaires

- [Guide d'installation complet](docs/installation.md)
- [Documentation du générateur d'accroches](docs/hook_generator.md)
- [Documentation du générateur d'images](docs/image_generator.md)
- [Guide développeur](docs/developer.md)
- [Exemples d'utilisation](examples/)
- [Tests unitaires](tests/)
