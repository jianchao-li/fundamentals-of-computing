"""
Mini-max Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements. The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    if board.check_win() is not None:
        if board.check_win() == provided.PLAYERX:
            return SCORES[provided.PLAYERX], (-1, -1)
        elif board.check_win() == provided.PLAYERO:
            return SCORES[provided.PLAYERO], (-1, -1)
        else:
            return SCORES[provided.DRAW], (-1, -1)
    else:
        best_score = -2
        best_move = (-1, -1)
        possible_moves = board.get_empty_squares()
        for possible_move in possible_moves:
            board_clone = board.clone()
            board_clone.move(possible_move[0], possible_move[1], player)
            score, dummy_move = mm_move(board_clone, provided.switch_player(player))
            negate_score = score * SCORES[player]
            if negate_score == 1:
                return score, possible_move
            if negate_score > best_score:
                best_score = negate_score
                best_move = possible_move
        return best_score * SCORES[player], best_move

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)