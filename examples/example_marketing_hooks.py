#!/usr/bin/env python3
"""
Exemple de génération de hooks marketing et d'images associées
Génère des accroches dans un ton très marketing pour des publicités
"""

from src.generators.hook_generator import HookGenerator
from src.generators.image_generator import ImageGenerator
from src.marketing_config import (
    get_marketing_subjects, 
    get_marketing_styles, 
    get_image_prompt,
    IMAGE_CONFIG,
    HOOK_CONFIG,
    MARKETING_SUBJECTS,
    MARKETING_STYLES
)
import time
import random

def generate_marketing_resources(num_resources=5):
    """
    Génère un nombre spécifié de ressources marketing (hook + images)
    
    Args:
        num_resources (int): Nombre de ressources à générer (1 ressource = 1 hook + ses images)
    
    Returns:
        list: Liste des ressources générées avec hooks et images
    """
    
    print(f"🎯 Génération de {num_resources} ressources marketing")
    print("=" * 60)
    
    # Initialiser les générateurs
    hook_generator = HookGenerator()
    image_generator = ImageGenerator()
    
    # Sélectionner automatiquement les sujets et styles
    # Utiliser tous les sujets disponibles et en répéter si nécessaire
    all_subjects = MARKETING_SUBJECTS
    all_styles = MARKETING_STYLES
    
    # Mélanger les listes pour plus de variété
    random.shuffle(all_subjects)
    random.shuffle(all_styles)
    
    # Sélectionner les sujets et styles nécessaires
    selected_subjects = []
    selected_styles = []
    
    for i in range(num_resources):
        # Utiliser le modulo pour répéter les listes si nécessaire
        subject = all_subjects[i % len(all_subjects)]
        style = all_styles[i % len(all_styles)]
        
        selected_subjects.append(subject)
        selected_styles.append(style)
    
    print(f"📝 Sujets sélectionnés: {len(selected_subjects)}")
    print(f"🎨 Styles sélectionnés: {len(selected_styles)}")
    
    all_resources = []
    
    # Générer les ressources
    for i, (subject, style) in enumerate(zip(selected_subjects, selected_styles)):
        print(f"\n{i+1}/{num_resources} - Génération pour: {subject}")
        print(f"   Style: {style}")
        
        # Générer le hook
        hooks = hook_generator.generate_hooks_simple(
            subject=subject,
            num_hooks=HOOK_CONFIG["num_hooks_per_subject"],
            style=style,
            model=HOOK_CONFIG["model"],
            language=HOOK_CONFIG["language"]
        )
        
        if hooks:
            hook_data = hooks[0]
            hook_data['subject'] = subject
            hook_data['style'] = style
            hook_data['images'] = []
            
            print(f"✅ Hook généré: {hook_data['hook']}")
            
            # Générer les images pour ce hook
            print(f"🎨 Génération de {len(IMAGE_CONFIG['styles'])} images...")
            
            for j, image_style in enumerate(IMAGE_CONFIG['styles']):
                print(f"  🎨 Image {j+1}/{len(IMAGE_CONFIG['styles'])} - Style: {image_style}")
                
                # Créer un prompt d'image personnalisé
                image_prompt = get_image_prompt(hook_data['hook'], image_style)
                
                image_filename = image_generator.generate_image(
                    subject_type="marketing",
                    prompt=image_prompt,
                    style=image_style,
                    size=IMAGE_CONFIG['size'],
                    quality=IMAGE_CONFIG['quality'],
                    model=IMAGE_CONFIG['model']
                )
                
                if image_filename:
                    print(f"  ✅ Image générée: {image_filename}")
                    hook_data['images'].append(image_filename)
                else:
                    print(f"  ❌ Échec de génération d'image {j+1}")
                
                # Pause entre les générations pour éviter les limites d'API
                if j < len(IMAGE_CONFIG['styles']) - 1:
                    time.sleep(2)
            
            all_resources.append(hook_data)
            
            # Pause entre les ressources
            if i < num_resources - 1:
                time.sleep(3)
        else:
            print(f"❌ Échec de génération pour: {subject}")
    
    # Afficher le résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ FINAL")
    print("=" * 60)
    
    total_images = sum(len(resource.get('images', [])) for resource in all_resources)
    
    print(f"🎯 Ressources générées: {len(all_resources)}")
    print(f"📸 Images générées: {total_images}")
    
    print("\n📋 Détail des ressources:")
    for i, resource in enumerate(all_resources, 1):
        print(f"\n{i}. {resource['hook']}")
        print(f"   Sujet: {resource['subject']}")
        print(f"   Style: {resource['style']}")
        print(f"   Description: {resource['description']}")
        if 'images' in resource and resource['images']:
            print(f"   Images: {', '.join(str(img) for img in resource['images'])}")
        else:
            print(f"   Images: Aucune générée")
    
    print(f"\n✅ Génération terminée!")
    print(f"💾 Hooks sauvegardés dans: generated/hooks/")
    print(f"🖼️  Images sauvegardées dans: generated/images/")
    print(f"\n💡 Ces ressources sont prêtes pour vos campagnes publicitaires!")
    print(f"💡 Utilisez-les dans vos ads pour maximiser les clics vers vos landing pages.")
    
    # Afficher des suggestions d'utilisation
    print(f"\n🎯 SUGGESTIONS D'UTILISATION:")
    print(f"📱 Facebook Ads: Utilisez les hooks avec les images réalistes")
    print(f"🔍 Google Ads: Utilisez les hooks avec les images photographiques")
    print(f"📧 Email Marketing: Adaptez les hooks pour vos campagnes email")
    print(f"🌐 Landing Pages: Utilisez les images pour vos pages de destination")
    
    return all_resources

def main():
    """Génère des hooks marketing et des images associées"""
    
    print("🎯 Générateur de Hooks Marketing et Images")
    print("=" * 60)
    
    # Utiliser la nouvelle fonction avec 5 ressources
    resources = generate_marketing_resources(num_resources=5)
    
    print(f"\n🎉 Génération terminée avec {len(resources)} ressources!")

if __name__ == "__main__":
    main() 