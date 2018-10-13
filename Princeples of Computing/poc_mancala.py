"""
Student facing implement of solitaire version of Mancala - Tchoukaillon

Goal: Move as many seeds from given houses into the store

In GUI, you make ask computer AI to make move or click to attempt a legal move
"""


class SolitaireMancala:
    """
    Simple class that implements Solitaire Mancala
    """
    
    def __init__(self):
        """
        Create Mancala game with empty store and no houses
        """
        self._board = [0]
    
    def set_board(self, configuration):
        """
        Take the list configuration of initial number of seeds for given houses
        house zero corresponds to the store and is on right
        houses are number in ascending order from right to left
        """
        self._board = list(configuration)
    
    def __str__(self):
        """
        Return string representation for Mancala board
        """
        reverse_board = list(self._board)
        reverse_board.reverse()        
        return str(reverse_board)
    
    def get_num_seeds(self, house_num):
        """
        Return the number of seeds in given house on board
        """
        return self._board[house_num]

    def is_game_won(self):
        """
        Check to see if all houses but house zero are empty
        """
        if(len(self._board) == 1):
            return True;
        else:
            if(max(self._board[1:]) == 0):
                return True
            else:
                return False
    
    def is_legal_move(self, house_num):
        """
        Check whether a given move is legal
        """
        if(house_num != 0 and self._board[house_num] == house_num):
            return True
        else:
            return False

    
    def apply_move(self, house_num):
        """
        Move all of the stones from house to lower/left houses
        Last seed must be played in the store (house zero)
        """
        if(self.is_legal_move(house_num)):
            self._board[house_num] = 0
            for house_index in range(0, house_num):
                self._board[house_index] += 1

    def choose_move(self):
        """
        Return the house for the next shortest legal move
        Shortest means legal move from house closest to store
        Note that using a longer legal move would make smaller illegal
        If no legal move, return house zero
        """
        reverse_board = list(self._board)
        reverse_board.reverse()
        for house_index in range(1, len(reverse_board)):
            if self.is_legal_move(house_index):
                return house_index
        return 0
    
    def plan_moves(self):
        """
        Return a sequence (list) of legal moves based on the following heuristic: 
        After each move, move the seeds in the house closest to the store 
        when given a choice of legal moves
        Not used in GUI version, only for machine testing
        """
        new_board = SolitaireMancala()
        new_board.set_board(self._board)
        moves = []
        next_move = new_board.choose_move()
        while next_move != 0:
            moves.append(next_move)
            new_board.apply_move(next_move)
            next_move = new_board.choose_move()
        return moves
 

# Create tests to check the correctness of your code

def test_mancala():
    """
    Test code for Solitaire Mancala
    """
    
    my_game = SolitaireMancala()
    print "Testing init - Computed:", my_game, "Expected: [0]"
    
    config1 = [0, 0, 1, 1, 3, 5, 0]    
    my_game.set_board(config1)   
    
    print "Testing set_board - Computed:", str(my_game), "Expected:", str([0, 5, 3, 1, 1, 0, 0])
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(1), "Expected:", config1[1]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(3), "Expected:", config1[3]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(5), "Expected:", config1[5]

    # add more tests here
    print "Testing is_game_won - Computed:", my_game.is_game_won(), "Expected:", False
    config2 = [6, 0, 0, 0, 0, 0, 0]
    my_game.set_board(config2)
    print "Testing is_game_won - Computed:", my_game.is_game_won(), "Expected:", True
    
    my_game.set_board(config1)
    print "Testing is_legal_move - Computed:", my_game.is_legal_move(5), "Expected:", True
    print "Testing is_legal_move - Computed:", my_game.is_legal_move(3), "Expected:", False
    
    my_game.apply_move(5)
    print "Testing apply_move - Computed:", str(my_game), "Expected:", str([0, 0, 4, 2, 2, 1, 1])
    
    my_game.set_board(config1)
    print "Testing choose_move - Computed:", my_game.choose_move(), "Expected:", 5
   
    print "Testing plan_moves - Computed:", my_game.plan_moves(), "Expected:", str([5, 1, 4, 1, 3, 1, 2, 1])	
    
# test_mancala()


# Import GUI code once you feel your code is correct
# import poc_mancala_gui
# poc_mancala_gui.run_gui(SolitaireMancala())
