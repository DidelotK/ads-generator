#!/usr/bin/env python3
"""
Tests pour le générateur de prompts d'images
"""

import unittest
import sys
import os
import json
import tempfile
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
            "elements": ["compteur", "factures", "personne"],
            "ambiance": "moderne et rassurante",
            "style": "realistic",
            "details_techniques": "haute résolution, éclairage naturel",
            "contraintes": "pas de texte sur l'image",
            "description": "Image réaliste montrant des économies d'énergie"
        }
        
        image_prompt = ImagePrompt(**prompt_data)
        self.assertEqual(image_prompt.style, prompt_data["style"])
        self.assertEqual(image_prompt.elements, prompt_data["elements"])
        self.assertEqual(image_prompt.ambiance, prompt_data["ambiance"])
        self.assertEqual(image_prompt.details_techniques, prompt_data["details_techniques"])
        self.assertEqual(image_prompt.contraintes, prompt_data["contraintes"])
        self.assertEqual(image_prompt.description, prompt_data["description"])
        # Vérifier que le prompt est généré automatiquement
        self.assertIsInstance(image_prompt.prompt, str)
        self.assertGreater(len(image_prompt.prompt), 0)
    
    def test_image_prompt_list_creation(self):
        """Test de création d'une liste de prompts"""
        prompts_data = {
            "prompts": [
                {
                    "elements": ["élément 1"],
                    "ambiance": "moderne",
                    "style": "realistic",
                    "details_techniques": "haute qualité",
                    "contraintes": "pas de texte",
                    "description": "Description 1"
                },
                {
                    "elements": ["élément 2"],
                    "ambiance": "artistique",
                    "style": "artistic",
                    "details_techniques": "couleurs vives",
                    "contraintes": "composition équilibrée",
                    "description": "Description 2"
                }
            ]
        }
        
        prompt_list = ImagePromptList(**prompts_data)
        self.assertEqual(len(prompt_list.prompts), 2)
        self.assertEqual(prompt_list.prompts[0].elements, ["élément 1"])
        self.assertEqual(prompt_list.prompts[0].style, "realistic")
        self.assertEqual(prompt_list.prompts[1].style, "artistic")
        # Vérifier que les prompts sont générés automatiquement
        self.assertIsInstance(prompt_list.prompts[0].prompt, str)
        self.assertIsInstance(prompt_list.prompts[1].prompt, str)

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
    def test_calculate_cost(self):
        """Test de calcul des coûts"""
        generator = PromptGenerator()
        
        cost = generator._calculate_cost("gpt-3.5-turbo", 1000, 500)
        self.assertIsInstance(cost, float)
        self.assertGreater(cost, 0)
    


