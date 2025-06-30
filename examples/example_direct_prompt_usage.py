#!/usr/bin/env python3
"""
Exemple d'utilisation directe des prompts textuels générés
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au path pour les imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from generators.prompt_generator import PromptGenerator

def main():
    """Exemple d'utilisation directe des prompts textuels"""
    
    print("🎨 Exemple : Utilisation Directe des Prompts Textuels")
    print("=" * 60)
    
    try:
        # Générer les prompts
        generator = PromptGenerator()
        
        hook = "Factures en baisse, pouvoir d'achat en hausse"
        description = "Augmentez votre pouvoir d'achat en adoptant notre méthode révolutionnaire pour diminuer vos factures énergétique et dépenser moins au quotidien."
        
        prompts = generator.generate_prompts(
            hook=hook,
            description=description,
            num_prompts=2,
            style="realistic",
            model="gpt-3.5-turbo"
        )
        
        print(f"\n✅ {len(prompts)} prompts générés")
        print("\n" + "="*60)
        print("🎯 PROMPTS PRÊTS À L'EMPLOI")
        print("="*60)
        
        # Afficher les prompts prêts à copier-coller
        for i, prompt_data in enumerate(prompts, 1):
            print(f"\n📸 PROMPT {i} (Style: {prompt_data['style']})")
            print("-" * 50)
            print("🎯 PROMPT COMPLET (copiez-collez directement):")
            print()
            print(f"{prompt_data['prompt']}")
            print()
            print("-" * 50)
        
        # Exemples d'utilisation avec différents générateurs
        print("\n" + "="*60)
        print("🔧 EXEMPLES D'UTILISATION")
        print("="*60)
        
        for i, prompt_data in enumerate(prompts, 1):
            prompt_text = prompt_data['prompt']
            
            print(f"\n📸 Utilisation du Prompt {i}:")
            print("-" * 40)
            
            print("1️⃣ DALL-E 3:")
            print(f"   Prompt: {prompt_text}")
            print("   Taille: 1024x1024")
            print("   Qualité: HD")
            
            print("\n2️⃣ Midjourney:")
            midjourney_prompt = f"/imagine {prompt_text} --ar 1:1 --v 6"
            print(f"   Commande: {midjourney_prompt}")
            
            print("\n3️⃣ Stable Diffusion:")
            stable_prompt = f"{prompt_text}, high quality, professional photography, 4k"
            print(f"   Prompt: {stable_prompt}")
            
            print("\n4️⃣ Leonardo.ai:")
            print(f"   Prompt: {prompt_text}")
            print("   Modèle: Leonardo Creative")
            
            print("\n5️⃣ Bing Image Creator:")
            print(f"   Prompt: {prompt_text}")
            
            print("-" * 40)
        
        print("\n" + "="*60)
        print("✅ Exemple terminé!")
        print("💡 Les prompts sont maintenant prêts à être utilisés")
        print("📝 Copiez-collez directement dans votre générateur d'images préféré")
        print("="*60)
        
    except ValueError as e:
        print(f"❌ Erreur de configuration: {e}")
        print("💡 Assurez-vous d'avoir défini OPENAI_API_KEY dans votre fichier .env")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

def show_prompt_formats():
    """Affiche les différents formats de prompts pour différents générateurs"""
    
    print("\n🎨 Formats de Prompts par Générateur")
    print("=" * 60)
    
    # Exemple de prompt généré
    example_prompt = "Image d'une cuisine moderne et lumineuse avec des équipements économes en énergie tels qu'un réfrigérateur classe A+, une cuisinière à induction et des ampoules LED intégrées. Sur le comptoir, des fruits frais et des légumes colorés sont disposés dans des paniers en osier. En arrière-plan, une fenêtre laisse entrer la lumière du jour, mettant en valeur l'aspect chaleureux et convivial de l'espace."
    
    print(f"📝 Prompt de base:\n{example_prompt}\n")
    
    print("🎯 Formats spécifiques:")
    
    print("\n1️⃣ DALL-E 3 (OpenAI):")
    print("   Format: Prompt direct")
    print(f"   Exemple: {example_prompt}")
    print("   Paramètres: size=1024x1024, quality=hd, style=vivid")
    
    print("\n2️⃣ Midjourney:")
    print("   Format: /imagine [prompt] [paramètres]")
    print(f"   Exemple: /imagine {example_prompt} --ar 1:1 --v 6")
    print("   Paramètres: --ar 1:1 (ratio carré), --v 6 (version 6)")
    
    print("\n3️⃣ Stable Diffusion:")
    print("   Format: [prompt], [paramètres positifs]")
    print(f"   Exemple: {example_prompt}, high quality, professional photography, 4k, detailed")
    print("   Paramètres négatifs: --neg \"text, watermark, blur, low quality\"")
    
    print("\n4️⃣ Leonardo.ai:")
    print("   Format: Prompt direct")
    print(f"   Exemple: {example_prompt}")
    print("   Modèles: Leonardo Creative, Leonardo Select, etc.")
    
    print("\n5️⃣ Bing Image Creator:")
    print("   Format: Prompt direct")
    print(f"   Exemple: {example_prompt}")
    print("   Limite: 25 générations par jour")
    
    print("\n6️⃣ Canva AI:")
    print("   Format: Prompt direct")
    print(f"   Exemple: {example_prompt}")
    print("   Intégré dans l'éditeur Canva")

if __name__ == "__main__":
    main()
    show_prompt_formats() 