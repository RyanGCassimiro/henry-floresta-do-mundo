import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import patch

from membro1_tsp.mapa import MAPA_DISTANCIAS
from membro1_tsp.quest import MISSAO_PRINCIPAL
from membro1_tsp.tsp import calcular_melhor_rota
from membro2_mundo.sorting import merge_sort_itens
from membro2_mundo.progressao import ganhar_exp, garantir_estado_magias, nome_magia
from membro2_mundo.dados import aplicar_dado_luta, aplicar_teste_mobilidade
from membro2_mundo.locais import ITENS_POR_LOCAL
from membro2_mundo.coleta import coletar_item_no_local
from membro2_mundo.combate import iniciar_combate_contra
from membro2_mundo.floresta_distorcida import garantir_estado_dungeon, gerar_criatura_distorcida
from membro3_inventario.inventory import criar_estado_inicial, adicionar_item, consultar_item, equipar_item, usar_consumivel
from membro3_inventario.save_manager import salvar_jogo, carregar_jogo

estado = criar_estado_inicial()
garantir_estado_magias(estado)
garantir_estado_dungeon(estado)

# TSP
rota, dist = calcular_melhor_rota(MISSAO_PRINCIPAL['local_inicial'], MISSAO_PRINCIPAL['locais_obrigatorios'], MAPA_DISTANCIAS)
assert rota[0] == MISSAO_PRINCIPAL['local_inicial'] and rota[-1] == MISSAO_PRINCIPAL['local_inicial']
assert dist < float('inf')

# Inventário + MergeSort
capa = next(item for item in ITENS_POR_LOCAL['Bosque do Ipê'] if item['nome'] == 'Capa de Ipê Roxo')
adicionar_item(estado, capa.copy())
assert consultar_item(estado, 'Capa de Ipê Roxo') is not None
ordenado = merge_sort_itens(estado['inventario'], 'valor_magico')
assert [i['valor_magico'] for i in ordenado] == sorted(i['valor_magico'] for i in ordenado)
assert equipar_item(estado, 'Capa de Ipê Roxo') is True

# Consumível
estado['status']['hp'] = 50
assert usar_consumivel(estado, 'Poção Pequena de HP') is True
assert estado['status']['hp'] > 50

# Progressão + magia tier
estado['status']['exp'] = 0
ganhar_exp(estado, 60)
assert estado['status']['nivel'] >= 2
estado['habilidades']['fire'] = 2
assert nome_magia('fire', 2) == 'Fire II'

# Dados
with patch('membro2_mundo.dados.rolar_d20', return_value=20):
    assert aplicar_dado_luta(10, 'Teste', minimo=0) >= 19
    aplicar_teste_mobilidade(estado, 'A', 'B', 10)

# Coleta com input
estado['local_atual'] = 'Lago das Capivaras'
anel_vitoria = next(item for item in ITENS_POR_LOCAL['Lago das Capivaras'] if item['nome'] == 'Anel de Vitória-régia')
evento_coleta = {
    'pista': 'Teste de coleta narrativa.',
    'pergunta': 'Investigar?',
    'sucesso': 'Item encontrado no teste.',
    'falha': 'Falha no teste.',
    'ignorar': 'Ignorado no teste.',
}
with patch('builtins.input', return_value='1'), \
     patch('membro2_mundo.coleta.choice', side_effect=[evento_coleta, anel_vitoria]), \
     patch('membro2_mundo.coleta.rolar_d20', return_value=16):
    coletar_item_no_local(estado)
assert any(i['nome'] == 'Anel de Vitória-régia' for i in estado['inventario'])

# Combate: fugir não dá recompensa
estado['status']['hp'] = estado['status']['hp_max']
moedas_antes = estado['moedas']
inimigo_fraco = {'nome':'Teste Fraco','hp':5,'ataque':1,'defesa':0,'exp':1,'moedas':999,'fraquezas':[],'resistencias':[],'tipo_dano':'fisico'}
with patch('builtins.input', return_value='6'):
    venceu = iniciar_combate_contra(estado, inimigo_fraco, contexto='teste')
assert venceu is False
assert estado['moedas'] == moedas_antes

# Combate: ataque vencedor
with patch('builtins.input', return_value='1'), patch('membro2_mundo.dados.rolar_d20', return_value=20):
    venceu = iniciar_combate_contra(estado, inimigo_fraco, contexto='teste')
assert venceu is True

# Dungeon gera criatura escalável
criatura = gerar_criatura_distorcida(estado, profundidade=2)
for campo in ['nome','hp','ataque','defesa','exp','moedas','fraquezas']:
    assert campo in criatura

# Save/load
save_path = Path('save_test.json')
salvar_jogo(estado, save_path)
carregado = carregar_jogo(save_path)
assert carregado['jogador'] == 'Henry'
save_path.unlink(missing_ok=True)

print('SMOKE_TEST_OK')
