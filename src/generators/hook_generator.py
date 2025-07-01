#!/usr/bin/env python3
"""
Module pour générer des accroches avec l'API OpenAI (ChatGPT)
"""

import os
import time
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import openai
from typing import List
from pydantic import BaseModel, Field, ValidationError
from enum import Enum
from src.marketing_config import HookStyle

# Charger les variables d'environnement
load_dotenv()

class Hook(BaseModel):
    hook: str = Field(..., description="L'accroche percutante (titre ou phrase d'accroche)")
    description: str = Field(..., description="Description détaillée de l'angle et de l'approche")

class HookList(BaseModel):
    hooks: List[Hook]

class HookGenerator:
    def __init__(self, api_key=None):
        """Initialise le générateur d'accroches"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("Clé API OpenAI requise. Définissez OPENAI_API_KEY dans .env ou passez-la en paramètre.")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.output_dir = Path("generated") / "hooks"
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
        style_prompts = HookStyle.get_style_prompts()
        return {
            style: {
                "name": style,
                "description": description
            }
            for style, description in style_prompts.items()
        }
    
    def generate_hooks(self, subject, num_hooks=5, style="engaging", model="gpt-3.5-turbo", language="français"):
        """
        Génère des accroches pour un sujet donné (avec parsing Pydantic et function calling)
        """
        start_time = time.time()
        if model not in self.models:
            print(f"⚠️  Modèle '{model}' non supporté. Utilisation du modèle par défaut: {self.default_model}")
            model = self.default_model
        
        # Valider le style
        if not HookStyle.is_valid_style(style):
            print(f"⚠️  Style '{style}' non supporté. Utilisation du style par défaut: {HookStyle.ENGAGING.value}")
            style = HookStyle.ENGAGING.value
            
        model_info = self.models[model]
        style_prompts = HookStyle.get_style_prompts()
        style_description = style_prompts.get(style, style_prompts[HookStyle.ENGAGING.value])
        
        # Définition de la fonction pour le function calling
        function_def = {
            "name": "generate_hooks",
            "description": "Génère une liste d'accroches pour un sujet donné.",
            "parameters": {
                "type": "object",
                "properties": {
                    "hooks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "hook": {
                                    "type": "string",
                                    "description": "L'accroche percutante (titre ou phrase d'accroche)"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Description détaillée de l'angle et de l'approche"
                                }
                            },
                            "required": ["hook", "description"]
                        }
                    }
                },
                "required": ["hooks"]
            }
        }
        
        prompt = f"""Tu es un expert en marketing et en création d'accroches percutantes.

Génère {num_hooks} accroches {style_description} pour le sujet suivant : '{subject}'.

IMPORTANT : Les accroches doivent être COURTES et PERCUTANTES (maximum 60 caractères pour le hook principal).

Format de réponse requis (JSON valide) :
{{
  "hooks": [
    {{
      "hook": "Accroche courte et percutante",
      "description": "Description brève de l'angle"
    }},
    {{
      "hook": "Autre accroche courte",
      "description": "Description concise"
    }}
  ]
}}

Règles :
- Hooks : Maximum 60 caractères, phrases courtes et impactantes
- Descriptions : Maximum 120 caractères, explications concises
- Les accroches doivent être en {language}, variées et non répétitives
- Privilégier les phrases courtes et directes
- Éviter les formulations longues et complexes

