"""Membro 3 — Interface textual do inventário."""


def mostrar_inventario(estado: dict) -> None:
    inventario = estado["inventario"]
    print("\n=== INVENTÁRIO DE HENRY ===")

    if not inventario:
        print("Inventário vazio.")
        return

    for i, item in enumerate(inventario, start=1):
        print(
            f"{i} - {item['nome']} | "
            f"tipo: {item.get('tipo', '-')} | "
            f"raridade: {item.get('raridade', '-')} | "
            f"peso: {item.get('peso', 0)} | "
            f"valor mágico: {item.get('valor_magico', 0)} | "
            f"preço: {item.get('preco', 0)}"
        )
        print(f"    {item.get('descricao', '')}")


def mostrar_equipamentos(estado: dict) -> None:
    print("\n=== EQUIPAMENTOS ===")
    for slot, item in estado["equipamentos"].items():
        if item:
            print(f"{slot}: {item['nome']} | efeitos: {item.get('efeitos', {})}")
        else:
            print(f"{slot}: vazio")


def mostrar_equipamentos_disponiveis(estado: dict) -> list[tuple[int, dict]]:
    """Mostra apenas equipamentos disponíveis para equipar por número."""
    equipamentos = [
        (indice, item)
        for indice, item in enumerate(estado["inventario"])
        if item.get("tipo") == "equipamento"
    ]

    print("\n=== EQUIPAMENTOS DISPONÍVEIS PARA EQUIPAR ===")
    if not equipamentos:
        print("Nenhum equipamento no inventário.")
        return []

    for numero, (_, item) in enumerate(equipamentos, start=1):
        print(
            f"{numero} - {item['nome']} | "
            f"slot: {item.get('slot', '-')} | "
            f"raridade: {item.get('raridade', '-')} | "
            f"efeitos: {item.get('efeitos', {})}"
        )
        print(f"    {item.get('descricao', '')}")

    print("0 - Cancelar")
    return equipamentos



def mostrar_itens_para_consulta(estado: dict) -> list[tuple[int, dict]]:
    """Mostra todos os itens com numeração para consulta."""
    inventario = estado["inventario"]
    print("\n=== CONSULTAR ITEM ===")
    if not inventario:
        print("Inventário vazio.")
        return []

    for numero, item in enumerate(inventario, start=1):
        print(f"{numero} - {item['nome']} | tipo: {item.get('tipo', '-')} | raridade: {item.get('raridade', '-')}")
    print("0 - Cancelar")
    return list(enumerate(inventario))


def mostrar_detalhes_item(item: dict) -> None:
    """Mostra os detalhes de um item de forma mais legível."""
    print("\n=== DETALHES DO ITEM ===")
    print(f"Nome: {item.get('nome', '-')}")
    print(f"Tipo: {item.get('tipo', '-')}")
    print(f"Raridade: {item.get('raridade', '-')}")
    print(f"Peso: {item.get('peso', 0)}")
    print(f"Valor mágico: {item.get('valor_magico', 0)}")
    print(f"Preço: {item.get('preco', 0)}")
    if item.get("slot"):
        print(f"Slot: {item.get('slot')}")
    if item.get("efeitos"):
        print(f"Efeitos: {item.get('efeitos')}")
    if item.get("descricao"):
        print(f"Descrição: {item.get('descricao')}")


def mostrar_consumiveis_disponiveis(estado: dict) -> list[tuple[int, dict]]:
    """Mostra apenas poções/consumíveis para uso por número."""
    consumiveis = [
        (indice, item)
        for indice, item in enumerate(estado["inventario"])
        if item.get("tipo") == "consumivel"
    ]

    print("\n=== USAR POÇÃO / CONSUMÍVEL ===")
    if not consumiveis:
        print("Nenhuma poção ou consumível no inventário.")
        return []

    for numero, (_, item) in enumerate(consumiveis, start=1):
        efeitos = item.get("efeitos", {})
        print(
            f"{numero} - {item['nome']} | "
            f"efeitos: {efeitos} | "
            f"descrição: {item.get('descricao', '')}"
        )
    print("0 - Cancelar")
    return consumiveis
