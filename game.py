"""
Junção daas partes dos três membros:
- Wanessa: TSP, mapa e missão.
- Ryan: locais, coleta, MergeSort, loja, combate e progressão.
- Santiago: inventário, interface textual e salvamento.
"""
from __future__ import annotations

from membro1_tsp.mapa import MAPA_DISTANCIAS, listar_locais, mostrar_mapa
from membro1_tsp.quest import MISSAO_PRINCIPAL, mostrar_missao
from membro1_tsp.tsp import calcular_melhor_rota
from membro1_tsp.tela_inicial import mostrar_tela_inicial, menu_tela_inicial
from membro1_tsp.creditos import mostrar_creditos

from membro2_mundo.coleta import coletar_item_no_local
from membro2_mundo.combate import iniciar_combate_no_local
from membro2_mundo.loja_capivara import abrir_loja_capivara
from membro2_mundo.floresta_distorcida import explorar_floresta_distorcida, garantir_estado_dungeon
from membro2_mundo.progressao import mostrar_status, gastar_ponto_habilidade, garantir_estado_magias
from membro2_mundo.quests_personagens import abrir_quests_personagens, garantir_estado_quests
from membro2_mundo.dialogos_npcs import abrir_dialogos_local
from membro2_mundo.sorting import merge_sort_itens
from membro2_mundo.dados import aplicar_teste_mobilidade
from membro2_mundo.dialogos_henry_mitis import (
    dialogo_entrada_local,
    dialogo_saida_local,
)


from membro3_inventario.inventory import (
    criar_estado_inicial,
    consultar_item,
    consultar_item_por_indice,
    equipar_item_por_indice,
    remover_item,
    usar_consumivel,
    usar_consumivel_por_indice,
)
from membro3_inventario.inventario_ui import (
    mostrar_inventario,
    mostrar_equipamentos,
    mostrar_equipamentos_disponiveis,
    mostrar_itens_para_consulta,
    mostrar_detalhes_item,
    mostrar_consumiveis_disponiveis,
)
from membro3_inventario.save_manager import salvar_jogo, carregar_jogo


def pausar() -> None:
    input("\nPressione ENTER para continuar...")

def mostrar_cabecalho_estado(estado: dict) -> None:
    """Mostra um cabeçalho fixo para orientar o jogador."""
    status = estado.get("status", {})
    local = estado.get("local_atual", "Local desconhecido")
    hp = status.get("hp", 0)
    hp_max = status.get("hp_max", hp)
    mana = status.get("mana", 0)
    mana_max = status.get("mana_max", mana)
    moedas = estado.get("moedas", 0)

    print("\n" + "=" * 60)
    print("HENRY E A FLORESTA DO MUNDO".center(60))
    print("=" * 60)
    print(f"Local atual: {local}")
    print(f"HP: {hp}/{hp_max} | Mana: {mana}/{mana_max} | Moedas: {moedas}")
    print("Objetivo: recuperar fragmentos da Árvore do Mundo")
    print("=" * 60)


def titulo() -> None:
    """Exibe a tela inicial do jogo.

    A tela inicial fica como atribuição do Membro 1, pois apresenta
    a missão principal e prepara o uso do mapa/TSP dentro da narrativa.
    """

def menu() -> None:
    print("\n=== MENU PRINCIPAL ===")
    print("1 - Explorar")
    print("2 - Inventário")
    print("3 - Personagem")
    print("4 - Missões")
    print("5 - Sistema")
    print("0 - Sair")
def menu_explorar() -> None:
    print("\n=== EXPLORAR ===")
    print("1 - Ver mapa")
    print("2 - Viajar para local")
    print("3 - Coletar item no local atual")
    print("4 - Enfrentar criatura do local")
    print("5 - Conversar com NPCs do local")
    print("6 - Entrar na Floresta Distorcida")
    print("7 - Loja da Capivara")
    print("0 - Voltar")


def menu_inventario() -> None:
    print("\n=== INVENTÁRIO ===")
    print("1 - Ver inventário")
    print("2 - Ordenar inventário com MergeSort")
    print("3 - Consultar item por número")
    print("4 - Usar poção/consumível por número")
    print("5 - Equipar item")
    print("6 - Remover item")
    print("0 - Voltar")


def menu_personagem() -> None:
    print("\n=== PERSONAGEM ===")
    print("1 - Ver status e habilidades")
    print("2 - Treinar habilidade / ver evolução")
    print("0 - Voltar")


