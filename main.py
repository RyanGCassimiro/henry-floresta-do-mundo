"""Ponto de entrada do RPG de terminal.

Execute com:
    python main.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from game import iniciar_jogo

if __name__ == "__main__":
    iniciar_jogo()
