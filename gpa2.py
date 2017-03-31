"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random

class Node(object):
    """Node in a tree"""
    def __init__(self, location, game, right = None, parent = None, children=None):
        self.location = location
        self.game = game
        self.parent = parent
        self.children = children
        self.right = right
        self.left = None
        self.score = None
    # def __lt__(self, other):
    #     return self.score < other.score
    # def __gt__(self, other):
    #     return self.score > other.score
    # def __eq__(self, other):
    #     try:
    #         result = self.score == other.score
    #     except:
    #         result = self == None
    #     return result
    # def __le__(self, other):
    #     return not self.__gt__(other)
    # def __ge__(self, other):
    #     return not self.__lt__(other)
    # def __ne__(self, other):
    #     return not self.__eq__(other)

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    num_of_opponent_legal_moves = len(game.get_legal_moves(game.get_opponent(player)))
    num_of_player_legal_moves = len(game.get_legal_moves())
    num_of_blank_spaces = len(game.get_blank_spaces())
    
    #Heuristic 1
    # - Moves availble by opponent
    h1 = 8-num_of_opponent_legal_moves
    return float(h1)

    # Heuristic 2
    # Moves availble by player(Self)
    h2 = num_of_player_legal_moves
    return float(h2)

    # Heuristic 3
    # Moves availble by player(Self) - Moves availble by opponent  
    h3 = h2 - h1
    return float(h3)
    
    # Heuristic 4
    # Moves availble by player(Self) / Total blank squares
    h4 = num_of_player_legal_moves/num_of_blank_spaces
    return float(h4)

    # Heuristic 5
    # - Moves availble by opponent / Total blank squares 
    h5 = num_of_opponent_legal_moves/num_of_blank_spaces
    return float(h5)

    # Heuristic 6
    # Moves availble by player(Self) / Total blank squares - Moves availble by opponent / Total blank squares 
    h6 = h4 - h5
    return float(h6)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left
    
        # return immediately if there are no legal moves
        if legal_moves == []:
            return (-1,-1)

        # Initial move from the game board (i.e., an opening book)
        if game.move_count < 3:
            if game.move_is_legal((int(game.height/2), int(game.width/2))):
                best_move = ((int(game.height/2), int(game.width/2)))
            else:
                best_move = (1, 1)
            return best_move
        
        # The try/except block will automatically catch the exception raised
        # by the search method when the timer gets close to expiring to
        # avoid timeout. 
        try:
            # The search method call (alpha beta or minimax) happen in here
            if self.iterative:
                for i in range(self.search_depth):
                    score, best_move = self.__search(game=game, depth=i , maximizing_player=True,  alpha=float("-inf"), beta=float("inf"))
            else:
                score, best_move = self.__search(game=game, depth= self.search_depth, maximizing_player=True,  alpha=float("-inf"), beta=float("inf"))
            
        except Timeout:
            # Handle any actions required at timeout, if necessary
            return best_move

        # Return the best move from the last completed search iteration
        return best_move

    def __search(game, depth, maximizing_player=True,  alpha=float("-inf"), beta=float("inf")):
        if self.method == "minimax":
            score, best_move = self.minimax(game=game, depth = depth, maximizing_player=maximizing_player)
        elif self.method == "alphabeta":
            score, best_move = self.alphabeta(game=game, depth= depth, alpha=alpha, beta=beta, maximizing_player=maximizing_player)
        else:
            raise NameError('No method named {}'.format(self.method))
        return score, best_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        
        location = game.get_player_location(game.active_player)
        game_tree = Node(location, game)
        current_node = self.update_branches(game_tree)
        current_depth = 0
        # build game tree for certain depth (Top-down)
        while current_depth < depth:
            for i, n in enumerate(current_node.children):
                current_node.children[i] = self.update_branches(n)
            print(current_node.children)
            if current_node.right != None:
                current_node = current_node.right
            else:
                while current_node.left != None:
                    current_node = current_node.left
                current_node = current_node.children[0]
                max_flag = not maximizing_player
                current_depth += 1

        # assign minimax game tree for certain depth (Bottom-up)

        #Set leaf scores
        while True:
            current_node.score = custom_score(current_node.game, current_node.game.active_player)
            if current_node.right != None:
                current_node = current_node.right
            else:
                while current_node.left != None:
                    current_node = current_node.left
                if  current_node.parent != None:
                    current_node = current_node.parent
                break
        
        

        #Set node scores
        while current_node.parent != None:
            print([n.score for n in current_node.children])
            if max_flag:
                current_node.score = max([n.score for n in current_node.children])
            else:
                current_node.score = min([n.score for n in current_node.children])


            if current_node.right != None:
                current_node = current_node.right
            else:
                while current_node.left != None:
                    current_node = current_node.left
                if  current_node.parent != None:
                    current_node = current_node.parent
                    max_flag = not max_flag

        #Choose best answer node
        if maximizing_player:
            print([n.score for n in current_node.children])
            best_choice =  max([n.score for n in current_node.children])
        else:
            best_choice =  min([n.score for n in current_node.children])
        return best_choice.score, best_choice.location

    def update_branches(self, current_node):
        parent = current_node
        game = current_node.game.forecast_move(current_node.location)
        moves = game.get_legal_moves()
        moves.reverse()
        children = []
        for i,move in enumerate(moves):
            try:
                children.append(Node(move, game, current_node, children[i-1], parent))
            except:
                children.append(Node(move, game, current_node, None, parent))
        for child in children:
            try:
                child.left = children[i+1]
            except:
                pass
        current_node.children = children
        current_node.children.reverse()
        return current_node

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        location = game.get_player_location(game.active_player)
        game_tree = Node(location, game)
        current_node = self.update_branches(game_tree)
        current_depth = 0

        while current_depth < depth:
            current_depth += 1
            current_node = current_node.children[0]
            maximizing_player = not maximizing_player
            current_node = self.update_branches(current_node)
        for node in current_node.parent.children:
            current_node.score = custom_score(current_node.game, current_node.game.active_player)
        maximizing_player = not maximizing_player
        current_node = current_node.parent

        #TODO: Implement Pruning 

        #Set node scores
        while current_node.parent != None:
            if maximizing_player:
                current_node.score = max([n.score for n in current_node.children])
            else:
                current_node.score = min([n.score for n in current_node.children])
            if current_node.right != None:
                current_node = current_node.right
            else:
                while current_node.left != None:
                    current_node = current_node.left
                current_node = current_node.parent
                max_flag = not max_flag

        #Choose best answer node
        if maximizing_player:
            best_choice =  max(current_node.children)
        else:
            best_choice =  min(current_node.children)
        return best_choice.score, best_choice.location