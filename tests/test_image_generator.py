#!/usr/bin/env python3
"""
Tests pour le générateur d'images et son intégration avec le PromptGenerator
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

from generators.image_generator import ImageGenerator, ImageStyle
from src.generators.prompt_generator import PromptGenerator

class TestImageGeneratorBasic(unittest.TestCase):
    """Tests de base pour ImageGenerator"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.mock_api_key = "test_api_key_123"
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_initialization_with_env_key(self):
        """Test d'initialisation avec clé d'environnement"""
        generator = ImageGenerator()
        self.assertEqual(generator.api_key, 'test_key')
        self.assertIsNotNone(generator.client)
        self.assertTrue(generator.output_dir.exists())
        self.assertIsInstance(generator.prompt_generator, PromptGenerator)
    
    def test_initialization_with_provided_key(self):
        """Test d'initialisation avec clé fournie"""
        generator = ImageGenerator(api_key=self.mock_api_key)
        self.assertEqual(generator.api_key, self.mock_api_key)
    
    def test_initialization_without_key(self):
        """Test d'initialisation sans clé API"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                ImageGenerator()
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_get_available_models(self):
        """Test de récupération des modèles disponibles"""
        generator = ImageGenerator()
        models = generator.get_available_models()
        
        self.assertIsInstance(models, dict)
        self.assertIn("gpt-image-1", models)
        self.assertIn("dall-e-3", models)
        self.assertIn("dall-e-2", models)
        
        for model_id, model_info in models.items():
            self.assertIn("name", model_info)
            self.assertIn("description", model_info)
            self.assertIn("supported_sizes", model_info)
            self.assertIn("supported_qualities", model_info)
            self.assertIn("pricing", model_info)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_get_model_info(self):
        """Test de récupération d'informations d'un modèle spécifique"""
        generator = ImageGenerator()
        
        # Test avec modèle existant
        model_info = generator.get_model_info("gpt-image-1")
        self.assertIsNotNone(model_info)
        self.assertIn("name", model_info)
        self.assertIn("description", model_info)
        
        # Test avec modèle inexistant
        model_info = generator.get_model_info("modele-inexistant")
        self.assertIsNone(model_info)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_get_available_styles(self):
        """Test de récupération des styles disponibles"""
        generator = ImageGenerator()
        styles = generator.get_available_styles()
        
        self.assertIsInstance(styles, dict)
        self.assertGreater(len(styles), 0)
        
        for style_name, style_info in styles.items():
            self.assertIn("name", style_info)
            self.assertIn("description", style_info)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_calculate_cost(self):
        """Test de calcul de coût"""
        generator = ImageGenerator()
        
        # Test avec modèle et paramètres valides
        cost = generator._calculate_cost("gpt-image-1", "1024x1024", "standard")
        self.assertGreater(cost, 0)
        self.assertIsInstance(cost, float)
        
        # Test avec paramètres invalides
        cost_invalid = generator._calculate_cost("gpt-image-1", "invalid_size", "standard")
        self.assertGreaterEqual(cost_invalid, 0)  # Devrait utiliser une valeur par défaut
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_save_image_with_url(self):
        """Test de sauvegarde d'image depuis URL"""
        generator = ImageGenerator()
        
        # Mock de la requête HTTP
        with patch('src.generators.image_generator.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.content = b"fake_image_data"
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            filename = generator._save_image(
                image_url="https://example.com/image.png",
                image_b64=None,
                style="realistic",
                model="gpt-image-1"
            )
            
            if filename:  # Si la sauvegarde réussit
                self.assertTrue(filename.exists())
                # Nettoyer
                filename.unlink()
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_save_image_with_base64(self):
        """Test de sauvegarde d'image depuis base64"""
        generator = ImageGenerator()
        
        # Créer une image base64 simple (pixel noir)
        import base64
        fake_image_b64 = base64.b64encode(b"fake_image_data").decode()
        
        filename = generator._save_image(
            image_url=None,
            image_b64=fake_image_b64,
            style="realistic",
            model="gpt-image-1"
        )
        
        if filename:  # Si la sauvegarde réussit
            self.assertTrue(filename.exists())
            # Nettoyer
            filename.unlink()
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_save_image_no_data(self):
        """Test de sauvegarde sans données"""
        generator = ImageGenerator()
        
        filename = generator._save_image(
            image_url=None,
            image_b64=None,
            style="realistic",
            model="gpt-image-1"
        )
        
        self.assertIsNone(filename)

class TestImageGeneratorIntegration(unittest.TestCase):
    """Tests d'intégration entre ImageGenerator et PromptGenerator"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.mock_api_key = "test_api_key_123"
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_image_generator_initializes_prompt_generator(self):
        """Test que ImageGenerator initialise correctement un PromptGenerator"""
        generator = ImageGenerator()
        
        # Vérifier que le PromptGenerator est initialisé
        self.assertIsInstance(generator.prompt_generator, PromptGenerator)
        self.assertEqual(generator.prompt_generator.api_key, generator.api_key)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_image_generator_uses_prompt_generator_for_file_resolution(self):
        """Test que ImageGenerator utilise PromptGenerator pour résoudre les prompts de fichiers"""
        generator = ImageGenerator()
        
        # Créer un fichier de prompt temporaire
        test_prompt = "Ceci est un prompt de test depuis un fichier"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(test_prompt)
            temp_file_path = temp_file.name
        
        try:
            # Tester que la résolution de prompt utilise bien le PromptGenerator
            resolved_prompt = generator.prompt_generator.resolve_prompt_input(temp_file_path)
            self.assertEqual(resolved_prompt, test_prompt)
            
            # Tester avec un prompt direct
            direct_prompt = "Prompt direct"
            resolved_direct = generator.prompt_generator.resolve_prompt_input(direct_prompt)
            self.assertEqual(resolved_direct, direct_prompt)
            
        finally:
            os.unlink(temp_file_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_image_generator_uses_prompt_generator_for_data_extraction(self):
        """Test que ImageGenerator utilise PromptGenerator pour extraire les données de prompt"""
        generator = ImageGenerator()
        
        # Test avec dictionnaire contenant une clé 'prompt'
        prompt_data_with_prompt = {
            "prompt": "Prompt complet déjà généré",
            "elements": ["élément1", "élément2"],
            "ambiance": "moderne"
        }
        
        extracted = generator.prompt_generator.extract_prompt_from_data(prompt_data_with_prompt)
        self.assertEqual(extracted, "Prompt complet déjà généré")
        
        # Test avec dictionnaire sans clé 'prompt'
        prompt_data_structured = {
            "elements": ["smartphone", "personne souriante"],
            "ambiance": "moderne et dynamique",
            "style": "photographique professionnel",
            "details_techniques": "haute résolution, éclairage naturel",
            "contraintes": "pas de texte, composition équilibrée"
        }
        
        extracted_structured = generator.prompt_generator.extract_prompt_from_data(prompt_data_structured)
        expected_lines = [
            "Éléments visuels: smartphone, personne souriante",
            "Ambiance: moderne et dynamique",
            "Style: photographique professionnel",
            "Détails techniques: haute résolution, éclairage naturel",
            "Contraintes: pas de texte, composition équilibrée"
        ]
        expected = "\n".join(expected_lines)
        self.assertEqual(extracted_structured, expected)
        
        # Test avec string simple
        simple_prompt = "Simple prompt string"
        extracted_simple = generator.prompt_generator.extract_prompt_from_data(simple_prompt)
        self.assertEqual(extracted_simple, simple_prompt)

class TestImageStyleCompatibility(unittest.TestCase):
    """Tests de compatibilité des styles entre ImageGenerator et PromptGenerator"""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_image_styles_are_valid(self):
        """Test que les styles ImageStyle sont valides"""
        generator = ImageGenerator()
        
        # Tester tous les styles ImageStyle
        for style in ImageStyle:
            style_value = style.value
            # Les styles d'image peuvent être différents des styles de prompt
            # mais ils doivent être des strings valides
            self.assertIsInstance(style_value, str)
            self.assertGreater(len(style_value), 0)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_get_available_styles_compatibility(self):
        """Test de compatibilité des méthodes get_available_styles"""
        image_generator = ImageGenerator()
        prompt_generator = PromptGenerator()
        
        # Les deux générateurs doivent avoir une méthode get_available_styles
        image_styles = image_generator.get_available_styles()
        prompt_styles = prompt_generator.get_available_styles()
        
        self.assertIsInstance(image_styles, dict)
        self.assertIsInstance(prompt_styles, dict)
        
        # Vérifier la structure des retours
        for style_name, style_info in image_styles.items():
            self.assertIn("name", style_info)
            self.assertIn("description", style_info)
        
        for style_name, style_info in prompt_styles.items():
            self.assertIn("name", style_info)
            self.assertIn("description", style_info)

class TestImageGeneratorAPIIntegration(unittest.TestCase):
    """Tests d'intégration avec l'API OpenAI mockée"""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.image_generator.openai.OpenAI')
    def test_generate_image_success(self, mock_openai):
        """Test de génération réussie d'image"""
        # Configuration du mock OpenAI
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        # Mock de la réponse d'image
        mock_response = Mock()
        mock_response.data = [Mock()]
        mock_response.data[0].url = "https://example.com/image.png"
        mock_client.images.generate.return_value = mock_response
        
        # Mock de la requête HTTP pour télécharger l'image
        with patch('src.generators.image_generator.requests.get') as mock_get:
            mock_get.return_value.content = b"fake_image_data"
            mock_get.return_value.raise_for_status.return_value = None
            
            generator = ImageGenerator()
            filename = generator.generate_image(
                prompt="Test image generation",
                style="realistic",
                size="1024x1024",
                quality="standard",
                model="gpt-image-1"
            )
            
            self.assertIsNotNone(filename)
            # Nettoyer si le fichier a été créé
            if filename and filename.exists():
                filename.unlink()
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.image_generator.openai.OpenAI')
    def test_generate_image_with_invalid_model(self, mock_openai):
        """Test avec modèle invalide"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.data = [Mock()]
        mock_response.data[0].url = "https://example.com/image.png"
        mock_client.images.generate.return_value = mock_response
        
        with patch('src.generators.image_generator.requests.get') as mock_get:
            mock_get.return_value.content = b"fake_image_data"
            mock_get.return_value.raise_for_status.return_value = None
            
            generator = ImageGenerator()
            filename = generator.generate_image(
                prompt="Test image generation",
                style="realistic",
                size="1024x1024",
                quality="standard",
                model="modele_inexistant"  # Modèle invalide
            )
            
            # Devrait utiliser le modèle par défaut et fonctionner
            self.assertIsNotNone(filename)
            if filename and filename.exists():
                filename.unlink()
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.image_generator.openai.OpenAI')
    def test_generate_image_with_invalid_style(self, mock_openai):
        """Test avec style invalide"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.data = [Mock()]
        mock_response.data[0].url = "https://example.com/image.png"
        mock_client.images.generate.return_value = mock_response
        
        with patch('src.generators.image_generator.requests.get') as mock_get:
            mock_get.return_value.content = b"fake_image_data"
            mock_get.return_value.raise_for_status.return_value = None
            
            generator = ImageGenerator()
            filename = generator.generate_image(
                prompt="Test image generation",
                style="style_inexistant",  # Style invalide
                size="1024x1024",
                quality="standard",
                model="gpt-image-1"
            )
            
            # Devrait utiliser le style par défaut et fonctionner
            self.assertIsNotNone(filename)
            if filename and filename.exists():
                filename.unlink()
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.image_generator.openai.OpenAI')
    def test_generate_image_api_error(self, mock_openai):
        """Test de gestion d'erreur API"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        # Simuler une erreur API
        mock_client.images.generate.side_effect = Exception("Erreur API simulée")
        
        generator = ImageGenerator()
        filename = generator.generate_image(
            prompt="Test image generation",
            style="realistic",
            size="1024x1024",
            quality="standard",
            model="gpt-image-1"
        )
        
        # Devrait retourner None en cas d'erreur
        self.assertIsNone(filename)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.image_generator.openai.OpenAI')
    def test_generate_multiple_styles(self, mock_openai):
        """Test de génération en plusieurs styles"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.data = [Mock()]
        mock_response.data[0].url = "https://example.com/image.png"
        mock_client.images.generate.return_value = mock_response
        
        with patch('src.generators.image_generator.requests.get') as mock_get:
            mock_get.return_value.content = b"fake_image_data"
            mock_get.return_value.raise_for_status.return_value = None
            
            generator = ImageGenerator()
            results = generator.generate_multiple_styles(
                prompt="Test image generation",
                styles=["realistic", "cartoon"],
                model="gpt-image-1"
            )
            
            self.assertIsInstance(results, list)
            self.assertEqual(len(results), 2)
            
            # Nettoyer les fichiers créés
            for style, filename in results:
                if filename and filename.exists():
                    filename.unlink()
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.image_generator.openai.OpenAI')
    def test_generate_images_from_file_success(self, mock_openai):
        """Test de génération d'images depuis un fichier JSON"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.data = [Mock()]
        mock_response.data[0].url = "https://example.com/image.png"
        mock_client.images.generate.return_value = mock_response
        
        with patch('src.generators.image_generator.requests.get') as mock_get:
            mock_get.return_value.content = b"fake_image_data"
            mock_get.return_value.raise_for_status.return_value = None
            
            # Créer un fichier de test temporaire
            test_data = {
                "metadata": {
                    "hook": "Test hook",
                    "style": "realistic",
                    "model": "gpt-3.5-turbo",
                    "generated_at": "2024-01-15T10:30:00",
                    "num_prompts": 2
                },
                "prompts": [
                    {
                        "prompt": "Une image de test 1",
                        "description": "Description test 1"
                    },
                    {
                        "elements": ["élément1", "élément2"],
                        "ambiance": "moderne",
                        "style": "photographique",
                        "description": "Description test 2"
                    }
                ]
            }
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                json.dump(test_data, temp_file)
                temp_file_path = temp_file.name
            
            try:
                generator = ImageGenerator()
                result = generator.generate_images_from_file(
                    temp_file_path,
                    model="gpt-image-1",
                    size="1024x1024",
                    quality="standard"
                )
                
                self.assertIsInstance(result, dict)
                self.assertIn("generated_files", result)
                self.assertIn("total_cost", result)
                self.assertIn("success_count", result)
                self.assertIn("total_count", result)
                self.assertEqual(result["total_count"], 2)
                
                # Nettoyer les fichiers générés
                for filename in result["generated_files"]:
                    if filename and filename.exists():
                        filename.unlink()
                        
            finally:
                os.unlink(temp_file_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_generate_images_from_file_invalid_json(self):
        """Test avec fichier JSON invalide"""
        # Créer un fichier JSON invalide
        invalid_json = "{ invalid json content"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file.write(invalid_json)
            temp_file_path = temp_file.name
        
        try:
            generator = ImageGenerator()
            result = generator.generate_images_from_file(temp_file_path)
            
            # Devrait retourner des valeurs par défaut pour un JSON invalide
            self.assertEqual(result["success_count"], 0)
            self.assertEqual(result["total_count"], 0)
            
        finally:
            os.unlink(temp_file_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_generate_images_from_file_no_prompts(self):
        """Test avec fichier sans prompts"""
        test_data = {
            "metadata": {"test": "data"},
            "prompts": []
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(test_data, temp_file)
            temp_file_path = temp_file.name
        
        try:
            generator = ImageGenerator()
            result = generator.generate_images_from_file(temp_file_path)
            
            self.assertEqual(result["success_count"], 0)
            self.assertEqual(result["total_count"], 0)
            
        finally:
            os.unlink(temp_file_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.image_generator.openai.OpenAI')
    def test_generate_with_model_different_formats(self, mock_openai):
        """Test de génération avec différents formats de réponse"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        # Test avec réponse base64
        mock_response = Mock()
        mock_response.data = [Mock()]
        mock_response.data[0].url = None
        mock_response.data[0].b64_json = "fake_base64_data"
        mock_client.images.generate.return_value = mock_response
        
        generator = ImageGenerator()
        filename = generator._generate_with_model(
            "Test prompt",
            "gpt-image-1",
            "1024x1024",
            "standard",
            "realistic"
        )
        
        if filename and filename.exists():
            filename.unlink()
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.image_generator.openai.OpenAI')
    def test_generate_with_model_no_image_data(self, mock_openai):
        """Test de génération sans données d'image"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        # Mock sans URL ni base64
        mock_response = Mock()
        mock_response.data = [Mock()]
        mock_response.data[0].url = None
        mock_response.data[0].b64_json = None
        mock_client.images.generate.return_value = mock_response
        
        generator = ImageGenerator()
        filename = generator._generate_with_model(
            "Test prompt",
            "gpt-image-1",
            "1024x1024",
            "standard",
            "realistic"
        )
        
        # Devrait retourner None si pas de données d'image
        self.assertIsNone(filename)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.image_generator.openai.OpenAI')  
    def test_generate_image_with_invalid_size_and_quality(self, mock_openai):
        """Test avec taille et qualité invalides"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.data = [Mock()]
        mock_response.data[0].url = "https://example.com/image.png"
        mock_client.images.generate.return_value = mock_response
        
        with patch('src.generators.image_generator.requests.get') as mock_get:
            mock_get.return_value.content = b"fake_image_data"
            mock_get.return_value.raise_for_status.return_value = None
            
            generator = ImageGenerator()
            filename = generator.generate_image(
                prompt="Test image generation",
                style="realistic",
                size="invalid_size",  # Taille invalide
                quality="invalid_quality",  # Qualité invalide
                model="gpt-image-1"
            )
            
            # Devrait fonctionner en utilisant les valeurs par défaut
            self.assertIsNotNone(filename)
            if filename and filename.exists():
                filename.unlink()

class TestImageGeneratorPromptHandling(unittest.TestCase):
    """Tests spécifiques à la gestion des prompts dans ImageGenerator"""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('src.generators.image_generator.openai.OpenAI')
    def test_generate_image_with_file_prompt_integration(self, mock_openai):
        """Test d'intégration complète de génération d'image avec prompt depuis fichier"""
        # Configuration du mock OpenAI
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        # Mock de la réponse d'image
        mock_response = Mock()
        mock_response.data = [Mock()]
        mock_response.data[0].url = "https://example.com/image.png"
        mock_client.images.generate.return_value = mock_response
        
        # Mock de la requête HTTP pour télécharger l'image
        with patch('src.generators.image_generator.requests.get') as mock_get:
            mock_get.return_value.content = b"fake_image_data"
            mock_get.return_value.raise_for_status.return_value = None
            
            generator = ImageGenerator()
            
            # Créer un fichier de prompt temporaire
            test_prompt = "Une image réaliste d'un produit technologique moderne"
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                temp_file.write(test_prompt)
                temp_file_path = temp_file.name
            
            try:
                # Tester que le prompt est bien résolu
                resolved_prompt = generator.prompt_generator.resolve_prompt_input(temp_file_path)
                self.assertEqual(resolved_prompt, test_prompt)
                
            finally:
                os.unlink(temp_file_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_generate_images_from_file_integration(self):
        """Test d'intégration pour la génération d'images depuis un fichier de prompts"""
        generator = ImageGenerator()
        
        # Créer un fichier de prompts temporaire
        prompts_data = {
            "metadata": {
                "hook": "Économisez sur vos factures d'énergie",
                "style": "realistic",
                "model": "gpt-3.5-turbo",
                "generated_at": "2024-01-15T10:30:00",
                "num_prompts": 2
            },
            "prompts": [
                {
                    "elements": ["compteur électrique", "factures", "personne souriante"],
                    "ambiance": "rassurante et moderne",
                    "style": "photographie professionnelle",
                    "details_techniques": "haute résolution, éclairage naturel",
                    "contraintes": "pas de texte sur l'image",
                    "description": "Image montrant les économies d'énergie",
                    "prompt": "Compteur électrique moderne avec factures et personne souriante, ambiance rassurante"
                },
                {
                    "elements": ["maison", "panneaux solaires", "famille"],
                    "ambiance": "écologique et positive",
                    "style": "photographie lifestyle",
                    "details_techniques": "couleurs vives, éclairage doux",
                    "contraintes": "composition équilibrée",
                    "description": "Famille devant maison avec panneaux solaires",
                    "prompt": "Famille heureuse devant maison avec panneaux solaires, ambiance écologique"
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(prompts_data, temp_file, ensure_ascii=False, indent=2)
            temp_file_path = temp_file.name
        
        try:
            # Tester l'extraction des prompts depuis le fichier
            for prompt_data in prompts_data['prompts']:
                extracted_prompt = generator.prompt_generator.extract_prompt_from_data(prompt_data)
                # Devrait retourner le prompt complet déjà généré
                self.assertEqual(extracted_prompt, prompt_data['prompt'])
                
            # Tester la fonction generate_images_from_file avec un fichier invalide
            result = generator.generate_images_from_file("/fichier/inexistant.json")
            self.assertEqual(result["success_count"], 0)
            self.assertEqual(result["total_count"], 0)
            
        finally:
            os.unlink(temp_file_path)

class TestImageGeneratorErrorHandling(unittest.TestCase):
    """Tests de gestion d'erreurs pour ImageGenerator avec PromptGenerator"""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_error_handling_for_missing_file(self):
        """Test de gestion d'erreur pour fichier manquant"""
        generator = ImageGenerator()
        
        # Tester avec un fichier inexistant
        result = generator.prompt_generator.read_prompt_from_file("/fichier/inexistant.txt")
        self.assertIn("Erreur lors de la lecture du fichier", result)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_error_handling_for_invalid_json(self):
        """Test de gestion d'erreur pour JSON invalide"""
        generator = ImageGenerator()
        
        # Créer un fichier JSON invalide
        invalid_json = "{ invalid json content"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file.write(invalid_json)
            temp_file_path = temp_file.name
        
        try:
            result = generator.prompt_generator.read_prompt_from_file(temp_file_path)
            self.assertIn("Erreur lors de la lecture du fichier", result)
            
        finally:
            os.unlink(temp_file_path)


if __name__ == '__main__':
    unittest.main() 