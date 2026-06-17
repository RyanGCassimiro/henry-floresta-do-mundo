# HENRY E A FLORESTA DO MUNDO — AVENTURA PELO TERMINAL

**Henry e a Floresta do Mundo** é um RPG de mesa textual em terminal, desenvolvido em Python para a atividade de **Modelagem de Dados e Laboratório de Análise de Algoritmo**.

O jogo acompanha **Henry**, um gato preto, e **Mitis**, um corujinha-buraqueira, em uma jornada para recuperar fragmentos mágicos da **Árvore do Mundo**. Durante a aventura, o jogador explora locais, coleta itens, conversa com NPCs, enfrenta criaturas, organiza o inventário, usa magias e resolve quests ligadas aos personagens aliados.

---

## 1. Como rodar

Na pasta raiz do projeto, execute:

```bash
python main.py
```

Em alguns sistemas, pode ser necessário usar:

```bash
python3 main.py
```

Não é necessário instalar bibliotecas externas.

---

## 2. Como testar

Antes de executar o jogo ou abrir Pull Request, recomenda-se rodar:

```bash
python -m compileall -q .
```

ou:

```bash
python3 -m compileall -q .
```

Também é possível rodar o teste básico do projeto:

```bash
python tests/smoke_test.py
```

ou:

```bash
python3 tests/smoke_test.py
```

Resultado esperado:

```txt
SMOKE_TEST_OK
```

---

## 3. Tela inicial

O jogo possui uma tela inicial com opções de abertura:

```txt
1 - Novo jogo
2 - Carregar
3 - Créditos
0 - Sair
```

Essa tela funciona antes do menu principal e foi criada para deixar o RPG mais organizado, simulando uma abertura de jogo.

---

## 4. Menu principal

Após iniciar ou carregar o jogo, o jogador acessa o menu principal:

```txt
1  - Ver missão
2  - Ver mapa
3  - Calcular melhor rota com TSP
4  - Viajar para local
5  - Coletar item no local atual
6  - Enfrentar criatura do local
7  - Loja da Capivara
8  - Ver inventário
9  - Ordenar inventário com MergeSort
10 - Consultar item por número
11 - Usar poção/consumível por número
12 - Equipar item
13 - Remover item
14 - Ver status e habilidades
15 - Treinar habilidade / ver evolução
16 - Salvar jogo
17 - Carregar jogo
18 - Quests dos aliados
19 - Entrar na Floresta Distorcida
20 - Conversar com NPCs do local
21 - Créditos
0  - Sair
```

---

## 5. Requisitos atendidos

O projeto atende aos requisitos principais da atividade:

- **TSP** para calcular a melhor rota entre os locais da missão;
- **Inventário** como estrutura de dados;
- **Coleta de itens** nos locais do mapa;
- **MergeSort** para ordenar o inventário;
- **Loja da Capivara** para compra e venda;
- **Poções de HP e mana**;
- **Equipamentos** com bônus de status e bônus elementais;
- **Combate** com magias de Henry e habilidades de Mitis;
- **Quests dos aliados**;
- **Santiago como tucano navegador**, liberado após cálculo da rota TSP;
- **Progressão por EXP**, level up e pontos de habilidade;
- **Proficiência de habilidades por uso**;
- **Floresta Distorcida**, uma dungeon paralela que muda a cada entrada;
- **Mobs escaláveis** de acordo com o nível de Henry e a profundidade;
- **Dados D20** para mobilidade e combate;
- **Eventos probabilísticos**, como a Pérola Furta-cor da Beatriz;
- **Diálogos de NPCs**;
- **Diálogos contextuais entre Henry e Mitis**;
- **Save/load em JSON**.

---

## 6. Personagens principais

### Henry

Henry é o protagonista do jogo. Ele é um gato preto que viaja pela floresta para investigar a febre mágica da Árvore do Mundo.

No MVP, Henry possui cinco famílias de magias ofensivas:

- **Fogo:** Fire → Fira → Firaga → Firaja;
- **Gelo:** Blizzard → Blizzara → Blizzaga → Blizzaja;
- **Trovão:** Thunder → Thundara → Thundaga → Thundaja;
- **Água:** Water → Watera → Waterga → Waterja;
- **Escuridão:** Dark → Darkra → Darkga → Darkja.

