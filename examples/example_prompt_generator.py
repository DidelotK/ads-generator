#!/usr/bin/env python3
"""
Exemple d'utilisation du générateur de prompts d'images
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path pour les imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from generators.prompt_generator import PromptGenerator

def main():
    """Exemple d'utilisation du générateur de prompts d'images"""
    
    print("🎨 Générateur de Prompts d'Images pour Facebook Ads")
    print("=" * 50)
    
    try:
        # Initialiser le générateur
        generator = PromptGenerator()
        
        # Afficher les modèles disponibles
        print("\n📋 Modèles disponibles:")
        models = generator.get_available_models()
        for model_id, info in models.items():
            print(f"  • {model_id}: {info['name']} - {info['description']}")
        
        # Afficher les styles disponibles
        print("\n🎨 Styles disponibles:")
        styles = generator.get_available_styles()
        for style_id, info in styles.items():
            print(f"  • {style_id}: {info['description']}")
        
        # Exemple 1: Génération simple
        print("\n" + "="*50)
        print("📝 EXEMPLE 1: Génération simple")
        print("="*50)
        
        hook = "Factures en baisse, pouvoir d'achat en hausse"
        description = "Augmentez votre pouvoir d'achat en adoptant notre méthode révolutionnaire pour diminuer vos factures énergétique et dépenser moins au quotidien."
        
        print(f"🎯 Hook: {hook}")
        print(f"📄 Description: {description}")
        
        prompts = generator.generate_prompts(
            hook=hook,
            description=description,
            num_prompts=2,
            style="realistic",
            model="gpt-3.5-turbo"
        )
        
        print(f"\n✅ {len(prompts)} prompts générés:")
        for i, prompt in enumerate(prompts, 1):
            print(f"\n📸 Prompt {i}:")
            print(f"  Style: {prompt['style']}")
            print(f"  Prompt: {prompt['prompt']}")
            print(f"  Éléments: {', '.join(prompt['elements'])}")
            print(f"  Description: {prompt['description']}")
        
        # Exemple 2: Génération avec plusieurs styles
        print("\n" + "="*50)
        print("📝 EXEMPLE 2: Génération avec plusieurs styles")
        print("="*50)
        
        hook2 = "Cette technologie interdite par les lobbies"
        description2 = "Découvrez pourquoi les grandes entreprises ne veulent pas que vous connaissiez cette méthode révolutionnaire pour produire votre propre électricité."
        
        print(f"🎯 Hook: {hook2}")
        print(f"📄 Description: {description2}")
        
        all_prompts = generator.generate_multiple_styles(
            hook=hook2,
            description=description2,
            styles=["realistic", "commercial", "dramatic"],
            num_prompts=1,
            model="gpt-3.5-turbo"
        )
        
        for style, prompts in all_prompts.items():
            print(f"\n🎨 Style '{style}':")
            for i, prompt in enumerate(prompts, 1):
                print(f"  📸 Prompt {i}:")
                print(f"    Prompt: {prompt['prompt'][:100]}...")
                print(f"    Éléments: {', '.join(prompt['elements'])}")
        
        # Exemple 3: Génération avec style artistique
        print("\n" + "="*50)
        print("📝 EXEMPLE 3: Style artistique")
        print("="*50)
        
        hook3 = "Le secret des millionnaires pour l'énergie gratuite"
        description3 = "Apprenez les techniques utilisées par les plus riches pour réduire drastiquement leurs factures d'énergie et gagner en indépendance."
        
        print(f"🎯 Hook: {hook3}")
        print(f"📄 Description: {description3}")
        
        artistic_prompts = generator.generate_prompts(
            hook=hook3,
            description=description3,
            num_prompts=1,
            style="artistic",
            model="gpt-3.5-turbo"
        )
        
        for i, prompt in enumerate(artistic_prompts, 1):
            print(f"\n🎨 Prompt artistique {i}:")
            print(f"  Style: {prompt['style']}")
            print(f"  Prompt: {prompt['prompt']}")
            print(f"  Éléments: {', '.join(prompt['elements'])}")
            print(f"  Description: {prompt['description']}")
        
        print("\n" + "="*50)
        print("✅ Génération terminée avec succès!")
        print("💾 Les prompts ont été sauvegardés dans le dossier 'generated/prompts/'")
        print("="*50)
        
    except ValueError as e:
        print(f"❌ Erreur de configuration: {e}")
        print("💡 Assurez-vous d'avoir défini OPENAI_API_KEY dans votre fichier .env")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    main() 