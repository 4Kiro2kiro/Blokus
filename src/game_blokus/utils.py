import os

def clear_screen():
    """Nettoie l'écran de manière cross-platform"""
    os.system('cls' if os.name == 'nt' else 'clear')
