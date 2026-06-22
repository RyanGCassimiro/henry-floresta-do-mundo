"""Membro 2 — Coleta de itens nos locais."""
from random import choice

from membro2_mundo.dados import rolar_d20
from membro2_mundo.locais import ITENS_POR_LOCAL
from membro3_inventario.inventory import adicionar_item


EVENTOS_COLETA = [
    {
        "pista": "Há um arbusto de formato estranho perto da trilha.",
        "pergunta": "Deseja verificar o arbusto?",
        "sucesso": "Henry afasta os galhos com cuidado e encontra algo escondido entre as folhas.",
        "falha": "O arbusto estava cheio de espinhos finos. Henry se machuca ao tentar mexer nele.",
        "ignorar": "Henry decide não mexer no arbusto. Talvez tenha sido melhor assim.",
    },
    {
        "pista": "Uma pedra destoa das outras, como se tivesse sido colocada ali de propósito.",
        "pergunta": "Deseja examinar a pedra?",
        "sucesso": "Henry vira a pedra e encontra um item escondido embaixo dela.",
        "falha": "A pedra se parte e libera uma poeira irritante. Henry perde um pouco de HP.",
        "ignorar": "Henry deixa a pedra onde está e segue o caminho.",
    },
    {
        "pista": "Uma flor estranha cresce sozinha em meio à vegetação escura.",
        "pergunta": "Deseja colher a flor?",
        "sucesso": "A flor brilha ao toque de Henry. Havia algo mágico preso às suas raízes.",
        "falha": "A flor solta um pó venenoso. Henry recua tossindo.",
        "ignorar": "Henry decide não tocar na flor desconhecida.",
    },
    {
        "pista": "Mitis nota uma árvore frutífera com frutos pequenos e luminosos.",
        "pergunta": "Deseja verificar os frutos?",
        "sucesso": "Henry encontra um item entre os frutos caídos.",
        "falha": "Quando Henry se aproxima, cipós escondidos arranham suas patas.",
        "ignorar": "Henry decide não arriscar comer ou tocar nos frutos.",
    },
    {
        "pista": "A terra está molhada e revirada, como se algo tivesse sido enterrado recentemente.",
        "pergunta": "Deseja cavar um pouco?",
        "sucesso": "Henry cava com cuidado e encontra algo enterrado.",
        "falha": "A terra afunda de repente e Henry machuca a pata ao tentar se equilibrar.",
        "ignorar": "Henry decide não mexer na terra revirada.",
    },
    {
        "pista": "Há desenhos antigos marcados em uma raiz grossa.",
        "pergunta": "Deseja examinar os desenhos?",
        "sucesso": "Os desenhos brilham por alguns segundos e revelam um item escondido.",
        "falha": "As marcas se apagam e liberam uma energia instável contra Henry.",
        "ignorar": "Henry ignora os desenhos e continua seguindo a trilha.",
    },
    {
        "pista": "Mitis percebe runas estranhas gravadas em uma pedra coberta por musgo.",
        "pergunta": "Deseja ler as runas?",
        "sucesso": "As runas reagem à presença de Henry e revelam algo útil.",
        "falha": "As runas estavam protegidas por uma armadilha mágica. Henry perde HP.",
        "ignorar": "Mitis observa as runas por mais um instante, mas Henry decide seguir.",
    },
]


def coletar_item_no_local(estado: dict) -> None:
    """Coleta narrativa de itens no local atual."""
    local = estado.get("local_atual")
    itens = ITENS_POR_LOCAL.get(local, [])

    if not itens:
        print(f"\nNão há sinais claros de itens coletáveis em {local}.")
        return

    evento = choice(EVENTOS_COLETA)
    item = choice(itens)

    print(f"\n=== EXPLORAÇÃO EM {local.upper()} ===")
    print(evento["pista"])
    print("Mitis observa o lugar com atenção.")
    print(f"\n{evento['pergunta']}")
    print("1 - Sim")
    print("2 - Não")

    escolha = input("Escolha: ").strip()

    if escolha != "1":
        print(f"\n{evento['ignorar']}")
        return

    rolagem = rolar_d20()
    print(f"\nRolagem de investigação: D20 = {rolagem}")

    if rolagem == 20:
        print("\nSucesso crítico!")
        print(evento["sucesso"])
        print("A floresta parece recompensar a coragem de Henry.")

        adicionar_item(estado, item.copy())
        print(f"Henry encontrou: {item['nome']}.")

        bonus_moedas = 10
        estado["moedas"] = estado.get("moedas", 0) + bonus_moedas
        print(f"Henry também encontrou {bonus_moedas} moedas antigas.")

    elif rolagem >= 12:
        print("\nSucesso!")
        print(evento["sucesso"])

        adicionar_item(estado, item.copy())
        print(f"Henry encontrou: {item['nome']}.")

    elif rolagem >= 8:
        print("\nResultado incerto.")
        print("Henry procura com cuidado, mas não encontra nada útil.")
        print("Mesmo assim, Mitis parece aliviado por nada pior ter acontecido.")

    else:
        dano = 5

        print("\nFalha!")
        print(evento["falha"])

        estado["status"]["hp"] = max(
            1,
            estado["status"].get("hp", 1) - dano,
        )

        print(f"Henry perdeu {dano} HP.")
        return
