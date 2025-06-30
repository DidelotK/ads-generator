#!/usr/bin/env python3
"""
Script de test pour le générateur de hooks
"""

from src.generators.hook_generator import HookGenerator

def test_hook_generation():
    """Test simple de génération de hooks"""
    
    print("🧪 Test du générateur de hooks")
    print("=" * 40)
    
    try:
        # Initialiser le générateur
        generator = HookGenerator()
        
        # Test avec un sujet simple
        print("🎯 Test de génération d'un hook...")
        hooks = generator.generate_hooks_simple(
            subject="Test de génération",
            num_hooks=1,
            style="engaging",
            model="gpt-3.5-turbo"
        )
        
        if hooks and len(hooks) > 0:
            print("✅ Test réussi!")
            print(f"📝 Hook généré: {hooks[0]['hook']}")
            print(f"📋 Description: {hooks[0]['description']}")
            return True
        else:
            print("❌ Aucun hook généré")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    success = test_hook_generation()
    if success:
        print("\n🎉 Le générateur fonctionne correctement!")
    else:
        print("\n💥 Le générateur a des problèmes") 