Essas magias usam mana do grupo e escalam com:

- atributo de magia;
- nível da habilidade;
- bônus de equipamento;
- fraqueza ou resistência elemental do inimigo.

### Mitis

Mitis é o corujinha-buraqueira que acompanha Henry. Ele atua como suporte, observador e mago de terra.

Suas principais habilidades são:

- **Terra:** Quake → Quakera → Quakega → Quakeja;
- **Cura:** Cure → Cura → Curaga → Curaja;
- **Remoção de status:** Esuna → Esunaga;
- **Tempo:** Haste → Hastera → Hastega;
- **Proteção física:** Protect → Protectga;
- **Proteção mágica:** Shell → Shellga;
- **Especial físico:** penas envenenadas, que causam dano inicial e veneno por turnos.

### Capivara Mercadora

NPC comerciante localizada no **Lago das Capivaras**. Ela permite comprar e vender itens, além de oferecer rumores sobre a floresta, quests e perigos.

### Camila

Tamanduá-bandeira ligada ao **Bosque do Ipê**. Sua quest envolve a Flor de Ipê e as formigas luminosas. Depois, Camila também atua como personagem ligada à criação/crafting de itens.

### Eduardo

Jaguatirica associada às **Ruínas da Arpia**. Sua quest envolve investigação e combate contra a Pena Sombria.

### Monique

Tatu-bola associada à **Caverna dos Golems**. Sua quest envolve defesa, resistência e confronto contra golems.

### Pietra

Onça-pintada guardiã, localizada na **Clareira da Árvore do Mundo**. Sua quest testa se Henry já evoluiu o suficiente para proteger a floresta.

### Santiago

Tucano navegador localizado na **Vila das Preguiças**. Sua quest exige calcular a rota principal com TSP. Após isso, Santiago passa a atuar como navegador do grupo.

### Beatriz

Beatriz é uma boto-cor-de-rosa simpática e tímida, localizada no **Lago das Capivaras**. Sua quest especial é **A Canção das Águas**, ligada à busca pela **Pérola Furta-cor**, um item mágico que ajuda a manter a pureza das águas doces.

---

## 7. Como a evolução das magias funciona

Ao subir de nível:

- os status base aumentam automaticamente;
- Henry ganha pontos de habilidade;
- as habilidades podem evoluir;
- magias e ações também podem melhorar por uso/proficiência.

Exemplo de evolução da família Fire:

```txt
fire nível 0 → Fire
fire nível 1 → Fira
fire nível 2 → Firaga
fire nível 3 ou mais → Firaja
```

A mesma lógica é aplicada para outras famílias, como Blizzard, Thunder, Water, Dark, Quake, Cure, Haste, Protect e Shell.

---

## 8. Floresta Distorcida

A **Floresta Distorcida** é uma dungeon dinâmica. Ela muda a cada entrada e cada sala sorteia:

- um trecho da floresta;
- um arquétipo de mob;
- fraquezas e resistências elementais;
- recompensas possíveis;
- eventos especiais.

Os mobs escalam com:

- nível atual de Henry;
- profundidade da exploração;
- tipo de criatura;
- elemento do trecho.

A Floresta Distorcida também possui eventos raros, como a possibilidade de encontrar a **Pérola Furta-cor**, item necessário para a quest da Beatriz.

---

## 9. Quest especial da Beatriz — A Canção das Águas

A quest da Beatriz é diferente das demais porque usa probabilidade.

Na história, a **Canção das Águas** era um item mágico entregue aos animais aquáticos de água doce para manter a pureza das águas. Essa canção se cristalizou em uma **Pérola Furta-cor**, que acabou perdida em algum nível aleatório da Floresta Distorcida.

A Pérola Furta-cor:

- aparece apenas em trechos aquáticos;
- possui baixa chance de ser encontrada;
- só aparece uma vez por jogo;
- é necessária para concluir a quest da Beatriz.

Essa quest adiciona uma mecânica de exploração, sorte controlada e recompensa rara.

---

## 10. Quests dos aliados

O MVP possui um menu de quests dos personagens aliados:

