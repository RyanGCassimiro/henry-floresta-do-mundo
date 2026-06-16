"""Membro 2 — Coleta de itens nos locais."""
from membro2_mundo.locais import ITENS_POR_LOCAL
from membro3_inventario.inventory import adicionar_item


def coletar_item_no_local(estado: dict) -> None:
    local = estado["local_atual"]
    itens = ITENS_POR_LOCAL.get(local, [])

    if not itens:
        print(f"Não há itens disponíveis em {local}.")
        return

    print(f"\n=== ITENS EM {local.upper()} ===")
    for i, item in enumerate(itens, start=1):
        print(f"{i} - {item['nome']} | {item['descricao']}")

    try:
        escolha = int(input("Escolha um item para coletar: "))
        item = itens[escolha - 1]
    except (ValueError, IndexError):
        print("Escolha inválida.")
        return

    chave_coletado = f"{local}:{item['nome']}"
    if chave_coletado in estado["itens_coletados"]:
        print("Esse item já foi coletado neste local.")
        return

    adicionar_item(estado, item.copy())
    estado["itens_coletados"].append(chave_coletado)
    print(f"Henry coletou: {item['nome']}")
