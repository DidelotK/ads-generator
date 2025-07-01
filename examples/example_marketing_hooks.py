#!/usr/bin/env python3
"""
Exemple d'utilisation pour générer des ressources marketing complètes
Combine la génération de hooks et d'images pour créer des campagnes publicitaires
"""

import sys
import os
import time
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from generators.hook_generator import HookGenerator
from generators.image_generator import ImageGenerator
from marketing_config import get_marketing_subjects, HookStyle, MARKETING_STYLES

def generate_marketing_resources(num_resources=3):
    """
    Génère des ressources marketing complètes (hooks + images)
    
    Args:
        num_resources (int): Nombre de ressources à générer
        
    Returns:
        list: Liste de dictionnaires contenant hook, subject, style et images
    """
    print(f"🚀 Génération de {num_resources} ressource(s) marketing complète(s)")
    print("=" * 60)
    
    # Initialiser les générateurs
    hook_generator = HookGenerator()
    image_generator = ImageGenerator()
    
    # Récupérer les sujets et styles
    subjects = get_marketing_subjects(num_resources)
    styles = MARKETING_STYLES[:num_resources]
    
    resources = []
    
    for i in range(num_resources):
        print(f"\n📝 Génération de la ressource {i+1}/{num_resources}")
        
        # Sélectionner le sujet et le style
        subject = subjects[i % len(subjects)]
        style = styles[i % len(styles)]
        
        print(f"   Sujet: {subject}")
        print(f"   Style: {style}")
        
        try:
            # Générer le hook
            print("   🎯 Génération du hook...")
            hooks = hook_generator.generate_hooks_simple(
                subject=subject,
                num_hooks=1,
                style=style,
                model="gpt-3.5-turbo"
            )
            
            if not hooks:
                print("   ❌ Échec de la génération du hook")
                continue
                
            hook_data = hooks[0]
            hook_text = hook_data['hook']
            
            print(f"   ✅ Hook généré: {hook_text[:50]}...")
            
            # Générer l'image basée sur le hook
            print("   🎨 Génération de l'image...")
            
            # Attendre un peu pour éviter les limites de taux
            time.sleep(1)
            
            image_path = image_generator.generate_image(
                prompt=hook_text,
                style="realistic",
                size="1024x1024",
                quality="hd"
            )
            
            print(f"   ✅ Image générée: {image_path}")
            
            # Créer la ressource complète
            resource = {
                'hook': hook_text,
                'subject': subject,
                'style': style,
                'description': hook_data.get('description', ''),
                'images': [image_path]
            }
            
            resources.append(resource)
            print(f"   🎉 Ressource {i+1} terminée")
            
        except Exception as e:
            print(f"   ❌ Erreur lors de la génération: {e}")
            continue
    
    print(f"\n🎯 Génération terminée: {len(resources)}/{num_resources} ressources créées")
    return resources

def main():
    """Fonction principale pour tester la génération de ressources"""
    print("🚀 Exemple de génération de ressources marketing")
    print("=" * 60)
    
    # Générer 2 ressources pour l'exemple
    resources = generate_marketing_resources(num_resources=2)
    
    # Afficher les résultats
    print("\n📊 RESSOURCES GÉNÉRÉES")
    print("=" * 60)
    
    for i, resource in enumerate(resources, 1):
        print(f"\n🎯 Ressource {i}:")
        print(f"   Sujet: {resource['subject']}")
        print(f"   Style: {resource['style']}")
        print(f"   Hook: {resource['hook']}")
        print(f"   Description: {resource['description']}")
        print(f"   Images: {', '.join(str(img) for img in resource['images'])}")

if __name__ == "__main__":
    main() 