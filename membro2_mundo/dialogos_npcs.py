"""Membro 2 — Diálogos de NPCs, rumores e criação de itens.

Este módulo adiciona uma camada de RPG de mesa ao terminal:
- cada local pode ter NPCs com diálogos;
- a Capivara pode contar rumores do mundo;
- Camila libera criação de mantos/capas após a quest dela ser concluída.
"""
from __future__ import annotations

from random import choice

from membro3_inventario.inventory import adicionar_item, consultar_item, remover_item


NPCS_POR_LOCAL = {
    "Vila das Preguiças": ["Santiago", "Preguiça Guardiã"],
    "Lago das Capivaras": ["Capivara Mercadora", "Beatriz"],
    "Bosque do Ipê": ["Camila"],
    "Ruínas da Arpia": ["Eduardo"],
    "Caverna dos Golems": ["Monique"],
    "Clareira da Árvore do Mundo": ["Pietra"],
}

RUMORES_CAPIVARA = [
    "Dizem que a Floresta Distorcida muda quando Henry sobe de nível.",
    "Ouvi dizer que as poções funcionam melhor quando Mitis treina Cure.",
    "Santiago conhece atalhos, mas só confia em quem respeita as rotas antigas.",
    "Camila aprendeu a tecer mantos com algodão e seiva clara.",
    "Golems resistem a trovão, mas água e gelo costumam abrir rachaduras na seiva.",
    "Se a água do lago ficar silenciosa demais, talvez ela esteja ouvindo você.",
]

DIALOGOS_NPCS = {
    "Preguiça Guardiã": [
        "A pressa quebra portais, Henry. Calcule a rota antes de atravessar caminhos antigos.",
        "A Árvore do Mundo não pede força bruta. Ela pede ordem, cuidado e memória.",
    ],
    "Santiago": [
        "Eu sou Santiago, navegador das correntes de vento. Um mapa bom vale mais que coragem sem rumo.",
        "Quando a rota TSP estiver calculada, eu consigo marcar atalhos seguros para vocês.",
    ],
    "Capivara Mercadora": [
        "Comprar barato, vender com calma e nunca atravessar pântano sem poção. Essa é a lei da margem.",
        "Quer um rumor? Pague com atenção, não com moeda. A floresta fala com quem escuta...",
    ],
    "Camila": [
        "Sou Camila. Onde todo mundo vê mato, eu vejo fibra, abrigo e ferramenta.",
        "Depois que as formigas luminosas se acalmarem, eu posso ajudar vocês a criar mantos babadeiros.",
    ],
    "Eduardo": [
        "Pegadas contam histórias. Nas ruínas, até o silêncio deixa rastro.",
        "Se uma Pena Sombria aparece duas vezes no mesmo lugar, ela não está perdida. Está guardando algo.",
    ],
    "Monique": [
        "Eu sou Monique. Às vezes vencer requer paciência e se o casco aguenta o impacto certo.",
        "Na caverna, defesa importa tanto quanto ataque. Golem não perdoa descuido.",
    ],
    "Pietra": [
        "Força sem propósito vira ameaça. Força com cuidado vira proteção.",
        "Quando você estiver pronto, a floresta vai reconhecer o seu passo.",
    ],
    "Beatriz": [
        "O-oi... eu sou Beatriz. Eu escuto a correnteza quando ela muda de voz.",
        "Estou procurando a Canção das Águas... ela virou uma Pérola Furta-cor dentro da Floresta Distorcida.",
    ],
}

