"""Membro 2 — Dungeon dinâmica: Floresta Distorcida.

A Floresta Distorcida é uma dungeon paralela/textual que muda a cada entrada.
Ela resolve o balanceamento dos mobs porque cada criatura é gerada com base em:
- nível atual do Henry;
- profundidade/andar da exploração;
- arquétipo do monstro sorteado;
- modificador elemental do trecho da floresta.

Assim, os inimigos acompanham o jogador sem precisar criar manualmente
uma tabela enorme de HP/ataque para cada nível.
"""
from __future__ import annotations

from random import choice, randint, random
from typing import Callable

from membro2_mundo.combate import iniciar_combate_contra
from membro2_mundo.progressao import calcular_status_total, garantir_estado_magias
from membro3_inventario.inventory import adicionar_item
from membro2_mundo.dados import aplicar_teste_mobilidade
from random import choice, randint, random
from typing import Callable

from membro2_mundo.combate import iniciar_combate_contra
from membro2_mundo.progressao import calcular_status_total, garantir_estado_magias
from membro3_inventario.inventory import adicionar_item
from membro2_mundo.dados import aplicar_teste_mobilidade
from membro2_mundo.dialogos_henry_mitis import dialogo_perola_furta_cor

TRECHOS_DISTORCIDOS = [
    {
        "nome": "Bosque Espelhado",
        "descricao": "as árvores parecem repetir os passos de Henry e Mitis.",
        "elemento": "blizzard",
        "fraqueza_extra": "fire",
    },
    {
        "nome": "Pântano de Seiva Negra",
        "descricao": "a seiva escura borbulha como se respirasse.",
        "elemento": "dark",
        "fraqueza_extra": "water",
    },
    {
        "nome": "Caminho dos Trovões Baixos",
        "descricao": "pequenos raios correm pelo chão antes de sumirem nas raízes.",
        "elemento": "thunder",
        "fraqueza_extra": "quake",
    },
    {
        "nome": "Raiz Invertida",
        "descricao": "raízes crescem para cima como arcos vivos.",
        "elemento": "quake",
        "fraqueza_extra": "blizzard",
    },
    {
        "nome": "Clareira de Névoa Azul",
        "descricao": "a névoa muda os sons de lugar e confunde a direção.",
        "elemento": "water",
        "fraqueza_extra": "thunder",
        "aquatico": True,
    },
    {
        "nome": "Lago Suspenso Furta-cor",
        "descricao": "um lago impossível flutua entre raízes, refletindo cores que não ficam paradas.",
        "elemento": "water",
        "fraqueza_extra": "thunder",
        "aquatico": True,
        "raro": True,
    },
]


ARQUETIPOS_MOBS = [
    {
        "nome_base": "Lodo Distorcido",
        "hp_base": 24,
        "hp_por_nivel": 8,
        "ataque_base": 4,
        "ataque_por_nivel": 1.6,
        "defesa_base": 1,
        "defesa_por_nivel": 0.35,
        "fraquezas": ["thunder"],
        "resistencias": ["water"],
        "tipo_dano": "fisico",
        "exp_base": 16,
        "moedas_base": 12,
    },
    {
        "nome_base": "Golem de Cipó",
        "hp_base": 34,
        "hp_por_nivel": 10,
        "ataque_base": 5,
        "ataque_por_nivel": 1.8,
        "defesa_base": 2,
        "defesa_por_nivel": 0.55,
        "fraquezas": ["fire", "blizzard"],
        "resistencias": ["quake", "dark"],
        "tipo_dano": "fisico",
        "exp_base": 22,
        "moedas_base": 16,
    },
    {
        "nome_base": "Sombra da Arpia",
        "hp_base": 28,
        "hp_por_nivel": 9,
        "ataque_base": 6,
        "ataque_por_nivel": 2.0,
        "defesa_base": 1,
        "defesa_por_nivel": 0.45,
        "fraquezas": ["blizzard"],
        "resistencias": ["dark", "fire"],
        "tipo_dano": "magico",
        "exp_base": 24,
        "moedas_base": 18,
    },
    {
        "nome_base": "Raiz Faminta",
        "hp_base": 30,
        "hp_por_nivel": 9,
        "ataque_base": 5,
        "ataque_por_nivel": 1.7,
        "defesa_base": 2,
        "defesa_por_nivel": 0.4,
        "fraquezas": ["fire"],
        "resistencias": ["water"],
        "tipo_dano": "fisico",
        "exp_base": 20,
        "moedas_base": 14,
        "aplica_veneno": True,
    },
    {
        "nome_base": "Eco de Seiva",
        "hp_base": 26,
        "hp_por_nivel": 8,
        "ataque_base": 7,
        "ataque_por_nivel": 1.9,
        "defesa_base": 1,
        "defesa_por_nivel": 0.3,
        "fraquezas": ["dark", "quake"],
        "resistencias": ["thunder"],
        "tipo_dano": "magico",
        "exp_base": 23,
        "moedas_base": 17,
    },
]



