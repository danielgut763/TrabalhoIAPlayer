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

### 4.1 Heurística customizada versão 1

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

### 4.2 Critério de parada do agente versão 1

**Profundidade máxima fixa.** O agente chama `minimax_move(state, 5, evaluate_custom)`, ou seja, a busca alfa-beta vai até profundidade 5 e então aplica a função de avaliação nas folhas. O tempo de cada jogada é medido e impresso, mas não há aprofundamento iterativo nem corte por tempo.


### 4.3 Resultado da avaliação (seção 2.3, item "b") e heurística versão 2

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
Com base no resultado do mini torneio, achamos estranho que a heurística custom perdeu de pretas para o mask. Com uma ajuda da IA (e uns prints para verificar os pesos calculados) entendemos que perder, nesse caso, fazia sentido e se tratava de uma falta de ajuste nos nossos calculos. A busca é idêntica em ambos, usando a mesma profundidade; a única diferença seria a heurística. Analisando o tabuleiro final do jogo, entendemos que a heurística custom diliua muito os valores conforme o andar do jogo, além de calcular o peso posicional e o de mobilidade com muita desparidade. No começo a mobilidade pesava 5 vezes mais que a posição. O agente prioriza ter muitas jogadas e quase ignora deixar o oponente se aproximar do canto, ou seja, o mask chegava ao canto mais rápido, e no final do jogo a estabilidade conquistado no inicío se fazia melhor. 

Com isso realizamos algumas alterações e um novo torneio entre eles. 

Alterado **Pesos dinâmicos por fase.**. Cedo e no meio priorizamos ocupar boas casas e fugir dos X/C-squares (o −50/−30 da matriz), com a mobilidade ajudando a não travar. E no fim, a paridade domina porque as peças viram estáveis.

   | Fase | Casas vazias | Posicional | Mobilidade | Peças |
   |------|--------------|-----------|-----------|-------|
   | Início | > 44 | 35 | 15 | −1 |
   | Meio | 15–44 | 25 | 15 | 10 |
   | Fim | ≤ 14 | 20 | 5 | 50 |

Contudo o resultado do torneio foi:
Player B (advsearch\dl_agent) DISQUALIFIED! Too many illegal move attempts.
Player W (advsearch\dl_agent) DISQUALIFIED! Too many illegal move attempts.

Ambos foram desclassificados por tempo excedido. 
Ambos tem a mesma profundidade de busca fixa, logo para ter uma comparação justa entre elas podemos ou adicionar uma poda de tempo ou diminuir a profundidade. Para âmbitos de validar nossos testes apenas alteramos a profundidade de todos para 4 e realizamos os novos confrontos. 

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

Ela venceu todas as **4 partidas** que disputou, demonstrando superioridade absoluta contra as outras duas estratégias e acumulando um total expressivo de **167 peças**. As nossas alterações provou ser muito mais acertiva. 

O Valor Posicional e a Contagem de Peças empataram em número de vitórias (1 cada), mas o Valor Posicional ficou em segundo lugar no critério de desempate, com um total de 110 peças capturadas contra 107 da Contagem.

### 4.4 Ajuste finos versão final e critério de parada do agente versão 2
Como regra para o torneio, para poder usar uma profundidade maior, temos que ter algum controle que nos impeça de extrapolar o tempo de 5sec. 
Para isso temos que adicionar esse controle no agente de torneio.

Aqui, com uma ideia da IA generativa, tentamos implementar um controle iterativo de profundidade. A ideia aqui é ir guardando a melhor jogada em tempo de execução e ir aumentando a profundidade, caso o tempo se aproxime de 5s (4s), retornamos a última em memória.
Basicamente começamos a rodar (nunca usando mais de uma thread) sobre o minimax normal (usando a heurística custom). Se o tempo estourar no meio, temos uma exception que descarta a avaliação pela metade, retornando a melhor rodada já avaliada por completo e salva.   

Logo temos esse novo critério de parada. Basicamente: o agente de torneio usa aprofundamento iterativo com corte por tempo (4s de margem sobre os 5s), enquanto os três arquivos de heurística básica usam profundidade fixa 4.

### 4.4 Implementação escolhida para o torneio

O agente de torneio (`advsearch/dl_agent/tournament_agent.py`) utiliza a **mesma heurística customizada** descrita na seção 4.3, chamando o minimax com poda alfa-beta e a função `evaluate_custom`. E o controle de tempo implementado em 4.4.


### 4.5 Extras
aprofundamento iterativo como melhoria sobre o alfa-beta clássico

## 5. Utilização de chatbots ou agentes de IA
