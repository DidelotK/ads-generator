#!/usr/bin/env python3
"""
Module pour générer des images avec l'API OpenAI (DALL-E)
"""

import os
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import openai
import requests

# Charger les variables d'environnement
load_dotenv()

class ImageGenerator:
    def __init__(self, api_key=None):
        """Initialise le générateur d'images"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("Clé API OpenAI requise. Définissez OPENAI_API_KEY dans .env ou passez-la en paramètre.")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.output_dir = Path("generated_images")
        self.output_dir.mkdir(exist_ok=True)
        
        # Configuration des modèles et leurs tarifs (en USD par image)
        self.models = {
            "dall-e-3": {
                "name": "DALL-E 3",
                "description": "Modèle le plus récent et avancé d'OpenAI",
                "pricing": {
                    "1024x1024": {"standard": 0.040, "hd": 0.080},
                    "1792x1024": {"standard": 0.080, "hd": 0.120},
                    "1024x1792": {"standard": 0.080, "hd": 0.120}
                },
                "supported_sizes": ["1024x1024", "1792x1024", "1024x1792"],
                "supported_qualities": ["standard", "hd"]
            },
            "dall-e-2": {
                "name": "DALL-E 2",
                "description": "Modèle précédent d'OpenAI, moins cher",
                "pricing": {
                    "256x256": {"standard": 0.016},
                    "512x512": {"standard": 0.018},
                    "1024x1024": {"standard": 0.020}
                },
                "supported_sizes": ["256x256", "512x512", "1024x1024"],
                "supported_qualities": ["standard"]
            }
        }
        
        # Modèle par défaut
        self.default_model = "dall-e-3"
    
    def get_available_models(self):
        """Retourne la liste des modèles disponibles avec leurs informations"""
        return {model_id: {
            "name": info["name"],
            "description": info["description"],
            "supported_sizes": info["supported_sizes"],
            "supported_qualities": info["supported_qualities"],
            "pricing": info["pricing"]
        } for model_id, info in self.models.items()}
    
    def get_model_info(self, model_id):
        """Retourne les informations d'un modèle spécifique"""
        return self.models.get(model_id)
    
    def generate_image(self, subject_type="chat", prompt=None, style="realistic", size="1024x1024", quality="standard", model="dall-e-3"):
        """
        Génère une image avec le modèle spécifié
        
        Args:
            subject_type (str): Type de sujet (chat, chien, paysage, portrait, etc.)
            prompt (str): Description personnalisée de l'image
            style (str): Style de l'image (realistic, cartoon, artistic, etc.)
            size (str): Taille de l'image
            quality (str): Qualité de l'image (standard, hd)
            model (str): Modèle à utiliser (dall-e-3, dall-e-2)
        """
        # Démarrer le timer
        start_time = time.time()
        
        # Vérifier que le modèle est supporté
        if model not in self.models:
            print(f"⚠️  Modèle '{model}' non supporté. Utilisation du modèle par défaut: {self.default_model}")
            model = self.default_model
        
        model_info = self.models[model]
        
        # Vérifier que la taille est supportée par le modèle
        if size not in model_info["supported_sizes"]:
            print(f"⚠️  Taille '{size}' non supportée par {model_info['name']}. Utilisation de la taille par défaut: {model_info['supported_sizes'][0]}")
            size = model_info["supported_sizes"][0]
        
        # Vérifier que la qualité est supportée par le modèle
        if quality not in model_info["supported_qualities"]:
            print(f"⚠️  Qualité '{quality}' non supportée par {model_info['name']}. Utilisation de la qualité par défaut: {model_info['supported_qualities'][0]}")
            quality = model_info["supported_qualities"][0]
        
        # Prompts prédéfinis pour différents styles
        style_prompts = {
            "realistic": f"Un {subject_type} réaliste et détaillé, photographie de haute qualité",
            "cartoon": f"Un {subject_type} mignon en style cartoon, illustration colorée",
            "artistic": f"Un {subject_type} en style artistique, peinture à l'huile",
            "anime": f"Un {subject_type} en style anime japonais, dessin animé",
            "watercolor": f"Un {subject_type} en aquarelle, peinture douce et colorée",
            "sketch": f"Un {subject_type} en croquis au crayon, dessin artistique",
            "cute": f"Un {subject_type} adorable et mignon, yeux grands et expressifs",
            "majestic": f"Un {subject_type} majestueux et élégant, pose royale",
            "minimalist": f"Un {subject_type} en style minimaliste, design épuré",
            "vintage": f"Un {subject_type} en style vintage, rétro et classique"
        }
        
        # Construire le prompt final
        if prompt:
            base_prompt = f"Une image de {subject_type}: {prompt}"
        else:
            base_prompt = style_prompts.get(style, style_prompts["realistic"])
        
        # Ajouter des détails pour améliorer la qualité
        final_prompt = f"{base_prompt}, haute résolution, détaillé, professionnel"
        
        print(f"🎨 Génération d'image avec {model_info['name']}")
        print(f"📝 Prompt: {final_prompt}")
        print(f"📏 Taille: {size}, 🎯 Qualité: {quality}")
        
        try:
            # Préparer les paramètres de génération
            generation_params = {
                "model": model,
                "prompt": final_prompt,
                "size": size,
                "n": 1
            }
            
            # Ajouter la qualité seulement si supportée par le modèle
            if "quality" in model_info["supported_qualities"]:
                generation_params["quality"] = quality
            
            # Générer l'image
            response = self.client.images.generate(**generation_params)
            
            # Calculer le temps écoulé
            generation_time = time.time() - start_time
            
            # Récupérer l'URL de l'image
            image_url = response.data[0].url
            
            # Calculer le coût estimé
            cost = self._calculate_cost(model, size, quality)
            
            # Afficher les statistiques
            print(f"⏱️  Temps de génération: {generation_time:.2f} secondes")
            print(f"💰 Coût estimé: ${cost:.3f} USD")
            print(f"📊 Taille du prompt: {len(final_prompt)} caractères")
            
            # Télécharger et sauvegarder l'image
            download_start = time.time()
            filename = self._download_and_save_image(image_url, subject_type, style, model)
            download_time = time.time() - download_start
            
            if filename:
                total_time = time.time() - start_time
                print(f"📥 Temps de téléchargement: {download_time:.2f} secondes")
                print(f"⏱️  Temps total: {total_time:.2f} secondes")
                print(f"✅ Image générée avec succès: {filename}")
            
            return filename
            
        except Exception as e:
            generation_time = time.time() - start_time
            print(f"❌ Erreur lors de la génération après {generation_time:.2f} secondes: {str(e)}")
            return None
    
    def _calculate_cost(self, model, size, quality):
        """Calcule le coût estimé de l'image selon le modèle"""
        try:
            model_info = self.models[model]
            return model_info["pricing"][size][quality]
        except KeyError:
            # Valeur par défaut si la taille/qualité n'est pas dans la liste
            default_pricing = list(model_info["pricing"].values())[0]
            return list(default_pricing.values())[0]
    
    def _download_and_save_image(self, image_url, subject_type, style, model):
        """Télécharge et sauvegarde l'image générée"""
        try:
            # Télécharger l'image
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Créer un nom de fichier unique avec le modèle
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_short = model.replace("-", "").replace("dall", "dalle")
            filename = f"{subject_type}_{style}_{model_short}_{timestamp}.png"
            filepath = self.output_dir / filename
            
            # Sauvegarder l'image
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return filepath
            
        except Exception as e:
            print(f"❌ Erreur lors du téléchargement: {str(e)}")
            return None
    
    def generate_multiple_styles(self, subject_type="chat", prompt=None, styles=None, model="dall-e-3", size="1024x1024", quality="standard"):
        """Génère des images dans plusieurs styles avec le modèle spécifié"""
        if styles is None:
            styles = ["realistic", "cartoon", "artistic", "cute"]
        
        total_start_time = time.time()
        total_cost = 0.0
        
        results = []
        for i, style in enumerate(styles, 1):
            print(f"\n🎨 Génération en style {style} ({i}/{len(styles)})...")
            filename = self.generate_image(subject_type, prompt, style, size, quality, model)
            if filename:
                results.append((style, filename))
                # Ajouter le coût estimé avec les paramètres réels
                total_cost += self._calculate_cost(model, size, quality)
        
        total_time = time.time() - total_start_time
        model_info = self.models[model]
        print(f"\n📊 Statistiques globales:")
        print(f"🤖 Modèle utilisé: {model_info['name']}")
        print(f"⏱️  Temps total pour {len(results)} images: {total_time:.2f} secondes")
        print(f"💰 Coût total estimé: ${total_cost:.3f} USD")
        print(f"📈 Temps moyen par image: {total_time/len(results):.2f} secondes")
        
        return results
    
    def generate_chat_image(self, prompt=None, style="realistic", size="1024x1024", quality="standard", model="dall-e-3"):
        """
        Méthode de compatibilité pour générer des images de chat
        (maintenue pour la rétrocompatibilité)
        """
        return self.generate_image("chat", prompt, style, size, quality, model) 