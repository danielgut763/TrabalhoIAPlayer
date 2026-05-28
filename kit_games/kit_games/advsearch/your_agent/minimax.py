import random
from typing import Tuple, Callable



def minimax_move(state, max_depth:int, eval_func:Callable) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game state.
    :param state: state to make the move (instance of GameState)
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate a terminal or leaf state (when search is interrupted at max_depth)
                    This function should take a GameState object and a string identifying the player,
                    and should return a float value representing the utility of the state for the player.
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    original_player = state.player

    #função auxiliar que implementa o algoritmo alpha-beta
    def alphabeta(current_state, alpha, beta, depth):
        if current_state.is_terminal() or depth == 0:
            return eval_func(current_state, original_player)
            
        if current_state.player == original_player:
            v = float('-inf')
            for move in current_state.legal_moves():
                next_s = current_state.next_state(move)
                val = alphabeta(next_s, alpha, beta, depth - 1)
                v = max(v, val)
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v
        else:
            v = float('inf')
            for move in current_state.legal_moves():
                next_s = current_state.next_state(move)
                val = alphabeta(next_s, alpha, beta, depth - 1)
                v = min(v, val)
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    #percorre todos os movimentos legais e aplica o algoritmo alpha-beta
    for move in state.legal_moves():
        if best_move is None:
            best_move = move
        next_s = state.next_state(move)
        val = alphabeta(next_s, alpha, beta, max_depth - 1)
        
        if val > best_value:
            best_value = val
            best_move = move
            
        alpha = max(alpha, best_value)

    return best_move
