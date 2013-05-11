"""Games, or Adversarial Search. (Chapter 5)
"""

from utils import *
import random
import pdb



def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
#    pdb.set_trace()
    return argmax(game.actions(state),
                  lambda a: min_value(game.result(state, a),
                                      -infinity, infinity, 0))

#______________________________________________________________________________
# Players for Games

def query_player(game, state):
    "Make a move by querying standard input."
    game.display(state)
    x,y =raw_input('Your move? ').split(',')
    x,y=int(x),int(y)
    print 'query player move at',x
    return (x,y)

def random_player(game, state):
    "A player that chooses a legal move at random."
    return random.choice(game.actions(state))

def alphabeta_player(game, state):
    x=alphabeta_search(state, game)
    print 'alpha beta player:',x
    return x
def play_game(game, *players):
    """Play an n-person, move-alternating game.
    >>> play_game(Fig52Game(), alphabeta_player, alphabeta_player)
    3
    """
    state = game.initial
    while True:
        for player in players:
            move = player(game, state)
            print 'MOVEING',move
            state = game.result(state, move)
            if game.terminal_test(state):
                print '%s wins'% player.__name__
                return game.utility(state, game.to_move(game.initial))

#______________________________________________________________________________
# Some Sample Games

class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        "Return a list of the allowable moves at this point."
        abstract

    def result(self, state, move):
        "Return the state that results from making a move from a state."
        abstract

    def utility(self, state, player):
        "Return the value of this final state to player."
        abstract

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.actions(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        print state

    def __repr__(self):
        return '<%s>' % self.__class__.__name__


class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""
    def __init__(self, h=6, v=6, k=4):
        update(self, h=h, v=v, k=k)
        moves = [(x, y) for x in range(1, h+1)
                 for y in range(1, v+1)]
        self.initial = Struct(to_move='X', utility=0, board={}, moves=moves)
        '''
    def actions(self, state):
        "Legal moves are any square not yet taken."
        return state.moves
        '''

    def actions(self, state):
        return [(x, y) for (x, y) in state.moves
                if y == 1 or (x, y-1) in state.board]

    def result(self, state, move):
        if move not in state.moves:
            print state.moves
            print 'illegal move:',move,type(move),type(state.moves[1])
            return state # Illegal move has no effect
        board = state.board.copy(); board[move] = state.to_move
        moves = list(state.moves); moves.remove(move)
        return  Struct(to_move=if_(state.to_move == 'X', 'O', 'X'),
                      utility=self.compute_utility(board, move, state.to_move),
                      board=board, moves=moves)

    def utility(self, state, player):
        "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
        return if_(player == 'X', state.utility, -state.utility)

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h+1):
            for y in range(1, self.v+1):
                print board.get((x, y), '.'),
            print

    def compute_utility(self, board, move, player):
        "If X wins with this move, return 1; if O return -1; else return 0."
        if (self.k_in_row(board, move, player, (0, 1)) or
            self.k_in_row(board, move, player, (1, 0)) or
            self.k_in_row(board, move, player, (1, -1)) or
            self.k_in_row(board, move, player, (1, 1))):
            return if_(player == 'X', +1, -1)
        else:
            return 0

    def k_in_row(self, board, move, player, (delta_x, delta_y)):
        "Return true if there is a line through move on board for player."
        x, y = move
        n = 0 # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1 # Because we counted move itself twice
        return n >= self.k

class ConnectFour(TicTacToe):
    """A TicTacToe-like game in which you can only make a move on the bottom
    row, or in a square directly above an occupied square.  Traditionally
    played on a 7x6 board and requiring 4 in a row."""

    def __init__(self, h=7, v=6, k=4):
        TicTacToe.__init__(self, h, v, k)

    def actions(self, state):
        return [(x, y) for (x, y) in state.moves
                if y == 1 or (x, y-1) in state.board]

if __name__ =='__main__':
    play_game(ConnectFour(), alphabeta_player, query_player)
