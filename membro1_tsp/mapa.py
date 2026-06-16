"""Membro 1 — Mapa textual e distâncias para o TSP."""

MAPA_DISTANCIAS = {
    "Vila das Preguiças": {
        "Lago das Capivaras": 8,
        "Bosque do Ipê": 5,
        "Ruínas da Arpia": 12,
        "Caverna dos Golems": 15,
        "Clareira da Árvore do Mundo": 10,
    },
    "Lago das Capivaras": {
        "Vila das Preguiças": 8,
        "Bosque do Ipê": 6,
        "Ruínas da Arpia": 7,
        "Caverna dos Golems": 13,
        "Clareira da Árvore do Mundo": 9,
    },
    "Bosque do Ipê": {
        "Vila das Preguiças": 5,
        "Lago das Capivaras": 6,
        "Ruínas da Arpia": 11,
        "Caverna dos Golems": 9,
        "Clareira da Árvore do Mundo": 4,
    },
    "Ruínas da Arpia": {
        "Vila das Preguiças": 12,
        "Lago das Capivaras": 7,
        "Bosque do Ipê": 11,
        "Caverna dos Golems": 6,
        "Clareira da Árvore do Mundo": 8,
    },
    "Caverna dos Golems": {
        "Vila das Preguiças": 15,
        "Lago das Capivaras": 13,
        "Bosque do Ipê": 9,
        "Ruínas da Arpia": 6,
        "Clareira da Árvore do Mundo": 7,
    },
    "Clareira da Árvore do Mundo": {
        "Vila das Preguiças": 10,
        "Lago das Capivaras": 9,
        "Bosque do Ipê": 4,
        "Ruínas da Arpia": 8,
        "Caverna dos Golems": 7,
    },
}


def listar_locais() -> list[str]:
    """Retorna os nomes dos locais do mapa."""
    return list(MAPA_DISTANCIAS.keys())


def mostrar_mapa() -> None:
    """Exibe o mapa textual com as distâncias."""
    print("\n=== MAPA DA FLORESTA ===")
    for origem, destinos in MAPA_DISTANCIAS.items():
        print(f"\n{origem}:")
        for destino, distancia in destinos.items():
            print(f"  -> {destino}: {distancia}")
