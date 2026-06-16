# HENRY E A FLORESTA DO MUNDO - AVENTURA PELO TERMINAL

RPG de mesa textual em terminal feito para a atividade **Modelagem de Dados e Laboratório de Análise de Algorítmo**.

Henry viaja pelo mundo com **Mitis**, para recuperar fragmentos mágicos da Árvore do Mundo.

## Como rodar

```bash
python main.py
```

Não precisa instalar bibliotecas externas.

## Requisitos atendidos

- TSP para calcular a melhor rota entre os locais da missão.
- Inventário como estrutura de dados.
- Coleta de itens nos locais do mapa.
- MergeSort para ordenar o inventário.
- Loja da Capivara para compra e venda.
- Poções de HP e mana.
- Equipamentos com bônus de status e bônus elementais.
- Combate com magias de Henry e habilidades de Mitis.
- Quests dos aliados: Camila, Eduardo, Monique, Pietra e Santiago.
- Santiago como tucano navegador, liberado após cálculo da rota TSP.
- Progressão por EXP, level up e pontos de habilidade.
- Floresta Distorcida: dungeon paralela que muda a cada entrada.
- Save/load em JSON.
- Dungeon dinâmica: Floresta Distorcida, com salas aleatórias e mobs que escalam com o nível de Henry.

## Personagens principais

### Henry

Henry é o protagonista. No MVP, ele possui cinco famílias de magias ofensivas:

- **Fogo:** Fire → Fira → Firaga → Firaja.
- **Gelo:** Blizzard → Blizzara → Blizzaga → Blizzaja.
- **Trovão:** Thunder → Thundara → Thundaga → Thundaja.
- **Água:** Water → Watera → Waterga → Waterja.
- **Escuridão:** Dark → Darkra → Darkga → Darkja.

Essas magias usam mana do grupo e escalam com:

- atributo `magia`;
- nível da habilidade;
- bônus de equipamento;
- fraqueza ou resistência elemental do inimigo.

### Mitis

Mitis é o corujinha-buraqueira que acompanha Henry. Ele atua como suporte e mago de terra:

- **Terra:** Quake → Quakera → Quakega → Quakeja.
- **Cura:** Cure → Cura → Curaga → Curaja.
- **Remoção de status:** Esuna → Esunaga.
- **Tempo:** Haste → Hastera → Hastega.
- **Proteção física:** Protect → Protectga.
- **Proteção mágica:** Shell → Shellga.
- **Especial:** penas envenenadas, que causam dano inicial e veneno por turnos.

## Como a evolução das magias funciona

Ao subir de nível:

- os status base aumentam automaticamente por porcentagem;
- Henry ganha pontos de habilidade;
- os pontos podem ser gastos em famílias de magia.

Exemplo:

```txt
fire nível 0 → Fire
fire nível 1 → Fira
fire nível 2 → Firaga
fire nível 3 ou mais → Firaja
```

A mesma regra vale para Blizzard, Thunder, Water, Dark, Quake, Cure, Haste, Protect e Shell.

## Floresta Distorcida

A Floresta Distorcida é uma dungeon. Ela muda a cada entrada e cada sala sorteia:

- um trecho da floresta;
- um arquétipo de mob;
- fraquezas e resistências elementais;
- recompensas possíveis.

Os mobs escalam com o nível de Henry e com a profundidade da exploração.

## Quests dos aliados

O MVP também possui um menu de quests dos personagens aliados:

- **Camila**, tamanduá-bandeira: quest no Bosque do Ipê envolvendo a Flor de Ipê e as formigas luminosas.
- **Eduardo**, jaguatirica: quest nas Ruínas da Arpia envolvendo investigação e combate contra a Pena Sombria.
- **Monique**, tatu-bola: quest na Caverna dos Golems envolvendo defesa e resistência.
- **Pietra**, onça-pintada: quest na Clareira da Árvore do Mundo para testar a evolução de Henry.
- **Santiago**, tucano navegador: quest na Vila das Preguiças que exige calcular a rota principal com TSP para liberar Santiago como navegador.

## Algoritmos

### TSP

Usado para calcular a menor rota da missão.
Complexidade da abordagem por força bruta:
```txt
O(n!)
```

### MergeSort

Usado para ordenar o inventário por nome, peso, raridade, valor mágico ou preço.
Complexidade:
```txt
O(n log n)
```

## Dados estilo RPG de mesa
O MVP agora usa dois testes simples com D20:
- **Dado de Mobilidade:** usado em viagens e ao avançar na Floresta Distorcida. A rolagem pode gerar atalho, perda de HP, recuperação de mana ou bônus de moedas.
- **Dado de Luta:** usado em ataques físicos, magias ofensivas de Henry, Quake/penas do Mitis e ataques dos mobs. A rolagem pode gerar falha crítica, golpe fraco, golpe normal, golpe forte ou crítico.
