#!/usr/bin/env python3
"""
Script de lancement pour générer des ressources marketing (hooks + images)
Usage: python generate_marketing_ads.py [nombre_ressources]
"""

import sys
import os

# Ajouter le répertoire examples au path pour importer la configuration
sys.path.append(os.path.join(os.path.dirname(__file__), 'examples'))

def main():
    """Lance la génération de ressources marketing"""
    
    # Récupérer le nombre de ressources depuis les arguments
    num_resources = 5  # Valeur par défaut
    if len(sys.argv) > 1:
        try:
            num_resources = int(sys.argv[1])
            if num_resources <= 0:
                print("❌ Le nombre de ressources doit être positif")
                return
        except ValueError:
            print("❌ Le nombre de ressources doit être un nombre entier")
            return
    
    print("🚀 Générateur de Ressources Marketing")
    print("=" * 50)
    print(f"Ce script va générer:")
    print(f"✅ {num_resources} ressources marketing")
    print(f"✅ 1 hook + 2 images par ressource")
    print(f"✅ Fichiers sauvegardés automatiquement")
    print(f"✅ Sélection automatique des sujets et styles")
    print()
    
    # Demander confirmation
    response = input("Voulez-vous continuer? (o/n): ").lower().strip()
    if response not in ['o', 'oui', 'y', 'yes']:
        print("❌ Génération annulée")
        return
    
    try:
        # Importer et exécuter le générateur
        from examples.example_marketing_hooks import generate_marketing_resources
        resources = generate_marketing_resources(num_resources=num_resources)
        
        print(f"\n🎉 Génération terminée avec succès!")
        print(f"📊 {len(resources)} ressources créées")
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Assurez-vous que tous les fichiers sont présents")
        print("💡 Vérifiez que vous avez configuré votre clé API OpenAI")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        print("💡 Vérifiez votre connexion internet et votre clé API")

if __name__ == "__main__":
    main() 