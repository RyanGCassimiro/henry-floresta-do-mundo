"""Membro 2 — Loja da Capivara para compra e venda de itens."""
from membro3_inventario.inventory import adicionar_item, remover_item_por_indice

ESTOQUE_CAPIVARA = [
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
        "nome": "Capa de Ipê Roxo",
        "tipo": "equipamento",
        "slot": "capa",
        "raridade": "rara",
        "peso": 2,
        "valor_magico": 40,
        "preco": 90,
        "efeitos": {"magia": 3},
        "descricao": "+3 magia.",
    },
    {
        "nome": "Anel de Vitória-régia",
        "tipo": "equipamento",
        "slot": "anel",
        "raridade": "rara",
        "peso": 1,
        "valor_magico": 35,
        "preco": 80,
        "efeitos": {"hp_max": 20},
        "descricao": "+20 HP máximo.",
    },
    {
        "nome": "Dólar Místico",
        "tipo": "equipamento",
        "slot": "amuleto",
        "raridade": "rara",
        "peso": 1,
        "valor_magico": 60,
        "preco": 100,
        "efeitos": {"mana_max": 50},
        "descricao": "+50 mana máxima.",
    },
    {
        "nome": "Staff de Brasa",
        "tipo": "equipamento",
        "slot": "arma",
        "raridade": "epica",
        "peso": 3,
        "valor_magico": 70,
        "preco": 120,
        "efeitos": {"magia": 4, "fire": 1},
        "descricao": "+4 magia e +1 bônus de fire.",
    },
    {
        "nome": "Cajado das Marés",
        "tipo": "equipamento",
        "slot": "arma",
        "raridade": "rara",
        "peso": 2,
        "valor_magico": 62,
        "preco": 105,
        "efeitos": {"magia": 2, "water": 1},
        "descricao": "+2 magia e +1 bônus de Water.",
    },
    {
        "nome": "Cristal Sombrio",
        "tipo": "equipamento",
        "slot": "amuleto",
        "raridade": "epica",
        "peso": 1,
        "valor_magico": 72,
        "preco": 130,
        "efeitos": {"dark": 1, "mana_max": 20},
        "descricao": "+1 bônus de Dark e +20 mana máxima.",
    },

    {
        "nome": "Orbe de Geada",
        "tipo": "equipamento",
        "slot": "amuleto",
        "raridade": "rara",
        "peso": 1,
        "valor_magico": 55,
        "preco": 95,
        "efeitos": {"magia": 2, "blizzard": 1},
        "descricao": "+2 magia e +1 bônus de Blizzard.",
    },
    {
        "nome": "Bracelete de Trovão",
        "tipo": "equipamento",
        "slot": "anel",
        "raridade": "rara",
        "peso": 1,
        "valor_magico": 58,
        "preco": 105,
        "efeitos": {"thunder": 1, "mana_max": 15},
        "descricao": "+1 bônus de thunder e +15 mana máxima.",
    },
    {
        "nome": "Totem de Barro do Mitis",
        "tipo": "equipamento",
        "slot": "amuleto",
        "raridade": "rara",
        "peso": 1,
        "valor_magico": 52,
        "preco": 95,
        "efeitos": {"quake": 2},
        "descricao": "+2 bônus de Quake para Mitis.",
    },
    {
        "nome": "Adagas de Veneno",
        "tipo": "equipamento",
        "slot": "arma",
        "raridade": "epica",
        "peso": 2,
        "valor_magico": 65,
        "preco": 110,
        "efeitos": {"ataque": 2, "veneno": 10},
        "descricao": "+2 ataque e +10 veneno.",
    },
]


def abrir_loja_capivara(estado: dict) -> None:
    print("\n=== LOJA DA CAPIVARA ===")
    print('A Capivara comerciante sorri: "Compra, vende, troca... só não aceito fiado."')

    while True:
        print(f"\nMoedas de Henry: {estado['moedas']}")
        print("1 - Comprar item")
        print("2 - Vender item")
        print("0 - Sair da loja")
        escolha = input("Escolha: ").strip()

        if escolha == "1":
            comprar_item(estado)
        elif escolha == "2":
            vender_item(estado)
        elif escolha == "0":
            print("A Capivara acena calmamente.")
            return
        else:
            print("Opção inválida.")


def comprar_item(estado: dict) -> None:
    print("\n=== ESTOQUE ===")
    for i, item in enumerate(ESTOQUE_CAPIVARA, start=1):
        print(f"{i} - {item['nome']} | preço: {item['preco']} | {item['descricao']}")

    try:
        escolha = int(input("Item para comprar: "))
        item = ESTOQUE_CAPIVARA[escolha - 1]
    except (ValueError, IndexError):
        print("Escolha inválida.")
        return

    if estado["moedas"] < item["preco"]:
        print("Moedas insuficientes.")
        return

    estado["moedas"] -= item["preco"]
    adicionar_item(estado, item.copy())
    print(f"Henry comprou {item['nome']}.")


def vender_item(estado: dict) -> None:
    inventario = estado["inventario"]
    if not inventario:
        print("Inventário vazio.")
        return

    print("\n=== VENDER ITEM ===")
    for i, item in enumerate(inventario, start=1):
        valor_venda = max(1, item.get("preco", 10) // 2)
        print(f"{i} - {item['nome']} | venda: {valor_venda}")

    try:
        escolha = int(input("Item para vender: "))
        item = inventario[escolha - 1]
    except (ValueError, IndexError):
        print("Escolha inválida.")
        return

    valor_venda = max(1, item.get("preco", 10) // 2)
    removido = remover_item_por_indice(estado, escolha - 1)
    if removido:
        estado["moedas"] += valor_venda
        print(f"Henry vendeu {item['nome']} por {valor_venda} moedas.")
