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
