#!/usr/bin/env python3
"""
Script de test pour la fonction generate_marketing_resources
"""

import sys
import os
from unittest.mock import patch, MagicMock
from pathlib import Path
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../examples'))

from example_marketing_hooks import generate_marketing_resources

def test_marketing_resources():
    """Test de la génération de ressources marketing"""
    
    print("🧪 Test de la fonction generate_marketing_resources")
    print("=" * 50)
    
    # Test avec 2 ressources
    print("🎯 Test avec 2 ressources...")
    resources = generate_marketing_resources(num_resources=2)
    assert resources and len(resources) == 2, "Nombre de ressources incorrect"
    for resource in resources:
        assert 'hook' in resource and 'subject' in resource and 'style' in resource, "Champs manquants dans la ressource"
        images = resource.get('images', [])
        image_paths = [str(img) if hasattr(img, '__str__') else img for img in images]
        assert isinstance(image_paths, list)

def test_different_quantities():
    """Test avec différentes quantités - version mockée pour accélération"""
    
    from src.generators.hook_generator import HookGenerator
    from src.generators.image_generator import ImageGenerator
    
    original_hook_method = HookGenerator.generate_hooks_simple
    original_image_method = ImageGenerator.generate_image
    original_sleep = time.sleep
    
    def mock_generate_hooks(*args, **kwargs):
        return [{
            'hook': 'Hook de test mocké',
            'description': 'Description de test mockée'
        }]
    def mock_generate_image(*args, **kwargs):
        return Path('generated/images/mock_image.png')
    def mock_sleep(seconds):
        return None
    
    HookGenerator.generate_hooks_simple = mock_generate_hooks
    ImageGenerator.generate_image = mock_generate_image
    time.sleep = mock_sleep
    
    try:
        test_quantities = [1, 3, 5]
        for quantity in test_quantities:
            resources = generate_marketing_resources(num_resources=quantity)
            assert resources and len(resources) == quantity, f"Échec pour {quantity} ressource(s)"
    finally:
        HookGenerator.generate_hooks_simple = original_hook_method
        ImageGenerator.generate_image = original_image_method
        time.sleep = original_sleep

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