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
from membro2_mundo.dados import aplicar_teste_mobilidade, rolar_d20
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

def evento_pedra_estranha(estado: dict) -> None:
    print("\nHenry e Mitis encontram um beco sem saída.")
    print("Há um desenho estranho gravado na pedra.")
    print("\n1 - Examinar o desenho")
    print("2 - Dar meia-volta")

    escolha = input("Escolha: ").strip()

    if escolha != "1":
        print("\nHenry decide não mexer na pedra.")
        print("Mitis observa o símbolo desaparecer atrás da névoa.")
        return

    rolagem = rolar_d20()
    print(f"\nRolagem de investigação: D20 = {rolagem}")

    if rolagem == 20:
        item = {
            "nome": "Fragmento de Seiva Antiga",
            "tipo": "material",
            "raridade": "raro",
            "peso": 1,
            "valor_magico": 40,
            "preco": 80,
            "descricao": "Um fragmento antigo escondido em uma pedra marcada por símbolos da Árvore do Mundo.",
        }

        print("\nSucesso crítico!")
        print("A pedra se abre e revela um item raro.")
        adicionar_item(estado, item)

    elif rolagem >= 16:
        item = {
            "nome": "Fragmento de Seiva",
            "tipo": "material",
            "raridade": "incomum",
            "peso": 1,
            "valor_magico": 20,
            "preco": 40,
            "descricao": "Um pequeno fragmento de seiva mágica encontrado na Floresta Distorcida.",
        }

        print("\nSucesso!")
        print("Henry encontra um fragmento escondido.")
        adicionar_item(estado, item)

    elif rolagem >= 10:
        print("\nSucesso parcial.")
        print("Henry encontra algumas moedas antigas.")
        estado["moedas"] = estado.get("moedas", 0) + 10

    else:
        print("\nFalha!")
        print("A pedra libera uma poeira mágica instável.")
        estado["status"]["hp"] = max(1, estado["status"].get("hp", 1) - 5)


def evento_voz_distorcida(estado: dict) -> None:
    """Evento narrativo opcional da Floresta Distorcida."""
    print("\nO ar fica mais frio por alguns segundos.")
    print("Mitis vira a cabeça de repente, como se tivesse ouvido algo entre as árvores.")
    print('Mitis: "Henry... você está escutando essa voz?"')
    print('Henry: "Que voz?"')
    print("A floresta fica em silêncio. Então, uma voz distante sussurra algo que nenhum dos dois entende.")

    print("\nDeseja seguir a voz?")
    print("1 - Seguir a voz")
    print("2 - Ignorar e continuar pelo caminho")

    escolha = input("Escolha: ").strip()

    if escolha != "1":
        print("\nHenry respira fundo e decide não seguir o som.")
        print("Mitis continua olhando para trás por alguns segundos.")
        print('Mitis: "Talvez tenha sido melhor assim..."')
        return

    rolagem = rolar_d20()
    print(f"\nRolagem de percepção: D20 = {rolagem}")

    if rolagem == 20:
        item = {
            "nome": "Eco Cristalizado",
            "tipo": "material",
            "raridade": "raro",
            "peso": 1,
            "valor_magico": 50,
            "preco": 100,
            "descricao": "Um fragmento de voz cristalizada encontrado na Floresta Distorcida.",
        }

        print("\nSucesso crítico!")
        print("A voz guia Henry e Mitis até uma clareira escondida.")
        print("No centro dela, um pequeno cristal vibra como se guardasse uma memória antiga.")
        adicionar_item(estado, item)

    elif rolagem >= 16:
        item = {
            "nome": "Pó de Memória da Floresta",
            "tipo": "material",
            "raridade": "incomum",
            "peso": 1,
            "valor_magico": 30,
            "preco": 60,
            "descricao": "Um pó mágico deixado por ecos antigos da Floresta Distorcida.",
        }

        print("\nSucesso!")
        print("Mitis consegue distinguir a direção da voz.")
        print("Henry encontra vestígios mágicos presos às raízes.")
        adicionar_item(estado, item)

    elif rolagem >= 10:
        mana = 5
        print("\nSucesso parcial.")
        print("A voz desaparece antes que Henry descubra sua origem.")
        print("Mesmo assim, a magia do lugar restaura um pouco da mana do grupo.")
        estado["status"]["mana"] = min(
            estado["status"].get("mana_max", 50),
            estado["status"].get("mana", 0) + mana,
        )
        print(f"Henry recuperou {mana} de mana.")

    else:
        dano = 5
        print("\nFalha!")
        print("A voz se multiplica em várias direções.")
        print("Henry sente uma pressão estranha na cabeça.")
        print("A Floresta Distorcida confundiu o grupo.")
        estado["status"]["hp"] = max(1, estado["status"].get("hp", 1) - dano)
        print(f"Henry perdeu {dano} HP.")


