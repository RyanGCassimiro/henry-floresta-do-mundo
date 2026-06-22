# HENRY E A FLORESTA DO MUNDO — AVENTURA PELO TERMINAL

**Henry e a Floresta do Mundo** é um RPG de mesa textual em terminal, desenvolvido em Python para a atividade de **Modelagem de Dados e Laboratório de Análise de Algoritmo**.

Henry, um gato preto, viaja com Mitis, uma coruja-buraqueira, para recuperar fragmentos mágicos da **Árvore do Mundo**. Durante a jornada, o jogador explora locais, coleta itens, conversa com NPCs, enfrenta criaturas, organiza o inventário, calcula rotas, evolui habilidades e enfrenta eventos imprevisíveis dentro da Floresta Distorcida.

---

## Como rodar

Na raiz do projeto, execute:

```bash
python main.py
```

Em alguns sistemas, pode ser necessário usar:

```bash
python3 main.py
```

Não é necessário instalar bibliotecas externas.

---

## Como testar

Antes de executar ou subir alterações para o GitHub, recomenda-se rodar:

```bash
python -m compileall -q .
```

Depois:

```bash
python tests/smoke_test.py
```

Resultado esperado:

```txt
SMOKE_TEST_OK
```

---

## Requisitos atendidos

O projeto atende aos requisitos principais da atividade e adiciona mecânicas extras de RPG textual:

- **TSP** para calcular a melhor rota entre os locais da missão;
- **Inventário** como estrutura de dados;
- **Coleta narrativa de itens** nos locais do mapa, com pistas, escolhas e D20;
- **MergeSort** para ordenar o inventário;
- **Loja da Capivara** para compra e venda;
- **Conversas com NPCs**, incluindo rumores aleatórios da Capivara;
- **Poções de HP e mana**;
- **Equipamentos** com bônus de status e bônus elementais;
- **Combate** com magias de Henry e habilidades de Mitis;
- **HUD de batalha separado** entre grupo do jogador e inimigo;
- **Bloqueio das habilidades de Mitis** quando ele está separado de Henry;
- **Quests dos aliados**;
- **Santiago como tucano navegador**, liberado após cálculo da rota TSP;
- **Progressão por EXP**, level up e pontos de habilidade;
- **Floresta Distorcida**, dungeon paralela que muda a cada entrada;
- **Eventos narrativos na Floresta Distorcida**;
- **Acampamento com risco**, definido por D20;
- **Mobs escaláveis**, de acordo com o nível de Henry e a profundidade;
- **Save/load em JSON**.

---

## Melhorias de UX no terminal

Após a primeira versão, o menu principal foi reorganizado em submenus para reduzir a poluição visual. Também foram adicionados textos narrativos antes de ações importantes, separação visual no HUD de combate e eventos interativos na coleta e na Floresta Distorcida.

Essas mudanças tornam o terminal menos parecido com uma lista de comandos e mais próximo de uma experiência de RPG de mesa narrado.

---

## Menu principal

O menu principal foi dividido em categorias:

```txt
1 - Explorar
2 - Inventário
3 - Personagem
4 - Missões
5 - Sistema
0 - Sair
```

### Explorar

Inclui ver mapa, viajar para local, coletar item no local atual, enfrentar criatura do local, conversar com NPCs, entrar na Floresta Distorcida e acessar a Loja da Capivara.

### Inventário

Inclui ver inventário, ordenar com MergeSort, consultar item por número, usar consumível por número, equipar item e remover item.

### Personagem

Inclui ver status, treinar habilidades e acompanhar evolução.

### Missões

Inclui ver missão principal, calcular rota TSP e acessar quests dos aliados.

### Sistema

Inclui salvar jogo, carregar jogo e créditos.

---

## Personagens principais

### Henry

Henry é o protagonista do jogo. Ele é um gato preto que viaja pela floresta para investigar a febre mágica da Árvore do Mundo.

No MVP, Henry possui cinco famílias de magias ofensivas:

- **Fogo:** Fire → Fira → Firaga → Firaja;
- **Gelo:** Blizzard → Blizzara → Blizzaga → Blizzaja;
- **Trovão:** Thunder → Thundara → Thundaga → Thundaja;
- **Água:** Water → Watera → Waterga → Waterja;
- **Escuridão:** Dark → Darkra → Darkga → Darkja.

Essas magias usam mana do grupo e escalam com atributo de magia, nível da habilidade, bônus de equipamento e fraqueza ou resistência elemental do inimigo.

### Mitis

Mitis é a coruja-buraqueira que acompanha Henry. Ele atua como suporte, observador e mago de terra.

Suas principais habilidades são:

- **Terra:** Quake → Quakera → Quakega → Quakeja;
- **Cura:** Cure → Cura → Curaga → Curaja;
- **Remoção de status:** Esuna → Esunaga;
- **Tempo:** Haste → Hastera → Hastega;
- **Proteção física:** Protect → Protectga;
- **Proteção mágica:** Shell → Shellga;
- **Especial:** penas envenenadas, que causam dano inicial e veneno por turnos.

