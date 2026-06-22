# Relatório do Trabalho 2: Busca com Adversário

## 1. Integrantes do grupo

| Nome | Cartão de matrícula | Turma |
|------|---------------------|-------|
| Leonardo Leites | 00338804 | B |
| Daniel Gutschwager | 00315708 | B |


## 2. Bibliotecas necessárias

A nossa implementação (minimax com poda alfa-beta e heurísticas do Othello e do Tic-Tac-Toe Misère) utiliza **apenas a biblioteca padrão do Python** (`random`, `typing`, `time`). Nenhuma dependência externa precisa ser instalada para executar os agentes.

Opcional (apenas para visualização do tabuleiro com cores, fornecida pelo kit): `pytermgui` (`pip install pytermgui`), usada pelo `server_tui.py`.

## 3. Poda alfa-beta no Tic-Tac-Toe Misère (seção 2.2, item "a")

O agente foi avaliado através do script `test_minimax_tttm.py` e em partidas contra o agente aleatório (`randomplayer`).
- **Testes Unitários:** Todos os 4 testes do script `test_minimax_tttm.py` passaram com sucesso. O agente avalia corretamente os estados terminais, sempre inicia jogando no centro `(1,1)` (evitando derrota forçada), joga perfeitamente quando pressionado e encontra com sucesso o caminho de vitória forçada quando o oponente comete um erro (blunder).
- **Partidas contra o agente aleatório:** Em simulações usando o `server.py`, o agente construído empata garantidamente quando joga como o primeiro jogador (Black), já que a teoria do Misère em tabuleiro 3x3 indica empate com jogadas perfeitas. Quando atua como segundo jogador (White), o agente frequentemente alcança vitórias explorando jogadas sub-ótimas do adversário, demonstrando plena efetividade do algoritmo Minimax com poda Alfa-Beta para a variação Misère.

### Resultados do Mini-Torneio Tic-Tac-Toe Misère
| Partida | Jogador 1 (B - Pretas) | Jogador 2 (W - Brancas) | Vencedor |
| :---: | :--- | :--- | :--- |
| **1** | Minimax | Aleatório | **Minimax** |
| **2** | Aleatório | Minimax | **Minimax** |
| **3** | Minimax | Aleatório | **Empate** |
| **4** | Aleatório | Minimax | **Minimax** |
| **5** | Minimax | Aleatório | **Minimax** |
| **6** | Aleatório | Minimax | **Minimax** |

### Desempenho Geral e Conclusão

| Colocação | Agente | Vitórias | Empates | Derrotas |
| :---: | :--- | :---: | :---: | :---: |
| **1º** | **Minimax** | **5** | **1** | **0** |
| **2º** | **Aleatório** | **0** | **1** | **5** |

**Conclusão:**
A implementação do algoritmo **Minimax** demonstrou superioridade absoluta contra o agente Aleatório, terminando a série de forma invicta com 5 vitórias e 1 empate. Como esperado, o Minimax foi capaz de forçar vitórias sistemáticas explorando as jogadas sub-ótimas (blunders) do adversário, tanto jogando como primeiro (Pretas) quanto como segundo jogador (Brancas).


## 4. Othello

### 4.1 Heurística customizada

A estrutura da heurística (componentes e fontes) descrita nesta seção é a definitiva. Apenas a **tabela de pesos por fase** foi recalibrada ao longo do desenvolvimento. A versão inicial está logo abaixo e a versão final, que de fato usamos, está na seção 4.3.

A heurística (`evaluate_custom`, em `advsearch/dl_agent/othello_minimax_custom.py`) combina quatro componentes, e estados terminais são tratados como utilidade absoluta (vitória = `+inf`, derrota = `-inf`, empate = `0`) para que o minimax sempre priorize sequências que levam à vitória em vez de apenas maximizar pontuação posicional.

Os componentes não-terminais são:

1. **Valor posicional (máscara estática).** Uma matriz de pesos fixos para as 64 casas, recompensando cantos (+100), penalizando fortemente as casas adjacentes a cantos / X-squares (−50, −30) e atribuindo valores baixos ao centro. O score é **normalizado para o intervalo [−100, 100]** dividindo a diferença (minhas casas − casas do oponente) pela soma dos pesos absolutos das casas ocupadas, para ficar na mesma escala das demais métricas.

2. **Mobilidade.** Diferença relativa de jogadas legais disponíveis, normalizada por `100 * (minhas − oponente) / (minhas + oponente)`.

3. **Paridade de peças.** Diferença relativa de peças, normalizada pela mesma fórmula. No início do jogo essa métrica recebe peso **negativo**, refletindo a estratégia de não acumular peças cedo (uma "parede" de peças no early-game facilita capturas do oponente).

4. **Pesos dinâmicos por fase.** O jogo é fatiado em três fases pela quantidade de casas vazias, e cada métrica recebe um multiplicador diferente:

   | Fase | Casas vazias | Posicional | Mobilidade | Peças |
   |------|--------------|-----------|-----------|-------|
   | Início | > 44 | 10 | 50 | −5 |
   | Meio | 15 a 44 | 20 | 20 | 5 |
   | Fim | ≤ 14 | 30 | 5 | 40 |

   O agente prioriza mobilidade no início, equilibra no meio e foca na contagem de peças (estáveis) no final. O valor final é a soma ponderada das métricas.

   > **Observação:** esta é a tabela de pesos da versão inicial. Ela foi recalibrada posteriormente. A tabela definitiva está na seção 4.3.

#### Fontes utilizadas

A heurística **não foi baseada de uma única fonte**: é uma combinação de ideias de diferentes referências, adaptada e calibrada pelo grupo.

- **Rosenbloom, P. (1982), programa IAGO.** Base teórica para o valor posicional: cantos são invioláveis (não podem ser recapturados) e por isso são as casas mais valiosas; bordas são mais estáveis que o centro; e a mobilidade torna-se a preocupação central no meio do jogo. Usamos esse raciocínio para desenhar a matriz de pesos e para dar peso alto à mobilidade.