def evento_chao_desaparece(estado: dict, profundidade: int) -> int | None:
    """Evento narrativo da Floresta Distorcida.

    Retorna None para continuar a sala normalmente, ou uma nova profundidade
    quando a floresta joga Henry e Mitis de volta ao início.
    """
    print("\nA trilha parece firme por alguns segundos.")
    print("Henry dá mais um passo floresta adentro.")
    print("Então, sem aviso, o chão desaparece sob suas patas.")
    print('Henry: "Mitis!"')
    print("Mitis mergulha no ar tentando segurar Henry com as garras.")

    rolagem = rolar_d20()
    print(f"\nRolagem de reflexo: D20 = {rolagem}")

    if rolagem == 20:
        item = {
            "nome": "Lasca de Raiz Suspensa",
            "tipo": "material",
            "raridade": "raro",
            "peso": 1,
            "valor_magico": 55,
            "preco": 110,
            "descricao": "Uma lasca de raiz que flutuava no vazio da Floresta Distorcida.",
        }

        print("\nSucesso crítico!")
        print("Mitis segura Henry no último instante.")
        print("Ao se puxarem de volta, os dois encontram uma raiz brilhando sobre o abismo.")
        adicionar_item(estado, item)
        return None

    if rolagem >= 16:
        print("\nSucesso!")
        print("Mitis consegue segurar Henry antes que ele caia completamente.")
        print("Os dois voltam para a trilha, assustados, mas ilesos.")
        return None

    if rolagem >= 10:
        dano = 8
        mana_perdida = 5

        print("\nSucesso parcial!")
        print("Mitis segura Henry por alguns segundos, mas a floresta dobra o caminho ao redor deles.")
        print("Quando conseguem escapar, percebem que foram jogados de volta ao início da dungeon.")
        print("A separação momentânea deixou o grupo exausto.")

        estado["status"]["hp"] = max(1, estado["status"].get("hp", 1) - dano)
        estado["status"]["mana"] = max(0, estado["status"].get("mana", 0) - mana_perdida)

        print(f"Henry perdeu {dano} HP.")
        print(f"O grupo perdeu {mana_perdida} de mana.")
        return 1

    dano = 15

    print("\nFalha!")
    print("Mitis tenta alcançar Henry, mas a própria floresta separa os dois no ar.")
    print("Por alguns instantes, Henry cai sozinho em um vazio cheio de raízes e ecos.")
    print("Quando abre os olhos, está novamente no início da Floresta Distorcida.")
    print("Mitis aparece logo depois, ofegante, vindo de outro caminho.")

    estado["status"]["hp"] = max(1, estado["status"].get("hp", 1) - dano)

    print(f"Henry perdeu {dano} HP.")
    return 1


def _tem_item_com_nome(estado: dict, trecho_nome: str) -> bool:
    """Verifica se existe item no inventário contendo parte do nome."""
    trecho_nome = trecho_nome.lower()
    return any(
        trecho_nome in item.get("nome", "").lower()
        for item in estado.get("inventario", [])
    )


def _criar_mob_toca(estado: dict, profundidade: int, numero: int) -> dict:
    """Cria mobs específicos para o evento da toca de Mitis."""
    criatura = gerar_criatura_distorcida(estado, profundidade)

    nomes = {
        1: "Slime de Lama da Toca",
        2: "Golem de Raiz Subterrânea",
        3: "Slime de Terra Antiga",
    }

    criatura["nome"] = f"{nomes.get(numero, 'Criatura da Toca')} Nv.{criatura.get('nivel', 1)}"
    criatura["fraquezas"] = ["fire", "blizzard", "quake"]
    criatura["resistencias"] = ["dark"]

    return criatura


