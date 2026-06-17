"""Diálogos contextuais de Henry e Mitis.

Responsável: Membro 2
Função:
- Exibir falas curtas entre Henry e Mitis em momentos importantes;
- Reforçar a narrativa do jogo;
- Dar personalidade aos personagens durante exploração, NPCs e dungeon.
"""

from __future__ import annotations

from random import choice


DIALOGOS_ENTRADA_LOCAL = {
    "Vila das Preguiças": [
        ("Henry", "A vila parece calma... calma até demais."),
        ("Mitis", "Preguiças guardiãs não têm pressa, Henry. Mas elas sempre percebem tudo."),
    ],
    "Lago das Capivaras": [
        ("Henry", "A água daqui é bastante cristalina ebrilha diferente... será que consigo pegar um peixe?"),
        ("Mitis", "É magia de água doce. Melhor falar baixo... o lago escuta."),
    ],
    "Bosque do Ipê": [
        ("Henry", "Olha Mitis! as flores parecem iluminar o caminho."),
        ("Mitis", "O Ipê guarda memórias antigas e as vezes alergia..."),
    ],
    "Ruínas da Arpia": [
        ("Henry", "Sinto que alguém já esteve aqui antes de nós."),
        ("Mitis", "As ruínas lembram até daquilo que os vivos esqueceram."),
    ],
    "Caverna dos Golems": [
        ("Henry", "Esse lugar parece respirar pedra."),
        ("Mitis", "Golems não gostam de visitas. Principalmente barulhentas."),
    ],
    "Clareira da Árvore do Mundo": [
        ("Henry", "Então é daqui que a febre começou..."),
        ("Mitis", "A Árvore ainda está viva. Mas está sonhando com dor."),
    ],
}


DIALOGOS_SAIDA_LOCAL = {
    "Vila das Preguiças": [
        ("Mitis", "A vila ficou para trás, mas os olhos das guardiãs ainda nos seguem."),
        ("Henry", "Isso deveria me deixar mais tranquilo ou mais preocupado?"),
    ],
    "Lago das Capivaras": [
        ("Henry", "A água parou de brilhar quando saímos."),
        ("Mitis", "Talvez ela só esteja esperando a gente voltar."),
    ],
    "Bosque do Ipê": [
        ("Mitis", "Leve o cheiro das flores com você. Ele espanta pensamentos ruins."),
        ("Henry", "Vou tentar lembrar disso se um golem correr atrás da gente."),
    ],
    "Ruínas da Arpia": [
        ("Henry", "Não gosto de virar as costas para ruínas."),
        ("Mitis", "Então ande rápido. Algumas memórias gostam de seguir viajantes."),
    ],
    "Caverna dos Golems": [
        ("Henry", "Finalmente ar puro."),
        ("Mitis", "E menos pedra tentando nos esmagar. Eu aprovo."),
    ],
    "Clareira da Árvore do Mundo": [
        ("Henry", "Prometo que vamos dar um jeito nisso."),
        ("Mitis", "Promessas feitas diante da Árvore criam raízes."),
    ],
}


DIALOGOS_NPC = {
    "Capivara Mercadora": [
        ("Henry", "Ela parece saber mais do que vende."),
        ("Mitis", "Capivaras sempre sabem. Só cobram em moedas, rumores ou paciência."),
    ],
    "Beatriz": [
        ("Henry", "A Beatriz fala baixinho, mas parece carregar um rio inteiro por dentro."),
        ("Mitis", "Algumas águas são tímidas até chegar a tempestade."),
    ],
    "Camila": [
        ("Henry", "Uau! a Camila transforma qualquer coisa em recurso útil."),
        ("Mitis", "Isso se chama talento. Ou sobrevivência com estilo."),
    ],
    "Santiago": [
        ("Henry", "O Santiago fala como se o céu fosse um mapa."),
        ("Mitis", "Para um tucano navegador, talvez seja mesmo."),
    ],
    "Pietra": [
        ("Henry", "A Pietra me olha como se soubesse se estou pronto ou não."),
        ("Mitis", "Ela sabe."),
    ],
}


DIALOGOS_FLORESTA_DISTORCIDA = [
    ("Henry", "Esse caminho não estava aqui antes."),
    ("Mitis", "Na Floresta Distorcida, caminhos são como as raízes da própria árvore do mundo."),

    ("Henry", "Oh Mitis, acho que aquela árvore piscou..."),
    ("Mitis", "Se ela piscar de novo, não pisque de volta ;) ."),

    ("Henry", "Está tudo se movendo... ou sou eu?"),
    ("Mitis", "Os dois. Péssima combinação."),

    ("Henry", "Mitis, você também ouviu essa música?"),
    ("Mitis", "Ouvi. E ela não veio de garganta nenhuma."),
]


DIALOGOS_PEROLA_FURTA_COR = [
    ("Henry", "Mitis, que bruxaria é essa?! A-aquela pérola... ela está cantando?"),
    ("Mitis", "Não é uma pérola comum. É a Canção das Águas recitando suas memórias mais preciosas."),
]


def mostrar_dialogo_linhas(falas: list[tuple[str, str]]) -> None:
    """Mostra falas no terminal."""
    print()
    for personagem, fala in falas:
        print(f"{personagem}: {fala}")


def dialogo_entrada_local(local: str) -> None:
    """Mostra diálogo ao entrar em um local."""
    falas = DIALOGOS_ENTRADA_LOCAL.get(local)
    if falas:
        mostrar_dialogo_linhas(falas)


def dialogo_saida_local(local: str) -> None:
    """Mostra diálogo ao sair de um local."""
    falas = DIALOGOS_SAIDA_LOCAL.get(local)
    if falas:
        mostrar_dialogo_linhas(falas)


def dialogo_apos_npc(nome_npc: str) -> None:
    """Mostra comentário de Henry e Mitis após falar com um NPC."""
    falas = DIALOGOS_NPC.get(nome_npc)
    if falas:
        mostrar_dialogo_linhas(falas)


def dialogo_floresta_distorcida() -> None:
    """Mostra diálogo aleatório ao entrar/avançar na Floresta Distorcida."""
    indice = choice(range(0, len(DIALOGOS_FLORESTA_DISTORCIDA), 2))
    mostrar_dialogo_linhas([
        DIALOGOS_FLORESTA_DISTORCIDA[indice],
        DIALOGOS_FLORESTA_DISTORCIDA[indice + 1],
    ])


def dialogo_perola_furta_cor() -> None:
    """Mostra fala especial ao encontrar a Pérola Furta-cor."""
    mostrar_dialogo_linhas(DIALOGOS_PEROLA_FURTA_COR)