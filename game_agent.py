"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random

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
    def heuristic_one(game, player):
        """
        Heuristic 1: Moves availble by player/Moves availble by opponent 
        """
        return float(len(game.get_legal_moves()))

    def heuristic_two(game, player):
        """
        Heuristic 2: Moves availble by player/Moves availble by opponent 
        """
        num_of_player_legal_moves = len(game.get_legal_moves())
        num_of_opponent_legal_moves = len(game.get_legal_moves(game.get_opponent(player)))
        return float(num_of_player_legal_moves+1)/float((num_of_opponent_legal_moves)+1)

    def heuristic_three(game, player):
        """
        Heuristic 3: Manhattan distance between agents
        """
        player_loc = game.get_player_location(player)
        opponent_loc = game.get_player_location(game.get_opponent(player))
        h3 = abs(player_loc[0]-opponent_loc[0]) + abs(player_loc[1]-opponent_loc[1])
        return float(h3)

    def heuristic_fourth(game, player):
        """
        Heuristic 4: Weight the number of moves left to the player with their respective position on the board
        """
        num_of_opponent_legal_moves = len(game.get_legal_moves(game.get_opponent(player)))
        player_loc = game.get_player_location(player)
        return float(num_of_opponent_legal_moves * abs(player_loc[0]-player_loc[1])*game.width)

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return (heuristic_one(game, player))
    #return (heuristic_two(game, player))
    #return (heuristic_three(game, player))
    #return (heuristic_fourth(game, player))

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
        def shift_values(x): return x+1
        self.time_left = time_left
        best_move = (-1,-1)
        # return immediately if there are no legal moves
        if len(legal_moves) == 0: return best_move

        # Initial move from the game board (i.e., an opening book)
        # if game.move_count < 2:
        #     return random.choice(legal_moves)
        if game.move_count < 2:
            center = (game.height/2, game.width/2) 
            if (center in legal_moves):
                best_move = center
            else:
                best_move = legal_moves[random.randint(0,len(legal_moves)-1)]
            return best_move
        
        # The try/except block will automatically catch the exception raised
        # by the search method when the timer gets close to expiring to
        # avoid timeout. 
        try:
            if self.iterative:
                depth = 1
                while True:
                    if self.method == "minimax":
                        result, best_move = self.minimax(game, depth)
                    else:
                        result, best_move = self.alphabeta(game, depth)
                    depth += 1
            else:
                if self.method == "minimax":
                    result, best_move = self.minimax(game, self.search_depth)
                else:
                    result, best_move = self.alphabeta(game, self.search_depth)
        except Timeout:
            pass
        return best_move

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

        # when no legal moves available
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return self.score(game, self), (-1, -1)

        # when depth is zero, reaching the end of tree
        if depth <= 0:
            return self.score(game, self), (-1, -1)

        if maximizing_player:
            max_value = float("-inf")
            current_max_move = (-1, -1)
            for move in legal_moves:
                score, _ = self.minimax(game.forecast_move(move), depth-1, not maximizing_player)
                current_max_move = move if score > max_value else current_max_move
                max_value = score if score > max_value else max_value
            return max_value, current_max_move
        else:
            min_value = float("inf")
            current_min_move = (-1, -1)
            for move in legal_moves:
                score, _ = self.minimax(game.forecast_move(move), depth-1, not maximizing_player)
                current_min_move = move if score < min_value else current_min_move
                min_value = score if score < min_value else min_value
            return min_value, current_min_move
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

        # when no legal moves available
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return self.score(game, self), (-1, -1)

        # when depth is zero, reaching the end of tree
        if depth <= 0:
            return self.score(game, self), (-1, -1)
        

        if maximizing_player:
            max_value = float("-inf")
            current_max_move = (-1, -1)
            for move in legal_moves:
                score, _ = self.alphabeta(game.forecast_move(move), depth-1, alpha, beta, not maximizing_player)
                current_max_move = move if score > max_value else current_max_move
                max_value = score if score > max_value else max_value
                alpha = max_value if max_value > alpha else alpha
                if beta <= alpha: break
            return max_value, current_max_move
        else:
            min_value = float("inf")
            current_min_move = (-1, -1)
            for move in legal_moves:
                score, loc = self.alphabeta(game.forecast_move(move), depth-1, alpha, beta, not maximizing_player)
                current_min_move = move if score < min_value else current_min_move
                min_value = score if score < min_value else min_value
                beta = min_value if min_value < beta else beta
                if beta <= alpha: break
            return min_value, current_min_move