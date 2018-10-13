"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1000      # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    Helper function that plays a game starting with the given 
    player by making random moves alternatively.
    """
    while board.check_win() == None:
        empty_squares = board.get_empty_squares()
        random_move = random.choice(empty_squares)
        board.move(random_move[0], random_move[1], player)
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
    Helper function that scores the completed board and updates
    the scores grid.
    """
    win_player = board.check_win()
    if win_player != None and win_player != provided.DRAW:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if player == win_player:
                    scores[row][col] += SCORE_CURRENT * (board.square(row, col) == player)
                    scores[row][col] -= SCORE_OTHER * (board.square(row, col) == provided.switch_player(player))
                else:
                    scores[row][col] -= SCORE_CURRENT * (board.square(row, col) == player)
                    scores[row][col] += SCORE_OTHER * (board.square(row, col) == provided.switch_player(player))

def get_best_move(board, scores):
    """
    Helper function that finds all of the empty squares with 
    the maximum score and randomly return one of them as a 
    (row, column) tuple.
    """
    empty_squares = board.get_empty_squares()
    if len(empty_squares) == 1:
        return empty_squares[0]
    best_score = scores[empty_squares[0][0]][empty_squares[0][1]]
    best_pos = []
    for empty_pos in empty_squares:
        if scores[empty_pos[0]][empty_pos[1]] > best_score:
            best_score = scores[empty_pos[0]][empty_pos[1]]
    for empty_pos in empty_squares:
        if scores[empty_pos[0]][empty_pos[1]] == best_score:
            best_pos.append((empty_pos[0], empty_pos[1]))
    return random.choice(best_pos)

def mc_move(board, player, trials):
    """
    Helper function that uses the Monte Carlo simulation 
    to return a move for the machine player in the form of a 
    (row, column) tuple.
    """
    scores = [[0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]
    for dummy_ind in range(trials):
        board_temp = board.clone()
        mc_trial(board_temp, player)
        mc_update_scores(scores, board_temp, player)
    return get_best_move(board, scores)

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)