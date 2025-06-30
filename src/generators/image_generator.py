#!/usr/bin/env python3
"""
Module pour générer des images avec l'API OpenAI (GPT-Image-1, DALL-E)
"""

import os
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import openai
import requests
from enum import Enum
from ..marketing_config import ImageStyle

# Charger les variables d'environnement
load_dotenv()

class ImageStyle(Enum):
    """Énumération des styles d'images disponibles"""
    REALISTIC = "realistic"
    CARTOON = "cartoon"
    ARTISTIC = "artistic"
    ANIME = "anime"
    WATERCOLOR = "watercolor"
    SKETCH = "sketch"
    CUTE = "cute"
    MAJESTIC = "majestic"
    MINIMALIST = "minimalist"
    VINTAGE = "vintage"
    
    @classmethod
    def get_style_prompts(cls):
        """Retourne le dictionnaire des descriptions de styles"""
        return {
            cls.REALISTIC.value: "Une image réaliste et détaillée, photographie de haute qualité",
            cls.CARTOON.value: "Une image mignonne en style cartoon, illustration colorée",
            cls.ARTISTIC.value: "Une image en style artistique, peinture à l'huile",
            cls.ANIME.value: "Une image en style anime japonais, dessin animé",
            cls.WATERCOLOR.value: "Une image en aquarelle, peinture douce et colorée",
            cls.SKETCH.value: "Une image en croquis au crayon, dessin artistique",
            cls.CUTE.value: "Une image adorable et mignonne, yeux grands et expressifs",
            cls.MAJESTIC.value: "Une image majestueuse et élégante, pose royale",
            cls.MINIMALIST.value: "Une image en style minimaliste, design épuré",
            cls.VINTAGE.value: "Une image en style vintage, rétro et classique"
        }
    
    @classmethod
    def get_default_styles(cls):
        """Retourne la liste des styles par défaut pour generate_multiple_styles"""
        return [cls.REALISTIC.value, cls.CARTOON.value, cls.ARTISTIC.value, cls.CUTE.value]
    
    @classmethod
    def is_valid_style(cls, style):
        """Vérifie si un style est valide"""
        return style in [s.value for s in cls]