RECEITAS_CAMILA = [
    {
        "nome": "Manto Simples de Algodão",
        "requer": {"Algodão Macio": 2},
        "resultado": {
            "nome": "Manto Simples de Algodão",
            "tipo": "equipamento",
            "slot": "capa",
            "raridade": "comum",
            "peso": 2,
            "valor_magico": 18,
            "preco": 35,
            "efeitos": {"defesa": 1},
            "descricao": "+1 defesa. Criado por Camila com algodão macio.",
        },
    },
    {
        "nome": "Capa Florida da Camila",
        "requer": {"Algodão Macio": 2, "Flor de Ipê": 1},
        "resultado": {
            "nome": "Capa Florida da Camila",
            "tipo": "equipamento",
            "slot": "capa",
            "raridade": "incomum",
            "peso": 2,
            "valor_magico": 32,
            "preco": 70,
            "efeitos": {"defesa": 1, "magia": 1},
            "descricao": "+1 defesa e +1 magia. Uma capa leve com fibras de ipê.",
        },
    },
    {
        "nome": "Manto de Seiva Trançada",
        "requer": {"Algodão Macio": 2, "Fragmento de Seiva": 1},
        "resultado": {
            "nome": "Manto de Seiva Trançada",
            "tipo": "equipamento",
            "slot": "capa",
            "raridade": "rara",
            "peso": 2,
            "valor_magico": 58,
            "preco": 115,
            "efeitos": {"defesa": 2, "magia": 2},
            "descricao": "+2 defesa e +2 magia. Manto criado com seiva estabilizada.",
        },
    },
]


def _contar_item(estado: dict, nome: str) -> int:
    nome_normalizado = nome.lower()
    return sum(1 for item in estado.get("inventario", []) if item.get("nome", "").lower() == nome_normalizado)


def _tem_materiais(estado: dict, requer: dict[str, int]) -> bool:
    return all(_contar_item(estado, nome) >= qtd for nome, qtd in requer.items())


def _mostrar_materiais(estado: dict, requer: dict[str, int]) -> str:
    partes = []
    for nome, qtd in requer.items():
        possui = _contar_item(estado, nome)
        partes.append(f"{nome} {possui}/{qtd}")
    return ", ".join(partes)


def _consumir_materiais(estado: dict, requer: dict[str, int]) -> None:
    for nome, qtd in requer.items():
        for _ in range(qtd):
            remover_item(estado, nome)


def camila_criacao_liberada(estado: dict) -> bool:
    return estado.get("quests_personagens", {}).get("camila") == "concluida"


def criar_item_camila(estado: dict, receita_indice: int) -> bool:
    """Cria um item pela bancada da Camila usando índice zero-based."""
    if not camila_criacao_liberada(estado):
        print("Camila ainda não liberou a criação de itens. Conclua a quest dela primeiro.")
        return False

    if not 0 <= receita_indice < len(RECEITAS_CAMILA):
        print("Receita inválida.")
        return False

    receita = RECEITAS_CAMILA[receita_indice]
    if not _tem_materiais(estado, receita["requer"]):
        print("Materiais insuficientes.")
        print("Necessário:", _mostrar_materiais(estado, receita["requer"]))
        return False

    _consumir_materiais(estado, receita["requer"])
    adicionar_item(estado, receita["resultado"].copy())
    print(f"Camila criou: {receita['resultado']['nome']}")
    return True


def abrir_criacao_camila(estado: dict) -> None:
    if not camila_criacao_liberada(estado):
        print("Camila observa as fibras, mas ainda está preocupada com as formigas luminosas.")
        print("Conclua a quest da Camila para liberar a criação de itens.")
        return

    while True:
        print("\n=== CRIAÇÃO DE ITENS — CAMILA ===")
        for i, receita in enumerate(RECEITAS_CAMILA, start=1):
            materiais = _mostrar_materiais(estado, receita["requer"])
            item = receita["resultado"]
            print(f"{i} - {receita['nome']} | requer: {materiais} | efeitos: {item.get('efeitos', {})}")
        print("0 - Voltar")
        escolha = input("Escolha uma receita: ").strip()
        if escolha == "0":
            return
        try:
            criar_item_camila(estado, int(escolha) - 1)
        except ValueError:
            print("Opção inválida.")