class TestPromptReading(unittest.TestCase):
    """Tests pour les fonctionnalités de lecture de prompts"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.mock_api_key = "test_api_key_123"
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_is_file_path_valid_file(self):
        """Test de détection de chemin de fichier valide"""
        generator = PromptGenerator()
        
        # Créer un fichier temporaire
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("Test content")
            temp_file_path = temp_file.name
        
        try:
            # Test avec un fichier existant
            self.assertTrue(generator._is_file_path(temp_file_path))
            
            # Test avec un texte normal (pas un chemin)
            self.assertFalse(generator._is_file_path("Ceci est un prompt normal"))
            
            # Test avec un chemin inexistant
            self.assertFalse(generator._is_file_path("/chemin/inexistant/fichier.txt"))
            
            # Test avec un texte très long (ne peut pas être un chemin)
            long_text = "Ceci est un très long texte " * 50
            self.assertFalse(generator._is_file_path(long_text))
            
            # Test avec None ou chaîne vide
            self.assertFalse(generator._is_file_path(None))
            self.assertFalse(generator._is_file_path(""))
            
        finally:
            # Nettoyer le fichier temporaire
            os.unlink(temp_file_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_read_prompt_from_text_file(self):
        """Test de lecture d'un prompt depuis un fichier texte"""
        generator = PromptGenerator()
        
        test_content = "Ceci est un prompt de test\navec plusieurs lignes\net du contenu détaillé."
        
        # Tester avec un fichier .txt
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(test_content)
            temp_file_path = temp_file.name
        
        try:
            result = generator._read_prompt_from_text(temp_file_path)
            self.assertEqual(result, test_content)
        finally:
            os.unlink(temp_file_path)
        
        # Tester avec un fichier .md
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
            temp_file.write(test_content)
            temp_file_path = temp_file.name
        
        try:
            result = generator._read_prompt_from_text(temp_file_path)
            self.assertEqual(result, test_content)
        finally:
            os.unlink(temp_file_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_read_prompt_from_json_file(self):
        """Test de lecture d'un prompt depuis un fichier JSON"""
        generator = PromptGenerator()
        
        # Test avec JSON simple (string)
        json_content = '"Ceci est un prompt simple en JSON"'
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file.write(json_content)
            temp_file_path = temp_file.name
        
        try:
            result = generator._read_prompt_from_json(temp_file_path)
            self.assertEqual(result, "Ceci est un prompt simple en JSON")
        finally:
            os.unlink(temp_file_path)
        
        # Test avec JSON objet avec clé 'prompt'
        json_content = json.dumps({"prompt": "Prompt depuis clé prompt"})
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file.write(json_content)
            temp_file_path = temp_file.name
        
        try:
            result = generator._read_prompt_from_json(temp_file_path)
            self.assertEqual(result, "Prompt depuis clé prompt")
        finally:
            os.unlink(temp_file_path)
        
        # Test avec JSON objet avec clé 'description'
        json_content = json.dumps({"description": "Prompt depuis description"})
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file.write(json_content)
            temp_file_path = temp_file.name
        
        try:
            result = generator._read_prompt_from_json(temp_file_path)
            self.assertEqual(result, "Prompt depuis description")
        finally:
            os.unlink(temp_file_path)
        
        # Test avec JSON liste
        json_content = json.dumps(["Premier prompt", "Deuxième prompt"])
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file.write(json_content)
            temp_file_path = temp_file.name
        
        try:
            result = generator._read_prompt_from_json(temp_file_path)
            self.assertEqual(result, "Premier prompt")
        finally:
            os.unlink(temp_file_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_read_prompt_from_file_dispatcher(self):
        """Test du dispatcher de lecture de fichiers selon l'extension"""
        generator = PromptGenerator()
        
        # Test avec fichier .txt
        txt_content = "Prompt depuis fichier texte"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(txt_content)
            temp_file_path = temp_file.name
        
        try:
            result = generator.read_prompt_from_file(temp_file_path)
            self.assertEqual(result, txt_content)
        finally:
            os.unlink(temp_file_path)
        
        # Test avec fichier .json
        json_content = json.dumps({"prompt": "Prompt depuis JSON"})
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file.write(json_content)
            temp_file_path = temp_file.name
        
        try:
            result = generator.read_prompt_from_file(temp_file_path)
            self.assertEqual(result, "Prompt depuis JSON")
        finally:
            os.unlink(temp_file_path)
        
        # Test avec extension inconnue (traité comme texte)
        unknown_content = "Prompt depuis extension inconnue"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.unknown', delete=False) as temp_file:
            temp_file.write(unknown_content)
            temp_file_path = temp_file.name
        
        try:
            result = generator.read_prompt_from_file(temp_file_path)
            self.assertEqual(result, unknown_content)
        finally:
            os.unlink(temp_file_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_resolve_prompt_input_with_file(self):
        """Test de résolution d'entrée prompt avec fichier"""
        generator = PromptGenerator()
        
        # Test avec fichier
        file_content = "Contenu du fichier de prompt"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        try:
            result = generator.resolve_prompt_input(temp_file_path)
            self.assertEqual(result, file_content)
        finally:
            os.unlink(temp_file_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_resolve_prompt_input_with_text(self):
        """Test de résolution d'entrée prompt avec texte direct"""
        generator = PromptGenerator()
        
        # Test avec prompt direct
        direct_prompt = "Ceci est un prompt direct, pas un fichier"
        result = generator.resolve_prompt_input(direct_prompt)
        self.assertEqual(result, direct_prompt)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_extract_prompt_from_data_dict_with_prompt(self):
        """Test d'extraction de prompt depuis dictionnaire avec clé 'prompt'"""
        generator = PromptGenerator()
        
        prompt_data = {
            "prompt": "Prompt complet déjà généré",
            "elements": ["élément1", "élément2"],
            "ambiance": "moderne"
        }
        
        result = generator.extract_prompt_from_data(prompt_data)
        self.assertEqual(result, "Prompt complet déjà généré")
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_extract_prompt_from_data_dict_without_prompt(self):
        """Test d'extraction de prompt depuis dictionnaire sans clé 'prompt'"""
        generator = PromptGenerator()
        
        prompt_data = {
            "elements": ["élément1", "élément2"],
            "ambiance": "moderne et élégant",
            "style": "photographique professionnel",
            "details_techniques": "haute résolution, éclairage naturel",
            "contraintes": "pas de texte, composition équilibrée"
        }
        
        result = generator.extract_prompt_from_data(prompt_data)
        expected_lines = [
            "Éléments visuels: élément1, élément2",
            "Ambiance: moderne et élégant",
            "Style: photographique professionnel",
            "Détails techniques: haute résolution, éclairage naturel",
            "Contraintes: pas de texte, composition équilibrée"
        ]
        expected = "\n".join(expected_lines)
        self.assertEqual(result, expected)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_extract_prompt_from_data_string(self):
        """Test d'extraction de prompt depuis string"""
        generator = PromptGenerator()
        
        prompt_data = "Ceci est un prompt simple sous forme de string"
        result = generator.extract_prompt_from_data(prompt_data)
        self.assertEqual(result, prompt_data)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_read_prompt_from_file_error_handling(self):
        """Test de gestion d'erreurs lors de la lecture de fichier"""
        generator = PromptGenerator()
        
        # Test avec fichier inexistant
        result = generator.read_prompt_from_file("/fichier/inexistant.txt")
        self.assertIn("Erreur lors de la lecture du fichier", result)


if __name__ == '__main__':
    unittest.main()