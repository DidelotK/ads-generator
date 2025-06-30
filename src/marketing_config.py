#!/usr/bin/env python3
"""
Configuration pour les hooks marketing
Personnalisez facilement les sujets et styles pour vos campagnes publicitaires
"""

from enum import Enum

# Sujets marketing très engageants (style "ce que l'état ne vous dit pas")
MARKETING_SUBJECTS = [
    "Production d'électricité solaire à domicile",
    "Secrets cachés par l'état sur l'énergie",
    "Méthode révolutionnaire pour réduire ses factures",
    "Technologie interdite par les lobbies",
    "Solution miracle pour l'indépendance énergétique",
    "Cette nouvelle astuce pour produire son électricité",
    "Ce que l'état ne vous dit pas sur l'énergie",
    "La méthode secrète des experts pour économiser",
    "Technologie bannie par les grandes entreprises",
    "Le secret des millionnaires pour l'énergie gratuite"
]

class HookStyle(Enum):
    """Énumération des styles d'accroches disponibles"""
    URGENT = "urgent"
    ENGAGING = "engaging"
    PROFESSIONAL = "professional"
    CREATIVE = "creative"
    EMOTIONAL = "emotional"
    HUMOROUS = "humorous"
    CURIOSITY = "curiosity"
    BENEFIT = "benefit"
    STORY = "story"
    QUESTION = "question"
    CONSPIRATIONNISTE = "conspirationniste"
    
    @classmethod
    def get_style_prompts(cls):
        """Retourne le dictionnaire des descriptions de styles"""
        return {
            cls.URGENT.value: "qui créent un sentiment d'urgence et d'action immédiate",
            cls.ENGAGING.value: "accrocheuses et engageantes qui captent immédiatement l'attention",
            cls.PROFESSIONAL.value: "professionnelles et sérieuses, adaptées à un public business",
            cls.CREATIVE.value: "créatives et originales, avec un angle unique et surprenant",
            cls.EMOTIONAL.value: "émotionnelles et touchantes, qui suscitent des sentiments",
            cls.HUMOROUS.value: "humoristiques et amusantes, avec une touche d'humour",
            cls.CURIOSITY.value: "qui éveillent la curiosité et poussent à en savoir plus",
            cls.BENEFIT.value: "qui mettent l'accent sur les bénéfices et avantages",
            cls.STORY.value: "narratives, qui racontent une histoire ou utilisent une anecdote",
            cls.QUESTION.value: "qui posent des questions pertinentes et provocantes",
            cls.CONSPIRATIONNISTE.value: "qui suggèrent des vérités cachées et des secrets révélés, avec un ton mystérieux et intriguant"
        }
    
    @classmethod
    def get_default_styles(cls):
        """Retourne la liste des styles par défaut pour generate_multiple_styles"""
        return [cls.ENGAGING.value, cls.PROFESSIONAL.value, cls.CREATIVE.value, cls.EMOTIONAL.value]
    
    @classmethod
    def is_valid_style(cls, style):
        """Vérifie si un style est valide"""
        return style in [s.value for s in cls]

# Styles marketing très engageants
MARKETING_STYLES = [
    "urgent",      # Créer un sentiment d'urgence
    "curiosity",   # Éveiller la curiosité
    "benefit",     # Mettre l'accent sur les bénéfices
    "emotional",   # Toucher émotionnellement
    "engaging",    # Accroche engageante
    "question",    # Poser des questions provocantes
    "story",       # Raconter une histoire
    "humorous",    # Humour pour attirer l'attention
    "creative",    # Angle créatif et unique
    "professional" # Ton professionnel mais accrocheur
]

# Configuration des images
IMAGE_CONFIG = {
    "styles": ["realistic", "photographic"],  # Styles d'images plus réalistes
    "size": "1024x1024",                      # Taille des images
    "quality": "hd",                          # Qualité HD pour plus de réalisme
    "model": "dall-e-3"                       # Modèle d'IA pour les images
}

# Configuration des hooks
HOOK_CONFIG = {
    "model": "gpt-3.5-turbo",            # Modèle d'IA pour les hooks
    "language": "français",              # Langue des hooks
    "num_hooks_per_subject": 1           # Nombre de hooks par sujet
}

# Prompts personnalisés pour les images - PLUS RÉALISTES
IMAGE_PROMPTS = {
    "realistic": "Image marketing ultra-réaliste, photographie professionnelle de haute qualité, style publicitaire moderne, couleurs naturelles, éclairage professionnel, composition parfaite, détails nets",
    "photographic": "Photographie marketing réaliste, style documentaire professionnel, éclairage naturel, couleurs authentiques, composition équilibrée, haute résolution, détails précis",
    "urgent": "Image marketing réaliste avec sentiment d'urgence, photographie professionnelle, couleurs chaudes naturelles, éclairage dramatique, composition impactante",
    "curiosity": "Image marketing mystérieuse et réaliste, photographie artistique, éclairage contrasté naturel, couleurs profondes, composition intrigante",
    "benefit": "Image marketing réaliste axée sur les bénéfices, photographie lifestyle, éclairage doux naturel, couleurs harmonieuses, composition rassurante"
}

