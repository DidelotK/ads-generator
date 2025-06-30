#!/usr/bin/env python3
"""
Script de test pour la fonction generate_marketing_resources
"""

from examples.example_marketing_hooks import generate_marketing_resources

def test_marketing_resources():
    """Test de la génération de ressources marketing"""
    
    print("🧪 Test de la fonction generate_marketing_resources")
    print("=" * 50)
    
    # Test avec 2 ressources
    print("🎯 Test avec 2 ressources...")
    try:
        resources = generate_marketing_resources(num_resources=2)
        
        if resources and len(resources) == 2:
            print("✅ Test réussi!")
            print(f"📊 {len(resources)} ressources générées")
            
            for i, resource in enumerate(resources, 1):
                print(f"\n📝 Ressource {i}:")
                print(f"   Hook: {resource['hook']}")
                print(f"   Sujet: {resource['subject']}")
                print(f"   Style: {resource['style']}")
                print(f"   Images: {len(resource.get('images', []))}")
            
            return True
        else:
            print("❌ Nombre de ressources incorrect")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_different_quantities():
    """Test avec différentes quantités"""
    
    print("\n🧪 Test avec différentes quantités")
    print("=" * 50)
    
    test_quantities = [1, 3, 5]
    
    for quantity in test_quantities:
        print(f"\n🎯 Test avec {quantity} ressource(s)...")
        try:
            resources = generate_marketing_resources(num_resources=quantity)
            
            if resources and len(resources) == quantity:
                print(f"✅ {quantity} ressource(s) générée(s) avec succès")
            else:
                print(f"❌ Échec pour {quantity} ressource(s)")
                return False
                
        except Exception as e:
            print(f"❌ Erreur pour {quantity} ressource(s): {e}")
            return False
    
    return True

def main():
    """Lance tous les tests"""
    
    print("🚀 Test de la fonction generate_marketing_resources")
    print("=" * 60)
    
    tests = [
        ("Test basique", test_marketing_resources),
        ("Test quantités", test_different_quantities)
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
        print("🎉 La fonction generate_marketing_resources fonctionne correctement!")
    else:
        print("⚠️  Certains tests ont échoué")

if __name__ == "__main__":
    main() 