| Personagem | Espécie | Quest | Local |
|---|---|---|---|
| Camila | Tamanduá-bandeira | As Formigas Luminosas do Ipê | Bosque do Ipê |
| Eduardo | Jaguatirica | O Rastro da Pena Sombria | Ruínas da Arpia |
| Monique | Tatu-bola | O Casco Contra os Golems | Caverna dos Golems |
| Pietra | Onça-pintada | O Juramento da Onça Guardiã | Clareira da Árvore do Mundo |
| Santiago | Tucano | As Cartas de Voo do Navegador | Vila das Preguiças |
| Beatriz | Boto-cor-de-rosa | A Canção das Águas | Lago das Capivaras |

---

## 11. Algoritmos

### 11.1 TSP

O **TSP — Travelling Salesman Problem** é usado para calcular a menor rota da missão principal.

Na narrativa, Henry e Mitis precisam visitar locais obrigatórios da floresta. Como a energia do portal é limitada, o mapa mágico calcula qual seria o caminho mais eficiente.

Complexidade da abordagem por força bruta:

```txt
O(n!)
```

No estado atual do jogo, o TSP funciona como uma **recomendação estratégica**. O jogador pode explorar livremente e não é bloqueado caso escolha outro caminho. A rota ótima serve para demonstrar o algoritmo dentro da narrativa.

Arquivos relacionados:

```txt
membro1_tsp/mapa.py
membro1_tsp/tsp.py
membro1_tsp/quest.py
```

### 11.2 MergeSort

O **MergeSort** é usado para ordenar o inventário por:

- nome;
- peso;
- raridade;
- valor mágico;
- preço.

Complexidade:

```txt
O(n log n)
```

Arquivo relacionado:

```txt
membro2_mundo/sorting.py
```

### 11.3 Dados estilo RPG de mesa — D20

O MVP usa testes simples com **D20**, ou seja, um dado de 20 faces.

Existem dois usos principais:

#### Dado de Mobilidade

Usado em viagens e ao avançar na Floresta Distorcida. A rolagem pode gerar:

- atalho;
- perda de HP;
- recuperação de mana;
- bônus de moedas;
- sucesso normal;
- falha parcial.

#### Dado de Luta

Usado em ataques físicos, magias ofensivas de Henry, Quake, penas do Mitis e ataques dos mobs.

A rolagem pode gerar:

- falha crítica;
- golpe fraco;
- golpe normal;
- golpe forte;
- crítico.

Arquivo relacionado:

```txt
membro2_mundo/dados.py
```

### 11.4 Probabilidade

A probabilidade aparece principalmente na Floresta Distorcida, que sorteia salas, criaturas, recompensas e eventos especiais.

O exemplo mais importante é a quest da Beatriz, pois a Pérola Furta-cor possui chance baixa de aparecer em trechos aquáticos.

---

## 12. Inventário

O inventário é uma estrutura baseada em lista de dicionários. Cada item pode possuir:

- nome;
- tipo;
- raridade;
- peso;
- valor mágico;
- preço;
- efeitos;
- descrição.

O jogador pode:

- ver inventário;
- consultar item por número;
- usar poção/consumível por número;
- equipar item por número;
- remover item;
- ordenar inventário com MergeSort.

Arquivos relacionados:

```txt
membro3_inventario/inventory.py
membro3_inventario/inventario_ui.py
```

---

## 13. Save/load

O jogo possui sistema de salvamento e carregamento em JSON.

Opções no menu:

```txt
16 - Salvar jogo
17 - Carregar jogo
```

Arquivo relacionado:

```txt
membro3_inventario/save_manager.py
```

---