Retourne UNIQUEMENT le JSON, sans texte avant ou après."""

        print(f"🎯 Génération de {num_hooks} accroches pour: {subject}")
        print(f"🤖 Modèle: {model_info['name']}")
        print(f"🎨 Style: {style}")
        print(f"🌍 Langue: {language}")
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Tu es un expert en marketing et en création d'accroches percutantes. Tu réponds toujours au format JSON valide."},
                    {"role": "user", "content": prompt}
                ],
                functions=[function_def],
                function_call={"name": "generate_hooks"},
                max_tokens=model_info["max_tokens"],
                temperature=0.8
            )
            generation_time = time.time() - start_time
            
            # Récupérer la réponse structurée
            arguments = response.choices[0].message.function_call.arguments
            print(f"🔍 Réponse brute de l'API: {arguments[:200]}...")
            
            hooks = []
            try:
                # Essayer de parser avec Pydantic
                hooks_obj = HookList.model_validate_json(arguments)
                hooks = [h.model_dump() for h in hooks_obj.hooks]
                print(f"✅ Parsing Pydantic réussi: {len(hooks)} hooks")
            except ValidationError as ve:
                print(f"⚠️  Erreur de validation Pydantic, tentative de parsing manuel...")
                print(f"❌ Détails: {ve}")
                
                # Fallback: parsing manuel
                try:
                    import json
                    # Essayer de parser comme JSON simple
                    data = json.loads(arguments)
                    if isinstance(data, dict) and "hooks" in data:
                        hooks = data["hooks"]
                        print(f"✅ Parsing JSON manuel réussi: {len(hooks)} hooks")
                    else:
                        # Essayer de parser directement comme liste
                        if isinstance(data, list):
                            hooks = data
                            print(f"✅ Parsing liste directe réussi: {len(hooks)} hooks")
                        else:
                            raise ValueError("Format de données inattendu")
                except (json.JSONDecodeError, ValueError) as json_error:
                    print(f"⚠️  Erreur JSON, tentative de parsing textuel...")
                    print(f"❌ Détails JSON: {json_error}")
                    
                    # Fallback final: parsing textuel
                    hooks = self._parse_hooks_from_text(arguments, num_hooks)
                    print(f"✅ Parsing textuel réussi: {len(hooks)} hooks")
            
            # Valider et nettoyer les hooks
            hooks = self._validate_and_clean_hooks(hooks, num_hooks)
            
            # Calculer les tokens utilisés
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
            cost = self._calculate_cost(model, input_tokens, output_tokens)
            
            print(f"⏱️  Temps de génération: {generation_time:.2f} secondes")
            print(f"💰 Coût estimé: ${cost:.4f} USD")
            print(f"📊 Tokens utilisés: {total_tokens} (entrée: {input_tokens}, sortie: {output_tokens})")
            print(f"✅ {len(hooks)} accroches générées")
            
            filename = self._save_hooks(hooks, subject, style, model)
            print(f"\n🎯 Accroches générées:")
            for i, hook_data in enumerate(hooks, 1):
                print(f"\n{i}. {hook_data['hook']}")
                print(f"   Description: {hook_data['description']}")
            if filename:
                print(f"\n💾 Résultats sauvegardés dans: {filename}")
            return hooks
            
        except Exception as e:
            generation_time = time.time() - start_time
            print(f"❌ Erreur lors de la génération après {generation_time:.2f} secondes: {str(e)}")
            return None
    
    def _parse_hooks_from_text(self, text, num_hooks):
        """Parse les hooks depuis un texte brut"""
        hooks = []
        lines = text.split('\n')
        current_hook = None
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('{') or line.startswith('}'):
                continue
                
            # Chercher les patterns d'accroches
            if '"hook"' in line or "hook" in line.lower():
                if current_hook and current_hook.get('hook'):
                    hooks.append(current_hook)
                current_hook = {"hook": "", "description": ""}
                
                # Extraire l'accroche
                if ':' in line:
                    hook_text = line.split(':', 1)[1].strip().strip('"').strip(',')
                    current_hook["hook"] = hook_text
                    
            elif '"description"' in line or "description" in line.lower():
                if current_hook and ':' in line:
                    desc_text = line.split(':', 1)[1].strip().strip('"').strip(',')
                    current_hook["description"] = desc_text
        
        # Ajouter la dernière accroche
        if current_hook and current_hook.get('hook'):
            hooks.append(current_hook)
        
        # Si pas assez de hooks, essayer de générer des hooks simples
        if len(hooks) < num_hooks:
            print(f"⚠️  Seulement {len(hooks)} hooks trouvés, génération de hooks simples...")
            simple_hooks = self._generate_simple_hooks(text, num_hooks - len(hooks))
            hooks.extend(simple_hooks)
        
        return hooks
    
    def _generate_simple_hooks(self, text, num_needed):
        """Génère des hooks simples à partir du texte"""
        hooks = []
        sentences = text.split('.')
        
        for i, sentence in enumerate(sentences[:num_needed]):
            sentence = sentence.strip()
            if len(sentence) > 10:  # Ignorer les phrases trop courtes
                hooks.append({
                    "hook": sentence[:100],  # Limiter la longueur
                    "description": f"Accroche générée automatiquement #{i+1}"
                })
        
        return hooks
    
    def _validate_and_clean_hooks(self, hooks, expected_num):
        """Valide et nettoie les hooks"""
        valid_hooks = []
        
        for hook in hooks:
            if isinstance(hook, dict):
                # S'assurer que les champs requis existent
                hook_text = hook.get('hook', '').strip()
                description = hook.get('description', '').strip()
                
                if hook_text and len(hook_text) > 5:  # Hook valide
                    valid_hooks.append({
                        "hook": hook_text,
                        "description": description if description else f"Description pour: {hook_text[:50]}..."
                    })
            elif isinstance(hook, str) and len(hook.strip()) > 5:
                # Si c'est juste une string, la traiter comme un hook
                valid_hooks.append({
                    "hook": hook.strip(),
                    "description": f"Accroche: {hook[:50]}..."
                })
        
        # S'assurer qu'on a le bon nombre de hooks
        if len(valid_hooks) < expected_num:
            print(f"⚠️  Seulement {len(valid_hooks)} hooks valides sur {expected_num} attendus")
        
        return valid_hooks[:expected_num]
    
    def _calculate_cost(self, model, input_tokens, output_tokens):
        """Calcule le coût estimé selon le modèle et les tokens utilisés"""
        try:
            model_info = self.models[model]
            input_cost = (input_tokens / 1000) * model_info["input_cost"]
            output_cost = (output_tokens / 1000) * model_info["output_cost"]
            return input_cost + output_cost
        except KeyError:
            return 0.0
    
    def _parse_hooks_manually(self, content):
        """Parse manuellement les accroches si le JSON échoue"""
        hooks = []
        lines = content.split('\n')
        current_hook = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('"hook"') or line.startswith("hook"):
                # Nouvelle accroche
                if current_hook:
                    hooks.append(current_hook)
                current_hook = {"hook": "", "description": ""}
                # Extraire l'accroche
                hook_text = line.split(':', 1)[1].strip().strip('"').strip(',')
                current_hook["hook"] = hook_text
            elif line.startswith('"description"') or line.startswith("description"):
                # Description de l'accroche
                if current_hook:
                    desc_text = line.split(':', 1)[1].strip().strip('"').strip(',')
                    current_hook["description"] = desc_text
        
        # Ajouter la dernière accroche
        if current_hook:
            hooks.append(current_hook)
        
        return hooks
    
    def _save_hooks(self, hooks, subject, style, model):
        """Sauvegarde les accroches dans un fichier JSON"""
        try:
            # Créer un nom de fichier unique
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_subject = "".join(c for c in subject if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_subject = safe_subject.replace(' ', '_')[:30]
            filename = f"hooks_{safe_subject}_{style}_{model}_{timestamp}.json"
            filepath = self.output_dir / filename
            
            # Préparer les données à sauvegarder
            data = {
                "metadata": {
                    "subject": subject,
                    "style": style,
                    "model": model,
                    "generated_at": datetime.now().isoformat(),
                    "num_hooks": len(hooks)
                },
                "hooks": hooks
            }
            
            # Sauvegarder en JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return filepath
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {str(e)}")
            return None
    
    def generate_multiple_styles(self, subject, styles=None, num_hooks=3, model="gpt-3.5-turbo"):
        """Génère des accroches dans plusieurs styles"""
        if styles is None:
            styles = HookStyle.get_default_styles()
        
        total_start_time = time.time()
        total_cost = 0.0
        
        all_results = {}
        for i, style in enumerate(styles, 1):
            print(f"\n🎨 Génération en style {style} ({i}/{len(styles)})...")
            hooks = self.generate_hooks(subject, num_hooks, style, model)
            if hooks:
                all_results[style] = hooks
                # Estimation du coût (approximatif)
                total_cost += 0.01  # Estimation basée sur l'expérience
        
        total_time = time.time() - total_start_time
        model_info = self.models[model]
        print(f"\n📊 Statistiques globales:")
        print(f"🤖 Modèle utilisé: {model_info['name']}")
        print(f"⏱️  Temps total pour {len(all_results)} styles: {total_time:.2f} secondes")
        print(f"💰 Coût total estimé: ${total_cost:.4f} USD")
        print(f"📈 Temps moyen par style: {total_time/len(all_results):.2f} secondes")
        
        return all_results
    
    def generate_hooks_simple(self, subject, num_hooks=5, style="engaging", model="gpt-3.5-turbo", language="français"):
        """
        Génère des accroches avec une approche plus simple et robuste
        """
        start_time = time.time()
        if model not in self.models:
            print(f"⚠️  Modèle '{model}' non supporté. Utilisation du modèle par défaut: {self.default_model}")
            model = self.default_model
        
        # Valider le style
        if not HookStyle.is_valid_style(style):
            print(f"⚠️  Style '{style}' non supporté. Utilisation du style par défaut: {HookStyle.ENGAGING.value}")
            style = HookStyle.ENGAGING.value
            
        model_info = self.models[model]
        style_prompts = HookStyle.get_style_prompts()
        style_description = style_prompts.get(style, style_prompts[HookStyle.ENGAGING.value])
        
        prompt = f"""Tu es un expert en marketing et en création d'accroches percutantes.