- **Kartik Kukreja, "Heuristic function for Reversi/Othello"** (https://kartikkukreja.wordpress.com/2013/03/30/heuristic-function-for-reversiothello/). Dela tiramos a fórmula de normalização `100 * (Max − Min) / (Max + Min)`, aplicada às métricas de mobilidade e paridade para colocá-las na mesma escala da matriz. As métricas de estabilidade e de cantos capturados descritas na fonte foram usadas apenas como referência conceitual.

- **Buro, M. (1997), programa Logistello.** ("The Othello match of the year: Takeshi Murakami vs. Logistello", ICCA Journal 20(3); ver também "The Evolution of Strong Othello Programs"). Base para a ideia de **pesos dinâmicos por fase do jogo**: o que é bom no início é ruim no fim, então os multiplicadores das métricas mudam conforme o tabuleiro se enche. Adaptamos o princípio com três fases simples baseadas em casas vazias.

Em resumo, o valor posicional vem da linha do IAGO, a normalização das métricas vem do material do Kukreja, e a transição de pesos por fase segue o princípio do Logistello. Todos esses elementos foram combinados e ajustados manualmente pelo grupo.

### 4.2 Critério de parada do agente versão 1

**Profundidade máxima fixa.** O agente chama `minimax_move(state, 5, evaluate_custom)`, ou seja, a busca alfa-beta vai até profundidade 5 e então aplica a função de avaliação nas folhas. O tempo de cada jogada é medido e impresso, mas não há aprofundamento iterativo nem corte por tempo.


### 4.3 Resultado da avaliação (seção 2.2, item "b") e heurística versão 2

### Resultados do Mini-Torneio othello

| Partida | Jogador 1 (B - Pretas) | Jogador 2 (W - Brancas) | Placar (B x W) | Vencedor |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Contagem de Peças | Valor Posicional | 37 x 27 | **Contagem de Peças** |
| **2** | Valor Posicional | Contagem de Peças | 26 x 38 | **Contagem de Peças** |
| **3** | Contagem de Peças | Heurística Customizada | 29 x 35 | **Heurística Customizada** |
| **4** | Heurística Customizada | Contagem de Peças | 42 x 22 | **Heurística Customizada** |
| **5** | Valor Posicional | Heurística Customizada | 23 x 41 | **Heurística Customizada** |
| **6** | Heurística Customizada | Valor Posicional | 24 x 40 | **Valor Posicional** |

### Desempenho Geral e Conclusão

| Colocação | Heurística | Vitórias | Peças Capturadas (Total) |
| :---: | :--- | :---: | :---: |
| **1º** | **Heurística Customizada** | **3** | **142** |
| 2º | Contagem de Peças | 2 | 126 |
| 3º | Valor Posicional | 1 | 116 |

**Conclusão:**
A implementação mais bem-sucedida foi a **Heurística Customizada**, terminando o torneio em primeiro lugar com o maior número de vitórias (3) e o maior saldo global de peças capturadas (142). A estratégia de utilizar pesos dinâmicos combinando múltiplas métricas provou ser mais robusta e eficiente do que as abordagens estáticas na maioria dos cenários. 

**Observação importante**

Chamou a atenção o fato de a heurística customizada perder, de pretas, para a heurística posicional (mask). Após análise, apoiada por IA e por prints dos pesos calculados durante a partida, concluímos que a derrota era coerente e decorria de um desajuste na calibração das nossas métricas. A busca é idêntica nos dois agentes, com a mesma profundidade fixa, portanto a única diferença está na heurística. Examinando o tabuleiro final, identificamos dois problemas: a heurística customizada diluía demais o valor das casas conforme o jogo avançava e atribuía pesos muito díspares entre posição e mobilidade. No início, a mobilidade pesava cinco vezes mais que a posição, de modo que o agente priorizava ter muitas jogadas e praticamente ignorava deixar o oponente se aproximar dos cantos. Como consequência, o mask alcançava os cantos mais cedo, e a estabilidade conquistada no início se mostrava decisiva no fim do jogo.

Com isso, realizamos alterações na heurística e repetimos o mini-torneio.

A mudança incidiu sobre os **pesos dinâmicos por fase**. No início e no meio do jogo, passamos a priorizar a ocupação de boas casas e a evitar os X/C-squares (as casas de valor −50/−30 da matriz), mantendo a mobilidade apenas como apoio para não travar a posição. No fim do jogo, a paridade de peças passa a dominar, pois nessa etapa as peças tendem a se tornar estáveis. A nova tabela de pesos (definitiva) é:

   | Fase | Casas vazias | Posicional | Mobilidade | Peças |
   |------|--------------|-----------|-----------|-------|
   | Início | > 44 | 35 | 15 | −1 |
   | Meio | 15 a 44 | 25 | 15 | 10 |
   | Fim | ≤ 14 | 20 | 5 | 50 |

Ao rodar com profundidade fixa 5, porém, ambos os agentes foram desclassificados:

```
Player B (advsearch\dl_agent) DISQUALIFIED! Too many illegal move attempts.
Player W (advsearch\dl_agent) DISQUALIFIED! Too many illegal move attempts.
```

A desclassificação ocorreu por exceder o tempo limite de 5 segundos. Como todos os agentes do mini-torneio usam a mesma profundidade de busca fixa, há duas formas de resolver: adicionar um corte por tempo ou reduzir a profundidade. Para garantir uma **comparação justa entre as heurísticas**, em que a única variável seja a própria heurística e não o tempo de busca disponível, optamos por fixar a profundidade de **todos** os agentes em 4 e repetir os confrontos.

**Resultados do NOVO Mini-Torneio**

| Partida | Jogador 1 (B - Pretas) | Jogador 2 (W - Brancas) | Placar (B x W) | Vencedor |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Contagem de Peças | Valor Posicional | 28 x 36 | **Valor Posicional** |
| **2** | Valor Posicional | Contagem de Peças | 22 x 42 | **Contagem de Peças** |
| **3** | Contagem de Peças | Heurística Customizada | 12 x 52 | **Heurística Customizada** |
| **4** | Heurística Customizada | Contagem de Peças | 39 x 25 | **Heurística Customizada** |
| **5** | Valor Posicional | Heurística Customizada | 27 x 37 | **Heurística Customizada** |
| **6** | Heurística Customizada | Valor Posicional | 39 x 25 | **Heurística Customizada** |


| Colocação | Heurística | Vitórias | Peças Capturadas (Total) |
| :---: | :--- | :---: | :---: |
| **1º** | **Heurística Customizada** | **4** | **167** |
| 2º | Valor Posicional | 1 | 110 |
| 3º | Contagem de Peças | 1 | 107 |

**Conclusão:**
A implementação mais bem-sucedida de todas foi, de forma invicta, a **Heurística Customizada**. 

Ela venceu todas as **4 partidas** que disputou, demonstrando superioridade contra as outras duas estratégias e acumulando um total expressivo de **167 peças**. As nossas alterações provaram ser muito mais assertivas.

O Valor Posicional e a Contagem de Peças empataram em número de vitórias (1 cada), mas o Valor Posicional ficou em segundo lugar no critério de desempate, com um total de 110 peças capturadas contra 107 da Contagem.

### 4.4 Ajustes finos da versão final e critério de parada (versão 2)

Para o torneio, a fim de permitir uma profundidade de busca maior sem extrapolar o limite de 5 segundos, é necessário um mecanismo de controle de tempo. Esse controle foi adicionado apenas ao agente de torneio.

Implementamos um **aprofundamento iterativo** (com apoio de IA generativa na concepção da ideia). O agente busca profundidades crescentes (1, 2, 3, ...) e, a cada profundidade concluída, guarda a melhor jogada encontrada. Quando o tempo decorrido se aproxima de 4 segundos, mantendo uma margem de segurança sobre os 5 segundos do servidor, a busca é interrompida e o agente devolve a melhor jogada da última profundidade que foi concluída por completo.

A interrupção é feita sem criar processos ou threads em segundo plano: a busca roda em uma única thread sobre o minimax padrão (com a heurística customizada), e uma exceção é levantada quando o tempo estoura, descartando a profundidade incompleta e retornando a melhor jogada já avaliada e armazenada.

Em resumo, o critério de parada final é o seguinte: o agente de torneio usa **aprofundamento iterativo com corte por tempo** (4 s de margem sobre os 5 s), enquanto os três arquivos de heurística básica (contagem, posicional e customizada) usam **profundidade fixa 4**.

### 4.5 Implementação escolhida para o torneio

O agente de torneio (`advsearch/dl_agent/tournament_agent.py`) utiliza a **mesma heurística customizada** descrita na seção 4.3, chamando o minimax com poda alfa-beta e a função `evaluate_custom`, combinada com o controle de tempo descrito na seção 4.4.

### 4.6 Extras

Como melhoria opcional sobre o minimax com poda alfa-beta clássico, implementamos a **busca com aprofundamento iterativo com corte por tempo** no agente de torneio (descrita na seção 4.4). A técnica permite aproveitar ao máximo o tempo disponível por jogada, buscando o mais fundo possível dentro do limite de 5 segundos, sem o risco de desclassificação por excesso de tempo. A concepção dessa abordagem contou com auxílio de IA generativa (ver seção 5).

## 5. Utilização de chatbots ou agentes de IA

Declaramos que utilizamos ferramentas de IA durante o desenvolvimento deste trabalho, dentro dos usos permitidos pelo enunciado (apoio ao projeto da heurística e à análise, sem geração de código completo que resolvesse a tarefa). Especificamente, a IA foi utilizada para: discutir e refinar o desenho da heurística customizada; analisar por que a versão inicial perdia para a heurística posicional (interpretação dos pesos e do tabuleiro final); sugerir a abordagem de controle de tempo por aprofundamento iterativo; e revisar a redação deste relatório. A implementação do código, a calibração dos pesos e a execução dos testes foram feitas pelo grupo.