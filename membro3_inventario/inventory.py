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
            {
                "nome": "Semente de Guaraná",
                "tipo": "consumivel",
                "raridade": "incomum",
                "peso": 1,
                "valor_magico": 18,
                "preco": 35,
                "efeitos": {"regen_hp": 10, "regen_mana": 5, "duracao_turnos": 4},
                "descricao": "Regenera 10 HP e 5 mana por turno durante 4 turnos (12s narrativos).",
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
            "guarana_turnos": 0,
            "guarana_hp": 0,
            "guarana_mana": 0,
        },
        "quests_personagens": {},
        "rota_tsp_calculada": False,
        "navegador_santiago_ativo": False,
    }


def adicionar_item(estado: dict, item: dict) -> None:
    estado["inventario"].append(item)


def _valor_maximo_com_equipamentos(estado: dict, atributo: str) -> int:
    """Calcula hp_max/mana_max considerando equipamentos equipados.

    Mantemos esta função aqui para o inventário não depender do módulo de
    progressão da Pessoa 2. Assim poções podem respeitar anéis/amuleto/itens
    equipados sem criar importação circular.
    """
    total = estado["status"].get(atributo, 0)
    for item in estado.get("equipamentos", {}).values():
        if not item:
            continue
        total += item.get("efeitos", {}).get(atributo, 0)
    return total


def listar_consumiveis_no_inventario(estado: dict) -> list[tuple[int, dict]]:
    """Retorna consumíveis disponíveis como pares (indice_real, item)."""
    return [
        (indice, item)
        for indice, item in enumerate(estado["inventario"])
        if item.get("tipo") == "consumivel"
    ]


def consultar_item_por_indice(estado: dict, indice_inventario: int) -> dict | None:
    """Consulta um item pelo índice real no inventário."""
    if 0 <= indice_inventario < len(estado["inventario"]):
        return estado["inventario"][indice_inventario]
    return None


def usar_consumivel_por_indice(estado: dict, indice_inventario: int) -> bool:
    """Usa um consumível pelo índice real dentro do inventário.

    Esta é a versão preferida para o terminal, porque evita obrigar o jogador
    a digitar o nome exato da poção.
    """
    if not 0 <= indice_inventario < len(estado["inventario"]):
        print("Índice de consumível inválido.")
        return False

    item = estado["inventario"][indice_inventario]
    if item.get("tipo") != "consumivel":
        print("Esse item não é consumível.")
        return False

    efeitos = item.get("efeitos", {})
    status = estado["status"]
    if "hp" in efeitos:
        bonus_cura = estado.get("habilidades", {}).get("cure", 0) * 5
        hp_max_total = _valor_maximo_com_equipamentos(estado, "hp_max")
        status["hp"] = min(hp_max_total, status["hp"] + efeitos["hp"] + bonus_cura)
        print(f"HP restaurado. HP atual: {status['hp']}/{hp_max_total}")
    if "mana" in efeitos:
        mana_max_total = _valor_maximo_com_equipamentos(estado, "mana_max")
        status["mana"] = min(mana_max_total, status["mana"] + efeitos["mana"])
        print(f"Mana restaurada. Mana atual: {status['mana']}/{mana_max_total}")

    if "regen_hp" in efeitos or "regen_mana" in efeitos:
        temporarios = estado.setdefault("efeitos_temporarios", {})
        duracao = int(efeitos.get("duracao_turnos", 4))
        temporarios["guarana_turnos"] = max(temporarios.get("guarana_turnos", 0), duracao)
        temporarios["guarana_hp"] = int(efeitos.get("regen_hp", 0))
        temporarios["guarana_mana"] = int(efeitos.get("regen_mana", 0))
        print(
            "Efeito de regeneração ativado: "
            f"+{temporarios['guarana_hp']} HP e +{temporarios['guarana_mana']} mana "
            f"por turno durante {temporarios['guarana_turnos']} turno(s)."
        )

    estado["inventario"].pop(indice_inventario)
    print(f"Consumível usado: {item['nome']}")
    return True


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
    """Usa consumível pelo nome.

    Mantido por compatibilidade com testes/fluxos antigos, mas no jogo o menu
    principal agora usa `usar_consumivel_por_indice`.
    """
    nome_normalizado = nome.strip().lower()
    for i, item in enumerate(estado["inventario"]):
        if item["nome"].lower() == nome_normalizado:
            return usar_consumivel_por_indice(estado, i)

    print("Consumível não encontrado.")
    return False

def listar_equipamentos_no_inventario(estado: dict) -> list[tuple[int, dict]]:
    """Retorna equipamentos disponíveis como pares (indice_real, item).

    O indice_real é o índice do item dentro de estado["inventario"].
    Assim a interface pode mostrar uma lista numerada só com equipamentos,
    mas ainda equipar o item correto dentro do inventário completo.
    """
    return [
        (indice, item)
        for indice, item in enumerate(estado["inventario"])
        if item.get("tipo") == "equipamento"
    ]


def equipar_item_por_indice(estado: dict, indice_inventario: int) -> bool:
    """Equipa um item pelo índice real dentro do inventário.

    Evita pedir o nome exato do equipamento no terminal.
    """
    if not 0 <= indice_inventario < len(estado["inventario"]):
        print("Índice de equipamento inválido.")
        return False

    item = estado["inventario"][indice_inventario]
    if item.get("tipo") != "equipamento":
        print("Esse item não é equipamento.")
        return False

    slot = item.get("slot")
    if slot not in estado["equipamentos"]:
        print("Slot de equipamento inválido.")
        return False

    antigo = estado["equipamentos"].get(slot)
    estado["equipamentos"][slot] = item
    estado["inventario"].pop(indice_inventario)

    if antigo:
        estado["inventario"].append(antigo)
        print(f"{antigo['nome']} voltou para o inventário.")

    print(f"Equipado: {item['nome']} no slot {slot}.")
    return True


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