Génère {num_hooks} accroches {style_description} pour le sujet suivant : '{subject}'.

IMPORTANT : Les accroches doivent être COURTES et PERCUTANTES (maximum 60 caractères pour le hook principal).

Format de réponse requis (JSON valide) :
{{
  "hooks": [
    {{
      "hook": "Accroche courte et percutante",
      "description": "Description brève de l'angle"
    }},
    {{
      "hook": "Autre accroche courte",
      "description": "Description concise"
    }}
  ]
}}

Règles :
- Hooks : Maximum 60 caractères, phrases courtes et impactantes
- Descriptions : Maximum 120 caractères, explications concises
- Les accroches doivent être en {language}, variées et non répétitives
- Privilégier les phrases courtes et directes
- Éviter les formulations longues et complexes

Retourne UNIQUEMENT le JSON, sans texte avant ou après."""

        print(f"🎯 Génération de {num_hooks} accroches pour: {subject}")
        print(f"🤖 Modèle: {model_info['name']}")
        print(f"🎨 Style: {style}")
        print(f"🌍 Langue: {language}")
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Tu es un expert en marketing. Tu réponds UNIQUEMENT au format JSON valide, sans texte supplémentaire."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=model_info["max_tokens"],
                temperature=0.8
            )
            
            generation_time = time.time() - start_time
            content = response.choices[0].message.content.strip()
            
            print(f"🔍 Réponse brute de l'API: {content[:200]}...")
            
            hooks = []
            try:
                import json
                # Nettoyer la réponse pour extraire le JSON
                content = self._extract_json_from_response(content)
                data = json.loads(content)
                
                if isinstance(data, dict) and "hooks" in data:
                    hooks = data["hooks"]
                elif isinstance(data, list):
                    hooks = data
                else:
                    raise ValueError("Format de données inattendu")
                    
                print(f"✅ Parsing JSON réussi: {len(hooks)} hooks")
                
            except (json.JSONDecodeError, ValueError) as e:
                print(f"⚠️  Erreur JSON, tentative de parsing textuel...")
                print(f"❌ Détails: {e}")
                hooks = self._parse_hooks_from_text(content, num_hooks)
                print(f"✅ Parsing textuel réussi: {len(hooks)} hooks")
            
            # Valider et nettoyer les hooks
            hooks = self._validate_and_clean_hooks(hooks, num_hooks)
            
            # Calculer les tokens utilisés
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
            cost = self._calculate_cost(model, input_tokens, output_tokens)
            
            print(f"⏱️  Temps de génération: {generation_time:.2f} secondes")
            print(f"💰 Coût estimé: ${cost:.4f} USD")
            print(f"📊 Tokens utilisés: {total_tokens} (entrée: {input_tokens}, sortie: {output_tokens})")
            print(f"✅ {len(hooks)} accroches générées")
            
            filename = self._save_hooks(hooks, subject, style, model)
            print(f"\n🎯 Accroches générées:")
            for i, hook_data in enumerate(hooks, 1):
                print(f"\n{i}. {hook_data['hook']}")
                print(f"   Description: {hook_data['description']}")
            if filename:
                print(f"\n💾 Résultats sauvegardés dans: {filename}")
            return hooks
            
        except Exception as e:
            generation_time = time.time() - start_time
            print(f"❌ Erreur lors de la génération après {generation_time:.2f} secondes: {str(e)}")
            return None
    
    def _extract_json_from_response(self, content):
        """Extrait le JSON de la réponse de l'API"""
        # Chercher le début du JSON
        start_idx = content.find('{')
        if start_idx == -1:
            start_idx = content.find('[')
        
        if start_idx == -1:
            return content
        
        # Chercher la fin du JSON (parenthèse fermante correspondante)
        brace_count = 0
        bracket_count = 0
        end_idx = start_idx
        
        for i, char in enumerate(content[start_idx:], start_idx):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
            elif char == '[':
                bracket_count += 1
            elif char == ']':
                bracket_count -= 1
            
            if (brace_count == 0 and bracket_count == 0) or (brace_count < 0 or bracket_count < 0):
                end_idx = i + 1
                break
        
        return content[start_idx:end_idx] 