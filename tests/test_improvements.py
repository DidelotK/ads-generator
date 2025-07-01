#!/usr/bin/env python3
"""
Script de test pour vérifier les améliorations des hooks et images
"""

import sys
import os
from unittest.mock import Mock, patch

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.generators.hook_generator import HookGenerator
from src.generators.image_generator import ImageGenerator, ImageStyle
from src.marketing_config import get_image_prompt, IMAGE_CONFIG, HookStyle

@patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
@patch('src.generators.hook_generator.openai.OpenAI')
def test_hook_length(mock_openai):
    """Test de la longueur des hooks générés"""
    
    # Mock de l'API OpenAI
    mock_client = Mock()
    mock_openai.return_value = mock_client
    
    # Mock de la réponse avec hooks courts
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = '''{
        "hooks": [
            {
                "hook": "Astuce révolutionnaire",
                "description": "Une méthode simple et efficace pour économiser"
            },
            {
                "hook": "Secret énergétique",
                "description": "La technique cachée des experts"
            }
        ]
    }'''
    mock_response.usage.prompt_tokens = 100
    mock_response.usage.completion_tokens = 50
    mock_response.usage.total_tokens = 150
    mock_client.chat.completions.create.return_value = mock_response
    
    generator = HookGenerator()
    hooks = generator.generate_hooks_simple(
        subject="Test de longueur",
        num_hooks=2,
        style=HookStyle.ENGAGING.value,
        model="gpt-3.5-turbo"
    )
    assert hooks, "Aucun hook généré"
    for hook in hooks:
        assert len(hook['hook']) <= 60, f"Hook trop long: {hook['hook']}"
        assert len(hook['description']) <= 120, f"Description trop longue: {hook['description']}"

def test_image_prompts():
    """Test des prompts d'images réalistes"""
    
    test_hook = "Cette nouvelle astuce pour produire son électricité"
    realistic_keywords = ["photographie", "réaliste", "professionnel", "haute qualité", "éclairage", "couleurs"]
    for style in [ImageStyle.REALISTIC.value]:
        prompt = get_image_prompt(test_hook, style)
        found_keywords = [kw for kw in realistic_keywords if kw in prompt.lower()]
        assert len(found_keywords) >= 3, f"Prompt peu réaliste pour le style {style}: {prompt}"

def test_configuration():
    """Test de la configuration"""
    
    assert IMAGE_CONFIG['quality'] == 'hd', "La qualité n'est pas HD"
    realistic_styles = ['realistic', 'photographic']
    assert all(style in IMAGE_CONFIG['styles'] for style in realistic_styles), "Styles réalistes non configurés"

def main():
    """Lance tous les tests"""
    
    print("🚀 Test des améliorations - Hooks courts et images réalistes")
    print("=" * 60)
    
    tests = [
        ("Longueur des hooks", lambda: test_hook_length()),
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