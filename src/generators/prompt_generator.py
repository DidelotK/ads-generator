#!/usr/bin/env python3
"""
Module pour générer des prompts d'images avec l'API OpenAI (ChatGPT)
"""

import os
import time
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import openai
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError
from enum import Enum
from src.marketing_config import HookStyle

# Charger les variables d'environnement
load_dotenv()

class ImagePrompt(BaseModel):
    prompt: str = Field(..., description="Le prompt détaillé pour générer l'image")
    style: str = Field(..., description="Le style d'image (réaliste, artistique, etc.)")
    elements: List[str] = Field(..., description="Les éléments visuels à mettre en avant")
    description: str = Field(..., description="Description de l'approche visuelle")

class ImagePromptList(BaseModel):
    prompts: List[ImagePrompt]

class PromptStyle(Enum):
    """Énumération des styles de prompts d'images disponibles"""
    REALISTIC = "realistic"
    PHOTOGRAPHIC = "photographic"
    ARTISTIC = "artistic"
    COMMERCIAL = "commercial"
    LIFESTYLE = "lifestyle"
    DRAMATIC = "dramatic"
    MINIMALIST = "minimalist"
    VIBRANT = "vibrant"
    PROFESSIONAL = "professional"
    EMOTIONAL = "emotional"
    
    @classmethod
    def get_style_prompts(cls):
        """Retourne le dictionnaire des descriptions de styles"""
        return {
            cls.REALISTIC.value: "style photographique ultra-réaliste, haute qualité, détails nets",
            cls.PHOTOGRAPHIC.value: "photographie professionnelle, éclairage naturel, couleurs authentiques",
            cls.ARTISTIC.value: "style artistique créatif, composition unique, couleurs expressives",
            cls.COMMERCIAL.value: "style publicitaire moderne, composition impactante, couleurs vives",
            cls.LIFESTYLE.value: "style lifestyle authentique, scènes quotidiennes, éclairage doux",
            cls.DRAMATIC.value: "style dramatique, éclairage contrasté, émotions intenses",
            cls.MINIMALIST.value: "style minimaliste, composition épurée, couleurs sobres",
            cls.VIBRANT.value: "style vibrant, couleurs éclatantes, énergie positive",
            cls.PROFESSIONAL.value: "style professionnel, composition équilibrée, couleurs harmonieuses",
            cls.EMOTIONAL.value: "style émotionnel, éclairage doux, atmosphère chaleureuse"
        }
    
    @classmethod
    def get_default_styles(cls):
        """Retourne la liste des styles par défaut"""
        return [cls.REALISTIC.value, cls.PHOTOGRAPHIC.value, cls.COMMERCIAL.value]
    
    @classmethod
    def is_valid_style(cls, style):
        """Vérifie si un style est valide"""
        return style in [s.value for s in cls]

