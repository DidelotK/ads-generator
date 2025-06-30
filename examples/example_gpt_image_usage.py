#!/usr/bin/env python3
"""
Exemple d'utilisation du générateur d'images avec GPT-Image-1
GPT-Image-1 offre une qualité d'image supérieure à DALL-E
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(str(Path(__file__).parent.parent))

from src.generators.image_generator import ImageGenerator
from src.marketing_config import ImageStyle

def main():
    """Exemple d'utilisation de GPT-Image-1 pour la génération d'images"""
    
    print("🎨 Exemple d'utilisation de GPT-Image-1 pour la génération d'images")
    print("=" * 60)
    
    try:
        # Initialiser le générateur
        generator = ImageGenerator()
        
        # Afficher les modèles disponibles
        print("\n📋 Modèles disponibles:")
        models = generator.get_available_models()
        for model_id, info in models.items():
            print(f"  • {info['name']} ({model_id}) - {info['description']}")
        
        print("\n🎨 Génération d'image avec GPT-Image-1 (qualité supérieure)...")
        
        # Exemple 1: Image réaliste avec GPT-Image-1
        print("\n1️⃣ Génération d'un chat réaliste avec GPT-Image-1:")
        filename1 = generator.generate_image(
            subject_type="chat",
            prompt="Un chat persan blanc assis sur un coussin rouge, éclairage doux",
            style=ImageStyle.REALISTIC.value,
            size="1024x1536",  # Résolution élevée
            quality="hd",
            model="gpt-image-1"
        )
        
        if filename1:
            print(f"✅ Image générée: {filename1}")
        
        # Exemple 2: Image artistique avec GPT-Image-1
        print("\n2️⃣ Génération d'un paysage artistique avec GPT-Image-1:")
        filename2 = generator.generate_image(
            subject_type="paysage",
            prompt="Montagnes enneigées au coucher du soleil, style réaliste",
            style=ImageStyle.ARTISTIC.value,
            size="1536x1024",
            quality="hd",
            model="gpt-image-1"
        )
        
        if filename2:
            print(f"✅ Image générée: {filename2}")
        
        # Exemple 3: Comparaison GPT-Image-1 vs DALL-E 3
        print("\n3️⃣ Comparaison GPT-Image-1 vs DALL-E 3:")
        
        # Avec GPT-Image-1
        print("   🎨 Génération avec GPT-Image-1...")
        filename_gpt = generator.generate_image(
            subject_type="portrait",
            prompt="Portrait d'une femme avec des cheveux roux, éclairage dramatique",
            style=ImageStyle.REALISTIC.value,
            size="1024x1024",
            quality="hd",
            model="gpt-image-1"
        )
        
        # Avec DALL-E 3
        print("   🎨 Génération avec DALL-E 3...")
        filename_dalle = generator.generate_image(
            subject_type="portrait",
            prompt="Portrait d'une femme avec des cheveux roux, éclairage dramatique",
            style=ImageStyle.REALISTIC.value,
            size="1024x1024",
            quality="hd",
            model="dall-e-3"
        )
        
        print(f"   ✅ GPT-Image-1: {filename_gpt}")
        print(f"   ✅ DALL-E 3: {filename_dalle}")
        
        # Exemple 4: Génération multiple avec GPT-Image-1
        print("\n4️⃣ Génération multiple avec GPT-Image-1:")
        results = generator.generate_multiple_styles(
            subject_type="chien",
            prompt="Un golden retriever jouant dans un parc",
            styles=[ImageStyle.REALISTIC.value, ImageStyle.CARTOON.value, ImageStyle.ARTISTIC.value],
            model="gpt-image-1",
            size="1024x1024",
            quality="hd"
        )
        
        print(f"✅ {len(results)} images générées avec GPT-Image-1:")
        for style, filename in results:
            print(f"   • {style}: {filename}")
        
        print("\n🎉 Tous les exemples terminés!")
        print("\n💡 Conseils pour GPT-Image-1:")
        print("   • GPT-Image-1 excelle dans les prompts détaillés")
        print("   • Utilisez des descriptions précises pour de meilleurs résultats")
        print("   • Les tailles élevées (1024x1536, 1536x1024) offrent la meilleure qualité")
        print("   • GPT-Image-1 est le modèle le plus récent et produit des images de qualité supérieure")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 