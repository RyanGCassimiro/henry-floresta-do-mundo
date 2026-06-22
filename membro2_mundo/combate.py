"""Membro 2 — Combate simples para gerar EXP e moedas.

Henry possui famílias de magias ofensivas:
- Fire → Fira → Firaga → Firaja
- Blizzard → Blizzara → Blizzaga → Blizzaja
- Thunder → Thundara → Thundaga → Thundaja
- Water → Watera → Waterga → Waterja
- Dark → Darkra → Darkga → Darkja

Mitis, o corujinha-buraqueira, possui:
- Quake → Quakera → Quakega → Quakeja
- Cure → Cura → Curaga → Curaja
- Esuna / Esunaga
- Haste → Hastera → Hastega
- Protect → Protectga
- Shell → Shellga
- Pena Envenenada como ataque físico básico do Mitis
"""
from __future__ import annotations

from copy import deepcopy
from contextlib import redirect_stdout
from io import StringIO

from membro2_mundo.locais import CRIATURAS_POR_LOCAL
from membro2_mundo.dados import aplicar_dado_luta
from membro2_mundo.progressao import (
    calcular_status_total,
    ganhar_exp,
    ganhar_exp_habilidades_usadas,
    garantir_estado_magias,
    nome_magia,
    registrar_uso_habilidade,
)
from membro3_inventario.inventory import listar_consumiveis_no_inventario, usar_consumivel_por_indice


MAGIAS_HENRY = {
    "fire": {
        "familia": "fire",
        "custo": 10,
        "multiplicador": 3,
        "descricao": "chamas mágicas",
    },
    "blizzard": {
        "familia": "blizzard",
        "custo": 9,
        "multiplicador": 3,
        "descricao": "gelo cortante",
    },
    "thunder": {
        "familia": "thunder",
        "custo": 12,
        "multiplicador": 4,
        "descricao": "raios concentrados",
    },
    "water": {
        "familia": "water",
        "custo": 10,
        "multiplicador": 3,
        "descricao": "correntezas mágicas",
    },
    "dark": {
        "familia": "dark",
        "custo": 14,
        "multiplicador": 4,
        "descricao": "energia sombria controlada",
    },
}


MENU_MAGIAS_HENRY = {
    "2": "fire",
    "3": "blizzard",
    "4": "thunder",
    "5": "water",
    "6": "dark",
}


MENU_MAGIAS_MITIS = {
    "7": "quake",
    "8": "cure",
    "9": "esuna",
    "10": "haste",
    "11": "protect",
    "12": "shell",
    "13": "mitis_penas",
}


def _barra(valor: int, maximo: int, largura: int = 10) -> str:
    """Cria barra simples de HP/MP para terminal."""
    maximo = max(1, int(maximo))
    valor = max(0, min(int(valor), maximo))
    preenchidos = round((valor / maximo) * largura)
    return "[" + ("#" * preenchidos) + ("-" * (largura - preenchidos)) + "]"


def _formatar_lista(valores: list[str]) -> str:
    return ", ".join(valores) if valores else "nenhuma"


def _capturar_saida(func, *args, **kwargs):
    """Executa uma ação antiga capturando prints para virar log resumido."""
    buffer = StringIO()
    with redirect_stdout(buffer):
        resultado = func(*args, **kwargs)
    texto = buffer.getvalue().strip()
    return resultado, texto or "A ação foi executada."


def mostrar_card_inimigo(inimigo: dict, contexto: str = "") -> None:
    """Mostra aparição do mob em bloco separado, sem arte ASCII."""
    titulo = contexto.upper() if contexto else "ENCONTRO"
    print("\n" + "=" * 56)
    print(f"{titulo:^56}")
    print("=" * 56)
    print("INIMIGO ENCONTRADO")
    print(f"Nome:        {inimigo.get('nome', '???')}")
    print(f"HP:          {inimigo.get('hp', 0)}")
    print(f"ATQ/DEF:     {inimigo.get('ataque', 0)} / {inimigo.get('defesa', 0)}")
    print(f"Fraquezas:   {_formatar_lista(inimigo.get('fraquezas', []))}")
    print(f"Resistência: {_formatar_lista(inimigo.get('resistencias', []))}")
    print("=" * 56)


