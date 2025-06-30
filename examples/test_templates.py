#!/usr/bin/env python3
"""
Script pour tester et afficher les templates d'accroches marketing
"""

from src.marketing_config import (
    HOOK_TEMPLATES, 
    get_templates_by_category, 
    get_random_template,
    MARKETING_SUBJECTS,
    MARKETING_STYLES
)

def main():
    """Affiche et teste les templates d'accroches"""
    
    print("🎯 Test des Templates d'Accroches Marketing")
    print("=" * 60)
    
    # Afficher les statistiques
    print(f"📊 Statistiques:")
    print(f"   • Total templates: {len(HOOK_TEMPLATES)}")
    print(f"   • Sujets disponibles: {len(MARKETING_SUBJECTS)}")
    print(f"   • Styles disponibles: {len(MARKETING_STYLES)}")
    
    # Afficher les catégories
    print(f"\n📋 Catégories de templates:")
    categories = ["urgence", "curiosité", "bénéfices", "émotionnel", "questions", 
                  "preuve_sociale", "rareté", "transformation", "révélation"]
    
    for cat in categories:
        templates = get_templates_by_category(cat)
        print(f"   • {cat.capitalize()}: {len(templates)} templates")
    
    # Afficher quelques exemples par catégorie
    print(f"\n🎯 Exemples par catégorie:")
    
    for cat in categories[:5]:  # Afficher les 5 premières catégories
        print(f"\n📌 {cat.upper()}:")
        templates = get_templates_by_category(cat)
        for i, template in enumerate(templates[:3], 1):  # 3 exemples par catégorie
            print(f"   {i}. {template}")
    
    # Afficher des templates aléatoires
    print(f"\n🎲 Templates aléatoires:")
    for i in range(5):
        template = get_random_template()
        print(f"   {i+1}. {template}")
    
    # Exemples avec des variables remplies
    print(f"\n💡 Exemples avec variables remplies:")
    examples = [
        ("Cette nouvelle {technologie} pour {bénéfice}", 
         {"technologie": "panneau solaire", "bénéfice": "économiser 80% sur vos factures"}),
        ("Ce que {autorité} ne vous dit pas sur {sujet}", 
         {"autorité": "les fournisseurs d'énergie", "sujet": "l'énergie solaire"}),
        ("La méthode secrète des {experts} pour {résultat}", 
         {"experts": "installateurs solaires", "résultat": "réduire vos coûts"}),
        ("{Nombre} personnes ont déjà {action}", 
         {"Nombre": "50 000", "action": "installé des panneaux solaires"}),
        ("Offre limitée: {bénéfice} exclusif", 
         {"bénéfice": "installation gratuite"})
    ]
    
    for template, variables in examples:
        filled_template = template.format(**variables)
        print(f"   • {filled_template}")
    
    print(f"\n✅ Test terminé!")
    print(f"💡 Utilisez ces templates pour inspirer vos hooks marketing")

if __name__ == "__main__":
    main() 