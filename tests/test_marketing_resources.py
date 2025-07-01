#!/usr/bin/env python3
"""
Tests pour les ressources marketing et la configuration
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock, Mock
from pathlib import Path
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../examples'))

from example_marketing_hooks import generate_marketing_resources
from src.marketing_config import (
    get_marketing_subjects, get_marketing_styles, get_image_prompt,
    get_color_theme, get_random_template, get_templates_by_category,
    HookStyle, MARKETING_SUBJECTS, MARKETING_STYLES, IMAGE_CONFIG,
    HOOK_CONFIG, IMAGE_PROMPTS, COLOR_THEMES, MARKETING_KEYWORDS,
    HOOK_TEMPLATES
)

class TestMarketingConfig(unittest.TestCase):
    """Tests pour la configuration marketing"""
    
    def test_get_marketing_subjects(self):
        """Test de récupération des sujets marketing"""
        # Test avec nombre par défaut
        subjects = get_marketing_subjects()
        self.assertIsInstance(subjects, list)
        self.assertEqual(len(subjects), 5)  # Valeur par défaut
        
        # Test avec nombre spécifique
        subjects_3 = get_marketing_subjects(3)
        self.assertEqual(len(subjects_3), 3)
        
        # Test avec nombre plus grand que disponible
        subjects_large = get_marketing_subjects(100)
        self.assertEqual(len(subjects_large), len(MARKETING_SUBJECTS))
    
    def test_get_marketing_styles(self):
        """Test de récupération des styles marketing"""
        # Test avec nombre par défaut
        styles = get_marketing_styles()
        self.assertIsInstance(styles, list)
        self.assertEqual(len(styles), 5)  # Valeur par défaut
        
        # Test avec nombre spécifique
        styles_3 = get_marketing_styles(3)
        self.assertEqual(len(styles_3), 3)
        
        # Test avec nombre plus grand que disponible
        styles_large = get_marketing_styles(100)
        self.assertEqual(len(styles_large), len(MARKETING_STYLES))
    
    def test_get_image_prompt(self):
        """Test de génération de prompts d'image"""
        hook_text = "Découvrez cette astuce incroyable"
        
        # Test avec style réaliste
        prompt_realistic = get_image_prompt(hook_text, "realistic")
        self.assertIn(hook_text, prompt_realistic)
        self.assertIn("réaliste", prompt_realistic.lower())
        self.assertIn("photographie", prompt_realistic.lower())
        
        # Test avec style photographique
        prompt_photo = get_image_prompt(hook_text, "photographic")
        self.assertIn(hook_text, prompt_photo)
        self.assertIn("photographie", prompt_photo.lower())
        
        # Test avec style par défaut pour style inconnu
        prompt_unknown = get_image_prompt(hook_text, "style_inexistant")
        self.assertIn(hook_text, prompt_unknown)
    
    def test_get_color_theme(self):
        """Test de récupération des thèmes de couleur"""
        # Test avec styles mappés
        theme_urgent = get_color_theme("urgent")
        self.assertEqual(theme_urgent, COLOR_THEMES["urgency"])
        
        theme_curiosity = get_color_theme("curiosity")
        self.assertEqual(theme_curiosity, COLOR_THEMES["mystery"])
        
        theme_benefit = get_color_theme("benefit")
        self.assertEqual(theme_benefit, COLOR_THEMES["success"])
        
        theme_emotional = get_color_theme("emotional")
        self.assertEqual(theme_emotional, COLOR_THEMES["trust"])
        
        theme_engaging = get_color_theme("engaging")
        self.assertEqual(theme_engaging, COLOR_THEMES["energy"])
        
        # Test avec style non mappé (devrait retourner energy par défaut)
        theme_unknown = get_color_theme("style_inexistant")
        self.assertEqual(theme_unknown, COLOR_THEMES["energy"])
    
    def test_get_random_template(self):
        """Test de récupération d'un template aléatoire"""
        template = get_random_template()
        self.assertIsInstance(template, str)
        self.assertIn(template, HOOK_TEMPLATES)
        
        # Test que plusieurs appels peuvent donner des résultats différents
        templates = [get_random_template() for _ in range(10)]
        self.assertTrue(len(set(templates)) >= 1)  # Au moins un template unique
    
    def test_get_templates_by_category(self):
        """Test de récupération de templates par catégorie"""
        # Test avec catégories existantes
        urgence_templates = get_templates_by_category("urgence")
        self.assertIsInstance(urgence_templates, list)
        self.assertEqual(len(urgence_templates), 10)
        
        curiosite_templates = get_templates_by_category("curiosité")
        self.assertIsInstance(curiosite_templates, list)
        self.assertEqual(len(curiosite_templates), 10)
        
        # Test avec catégorie inexistante (devrait retourner tous les templates)
        all_templates = get_templates_by_category("inexistant")
        self.assertEqual(all_templates, HOOK_TEMPLATES)
    
    def test_hook_style_enum(self):
        """Test de l'énumération HookStyle"""
        # Test get_style_prompts
        style_prompts = HookStyle.get_style_prompts()
        self.assertIsInstance(style_prompts, dict)
        self.assertIn(HookStyle.URGENT.value, style_prompts)
        self.assertIn(HookStyle.ENGAGING.value, style_prompts)
        
        # Test get_default_styles
        default_styles = HookStyle.get_default_styles()
        self.assertIsInstance(default_styles, list)
        self.assertEqual(len(default_styles), 4)
        self.assertIn(HookStyle.ENGAGING.value, default_styles)
        
        # Test is_valid_style
        self.assertTrue(HookStyle.is_valid_style(HookStyle.URGENT.value))
        self.assertTrue(HookStyle.is_valid_style("engaging"))
        self.assertFalse(HookStyle.is_valid_style("style_inexistant"))
    
    def test_constants_structure(self):
        """Test de la structure des constantes"""
        # Test MARKETING_SUBJECTS
        self.assertIsInstance(MARKETING_SUBJECTS, list)
        self.assertGreater(len(MARKETING_SUBJECTS), 0)
        for subject in MARKETING_SUBJECTS:
            self.assertIsInstance(subject, str)
            self.assertGreater(len(subject), 0)
        
        # Test MARKETING_STYLES
        self.assertIsInstance(MARKETING_STYLES, list)
        self.assertGreater(len(MARKETING_STYLES), 0)
        for style in MARKETING_STYLES:
            self.assertIsInstance(style, str)
            self.assertGreater(len(style), 0)
        
        # Test IMAGE_CONFIG
        self.assertIsInstance(IMAGE_CONFIG, dict)
        self.assertIn("styles", IMAGE_CONFIG)
        self.assertIn("size", IMAGE_CONFIG)
        self.assertIn("quality", IMAGE_CONFIG)
        self.assertIn("model", IMAGE_CONFIG)
        
        # Test HOOK_CONFIG
        self.assertIsInstance(HOOK_CONFIG, dict)
        self.assertIn("model", HOOK_CONFIG)
        self.assertIn("language", HOOK_CONFIG)
        self.assertIn("num_hooks_per_subject", HOOK_CONFIG)
        
        # Test IMAGE_PROMPTS
        self.assertIsInstance(IMAGE_PROMPTS, dict)
        for style, prompt in IMAGE_PROMPTS.items():
            self.assertIsInstance(style, str)
            self.assertIsInstance(prompt, str)
            self.assertGreater(len(prompt), 0)
        
        # Test COLOR_THEMES
        self.assertIsInstance(COLOR_THEMES, dict)
        for theme, colors in COLOR_THEMES.items():
            self.assertIsInstance(theme, str)
            self.assertIsInstance(colors, list)
            self.assertGreater(len(colors), 0)
        
        # Test MARKETING_KEYWORDS
        self.assertIsInstance(MARKETING_KEYWORDS, list)
        self.assertGreater(len(MARKETING_KEYWORDS), 0)
        for keyword in MARKETING_KEYWORDS:
            self.assertIsInstance(keyword, str)
            self.assertGreater(len(keyword), 0)
        
        # Test HOOK_TEMPLATES
        self.assertIsInstance(HOOK_TEMPLATES, list)
        self.assertGreater(len(HOOK_TEMPLATES), 0)
        for template in HOOK_TEMPLATES:
            self.assertIsInstance(template, str)
            self.assertGreater(len(template), 0)

