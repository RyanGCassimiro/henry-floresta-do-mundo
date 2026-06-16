"""Membro 2 — Progressão de nível, EXP e habilidades.

Regra do MVP:
- Matar criaturas gera EXP.
- Subir de nível aumenta os status base por porcentagem equilibrada.
- Pontos ganhos no level up são usados para aumentar famílias de magia.
- Henry possui magias elementais ofensivas em tiers clássicos.
- Mitis possui terra, cura, suporte e penas envenenadas como habilidade especial.
"""

FAMILIAS_MAGIAS = {
    # Henry
    "fire": ["Fire", "Fira", "Firaga", "Firaja"],
    "blizzard": ["Blizzard", "Blizzara", "Blizzaga", "Blizzaja"],
    "thunder": ["Thunder", "Thundara", "Thundaga", "Thundaja"],
    "water": ["Water", "Watera", "Waterga", "Waterja"],
    "dark": ["Dark", "Darkra", "Darkga", "Darkja"],

    # Mitis
    "quake": ["Quake", "Quakera", "Quakega", "Quakeja"],
    "cure": ["Cure", "Cura", "Curaga", "Curaja"],
    "esuna": ["Esuna", "Esunaga"],
    "haste": ["Haste", "Hastera", "Hastega"],
    "protect": ["Protect", "Protectga"],
    "shell": ["Shell", "Shellga"],
}

HABILIDADES_VALIDAS = {
    "fire": "Henry usa magia de fogo: Fire → Fira → Firaga → Firaja.",
    "blizzard": "Henry usa magia de gelo: Blizzard → Blizzara → Blizzaga → Blizzaja.",
    "thunder": "Henry usa magia de trovão: Thunder → Thundara → Thundaga → Thundaja.",
    "water": "Henry usa magia de água: Water → Watera → Waterga → Waterja.",
    "dark": "Henry usa magia de escuridão: Dark → Darkra → Darkga → Darkja.",
    "quake": "Mitis usa magia de terra: Quake → Quakera → Quakega → Quakeja.",
    "cure": "Mitis usa cura: Cure → Cura → Curaga → Curaja.",
    "esuna": "Mitis remove status negativos: Esuna ou Esunaga.",
    "haste": "Mitis acelera Henry: Haste → Hastera → Hastega.",
    "protect": "Mitis reduz dano físico recebido: Protect → Protectga.",
    "shell": "Mitis reduz dano mágico/elemental recebido: Shell → Shellga.",
    "mitis_penas": "Mitis lança penas envenenadas que causam dano e veneno por turnos.",
    "defesa": "Aumenta a resistência geral do grupo contra dano recebido.",
}

GRUPOS_HABILIDADES = {
    "Henry — Magias elementais": ["fire", "blizzard", "thunder", "water", "dark"],
    "Mitis — Terra, cura e suporte": ["quake", "cure", "esuna", "haste", "protect", "shell", "mitis_penas"],
    "Defesa do grupo": ["defesa"],
}


def nome_magia(chave: str, nivel: int) -> str:
    """Retorna o nome da magia conforme o nível da habilidade.

    Nível 0 usa a primeira magia da família.
    Nível 1 usa a segunda.
    Nível 2 usa a terceira.
    Nível 3 ou mais usa a quarta, quando existir.
    """
    familia = FAMILIAS_MAGIAS.get(chave)
    if not familia:
        return chave
    indice = min(max(nivel, 0), len(familia) - 1)
    return familia[indice]


def proximo_nome_magia(chave: str, nivel: int) -> str:
    familia = FAMILIAS_MAGIAS.get(chave)
    if not familia:
        return chave
    indice = min(nivel + 1, len(familia) - 1)
    return familia[indice]


def calcular_status_total(estado: dict) -> dict:
    """Soma status base + bônus de equipamentos."""
    total = estado["status"].copy()
    for item in estado["equipamentos"].values():
        if not item:
            continue
        for atributo, valor in item.get("efeitos", {}).items():
            if atributo in total:
                total[atributo] += valor
    return total


def garantir_estado_magias(estado: dict) -> None:
    """Garante compatibilidade caso um save antigo seja carregado."""
    habilidades = estado.setdefault("habilidades", {})
    for chave in HABILIDADES_VALIDAS:
        habilidades.setdefault(chave, 0)

    status = estado.setdefault("status", {})
    for chave in ["fire", "blizzard", "thunder", "water", "dark", "quake", "cure", "esuna", "haste", "protect", "shell", "veneno"]:
        status.setdefault(chave, 0)

    estado.setdefault("efeitos_temporarios", {})
    estado["efeitos_temporarios"].setdefault("haste", 0)
    estado["efeitos_temporarios"].setdefault("protect", 0)
    estado["efeitos_temporarios"].setdefault("shell", 0)
    estado["efeitos_temporarios"].setdefault("veneno", 0)


