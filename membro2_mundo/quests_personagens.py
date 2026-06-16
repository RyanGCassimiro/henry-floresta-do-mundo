"""Membro 2 — Quests dos personagens aliados.

Este módulo concentra as quests narrativas dos colegas/personagens do mundo.
Ele fica com o Membro 2 porque envolve locais, exploração, coleta, combate,
progressão, recompensas e integração com o mundo do RPG textual.
"""
from __future__ import annotations

from membro2_mundo.progressao import ganhar_exp
from membro3_inventario.inventory import adicionar_item, consultar_item, remover_item


QUESTS_PERSONAGENS = {
    "camila": {
        "personagem": "Camila",
        "especie": "tamanduá-bandeira",
        "titulo": "As Formigas Luminosas do Ipê",
        "local": "Bosque do Ipê",
        "descricao": (
            "Camila precisa de uma Flor de Ipê para acalmar as formigas luminosas "
            "que estão fugindo da seiva corrompida."
        ),
        "requisitos": {
            "local": "Bosque do Ipê",
            "itens": ["Flor de Ipê"],
        },
        "recompensa": {
            "exp": 25,
            "moedas": 20,
            "skill_points": 1,
            "item": {
                "nome": "Tônico da Camila",
                "tipo": "consumivel",
                "raridade": "incomum",
                "peso": 1,
                "valor_magico": 18,
                "preco": 35,
                "efeitos": {"hp": 45},
                "descricao": "Tônico preparado por Camila. Restaura 45 HP.",
            },
        },
    },
    "eduardo": {
        "personagem": "Eduardo",
        "especie": "jaguatirica",
        "titulo": "O Rastro da Pena Sombria",
        "local": "Ruínas da Arpia",
        "descricao": (
            "Eduardo encontrou marcas estranhas nas ruínas. Para concluir a investigação, "
            "Henry e Mitis precisam derrotar uma Pena Sombria."
        ),
        "requisitos": {
            "local": "Ruínas da Arpia",
            "criaturas": {"Pena Sombria": 1},
        },
        "recompensa": {
            "exp": 40,
            "moedas": 35,
            "skill_points": 1,
            "item": {
                "nome": "Talismã da Jaguatirica",
                "tipo": "equipamento",
                "slot": "amuleto",
                "raridade": "rara",
                "peso": 1,
                "valor_magico": 42,
                "preco": 85,
                "efeitos": {"ataque": 3, "thunder": 1},
                "descricao": "+3 ataque e +1 bônus de Thunder.",
            },
        },
    },
    "monique": {
        "personagem": "Monique",
        "especie": "tatu-bola",
        "titulo": "O Casco Contra os Golems",
        "local": "Caverna dos Golems",
        "descricao": (
            "Monique descobriu rachaduras antigas na caverna. Ela precisa que Henry "
            "derrote um Golem de Seiva para testar uma proteção de casco mágico."
        ),
        "requisitos": {
            "local": "Caverna dos Golems",
            "criaturas": {"Golem de Seiva": 1},
        },
        "recompensa": {
            "exp": 60,
            "moedas": 40,
            "skill_points": 1,
            "item": {
                "nome": "Casco Protetor da Monique",
                "tipo": "equipamento",
                "slot": "capa",
                "raridade": "rara",
                "peso": 2,
                "valor_magico": 45,
                "preco": 90,
                "efeitos": {"defesa": 4, "hp_max": 15},
                "descricao": "+4 defesa e +15 HP máximo.",
            },
        },
    },
    "pietra": {
        "personagem": "Pietra",
        "especie": "onça-pintada",
        "titulo": "O Juramento da Onça Guardiã",
        "local": "Clareira da Árvore do Mundo",
        "descricao": (
            "Pietra testa se Henry está pronto para proteger a floresta. "
            "Para provar sua evolução, Henry precisa estar pelo menos no nível 2."
        ),
        "requisitos": {
            "local": "Clareira da Árvore do Mundo",
            "nivel_minimo": 2,
        },
        "recompensa": {
            "exp": 50,
            "moedas": 45,
            "skill_points": 2,
            "item": {
                "nome": "Medalhão da Pietra",
                "tipo": "equipamento",
                "slot": "amuleto",
                "raridade": "epica",
                "peso": 1,
                "valor_magico": 70,
                "preco": 130,
                "efeitos": {"ataque": 3, "defesa": 3},
                "descricao": "+3 ataque e +3 defesa.",
            },
        },
    },
    "santiago": {
        "personagem": "Santiago",
        "especie": "tucano",
        "titulo": "As Cartas de Voo do Navegador",
        "local": "Vila das Preguiças",
        "descricao": (
            "Santiago é um tucano navegador. Ele ajuda Henry e Mitis a interpretar "
            "as rotas do mapa mágico. Para concluir a quest, calcule a rota principal com TSP."
        ),
        "requisitos": {
            "local": "Vila das Preguiças",
            "tsp_calculado": True,
        },
        "recompensa": {
            "exp": 30,
            "moedas": 30,
            "skill_points": 1,
            "flag": "navegador_santiago_ativo",
            "item": {
                "nome": "Mapa de Navegação do Santiago",
                "tipo": "chave",
                "raridade": "rara",
                "peso": 1,
                "valor_magico": 40,
                "preco": 0,
                "efeitos": {},
                "descricao": "Mapa do tucano navegador. Marca rotas seguras entre os portais.",
            },
        },
    },
}