def evento_toca_mitis(estado: dict, profundidade: int) -> bool:
    """Evento especial da Floresta Distorcida.

    Mitis entra em uma toca e Henry enfrenta combates sozinho enquanto ele
    investiga runas subterrâneas. Retorna True quando substitui a sala normal.
    """
    print("\nEntre raízes tortas e folhas úmidas, Mitis para de repente.")
    print("Há uma pequena toca escura aberta na lateral do caminho.")
    print("O buraco parece comum, mas a terra ao redor pulsa com uma magia antiga.")
    print('Mitis: "Henry... essa toca não estava aqui antes."')
    print('Henry: "Você quer entrar aí?"')
    print("Mitis observa a entrada em silêncio.")
    print("Por ser uma coruja-buraqueira, ele se sente intrigado.")
    print("É quase como se a própria toca o convidasse a entrar.")

    print("\nDeseja deixar Mitis investigar a toca?")
    print("1 - Sim, Mitis entra na toca")
    print("2 - Não, dar meia-volta e seguir junto")

    escolha = input("Escolha: ").strip()

    if escolha != "1":
        print("\nHenry chama Mitis de volta.")
        print('Mitis: "Talvez seja melhor não obedecer tudo que a floresta oferece."')
        return False

    print("\nMitis respira fundo e entra na toca.")
    print("A passagem é estreita demais para Henry acompanhar.")
    print("Por alguns segundos, só o som das garras de Mitis ecoa sob a terra.")
    print("Então a floresta ao redor de Henry fica silenciosa demais.")
    print("Galhos se mexem. A seiva escura borbulha entre as raízes.")
    print("Um monstro surge entre as árvores enquanto Mitis ainda está lá dentro.")

    estado["mitis_separado"] = True

    try:
        mob1 = _criar_mob_toca(estado, profundidade, 1)
        venceu = iniciar_combate_contra(
            estado,
            mob1,
            contexto="Floresta Distorcida — Toca de Mitis | Henry sozinho",
        )

        if not venceu or estado["status"].get("hp", 0) <= 0:
            return True

        print("\nHenry limpa a poeira das patas, olhando para a entrada da toca.")
        print('Henry: "Mitis, tudo bem por aí?"')
        print('Mitis: "Interessante..."')
        print('Henry: "Leve o tempo que precisar... até lá viro acervo da floresta T_T"')
        print('Mitis: "Não seja dramático. Há algo peculiar aqui. Sinto que há algo escondido."')
        print('Henry: "Uma ajuda seria bem-vinda :)"')
        print('Mitis: "Achei!"')
        print("\nMitis puxa uma raiz estranha. Ela se esfarela e revela um pequeno altar de pedra.")
        print("Mitis se aproxima para examinar o altar mais de perto.")

        print("\nOutro monstro aparece entre as árvores.")
        print('Henry: "Mitis, é para hoje?"')
        print('Mitis: "Não se apressa o conhecimento. Essas runas são antigas, preciso de tempo..."')

        mob2 = _criar_mob_toca(estado, profundidade + 1, 2)
        venceu = iniciar_combate_contra(
            estado,
            mob2,
            contexto="Floresta Distorcida — Altar Subterrâneo | Henry sozinho",
        )

        if not venceu or estado["status"].get("hp", 0) <= 0:
            return True

        print("\nMitis averigua as runas cuidadosamente.")
        print("Ele percebe que elas descrevem um item. Uma ativação de item, para ser mais preciso.")

        print("\nDeseja checar o item indicado pelas runas?")
        print("1 - Sim")
        print("2 - Não")

        escolha_item = input("Escolha: ").strip()

        if escolha_item == "1":
            print("\nAs runas brilham fraco e desenham a forma de uma pedra luminosa.")
            print("Item necessário: Pedra Fluorescente.")

            if _tem_item_com_nome(estado, "Pedra Fluorescente"):
                print("\nHenry possui uma Pedra Fluorescente no inventário.")
                print('Mitis: "Ué... por que não está funcionando a ativação?"')
                print('Henry: "Leia novamente, pode ter deixado algo passar!"')
            else:
                print("\nHenry não possui uma Pedra Fluorescente.")
                print("O altar permanece apagado.")
                print('Mitis: "Sem a pedra certa, não consigo ativar isso agora."')
                print("Mitis retorna pela toca e se junta novamente a Henry.")
                return True
        else:
            print("\nHenry decide não mexer no item indicado.")
            print("Mitis retorna pela toca, ainda desconfiado das runas.")
            return True

        print("\nEnquanto Mitis relê as runas, outra criatura surge.")
        print("A Pedra Fluorescente faz aparecer novas linhas no altar.")
        print('Mitis: "Ao ser que chegou até aqui, preste bastante atenção..."')
        print('Mitis: "É preciso usar a magia que há desde o início da Criação."')
        print('Henry: "Estamos ferrados..."')
        print('Mitis: "Vamos lá, pensa, Mitis..."')
        print('Henry: "Esses Slimes de Lama ou Terra são terríveis de derrotar sem magia."')
        print('Henry: "Estou quase sem mana. Uma ajuda seria bem-vinda :)"')
        print('Mitis: "É isso!"')
        print('Henry: "Uma ajuda seria bem-vinda?"')
        print('Mitis: "Não, seu felino tolo. Magia da criação... Terra!"')
        print('Henry: "Ei!... Boa, Mitis."')

        mob3 = _criar_mob_toca(estado, profundidade + 2, 3)
        venceu = iniciar_combate_contra(
            estado,
            mob3,
            contexto="Floresta Distorcida — Runas da Terra | Henry sozinho",
        )

        if not venceu or estado["status"].get("hp", 0) <= 0:
            return True

        print("\nMitis quer executar a magia da Terra no altar.")
        print("Deseja executar?")
        print("1 - Sim")
        print("2 - Não")

        escolha_magia = input("Escolha: ").strip()

        if escolha_magia == "1":
            print("\nMitis concentra a magia da Terra.")
            print("O altar começa a brilhar, mudando de textura.")
            print("A pedra parece ser absorvida pela própria magia elemental.")
            print("A parede de terra se abre lentamente, revelando um novo caminho.")
            print("Mitis atravessa a passagem e finalmente se junta a Henry.")

            item = {
                "nome": "Fragmento de Altar de Terra",
                "tipo": "material",
                "raridade": "raro",
                "peso": 1,
                "valor_magico": 60,
                "preco": 120,
                "descricao": "Fragmento de um altar antigo ativado pela magia da Terra de Mitis.",
            }
            adicionar_item(estado, item)

            print('\nMitis: "Pode dizer, sentiu saudades hahaha"')
            print('Henry: "Sim, saudades de te usar de escudo..."')
            print('Mitis: "Abri o caminho :)"')
            print('Henry: "E o meu quase encerrou..."')
        else:
            print("\nMitis decide não ativar o altar.")
            print("A passagem se fecha lentamente, como se nunca tivesse existido.")
            print("Ele retorna pelo caminho antigo e se junta a Henry.")

        return True

    finally:
        estado["mitis_separado"] = False