class PromptGenerator:
    def __init__(self, api_key=None):
        """Initialise le générateur de prompts d'images"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("Clé API OpenAI requise. Définissez OPENAI_API_KEY dans .env ou passez-la en paramètre.")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.output_dir = Path("generated") / "prompts"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuration des modèles et leurs tarifs (en USD par 1K tokens)
        self.models = {
            "gpt-4": {
                "name": "GPT-4",
                "description": "Modèle le plus avancé pour la génération de contenu créatif",
                "input_cost": 0.030,  # par 1K tokens d'entrée
                "output_cost": 0.060,  # par 1K tokens de sortie
                "max_tokens": 4096
            },
            "gpt-3.5-turbo": {
                "name": "GPT-3.5 Turbo",
                "description": "Modèle rapide et économique pour la génération de contenu",
                "input_cost": 0.0015,  # par 1K tokens d'entrée
                "output_cost": 0.002,  # par 1K tokens de sortie
                "max_tokens": 4096
            }
        }
        
        # Modèle par défaut
        self.default_model = "gpt-3.5-turbo"
    
    def get_available_models(self):
        """Retourne la liste des modèles disponibles avec leurs informations"""
        return {model_id: {
            "name": info["name"],
            "description": info["description"],
            "input_cost": info["input_cost"],
            "output_cost": info["output_cost"],
            "max_tokens": info["max_tokens"]
        } for model_id, info in self.models.items()}
    
    def get_model_info(self, model_id):
        """Retourne les informations d'un modèle spécifique"""
        return self.models.get(model_id)
    
    def get_available_styles(self):
        """Retourne la liste des styles disponibles avec leurs descriptions"""
        style_prompts = PromptStyle.get_style_prompts()
        return {
            style: {
                "name": style,
                "description": description
            }
            for style, description in style_prompts.items()
        }
    
    def generate_prompts(self, hook, description, num_prompts=3, style="realistic", model="gpt-3.5-turbo", language="français"):
        """
        Génère des prompts d'images pour un hook et une description donnés
        """
        start_time = time.time()
        if model not in self.models:
            print(f"⚠️  Modèle '{model}' non supporté. Utilisation du modèle par défaut: {self.default_model}")
            model = self.default_model
        
        # Valider le style
        if not PromptStyle.is_valid_style(style):
            print(f"⚠️  Style '{style}' non supporté. Utilisation du style par défaut: {PromptStyle.REALISTIC.value}")
            style = PromptStyle.REALISTIC.value
            
        model_info = self.models[model]
        style_prompts = PromptStyle.get_style_prompts()
        style_description = style_prompts.get(style, style_prompts[PromptStyle.REALISTIC.value])

        base_prompt = """Génère une image pour une publicité facebook ads qui a les informations suivantes :

Titre : {hook}
Description : {description}

Sur l'image il pourrait être intéressant de mettre en avant des éléments comme :
{elements}

L'image générée :
- Style : {style_description}
- L'image doit être ultra-réaliste et professionnelle
- Pas de texte, pas de titre, pas de description sur l'image
- Pas d'anomalies anatomiques (humains avec 3 mains, etc.)
- Pas d'éléments flottants ou impossibles
- Composition équilibrée et professionnelle
- Éclairage naturel et cohérent
- Couleurs harmonieuses et réalistes
- Détails nets et précis
- Qualité photographique professionnelle

"""

        print(f"🎨 Génération de {num_prompts} prompts d'images pour: {hook}")
        print(f"🤖 Modèle: {model_info['name']}")
        print(f"🎨 Style: {style}")
        print(f"🌍 Langue: {language}")
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Tu es un expert en création de prompts d'images pour publicités. Tu génères des prompts textuels directs et détaillés, prêts à être utilisés directement pour générer des images. Chaque prompt doit être complet et autonome."},
                    {"role": "user", "content": f"""
Génère {num_prompts} prompts qui seront utilisés par un autre llm pour créer des images. Les prompts doivent être sous le format suivant :
<prompt>
{base_prompt}
</prompt>

IMPORTANT : Chaque prompt doit être un texte complet et détaillé, prêt à être utilisé directement pour générer une image. Retourne les prompts numérotés (1, 2, 3, etc.). Chaque prompt doit être autonome et contenir toutes les informations nécessaires.
                    """}
                ],
                max_tokens=model_info["max_tokens"],
                temperature=0.8
            )
            generation_time = time.time() - start_time
            
            # Récupérer la réponse textuelle
            content = response.choices[0].message.content
            print(f"🔍 Réponse brute de l'API: {content[:200]}...")
            
            # Parser les prompts depuis le texte
            prompts = self._parse_text_prompts(content, num_prompts, style)
            
            # Valider et nettoyer les prompts
            prompts = self._validate_and_clean_prompts(prompts, num_prompts)
            
            # Calculer les coûts
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            cost = self._calculate_cost(model, input_tokens, output_tokens)
            
            print(f"⏱️  Temps de génération: {generation_time:.2f}s")
            print(f"💰 Coût estimé: ${cost:.4f}")
            print(f"📊 Tokens utilisés: {input_tokens} entrée, {output_tokens} sortie")
            
            # Sauvegarder les prompts (JSON et texte)
            self._save_prompts(prompts, hook, style, model)
            self._save_prompts_text(prompts, hook, style, model)
            
            return prompts
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")
            return []
    
    def _parse_text_prompts(self, content, num_prompts, style):
        """Parse les prompts depuis le texte de réponse"""
        prompts = []
        lines = content.split('\n')
        current_prompt = ""
        prompt_number = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Détecter le début d'un nouveau prompt (numéroté)
            if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')) or \
               line.startswith(('1)', '2)', '3)', '4)', '5)', '6)', '7)', '8)', '9)')):
                # Sauvegarder le prompt précédent s'il existe
                if current_prompt:
                    prompts.append({
                        "prompt": current_prompt.strip(),
                        "style": style,
                        "elements": self._extract_elements_from_prompt(current_prompt),
                        "description": f"Prompt {prompt_number} généré automatiquement"
                    })
                    prompt_number += 1
                
                # Commencer un nouveau prompt
                current_prompt = line.split('.', 1)[1] if '.' in line else line.split(')', 1)[1] if ')' in line else line
            else:
                # Continuer le prompt actuel
                if current_prompt:
                    current_prompt += " " + line
                else:
                    current_prompt = line
        
        # Ajouter le dernier prompt
        if current_prompt and len(prompts) < num_prompts:
            prompts.append({
                "prompt": current_prompt.strip(),
                "style": style,
                "elements": self._extract_elements_from_prompt(current_prompt),
                "description": f"Prompt {prompt_number + 1} généré automatiquement"
            })
        
        return prompts
    
    def _extract_elements_from_prompt(self, prompt_text):
        """Extrait les éléments visuels mentionnés dans le prompt"""
        # Mots-clés communs pour les éléments visuels
        visual_keywords = [
            "compteur", "facture", "personne", "humain", "main", "visage", "yeux", "bureau",
            "maison", "appartement", "voiture", "argent", "euro", "dollar", "carte", "téléphone",
            "ordinateur", "écran", "document", "papier", "stylo", "table", "chaise", "fenêtre",
            "porte", "lumière", "ampoule", "électricité", "énergie", "panneau", "solaire",
            "éolienne", "batterie", "câble", "prise", "interrupteur", "thermostat", "chauffage",
            "climatisation", "isolation", "toit", "mur", "sol", "plafond", "escalier", "couloir",
            "cuisine", "salle de bain", "chambre", "salon", "jardin", "balcon", "terrasse"
        ]
        
        elements = []
        prompt_lower = prompt_text.lower()
        
        for keyword in visual_keywords:
            if keyword in prompt_lower:
                elements.append(keyword)
        
        # Si aucun élément trouvé, retourner des éléments génériques
        if not elements:
            elements = ["élément visuel principal", "composition", "éclairage"]
        
        return elements[:5]  # Limiter à 5 éléments
    
    def _parse_prompts_manually(self, content):
        """Parse manuellement les prompts depuis le contenu texte"""
        prompts = []
        try:
            # Essayer d'extraire du JSON
            json_match = self._extract_json_from_response(content)
            if json_match:
                data = json.loads(json_match)
                if isinstance(data, dict) and "prompts" in data:
                    return data["prompts"]
            
            # Fallback: parsing basique
            lines = content.split('\n')
            current_prompt = {}
            
            for line in lines:
                line = line.strip()
                if '"prompt":' in line:
                    current_prompt["prompt"] = line.split('"prompt":')[1].strip().strip('",')
                elif '"style":' in line:
                    current_prompt["style"] = line.split('"style":')[1].strip().strip('",')
                elif '"elements":' in line:
                    # Extraire les éléments
                    elements_start = content.find('"elements":')
                    if elements_start != -1:
                        elements_text = content[elements_start:].split(']')[0]
                        elements = [e.strip().strip('"') for e in elements_text.split('[')[1].split(',')]
                        current_prompt["elements"] = elements
                elif '"description":' in line:
                    current_prompt["description"] = line.split('"description":')[1].strip().strip('",')
                    if len(current_prompt) >= 4:
                        prompts.append(current_prompt.copy())
                        current_prompt = {}
            
            return prompts
            
        except Exception as e:
            print(f"❌ Erreur de parsing manuel: {e}")
            return []
    
    def _validate_and_clean_prompts(self, prompts, expected_num):
        """Valide et nettoie les prompts générés"""
        if not prompts:
            return []
        
        cleaned_prompts = []
        for prompt in prompts:
            if isinstance(prompt, dict):
                # S'assurer que tous les champs requis sont présents
                if "prompt" not in prompt or not prompt["prompt"]:
                    continue
                if "style" not in prompt:
                    prompt["style"] = "realistic"
                if "elements" not in prompt or not prompt["elements"]:
                    prompt["elements"] = ["élément visuel principal"]
                if "description" not in prompt:
                    prompt["description"] = "Approche visuelle standard"
                
                # Nettoyer les éléments
                if isinstance(prompt["elements"], str):
                    prompt["elements"] = [prompt["elements"]]
                
                cleaned_prompts.append(prompt)
        
        # Limiter au nombre demandé
        return cleaned_prompts[:expected_num]
    
    def _calculate_cost(self, model, input_tokens, output_tokens):
        """Calcule le coût estimé de la génération"""
        model_info = self.models.get(model, self.models[self.default_model])
        input_cost = (input_tokens / 1000) * model_info["input_cost"]
        output_cost = (output_tokens / 1000) * model_info["output_cost"]
        return input_cost + output_cost
    
    def _save_prompts(self, prompts, hook, style, model):
        """Sauvegarde les prompts générés dans un fichier JSON"""
        if not prompts:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"prompts_{timestamp}_{style}_{model}.json"
        filepath = self.output_dir / filename
        
        data = {
            "metadata": {
                "hook": hook,
                "style": style,
                "model": model,
                "generated_at": datetime.now().isoformat(),
                "num_prompts": len(prompts)
            },
            "prompts": prompts
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"💾 Prompts JSON sauvegardés: {filepath}")
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde JSON: {e}")
    
    def _save_prompts_text(self, prompts, hook, style, model):
        """Sauvegarde les prompts générés dans un fichier texte prêt à l'emploi"""
        if not prompts:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"prompts_{timestamp}_{style}_{model}.txt"
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"🎨 PROMPTS D'IMAGES GÉNÉRÉS\n")
                f.write(f"=" * 60 + "\n\n")
                f.write(f"📋 Métadonnées:\n")
                f.write(f"   Hook: {hook}\n")
                f.write(f"   Style: {style}\n")
                f.write(f"   Modèle: {model}\n")
                f.write(f"   Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"   Nombre de prompts: {len(prompts)}\n\n")
                f.write(f"=" * 60 + "\n\n")
                
                for i, prompt_data in enumerate(prompts, 1):
                    f.write(f"📸 PROMPT {i} (Style: {prompt_data['style']})\n")
                    f.write(f"-" * 40 + "\n")
                    f.write(f"🎯 Prompt complet:\n")
                    f.write(f"{prompt_data['prompt']}\n\n")
                    f.write(f"🔍 Éléments détectés: {', '.join(prompt_data['elements'])}\n")
                    f.write(f"📄 Description: {prompt_data['description']}\n")
                    f.write(f"\n" + "=" * 60 + "\n\n")
                
                f.write(f"💡 UTILISATION:\n")
                f.write(f"- Copiez le prompt complet dans DALL-E 3\n")
                f.write(f"- Ou utilisez-le avec Midjourney: /imagine [prompt] --ar 1:1 --v 6\n")
                f.write(f"- Ou avec Stable Diffusion ou tout autre générateur d'images\n")
                f.write(f"- Les prompts sont optimisés pour Facebook Ads (pas de texte sur l'image)\n")
            
            print(f"📝 Prompts texte sauvegardés: {filepath}")
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde texte: {e}")
    
    def generate_multiple_styles(self, hook, description, styles=None, num_prompts=2, model="gpt-3.5-turbo"):
        """Génère des prompts pour plusieurs styles différents"""
        if styles is None:
            styles = PromptStyle.get_default_styles()
        
        all_prompts = {}
        for style in styles:
            print(f"\n🎨 Génération pour le style: {style}")
            prompts = self.generate_prompts(hook, description, num_prompts, style, model)
            all_prompts[style] = prompts
        
        return all_prompts
    
    def _extract_json_from_response(self, content):
        """Extrait le JSON de la réponse de l'API"""
        try:
            # Chercher des accolades
            start = content.find('{')
            if start == -1:
                return None
            
            # Trouver la fin correspondante
            brace_count = 0
            for i, char in enumerate(content[start:], start):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        return content[start:i+1]
            
            return None
        except Exception:
            return None 