---

## Como a evolução das magias funciona

Ao subir de nível, os status base aumentam automaticamente por porcentagem, Henry ganha pontos de habilidade, os pontos podem ser gastos em famílias de magia e as habilidades também podem evoluir por uso.

Cada família possui subníveis antes de trocar para a próxima magia.

Exemplo:

```txt
fire nível 0 → Fire
fire nível 1 → Fire I
fire nível 2 → Fire II
fire nível 3 → Fire III
fire nível 4 → Fira
```

A mesma lógica vale para Blizzard, Thunder, Water, Dark, Quake, Cure, Haste, Protect e Shell.

---

## Coleta narrativa

A coleta não mostra mais uma lista direta de itens disponíveis. Em vez disso, o jogo apresenta uma cena curta de exploração.

Exemplo:

```txt
Há um arbusto de formato estranho perto da trilha.
Mitis observa o lugar com atenção.

Deseja verificar o arbusto?
1 - Sim
2 - Não
```

Se Henry investigar, uma rolagem de D20 decide o resultado:

```txt
20    → encontra item e moedas
12-19 → encontra item
8-11  → nada útil acontece
1-7   → Henry sofre uma consequência e perde HP
```

Os eventos podem envolver arbustos estranhos, pedras fora do padrão, flores desconhecidas, árvores frutíferas, terra molhada ou revirada, desenhos antigos e runas estranhas.

Essa mudança transforma a coleta em uma decisão de risco e recompensa, aproximando o sistema de um RPG de mesa.

---

## Floresta Distorcida

A **Floresta Distorcida** é uma dungeon dinâmica. Ela muda a cada entrada e cada sala sorteia um trecho da floresta, um arquétipo de mob, fraquezas, resistências, recompensas e eventos especiais.

Os mobs escalam com o nível atual de Henry, a profundidade da exploração, o tipo de criatura e o elemento do trecho.

Além do combate normal, a Floresta pode disparar eventos narrativos.

### Eventos narrativos da Floresta

#### Pedra Estranha

Henry e Mitis encontram uma pedra ou parede marcada por símbolos estranhos. O jogador pode investigar. Dependendo do D20, pode encontrar fragmentos, moedas ou sofrer dano.

#### Voz Distorcida

Mitis escuta uma voz que Henry não percebe.

```txt
Mitis: "Henry... você está escutando essa voz?"
Henry: "Que voz?"
```

O jogador pode seguir a voz ou ignorá-la. A rolagem pode gerar item, recuperação de mana ou dano.

#### Chão Desaparece

Durante a exploração, o chão some sob Henry e Mitis. Dependendo da rolagem de reflexo, eles podem escapar, sofrer dano ou voltar para o início da dungeon.

#### Toca de Mitis

Mitis encontra uma toca e, por ser uma coruja-buraqueira, sente-se intrigado. Se o jogador permitir, Mitis entra na toca enquanto Henry fica do lado de fora enfrentando monstros sozinho.

Durante esse evento, Mitis investiga raízes, runas e um altar antigo; Henry enfrenta combates sem poder usar as habilidades de Mitis; a HUD informa que Mitis está indisponível; o altar exige interpretação das runas e uso de magia de Terra; e, ao final, Mitis abre um novo caminho e retorna para Henry.

#### Acampamento

Depois de vencer uma sala da Floresta, o jogador pode escolher acampar antes de continuar.

O descanso usa D20:

```txt
20    → descanso perfeito, restaura HP e mana, concede fruta especial
15-19 → bom descanso, recupera parte de HP e mana
8-14  → descanso ruim, recupera pouco e pode aplicar penalidade
1-7   → emboscada de monstros
```

Se o dado for máximo, a floresta parece recompensar a bravura do grupo, permitindo um descanso tranquilo e oferecendo frutas para consumo.

Depois de vencer uma sala, o jogador pode escolher:

```txt
1 - Continuar mais fundo
2 - Acampar antes de continuar
3 - Sair da Floresta Distorcida
```

---

## HUD de batalha

O combate foi reorganizado para separar visualmente o grupo do jogador e o inimigo.

A tela de batalha diferencia:

```txt
GRUPO DO JOGADOR
Henry HP / Mana

INIMIGO
Nome, HP, ATQ/DEF, fraquezas e resistências
```

Quando Mitis está separado, como no evento da toca, a batalha aparece como Henry sozinho e a opção de habilidades de Mitis fica bloqueada.

---

## Quests dos aliados

O MVP possui quests associadas aos personagens aliados:

