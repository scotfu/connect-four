#-*- coding:utf-8-*-
import pprint
from copy import deepcopy

WIDTH = 4
HEIGHT = 5
HUMAN='human'
AI='ai'
infinity = 1.0e400



def if_(test, result, alternative):
    """Like C++ and Java's (test ? result : alternative), except
    both result and alternative are always evaluated. However, if
    either evaluates to a function, it is applied to the empty arglist,
    so you can delay execution by putting it in a lambda.
    >>> if_(2 + 2 == 4, 'ok', lambda: expensive_computation())
    'ok'
    """
    if test:
        if callable(result): return result()
        return result
    else:
        if callable(alternative): return alternative()
        return alternative

def query_player(game, state):
    "Make a move by querying standard input."
    game.display(state)
    x = num_or_str(raw_input('Your move? '))
    print 'query player move at',x
    return x

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
                return game.utility(state, game.to_move(game.initial))

class Struct:
    """Create an instance with argument=value slots.
    This is for making a lightweight object whose class doesn't matter."""
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __cmp__(self, other):
        if isinstance(other, Struct):
            return cmp(self.__dict__, other.__dict__)
        else:
            return cmp(self.__dict__, other)

    def __repr__(self):
        args = ['%s=%s' % (k, repr(v)) for (k, v) in vars(self).items()]
        return 'Struct(%s)' % ', '.join(args)


    
class Game:

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



def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state,player):
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
        for a in game.actions(state,player):
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
    return argmax(game.actions(state,state.to_move),
                  lambda a: min_value(game.result(state, a),
                                      -infinity, infinity, 0))

def argmax(seq, fn):
    """Return an element with highest fn(seq[i]) score; tie goes to first one.
    >>> argmax(['one', 'to', 'three'], len)
    'three'
    """
    return argmin(seq, lambda x: -fn(x))

def argmin(seq, fn):
    """Return an element with lowest fn(seq[i]) score; tie goes to first one.
    >>> argmin(['one', 'to', 'three'], len)
    'to'
    """
    best = seq[0]; best_score = fn(best)
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score
    return best

def make_board():
    board=[]
    for x in range(0,WIDTH):
        board.append([])
    return board


class C4(Game):
    def __init__(self):
        board = make_board()
        self.initial = Struct(to_move='X',utility=0,board=board)    
        self.k=4

    def actions(self,state,player):
        actions=[]
        for i in range(0,WIDTH):
            if len(state.board[i])< HEIGHT:
                actions.append(('add',i))
        for j in range(0,WIDTH):
            try:
                if state.board[j][1] == player:
                    actions.append(('remove',j))
            except:
                pass
        return actions


    def result(self,state, move):
        if move not in self.actions(state,state.to_move):
            return state #illegal move has no effect
        board = deepcopy(state.board)
        if move[0]=='add':
            board[move[1]].append(state.to_move)
        else:
            board[move[1]].pop(0)
        return Struct(to_move=if_(state.to_move == 'X', 'O', 'X'),
                      utility=self.compute_utility(board, move, state.to_move),board=board)



    def make_move(board,player,move):
        if move[0] == 'remove':
            if board[move[1]][0] == player:
                board[move[1]].remove(player)
            else:
                print 'something is wrong'
        if type == 'add':
            if len(board[move[1]]) < HEIGHT:
                board[move[1]].append(player)
            else:
                print 'something is wrong'

    def display(self):
        board=deepcopy(self.state)
        for y in range(0,HEIGHT):
            for x in range(0,WIDTH):
                try:
                    board[x][y]
                except:
                    board[x].append(None)
        print '\n---------------------------'
        for y in range(HEIGHT-1,-1,-1):
            for x in range(0,WIDTH):
                print board[x][y],'|',
            print '\n---------------------------'    
            
    def utility(self, state, player):
        "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
        return if_(player == 'X', state.utility, -state.utility)

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        return state.utility != 0 or len(game.actions(state.to_move)) == 0



    def compute_utility(self, board, player):
        "If player has k in a row return k"


    def k_in_row(self, board,player, (delta_x, delta_y)):
        "Return true if there is a line through move on board for player."
        n = 0 # n is number of moves in row
        while board[(x, y)] == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board[(x, y)] == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1 # Because we counted move itself twice
        return n 


if __name__ == '__main__':
    play_game(C4(), alphabeta_player, query_player)


