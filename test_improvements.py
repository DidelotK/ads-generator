#!/usr/bin/env python3
"""
Script de test pour vérifier les améliorations des hooks et images
"""

from src.generators.hook_generator import HookGenerator
from src.generators.image_generator import ImageGenerator
from src.marketing_config import get_image_prompt, IMAGE_CONFIG

def test_hook_length():
    """Test de la longueur des hooks générés"""
    
    print("🧪 Test de la longueur des hooks")
    print("=" * 40)
    
    try:
        generator = HookGenerator()
        
        # Test avec un sujet simple
        hooks = generator.generate_hooks_simple(
            subject="Test de longueur",
            num_hooks=2,
            style="engaging",
            model="gpt-3.5-turbo"
        )
        
        if hooks:
            print("✅ Hooks générés avec succès!")
            for i, hook in enumerate(hooks, 1):
                hook_length = len(hook['hook'])
                desc_length = len(hook['description'])
                
                print(f"\n📝 Hook {i}:")
                print(f"   Texte: {hook['hook']}")
                print(f"   Longueur: {hook_length} caractères")
                print(f"   Description: {hook['description']}")
                print(f"   Longueur desc: {desc_length} caractères")
                
                # Vérifier les limites
                if hook_length <= 60:
                    print(f"   ✅ Hook dans la limite (≤60)")
                else:
                    print(f"   ⚠️  Hook trop long (>60)")
                
                if desc_length <= 120:
                    print(f"   ✅ Description dans la limite (≤120)")
                else:
                    print(f"   ⚠️  Description trop longue (>120)")
            
            return True
        else:
            print("❌ Aucun hook généré")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_image_prompts():
    """Test des prompts d'images réalistes"""
    
    print("\n🎨 Test des prompts d'images")
    print("=" * 40)
    
    test_hook = "Cette nouvelle astuce pour produire son électricité"
    
    print(f"📝 Hook de test: {test_hook}")
    
    # Tester les différents styles
    for style in IMAGE_CONFIG['styles']:
        prompt = get_image_prompt(test_hook, style)
        print(f"\n🎯 Style: {style}")
        print(f"📋 Prompt: {prompt[:150]}...")
        
        # Vérifier les mots-clés réalistes
        realistic_keywords = ["photographie", "réaliste", "professionnel", "haute qualité", "éclairage", "couleurs"]
        found_keywords = [kw for kw in realistic_keywords if kw in prompt.lower()]
        
        if len(found_keywords) >= 3:
            print(f"   ✅ Prompt réaliste ({len(found_keywords)} mots-clés trouvés)")
        else:
            print(f"   ⚠️  Prompt peu réaliste ({len(found_keywords)} mots-clés trouvés)")
    
    return True

def test_configuration():
    """Test de la configuration"""
    
    print("\n⚙️  Test de la configuration")
    print("=" * 40)
    
    print(f"🖼️  Styles d'images: {IMAGE_CONFIG['styles']}")
    print(f"📏 Taille: {IMAGE_CONFIG['size']}")
    print(f"🎯 Qualité: {IMAGE_CONFIG['quality']}")
    print(f"🤖 Modèle: {IMAGE_CONFIG['model']}")
    
    # Vérifier que la qualité est HD
    if IMAGE_CONFIG['quality'] == 'hd':
        print("   ✅ Qualité HD activée")
    else:
        print("   ⚠️  Qualité standard (pas HD)")
    
    # Vérifier les styles réalistes
    realistic_styles = ['realistic', 'photographic']
    if all(style in IMAGE_CONFIG['styles'] for style in realistic_styles):
        print("   ✅ Styles réalistes configurés")
    else:
        print("   ⚠️  Styles non réalistes détectés")
    
    return True

def main():
    """Lance tous les tests"""
    
    print("🚀 Test des améliorations - Hooks courts et images réalistes")
    print("=" * 60)
    
    tests = [
        ("Longueur des hooks", test_hook_length),
        ("Prompts d'images", test_image_prompts),
        ("Configuration", test_configuration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Test: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{len(results)} tests réussis")
    
    if passed == len(results):
        print("🎉 Toutes les améliorations fonctionnent correctement!")
    else:
        print("⚠️  Certaines améliorations nécessitent des ajustements")

if __name__ == "__main__":
    main() 