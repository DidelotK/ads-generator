#!/usr/bin/env python3
"""
Script de test pour le générateur de hooks
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.generators.hook_generator import HookGenerator
from src.marketing_config import HookStyle

def test_hook_generation():
    """Test simple de génération de hooks"""
    generator = HookGenerator()
    hooks = generator.generate_hooks_simple(
        subject="Test de génération",
        num_hooks=1,
        style=HookStyle.ENGAGING.value,
        model="gpt-3.5-turbo"
    )
    assert hooks is not None and len(hooks) > 0, "Aucun hook généré"
    assert 'hook' in hooks[0] and 'description' in hooks[0], "Le hook généré n'a pas les bons champs"
    assert isinstance(hooks[0]['hook'], str) and isinstance(hooks[0]['description'], str), "Les champs ne sont pas des chaînes de caractères"

if __name__ == "__main__":
    test_hook_generation() 