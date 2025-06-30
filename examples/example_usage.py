#!/usr/bin/env python3
"""
Exemples d'utilisation du générateur d'images avec différents modèles
"""

from src.generators.image_generator import ImageGenerator
from src.marketing_config import ImageStyle

def main():
    """Exemples d'utilisation"""
    
    # Initialiser le générateur
    generator = ImageGenerator()
    
    print("🎨 Exemples d'utilisation du générateur d'images")
    print("=" * 60)
    
    # Afficher les modèles disponibles
    print("\n1️⃣  Modèles disponibles:")
    models = generator.get_available_models()
    for model_id, info in models.items():
        print(f"   • {info['name']} ({model_id})")
        print(f"     Description: {info['description']}")
        print(f"     Tarifs: {', '.join([f'${list(qualities.values())[0]:.3f}' for qualities in info['pricing'].values()])}")
    
    print("\n" + "=" * 60)
    
    # Exemple 1: Génération avec GPT IMAGE 1 (modèle par défaut)
    print("\n2️⃣  Exemple avec GPT IMAGE 1 (haute qualité):")
    print("   Génération d'un chat réaliste en HD...")
    
    # Note: Décommentez les lignes suivantes pour tester
    # filename = generator.generate_image(
    #     subject_type="chat",
    #     prompt="Un chat persan élégant assis sur un coussin de velours",
    #     style=ImageStyle.REALISTIC.value,
    #     size="1024x1024",
    #     quality="hd",
    #     model="gpt-image-1"
    # )
    
    # Exemple 2: Génération avec DALL-E 2 (moins cher)
    print("\n3️⃣  Exemple avec DALL-E 2 (économique):")
    print("   Génération d'un chat cartoon en 512x512...")
    
    # Note: Décommentez les lignes suivantes pour tester
    # filename = generator.generate_image(
    #     subject_type="chat",
    #     prompt="Un chaton mignon jouant avec une pelote de laine",
    #     style=ImageStyle.CARTOON.value,
    #     size="512x512",
    #     quality="standard",
    #     model="dall-e-2"
    # )
    
    # Exemple 3: Génération multiple avec GPT IMAGE 1
    print("\n4️⃣  Exemple de génération multiple:")
    print("   Génération de 4 styles différents...")
    
    # Note: Décommentez les lignes suivantes pour tester
    # results = generator.generate_multiple_styles(
    #     subject_type="chat",
    #     prompt="Un chat élégant dans un salon luxueux",
    #     styles=[ImageStyle.REALISTIC.value, ImageStyle.CARTOON.value, ImageStyle.ARTISTIC.value, ImageStyle.CUTE.value],
    #     model="gpt-image-1",
    #     size="1024x1024",
    #     quality="standard"
    # )
    
    print("\n✅ Exemples terminés!")
    print("\n💡 Pour tester réellement, décommentez les lignes dans le code.")
    print("💡 Utilisez --list-models pour voir tous les modèles disponibles:")
    print("   python chat_image_generator.py --list-models")

if __name__ == "__main__":
    main() 