def mostrar_hud_batalha(estado: dict, inimigo: dict, ultima_acao: str, turno: int, contexto: str = "") -> None:
    """HUD compacto da batalha."""
    status = calcular_status_total(estado)
    efeitos = estado.setdefault("efeitos_temporarios", {})
    hp_h = estado["status"].get("hp", 0)
    mp_h = estado["status"].get("mana", 0)
    hp_max_h = status.get("hp_max", 1)
    mp_max_h = status.get("mana_max", 1)
    hp_i = max(0, inimigo.get("hp", 0))
    hp_max_i = inimigo.get("hp_max", max(1, hp_i))

    print("\n" + "=" * 56)
    titulo = "BATALHA — HENRY" if estado.get("mitis_separado") else "BATALHA — HENRY & MITIS"
    print(titulo.center(56))
    if contexto:
        print(f"Local: {contexto} | Turno: {turno}")
    else:
        print(f"Turno: {turno}")
    print("=" * 56)
    print("GRUPO DO JOGADOR")
    print(f"Henry   HP: {_barra(hp_h, hp_max_h)} {hp_h}/{hp_max_h}")
    print(f"Mana    MP: {_barra(mp_h, mp_max_h)} {mp_h}/{mp_max_h}")
    print("-" * 56)
    print("INIMIGO")
    print(inimigo.get("nome", "???"))
    print(f"HP:     {_barra(hp_i, hp_max_i)} {hp_i}/{hp_max_i}")
    print(f"ATQ/DEF: {inimigo.get('ataque', 0)} / {inimigo.get('defesa', 0)}")
    print(f"Fraqueza: {_formatar_lista(inimigo.get('fraquezas', []))}")
    print(f"Resistência: {_formatar_lista(inimigo.get('resistencias', []))}")

    buffs = []
    for chave in ["haste", "protect", "shell", "veneno", "guarana_turnos"]:
        valor = efeitos.get(chave, 0)
        if valor:
            nome = "guaraná" if chave == "guarana_turnos" else chave
            buffs.append(f"{nome}:{valor}")
    if buffs:
        print("Efeitos: " + " | ".join(buffs))

    print("-" * 56)
    print("Última ação:")
    for linha in (ultima_acao or "A batalha começou.").splitlines()[-4:]:
        print(f"- {linha}")
    print("-" * 56)


def mostrar_menu_batalha(estado: dict) -> str:
    print("AÇÕES")
    print("1 - Ataque físico de Henry")
    print("2 - Magias de Henry")
    if estado.get("mitis_separado"):
        print("3 - Habilidades do Mitis (indisponível: Mitis está na toca)")
    else:
        print("3 - Habilidades do Mitis")
    print("4 - Usar poção/consumível")
    print("5 - Ver status detalhado")
    print("6 - Fugir")
    print("0 - Atualizar tela")
    return input("Escolha: ").strip()


def escolher_magia_henry(estado: dict) -> str | None:
    opcoes = ["fire", "blizzard", "thunder", "water", "dark"]
    print("\n=== MAGIAS DE HENRY ===")
    for i, chave in enumerate(opcoes, start=1):
        nivel = estado["habilidades"].get(chave, 0)
        custo = MAGIAS_HENRY[chave]["custo"] + (nivel * 3)
        print(f"{i} - {nome_magia(chave, nivel)} | MP {custo}")
    print("0 - Voltar")
    escolha = input("Magia: ").strip()
    if escolha == "0":
        return None
    if not escolha.isdigit() or not 1 <= int(escolha) <= len(opcoes):
        print("Opção inválida.")
        return None
    return opcoes[int(escolha) - 1]


def escolher_habilidade_mitis(estado: dict) -> str | None:
    opcoes = [
        ("mitis_penas", "ataque físico"),
        ("quake", "terra"),
        ("cure", "cura"),
        ("esuna", "remove status"),
        ("haste", "aceleração"),
        ("protect", "proteção física"),
        ("shell", "proteção mágica"),
    ]
    print("\n=== HABILIDADES DO MITIS ===")
    for i, (chave, desc) in enumerate(opcoes, start=1):
        nivel = estado["habilidades"].get(chave, 0)
        print(f"{i} - {nome_magia(chave, nivel)} | {desc}")
    print("0 - Voltar")
    escolha = input("Habilidade: ").strip()
    if escolha == "0":
        return None
    if not escolha.isdigit() or not 1 <= int(escolha) <= len(opcoes):
        print("Opção inválida.")
        return None
    return opcoes[int(escolha) - 1][0]


