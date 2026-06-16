"""Membro 1 — Missão principal conectada ao TSP."""

MISSAO_PRINCIPAL = {
    "nome": "Fragmentos da Árvore do Mundo",
    "local_inicial": "Vila das Preguiças",
    "locais_obrigatorios": [
        "Bosque do Ipê",
        "Lago das Capivaras",
        "Ruínas da Arpia",
        "Caverna dos Golems",
    ],
    "objetivo": "Visitar os locais, coletar fragmentos e voltar antes que o portal feche.",
}

def mostrar_missao() -> None:
    print("\n=== MISSÃO PRINCIPAL ===")
    print(f"Nome: {MISSAO_PRINCIPAL['nome']}")
    print(f"Objetivo: {MISSAO_PRINCIPAL['objetivo']}")
    print("\nLocais obrigatórios:")
    for local in MISSAO_PRINCIPAL["locais_obrigatorios"]:
        print(f"- {local}")
    print("\nJustificativa do TSP:")
    print("A energia do portal é limitada. Henry e Mitis precisam visitar todos")
    print("os pontos pelo menor caminho possível para economizar a mana restante.")
