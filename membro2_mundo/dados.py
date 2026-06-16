"""Membro 2 — Dados estilo RPG de mesa para mobilidade e luta.

O MVP usa dois testes simples inspirados em D&D:
- D20 de mobilidade: usado quando Henry e Mitis viajam ou avançam na dungeon.
- D20 de luta: usado em ataques físicos, magias ofensivas e golpes dos inimigos.

A ideia não é virar um sistema complexo de mesa, mas deixar o terminal com
sensação de RPG narrado: rolagem, sucesso, falha e crítico.
"""
from __future__ import annotations

from random import randint


def rolar_d20() -> int:
    """Rola um dado de 20 lados."""
    return randint(1, 20)


def aplicar_teste_mobilidade(estado: dict, origem: str, destino: str, dificuldade: int = 10) -> None:
    """Aplica um teste de mobilidade durante viagem/exploração.

    O deslocamento sempre acontece para não travar o MVP, mas a rolagem pode
    gerar bônus ou pequenos prejuízos narrativos.
    """
    nivel = estado.get("status", {}).get("nivel", 1)
    modificador = max(0, nivel // 2)
    rolagem = rolar_d20()
    total = rolagem + modificador

    print("\n=== TESTE DE MOBILIDADE ===")
    print(f"Rota: {origem} -> {destino}")
    print(f"D20: {rolagem} + modificador de nível {modificador} = {total}")
    print(f"Dificuldade: {dificuldade}")

    status = estado.setdefault("status", {})

    if rolagem == 20:
        bonus_moedas = 8 + nivel
        estado["moedas"] = estado.get("moedas", 0) + bonus_moedas
        status["mana"] = min(status.get("mana_max", 50), status.get("mana", 0) + 5)
        print(f"Crítico! Santiago encontra um atalho seguro. +{bonus_moedas} moedas e +5 mana.")
    elif rolagem == 1:
        dano = max(3, 5 + nivel)
        status["hp"] = max(1, status.get("hp", 1) - dano)
        print(f"Falha crítica! Raízes distorcidas ferem Henry. -{dano} HP.")
    elif total >= dificuldade + 5:
        status["mana"] = min(status.get("mana_max", 50), status.get("mana", 0) + 3)
        print("Sucesso alto! Mitis guia Henry por uma passagem mais leve. +3 mana.")
    elif total >= dificuldade:
        print("Sucesso. A viagem ocorreu sem problemas.")
    else:
        dano = max(2, dificuldade - total)
        status["hp"] = max(1, status.get("hp", 1) - dano)
        print(f"Falha parcial. O caminho estava instável. Henry perdeu {dano} HP, mas chegou ao destino.")


def aplicar_dado_luta(dano_base: int, atacante: str = "Atacante", minimo: int = 0) -> int:
    """Aplica o D20 de luta ao dano calculado.

    Faixas:
    - 1: falha crítica, dano 0.
    - 2 a 7: golpe fraco, 75% do dano.
    - 8 a 16: golpe normal.
    - 17 a 19: golpe forte, 125% do dano.
    - 20: crítico, 175% do dano + 2.
    """
    rolagem = rolar_d20()

    if rolagem == 1:
        print(f"{atacante} rolou D20 = 1. Falha crítica!")
        return 0
    if rolagem <= 7:
        dano = int(dano_base * 0.75)
        print(f"{atacante} rolou D20 = {rolagem}. Golpe fraco.")
        return max(minimo, dano)
    if rolagem <= 16:
        print(f"{atacante} rolou D20 = {rolagem}. Golpe normal.")
        return max(minimo, dano_base)
    if rolagem <= 19:
        dano = int(dano_base * 1.25)
        print(f"{atacante} rolou D20 = {rolagem}. Golpe forte!")
        return max(minimo, dano)

    dano = int(dano_base * 1.75) + 2
    print(f"{atacante} rolou D20 = 20. CRÍTICO!")
    return max(minimo, dano)