def ganhar_exp(estado: dict, quantidade: int) -> None:
    garantir_estado_magias(estado)
    status = estado["status"]
    status["exp"] += quantidade
    print(f"Henry ganhou {quantidade} EXP.")

    while status["exp"] >= status["exp_proximo"]:
        status["exp"] -= status["exp_proximo"]
        subir_nivel(estado)


def subir_nivel(estado: dict) -> None:
    garantir_estado_magias(estado)
    status = estado["status"]
    status["nivel"] += 1

    # Aumento equilibrado por porcentagem aproximada.
    # O level up melhora os status automaticamente.
    # Os pontos de habilidade ficam separados para evoluir magias.
    status["hp_max"] = int(status["hp_max"] * 1.10)
    status["mana_max"] = int(status["mana_max"] * 1.08)
    status["ataque"] = int(status["ataque"] * 1.07) + 1
    status["defesa"] = int(status["defesa"] * 1.06) + 1
    status["magia"] = int(status["magia"] * 1.08) + 1
    status["exp_proximo"] = int(status["exp_proximo"] * 1.35)
    status["skill_points"] += 2

    # Restaura HP e mana considerando bônus de equipamentos ativos.
    status_total = calcular_status_total(estado)
    status["hp"] = status_total["hp_max"]
    status["mana"] = status_total["mana_max"]

    print("\n*** LEVEL UP! ***")
    print(f"Henry chegou ao nível {status['nivel']}.")
    print("Status base aumentaram de forma equilibrada.")
    print("+2 pontos de habilidade disponíveis para evoluir magias de Henry ou Mitis.")


def mostrar_status(estado: dict) -> None:
    garantir_estado_magias(estado)
    status_total = calcular_status_total(estado)
    base = estado["status"]
    print("\n=== STATUS DE HENRY E MITIS ===")
    print(f"Jogador: {estado['jogador']}")
    print(f"Companheiro: {estado['companheiro']}")
    print(f"Nível: {base['nivel']} | EXP: {base['exp']}/{base['exp_proximo']}")
    print(f"HP: {base['hp']}/{status_total['hp_max']}")
    print(f"Mana do grupo: {base['mana']}/{status_total['mana_max']}")
    print(f"Ataque físico: {status_total['ataque']}")
    print(f"Defesa: {status_total['defesa']}")
    print(f"Magia base: {status_total['magia']}")
    print(f"Moedas: {estado['moedas']}")
    print(f"Pontos de habilidade: {base['skill_points']}")

    print("\nBônus elementais/equipamentos:")
    for chave in ["fire", "blizzard", "thunder", "water", "dark", "quake", "cure", "haste", "protect", "shell", "veneno"]:
        print(f"- {chave}: {status_total.get(chave, 0)}")

    print("\nEfeitos temporários:")
    efeitos = estado.get("efeitos_temporarios", {})
    print(f"- Haste: {efeitos.get('haste', 0)} turno(s)")
    print(f"- Protect: {efeitos.get('protect', 0)} turno(s)")
    print(f"- Shell: {efeitos.get('shell', 0)} turno(s)")
    print(f"- Veneno em Henry: {efeitos.get('veneno', 0)} turno(s)")

    for grupo, nomes in GRUPOS_HABILIDADES.items():
        print(f"\n{grupo}:")
        for chave in nomes:
            nivel = estado["habilidades"].get(chave, 0)
            atual = nome_magia(chave, nivel)
            print(f"- {chave}: nível {nivel} | atual: {atual}")


def gastar_ponto_habilidade(estado: dict) -> None:
    garantir_estado_magias(estado)
    if estado["status"]["skill_points"] <= 0:
        print("Henry não possui pontos de habilidade disponíveis.")
        return

    print("\n=== AUMENTAR HABILIDADE ===")
    print("Pontos podem evoluir magias de Henry ou habilidades de Mitis.")
    for grupo, nomes in GRUPOS_HABILIDADES.items():
        print(f"\n{grupo}:")
        for nome in nomes:
            nivel = estado["habilidades"].get(nome, 0)
            descricao = HABILIDADES_VALIDAS[nome]
            atual = nome_magia(nome, nivel)
            prox = proximo_nome_magia(nome, nivel)
            print(f"- {nome} | nível {nivel} | atual: {atual} | próximo: {prox} | {descricao}")

    escolha = input("Digite o nome da habilidade: ").strip().lower()
    if escolha not in HABILIDADES_VALIDAS:
        print("Habilidade inválida.")
        return

    estado["habilidades"][escolha] += 1
    estado["status"]["skill_points"] -= 1
    nivel = estado["habilidades"][escolha]
    print(f"Habilidade {escolha} aumentou para nível {nivel}.")
    print(f"Magia atual: {nome_magia(escolha, nivel)}")
