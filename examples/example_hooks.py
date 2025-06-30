#!/usr/bin/env python3
"""
Exemples d'utilisation du générateur d'accroches
"""

from src.generators.hook_generator import HookGenerator

def main():
    """Exemples d'utilisation"""
    
    # Initialiser le générateur
    generator = HookGenerator()
    
    print("🎯 Exemples d'utilisation du générateur d'accroches")
    print("=" * 60)
    
    # Afficher les modèles disponibles
    print("\n1️⃣  Modèles disponibles:")
    models = generator.get_available_models()
    for model_id, info in models.items():
        print(f"   • {info['name']} ({model_id})")
        print(f"     Description: {info['description']}")
        print(f"     Coût: ${info['input_cost']:.4f} entrée, ${info['output_cost']:.4f} sortie par 1K tokens")
    
    print("\n" + "=" * 60)
    
    # Exemple 1: Génération d'accroches engageantes
    print("\n2️⃣  Exemple: Accroches engageantes pour un produit tech")
    print("   Génération de 3 accroches engageantes...")
    
    # Note: Décommentez les lignes suivantes pour tester
    hooks = generator.generate_hooks(
        subject="Application mobile de fitness",
        num_hooks=3,
        style="engaging",
        model="gpt-3.5-turbo"
    )
    
    # Exemple 2: Génération d'accroches professionnelles
    print("\n3️⃣  Exemple: Accroches professionnelles pour un service B2B")
    print("   Génération de 2 accroches professionnelles...")
    
    # Note: Décommentez les lignes suivantes pour tester
    # hooks = generator.generate_hooks(
    #     subject="Solution de gestion de projet pour entreprises",
    #     num_hooks=2,
    #     style="professional",
    #     model="gpt-4"
    # )
    
    # Exemple 3: Génération d'accroches créatives
    print("\n4️⃣  Exemple: Accroches créatives pour un restaurant")
    print("   Génération de 3 accroches créatives...")
    
    # Note: Décommentez les lignes suivantes pour tester
    # hooks = generator.generate_hooks(
    #     subject="Restaurant gastronomique fusion asiatique",
    #     num_hooks=3,
    #     style="creative",
    #     model="gpt-3.5-turbo"
    # )
    
    # Exemple 4: Génération multiple de styles
    print("\n5️⃣  Exemple: Génération multiple de styles")
    print("   Génération de 2 accroches par style...")
    
    # Note: Décommentez les lignes suivantes pour tester
    # results = generator.generate_multiple_styles(
    #     subject="Formation en ligne de marketing digital",
    #     styles=["engaging", "professional", "emotional"],
    #     num_hooks=2,
    #     model="gpt-3.5-turbo"
    # )
    
    print("\n✅ Exemples terminés!")
    print("\n💡 Pour tester réellement, décommentez les lignes dans le code.")
    print("💡 Utilisez --list-models pour voir tous les modèles disponibles:")
    print("   python hook_generator.py --list-models")
    print("\n💡 Exemple d'utilisation en ligne de commande:")
    print("   python hook_generator.py --subject 'Application mobile' --num-hooks 3 --style engaging")

if __name__ == "__main__":
    main() 