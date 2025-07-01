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
    elements: List[str] = Field(..., description="Les éléments visuels à inclure dans l'image")
    ambiance: str = Field(..., description="L'ambiance et l'émotion à transmettre")
    style: str = Field(..., description="Le style photographique à utiliser")
    details_techniques: str = Field(..., description="Les détails techniques (qualité, couleurs, etc.)")
    contraintes: str = Field(..., description="Les contraintes de l'image (pas de texte, composition, etc.)")
    description: str = Field(..., description="Description de l'approche visuelle")
    
    @property
    def prompt(self) -> str:
        """Génère le prompt complet en combinant tous les éléments"""
        elements_str = ", ".join(self.elements)
        
        prompt_parts = [
            f"Éléments visuels: {elements_str}",
            f"Ambiance: {self.ambiance}",
            f"Style: {self.style}",
            f"Détails techniques: {self.details_techniques}",
            f"Contraintes: {self.contraintes}"
        ]
        
        return ". ".join(prompt_parts) + "."
    
    def model_dump(self, **kwargs):
        """Override pour inclure la propriété prompt dans la sérialisation"""
        data = super().model_dump(**kwargs)
        data['prompt'] = self.prompt
        return data

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

        print(f"🎨 Génération de {num_prompts} prompts d'images pour: {hook}")
        print(f"🤖 Modèle: {model_info['name']}")
        print(f"🎨 Style: {style}")
        print(f"🌍 Langue: {language}")
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": """Tu es un expert en création de prompts d'images pour publicités Facebook Ads. 
Tu génères des prompts textuels directs et détaillés, prêts à être utilisés directement pour générer des images avec DALL-E, Midjourney ou Stable Diffusion.

IMPORTANT : Tu dois toujours répondre au format JSON valide avec la structure suivante :
{
  "prompts": [
    {
      "elements": ["élément1", "élément2", "élément3"],
      "ambiance": "Description de l'ambiance et émotion à transmettre",
      "style": "Description du style photographique",
      "details_techniques": "Détails techniques (qualité, couleurs, éclairage, composition)",
      "contraintes": "Contraintes spécifiques (pas de texte, pas d'anomalies, composition équilibrée, etc.)",
      "description": "Description de l'approche visuelle générale"
    }
  ]
}"""},
                    {"role": "user", "content": f"""Génère {num_prompts} prompts d'images pour une publicité Facebook Ads.

CONTEXTE :
- Accroche de l'ads : {hook}
- Description de l'ads : {description}
- Style souhaité : {style_description}

INSTRUCTIONS :
Génère {num_prompts} prompts qui décrivent des images visuellement impactantes pour cette publicité.

