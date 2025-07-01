#!/usr/bin/env python3
"""
Tests complets pour le générateur de hooks
"""

import sys
import os
import unittest
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.generators.hook_generator import HookGenerator, Hook, HookList
from src.marketing_config import HookStyle

class TestHookGenerator(unittest.TestCase):
    """Tests pour le générateur de hooks"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.mock_api_key = "test_api_key_123"
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_initialization_with_env_key(self):
        """Test d'initialisation avec clé d'environnement"""
        generator = HookGenerator()
        self.assertEqual(generator.api_key, 'test_key')
        self.assertIsNotNone(generator.client)
        self.assertTrue(generator.output_dir.exists())
    
    def test_initialization_with_provided_key(self):
        """Test d'initialisation avec clé fournie"""
        generator = HookGenerator(api_key=self.mock_api_key)
        self.assertEqual(generator.api_key, self.mock_api_key)
    
    def test_initialization_without_key(self):
        """Test d'initialisation sans clé API"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                HookGenerator()
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_get_available_models(self):
        """Test de récupération des modèles disponibles"""
        generator = HookGenerator()
        models = generator.get_available_models()
        
        self.assertIsInstance(models, dict)
        self.assertIn("gpt-3.5-turbo", models)
        self.assertIn("gpt-4", models)
        
        for model_id, model_info in models.items():
            self.assertIn("name", model_info)
            self.assertIn("description", model_info)
            self.assertIn("input_cost", model_info)
            self.assertIn("output_cost", model_info)
            self.assertIn("max_tokens", model_info)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_get_model_info(self):
        """Test de récupération d'informations d'un modèle spécifique"""
        generator = HookGenerator()
        
        # Test avec modèle existant
        model_info = generator.get_model_info("gpt-3.5-turbo")
        self.assertIsNotNone(model_info)
        self.assertIn("name", model_info)
        self.assertIn("description", model_info)
        
        # Test avec modèle inexistant
        model_info = generator.get_model_info("modele-inexistant")
        self.assertIsNone(model_info)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_get_available_styles(self):
        """Test de récupération des styles disponibles"""
        generator = HookGenerator()
        styles = generator.get_available_styles()
        
        self.assertIsInstance(styles, dict)
        self.assertGreater(len(styles), 0)
        
        for style_name, style_info in styles.items():
            self.assertIn("name", style_info)
            self.assertIn("description", style_info)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_validate_and_clean_hooks(self):
        """Test de validation et nettoyage des hooks"""
        generator = HookGenerator()
        
        # Test avec hooks valides
        valid_hooks = [
            {"hook": "Accroche test 1", "description": "Description test 1"},
            {"hook": "Accroche test 2", "description": "Description test 2"}
        ]
        
        cleaned = generator._validate_and_clean_hooks(valid_hooks, 2)
        self.assertEqual(len(cleaned), 2)
        self.assertEqual(cleaned[0]["hook"], "Accroche test 1")
        
        # Test avec hooks invalides
        invalid_hooks = [
            {"hook": "", "description": "Description vide"},  # Hook vide
            {"hook": "OK", "description": "Description OK"},  # Hook trop court
            {"hook": "Accroche valide", "description": "Description OK"}  # Hook valide
        ]
        
        cleaned = generator._validate_and_clean_hooks(invalid_hooks, 3)
        self.assertEqual(len(cleaned), 1)  # Seul le hook valide reste
        
        # Test avec strings simples
        string_hooks = ["Accroche string 1", "Accroche string 2"]
        cleaned = generator._validate_and_clean_hooks(string_hooks, 2)
        self.assertEqual(len(cleaned), 2)
        self.assertIn("hook", cleaned[0])
        self.assertIn("description", cleaned[0])
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_parse_hooks_from_text(self):
        """Test de parsing de hooks depuis du texte"""
        generator = HookGenerator()
        
        # Test avec texte structuré
        text = '''
        "hook": "Première accroche test",
        "description": "Première description test",
        "hook": "Deuxième accroche test",
        "description": "Deuxième description test"
        '''
        
        hooks = generator._parse_hooks_from_text(text, 2)
        self.assertGreaterEqual(len(hooks), 1)
        
        for hook in hooks:
            self.assertIn("hook", hook)
            self.assertIn("description", hook)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_generate_simple_hooks(self):
        """Test de génération de hooks simples"""
        generator = HookGenerator()
        
        text = "Première phrase test. Deuxième phrase test. Troisième phrase test."
        hooks = generator._generate_simple_hooks(text, 2)
        
        self.assertEqual(len(hooks), 2)
        for hook in hooks:
            self.assertIn("hook", hook)
            self.assertIn("description", hook)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_calculate_cost(self):
        """Test de calcul de coût"""
        generator = HookGenerator()
        
        # Test avec modèle existant
        cost = generator._calculate_cost("gpt-3.5-turbo", 100, 50)
        self.assertGreater(cost, 0)
        self.assertIsInstance(cost, float)
        
        # Test avec modèle inexistant
        cost_invalid = generator._calculate_cost("modele-inexistant", 100, 50)
        self.assertEqual(cost_invalid, 0.0)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_extract_json_from_response(self):
        """Test d'extraction JSON depuis une réponse"""
        generator = HookGenerator()
        
        # Test avec JSON valide
        json_response = '{"hooks": [{"hook": "Test", "description": "Test desc"}]}'
        extracted = generator._extract_json_from_response(json_response)
        self.assertEqual(extracted, json_response)
        
        # Test avec texte contenant du JSON
        text_with_json = 'Voici le résultat:\n{"hooks": [{"hook": "Test", "description": "Test desc"}]}\nFin.'
        extracted = generator._extract_json_from_response(text_with_json)
        self.assertIn("hooks", extracted)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_save_hooks(self):
        """Test de sauvegarde des hooks"""
        generator = HookGenerator()
        
        hooks = [
            {"hook": "Test hook", "description": "Test description"}
        ]
        
        # Test de sauvegarde
        filename = generator._save_hooks(hooks, "Test Subject", "engaging", "gpt-3.5-turbo")
        
        if filename:  # Si la sauvegarde réussit
            self.assertTrue(filename.exists())
            
            # Vérifier le contenu du fichier
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.assertIn("metadata", data)
            self.assertIn("hooks", data)
            self.assertEqual(data["metadata"]["subject"], "Test Subject")
            self.assertEqual(len(data["hooks"]), 1)
            
            # Nettoyer
            filename.unlink()