def acampar_floresta_distorcida(estado: dict, profundidade: int) -> bool:
    """Permite acampar na Floresta Distorcida usando D20.

    Retorna True quando o descanso foi resolvido, ou False quando uma
    emboscada deve acontecer.
    """
    print("\n=== ACAMPAR NA FLORESTA DISTORCIDA ===")
    print("Henry observa a trilha se dobrando entre as raízes.")
    print("Mitis pousa em um galho baixo, atento ao silêncio estranho ao redor.")
    print('Henry: "Talvez a gente precise parar um pouco."')
    print('Mitis: "Descansar aqui é arriscado... mas continuar exausto também é."')

    print("\nDeseja montar acampamento?")
    print("1 - Sim, tentar descansar")
    print("2 - Não, continuar em movimento")

    escolha = input("Escolha: ").strip()

    if escolha != "1":
        print("\nHenry decide continuar andando.")
        print("Mitis balança as penas, ainda desconfiado da floresta.")
        return True

    rolagem = rolar_d20()
    print(f"\nRolagem de descanso: D20 = {rolagem}")

    status = estado["status"]
    hp_max = status.get("hp_max", status.get("hp", 100))
    mana_max = status.get("mana_max", status.get("mana", 50))

    if rolagem == 20:
        print("\nDescanso perfeito!")
        print("A Floresta Distorcida, por algum motivo, não os rejeita desta vez.")
        print("As raízes se afastam, o vento fica leve e pequenas frutas luminosas aparecem perto do acampamento.")
        print('Mitis: "Estranho... é quase como se a floresta estivesse recompensando nossa bravura."')
        print('Henry: "Finalmente ela resolveu ser simpática."')

        status["hp"] = hp_max
        status["mana"] = mana_max

        fruta = {
            "nome": "Fruta Serena da Floresta",
            "tipo": "consumivel",
            "raridade": "raro",
            "peso": 1,
            "valor_magico": 35,
            "preco": 70,
            "efeitos": {
                "hp": 35,
                "mana": 20,
            },
            "descricao": "Uma fruta luminosa encontrada durante um descanso perfeito na Floresta Distorcida.",
        }

        adicionar_item(estado, fruta)
        print("HP e mana foram totalmente restaurados.")
        print("Henry recebeu: Fruta Serena da Floresta.")
        return True

    if rolagem >= 15:
        cura_hp = max(10, hp_max // 3)
        cura_mana = max(8, mana_max // 3)

        print("\nBom descanso.")
        print("A noite não foi tranquila, mas Henry e Mitis conseguiram recuperar parte das forças.")
        print("Mitis permaneceu acordado por alguns momentos, observando sombras que se moviam longe demais.")

        status["hp"] = min(hp_max, status.get("hp", 0) + cura_hp)
        status["mana"] = min(mana_max, status.get("mana", 0) + cura_mana)

        print(f"Henry recuperou {cura_hp} HP.")
        print(f"O grupo recuperou {cura_mana} de mana.")
        return True

    if rolagem >= 8:
        print("\nDescanso inquieto.")
        print("Henry tenta dormir, mas a floresta sussurra entre as raízes.")
        print("Mitis acorda várias vezes, certo de que algo passou perto do acampamento.")
        print("Eles descansam, mas não o suficiente.")

        cura_hp = max(5, hp_max // 10)
        status["hp"] = min(hp_max, status.get("hp", 0) + cura_hp)

        penalidade_mana = 3
        status["mana"] = max(0, status.get("mana", 0) - penalidade_mana)

        print(f"Henry recuperou apenas {cura_hp} HP.")
        print(f"A tensão consumiu {penalidade_mana} de mana.")
        return True

    print("\nEmboscada!")
    print("O fogo improvisado apaga de repente.")
    print("Mitis abre as asas, mas já é tarde.")
    print("Algo estava observando o acampamento desde o começo.")
    print('Henry: "Eu sabia que dormir aqui era uma péssima ideia."')
    print('Mitis: "Reclame depois. Agora levante!"')

    return False


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
        evento_resolveu_sala = False

        if random() < 0.20:
            evento_resolveu_sala = evento_toca_mitis(estado, profundidade)

        if estado["status"].get("hp", 0) <= 0:
            print("\nA Floresta Distorcida expulsou Henry e Mitis de volta para a Vila das Preguiças.")
            _curar_ao_sair(estado)
            return

        if not evento_resolveu_sala and random() < 0.35:
            evento = choice([
                evento_pedra_estranha,
                evento_voz_distorcida,
                evento_chao_desaparece,
            ])

            if evento == evento_chao_desaparece:
                nova_profundidade = evento_chao_desaparece(estado, profundidade)
                if nova_profundidade is not None:
                    profundidade = nova_profundidade
                    continue
            else:
                evento(estado)

        if evento_resolveu_sala:
            if estado.get("ultimo_resultado_combate") in {"fuga", "derrota"}:
                print("\nHenry e Mitis escaparam antes de dominar a sala. Nenhuma recompensa da dungeon foi entregue.")
                _curar_ao_sair(estado)
                return
            venceu = True
        else:
            print("-" * 56)
            print("Henry e Mitis sentem que algo se aproxima...")
            print("=" * 56)
            estado["mitis_separado"] = False
            venceu = iniciar_combate_contra(
                estado,
                criatura,
                contexto=f"Floresta Distorcida — Sala {profundidade:02d}",
            )

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
        print("2 - Acampar antes de continuar")
        print("3 - Sair da Floresta Distorcida")
        escolha = input("Escolha: ").strip()

        if escolha == "2":
            descanso_seguro = acampar_floresta_distorcida(estado, profundidade)

            if not descanso_seguro:
                criatura_emboscada = gerar_criatura_distorcida(estado, profundidade + 1)
                criatura_emboscada["nome"] = "Emboscador da Floresta Distorcida"

                venceu_emboscada = iniciar_combate_contra(
                    estado,
                    criatura_emboscada,
                    contexto=f"Emboscada no Acampamento — Profundidade {profundidade:02d}",
                )

                if estado["status"].get("hp", 0) <= 0:
                    print("\nA Floresta Distorcida expulsou Henry e Mitis de volta para a Vila das Preguiças.")
                    _curar_ao_sair(estado)
                    return

                if not venceu_emboscada:
                    print("\nHenry e Mitis fugiram da emboscada e retornaram para a entrada da floresta.")
                    _curar_ao_sair(estado)
                    return

            print("\nDepois do acampamento, Henry e Mitis seguem mais fundo.")

        elif escolha != "1":
            print("Henry e Mitis retornaram pelo portal antes que a floresta mudasse de novo.")
            _curar_ao_sair(estado)
            return

        aplicar_teste_mobilidade(estado, "Profundidade " + str(profundidade), "Profundidade " + str(profundidade + 1), 10 + profundidade)
        profundidade += 1