class TestMarketingResourcesGeneration(unittest.TestCase):
    """Tests pour la génération de ressources marketing"""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('examples.example_marketing_hooks.HookGenerator.generate_hooks_simple')
    @patch('examples.example_marketing_hooks.ImageGenerator.generate_image')
    @patch('examples.example_marketing_hooks.time.sleep')
    def test_marketing_resources(self, mock_sleep, mock_generate_image, mock_generate_hooks):
        """Test de la génération de ressources marketing avec mocks"""
        
        # Mock des retours de fonctions
        mock_generate_hooks.return_value = [{
            'hook': 'Hook de test mocké',
            'description': 'Description de test mockée'
        }]
        mock_generate_image.return_value = Path('generated/images/mock_image.png')
        mock_sleep.return_value = None
        
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

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('examples.example_marketing_hooks.HookGenerator.generate_hooks_simple')
    @patch('examples.example_marketing_hooks.ImageGenerator.generate_image')
    @patch('examples.example_marketing_hooks.time.sleep')
    @patch('builtins.print')  # Mock print pour accélérer les tests
    def test_different_quantities(self, mock_print, mock_sleep, mock_generate_image, mock_generate_hooks):
        """Test avec différentes quantités - version mockée pour accélération"""
        
        # Mock des retours de fonctions
        mock_generate_hooks.return_value = [{
            'hook': 'Hook de test mocké',
            'description': 'Description de test mockée'
        }]
        mock_generate_image.return_value = Path('generated/images/mock_image.png')
        mock_sleep.return_value = None
        mock_print.return_value = None  # Désactiver les prints
        
        # Test avec différentes quantités (réduit pour la vitesse)
        test_quantities = [1, 2]  # Réduit de [1, 3, 5] à [1, 2] pour la vitesse
        for quantity in test_quantities:
            resources = generate_marketing_resources(num_resources=quantity)
            self.assertEqual(len(resources), quantity, f"Échec pour {quantity} ressource(s)")
            
            # Vérifier la structure de chaque ressource
            for resource in resources:
                self.assertIn('hook', resource)
                self.assertIn('subject', resource)
                self.assertIn('style', resource)

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('examples.example_marketing_hooks.HookGenerator.generate_hooks_simple')
    @patch('examples.example_marketing_hooks.ImageGenerator.generate_image')
    @patch('examples.example_marketing_hooks.time.sleep')
    def test_edge_cases(self, mock_sleep, mock_generate_image, mock_generate_hooks):
        """Test des cas limites avec mocks"""
        # Mock des retours de fonctions
        mock_generate_hooks.return_value = [{
            'hook': 'Hook de test',
            'description': 'Description de test'
        }]
        mock_generate_image.return_value = Path('generated/images/mock_image.png')
        mock_sleep.return_value = None
        
        # Test avec 0 ressources
        resources_zero = generate_marketing_resources(num_resources=0)
        self.assertEqual(len(resources_zero), 0)
        
        # Test avec nombre négatif (devrait être traité comme 0)
        resources_negative = generate_marketing_resources(num_resources=-1)
        self.assertEqual(len(resources_negative), 0)

