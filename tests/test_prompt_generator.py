#!/usr/bin/env python3
"""
Tests complets pour le générateur de prompts d'images
"""

import unittest
import sys
import os
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Ajouter le répertoire src au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from src.generators.prompt_generator import PromptGenerator, PromptStyle, ImagePrompt, ImagePromptList

class TestPromptStyle(unittest.TestCase):
    """Tests pour l'énumération PromptStyle"""
    
    def test_get_style_prompts(self):
        """Test de récupération des descriptions de styles"""
        style_prompts = PromptStyle.get_style_prompts()
        
        self.assertIsInstance(style_prompts, dict)
        self.assertIn(PromptStyle.REALISTIC.value, style_prompts)
        self.assertIn(PromptStyle.PHOTOGRAPHIC.value, style_prompts)
        self.assertIn(PromptStyle.ARTISTIC.value, style_prompts)
        
        # Vérifier que chaque style a une description
        for style, description in style_prompts.items():
            self.assertIsInstance(description, str)
            self.assertGreater(len(description), 0)
    
    def test_get_default_styles(self):
        """Test de récupération des styles par défaut"""
        default_styles = PromptStyle.get_default_styles()
        
        self.assertIsInstance(default_styles, list)
        self.assertEqual(len(default_styles), 3)
        self.assertIn(PromptStyle.REALISTIC.value, default_styles)
        self.assertIn(PromptStyle.PHOTOGRAPHIC.value, default_styles)
        self.assertIn(PromptStyle.COMMERCIAL.value, default_styles)
    
    def test_is_valid_style(self):
        """Test de validation des styles"""
        # Styles valides
        self.assertTrue(PromptStyle.is_valid_style("realistic"))
        self.assertTrue(PromptStyle.is_valid_style("photographic"))
        self.assertTrue(PromptStyle.is_valid_style("artistic"))
        
        # Styles invalides
        self.assertFalse(PromptStyle.is_valid_style("inexistant"))
        self.assertFalse(PromptStyle.is_valid_style(""))
        self.assertFalse(PromptStyle.is_valid_style(None))

class TestImagePrompt(unittest.TestCase):
    """Tests pour la classe ImagePrompt"""
    
    def test_image_prompt_creation(self):
        """Test de création d'un ImagePrompt"""
        prompt = ImagePrompt(
            elements=["smartphone", "personne"],
            ambiance="moderne et technologique",
            style="photographie professionnelle",
            details_techniques="haute résolution, éclairage naturel",
            contraintes="pas de texte, composition équilibrée",
            description="Image d'une personne utilisant un smartphone"
        )
        
        self.assertEqual(prompt.elements, ["smartphone", "personne"])
        self.assertEqual(prompt.ambiance, "moderne et technologique")
        self.assertIn("smartphone, personne", prompt.prompt)
        self.assertIn("moderne et technologique", prompt.prompt)
    
    def test_image_prompt_list_creation(self):
        """Test de création d'une ImagePromptList"""
        prompt1 = ImagePrompt(
            elements=["test1"],
            ambiance="test",
            style="test",
            details_techniques="test",
            contraintes="test",
            description="test1"
        )
        prompt2 = ImagePrompt(
            elements=["test2"],
            ambiance="test",
            style="test",
            details_techniques="test",
            contraintes="test",
            description="test2"
        )
        
        prompt_list = ImagePromptList(prompts=[prompt1, prompt2])
        self.assertEqual(len(prompt_list.prompts), 2)