Pour chaque prompt, tu dois définir :
- **elements** : Liste des éléments visuels spécifiques à inclure (objets, personnes, environnement) EN RAPPORT DIRECT avec le hook "{hook}"
- **ambiance** : L'ambiance et l'émotion à transmettre (mystérieux, moderne, rassurant, etc.)
- **style** : Le style photographique précis ({style_description})
- **details_techniques** : Détails techniques précis (qualité, couleurs dominantes, type d'éclairage, composition)
- **contraintes** : Contraintes spécifiques (pas de texte sur l'image, pas d'anomalies anatomiques, pas d'éléments flottants, composition équilibrée, éclairage cohérent, couleurs réalistes, qualité professionnelle)
- **description** : Description générale de l'approche visuelle

RÉPONSE REQUISE :
Tu dois répondre UNIQUEMENT au format JSON valide avec la structure exacte :
{{
  "prompts": [
    {{
      "elements": ["élément spécifique 1", "élément spécifique 2", "élément spécifique 3"],
      "ambiance": "Description précise de l'ambiance",
      "style": "{style_description}",
      "details_techniques": "Détails techniques précis",
      "contraintes": "Contraintes spécifiques de l'image",
      "description": "Description de l'approche visuelle"
    }}
  ]
}}

IMPORTANT : Les éléments doivent être EN RAPPORT DIRECT avec "{hook}" et "{description}" !"""}
                ],
                max_tokens=model_info["max_tokens"],
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            generation_time = time.time() - start_time
            
            # Récupérer la réponse JSON
            content = response.choices[0].message.content
            print(f"🔍 Réponse JSON de l'API: {content[:200]}...")
            
            # Parser avec Pydantic
            try:
                prompt_list = ImagePromptList.model_validate_json(content)
                prompts = [prompt.model_dump() for prompt in prompt_list.prompts]
                print(f"✅ {len(prompts)} prompts parsés avec succès via Pydantic")
            except ValidationError as e:
                print(f"❌ Erreur de validation Pydantic: {e}")
                print(f"🔍 Contenu reçu: {content}")
                raise ValueError(f"La réponse de l'API n'est pas dans le format attendu. Erreur de validation: {e}")
            
            # Limiter au nombre demandé
            prompts = prompts[:num_prompts]
            
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

    def resolve_prompt_input(self, prompt_input):
        """
        Résout l'entrée prompt : soit un texte direct, soit un chemin vers un fichier
        
        Args:
            prompt_input (str): Prompt direct ou chemin vers un fichier
            
        Returns:
            str: Prompt résolu
        """
        # Vérifier si c'est un chemin vers un fichier existant
        if self._is_file_path(prompt_input):
            print(f"📁 Lecture du prompt depuis le fichier: {prompt_input}")
            return self.read_prompt_from_file(prompt_input)
        else:
            # C'est un prompt direct
            return prompt_input

    def _is_file_path(self, text):
        """
        Détermine si le texte est un chemin vers un fichier existant
        
        Args:
            text (str): Texte à analyser
            
        Returns:
            bool: True si c'est un chemin vers un fichier existant
        """
        # Vérifications simples pour détecter un chemin de fichier
        if not text or len(text) > 500:  # Prompts très longs peu probable d'être des chemins
            return False
        
        # Vérifier si le fichier existe
        if os.path.exists(text):
            return os.path.isfile(text)
        
        return False

    def read_prompt_from_file(self, file_path):
        """
        Lit un prompt depuis un fichier
        
        Args:
            file_path (str): Chemin vers le fichier
            
        Returns:
            str: Contenu du prompt
        """
        try:
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension == '.json':
                return self._read_prompt_from_json(file_path)
            elif file_extension in ['.txt', '.md', '.text']:
                return self._read_prompt_from_text(file_path)
            else:
                # Essayer de lire comme un fichier texte par défaut
                return self._read_prompt_from_text(file_path)
                
        except Exception as e:
            print(f"❌ Erreur lors de la lecture du fichier {file_path}: {e}")
            return f"Erreur lors de la lecture du fichier: {file_path}"

    def _read_prompt_from_text(self, file_path):
        """
        Lit un prompt depuis un fichier texte simple
        
        Args:
            file_path (str): Chemin vers le fichier texte
            
        Returns:
            str: Contenu du fichier
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        print(f"📝 Prompt lu depuis {file_path}: {content[:100]}...")
        return content

    def _read_prompt_from_json(self, file_path):
        """
        Lit un prompt depuis un fichier JSON simple (pas les fichiers de batch de prompts)
        
        Args:
            file_path (str): Chemin vers le fichier JSON
            
        Returns:
            str: Prompt extrait du JSON
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Différentes structures possibles pour un prompt simple
        if isinstance(data, str):
            # JSON simple contenant juste un string
            prompt = data
        elif isinstance(data, dict):
            if 'prompt' in data:
                # Structure avec clé 'prompt'
                prompt = data['prompt']
            elif 'description' in data:
                # Structure avec clé 'description'
                prompt = data['description']
            elif 'text' in data:
                # Structure avec clé 'text'
                prompt = data['text']
            elif 'content' in data:
                # Structure avec clé 'content'
                prompt = data['content']
            else:
                # Convertir tout le dict en string
                prompt = str(data)
        elif isinstance(data, list) and data:
            # Liste de prompts, prendre le premier
            prompt = str(data[0])
        else:
            prompt = str(data)
        
        print(f"📝 Prompt lu depuis {file_path}: {prompt[:100]}...")
        return prompt

    def extract_prompt_from_data(self, prompt_data):
        """
        Extrait le prompt complet à partir des données de prompt
        
        Args:
            prompt_data: Données du prompt (dict ou str)
            
        Returns:
            str: Prompt complet formaté
        """
        if isinstance(prompt_data, dict):
            # Nouvelle structure avec propriétés séparées
            if 'prompt' in prompt_data:
                # Prompt complet déjà généré
                return prompt_data['prompt']
            else:
                # Construire le prompt à partir des éléments
                elements = prompt_data.get('elements', [])
                ambiance = prompt_data.get('ambiance', '')
                style_desc = prompt_data.get('style', '')
                details_techniques = prompt_data.get('details_techniques', '')
                contraintes = prompt_data.get('contraintes', '')
                
                # Construire le prompt complet
                prompt_parts = []
                if elements:
                    prompt_parts.append(f"Éléments visuels: {', '.join(elements)}")
                if ambiance:
                    prompt_parts.append(f"Ambiance: {ambiance}")
                if style_desc:
                    prompt_parts.append(f"Style: {style_desc}")
                if details_techniques:
                    prompt_parts.append(f"Détails techniques: {details_techniques}")
                if contraintes:
                    prompt_parts.append(f"Contraintes: {contraintes}")
                
                return "\n".join(prompt_parts)
        else:
            # Ancienne structure ou prompt simple
            return str(prompt_data) 