PEROLA_FURTA_COR = {
    "nome": "Pérola Furta-cor",
    "tipo": "chave",
    "raridade": "lendaria",
    "peso": 1,
    "valor_magico": 120,
    "preco": 0,
    "efeitos": {},
    "descricao": "Cristalização da Canção das Águas. Mantém a pureza das águas doces.",
}

RECOMPENSAS_DUNGEON = [
    {
        "nome": "Poção Média de HP",
        "tipo": "consumivel",
        "raridade": "incomum",
        "peso": 1,
        "valor_magico": 12,
        "preco": 35,
        "efeitos": {"hp": 55},
        "descricao": "Restaura 55 HP. Encontrada em trechos instáveis da floresta.",
    },
    {
        "nome": "Éter de Seiva",
        "tipo": "consumivel",
        "raridade": "incomum",
        "peso": 1,
        "valor_magico": 16,
        "preco": 40,
        "efeitos": {"mana": 45},
        "descricao": "Restaura 45 mana do grupo.",
    },
    {
        "nome": "Anel de Raiz Viva",
        "tipo": "equipamento",
        "slot": "anel",
        "raridade": "rara",
        "peso": 1,
        "valor_magico": 35,
        "preco": 90,
        "efeitos": {"hp_max": 18, "defesa": 1},
        "descricao": "+18 HP máximo e +1 defesa.",
    },
    {
        "nome": "Amuleto da Névoa Azul",
        "tipo": "equipamento",
        "slot": "amuleto",
        "raridade": "rara",
        "peso": 1,
        "valor_magico": 38,
        "preco": 95,
        "efeitos": {"mana_max": 25, "water": 1},
        "descricao": "+25 mana máxima e +1 bônus de Water.",
    },
]

RECOMPENSAS_DUNGEON.extend([
    {
        "nome": "Semente de Guaraná",
        "tipo": "consumivel",
        "raridade": "incomum",
        "peso": 1,
        "valor_magico": 18,
        "preco": 35,
        "efeitos": {"regen_hp": 10, "regen_mana": 5, "duracao_turnos": 4},
        "descricao": "Regenera 10 HP e 5 mana por turno durante 4 turnos.",
    },
    {
        "nome": "Pedra Fluorescente Grande",
        "tipo": "material",
        "raridade": "rara",
        "peso": 2,
        "valor_magico": 35,
        "preco": 45,
        "efeitos": {},
        "descricao": "Cristal raro gerado pela Floresta Distorcida.",
    },
])


def garantir_estado_dungeon(estado: dict) -> None:
    """Cria os campos de controle da dungeon caso ainda não existam."""
    estado.setdefault("floresta_distorcida", {})
    estado["floresta_distorcida"].setdefault("entradas", 0)
    estado["floresta_distorcida"].setdefault("maior_profundidade", 0)
    estado["floresta_distorcida"].setdefault("mobs_derrotados", 0)
    estado["floresta_distorcida"].setdefault("perola_furta_cor_encontrada", False)