class TestPromptGenerator(unittest.TestCase):
    """Tests pour la classe PromptGenerator"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.mock_api_key = "test_api_key_123"
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_init_with_env_key(self):
        """Test d'initialisation avec clé d'environnement"""
        generator = PromptGenerator()
        self.assertEqual(generator.api_key, 'test_key')
        self.assertIsNotNone(generator.client)
        self.assertTrue(generator.output_dir.exists())
    
    def test_init_with_provided_key(self):
        """Test d'initialisation avec clé fournie"""
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
        
        self.assertIsInstance(models, dict)
        self.assertIn("gpt-3.5-turbo", models)
        self.assertIn("gpt-4", models)
        
        for model_id, model_info in models.items():
            self.assertIn("name", model_info)
            self.assertIn("description", model_info)
            self.assertIn("input_cost", model_info)
            self.assertIn("output_cost", model_info)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_get_available_styles(self):
        """Test de récupération des styles disponibles"""
        generator = PromptGenerator()
        styles = generator.get_available_styles()
        
        self.assertIsInstance(styles, dict)
        for style_name, style_info in styles.items():
            self.assertIn("name", style_info)
            self.assertIn("description", style_info)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_calculate_cost(self):
        """Test de calcul de coût"""
        generator = PromptGenerator()
        
        # Test avec modèle valide
        cost = generator._calculate_cost("gpt-3.5-turbo", 100, 50)
        self.assertGreater(cost, 0)
        self.assertIsInstance(cost, float)
        
        # Test avec modèle inexistant (devrait utiliser le défaut)
        cost_default = generator._calculate_cost("modele_inexistant", 100, 50)
        self.assertGreater(cost_default, 0)