## 14. Estrutura do projeto

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
├── tests/
│   └── smoke_test.py
└── docs/
```

---

## 15. Divisão por membros

### Membro 1 — Wanessa

Responsável por:

- TSP;
- mapa textual;
- missão principal;
- tela inicial;
- créditos.

Arquivos principais:

```txt
membro1_tsp/mapa.py
membro1_tsp/tsp.py
membro1_tsp/quest.py
membro1_tsp/tela_inicial.py
membro1_tsp/creditos.py
```

### Membro 2 — Ryan

Responsável por:

- locais;
- coleta;
- MergeSort;
- loja;
- combate;
- progressão;
- D20;
- Floresta Distorcida;
- quests;
- diálogos de NPCs;
- diálogos de Henry e Mitis;
- Beatriz e Pérola Furta-cor.

Arquivos principais:

```txt
membro2_mundo/coleta.py
membro2_mundo/combate.py
membro2_mundo/dados.py
membro2_mundo/dialogos_npcs.py
membro2_mundo/dialogos_henry_mitis.py
membro2_mundo/floresta_distorcida.py
membro2_mundo/locais.py
membro2_mundo/loja_capivara.py
membro2_mundo/progressao.py
membro2_mundo/quests_personagens.py
membro2_mundo/sorting.py
```

### Membro 3 — Santiago

Responsável por:

- inventário;
- interface textual do inventário;
- consumíveis;
- equipamentos;
- consulta de item por número;
- salvar e carregar jogo.

Arquivos principais:

```txt
membro3_inventario/inventory.py
membro3_inventario/inventario_ui.py
membro3_inventario/save_manager.py
```

---

## 16. Arquivos principais

### main.py

Arquivo de entrada do jogo. Importa e executa `iniciar_jogo()`.

### game.py

Arquivo de integração geral. Conecta os módulos dos três membros e controla o fluxo principal do menu.

### membro1_tsp/mapa.py

Define os locais e distâncias usados pelo mapa e pelo TSP.

### membro1_tsp/tsp.py

Implementa o cálculo da melhor rota.

### membro1_tsp/quest.py

Define a missão principal e os locais obrigatórios.

### membro1_tsp/tela_inicial.py

Exibe a tela inicial do jogo.

### membro1_tsp/creditos.py

Exibe os créditos.

### membro2_mundo/coleta.py

Controla a coleta de itens por local.

### membro2_mundo/combate.py

Controla batalhas, ataques, magias, habilidades e uso de consumíveis em combate.

### membro2_mundo/dados.py

Implementa os testes com D20.

### membro2_mundo/dialogos_npcs.py

Controla os diálogos com NPCs.

### membro2_mundo/dialogos_henry_mitis.py

Controla falas contextuais entre Henry e Mitis.

### membro2_mundo/floresta_distorcida.py

Controla a dungeon dinâmica, mobs escaláveis e recompensas probabilísticas.

### membro2_mundo/locais.py

Define locais, itens e criaturas do mundo.

### membro2_mundo/loja_capivara.py

Controla a loja da Capivara.

### membro2_mundo/progressao.py

Controla EXP, level up e evolução de habilidades.

### membro2_mundo/quests_personagens.py

Controla as quests dos aliados.

### membro2_mundo/sorting.py

Implementa o MergeSort.

### membro3_inventario/inventory.py

Controla a estrutura do inventário e suas operações.

### membro3_inventario/inventario_ui.py

Controla a interface textual do inventário.

### membro3_inventario/save_manager.py

Controla save/load em JSON.

---

## 17. Checklist rápido de validação

Antes de entregar:

```bash
python -m compileall -q .
python tests/smoke_test.py
python main.py
```

Teste manual sugerido:

1. Abrir o jogo;
2. Escolher Novo jogo;
3. Ver missão;
4. Ver mapa;
5. Calcular TSP;
6. Viajar para outro local;
7. Coletar item;
8. Ver inventário;
9. Ordenar inventário;
10. Conversar com NPC;
11. Entrar na Floresta Distorcida;
12. Salvar jogo.

---

## 18. Status atual

O projeto possui:

- tela inicial;
- créditos;
- TSP funcional;
- mapa textual;
- missão principal;
- coleta;
- inventário;
- MergeSort;
- loja;
- combate;
- magias;
- habilidades;
- D20;
- progressão;
- quests;
- diálogos;
- Floresta Distorcida;
- Beatriz e Pérola Furta-cor;
- save/load.

---

## 19. Conclusão

**Henry e a Floresta do Mundo** transforma os requisitos acadêmicos de algoritmos em mecânicas jogáveis. O TSP orienta a missão principal, o MergeSort organiza o inventário, a coleta incentiva exploração, o D20 cria incerteza controlada e a Floresta Distorcida adiciona eventos probabilísticos.

O resultado é um RPG textual simples de executar, organizado por módulos e conectado à narrativa dos personagens.
