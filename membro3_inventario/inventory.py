"""Membro 3 — Estrutura de dados do inventário e operações principais."""
from __future__ import annotations


def criar_estado_inicial() -> dict:
    """Cria o estado inicial do jogador e do inventário."""
    return {
        "jogador": "Henry",
        "companheiro": "Mitis, o corujinha-buraqueira",
        "local_atual": "Vila das Preguiças",
        "moedas": 100,
        "status": {
            "nivel": 1,
            "exp": 0,
            "exp_proximo": 50,
            "hp_max": 100,
            "hp": 100,
            "mana_max": 50,
            "mana": 50,
            "ataque": 10,
            "defesa": 5,
            "magia": 8,
            "fire": 0,
            "blizzard": 0,
            "thunder": 0,
            "water": 0,
            "dark": 0,
            "quake": 0,
            "cure": 0,
            "esuna": 0,
            "haste": 0,
            "protect": 0,
            "shell": 0,
            "veneno": 0,
            "skill_points": 0,
        },
        "habilidades": {
            "fire": 0,
            "blizzard": 0,
            "thunder": 0,
            "water": 0,
            "dark": 0,
            "quake": 0,
            "cure": 0,
            "esuna": 0,
            "haste": 0,
            "protect": 0,
            "shell": 0,
            "mitis_penas": 0,
            "defesa": 0,
        },
        "inventario": [
            {
                "nome": "Poção Pequena de HP",
                "tipo": "consumivel",
                "raridade": "comum",
                "peso": 1,
                "valor_magico": 5,
                "preco": 15,
                "efeitos": {"hp": 30},
                "descricao": "Restaura 30 HP.",
            },
            {
                "nome": "Poção de Mana",
                "tipo": "consumivel",
                "raridade": "comum",
                "peso": 1,
                "valor_magico": 8,
                "preco": 18,
                "efeitos": {"mana": 25},
                "descricao": "Restaura 25 mana.",
            },
        ],
        "equipamentos": {
            "capa": None,
            "anel": None,
            "amuleto": None,
            "arma": None,
        },
        "itens_coletados": [],
        "criaturas_derrotadas": {},
        "efeitos_temporarios": {
            "haste": 0,
            "protect": 0,
            "shell": 0,
            "veneno": 0,
        },
        "quests_personagens": {},
        "rota_tsp_calculada": False,
        "navegador_santiago_ativo": False,
    }


def adicionar_item(estado: dict, item: dict) -> None:
    estado["inventario"].append(item)


def remover_item(estado: dict, nome: str) -> bool:
    nome_normalizado = nome.strip().lower()
    for i, item in enumerate(estado["inventario"]):
        if item["nome"].lower() == nome_normalizado:
            removido = estado["inventario"].pop(i)
            print(f"Item removido: {removido['nome']}")
            return True
    print("Item não encontrado.")
    return False


def remover_item_por_indice(estado: dict, indice: int) -> dict | None:
    if 0 <= indice < len(estado["inventario"]):
        return estado["inventario"].pop(indice)
    return None


def consultar_item(estado: dict, nome: str) -> dict | None:
    nome_normalizado = nome.strip().lower()
    for item in estado["inventario"]:
        if item["nome"].lower() == nome_normalizado:
            return item
    return None


def usar_consumivel(estado: dict, nome: str) -> bool:
    nome_normalizado = nome.strip().lower()
    for i, item in enumerate(estado["inventario"]):
        if item["nome"].lower() == nome_normalizado:
            if item.get("tipo") != "consumivel":
                print("Esse item não é consumível.")
                return False

            efeitos = item.get("efeitos", {})
            status = estado["status"]
            if "hp" in efeitos:
                # Mitis ajuda Henry a aproveitar melhor poções de cura.
                bonus_cura = estado["habilidades"].get("cure", 0) * 5
                status["hp"] = min(status["hp_max"], status["hp"] + efeitos["hp"] + bonus_cura)
                print(f"HP restaurado. HP atual: {status['hp']}/{status['hp_max']}")
            if "mana" in efeitos:
                status["mana"] = min(status["mana_max"], status["mana"] + efeitos["mana"])
                print(f"Mana restaurada. Mana atual: {status['mana']}/{status['mana_max']}")

            estado["inventario"].pop(i)
            print(f"Consumível usado: {item['nome']}")
            return True

    print("Consumível não encontrado.")
    return False


def equipar_item(estado: dict, nome: str) -> bool:
    nome_normalizado = nome.strip().lower()
    for i, item in enumerate(estado["inventario"]):
        if item["nome"].lower() == nome_normalizado:
            if item.get("tipo") != "equipamento":
                print("Esse item não é equipamento.")
                return False

            slot = item.get("slot")
            if slot not in estado["equipamentos"]:
                print("Slot de equipamento inválido.")
                return False

            antigo = estado["equipamentos"].get(slot)
            estado["equipamentos"][slot] = item
            estado["inventario"].pop(i)
            if antigo:
                estado["inventario"].append(antigo)
                print(f"{antigo['nome']} voltou para o inventário.")

            print(f"Equipado: {item['nome']} no slot {slot}.")
            return True

    print("Equipamento não encontrado.")
    return False
