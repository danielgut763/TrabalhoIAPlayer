from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move
import time

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

EVAL_TEMPLATE = [
    [100, -30, 6, 2, 2, 6, -30, 100],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [100, -30, 6, 2, 2, 6, -30, 100]
]

def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    # chama o minimax com poda alfa-beta (profundidade fixa 5) usando a heuristica customizada
    start_time = time.perf_counter()
    # print (evaluate_custom(state, 'B'), evaluate_custom(state, 'W'))
    move =  minimax_move(state, 4, evaluate_custom)

    # mede e imprime o tempo gasto no calculo da jogada
    end_time = time.perf_counter()
    print(f"Minimax Custom move calculated in {end_time - start_time:.4f} seconds")

    return move


def evaluate_custom(state, player:str) -> float:
    """
    Evaluates an othello state from the point of view of the given player. 
    If the state is terminal, returns its utility. 
    If non-terminal, returns an estimate of its value based on your custom heuristic
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """
    board = state.get_board()
    opponent = Board.opponent(player)

    # fase 1: Verifica se o estado é terminal
    if board.is_terminal_state():
        vencedor = board.winner()
        if vencedor == player:
            return float('inf')
        elif vencedor == opponent:
            return float('-inf')
        else:
            return 0.0

    # fase 2: Avalia a posição das peças no tabuleiro
    meu_pos = 0
    opp_pos = 0
    total_pos = 0
    for y in range(8):
        for x in range(8):
            piece = board.tiles[y][x]
            peso = EVAL_TEMPLATE[y][x]
            if piece == player:
                meu_pos += peso
            elif piece == opponent:
                opp_pos += peso
            if piece != Board.EMPTY:
                total_pos += abs(peso)

    if total_pos != 0:
        score_posicional = 100 * (meu_pos - opp_pos) / total_pos 
    else:  
        score_posicional = 0

    # fase 3: Avalia a mobilidade (quantidade de movimentos legais)
    minhas_jogadas = len(board.legal_moves(player))
    jogadas_oponente = len(board.legal_moves(opponent))
    if (minhas_jogadas + jogadas_oponente) != 0:
        score_mobilidade = 100 * (minhas_jogadas - jogadas_oponente) / (minhas_jogadas + jogadas_oponente)
    else:
        score_mobilidade = 0

    # fase 4: Avalia a quantidade de peças no tabuleiro
    minhas_pecas = board.num_pieces(player)
    pecas_oponente = board.num_pieces(opponent)
    if (minhas_pecas + pecas_oponente) != 0:
        score_pecas = 100 * (minhas_pecas - pecas_oponente) / (minhas_pecas + pecas_oponente)
    else:
        score_pecas = 0

    # fase 5: Define pesos para cada fase do jogo
    espacos_vazios = board.num_pieces(Board.EMPTY)
    if espacos_vazios > 44: # Início
        peso_posicional = 35
        peso_mobilidade = 10
        peso_pecas = -1
    elif espacos_vazios > 14: # Meio
        peso_posicional = 25
        peso_mobilidade = 15
        peso_pecas = 10
    else: # Fim
        peso_posicional = 20
        peso_mobilidade = 5
        peso_pecas = 50

    # fase 6: Combina as pontuações ponderadas para obter a avaliação final
    return float((score_posicional * peso_posicional) + 
                 (score_mobilidade * peso_mobilidade) + 
                 (score_pecas * peso_pecas))