class ImageGenerator:
    def __init__(self, api_key=None):
        """Initialise le générateur d'images"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("Clé API OpenAI requise. Définissez OPENAI_API_KEY dans .env ou passez-la en paramètre.")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.output_dir = Path("generated") / "images"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuration des modèles et leurs tarifs (en USD par image)
        self.models = {
            "gpt-image-1": {
                "name": "GPT-Image-1",
                "description": "Modèle d'image le plus récent d'OpenAI (remplace DALL-E)",
                "pricing": {
                    "1024x1024": {"standard": 0.040, "hd": 0.080},
                    "1024x1536": {"standard": 0.080, "hd": 0.120},
                    "1536x1024": {"standard": 0.080, "hd": 0.120},
                    "auto": {"standard": 0.040, "hd": 0.080}
                },
                "supported_sizes": ["1024x1024", "1024x1536", "1536x1024", "auto"],
                "supported_qualities": ["standard", "hd"],
                "type": "image"
            },
            "dall-e-3": {
                "name": "DALL-E 3",
                "description": "Modèle précédent d'OpenAI pour l'image",
                "pricing": {
                    "1024x1024": {"standard": 0.040, "hd": 0.080},
                    "1792x1024": {"standard": 0.080, "hd": 0.120},
                    "1024x1792": {"standard": 0.080, "hd": 0.120}
                },
                "supported_sizes": ["1024x1024", "1792x1024", "1024x1792"],
                "supported_qualities": ["standard", "hd"],
                "type": "image"
            },
            "dall-e-2": {
                "name": "DALL-E 2",
                "description": "Ancien modèle d'OpenAI, moins cher",
                "pricing": {
                    "256x256": {"standard": 0.016},
                    "512x512": {"standard": 0.018},
                    "1024x1024": {"standard": 0.020}
                },
                "supported_sizes": ["256x256", "512x512", "1024x1024"],
                "supported_qualities": ["standard"],
                "type": "image"
            }
        }
        
        # Modèle par défaut - GPT-Image-1 pour la meilleure qualité
        self.default_model = "gpt-image-1"
    
    def get_available_models(self):
        """Retourne la liste des modèles disponibles avec leurs informations"""
        return {model_id: {
            "name": info["name"],
            "description": info["description"],
            "supported_sizes": info["supported_sizes"],
            "supported_qualities": info["supported_qualities"],
            "pricing": info["pricing"],
            "type": info["type"]
        } for model_id, info in self.models.items()}
    
    def get_model_info(self, model_id):
        """Retourne les informations d'un modèle spécifique"""
        return self.models.get(model_id)
    
    def get_available_styles(self):
        """Retourne la liste des styles disponibles avec leurs descriptions"""
        style_prompts = ImageStyle.get_style_prompts()
        return {
            style: {
                "name": style,
                "description": description
            }
            for style, description in style_prompts.items()
        }
    
    def generate_image(self, prompt=None, style="realistic", size="1024x1024", quality="standard", model="gpt-image-1"):
        """
        Génère une image avec le modèle spécifié
        
        Args:
            prompt (str): Description complète de l'image à générer
            style (str): Style de l'image (realistic, cartoon, artistic, etc.)
            size (str): Taille de l'image
            quality (str): Qualité de l'image (standard, hd)
            model (str): Modèle à utiliser (gpt-image-1, dall-e-3, dall-e-2)
        """
        # Démarrer le timer
        start_time = time.time()
        
        # Vérifier que le modèle est supporté
        if model not in self.models:
            print(f"⚠️  Modèle '{model}' non supporté. Utilisation du modèle par défaut: {self.default_model}")
            model = self.default_model
        
        # Valider le style
        if not ImageStyle.is_valid_style(style):
            print(f"⚠️  Style '{style}' non supporté. Utilisation du style par défaut: {ImageStyle.REALISTIC.value}")
            style = ImageStyle.REALISTIC.value
        
        model_info = self.models[model]
        
        # Vérifier que la taille est supportée par le modèle
        if size not in model_info["supported_sizes"]:
            print(f"⚠️  Taille '{size}' non supportée par {model_info['name']}. Utilisation de la taille par défaut: {model_info['supported_sizes'][0]}")
            size = model_info["supported_sizes"][0]
        
        # Vérifier que la qualité est supportée par le modèle
        if quality not in model_info["supported_qualities"]:
            print(f"⚠️  Qualité '{quality}' non supportée par {model_info['name']}. Utilisation de la qualité par défaut: {model_info['supported_qualities'][0]}")
            quality = model_info["supported_qualities"][0]
        
        # Prompts prédéfinis pour différents styles (utilisés seulement si aucun prompt n'est fourni)
        style_prompts = ImageStyle.get_style_prompts()
        
        # Construire le prompt final
        if prompt:
            base_prompt = prompt
        else:
            base_prompt = style_prompts.get(style, style_prompts["realistic"])
        
        # Ajouter des détails pour améliorer la qualité
        final_prompt = f"{base_prompt}, haute résolution, détaillé, professionnel"
        
        print(f"🎨 Génération d'image avec {model_info['name']}")
        print(f"📝 Prompt: {final_prompt}")
        print(f"📏 Taille: {size}, 🎯 Qualité: {quality}")
        
        try:
            filename = self._generate_with_model(final_prompt, model, size, quality, style)
            if filename:
                total_time = time.time() - start_time
                cost = self._calculate_cost(model, size, quality)
                print(f"⏱️  Temps total: {total_time:.2f} secondes")
                print(f"💰 Coût estimé: ${cost:.3f} USD")
                print(f"✅ Image générée avec succès: {filename}")
            return filename
        except Exception as e:
            generation_time = time.time() - start_time
            print(f"❌ Erreur lors de la génération après {generation_time:.2f} secondes: {str(e)}")
            return None

    def _generate_with_model(self, prompt, model, size, quality, style):
        """Génère une image en utilisant le modèle spécifié (GPT-Image-1, DALL-E, etc.)"""
        try:
            # Préparer les paramètres de génération
            generation_params = {
                "model": model,
                "prompt": prompt,
                "size": size,
                "n": 1
            }
            
            # Ajouter la qualité seulement si supportée par le modèle
            model_info = self.models[model]
            if "quality" in model_info["supported_qualities"]:
                generation_params["quality"] = quality
            
            # Générer l'image
            response = self.client.images.generate(**generation_params)
            
            # Récupérer l'URL ou le base64 selon le modèle
            image_url = None
            image_b64 = None
            if model == "gpt-image-1":
                # GPT-Image-1 peut retourner une image en base64 ou une URL
                data = response.data[0]
                if hasattr(data, 'url') and data.url:
                    image_url = data.url
                elif hasattr(data, 'b64_json') and data.b64_json:
                    image_b64 = data.b64_json
                elif hasattr(data, 'image') and data.image:
                    image_b64 = data.image
                else:
                    # Afficher la structure pour debug
                    print(f"❌ Aucune URL ni image base64 retournée par {model}")
                    print(f"📊 Structure de réponse: {response}")
                    return None
            else:
                # DALL-E a la structure classique
                image_url = response.data[0].url
            
            # Vérifier qu'on a bien une image à sauvegarder
            if not image_url and not image_b64:
                print(f"❌ Aucune image retournée par {model}")
                print(f"📊 Structure de réponse: {response}")
                return None
            
            # Télécharger ou décoder et sauvegarder l'image
            filename = self._save_image(image_url, image_b64, style, model)
            return filename
        except Exception as e:
            print(f"❌ Erreur avec {model}: {str(e)}")
            return None

    def _save_image(self, image_url, image_b64, style, model):
        """Télécharge ou décode et sauvegarde l'image générée, avec un nom explicite du modèle"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Utiliser le nom du modèle tel quel
            model_short = model.replace("-", "_")
            filename = f"{style}_{model_short}_{timestamp}.png"
            filepath = self.output_dir / filename
            if image_url:
                response = requests.get(image_url)
                response.raise_for_status()
                with open(filepath, 'wb') as f:
                    f.write(response.content)
            elif image_b64:
                import base64
                with open(filepath, 'wb') as f:
                    f.write(base64.b64decode(image_b64))
            else:
                print("❌ Impossible de sauvegarder l'image : aucune donnée valide")
                return None
            return filepath
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {str(e)}")
            return None

    def _calculate_cost(self, model, size, quality):
        """Calcule le coût estimé de l'image selon le modèle"""
        try:
            model_info = self.models[model]
            return model_info["pricing"][size][quality]
        except KeyError:
            default_pricing = list(model_info["pricing"].values())[0]
            return list(default_pricing.values())[0]

    def generate_multiple_styles(self, prompt=None, styles=None, model="gpt-image-1", size="1024x1024", quality="standard"):
        """Génère des images dans plusieurs styles avec le modèle spécifié"""
        if styles is None:
            styles = ImageStyle.get_default_styles()
        total_start_time = time.time()
        total_cost = 0.0
        results = []
        for i, style in enumerate(styles, 1):
            print(f"\n🎨 Génération en style {style} ({i}/{len(styles)})...")
            filename = self.generate_image(prompt, style, size, quality, model)
            if filename:
                results.append((style, filename))
                total_cost += self._calculate_cost(model, size, quality)
        total_time = time.time() - total_start_time
        model_info = self.models[model]
        print(f"\n📊 Statistiques globales:")
        print(f"🤖 Modèle utilisé: {model_info['name']}")
        print(f"⏱️  Temps total pour {len(results)} images: {total_time:.2f} secondes")
        print(f"💰 Coût total estimé: ${total_cost:.3f} USD")
        print(f"📈 Temps moyen par image: {total_time/len(results):.2f} secondes")
        return results

    def generate_chat_image(self, prompt=None, style="realistic", size="1024x1024", quality="standard", model="gpt-image-1"):
        """
        Méthode de compatibilité pour générer des images de chat
        (maintenue pour la rétrocompatibilité)
        """
        # Si aucun prompt n'est fourni, créer un prompt par défaut pour un chat
        if not prompt:
            prompt = "Un chat mignon et expressif"
        return self.generate_image(prompt, style, size, quality, model)