def menu_missoes() -> None:
    print("\n=== MISSÕES ===")
    print("1 - Ver missão principal")
    print("2 - Calcular melhor rota com TSP")
    print("3 - Quests dos aliados")
    print("0 - Voltar")


def menu_sistema() -> None:
    print("\n=== SISTEMA ===")
    print("1 - Salvar jogo")
    print("2 - Carregar jogo")
    print("3 - Créditos")
    print("0 - Voltar")

def escolher_local(estado: dict) -> None:
    locais = listar_locais()
    print("\n=== VIAJAR ===")
    for i, local in enumerate(locais, start=1):
        marcador = " <-- local atual" if local == estado["local_atual"] else ""
        print(f"{i} - {local}{marcador}")

    try:
        escolha = int(input("Escolha o destino: "))
        destino = locais[escolha - 1]
    except (ValueError, IndexError):
        print("Opção inválida.")
        return

    origem = estado["local_atual"]
    if destino == origem:
        print("Henry já está nesse local.")
        return

    distancia = MAPA_DISTANCIAS.get(origem, {}).get(destino)
    if distancia is None:
        print("Não existe caminho direto para esse local.")
        return

    dificuldade = 8 + max(1, distancia // 4)
    aplicar_teste_mobilidade(estado, origem, destino, dificuldade)

    dialogo_saida_local(origem)

    estado["local_atual"] = destino
    print(f"\nHenry e Mitis viajaram de {origem} para {destino}.")
    print(f"Distância percorrida: {distancia}")

    dialogo_entrada_local(destino)

def ordenar_inventario(estado: dict) -> None:
    if not estado["inventario"]:
        print("O inventário está vazio.")
        return

    print("\n=== ORDENAR INVENTÁRIO COM MERGESORT ===")
    print("1 - Nome")
    print("2 - Peso")
    print("3 - Raridade")
    print("4 - Valor mágico")
    print("5 - Preço")

    opcoes = {
        "1": "nome",
        "2": "peso",
        "3": "raridade",
        "4": "valor_magico",
        "5": "preco",
    }

    escolha = input("Escolha o critério: ").strip()
    chave = opcoes.get(escolha)

    if not chave:
        print("Critério inválido.")
        return

    estado["inventario"] = merge_sort_itens(estado["inventario"], chave)
    print(f"Inventário ordenado por {chave} usando MergeSort.")
    mostrar_inventario(estado)

def equipar_item_por_menu(estado: dict) -> None:
    """Permite equipar usando número, sem digitar nome exato do item."""
    equipamentos = mostrar_equipamentos_disponiveis(estado)
    if not equipamentos:
        return

    try:
        escolha = int(input("Escolha o número do equipamento, ou 0 para cancelar: ").strip())
    except ValueError:
        print("Opção inválida. Digite apenas o número do equipamento.")
        return

    if escolha == 0:
        print("Equipamento cancelado.")
        return

    if not 1 <= escolha <= len(equipamentos):
        print("Opção inválida.")
        return

    indice_real, _ = equipamentos[escolha - 1]
    equipar_item_por_indice(estado, indice_real)


def consultar_item_por_menu(estado: dict) -> None:
    """Consulta item por número para evitar digitar nome exato."""
    itens = mostrar_itens_para_consulta(estado)
    if not itens:
        return

    try:
        escolha = int(input("Escolha o número do item, ou 0 para cancelar: ").strip())
    except ValueError:
        print("Opção inválida. Digite apenas o número do item.")
        return

    if escolha == 0:
        print("Consulta cancelada.")
        return

    if not 1 <= escolha <= len(itens):
        print("Opção inválida.")
        return

    indice_real, _ = itens[escolha - 1]
    item = consultar_item_por_indice(estado, indice_real)
    if item:
        mostrar_detalhes_item(item)
    else:
        print("Item não encontrado.")


def usar_consumivel_por_menu(estado: dict) -> None:
    """Usa poção/consumível por número."""
    consumiveis = mostrar_consumiveis_disponiveis(estado)
    if not consumiveis:
        return

    try:
        escolha = int(input("Escolha o número do consumível, ou 0 para cancelar: ").strip())
    except ValueError:
        print("Opção inválida. Digite apenas o número do consumível.")
        return

    if escolha == 0:
        print("Uso de consumível cancelado.")
        return

    if not 1 <= escolha <= len(consumiveis):
        print("Opção inválida.")
        return

    indice_real, _ = consumiveis[escolha - 1]
    usar_consumivel_por_indice(estado, indice_real)


def calcular_rota_tsp() -> None:
    inicio = MISSAO_PRINCIPAL["local_inicial"]
    obrigatorios = MISSAO_PRINCIPAL["locais_obrigatorios"]
    rota, distancia = calcular_melhor_rota(inicio, obrigatorios, MAPA_DISTANCIAS)
    print("\n=== ROTA ÓTIMA DA MISSÃO ===")
    print(" -> ".join(rota))
    print(f"Distância total: {distancia}")

def iniciar_jogo() -> None:
    estado = criar_estado_inicial()
    # MENU_INICIAL_MEMBRO1
    while True:
        escolha_inicial = menu_tela_inicial()
        if escolha_inicial == "1":
            break
        if escolha_inicial == "2":
            try:
                estado_carregado = carregar_jogo()
                if estado_carregado:
                    print("\nJogo carregado com sucesso!")
                    estado = estado_carregado
                    break
                print("\nNenhum jogo salvo encontrado. Iniciando novo jogo.")
                break
            except Exception as erro:
                print(f"\nNão foi possível carregar o jogo: {erro}")
                input("Pressione ENTER para voltar à tela inicial...")
        elif escolha_inicial == "3":
            mostrar_creditos()
        elif escolha_inicial == "0":
            print("\nAté a próxima aventura!")
            return
    garantir_estado_magias(estado)
    garantir_estado_quests(estado)
    garantir_estado_dungeon(estado)
    titulo()

    while True:
        mostrar_cabecalho_estado(estado)
        menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            abrir_menu_explorar(estado)

        elif opcao == "2":
            abrir_menu_inventario(estado)

        elif opcao == "3":
            abrir_menu_personagem(estado)

        elif opcao == "4":
            abrir_menu_missoes(estado)

        elif opcao == "5":
            abrir_menu_sistema(estado)

        elif opcao == "0":
            print("Até a próxima aventura de Henry e Mitis!")
            break

        else:
            print("Opção inválida.")
            pausar()


def abrir_menu_explorar(estado: dict) -> None:
    while True:
        mostrar_cabecalho_estado(estado)
        menu_explorar()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            mostrar_mapa()
            pausar()
        elif opcao == "2":
            escolher_local(estado)
            pausar()
        elif opcao == "3":
            coletar_item_no_local(estado)
            pausar()
        elif opcao == "4":
            iniciar_combate_no_local(estado)
            pausar()
        elif opcao == "5":
            abrir_dialogos_local(estado)
            pausar()
        elif opcao == "6":
            explorar_floresta_distorcida(estado)
            pausar()
        elif opcao == "7":
            abrir_loja_capivara(estado)
            pausar()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")
            pausar()


def abrir_menu_inventario(estado: dict) -> None:
    while True:
        mostrar_cabecalho_estado(estado)
        menu_inventario()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            mostrar_inventario(estado)
            mostrar_equipamentos(estado)
            pausar()
        elif opcao == "2":
            ordenar_inventario(estado)
            pausar()
        elif opcao == "3":
            consultar_item_por_menu(estado)
            pausar()
        elif opcao == "4":
            usar_consumivel_por_menu(estado)
            pausar()
        elif opcao == "5":
            equipar_item_por_menu(estado)
            pausar()
        elif opcao == "6":
            nome = input("Nome do item para remover: ")
            remover_item(estado, nome)
            pausar()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")
            pausar()


def abrir_menu_personagem(estado: dict) -> None:
    while True:
        mostrar_cabecalho_estado(estado)
        menu_personagem()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            mostrar_status(estado)
            pausar()
        elif opcao == "2":
            gastar_ponto_habilidade(estado)
            pausar()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")
            pausar()


def abrir_menu_missoes(estado: dict) -> None:
    while True:
        mostrar_cabecalho_estado(estado)
        menu_missoes()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            mostrar_missao()
            pausar()
        elif opcao == "2":
            calcular_rota_tsp()
            estado["rota_tsp_calculada"] = True
            pausar()
        elif opcao == "3":
            abrir_quests_personagens(estado)
            pausar()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")
            pausar()


def abrir_menu_sistema(estado: dict) -> None:
    while True:
        mostrar_cabecalho_estado(estado)
        menu_sistema()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            salvar_jogo(estado)
            pausar()
        elif opcao == "2":
            carregado = carregar_jogo()
            if carregado:
                estado.clear()
                estado.update(carregado)
                garantir_estado_magias(estado)
                garantir_estado_quests(estado)
                garantir_estado_dungeon(estado)
                print("Jogo carregado com sucesso.")
            pausar()
        elif opcao == "3":
            mostrar_creditos()
            pausar()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")
            pausar()