class TestPromptReading(unittest.TestCase):
    """Tests pour la lecture de prompts depuis des fichiers"""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_is_file_path_valid_file(self):
        """Test de détection de chemin de fichier valide"""
        generator = PromptGenerator()
        
        # Créer un fichier temporaire
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"test content")
            temp_file_path = temp_file.name
        
        try:
            # Devrait détecter que c'est un fichier
            self.assertTrue(generator._is_file_path(temp_file_path))
            
            # Test avec texte normal (pas un fichier)
            self.assertFalse(generator._is_file_path("Ceci est un prompt normal"))
            
            # Test avec texte très long
            long_text = "a" * 600
            self.assertFalse(generator._is_file_path(long_text))
            
            # Test avec None/empty
            self.assertFalse(generator._is_file_path(None))
            self.assertFalse(generator._is_file_path(""))
            
        finally:
            os.unlink(temp_file_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_read_prompt_from_text_file(self):
        """Test de lecture depuis un fichier texte"""
        generator = PromptGenerator()
        
        test_content = "Ceci est un prompt de test depuis un fichier texte"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(test_content)
            temp_file_path = temp_file.name
        
        try:
            result = generator._read_prompt_from_text(temp_file_path)
            self.assertEqual(result, test_content)
        finally:
            os.unlink(temp_file_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_read_prompt_from_json_file(self):
        """Test de lecture depuis un fichier JSON"""
        generator = PromptGenerator()
        
        # Test avec différentes structures JSON
        test_cases = [
            {"prompt": "Test prompt depuis JSON"},
            {"description": "Test description depuis JSON"},
            {"text": "Test text depuis JSON"},
            {"content": "Test content depuis JSON"},
            "Simple string JSON",
            ["Premier élément de liste"],
            {"autre_clé": "Valeur quelconque"}
        ]
        
        for test_data in test_cases:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                json.dump(test_data, temp_file)
                temp_file_path = temp_file.name
            
            try:
                result = generator._read_prompt_from_json(temp_file_path)
                self.assertIsInstance(result, str)
                self.assertGreater(len(result), 0)
            finally:
                os.unlink(temp_file_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_read_prompt_from_file_dispatcher(self):
        """Test du dispatcher de lecture de fichier"""
        generator = PromptGenerator()
        
        # Test avec fichier .txt
        test_content = "Test content"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(test_content)
            temp_file_path = temp_file.name
        
        try:
            result = generator.read_prompt_from_file(temp_file_path)
            self.assertEqual(result, test_content)
        finally:
            os.unlink(temp_file_path)
        
        # Test avec fichier .json
        test_json = {"prompt": "Test JSON prompt"}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(test_json, temp_file)
            temp_file_path = temp_file.name
        
        try:
            result = generator.read_prompt_from_file(temp_file_path)
            self.assertEqual(result, "Test JSON prompt")
        finally:
            os.unlink(temp_file_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_read_prompt_from_file_error_handling(self):
        """Test de gestion d'erreur pour fichier inexistant"""
        generator = PromptGenerator()
        
        result = generator.read_prompt_from_file("/fichier/inexistant.txt")
        self.assertIn("Erreur lors de la lecture du fichier", result)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_resolve_prompt_input_with_file(self):
        """Test de résolution d'input avec fichier"""
        generator = PromptGenerator()
        
        test_content = "Prompt depuis fichier"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(test_content)
            temp_file_path = temp_file.name
        
        try:
            result = generator.resolve_prompt_input(temp_file_path)
            self.assertEqual(result, test_content)
        finally:
            os.unlink(temp_file_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_resolve_prompt_input_with_text(self):
        """Test de résolution d'input avec texte direct"""
        generator = PromptGenerator()
        
        direct_prompt = "Ceci est un prompt direct"
        result = generator.resolve_prompt_input(direct_prompt)
        self.assertEqual(result, direct_prompt)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_extract_prompt_from_data_string(self):
        """Test d'extraction de prompt depuis string"""
        generator = PromptGenerator()
        
        test_prompt = "Test prompt simple"
        result = generator.extract_prompt_from_data(test_prompt)
        self.assertEqual(result, test_prompt)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_extract_prompt_from_data_dict_with_prompt(self):
        """Test d'extraction depuis dict avec clé prompt"""
        generator = PromptGenerator()
        
        test_data = {"prompt": "Prompt complet existant"}
        result = generator.extract_prompt_from_data(test_data)
        self.assertEqual(result, "Prompt complet existant")
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_extract_prompt_from_data_dict_without_prompt(self):
        """Test d'extraction depuis dict sans clé prompt"""
        generator = PromptGenerator()
        
        test_data = {
            "elements": ["élément1", "élément2"],
            "ambiance": "moderne",
            "style": "photographique",
            "details_techniques": "haute résolution",
            "contraintes": "pas de texte"
        }
        
        result = generator.extract_prompt_from_data(test_data)
        self.assertIn("élément1, élément2", result)
        self.assertIn("moderne", result)
        self.assertIn("photographique", result)

class TestPromptGeneratorIntegration(unittest.TestCase):
    """Tests d'intégration avec l'API OpenAI mockée"""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.prompt_generator.openai.OpenAI')
    def test_generate_prompts_success(self, mock_openai):
        """Test de génération de prompts avec succès"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        # Mock de la réponse API
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '''{
            "prompts": [
                {
                    "elements": ["smartphone", "personne"],
                    "ambiance": "moderne",
                    "style": "photographique",
                    "details_techniques": "haute résolution",
                    "contraintes": "pas de texte",
                    "description": "Test prompt description"
                }
            ]
        }'''
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_client.chat.completions.create.return_value = mock_response
        
        generator = PromptGenerator()
        prompts = generator.generate_prompts(
            hook="Test hook",
            description="Test description",
            num_prompts=1,
            style="realistic",
            model="gpt-3.5-turbo"
        )
        
        self.assertIsInstance(prompts, list)
        self.assertEqual(len(prompts), 1)
        self.assertIn("prompt", prompts[0])
        self.assertIn("elements", prompts[0])
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.prompt_generator.openai.OpenAI')
    def test_generate_prompts_with_invalid_style(self, mock_openai):
        """Test avec style invalide"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '''{
            "prompts": [
                {
                    "elements": ["test"],
                    "ambiance": "test",
                    "style": "test",
                    "details_techniques": "test",
                    "contraintes": "test",
                    "description": "test"
                }
            ]
        }'''
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_client.chat.completions.create.return_value = mock_response
        
        generator = PromptGenerator()
        prompts = generator.generate_prompts(
            hook="Test hook",
            description="Test description",
            num_prompts=1,
            style="style_invalide",  # Style invalide
            model="gpt-3.5-turbo"
        )
        
        # Devrait utiliser le style par défaut et fonctionner
        self.assertIsInstance(prompts, list)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.prompt_generator.openai.OpenAI')
    def test_generate_prompts_with_invalid_model(self, mock_openai):
        """Test avec modèle invalide"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '''{
            "prompts": [
                {
                    "elements": ["test"],
                    "ambiance": "test",
                    "style": "test",
                    "details_techniques": "test",
                    "contraintes": "test",
                    "description": "test"
                }
            ]
        }'''
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_client.chat.completions.create.return_value = mock_response
        
        generator = PromptGenerator()
        prompts = generator.generate_prompts(
            hook="Test hook",
            description="Test description",
            num_prompts=1,
            style="realistic",
            model="modele_invalide"  # Modèle invalide
        )
        
        # Devrait utiliser le modèle par défaut et fonctionner
        self.assertIsInstance(prompts, list)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.prompt_generator.openai.OpenAI')
    def test_generate_prompts_api_error(self, mock_openai):
        """Test de gestion d'erreur API"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        # Simuler une erreur API
        mock_client.chat.completions.create.side_effect = Exception("Erreur API simulée")
        
        generator = PromptGenerator()
        prompts = generator.generate_prompts(
            hook="Test hook",
            description="Test description",
            num_prompts=1,
            style="realistic",
            model="gpt-3.5-turbo"
        )
        
        # Devrait retourner une liste vide en cas d'erreur
        self.assertEqual(prompts, [])
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.prompt_generator.openai.OpenAI')
    def test_generate_prompts_invalid_json_response(self, mock_openai):
        """Test avec réponse JSON invalide"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"invalid": "json structure"}'
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_client.chat.completions.create.return_value = mock_response
        
        generator = PromptGenerator()
        
        # Le générateur retourne une liste vide en cas de JSON invalide
        prompts = generator.generate_prompts(
            hook="Test hook",
            description="Test description",
            num_prompts=1,
            style="realistic",
            model="gpt-3.5-turbo"
        )
        
        # Devrait retourner une liste vide en cas d'erreur
        self.assertEqual(prompts, [])
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.prompt_generator.openai.OpenAI')
    def test_generate_multiple_styles(self, mock_openai):
        """Test de génération avec plusieurs styles"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '''{
            "prompts": [
                {
                    "elements": ["test"],
                    "ambiance": "test",
                    "style": "test",
                    "details_techniques": "test",
                    "contraintes": "test",
                    "description": "test"
                }
            ]
        }'''
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_client.chat.completions.create.return_value = mock_response
        
        generator = PromptGenerator()
        results = generator.generate_multiple_styles(
            hook="Test hook",
            description="Test description",
            styles=["realistic", "photographic"],
            num_prompts=1,
            model="gpt-3.5-turbo"
        )
        
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 2)
        self.assertIn("realistic", results)
        self.assertIn("photographic", results)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.prompt_generator.openai.OpenAI')
    def test_generate_multiple_styles_with_defaults(self, mock_openai):
        """Test de génération avec styles par défaut"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '''{
            "prompts": [
                {
                    "elements": ["test"],
                    "ambiance": "test",
                    "style": "test",
                    "details_techniques": "test",
                    "contraintes": "test",
                    "description": "test"
                }
            ]
        }'''
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_client.chat.completions.create.return_value = mock_response
        
        generator = PromptGenerator()
        results = generator.generate_multiple_styles(
            hook="Test hook",
            description="Test description",
            styles=None,  # Utiliser les styles par défaut
            num_prompts=1,
            model="gpt-3.5-turbo"
        )
        
        self.assertIsInstance(results, dict)
        # Devrait utiliser les 3 styles par défaut
        self.assertEqual(len(results), 3)

if __name__ == '__main__':
    unittest.main()