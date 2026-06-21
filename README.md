# TrabalhoIAPlayer

## 1. Integrantes do grupo

| Nome | Cartão de matrícula |
|------|---------------------|
| Leonardo Leites | 00338804 | 
| Daniel Gutschwager | 00315708 |


## 2. Bibliotecas necessárias

A nossa implementação (minimax com poda alfa-beta e heurísticas do Othello e do Tic-Tac-Toe Misère) utiliza **apenas a biblioteca padrão do Python** (`random`, `typing`, `time`). Nenhuma dependência externa precisa ser instalada para executar os agentes.

Opcional (apenas para visualização do tabuleiro com cores, fornecida pelo kit): `pytermgui` (`pip install pytermgui`), usada pelo `server_tui.py`.

## 3. Poda alfa-beta no Tic-Tac-Toe Misère (seção 2.3, item "a")

O agente foi avaliado através do script `test_minimax_tttm.py` e em partidas contra o agente aleatório (`randomplayer`).
- **Testes Unitários:** Todos os 4 testes do script `test_minimax_tttm.py` passaram com sucesso. O agente avalia corretamente os estados terminais, sempre inicia jogando no centro `(1,1)` (evitando derrota forçada), joga perfeitamente quando pressionado e encontra com sucesso o caminho de vitória forçada quando o oponente comete um erro (blunder).
- **Partidas contra o agente aleatório:** Em simulações usando o `server.py`, o agente construído empata garantidamente quando joga como o primeiro jogador (Black), já que a teoria do Misère em tabuleiro 3x3 indica empate com jogadas perfeitas. Quando atua como segundo jogador (White), o agente frequentemente alcança vitórias explorando jogadas sub-ótimas do adversário, demonstrando plena efetividade do algoritmo Minimax com poda Alfa-Beta para a variação Misère.

## 4. Othello

### 4.1 Heurística customizada

A heurística (`evaluate_custom`, em `advsearch/dl_agent/othello_minimax_custom.py`) combina quatro componentes, e estados terminais são tratados como utilidade absoluta (vitória = `+inf`, derrota = `-inf`, empate = `0`) para que o minimax sempre priorize sequências que levam à vitória em vez de apenas maximizar pontuação posicional.

Os componentes não-terminais são:

1. **Valor posicional (máscara estática).** Uma matriz de pesos fixos para as 64 casas, recompensando cantos (+100), penalizando fortemente as casas adjacentes a cantos / X-squares (−50, −30) e atribuindo valores baixos ao centro. O score é **normalizado para o intervalo [−100, 100]** dividindo a diferença (minhas casas − casas do oponente) pela soma dos pesos absolutos das casas ocupadas, para ficar na mesma escala das demais métricas.

2. **Mobilidade.** Diferença relativa de jogadas legais disponíveis, normalizada por `100 * (minhas − oponente) / (minhas + oponente)`.

3. **Paridade de peças.** Diferença relativa de peças, normalizada pela mesma fórmula. No início do jogo essa métrica recebe peso **negativo**, refletindo a estratégia de não acumular peças cedo (uma "parede" de peças no early-game facilita capturas do oponente).

4. **Pesos dinâmicos por fase.** O jogo é fatiado em três fases pela quantidade de casas vazias, e cada métrica recebe um multiplicador diferente:

   | Fase | Casas vazias | Posicional | Mobilidade | Peças |
   |------|--------------|-----------|-----------|-------|
   | Início | > 44 | 10 | 50 | −5 |
   | Meio | 15–44 | 20 | 20 | 5 |
   | Fim | ≤ 14 | 30 | 5 | 40 |

   O agente prioriza mobilidade no início, equilibra no meio e foca na contagem de peças (estáveis) no final. O valor final é a soma ponderada das métricas.

#### Fontes utilizadas

A heurística **não foi baseada de uma única fonte**: é uma combinação de ideias de diferentes referências, adaptada e calibrada pelo grupo.

- **Rosenbloom, P. (1982) — programa IAGO.** Base teórica para o valor posicional: cantos são invioláveis (não podem ser recapturados) e por isso são as casas mais valiosas; bordas são mais estáveis que o centro; e a mobilidade torna-se a preocupação central no meio do jogo. Usamos esse raciocínio para desenhar a matriz de pesos e para dar peso alto à mobilidade.

- **Kartik Kukreja — "Heuristic function for Reversi/Othello"** (https://kartikkukreja.wordpress.com/2013/03/30/heuristic-function-for-reversiothello/). Dela tiramos a fórmula de normalização `100 * (Max − Min) / (Max + Min)`, aplicada às métricas de mobilidade e paridade para colocá-las na mesma escala da matriz. As métricas de estabilidade e de cantos capturados descritas na fonte foram usadas apenas como referência conceitual.

- **Buro, M. (1997) — programa Logistello.** ("The Othello match of the year: Takeshi Murakami vs. Logistello", ICCA Journal 20(3); ver também "The Evolution of Strong Othello Programs"). Base para a ideia de **pesos dinâmicos por fase do jogo**: o que é bom no início é ruim no fim, então os multiplicadores das métricas mudam conforme o tabuleiro se enche. Adaptamos o princípio com três fases simples baseadas em casas vazias.

Em resumo: o valor posicional vem da linha do IAGO, a normalização das métricas vem do material do Kukreja, e a transição de pesos por fase segue o princípio do Logistello — todos combinados e ajustados manualmente pelo grupo.

### 4.2 Critério de parada do agente

**Profundidade máxima fixa.** O agente chama `minimax_move(state, 5, evaluate_custom)`, ou seja, a busca alfa-beta vai até profundidade 5 e então aplica a função de avaliação nas folhas. O tempo de cada jogada é medido e impresso, mas não há aprofundamento iterativo nem corte por tempo.


### 4.3 Resultado da avaliação (seção 2.3, item "b")

_[preencher com o resultado da avaliação do agente de Othello — ex.: partidas contra o random e/ou contra os agentes de contagem e máscara, placares, taxa de vitória, etc.]_

### 4.4 Implementação escolhida para o torneio

O agente de torneio (`advsearch/dl_agent/tournament_agent.py`) utiliza a **mesma heurística customizada** descrita na seção 4.1, chamando o minimax com poda alfa-beta e a função `evaluate_custom`.


### 4.5 Extras


## 5. Utilização de chatbots ou agentes de IA