def calcular_nivel_mob(estado: dict, profundidade: int) -> int:
    """Escala o mob com o nível do player e com a profundidade da dungeon."""
    nivel_henry = estado.get("status", {}).get("nivel", 1)
    variacao = randint(-1, 1)
    nivel_mob = nivel_henry + ((profundidade - 1) // 2) + variacao
    return max(1, nivel_mob)




def escolher_trecho_distorcido(profundidade: int) -> dict:
    """Escolhe um trecho da Floresta Distorcida.

    Trechos raros possuem baixa chance de aparecer. Isso permite que a Pérola
    Furta-cor da quest da Beatriz surja apenas em mapas aquáticos e com baixa
    probabilidade nos dados.
    """
    trechos_comuns = [trecho for trecho in TRECHOS_DISTORCIDOS if not trecho.get("raro")]
    trechos_raros = [trecho for trecho in TRECHOS_DISTORCIDOS if trecho.get("raro")]

    # Chance baixa: começa em 5% e sobe pouco com a profundidade, limitada a 12%.
    chance_rara = min(0.12, 0.05 + (profundidade * 0.005))

    if trechos_raros and random() < chance_rara:
        return choice(trechos_raros)

    return choice(trechos_comuns)


def gerar_criatura_distorcida(estado: dict, profundidade: int) -> dict:
    """Gera uma criatura nova a cada sala.

    O resultado usa o mesmo contrato de dados dos inimigos normais do jogo,
    então pode ser enviado diretamente para o sistema de combate.
    """
    trecho = escolher_trecho_distorcido(profundidade)
    base = choice(ARQUETIPOS_MOBS)
    nivel_mob = calcular_nivel_mob(estado, profundidade)

    hp = int(base["hp_base"] + (base["hp_por_nivel"] * nivel_mob) + (profundidade * 3))
    ataque = int(base["ataque_base"] + (base["ataque_por_nivel"] * nivel_mob) + (profundidade * 0.6))
    defesa = int(base["defesa_base"] + (base["defesa_por_nivel"] * nivel_mob) + (profundidade * 0.25))
    exp = int(base["exp_base"] + (nivel_mob * 11) + (profundidade * 4))
    moedas = int(base["moedas_base"] + (nivel_mob * 7) + (profundidade * 3))

    fraquezas = list(dict.fromkeys(base.get("fraquezas", []) + [trecho["fraqueza_extra"]]))
    resistencias = [r for r in base.get("resistencias", []) if r not in fraquezas]

    criatura = {
        "nome": f"{base['nome_base']} Nv.{nivel_mob}",
        "hp": hp,
        "ataque": ataque,
        "defesa": defesa,
        "exp": exp,
        "moedas": moedas,
        "fraquezas": fraquezas,
        "resistencias": resistencias,
        "tipo_dano": base.get("tipo_dano", "fisico"),
        "aplica_veneno": base.get("aplica_veneno", False) or trecho["elemento"] == "dark",
        "trecho": trecho["nome"],
        "elemento_distorcido": trecho["elemento"],
        "descricao_trecho": trecho["descricao"],
        "trecho_aquatico": trecho.get("aquatico", False),
        "trecho_raro": trecho.get("raro", False),
    }
    return criatura


def _curar_ao_sair(estado: dict) -> None:
    """Pequena recuperação para a dungeon não travar o jogo no MVP."""
    status_total = calcular_status_total(estado)
    estado["status"]["hp"] = max(1, min(status_total["hp_max"], estado["status"].get("hp", 1)))
    estado["status"]["mana"] = max(0, min(status_total["mana_max"], estado["status"].get("mana", 0)))




def _tentar_recompensa_beatriz(estado: dict, criatura: dict, profundidade: int) -> bool:
    """Tenta entregar a Pérola Furta-cor em uma sala aquática rara.

    A chance é baixa e depende do trecho da dungeon:
    - só funciona em trecho aquático;
    - aumenta levemente com a profundidade;
    - só entrega uma vez por jogo.
    """
    dungeon = estado.get("floresta_distorcida", {})
    if dungeon.get("perola_furta_cor_encontrada"):
        return False

    if not criatura.get("trecho_aquatico"):
        return False

    # Chance baixa: 8% + 1% por profundidade, com limite de 18%.
    chance = min(0.18, 0.08 + (profundidade * 0.01))

    # Se o trecho for o Lago Suspenso Furta-cor, a chance é melhor,
    # mas o próprio mapa já tem baixa chance de aparecer.
    if criatura.get("trecho_raro"):
        chance = max(chance, 0.35)

    if random() > chance:
        return False

    adicionar_item(estado, PEROLA_FURTA_COR.copy())
    estado["floresta_distorcida"]["perola_furta_cor_encontrada"] = True

    dialogo_perola_furta_cor()

    print("\nA água distorcida canta baixinho entre as raízes.")
    print("Henry encontrou a Pérola Furta-cor — a Canção das Águas cristalizada.")
    print("Beatriz precisa desse item para proteger os animais aquáticos de água doce.")
    return True


def _premio_pos_sala(estado: dict, profundidade: int) -> None:
    """Chance simples de recompensa adicional após uma sala vencida."""
    # Quanto mais fundo, maior a chance de ganhar item.
    chance = min(0.45, 0.18 + (profundidade * 0.03))
    if random() > chance:
        return

    item = choice(RECOMPENSAS_DUNGEON).copy()
    adicionar_item(estado, item)
    print(f"\nA floresta deixou uma recompensa para trás: {item['nome']}.")


def explorar_floresta_distorcida(estado: dict) -> None:
    """Loop principal da dungeon dinâmica.

    O jogador entra, enfrenta salas que mudam e pode sair depois de cada vitória.
    Mobs acompanham o nível de Henry, então a dungeon continua útil no começo
    e depois que o personagem sobe de nível.
    """
    garantir_estado_magias(estado)
    garantir_estado_dungeon(estado)

    estado["floresta_distorcida"]["entradas"] += 1
    profundidade = 1

    print("\n=== FLORESTA DISTORCIDA ===")
    print("Henry e Mitis atravessam uma fenda lilás aberta pelas preguiças guardiãs.")
    print("Este lugar muda a cada entrada. Os caminhos e os mobs escalam com o nível de Henry.")

    while estado["status"].get("hp", 0) > 0:
        criatura = gerar_criatura_distorcida(estado, profundidade)
        estado["floresta_distorcida"]["maior_profundidade"] = max(
            estado["floresta_distorcida"]["maior_profundidade"], profundidade
        )

        print("\n" + "=" * 56)
        print(f"FLORESTA DISTORCIDA — SALA {profundidade:02d}".center(56))
        print("=" * 56)
        print(f"Trecho: {criatura['trecho']}")
        if criatura.get("trecho_aquatico"):
            print("Tipo de trecho: aquático")
        if criatura.get("trecho_raro"):
            print("Raridade do trecho: raro")
        print(f"Descrição: {criatura['descricao_trecho']}")
        print("A distorção muda o padrão dos monstros deste trecho.")
        print("-" * 56)
        print("PRÓXIMO ENCONTRO")
        print(f"Inimigo:     {criatura['nome']}")
        print(f"HP:          {criatura['hp']}")
        print(f"ATQ/DEF:     {criatura['ataque']} / {criatura['defesa']}")
        print(f"Fraquezas:   {', '.join(criatura['fraquezas'])}")
        print(f"Resistência: {', '.join(criatura.get('resistencias', [])) or 'nenhuma'}")
        print("=" * 56)

        venceu = iniciar_combate_contra(estado, criatura, contexto=f"Floresta Distorcida — Sala {profundidade:02d}")

        if estado["status"].get("hp", 0) <= 0:
            print("\nA Floresta Distorcida expulsou Henry e Mitis de volta para a Vila das Preguiças.")
            _curar_ao_sair(estado)
            return

        if not venceu:
            print("\nHenry e Mitis escaparam antes de dominar a sala. Nenhuma recompensa da dungeon foi entregue.")
            _curar_ao_sair(estado)
            return

        estado["floresta_distorcida"]["mobs_derrotados"] += 1
        _tentar_recompensa_beatriz(estado, criatura, profundidade)
        _premio_pos_sala(estado, profundidade)

        print("\nA trilha se reorganiza diante de Henry.")
        print("1 - Continuar mais fundo")
        print("2 - Sair da Floresta Distorcida")
        escolha = input("Escolha: ").strip()
        if escolha != "1":
            print("Henry e Mitis retornaram pelo portal antes que a floresta mudasse de novo.")
            _curar_ao_sair(estado)
            return

        aplicar_teste_mobilidade(estado, "Profundidade " + str(profundidade), "Profundidade " + str(profundidade + 1), 10 + profundidade)
        profundidade += 1
