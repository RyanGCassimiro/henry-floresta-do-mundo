"""Membro 3 — Salvamento e carregamento em JSON."""
from __future__ import annotations

import json
from pathlib import Path

SAVE_PATH = Path("save.json")


def salvar_jogo(estado: dict, caminho: Path = SAVE_PATH) -> None:
    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(estado, arquivo, ensure_ascii=False, indent=2)
    print(f"Jogo salvo em {caminho}.")


def carregar_jogo(caminho: Path = SAVE_PATH) -> dict | None:
    if not caminho.exists():
        print("Nenhum save encontrado.")
        return None

    with caminho.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)