def usar_item_em_combate(estado: dict) -> tuple[bool, str]:
    consumiveis = listar_consumiveis_no_inventario(estado)
    if not consumiveis:
        return False, "Não há poções/consumíveis no inventário."

    print("\n=== POÇÕES / CONSUMÍVEIS ===")
    for pos, (_, item) in enumerate(consumiveis, start=1):
        print(f"{pos} - {item['nome']} | efeitos: {item.get('efeitos', {})}")
    print("0 - Cancelar")
    escolha_item = input("Escolha o número do consumível: ").strip()
    if escolha_item == "0":
        return False, "Uso de item cancelado."
    if not escolha_item.isdigit() or not 1 <= int(escolha_item) <= len(consumiveis):
        return False, "Opção inválida."

    indice_real, _ = consumiveis[int(escolha_item) - 1]
    _, log = _capturar_saida(usar_consumivel_por_indice, estado, indice_real)
    return True, log


def mostrar_status_detalhado(estado: dict, inimigo: dict) -> None:
    status = calcular_status_total(estado)
    print("\n=== STATUS DETALHADO ===")
    print("[HENRY]")
    print(f"Nível: {estado['status'].get('nivel', 1)} | EXP: {estado['status'].get('exp', 0)}/{estado['status'].get('exp_proximo', 0)}")
    print(f"HP: {estado['status'].get('hp', 0)}/{status.get('hp_max', 0)} | MP: {estado['status'].get('mana', 0)}/{status.get('mana_max', 0)}")
    print(f"ATQ: {status.get('ataque', 0)} | DEF: {status.get('defesa', 0)} | MAG: {status.get('magia', 0)}")
    print("\n[PROFICIÊNCIAS]")
    for chave in ["fire", "blizzard", "thunder", "water", "dark", "quake", "cure", "esuna", "haste", "protect", "shell", "mitis_penas"]:
        nivel = estado.get("habilidades", {}).get(chave, 0)
        print(f"- {chave}: {nome_magia(chave, nivel)}")
    print("\n[INIMIGO]")
    print(f"Nome: {inimigo.get('nome', '???')}")
    print(f"HP: {max(0, inimigo.get('hp', 0))}/{inimigo.get('hp_max', inimigo.get('hp', 0))}")
    print(f"ATQ: {inimigo.get('ataque', 0)} | DEF: {inimigo.get('defesa', 0)}")
    print(f"Fraquezas: {_formatar_lista(inimigo.get('fraquezas', []))}")
    print(f"Resistências: {_formatar_lista(inimigo.get('resistencias', []))}")
    input("Pressione ENTER para voltar à batalha...")