- **Camila, tamanduá-bandeira:** quest no Bosque do Ipê envolvendo a Flor de Ipê e as formigas luminosas;
- **Eduardo, jaguatirica:** quest nas Ruínas da Arpia envolvendo investigação e combate contra a Pena Sombria;
- **Monique, tatu-bola:** quest na Caverna dos Golems envolvendo defesa e resistência;
- **Pietra, onça-pintada:** quest na Clareira da Árvore do Mundo para testar a evolução de Henry;
- **Santiago, tucano navegador:** quest na Vila das Preguiças que exige calcular a rota principal com TSP para liberar Santiago como navegador;
- **Beatriz, boto-cor-de-rosa:** quest no Lago das Capivaras envolvendo a Canção das Águas e a busca pela Pérola Furta-cor em trechos aquáticos raros da Floresta Distorcida.

---

## Quest da Beatriz — A Canção das Águas

Beatriz é uma boto-cor-de-rosa localizada no Lago das Capivaras. Sua quest gira em torno da **Canção das Águas**, uma magia antiga ligada à proteção das águas doces da floresta.

A Canção das Águas se cristalizou em uma **Pérola Furta-cor**, perdida dentro da Floresta Distorcida. Diferente de outros itens de quest, a Pérola não aparece em um local fixo. Ela depende de eventos e trechos aquáticos raros da dungeon, usando probabilidade para tornar a busca mais imprevisível.

Essa quest integra narrativa, exploração, aleatoriedade, recompensa rara e ligação temática com a preservação das águas doces.

---

## Algoritmos

### TSP

O **TSP — Travelling Salesman Problem** é usado para calcular a menor rota da missão principal.

Complexidade da abordagem por força bruta:

```txt
O(n!)
```

No jogo, a rota calculada funciona como orientação estratégica. O jogador pode explorar livremente, mas o sistema demonstra qual seria o caminho mais eficiente para cumprir a missão.

### MergeSort

O **MergeSort** é usado para ordenar o inventário por nome, peso, raridade, valor mágico ou preço.

Complexidade:

```txt
O(n log n)
```

### Dados estilo RPG de mesa

O MVP usa rolagens de **D20** em diferentes situações:

- **Dado de Mobilidade:** usado em viagens e ao avançar na Floresta Distorcida;
- **Dado de Luta:** usado em ataques físicos, magias ofensivas, Quake, penas do Mitis e ataques dos mobs;
- **Dado de Investigação:** usado na coleta narrativa, eventos de runas, pedras, arbustos, tocas e locais suspeitos;
- **Dado de Acampamento:** usado para decidir se o descanso foi tranquilo, parcial ou se gerou emboscada.

As rolagens podem gerar falha crítica, falha parcial, sucesso, sucesso alto ou crítico, dependendo da situação.

---

## Estrutura do projeto

```txt
.
├── main.py
├── game.py
├── README.md
├── membro1_tsp/
│   ├── mapa.py
│   ├── tsp.py
│   ├── quest.py
│   ├── tela_inicial.py
│   └── creditos.py
├── membro2_mundo/
│   ├── coleta.py
│   ├── combate.py
│   ├── dados.py
│   ├── dialogos_npcs.py
│   ├── dialogos_henry_mitis.py
│   ├── floresta_distorcida.py
│   ├── locais.py
│   ├── loja_capivara.py
│   ├── progressao.py
│   ├── quests_personagens.py
│   └── sorting.py
├── membro3_inventario/
│   ├── inventory.py
│   ├── inventario_ui.py
│   └── save_manager.py
└── tests/
    └── smoke_test.py
```

---

## Divisão por membros

### Membro 1 — Wanessa

Responsável por TSP, mapa textual, missão principal, tela inicial e créditos.

### Membro 2 — Ryan

Responsável por locais, coleta, MergeSort, loja, combate, progressão, D20, Floresta Distorcida, quests, diálogos de NPCs, eventos narrativos, Beatriz e Pérola Furta-cor.

### Membro 3 — Santiago

Responsável por inventário, interface textual do inventário, consumíveis, equipamentos, consulta de item por número, salvar e carregar jogo.

---

## Checklist rápido de validação

Antes de entregar ou abrir Pull Request:

```bash
python -m compileall -q .
python tests/smoke_test.py
python main.py
```

Teste manual sugerido:

1. Abrir o jogo;
2. Escolher Novo jogo;
3. Entrar em Explorar;
4. Viajar para outro local;
5. Testar coleta narrativa;
6. Ver inventário;
7. Ordenar inventário;
8. Conversar com NPC;
9. Testar rumores da Capivara;
10. Entrar na Floresta Distorcida;
11. Vencer uma sala;
12. Testar acampamento;
13. Salvar jogo.

---

## Conclusão

**Henry e a Floresta do Mundo** transforma os requisitos acadêmicos de algoritmos em mecânicas jogáveis. O TSP orienta a missão principal, o MergeSort organiza o inventário, a coleta narrativa incentiva exploração, o D20 cria incerteza controlada e a Floresta Distorcida adiciona eventos probabilísticos e escolhas de risco.

O resultado é um RPG textual executável pelo terminal, organizado por módulos e conectado à narrativa dos personagens.
