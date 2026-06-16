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

from membro2_mundo.coleta import coletar_item_no_local
from membro2_mundo.combate import iniciar_combate_no_local
from membro2_mundo.loja_capivara import abrir_loja_capivara
from membro2_mundo.floresta_distorcida import explorar_floresta_distorcida, garantir_estado_dungeon
from membro2_mundo.progressao import mostrar_status, gastar_ponto_habilidade, garantir_estado_magias
from membro2_mundo.quests_personagens import abrir_quests_personagens, garantir_estado_quests
from membro2_mundo.sorting import merge_sort_itens
from membro2_mundo.dados import aplicar_teste_mobilidade

from membro3_inventario.inventory import (
    criar_estado_inicial,
    consultar_item,
    equipar_item,
    remover_item,
    usar_consumivel,
)
from membro3_inventario.inventario_ui import mostrar_inventario, mostrar_equipamentos
from membro3_inventario.save_manager import carregar_jogo, salvar_jogo


def pausar() -> None:
    input("\nPressione ENTER para continuar...")

def titulo() -> None:
    print("=" * 60)
    print("HENRY E A FLORESTA DO MUNDO - AVENTURA PELO TERMINAL")
    print("=" * 60)
    print("Henry viaja pelo mundo com Mitis, o corujinha-buraqueira.")
    print("A Árvore do Mundo perdeu fragmentos de seiva mágica.")
    print("Use rotas, itens, habilidades e estratégia para restaurar a floresta.")

def menu() -> None:
    print("\n=== MENU PRINCIPAL ===")
    print("1  - Ver missão")
    print("2  - Ver mapa")
    print("3  - Calcular melhor rota com TSP")
    print("4  - Viajar para local")
    print("5  - Coletar item no local atual")
    print("6  - Enfrentar criatura do local")
    print("7  - Loja da Capivara")
    print("8  - Ver inventário")
    print("9  - Ordenar inventário com MergeSort")
    print("10 - Consultar item")
    print("11 - Usar poção/consumível")
    print("12 - Equipar item")
    print("13 - Remover item")
    print("14 - Ver status e habilidades")
    print("15 - Gastar ponto de habilidade")
    print("16 - Salvar jogo")
    print("17 - Carregar jogo")
    print("18 - Quests dos aliados")
    print("19 - Entrar na Floresta Distorcida")
    print("0  - Sair")

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

    estado["local_atual"] = destino
    print(f"\nHenry e Mitis viajaram de {origem} para {destino}.")
    print(f"Distância percorrida: {distancia}")

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

def calcular_rota_tsp() -> None:
    inicio = MISSAO_PRINCIPAL["local_inicial"]
    obrigatorios = MISSAO_PRINCIPAL["locais_obrigatorios"]
    rota, distancia = calcular_melhor_rota(inicio, obrigatorios, MAPA_DISTANCIAS)
    print("\n=== ROTA ÓTIMA DA MISSÃO ===")
    print(" -> ".join(rota))
    print(f"Distância total: {distancia}")

def iniciar_jogo() -> None:
    estado = criar_estado_inicial()
    garantir_estado_magias(estado)
    garantir_estado_quests(estado)
    garantir_estado_dungeon(estado)
    titulo()

    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            mostrar_missao()
            pausar()
        elif opcao == "2":
            mostrar_mapa()
            pausar()
        elif opcao == "3":
            calcular_rota_tsp()
            estado["rota_tsp_calculada"] = True
            pausar()
        elif opcao == "4":
            escolher_local(estado)
            pausar()
        elif opcao == "5":
            coletar_item_no_local(estado)
            pausar()
        elif opcao == "6":
            iniciar_combate_no_local(estado)
            pausar()
        elif opcao == "7":
            abrir_loja_capivara(estado)
            pausar()
        elif opcao == "8":
            mostrar_inventario(estado)
            mostrar_equipamentos(estado)
            pausar()
        elif opcao == "9":
            ordenar_inventario(estado)
            pausar()
        elif opcao == "10":
            nome = input("Nome do item para consultar: ")
            item = consultar_item(estado, nome)
            if item:
                print(item)
            else:
                print("Item não encontrado.")
            pausar()
        elif opcao == "11":
            nome = input("Nome do consumível para usar: ")
            usar_consumivel(estado, nome)
            pausar()
        elif opcao == "12":
            nome = input("Nome do equipamento para equipar: ")
            equipar_item(estado, nome)
            pausar()
        elif opcao == "13":
            nome = input("Nome do item para remover: ")
            remover_item(estado, nome)
            pausar()
        elif opcao == "14":
            mostrar_status(estado)
            pausar()
        elif opcao == "15":
            gastar_ponto_habilidade(estado)
            pausar()
        elif opcao == "16":
            salvar_jogo(estado)
            pausar()
        elif opcao == "17":
            carregado = carregar_jogo()
            if carregado:
                estado = carregado
                garantir_estado_magias(estado)
                garantir_estado_quests(estado)
                garantir_estado_dungeon(estado)
                print("Jogo carregado com sucesso.")
            pausar()
        elif opcao == "18":
            abrir_quests_personagens(estado)
            pausar()
        elif opcao == "19":
            explorar_floresta_distorcida(estado)
            pausar()
        elif opcao == "0":
            print("Até a próxima aventura de Henry e Mitis!")
            break
        else:
            print("Opção inválida.")
            pausar()