def conversar_beatriz(estado: dict) -> None:
    """Diálogo com Beatriz, a boto-cor-de-rosa.

    Beatriz é simpática, tímida e ligada às águas doces. Sua quest especial
    envolve a Canção das Águas e a Pérola Furta-cor perdida em uma sala aquática
    rara da Floresta Distorcida.
    """
    print("\n=== BEATRIZ — BOTO-COR-DE-ROSA ===")
    print('Beatriz aparece perto da margem, meio escondida pela água brilhante.')
    print('"O-oi... eu sou a Beatriz. Eu escuto a correnteza quando ela muda de voz."')

    while True:
        print("\n1 - Perguntar sobre o lago")
        print("2 - Perguntar sobre magia de água")
        print("3 - Perguntar sobre a Canção das Águas")
        print("4 - Perguntar sobre a Pérola Furta-cor")
        print("0 - Encerrar conversa")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            print('\nBeatriz: "O lago parece calmo, mas ele guarda caminhos que só aparecem para quem observa devagar."')
        elif opcao == "2":
            print('\nBeatriz: "Water não é só ataque. Água também carrega memória, cura e passagem."')
            print('Ela aponta para pequenas ondas rosadas que brilham perto de Henry.')
        elif opcao == "3":
            print('\nBeatriz: "A Canção das Águas era protegida pelos animais aquáticos de água doce."')
            print('"Ela mantém a pureza das águas. Sem ela, até os rios começam a esquecer o próprio caminho."')
        elif opcao == "4":
            print('\nBeatriz: "A canção se cristalizou numa Pérola Furta-cor..."')
            print('"Ela caiu em um nível aleatório da Floresta Distorcida, mas só aparece em trechos ligados à água."')
            print("Dica: procure salas como Clareira de Névoa Azul ou outros trechos aquáticos da dungeon.")
        elif opcao == "0":
            print('\nBeatriz: "Obrigada por procurar comigo..."')
            return
        else:
            print("Opção inválida.")


def escutar_rumor_capivara() -> None:
    print("\nCapivara Mercadora ajeita os itens sobre a banca.")
    print(f'Capivara: "{choice(RUMORES_CAPIVARA)}"')


def conversar_capivara(estado: dict) -> None:
    while True:
        print("\n=== CAPIVARA MERCADORA ===")
        print("A Capivara observa Henry com calma, como se já soubesse o que ele procura.")
        print("\n1 - Conversar")
        print("2 - Escutar rumor")
        print("0 - Voltar")

        escolha = input("Escolha: ").strip()

        if escolha == "1":
            print('\nCapivara: "Comprar é fácil. Difícil é saber o que levar para sobreviver."')
        elif escolha == "2":
            escutar_rumor_capivara()
        elif escolha == "0":
            return
        else:
            print("Opção inválida.")


def _falar_com_npc(estado: dict, npc: str) -> None:
    if npc == "Beatriz":
        conversar_beatriz(estado)
        return
    if npc == "Capivara Mercadora":
        conversar_capivara(estado)
        return

    print(f"\n=== {npc.upper()} ===")
    for fala in DIALOGOS_NPCS.get(npc, ["..."]):
        print(f"{npc}: {fala}")

    if npc == "Camila":
        print("\n1 - Abrir criação de itens da Camila")
        print("0 - Voltar")
        escolha = input("Escolha: ").strip()
        if escolha == "1":
            abrir_criacao_camila(estado)


def abrir_dialogos_local(estado: dict) -> None:
    local = estado.get("local_atual", "")
    npcs = NPCS_POR_LOCAL.get(local, [])

    if not npcs:
        print(f"Não há NPCs disponíveis em {local}.")
        return

    while True:
        print(f"\n=== NPCS EM {local.upper()} ===")
        for i, npc in enumerate(npcs, start=1):
            print(f"{i} - Conversar com {npc}")
        print("0 - Voltar")

        escolha = input("Escolha um NPC: ").strip()
        if escolha == "0":
            return
        try:
            npc = npcs[int(escolha) - 1]
        except (ValueError, IndexError):
            print("Opção inválida.")
            continue
        _falar_com_npc(estado, npc)
