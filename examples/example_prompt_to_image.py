#!/usr/bin/env python3
"""
Exemple d'utilisation : Générer des prompts puis les utiliser pour créer des images
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path pour les imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from generators.prompt_generator import PromptGenerator
from generators.image_generator import ImageGenerator

def main():
    """Exemple complet : prompt → image"""
    
    print("🎨 Exemple : Génération de Prompts → Images")
    print("=" * 60)
    
    try:
        # 1. Générer les prompts
        print("📝 Étape 1 : Génération des prompts d'images")
        print("-" * 40)
        
        prompt_gen = PromptGenerator()
        
        hook = "Factures en baisse, pouvoir d'achat en hausse"
        description = "Augmentez votre pouvoir d'achat en adoptant notre méthode révolutionnaire pour diminuer vos factures énergétique et dépenser moins au quotidien."
        
        prompts = prompt_gen.generate_prompts(
            hook=hook,
            description=description,
            num_prompts=2,
            style="realistic",
            model="gpt-3.5-turbo"
        )
        
        print(f"✅ {len(prompts)} prompts générés")
        
        # 2. Utiliser les prompts pour générer des images
        print("\n🖼️  Étape 2 : Génération des images")
        print("-" * 40)
        
        image_gen = ImageGenerator()
        
        for i, prompt_data in enumerate(prompts, 1):
            print(f"\n📸 Génération de l'image {i}...")
            print(f"Prompt: {prompt_data['prompt'][:100]}...")
            
            # Utiliser directement le prompt textuel pour générer l'image
            try:
                # Note: Cette partie nécessite une clé API OpenAI configurée
                # et peut générer des coûts
                image_path = image_gen.generate_image(
                    prompt=prompt_data['prompt'],
                    size="1024x1024",
                    quality="hd",
                    style="vivid"
                )
                
                print(f"✅ Image générée: {image_path}")
                
            except Exception as e:
                print(f"⚠️  Erreur lors de la génération d'image: {e}")
                print("💡 Assurez-vous d'avoir configuré votre clé API OpenAI")
                print("💡 Cette étape peut générer des coûts")
        
        # 3. Afficher les prompts complets pour utilisation manuelle
        print("\n📋 Prompts complets pour utilisation manuelle:")
        print("-" * 40)
        
        for i, prompt_data in enumerate(prompts, 1):
            print(f"\n🎯 Prompt {i} (Style: {prompt_data['style']}):")
            print(f"📝 {prompt_data['prompt']}")
            print(f"🔍 Éléments détectés: {', '.join(prompt_data['elements'])}")
            print(f"📄 Description: {prompt_data['description']}")
            print("-" * 60)
        
        print("\n" + "="*60)
        print("✅ Exemple terminé!")
        print("💡 Vous pouvez maintenant utiliser ces prompts avec:")
        print("   - DALL-E 3")
        print("   - Midjourney")
        print("   - Stable Diffusion")
        print("   - Ou tout autre générateur d'images IA")
        print("="*60)
        
    except ValueError as e:
        print(f"❌ Erreur de configuration: {e}")
        print("💡 Assurez-vous d'avoir défini OPENAI_API_KEY dans votre fichier .env")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

def show_prompt_usage_examples():
    """Affiche des exemples d'utilisation des prompts générés"""
    
    print("\n🔧 Exemples d'utilisation des prompts générés:")
    print("=" * 60)
    
    # Exemple de prompt généré
    example_prompt = """Une image mettant en scène une famille souriante autour d'une table, en train de regarder des factures d'énergie et des relevés de dépenses. Le père, la mère et l'enfant semblent surpris et heureux en découvrant des économies réalisées. En arrière-plan, des ampoules LED, des panneaux solaires et des appareils électroménagers économes en énergie renforcent le message de réduction des factures. L'ambiance est chaleureuse et conviviale, reflétant le bien-être financier que procure l'adoption de la méthode proposée."""
    
    print(f"📝 Prompt généré:\n{example_prompt}")
    
    print("\n🎯 Utilisation avec différents générateurs:")
    
    print("\n1️⃣ DALL-E 3 (via OpenAI):")
    print("   - Copiez le prompt directement")
    print("   - Utilisez-le dans l'API DALL-E 3")
    print("   - Taille recommandée: 1024x1024")
    
    print("\n2️⃣ Midjourney:")
    print("   - Ajoutez --ar 1:1 pour un ratio carré")
    print("   - Ajoutez --v 6 pour la version 6")
    print("   - Exemple: /imagine [prompt] --ar 1:1 --v 6")
    
    print("\n3️⃣ Stable Diffusion:")
    print("   - Utilisez le prompt dans l'interface web")
    print("   - Ajoutez des paramètres négatifs si nécessaire")
    print("   - Exemple: [prompt], high quality, professional photography")
    
    print("\n4️⃣ Leonardo.ai:")
    print("   - Copiez le prompt dans l'éditeur")
    print("   - Sélectionnez le modèle approprié")
    print("   - Ajustez les paramètres de génération")

if __name__ == "__main__":
    main()
    show_prompt_usage_examples() 