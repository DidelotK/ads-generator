#!/bin/bash

# Script de configuration automatique pour le générateur d'images de chat
echo "🐱 Configuration du générateur d'images de chat avec uv"

# Vérifier si uv est installé
if ! command -v uv &> /dev/null; then
    echo "❌ uv n'est pas installé. Installation en cours..."
    
    # Détecter le système d'exploitation
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            echo "📦 Installation avec Homebrew..."
            brew install uv
        else
            echo "📦 Installation avec curl..."
            curl -LsSf https://astral.sh/uv/install.sh | sh
        fi
    else
        # Linux
        echo "📦 Installation avec curl..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
    fi
    
    # Recharger le shell
    source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null || true
fi

echo "✅ uv installé: $(uv --version)"

# Installer les dépendances
echo "📦 Installation des dépendances..."
uv sync

# Vérifier si le fichier .env existe
if [ ! -f ".env" ]; then
    echo "⚠️  Fichier .env non trouvé"
    echo "📝 Création du fichier .env..."
    cp env_example.txt .env
    echo "🔑 Veuillez ajouter votre clé API OpenAI dans le fichier .env"
    echo "   Obtenez votre clé sur: https://platform.openai.com/api-keys"
else
    echo "✅ Fichier .env trouvé"
fi

echo ""
echo "🎉 Configuration terminée!"
echo ""
echo "📖 Pour utiliser le générateur:"
echo "   uv run python chat_image_generator.py"
echo ""
echo "📖 Pour voir l'aide:"
echo "   uv run python chat_image_generator.py --help"
echo ""
echo "📖 Pour un exemple d'utilisation:"
echo "   uv run python example_usage.py" 