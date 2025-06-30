#!/usr/bin/env python3
"""
Script pour générer des accroches avec l'API OpenAI (ChatGPT)
"""

import sys
import argparse
from src.generators.hook_generator import HookGenerator
from src.marketing_config import HookStyle

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Générateur d'accroches avec l'API OpenAI")
    parser.add_argument("--subject", "-s",
                       help="Sujet pour lequel générer les accroches")
    parser.add_argument("--num-hooks", "-n", type=int, default=5,
                       help="Nombre d'accroches à générer (défaut: 5)")
    parser.add_argument("--style", default=HookStyle.ENGAGING.value,
                       choices=[s.value for s in HookStyle],
                       help="Style des accroches")
    parser.add_argument("--model", "-m", default="gpt-3.5-turbo",
                       choices=["gpt-4", "gpt-3.5-turbo"],
                       help="Modèle à utiliser")
    parser.add_argument("--language", "-l", default="français",
                       help="Langue de génération")
    parser.add_argument("--multiple-styles", action="store_true",
                       help="Générer dans plusieurs styles")
    parser.add_argument("--api-key", help="Clé API OpenAI (optionnel si dans .env)")
    parser.add_argument("--list-models", action="store_true",
                       help="Afficher la liste des modèles disponibles avec leurs tarifs")
    
    args = parser.parse_args()
    
    try:
        # Initialiser le générateur
        generator = HookGenerator(api_key=args.api_key)
        
        # Afficher les modèles disponibles si demandé
        if args.list_models:
            print("🤖 Modèles disponibles:")
            print("=" * 50)
            models = generator.get_available_models()
            for model_id, info in models.items():
                print(f"\n📋 {info['name']} ({model_id})")
                print(f"   Description: {info['description']}")
                print(f"   Coût entrée: ${info['input_cost']:.4f} USD par 1K tokens")
                print(f"   Coût sortie: ${info['output_cost']:.4f} USD par 1K tokens")
                print(f"   Tokens max: {info['max_tokens']}")
            return
        
        # Vérifier que le sujet est fourni si pas de list-models
        if not args.subject:
            print("❌ Erreur: L'argument --subject/-s est requis pour générer des accroches.")
            print("💡 Utilisez --list-models pour voir les modèles disponibles.")
            sys.exit(1)
        
        if args.multiple_styles:
            # Générer dans plusieurs styles
            styles = HookStyle.get_default_styles()
            results = generator.generate_multiple_styles(
                args.subject, 
                styles, 
                args.num_hooks, 
                args.model
            )
            
            print(f"\n🎉 Génération terminée! {len(results)} styles créés:")
            for style, hooks in results.items():
                print(f"  • {style}: {len(hooks)} accroches")
        else:
            # Générer des accroches dans un style
            hooks = generator.generate_hooks(
                subject=args.subject,
                num_hooks=args.num_hooks,
                style=args.style,
                model=args.model,
                language=args.language
            )
            
            if hooks:
                print(f"\n🎉 {len(hooks)} accroches générées avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 