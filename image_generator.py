#!/usr/bin/env python3
"""
Script pour générer des images avec l'API OpenAI (GPT-Image-1, DALL-E)
"""

import sys
import argparse
from src.generators.image_generator import ImageGenerator
from src.marketing_config import ImageStyle

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Générateur d'images avec l'API OpenAI")
    parser.add_argument("--prompt", "-p", help="Description personnalisée de l'image")
    parser.add_argument("--style", "-s", default=ImageStyle.REALISTIC.value, 
                       choices=[s.value for s in ImageStyle],
                       help="Style de l'image")
    parser.add_argument("--size", default="1024x1024",
                       choices=["256x256", "512x512", "1024x1024", "1024x1536", "1536x1024", "1792x1024", "1024x1792", "auto"],
                       help="Taille de l'image")
    parser.add_argument("--quality", default="standard",
                       choices=["standard", "hd"],
                       help="Qualité de l'image")
    parser.add_argument("--model", "-m", default="gpt-image-1",
                       choices=["gpt-image-1", "dall-e-3", "dall-e-2"],
                       help="Modèle à utiliser (gpt-image-1 pour la meilleure qualité)")
    parser.add_argument("--multiple", action="store_true",
                       help="Générer dans plusieurs styles")
    parser.add_argument("--api-key", help="Clé API OpenAI (optionnel si dans .env)")
    parser.add_argument("--list-models", action="store_true",
                       help="Afficher la liste des modèles disponibles avec leurs tarifs")
    
    args = parser.parse_args()
    
    try:
        # Initialiser le générateur
        generator = ImageGenerator(api_key=args.api_key)
        
        # Afficher les modèles disponibles si demandé
        if args.list_models:
            print("🤖 Modèles disponibles:")
            print("=" * 50)
            models = generator.get_available_models()
            for model_id, info in models.items():
                print(f"\n📋 {info['name']} ({model_id})")
                print(f"   Description: {info['description']}")
                print(f"   Type: {info['type']}")
                print(f"   Tailles supportées: {', '.join(info['supported_sizes'])}")
                print(f"   Qualités supportées: {', '.join(info['supported_qualities'])}")
                print("   Tarifs:")
                for size, qualities in info['pricing'].items():
                    for quality, price in qualities.items():
                        print(f"     • {size} ({quality}): ${price:.3f} USD")
            return
        
        if args.multiple:
            # Générer dans plusieurs styles
            styles = ImageStyle.get_default_styles()
            results = generator.generate_multiple_styles(
                args.prompt, 
                styles, 
                args.model, 
                args.size, 
                args.quality
            )
            
            print(f"\n🎉 Génération terminée! {len(results)} images créées:")
            for style, filename in results:
                print(f"  • {style}: {filename}")
        else:
            # Générer une seule image
            filename = generator.generate_image(
                prompt=args.prompt,
                style=args.style,
                size=args.size,
                quality=args.quality,
                model=args.model
            )
            
            if filename:
                print(f"\n🎉 Image générée avec succès: {filename}")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