def _ataque_fisico_henry(estado: dict, inimigo: dict) -> bool:
    status = calcular_status_total(estado)
    efeitos = estado.setdefault("efeitos_temporarios", {})
    haste_bonus = 1.20 if efeitos.get("haste", 0) > 0 else 1.0
    dano = max(1, int((status["ataque"] + status.get("veneno", 0) // 5) * haste_bonus) - inimigo["defesa"])
    dano = aplicar_dado_luta(dano, atacante="Henry", minimo=0)
    inimigo["hp"] -= dano
    if dano > 0:
        print(f"Henry atacou fisicamente e causou {dano} de dano.")
    else:
        print("Henry errou o ataque físico.")
    return True


def _aplicar_multiplicador_elemental(dano: int, elemento: str, inimigo: dict) -> int:
    """Aumenta ou reduz dano conforme fraqueza/resistência do inimigo."""
    fraquezas = inimigo.get("fraquezas", [])
    resistencias = inimigo.get("resistencias", [])

    if elemento in fraquezas:
        dano = int(dano * 1.30)
        print("Fraqueza elemental ativada!")
    elif elemento in resistencias:
        dano = max(1, int(dano * 0.75))
        print("O inimigo resistiu parcialmente à magia.")

    return dano


def _lancar_magia_henry(estado: dict, inimigo: dict, elemento: str) -> bool:
    magia = MAGIAS_HENRY[elemento]
    status = calcular_status_total(estado)
    nivel_habilidade = estado["habilidades"].get(elemento, 0)
    custo = magia["custo"] + (nivel_habilidade * 3)

    if estado["status"]["mana"] < custo:
        print("Mana insuficiente.")
        return False

    estado["status"]["mana"] -= custo
    bonus_equipamento = status.get(elemento, 0)
    haste_bonus = 1.25 if estado.get("efeitos_temporarios", {}).get("haste", 0) > 0 else 1.0
    dano_base = status["magia"] + (nivel_habilidade * magia["multiplicador"]) + (bonus_equipamento * 2)
    dano = max(2, int(dano_base * haste_bonus) - inimigo["defesa"])
    dano = aplicar_dado_luta(dano, atacante="Henry", minimo=0)
    if dano > 0:
        dano = _aplicar_multiplicador_elemental(dano, elemento, inimigo)

    nome = nome_magia(elemento, nivel_habilidade)
    inimigo["hp"] -= dano
    registrar_uso_habilidade(estado, elemento)
    print(f"Henry lançou {nome} com {magia['descricao']} e causou {dano} de dano.")
    return True


def _mitis_quake(estado: dict, inimigo: dict) -> bool:
    nivel = estado["habilidades"].get("quake", 0)
    custo = 11 + (nivel * 3)
    if estado["status"]["mana"] < custo:
        print("Mana insuficiente para Mitis usar magia de terra.")
        return False

    estado["status"]["mana"] -= custo
    status = calcular_status_total(estado)
    bonus = status.get("quake", 0)
    dano = max(2, status["magia"] + (nivel * 4) + (bonus * 2) - (inimigo["defesa"] // 2))
    dano = aplicar_dado_luta(dano, atacante="Mitis", minimo=0)
    if dano > 0:
        dano = _aplicar_multiplicador_elemental(dano, "quake", inimigo)

    inimigo["hp"] -= dano
    registrar_uso_habilidade(estado, "quake")
    nome = nome_magia("quake", nivel)
    print(f"Mitis bate as asas contra o chão e conjura {nome}. Dano causado: {dano}.")
    return True


def _mitis_curar(estado: dict) -> bool:
    nivel = estado["habilidades"].get("cure", 0)
    custo = 8 + (nivel * 3)
    if estado["status"]["mana"] < custo:
        print("Mana insuficiente para Mitis curar.")
        return False

    estado["status"]["mana"] -= custo
    status = calcular_status_total(estado)
    bonus_cure = status.get("cure", 0)
    cura = 20 + (nivel * 14) + (status["magia"] // 2) + (bonus_cure * 4)
    estado["status"]["hp"] = min(status["hp_max"], estado["status"]["hp"] + cura)
    registrar_uso_habilidade(estado, "cure")
    nome = nome_magia("cure", nivel)
    print(f"Mitis conjurou {nome}. Henry recuperou {cura} HP.")
    print(f"HP atual: {estado['status']['hp']}/{status['hp_max']}")
    return True


def _mitis_esuna(estado: dict) -> bool:
    nivel = estado["habilidades"].get("esuna", 0)
    custo = 6 + (nivel * 2)
    if estado["status"]["mana"] < custo:
        print("Mana insuficiente para Esuna.")
        return False

    estado["status"]["mana"] -= custo
    efeitos = estado.setdefault("efeitos_temporarios", {})
    tinha_status = efeitos.get("veneno", 0) > 0
    efeitos["veneno"] = 0
    registrar_uso_habilidade(estado, "esuna")
    nome = nome_magia("esuna", nivel)
    if tinha_status:
        print(f"Mitis conjurou {nome}. O veneno em Henry foi removido.")
    else:
        print(f"Mitis conjurou {nome}. Não havia status negativo ativo.")
    return True


def _mitis_haste(estado: dict) -> bool:
    nivel = estado["habilidades"].get("haste", 0)
    custo = 10 + (nivel * 3)
    if estado["status"]["mana"] < custo:
        print("Mana insuficiente para Haste.")
        return False

    estado["status"]["mana"] -= custo
    status = calcular_status_total(estado)
    bonus = status.get("haste", 0)
    duracao = 2 + min(nivel, 2) + bonus
    estado.setdefault("efeitos_temporarios", {})["haste"] = max(estado["efeitos_temporarios"].get("haste", 0), duracao)
    registrar_uso_habilidade(estado, "haste")
    nome = nome_magia("haste", nivel)
    print(f"Mitis conjurou {nome}. Henry fica acelerado por {duracao} turno(s).")
    print("Enquanto Haste estiver ativo, as magias de Henry causam mais dano.")
    return True


def _mitis_protect(estado: dict) -> bool:
    nivel = estado["habilidades"].get("protect", 0)
    custo = 9 + (nivel * 3)
    if estado["status"]["mana"] < custo:
        print("Mana insuficiente para Protect.")
        return False

    estado["status"]["mana"] -= custo
    status = calcular_status_total(estado)
    bonus = status.get("protect", 0)
    duracao = 3 + min(nivel, 1) + bonus
    estado.setdefault("efeitos_temporarios", {})["protect"] = max(estado["efeitos_temporarios"].get("protect", 0), duracao)
    registrar_uso_habilidade(estado, "protect")
    nome = nome_magia("protect", nivel)
    print(f"Mitis conjurou {nome}. Dano físico recebido será reduzido por {duracao} turno(s).")
    return True


def _mitis_shell(estado: dict) -> bool:
    nivel = estado["habilidades"].get("shell", 0)
    custo = 9 + (nivel * 3)
    if estado["status"]["mana"] < custo:
        print("Mana insuficiente para Shell.")
        return False

    estado["status"]["mana"] -= custo
    status = calcular_status_total(estado)
    bonus = status.get("shell", 0)
    duracao = 3 + min(nivel, 1) + bonus
    estado.setdefault("efeitos_temporarios", {})["shell"] = max(estado["efeitos_temporarios"].get("shell", 0), duracao)
    registrar_uso_habilidade(estado, "shell")
    nome = nome_magia("shell", nivel)
    print(f"Mitis conjurou {nome}. Dano mágico/elemental será reduzido por {duracao} turno(s).")
    return True


def _mitis_penas_envenenadas(estado: dict, inimigo: dict) -> bool:
    """Ataque físico básico do Mitis.

    Diferente das magias, não gasta mana. A Pena Envenenada progride
    por proficiência de uso, igual às magias do Henry.
    """
    status = calcular_status_total(estado)
    nivel = estado["habilidades"].get("mitis_penas", 0)
    bonus_veneno = status.get("veneno", 0)
    haste_bonus = 1.15 if estado.get("efeitos_temporarios", {}).get("haste", 0) > 0 else 1.0
    dano_base = int((7 + (nivel * 2) + (bonus_veneno // 3)) * haste_bonus)
    dano = max(1, dano_base - inimigo["defesa"])
    dano = aplicar_dado_luta(dano, atacante="Mitis", minimo=0)

    inimigo["hp"] -= dano
    registrar_uso_habilidade(estado, "mitis_penas")
    nome = nome_magia("mitis_penas", nivel)
    if dano > 0:
        inimigo["veneno_turnos"] = max(inimigo.get("veneno_turnos", 0), 3)
        inimigo["veneno_dano"] = max(inimigo.get("veneno_dano", 0), 2 + nivel + (bonus_veneno // 5))
        print(f"Mitis atacou com {nome} e causou {dano} de dano físico.")
        print(f"O inimigo ficou envenenado por {inimigo['veneno_turnos']} turnos.")
    else:
        print(f"Mitis tentou usar {nome}, mas errou o alvo.")
    return True


def _aplicar_veneno_inimigo(inimigo: dict) -> None:
    if inimigo.get("veneno_turnos", 0) <= 0:
        return

    dano = inimigo.get("veneno_dano", 0)
    inimigo["hp"] -= dano
    inimigo["veneno_turnos"] -= 1
    print(f"O veneno das penas de Mitis causou {dano} de dano adicional.")


def _aplicar_status_henry(estado: dict) -> None:
    efeitos = estado.setdefault("efeitos_temporarios", {})
    if efeitos.get("veneno", 0) > 0:
        dano = 4
        estado["status"]["hp"] -= dano
        efeitos["veneno"] -= 1
        print(f"Henry sofreu {dano} de dano de veneno. Use Esuna para remover esse status.")

    if efeitos.get("guarana_turnos", 0) > 0:
        status_total = calcular_status_total(estado)
        hp_rec = int(efeitos.get("guarana_hp", 0))
        mana_rec = int(efeitos.get("guarana_mana", 0))
        estado["status"]["hp"] = min(status_total["hp_max"], estado["status"].get("hp", 0) + hp_rec)
        estado["status"]["mana"] = min(status_total["mana_max"], estado["status"].get("mana", 0) + mana_rec)
        efeitos["guarana_turnos"] -= 1
        print(
            "A Semente de Guaraná pulsa no corpo de Henry: "
            f"+{hp_rec} HP, +{mana_rec} mana "
            f"({efeitos['guarana_turnos']} turno(s) restante(s))."
        )
        if efeitos["guarana_turnos"] <= 0:
            efeitos["guarana_hp"] = 0
            efeitos["guarana_mana"] = 0
            print("O efeito da Semente de Guaraná acabou.")


def _reduzir_buffs(estado: dict) -> None:
    efeitos = estado.setdefault("efeitos_temporarios", {})
    for chave in ["haste", "protect", "shell"]:
        if efeitos.get(chave, 0) > 0:
            efeitos[chave] -= 1


def _ataque_inimigo(estado: dict, inimigo: dict) -> None:
    status = calcular_status_total(estado)
    reducao_grupo = estado["habilidades"].get("defesa", 0)
    dano_inimigo = max(1, inimigo["ataque"] - status["defesa"] - reducao_grupo)

    efeitos = estado.setdefault("efeitos_temporarios", {})
    if efeitos.get("protect", 0) > 0:
        dano_inimigo = max(1, int(dano_inimigo * 0.65))
    if inimigo.get("tipo_dano") == "magico" and efeitos.get("shell", 0) > 0:
        dano_inimigo = max(1, int(dano_inimigo * 0.65))

    dano_inimigo = aplicar_dado_luta(dano_inimigo, atacante=inimigo["nome"], minimo=0)
    estado["status"]["hp"] -= dano_inimigo
    if dano_inimigo > 0:
        print(f"{inimigo['nome']} causou {dano_inimigo} de dano em Henry.")
    else:
        print(f"{inimigo['nome']} errou o ataque.")

    # Alguns inimigos podem aplicar veneno simples para Esuna ter utilidade no MVP.
    if dano_inimigo > 0 and inimigo.get("aplica_veneno") and efeitos.get("veneno", 0) <= 0:
        efeitos["veneno"] = 3
        print(f"{inimigo['nome']} aplicou veneno em Henry!")


def iniciar_combate_no_local(estado: dict) -> None:
    garantir_estado_magias(estado)
    local = estado["local_atual"]
    inimigo_base = CRIATURAS_POR_LOCAL.get(local)

    if not inimigo_base:
        print(f"Não há criaturas hostis em {local}.")
        return

    iniciar_combate_contra(estado, inimigo_base, contexto=local)


def iniciar_combate_contra(estado: dict, inimigo_base: dict, contexto: str = "") -> bool:
    """Inicia combate contra um inimigo já montado.

    Versão compacta para terminal:
    - aparição do mob em card;
    - HUD com barras de HP/MP;
    - menu principal curto;
    - submenus para Henry, Mitis e itens;
    - log resumido da última ação.
    """
    garantir_estado_magias(estado)
    estado["ultimo_resultado_combate"] = "em_andamento"
    inimigo = deepcopy(inimigo_base)
    inimigo.setdefault("hp_max", inimigo.get("hp", 1))
    habilidades_usadas_combate: list[str] = []
    turno = 1
    ultima_acao = "A batalha começou."

    mostrar_card_inimigo(inimigo, contexto)

    while inimigo["hp"] > 0 and estado["status"]["hp"] > 0:
        mostrar_hud_batalha(estado, inimigo, ultima_acao, turno, contexto)
        escolha = mostrar_menu_batalha(estado)

        turno_valido = True
        habilidade_usada: str | None = None
        log_acao = ""

        if escolha == "0":
            ultima_acao = "Tela atualizada."
            continue
        if escolha == "1":
            turno_valido, log_acao = _capturar_saida(_ataque_fisico_henry, estado, inimigo)
        elif escolha == "2":
            habilidade = escolher_magia_henry(estado)
            if not habilidade:
                ultima_acao = "Henry reconsiderou a magia."
                continue
            turno_valido, log_acao = _capturar_saida(_lancar_magia_henry, estado, inimigo, habilidade)
            habilidade_usada = habilidade if turno_valido else None
        elif escolha == "3":
            if estado.get("mitis_separado"):
                ultima_acao = "Mitis está dentro da toca e não pode agir neste turno."
                continue

            habilidade = escolher_habilidade_mitis(estado)
            if not habilidade:
                ultima_acao = "Mitis aguardou a ordem de Henry."
                continue
            if habilidade == "quake":
                turno_valido, log_acao = _capturar_saida(_mitis_quake, estado, inimigo)
            elif habilidade == "cure":
                turno_valido, log_acao = _capturar_saida(_mitis_curar, estado)
            elif habilidade == "esuna":
                turno_valido, log_acao = _capturar_saida(_mitis_esuna, estado)
            elif habilidade == "haste":
                turno_valido, log_acao = _capturar_saida(_mitis_haste, estado)
            elif habilidade == "protect":
                turno_valido, log_acao = _capturar_saida(_mitis_protect, estado)
            elif habilidade == "shell":
                turno_valido, log_acao = _capturar_saida(_mitis_shell, estado)
            elif habilidade == "mitis_penas":
                turno_valido, log_acao = _capturar_saida(_mitis_penas_envenenadas, estado, inimigo)
            else:
                turno_valido = False
                log_acao = "Habilidade inválida."
            habilidade_usada = habilidade if turno_valido else None
        elif escolha == "4":
            turno_valido, log_acao = usar_item_em_combate(estado)
            if not turno_valido:
                ultima_acao = log_acao
                continue
        elif escolha == "5":
            mostrar_status_detalhado(estado, inimigo)
            ultima_acao = "Status detalhado consultado."
            continue
        elif escolha == "6":
            if estado.get("mitis_separado"):
                print("Henry fugiu do combate enquanto procurava o caminho de volta para Mitis.")
            else:
                print("Henry e Mitis fugiram do combate.")
            estado["ultimo_resultado_combate"] = "fuga"
            return False
        else:
            ultima_acao = "Ação inválida."
            continue

        if not turno_valido:
            ultima_acao = log_acao or "A ação não pôde ser executada."
            continue

        if habilidade_usada:
            habilidades_usadas_combate.append(habilidade_usada)

        _, log_veneno = _capturar_saida(_aplicar_veneno_inimigo, inimigo)
        logs_turno = [log_acao]
        if log_veneno and log_veneno != "A ação foi executada.":
            logs_turno.append(log_veneno)

        if inimigo["hp"] <= 0:
            print(f"{inimigo['nome']} foi derrotado!")
            derrotadas = estado.setdefault("criaturas_derrotadas", {})
            derrotadas[inimigo["nome"]] = derrotadas.get(inimigo["nome"], 0) + 1
            _, log_exp = _capturar_saida(ganhar_exp, estado, inimigo["exp"])
            _, log_skill = _capturar_saida(ganhar_exp_habilidades_usadas, estado, habilidades_usadas_combate, inimigo["exp"])
            estado["moedas"] += inimigo["moedas"]
            print(log_exp)
            if log_skill and log_skill != "A ação foi executada.":
                print(log_skill)
            print(f"Henry recebeu {inimigo['moedas']} moedas.")
            estado["ultimo_resultado_combate"] = "vitoria"
            return True

        _, log_inimigo = _capturar_saida(_ataque_inimigo, estado, inimigo)
        _, log_status = _capturar_saida(_aplicar_status_henry, estado)
        _reduzir_buffs(estado)
        logs_turno.append(log_inimigo)
        if log_status and log_status != "A ação foi executada.":
            logs_turno.append(log_status)
        ultima_acao = "\n".join([l for l in logs_turno if l and l.strip()])
        turno += 1

    if estado["status"]["hp"] <= 0:
        if estado.get("mitis_separado"):
            print("Henry caiu em combate, mas a Floresta Distorcida o expulsou para a Vila das Preguiças.")
        else:
            print("Henry caiu em combate, mas Mitis o levou de volta para a Vila das Preguiças.")
        estado["ultimo_resultado_combate"] = "derrota"
        estado["local_atual"] = "Vila das Preguiças"
        status_total = calcular_status_total(estado)
        estado["status"]["hp"] = max(1, status_total.get("hp_max", 100) // 2)
    elif estado.get("ultimo_resultado_combate") == "em_andamento":
        estado["ultimo_resultado_combate"] = "fuga"
    return False
