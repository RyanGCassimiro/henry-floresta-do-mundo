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
- Penas envenenadas como habilidade especial
"""
from __future__ import annotations

from copy import deepcopy

from membro2_mundo.locais import CRIATURAS_POR_LOCAL
from membro2_mundo.dados import aplicar_dado_luta
from membro2_mundo.progressao import (
    calcular_status_total,
    ganhar_exp,
    garantir_estado_magias,
    nome_magia,
)
from membro3_inventario.inventory import usar_consumivel


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
    nome = nome_magia("shell", nivel)
    print(f"Mitis conjurou {nome}. Dano mágico/elemental será reduzido por {duracao} turno(s).")
    return True


def _mitis_penas_envenenadas(estado: dict, inimigo: dict) -> bool:
    custo = 7
    if estado["status"]["mana"] < custo:
        print("Mana insuficiente para as penas envenenadas de Mitis.")
        return False

    estado["status"]["mana"] -= custo
    status = calcular_status_total(estado)
    nivel = estado["habilidades"].get("mitis_penas", 0)
    bonus_veneno = status.get("veneno", 0)
    dano = max(2, 6 + (nivel * 3) + (bonus_veneno // 3) - inimigo["defesa"])
    dano = aplicar_dado_luta(dano, atacante="Mitis", minimo=0)

    inimigo["hp"] -= dano
    if dano > 0:
        inimigo["veneno_turnos"] = max(inimigo.get("veneno_turnos", 0), 3)
        inimigo["veneno_dano"] = max(inimigo.get("veneno_dano", 0), 3 + nivel + (bonus_veneno // 5))
        print(f"Mitis lançou penas envenenadas e causou {dano} de dano inicial.")
        print(f"O inimigo ficou envenenado por {inimigo['veneno_turnos']} turnos.")
    else:
        print("As penas de Mitis erraram o alvo e não aplicaram veneno.")
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

    Esta função permite reaproveitar o combate dos locais fixos
    também na Floresta Distorcida, onde os mobs são gerados dinamicamente.
    """
    garantir_estado_magias(estado)
    inimigo = deepcopy(inimigo_base)
    if contexto:
        print(f"\nUm {inimigo['nome']} apareceu em {contexto}!")
    else:
        print(f"\nUm {inimigo['nome']} apareceu!")

    while inimigo["hp"] > 0 and estado["status"]["hp"] > 0:
        status = calcular_status_total(estado)
        efeitos = estado.setdefault("efeitos_temporarios", {})
        print(f"\nHenry HP: {estado['status']['hp']}/{status['hp_max']} | Mana: {estado['status']['mana']}/{status['mana_max']}")
        print(f"Buffs: Haste {efeitos.get('haste', 0)} | Protect {efeitos.get('protect', 0)} | Shell {efeitos.get('shell', 0)} | Veneno {efeitos.get('veneno', 0)}")
        print(f"{inimigo['nome']} HP: {inimigo['hp']}")
        print("1  - Ataque físico de Henry")
        print(f"2  - Henry: {nome_magia('fire', estado['habilidades'].get('fire', 0))}")
        print(f"3  - Henry: {nome_magia('blizzard', estado['habilidades'].get('blizzard', 0))}")
        print(f"4  - Henry: {nome_magia('thunder', estado['habilidades'].get('thunder', 0))}")
        print(f"5  - Henry: {nome_magia('water', estado['habilidades'].get('water', 0))}")
        print(f"6  - Henry: {nome_magia('dark', estado['habilidades'].get('dark', 0))}")
        print(f"7  - Mitis: {nome_magia('quake', estado['habilidades'].get('quake', 0))}")
        print(f"8  - Mitis: {nome_magia('cure', estado['habilidades'].get('cure', 0))}")
        print(f"9  - Mitis: {nome_magia('esuna', estado['habilidades'].get('esuna', 0))}")
        print(f"10 - Mitis: {nome_magia('haste', estado['habilidades'].get('haste', 0))}")
        print(f"11 - Mitis: {nome_magia('protect', estado['habilidades'].get('protect', 0))}")
        print(f"12 - Mitis: {nome_magia('shell', estado['habilidades'].get('shell', 0))}")
        print("13 - Mitis: penas envenenadas")
        print("14 - Usar poção/consumível")
        print("15 - Fugir")
        escolha = input("Ação: ").strip()

        turno_valido = True
        if escolha == "1":
            haste_bonus = 1.20 if efeitos.get("haste", 0) > 0 else 1.0
            dano = max(1, int((status["ataque"] + status.get("veneno", 0) // 5) * haste_bonus) - inimigo["defesa"])
            dano = aplicar_dado_luta(dano, atacante="Henry", minimo=0)
            inimigo["hp"] -= dano
            if dano > 0:
                print(f"Henry atacou fisicamente e causou {dano} de dano.")
            else:
                print("Henry errou o ataque físico.")
        elif escolha in MENU_MAGIAS_HENRY:
            turno_valido = _lancar_magia_henry(estado, inimigo, MENU_MAGIAS_HENRY[escolha])
        elif escolha == "7":
            turno_valido = _mitis_quake(estado, inimigo)
        elif escolha == "8":
            turno_valido = _mitis_curar(estado)
        elif escolha == "9":
            turno_valido = _mitis_esuna(estado)
        elif escolha == "10":
            turno_valido = _mitis_haste(estado)
        elif escolha == "11":
            turno_valido = _mitis_protect(estado)
        elif escolha == "12":
            turno_valido = _mitis_shell(estado)
        elif escolha == "13":
            turno_valido = _mitis_penas_envenenadas(estado, inimigo)
        elif escolha == "14":
            nome = input("Nome da poção/consumível: ")
            usar_consumivel(estado, nome)
            continue
        elif escolha == "15":
            print("Henry e Mitis fugiram do combate.")
            return False
        else:
            print("Ação inválida.")
            continue

        if not turno_valido:
            continue

        _aplicar_veneno_inimigo(inimigo)

        if inimigo["hp"] <= 0:
            print(f"{inimigo['nome']} foi derrotado!")
            derrotadas = estado.setdefault("criaturas_derrotadas", {})
            derrotadas[inimigo["nome"]] = derrotadas.get(inimigo["nome"], 0) + 1
            ganhar_exp(estado, inimigo["exp"])
            estado["moedas"] += inimigo["moedas"]
            print(f"Henry recebeu {inimigo['moedas']} moedas.")
            return True

        _ataque_inimigo(estado, inimigo)
        _aplicar_status_henry(estado)
        _reduzir_buffs(estado)

    if estado["status"]["hp"] <= 0:
        print("Henry caiu em combate, mas Mitis o levou de volta para a Vila das Preguiças.")
        estado["local_atual"] = "Vila das Preguiças"
        estado["status"]["hp"] = max(1, estado["status"].get("hp_max", 100) // 2)
    return False