# Thèmes de couleurs pour les images
COLOR_THEMES = {
    "energy": ["#FF6B35", "#F7931E", "#FFD700"],      # Couleurs énergétiques
    "trust": ["#2E86AB", "#A23B72", "#F18F01"],       # Couleurs de confiance
    "urgency": ["#FF0000", "#FF4500", "#FF6347"],     # Couleurs d'urgence
    "success": ["#32CD32", "#228B22", "#90EE90"],     # Couleurs de succès
    "mystery": ["#4B0082", "#800080", "#9370DB"]      # Couleurs mystérieuses
}

# Mots-clés marketing pour enrichir les prompts
MARKETING_KEYWORDS = [
    "révolutionnaire", "secret", "interdit", "miracle", "astuce",
    "méthode", "technologie", "solution", "découverte", "innovation",
    "exclusif", "limité", "urgent", "gratuit", "économies",
    "indépendance", "liberté", "contrôle", "puissance", "succès"
]

# Phrases d'accroche types pour inspiration - ÉTENDU
HOOK_TEMPLATES = [
    # Templates d'urgence et de rareté
    "Cette nouvelle {technologie} pour {bénéfice}",
    "Ce que {autorité} ne vous dit pas sur {sujet}",
    "La méthode secrète des {experts} pour {résultat}",
    "{Technologie} interdite par les {lobbies}",
    "Le secret des {millionnaires} pour {objectif}",
    "Découvrez pourquoi {sujet} est {qualificatif}",
    "Cette {solution} va {transformer} votre {domaine}",
    "Les {experts} utilisent cette {méthode} depuis {temps}",
    "Attention: {avertissement} sur {sujet}",
    "Rejoignez les {nombre} personnes qui ont {action}",
    
    # Templates de curiosité et de mystère
    "Ce que {profession} ne veulent pas que vous sachiez",
    "La vérité cachée sur {sujet} révélée",
    "Pourquoi {sujet} est {qualificatif} que vous pensez",
    "Le {secret} que {autorité} garde sous silence",
    "Découvrez le {mystère} derrière {sujet}",
    "Ce que les {experts} ne partagent jamais",
    "La {vérité} sur {sujet} enfin dévoilée",
    "Pourquoi {sujet} va {changer} votre vie",
    "Le {facteur} caché qui explique {phénomène}",
    "Ce que {nombre}% des gens ignorent sur {sujet}",
    
    # Templates de bénéfices et de résultats
    "Comment {action} en {temps} seulement",
    "La {méthode} qui {résultat} à coup sûr",
    "Transformez votre {domaine} avec cette {technique}",
    "Obtenez {bénéfice} sans {effort}",
    "La {solution} qui {résout} tous vos {problèmes}",
    "Découvrez comment {action} facilement",
    "La {stratégie} qui {multiplie} vos {résultats}",
    "Comment {atteindre} {objectif} rapidement",
    "La {technologie} qui {révolutionne} {domaine}",
    "Obtenez {résultat} en {temps} record",
    
    # Templates émotionnels et personnels
    "Imaginez {scénario} dans votre vie",
    "Ce que {personne} a découvert va vous {émotion}",
    "La {histoire} qui va {toucher} votre cœur",
    "Comment {sujet} a {changé} ma vie pour toujours",
    "Le {moment} qui a tout {transformé}",
    "Ce que {expérience} m'a appris sur {sujet}",
    "La {révélation} qui m'a {marqué} à jamais",
    "Comment {sujet} peut {améliorer} votre quotidien",
    "Le {secret} qui m'a permis de {réussir}",
    "Ce que {événement} m'a révélé sur {sujet}",
    
    # Templates de questions provocantes
    "Et si {sujet} était {qualificatif} que vous croyez?",
    "Que se passerait-il si vous {action}?",
    "Pourquoi {nombre}% des gens {échouent}?",
    "Êtes-vous prêt à {découvrir} {vérité}?",
    "Que feriez-vous si {scénario}?",
    "Pourquoi {sujet} est-il {qualificatif}?",
    "Et si {solution} existait vraiment?",
    "Que diriez-vous si {bénéfice} était possible?",
    "Pourquoi {experts} gardent-ils {secret}?",
    "Et si {technologie} pouvait {transformer} tout?",
    
    # Templates de preuve sociale
    "{Nombre} personnes ont déjà {action}",
    "Rejoignez les {nombre} utilisateurs satisfaits",
    "Ce que disent les {profession} sur {sujet}",
    "La {méthode} approuvée par {experts}",
    "Pourquoi {nombre}% recommandent {solution}",
    "Les {témoignages} qui parlent d'eux-mêmes",
    "Ce que {clients} disent de {produit}",
    "La {technique} utilisée par {celebrités}",
    "Pourquoi {nombre} entreprises choisissent {solution}",
    "Les {résultats} obtenus par {utilisateurs}",
    
    # Templates de rareté et d'exclusivité
    "Offre limitée: {bénéfice} exclusif",
    "Seulement {nombre} places disponibles",
    "Accès exclusif à {contenu}",
    "Cette {opportunité} ne se représentera plus",
    "Offre spéciale pour {durée} seulement",
    "Accès prioritaire à {solution}",
    "Édition limitée de {produit}",
    "Cette {méthode} n'est plus disponible",
    "Dernière chance de {action}",
    "Accès VIP à {contenu} exclusif",
    
    # Templates de transformation
    "De {état_initial} à {état_final} en {temps}",
    "Transformez {problème} en {solution}",
    "Comment {changer} votre {situation}",
    "De {difficulté} à {succès} facilement",
    "Transformez votre {domaine} du jour au lendemain",
    "Comment {passer} de {état1} à {état2}",
    "La {méthode} qui {transforme} tout",
    "De {échec} à {victoire} en {étapes}",
    "Transformez {négatif} en {positif}",
    "Comment {évolution} votre {situation}",
    
    # Templates de révélation et de découverte
    "Ce que {étude} révèle sur {sujet}",
    "La {découverte} qui {change} tout",
    "Ce que {recherche} nous apprend",
    "La {révélation} sur {sujet} enfin publique",
    "Ce que {scientifiques} ont découvert",
    "La {vérité} cachée dans {données}",
    "Ce que {analyse} révèle vraiment",
    "La {découverte} qui {surprend} tout le monde",
    "Ce que {étude} nous cache",
    "La {révélation} qui {explique} tout"
]

