import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move
from .othello_minimax_custom import evaluate_custom
import time

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

class TempoEsgotado(Exception):
    pass

def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state. 
    Consider that this will be called in the Othello tournament situation,
    so you should call the best implementation you got.

    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    if state.game_name == 'Othello':
        TEMPO_LIMITE = 4 #aqui adicionamos o tempo maximo para calcular a jogada. Se não chegar a
        # máxima profundidade e o tempo chegar a 4sec, retorna a melhjor jogada encontrada até o momento.
        deadline = time.perf_counter() + TEMPO_LIMITE

        def verifica_com_tempo(state, player):
            if time.perf_counter() > deadline:
                raise TempoEsgotado() #lança a exceção para interromper o cálculo da jogada
            return evaluate_custom(state, player) #aqui retorna a avaliação da jogada

        melhor_jogada = None #aqui retorna uma jogada válida caso o tempo esgote antes de encontrar a melhor jogada
        jogadas = list(state.legal_moves())

        if jogadas:
            melhor_jogada = jogadas[0] #inicializa a melhor jogada com a primeira jogada legal

        profundidade = 1
        try:
            while profundidade <= 10: #aqui tentamos encontrar a melhor jogada aumentando a profundidade até o limite de 10
                move = minimax_move(state, profundidade, verifica_com_tempo) #aqui chama o minimax com a função de avaliação que verifica o tempo
                if move is not None:
                    melhor_jogada = move #atualiza a melhor jogada encontrada
                profundidade += 1
                if time.perf_counter() > deadline:
                    break #se o tempo esgotar, sai do loop
        except TempoEsgotado:
            pass #se a exceção for lançada, apenas sai do loop e retorna a melhor jogada encontrada até o momento
        # print(f"profundidade: {profundidade - 1} time: {time.perf_counter() - (deadline - TEMPO_LIMITE):.4f} seconds")
        return melhor_jogada
            


