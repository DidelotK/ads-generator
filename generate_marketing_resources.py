#!/usr/bin/env python3
"""
Script de lancement pour générer des hooks marketing et images
Usage: python generate_marketing_ads.py
"""

import sys
import os

# Ajouter le répertoire examples au path pour importer la configuration
sys.path.append(os.path.join(os.path.dirname(__file__), 'examples'))

def main():
    """Lance la génération de hooks marketing et d'images"""
    
    print("🚀 Générateur de Hooks Marketing et Images")
    print("=" * 50)
    print("Ce script va générer:")
    print("✅ 5 hooks marketing très engageants")
    print("✅ 2 images par hook (réaliste + artistique)")
    print("✅ Fichiers sauvegardés automatiquement")
    print()
    
    # Demander confirmation
    response = input("Voulez-vous continuer? (o/n): ").lower().strip()
    if response not in ['o', 'oui', 'y', 'yes']:
        print("❌ Génération annulée")
        return
    
    try:
        # Importer et exécuter le générateur
        from examples.example_marketing_hooks import generate_marketing_resources
        generate_marketing_resources(
            num_subjects=5,
            num_styles=5
        )
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Assurez-vous que tous les fichiers sont présents")
        print("💡 Vérifiez que vous avez configuré votre clé API OpenAI")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        print("💡 Vérifiez votre connexion internet et votre clé API")

if __name__ == "__main__":
    main() 