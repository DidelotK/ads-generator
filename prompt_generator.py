#!/usr/bin/env python3
"""
Script principal pour générer des prompts d'images pour Facebook Ads
"""

import sys
import argparse
from pathlib import Path

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from generators.prompt_generator import PromptGenerator

def main():
    """Script principal pour générer des prompts d'images"""
    
    parser = argparse.ArgumentParser(
        description="Générateur de prompts d'images pour Facebook Ads",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python prompt_generator.py "Mon hook" "Ma description"
  python prompt_generator.py "Factures en baisse" "Économisez sur vos factures" --style realistic --num 3
  python prompt_generator.py "Technologie révolutionnaire" "Découvrez notre méthode" --style commercial --model gpt-4
  python prompt_generator.py "Secret révélé" "Ce que l'état cache" --multi-style
        """
    )
    
    parser.add_argument("hook", nargs="?", help="L'accroche (titre) de la publicité")
    parser.add_argument("description", nargs="?", help="La description de la publicité")
    parser.add_argument("--style", "-s", default="realistic", 
                       help="Style d'image (realistic, photographic, artistic, commercial, etc.)")
    parser.add_argument("--num", "-n", type=int, default=3,
                       help="Nombre de prompts à générer (défaut: 3)")
    parser.add_argument("--model", "-m", default="gpt-3.5-turbo",
                       help="Modèle OpenAI à utiliser (défaut: gpt-3.5-turbo)")
    parser.add_argument("--language", "-l", default="français",
                       help="Langue des prompts (défaut: français)")
    parser.add_argument("--multi-style", action="store_true",
                       help="Générer des prompts pour plusieurs styles")
    parser.add_argument("--list-styles", action="store_true",
                       help="Lister tous les styles disponibles")
    parser.add_argument("--list-models", action="store_true",
                       help="Lister tous les modèles disponibles")
    
    args = parser.parse_args()
    
    print("🎨 Générateur de Prompts d'Images pour Facebook Ads")
    print("=" * 60)
    
    try:
        # Initialiser le générateur
        generator = PromptGenerator()
        
        # Lister les styles si demandé
        if args.list_styles:
            print("\n🎨 Styles disponibles:")
            styles = generator.get_available_styles()
            for style_id, info in styles.items():
                print(f"  • {style_id}: {info['description']}")
            return
        
        # Lister les modèles si demandé
        if args.list_models:
            print("\n📋 Modèles disponibles:")
            models = generator.get_available_models()
            for model_id, info in models.items():
                print(f"  • {model_id}: {info['name']} - {info['description']}")
                print(f"    Coût entrée: ${info['input_cost']}/1K tokens, Sortie: ${info['output_cost']}/1K tokens")
            return
        
        # Vérifier que les arguments obligatoires sont présents
        if not args.hook or not args.description:
            parser.error("Les arguments 'hook' et 'description' sont requis sauf pour --list-styles ou --list-models.")
        
        # Afficher les informations de la génération
        print(f"🎯 Hook: {args.hook}")
        print(f"📄 Description: {args.description}")
        print(f"🎨 Style: {args.style}")
        print(f"🤖 Modèle: {args.model}")
        print(f"📊 Nombre de prompts: {args.num}")
        print(f"🌍 Langue: {args.language}")
        
        if args.multi_style:
            print("\n🔄 Génération multi-styles...")
            # Styles par défaut pour la génération multi-styles
            default_styles = ["realistic", "commercial", "photographic"]
            all_prompts = generator.generate_multiple_styles(
                hook=args.hook,
                description=args.description,
                styles=default_styles,
                num_prompts=args.num,
                model=args.model
            )
            
            print(f"\n✅ Génération terminée pour {len(all_prompts)} styles:")
            for style, prompts in all_prompts.items():
                print(f"\n🎨 Style '{style}' ({len(prompts)} prompts):")
                for i, prompt in enumerate(prompts, 1):
                    print(f"  📸 Prompt {i}:")
                    print(f"    Style: {prompt['style']}")
                    print(f"    Prompt: {prompt['prompt']}")
                    print(f"    Éléments: {', '.join(prompt['elements'])}")
                    print(f"    Description: {prompt['description']}")
                    print()
        else:
            print(f"\n🔄 Génération en cours...")
            prompts = generator.generate_prompts(
                hook=args.hook,
                description=args.description,
                num_prompts=args.num,
                style=args.style,
                model=args.model,
                language=args.language
            )
            
            print(f"\n✅ {len(prompts)} prompts générés:")
            for i, prompt in enumerate(prompts, 1):
                print(f"\n📸 Prompt {i}:")
                print(f"  Style: {prompt['style']}")
                print(f"  🎯 PROMPT COMPLET (prêt à copier-coller):")
                print(f"  {'='*50}")
                print(f"  {prompt['prompt']}")
                print(f"  {'='*50}")
                print(f"  🔍 Éléments: {', '.join(prompt['elements'])}")
                print(f"  📄 Description: {prompt['description']}")
                print()
        
        print("\n" + "="*60)
        print("✅ Génération terminée avec succès!")
        print("💾 Les prompts ont été sauvegardés dans le dossier 'generated/prompts/'")
        print("📝 Format JSON: pour traitement programmatique")
        print("📄 Format TXT: pour utilisation directe (copier-coller)")
        print("🎯 Vous pouvez maintenant copier-coller les prompts dans DALL-E, Midjourney, etc.")
        print("="*60)
        
    except ValueError as e:
        print(f"❌ Erreur de configuration: {e}")
        print("💡 Assurez-vous d'avoir défini OPENAI_API_KEY dans votre fichier .env")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Génération interrompue par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 