def garantir_estado_quests(estado: dict) -> None:
    """Garante que o save antigo também tenha campos de quests."""
    estado.setdefault("quests_personagens", {})
    estado.setdefault("criaturas_derrotadas", {})
    estado.setdefault("rota_tsp_calculada", False)
    estado.setdefault("navegador_santiago_ativo", False)

    for quest_id in QUESTS_PERSONAGENS:
        estado["quests_personagens"].setdefault(quest_id, "pendente")


def listar_quests_personagens(estado: dict) -> None:
    garantir_estado_quests(estado)
    print("\n=== QUESTS DOS ALIADOS ===")
    for i, (quest_id, quest) in enumerate(QUESTS_PERSONAGENS.items(), start=1):
        status = estado["quests_personagens"].get(quest_id, "pendente")
        print(f"{i} - {quest['personagem']} ({quest['especie']}) | {quest['titulo']} | {status}")


def _tem_itens(estado: dict, nomes_itens: list[str]) -> bool:
    return all(consultar_item(estado, nome) is not None for nome in nomes_itens)


def _tem_criaturas_derrotadas(estado: dict, criaturas: dict[str, int]) -> bool:
    derrotadas = estado.get("criaturas_derrotadas", {})
    return all(derrotadas.get(nome, 0) >= quantidade for nome, quantidade in criaturas.items())


def _validar_requisitos(estado: dict, quest: dict) -> tuple[bool, str]:
    requisitos = quest["requisitos"]

    local_necessario = requisitos.get("local")
    if local_necessario and estado.get("local_atual") != local_necessario:
        return False, f"Vá para {local_necessario} para concluir esta quest."

    itens = requisitos.get("itens", [])
    if itens and not _tem_itens(estado, itens):
        return False, "Você ainda não possui os itens necessários: " + ", ".join(itens)

    criaturas = requisitos.get("criaturas", {})
    if criaturas and not _tem_criaturas_derrotadas(estado, criaturas):
        pendentes = [f"{nome} x{qtd}" for nome, qtd in criaturas.items()]
        return False, "Derrote as criaturas necessárias: " + ", ".join(pendentes)

    nivel_minimo = requisitos.get("nivel_minimo")
    if nivel_minimo and estado["status"]["nivel"] < nivel_minimo:
        return False, f"Henry precisa estar no nível {nivel_minimo} ou maior."

    if requisitos.get("tsp_calculado") and not estado.get("rota_tsp_calculada"):
        return False, "Calcule a rota principal com TSP antes de falar com Santiago."

    return True, "Requisitos cumpridos."


def _aplicar_recompensa(estado: dict, quest: dict) -> None:
    recompensa = quest["recompensa"]

    # Remove itens entregues, quando a quest pedir item.
    for nome_item in quest["requisitos"].get("itens", []):
        remover_item(estado, nome_item)

    moedas = recompensa.get("moedas", 0)
    if moedas:
        estado["moedas"] += moedas
        print(f"+{moedas} moedas")

    skill_points = recompensa.get("skill_points", 0)
    if skill_points:
        estado["status"]["skill_points"] += skill_points
        print(f"+{skill_points} ponto(s) de habilidade")

    item = recompensa.get("item")
    if item:
        adicionar_item(estado, item.copy())
        print(f"Item recebido: {item['nome']}")

    flag = recompensa.get("flag")
    if flag:
        estado[flag] = True
        print("Santiago agora está disponível como navegador do grupo.")

    exp = recompensa.get("exp", 0)
    if exp:
        ganhar_exp(estado, exp)


def abrir_quests_personagens(estado: dict) -> None:
    garantir_estado_quests(estado)

    while True:
        listar_quests_personagens(estado)
        print("0 - Voltar")
        escolha = input("Escolha uma quest para ver/concluir: ").strip()

        if escolha == "0":
            return

        try:
            indice = int(escolha) - 1
            quest_id = list(QUESTS_PERSONAGENS.keys())[indice]
        except (ValueError, IndexError):
            print("Opção inválida.")
            continue

        quest = QUESTS_PERSONAGENS[quest_id]
        status = estado["quests_personagens"].get(quest_id, "pendente")

        print(f"\n=== {quest['titulo']} ===")
        print(f"Personagem: {quest['personagem']} — {quest['especie']}")
        print(f"Local: {quest['local']}")
        print(quest["descricao"])
        print(f"Status: {status}")

        if status == "concluida":
            print("Essa quest já foi concluída.")
            continue

        pode_concluir, mensagem = _validar_requisitos(estado, quest)
        print(mensagem)
        if not pode_concluir:
            continue

        confirmar = input("Concluir quest agora? (s/n): ").strip().lower()
        if confirmar != "s":
            continue

        estado["quests_personagens"][quest_id] = "concluida"
        print(f"Quest concluída: {quest['titulo']}")
        _aplicar_recompensa(estado, quest)
