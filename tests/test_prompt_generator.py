#!/usr/bin/env python3
"""
Tests pour le générateur de prompts d'images
"""

import unittest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Ajouter le répertoire src au path pour les imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from generators.prompt_generator import PromptGenerator, PromptStyle, ImagePrompt, ImagePromptList

class TestPromptStyle(unittest.TestCase):
    """Tests pour la classe PromptStyle"""
    
    def test_get_style_prompts(self):
        """Test de récupération des descriptions de styles"""
        styles = PromptStyle.get_style_prompts()
        self.assertIsInstance(styles, dict)
        self.assertIn("realistic", styles)
        self.assertIn("photographic", styles)
        self.assertIn("artistic", styles)
    
    def test_get_default_styles(self):
        """Test de récupération des styles par défaut"""
        default_styles = PromptStyle.get_default_styles()
        self.assertIsInstance(default_styles, list)
        self.assertIn("realistic", default_styles)
        self.assertIn("photographic", default_styles)
        self.assertIn("commercial", default_styles)
    
    def test_is_valid_style(self):
        """Test de validation des styles"""
        self.assertTrue(PromptStyle.is_valid_style("realistic"))
        self.assertTrue(PromptStyle.is_valid_style("artistic"))
        self.assertFalse(PromptStyle.is_valid_style("invalid_style"))

class TestImagePrompt(unittest.TestCase):
    """Tests pour les modèles Pydantic"""
    
    def test_image_prompt_creation(self):
        """Test de création d'un prompt d'image"""
        prompt_data = {
            "prompt": "Une image réaliste d'un compteur d'énergie",
            "style": "realistic",
            "elements": ["compteur", "factures", "personne"],
            "description": "Image réaliste montrant des économies d'énergie"
        }
        
        image_prompt = ImagePrompt(**prompt_data)
        self.assertEqual(image_prompt.prompt, prompt_data["prompt"])
        self.assertEqual(image_prompt.style, prompt_data["style"])
        self.assertEqual(image_prompt.elements, prompt_data["elements"])
        self.assertEqual(image_prompt.description, prompt_data["description"])
    
    def test_image_prompt_list_creation(self):
        """Test de création d'une liste de prompts"""
        prompts_data = {
            "prompts": [
                {
                    "prompt": "Prompt 1",
                    "style": "realistic",
                    "elements": ["élément 1"],
                    "description": "Description 1"
                },
                {
                    "prompt": "Prompt 2",
                    "style": "artistic",
                    "elements": ["élément 2"],
                    "description": "Description 2"
                }
            ]
        }
        
        prompt_list = ImagePromptList(**prompts_data)
        self.assertEqual(len(prompt_list.prompts), 2)
        self.assertEqual(prompt_list.prompts[0].prompt, "Prompt 1")
        self.assertEqual(prompt_list.prompts[1].style, "artistic")

class TestPromptGenerator(unittest.TestCase):
    """Tests pour le générateur de prompts"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.mock_api_key = "test_api_key_123"
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_init_with_env_key(self):
        """Test d'initialisation avec clé API depuis l'environnement"""
        generator = PromptGenerator()
        self.assertEqual(generator.api_key, 'test_key')
    
    def test_init_with_provided_key(self):
        """Test d'initialisation avec clé API fournie"""
        generator = PromptGenerator(api_key=self.mock_api_key)
        self.assertEqual(generator.api_key, self.mock_api_key)
    
    def test_init_without_key(self):
        """Test d'initialisation sans clé API"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                PromptGenerator()
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_get_available_models(self):
        """Test de récupération des modèles disponibles"""
        generator = PromptGenerator()
        models = generator.get_available_models()
        
        self.assertIn("gpt-4", models)
        self.assertIn("gpt-3.5-turbo", models)
        
        gpt4_info = models["gpt-4"]
        self.assertIn("name", gpt4_info)
        self.assertIn("description", gpt4_info)
        self.assertIn("input_cost", gpt4_info)
        self.assertIn("output_cost", gpt4_info)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_get_available_styles(self):
        """Test de récupération des styles disponibles"""
        generator = PromptGenerator()
        styles = generator.get_available_styles()
        
        self.assertIn("realistic", styles)
        self.assertIn("artistic", styles)
        self.assertIn("commercial", styles)
        
        realistic_info = styles["realistic"]
        self.assertIn("name", realistic_info)
        self.assertIn("description", realistic_info)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_validate_and_clean_prompts(self):
        """Test de validation et nettoyage des prompts"""
        generator = PromptGenerator()
        
        # Test avec prompts valides
        valid_prompts = [
            {
                "prompt": "Test prompt",
                "style": "realistic",
                "elements": ["élément 1", "élément 2"],
                "description": "Test description"
            }
        ]
        
        cleaned = generator._validate_and_clean_prompts(valid_prompts, 1)
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned[0]["prompt"], "Test prompt")
        
        # Test avec prompt incomplet
        invalid_prompts = [
            {
                "style": "realistic",
                "elements": ["élément 1"],
                "description": "Test description"
            }
        ]
        
        cleaned = generator._validate_and_clean_prompts(invalid_prompts, 1)
        self.assertEqual(len(cleaned), 0)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_calculate_cost(self):
        """Test de calcul des coûts"""
        generator = PromptGenerator()
        
        cost = generator._calculate_cost("gpt-3.5-turbo", 1000, 500)
        self.assertIsInstance(cost, float)
        self.assertGreater(cost, 0)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_extract_json_from_response(self):
        """Test d'extraction JSON de la réponse"""
        generator = PromptGenerator()
        
        # Test avec JSON valide
        content = 'Some text {"key": "value"} more text'
        json_result = generator._extract_json_from_response(content)
        self.assertEqual(json_result, '{"key": "value"}')
        
        # Test sans JSON
        content = 'No JSON here'
        json_result = generator._extract_json_from_response(content)
        self.assertIsNone(json_result)

if __name__ == '__main__':
    unittest.main() 