class TestHookGeneratorIntegration(unittest.TestCase):
    """Tests d'intégration avec mock de l'API OpenAI"""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.hook_generator.openai.OpenAI')
    def test_generate_hooks_simple_success(self, mock_openai):
        """Test d'intégration de génération simple avec API mockée"""
        # Configuration du mock OpenAI
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        # Mock de la réponse d'API
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
        self.assertEqual(hooks[0]["description"], "Test description")
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.hook_generator.openai.OpenAI')
    def test_generate_hooks_simple_with_invalid_style(self, mock_openai):
        """Test avec style invalide"""
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
            style="style_inexistant",  # Style invalide
            model="gpt-3.5-turbo"
        )
        
        # Devrait utiliser le style par défaut et fonctionner
        self.assertIsNotNone(hooks)
        self.assertEqual(len(hooks), 1)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.hook_generator.openai.OpenAI')
    def test_generate_hooks_simple_with_invalid_model(self, mock_openai):
        """Test avec modèle invalide"""
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
            model="modele_inexistant"  # Modèle invalide
        )
        
        # Devrait utiliser le modèle par défaut et fonctionner
        self.assertIsNotNone(hooks)
        self.assertEqual(len(hooks), 1)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.hook_generator.openai.OpenAI')
    def test_generate_hooks_simple_api_error(self, mock_openai):
        """Test de gestion d'erreur API"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        # Simuler une erreur API
        mock_client.chat.completions.create.side_effect = Exception("Erreur API simulée")
        
        generator = HookGenerator()
        hooks = generator.generate_hooks_simple(
            subject="Test Subject",
            num_hooks=1,
            style=HookStyle.ENGAGING.value,
            model="gpt-3.5-turbo"
        )
        
        # Devrait retourner None en cas d'erreur
        self.assertIsNone(hooks)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.hook_generator.openai.OpenAI')
    def test_generate_hooks_with_function_calling(self, mock_openai):
        """Test de la génération avec function calling"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        # Mock de la réponse avec function calling
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.function_call.arguments = '{"hooks": [{"hook": "Function call hook", "description": "Generated with function calling"}]}'
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_response.usage.total_tokens = 150
        mock_client.chat.completions.create.return_value = mock_response
        
        generator = HookGenerator()
        hooks = generator.generate_hooks(
            subject="Test Subject",
            num_hooks=1,
            style=HookStyle.ENGAGING.value,
            model="gpt-3.5-turbo"
        )
        
        # Devrait retourner les hooks générés
        self.assertIsNotNone(hooks)
        self.assertEqual(len(hooks), 1)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.hook_generator.openai.OpenAI')
    def test_generate_hooks_with_pydantic_validation_error(self, mock_openai):
        """Test avec erreur de validation Pydantic"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        # Mock avec JSON invalide pour Pydantic
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.function_call.arguments = '{"invalid": "data"}'
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_response.usage.total_tokens = 150
        mock_client.chat.completions.create.return_value = mock_response
        
        generator = HookGenerator()
        hooks = generator.generate_hooks(
            subject="Test Subject",
            num_hooks=1,
            style=HookStyle.ENGAGING.value,
            model="gpt-3.5-turbo"
        )
        
        # Devrait gérer l'erreur et tenter un parsing alternatif
        self.assertIsNotNone(hooks)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.hook_generator.openai.OpenAI')
    def test_generate_multiple_styles(self, mock_openai):
        """Test de génération en plusieurs styles"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.function_call.arguments = '{"hooks": [{"hook": "Multi style hook", "description": "Test description"}]}'
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_response.usage.total_tokens = 150
        mock_client.chat.completions.create.return_value = mock_response
        
        generator = HookGenerator()
        results = generator.generate_multiple_styles(
            subject="Test Subject",
            styles=["engaging", "professional"],
            num_hooks=1,
            model="gpt-3.5-turbo"
        )
        
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 2)
        self.assertIn("engaging", results)
        self.assertIn("professional", results)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.hook_generator.openai.OpenAI')
    def test_generate_multiple_styles_with_defaults(self, mock_openai):
        """Test de génération avec styles par défaut"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.function_call.arguments = '{"hooks": [{"hook": "Default style hook", "description": "Test description"}]}'
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_response.usage.total_tokens = 150
        mock_client.chat.completions.create.return_value = mock_response
        
        generator = HookGenerator()
        results = generator.generate_multiple_styles(
            subject="Test Subject",
            styles=None,  # Utiliser les styles par défaut
            num_hooks=1,
            model="gpt-3.5-turbo"
        )
        
        self.assertIsInstance(results, dict)
        # Devrait utiliser les 4 styles par défaut
        self.assertEqual(len(results), 4)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_parse_hooks_manually(self):
        """Test du parsing manuel d'hooks"""
        generator = HookGenerator()
        
        content = '''
        "hook": "Premier hook test"
        "description": "Première description test"
        "hook": "Deuxième hook test"
        "description": "Deuxième description test"
        '''
        
        hooks = generator._parse_hooks_manually(content)
        self.assertGreaterEqual(len(hooks), 1)
        
        for hook in hooks:
            self.assertIn("hook", hook)
            self.assertIn("description", hook)

@patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
@patch('src.generators.hook_generator.openai.OpenAI')
def test_hook_generation(mock_openai):
    """Test simple de génération de hooks (pour compatibilité)"""
    # Configuration du mock OpenAI
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
        subject="Test de génération",
        num_hooks=1,
        style=HookStyle.ENGAGING.value,
        model="gpt-3.5-turbo"
    )
    assert hooks is not None and len(hooks) > 0, "Aucun hook généré"
    assert 'hook' in hooks[0] and 'description' in hooks[0], "Le hook généré n'a pas les bons champs"
    assert isinstance(hooks[0]['hook'], str) and isinstance(hooks[0]['description'], str), "Les champs ne sont pas des chaînes de caractères"

if __name__ == "__main__":
    unittest.main() 