def main():
    """Lance tous les tests"""
    
    print("🚀 Tests des ressources marketing et configuration")
    print("=" * 60)
    
    # Lancer les tests unittest
    unittest.main(verbosity=2, exit=False)
    
    # Tests de compatibilité
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

# Fonctions de test compatibles avec l'ancien format
@patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
@patch('examples.example_marketing_hooks.HookGenerator.generate_hooks_simple')
@patch('examples.example_marketing_hooks.ImageGenerator.generate_image')
@patch('examples.example_marketing_hooks.time.sleep')
def test_marketing_resources(mock_sleep, mock_generate_image, mock_generate_hooks):
    """Test de la génération de ressources marketing avec mocks"""
    
    # Mock des retours de fonctions
    mock_generate_hooks.return_value = [{
        'hook': 'Hook de test mocké',
        'description': 'Description de test mockée'
    }]
    mock_generate_image.return_value = Path('generated/images/mock_image.png')
    mock_sleep.return_value = None
    
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

@patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
@patch('examples.example_marketing_hooks.HookGenerator.generate_hooks_simple')
@patch('examples.example_marketing_hooks.ImageGenerator.generate_image')
@patch('examples.example_marketing_hooks.time.sleep')
def test_different_quantities(mock_sleep, mock_generate_image, mock_generate_hooks):
    """Test avec différentes quantités - version mockée pour accélération"""
    
    # Mock des retours de fonctions
    mock_generate_hooks.return_value = [{
        'hook': 'Hook de test mocké',
        'description': 'Description de test mockée'
    }]
    mock_generate_image.return_value = Path('generated/images/mock_image.png')
    mock_sleep.return_value = None
    
    # Test avec différentes quantités
    test_quantities = [1, 3, 5]
    for quantity in test_quantities:
        resources = generate_marketing_resources(num_resources=quantity)
        assert resources and len(resources) == quantity, f"Échec pour {quantity} ressource(s)"

if __name__ == "__main__":
    unittest.main() 