def get_marketing_subjects(num_subjects=5):
    """Retourne une liste de sujets marketing"""
    return MARKETING_SUBJECTS[:num_subjects]

def get_marketing_styles(num_styles=5):
    """Retourne une liste de styles marketing"""
    return MARKETING_STYLES[:num_styles]

def get_image_prompt(hook_text, style="realistic"):
    """Génère un prompt d'image basé sur le hook et le style"""
    # Créer un prompt plus réaliste et détaillé
    if style == "realistic":
        base_prompt = f"Photographie marketing ultra-réaliste pour: {hook_text}. "
        base_prompt += "Style publicitaire professionnel, photographie de haute qualité, éclairage studio naturel, "
        base_prompt += "couleurs authentiques, composition parfaite, détails nets, haute résolution, "
        base_prompt += "style documentaire moderne, sans effets artificiels, réalisme photographique"
    elif style == "photographic":
        base_prompt = f"Photographie marketing documentaire pour: {hook_text}. "
        base_prompt += "Style photo-journalisme professionnel, éclairage naturel, couleurs vraies, "
        base_prompt += "composition équilibrée, détails précis, haute définition, "
        base_prompt += "style reportage, authenticité maximale, réalisme pur"
    else:
        base_prompt = f"Image marketing réaliste pour: {hook_text}. "
        base_prompt += IMAGE_PROMPTS.get(style, IMAGE_PROMPTS["realistic"])
    
    return base_prompt

def get_color_theme(style):
    """Retourne un thème de couleur basé sur le style"""
    theme_mapping = {
        "urgent": "urgency",
        "curiosity": "mystery", 
        "benefit": "success",
        "emotional": "trust",
        "engaging": "energy"
    }
    return COLOR_THEMES.get(theme_mapping.get(style, "energy"))

def get_random_template():
    """Retourne un template d'accroche aléatoire"""
    import random
    return random.choice(HOOK_TEMPLATES)

def get_templates_by_category(category):
    """Retourne les templates d'une catégorie spécifique"""
    categories = {
        "urgence": HOOK_TEMPLATES[:10],
        "curiosité": HOOK_TEMPLATES[10:20],
        "bénéfices": HOOK_TEMPLATES[20:30],
        "émotionnel": HOOK_TEMPLATES[30:40],
        "questions": HOOK_TEMPLATES[40:50],
        "preuve_sociale": HOOK_TEMPLATES[50:60],
        "rareté": HOOK_TEMPLATES[60:70],
        "transformation": HOOK_TEMPLATES[70:80],
        "révélation": HOOK_TEMPLATES[80:90]
    }
    return categories.get(category, HOOK_TEMPLATES)

if __name__ == "__main__":
    print("🎯 Configuration Marketing")
    print("=" * 40)
    print(f"📝 Sujets disponibles: {len(MARKETING_SUBJECTS)}")
    print(f"🎨 Styles disponibles: {len(MARKETING_STYLES)}")
    print(f"🖼️  Styles d'images: {IMAGE_CONFIG['styles']}")
    print(f"🎨 Thèmes de couleurs: {list(COLOR_THEMES.keys())}")
    print(f"🔑 Mots-clés marketing: {len(MARKETING_KEYWORDS)}")
    print(f"📋 Templates d'accroche: {len(HOOK_TEMPLATES)}")
    
    print(f"\n📋 Catégories de templates:")
    categories = ["urgence", "curiosité", "bénéfices", "émotionnel", "questions", 
                  "preuve_sociale", "rareté", "transformation", "révélation"]
    for cat in categories:
        templates = get_templates_by_category(cat)
        print(f"  • {cat}: {len(templates)} templates") 