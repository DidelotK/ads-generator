#!/usr/bin/env python3
"""
Tests rapides avec tous les mocks nécessaires pour éviter les appels API
"""

import unittest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.generators.hook_generator import HookGenerator, HookStyle
from src.generators.image_generator import ImageGenerator, ImageStyle
from src.generators.prompt_generator import PromptGenerator, PromptStyle
from src.marketing_config import (
    get_marketing_subjects, get_marketing_styles, get_image_prompt,
    get_color_theme, get_random_template, IMAGE_CONFIG
)

class TestFastHookGenerator(unittest.TestCase):
    """Tests rapides pour HookGenerator avec mocks complets"""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.hook_generator.openai.OpenAI')
    def test_hook_generation_fast(self, mock_openai):
        """Test rapide de génération de hooks"""
        # Mock complet de l'API
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"hooks": [{"hook": "Test hook", "description": "Test description"}]}'
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_response.usage.total_tokens = 150
        mock_client.chat.completions.create.return_value = mock_response
        
        generator = HookGenerator()
        hooks = generator.generate_hooks_simple(
            subject="Test Subject",
            num_hooks=1,
            style=HookStyle.ENGAGING.value,
            model="gpt-3.5-turbo"
        )
        
        self.assertIsNotNone(hooks)
        self.assertEqual(len(hooks), 1)
        self.assertEqual(hooks[0]["hook"], "Test hook")

class TestFastMarketingConfig(unittest.TestCase):
    """Tests rapides pour les fonctions de configuration marketing"""
    
    def test_marketing_functions(self):
        """Test de toutes les fonctions marketing sans appel API"""
        # Test des sujets
        subjects = get_marketing_subjects(3)
        self.assertEqual(len(subjects), 3)
        
        # Test des styles
        styles = get_marketing_styles(3)
        self.assertEqual(len(styles), 3)
        
        # Test de prompt d'image
        hook_text = "Test hook"
        prompt = get_image_prompt(hook_text, "realistic")
        self.assertIn(hook_text, prompt)
        
        # Test de thème de couleur
        theme = get_color_theme("urgent")
        self.assertIsInstance(theme, list)
        
        # Test de template aléatoire
        template = get_random_template()
        self.assertIsInstance(template, str)
        
        # Test HookStyle
        self.assertTrue(HookStyle.is_valid_style("engaging"))
        self.assertFalse(HookStyle.is_valid_style("inexistant"))

if __name__ == '__main__':
    unittest.main(verbosity=2, buffer=True)
