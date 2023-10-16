from math import sqrt, log
from time import time
from random import shuffle, choice
from typing import Union, Dict, List, Any


Move = Any # MCTS does not care about the contents of a move; it merely passes the output of get_legal_moves() to make_move(), both of which are handled by the user.
Team = Union[int,str]
Rewards = Dict[Team,float]


class GameState:
    def get_current_team(self) -> Team:
        """The identifier of the current player's team."""
        raise NotImplementedError("GameState must implement get_current_team.")

    def get_legal_moves(self) -> List[Move]:
        """List of all legal moves from this state."""
        raise NotImplementedError("GameState must implement get_legal_moves.")

    def make_move(self, move:Move) -> 'GameState':
        """A new GameState--the result of applying the given move to this state.
        Note: The current state (self) should NOT be modified. Rather, modify a copy of it.
        """
        raise NotImplementedError("GameState must implement make_move.")

    def is_terminal(self) -> bool:
        """Is the game over?"""
        raise NotImplementedError("GameState must implement is_terminal.")

    def get_reward(self) -> Union[float,Rewards]:
        """The reward earned by the team that played the game-ending move (the "terminal team", or the team from the previous state).
        Typically 1 for win, -1 for loss, 0 for draw.
        Alternatively, returns a dict of teams/rewards: {team1:reward1, team2:reward2, ...}
        Note: This method is only called on terminal states.
        """
        raise NotImplementedError("GameState must implement get_reward.")


class Node:
    """Represents a game state node in the MCTS search tree.
    Args:
        state (GameState): The game state at the current node.
        parent (Node): The parent of the current node in the search tree.
        move (Move): The move that was played from the parent node to get to this node.
    Attributes:
        children (List[Node]): The child nodes of the current node. These represent legal moves that have been visited.
        visits (int): The number of times the node has been visited.
        rewards (dict): All teams' rewards obtained from simulations through the node. Keys are teams; values are rewards.
        is_terminal (bool): Whether the node represents a terminal state.
        is_fully_expanded (bool): Whether all children of the node have been visited.
        remaining_moves (list): A list of moves that have not yet been tried.
    """
    def __init__(self, state:GameState, parent:'Node'=None, move:Move=None):
        self.state = state
        self.parent = parent
        self.move = move

        self.children:List['Node'] = []
        self.visits = 0
        self.rewards = {}
        self.is_terminal = self.state.is_terminal()
        self.is_fully_expanded = self.is_terminal
        if self.is_fully_expanded:
            self.remaining_moves = []
        else:
            self.remaining_moves = self.state.get_legal_moves()
            shuffle(self.remaining_moves)

        # The following are cached for performance.
        self.team = self.state.get_current_team()
        if self.parent is not None:
            self.rewards[self.parent.team] = 0
        self.sqrtlog_visits = 0
        self.invsqrt_visits = 0
        self.avg_reward = 0

    def apply_rewards(self, rewards:Rewards):
        """Update this node's visits and rewards, and cache some variables for more efficient UCB calculation."""
        self.visits += 1

        self.sqrtlog_visits = sqrt(log(self.visits))
        self.invsqrt_visits = 1 / sqrt(self.visits)

        total_rewards = 0
        for k,v in rewards.items():
            if k not in self.rewards:
                self.rewards[k] = 0
            self.rewards[k] += v
            total_rewards += self.rewards[k]

        if self.parent is not None:
            # Average reward is (reward for my parent's team - rewards for all other teams) / num visits to this node.
            self.avg_reward = ((2 * self.rewards[self.parent.team]) - total_rewards) / self.visits

    def ucb(self, exploration_bias:float, parent_sqrtlog_visits:float):
        """Upper Confidence Bound
        ucb = (x / n) + C * sqrt(ln(N) / n)
        x=reward for this node
        n=number of simulations for this node
        N=number of simulations for parent node
        C=exploration bias
        """
        # ucb = avgR + C * sqrt(ln(N)) * (1/sqrt(n))
        return self.avg_reward + exploration_bias * parent_sqrtlog_visits * self.invsqrt_visits


class MCTS:
    def __init__(self, exploration_bias:float=1.414):
        """Initializes an MCTS agent.
        Args:
            exploration_bias (float): The exploration bias, which balances exploration (favoring untested moves) and exploitation (favoring good moves).
                The default √2 is often used in practice. However, the optimal value depends on the game and is usually found by experimentation.
        """
        self.exploration_bias = exploration_bias

    def search(self, state:GameState, *, max_time:Union[int,float]=None, max_iterations:int=None, heuristic=None, return_type:str="state") -> Union[GameState,Move,Node]:
        """Searches for this state's best move until some limit has been reached.
        Args:
            state (GameState): The game state for which to find the best move.
            max_time (int|float): The maximum time to search, in seconds.
            max_iterations (int): The maximum number of selections/simulations to perform.
            heuristic (callable): A function that takes a state and returns a move. See simulate() for more information.
            return_type (str): One of "state", "move", or "node".
        Returns:
            GameState: A new game state which is the result of applying the best move to the given state.
        """
        return_type = return_type.lower()
        VALID_RETURN_TYPES = {"state","move","node"}
        if return_type not in VALID_RETURN_TYPES:
            raise ValueError(f'Invalid return type: {return_type}, must be one of {VALID_RETURN_TYPES}')

        if max_time is None and max_iterations is None:
            raise ValueError("One or more of max_time/max_iterations is required.")

        node = Node(state)

        if max_time is not None:
            end_time = time() + max_time
        if max_iterations is not None:
            i = 0

        while True:
            child = self.select(node)
            rewards = self.simulate(child, heuristic=heuristic)
            self.backpropagate(child, rewards)

            # If there is only one legal move, we don't need to search.
            if node.is_fully_expanded and len(node.children) == 1:
                break

            if max_time is not None:
                if time() >= end_time:
                    break
            if max_iterations is not None:
                i += 1
                if i >= max_iterations:
                    break

        best = self.get_best_child(node)

        if return_type == "state":
            return best.state
        elif return_type == "move":
            return best.move
        elif return_type == "node":
            return best

    def select(self, node:Node) -> Node:
        """Step 1: Selection
        Traverse the tree for the node we most want to simulate.
        Looks for an unexplored child of this node's best child's best child's...best child.
        """
        while not node.is_terminal:
            if not node.is_fully_expanded:
                return self.expand(node)
            else:
                node = self.get_best_child(node)
        return node

    def expand(self, node:Node) -> Node:
        """Step 2: Expansion
        Add a new child to this node.
        """
        move = node.remaining_moves.pop()
        if len(node.remaining_moves) == 0:
            node.is_fully_expanded = True

        child = Node(state=node.state.make_move(move), parent=node, move=move)
        node.children.append(child)

        return child

    def simulate(self, node:Node, heuristic=None) -> Rewards:
        """Step 3: Simulation (aka playout/rollout)
        Play out a game, from the given node to termination, and return the final reward.
        A heuristic function may be used to guide the simulation. Otherwise, moves are chosen randomly.
        Args:
            node (Node): The node from which to begin the simulation.
            heuristic (callable): A function that takes a state and returns a move.
        """
        state = node.state

        terminal_team = None
        if node.is_terminal:
            terminal_team = node.parent.team
        else:
            while not state.is_terminal():
                terminal_team = state.get_current_team()
                if heuristic is not None:
                    move = heuristic(state)
                else:
                    move = choice(state.get_legal_moves())
                state = state.make_move(move)

        reward = state.get_reward()
        if not isinstance(reward, dict):
            reward = {terminal_team: reward}

        return {k:v for k,v in reward.items() if v!=0}

    def backpropagate(self, node:Node, rewards:Rewards):
        """Step 4: Backpropagation
        Update all ancestors with the reward from this terminal node.
        """
        while node is not None:
            node.apply_rewards(rewards)
            node = node.parent

    def get_best_child(self, node:Node) -> Node:
        """Find the child with the highest Upper Confidence Bound (UCB)."""
        parent_sqrtlog_visits = node.sqrtlog_visits
        best_score = float('-inf')

        for child in node.children:
            ucb = child.ucb(self.exploration_bias, parent_sqrtlog_visits)
            if ucb > best_score:
                best_score = ucb
                best_child = child

        return best_child


if __name__ == "__main__":
    class Score10(GameState):
        def __init__(self, player=1, score=-4):
            self.player = player
            self.score = score
        def get_current_team(self): return self.player
        def get_legal_moves(self): return list(range(-9,10))
        def make_move(self, move): return Score10(-1*self.player, self.score+move)
        def is_terminal(self): return abs(self.score) >= 10
        def get_reward(self): return -1 * self.player * self.score
        def __repr__(self): return f'{str(self.score).rjust(3)} : {"pos" if self.player==1 else "neg"} to play'
    mcts = MCTS()
    state = Score10()
    while not state.is_terminal():
        move = mcts.search(state, max_iterations=100, return_type="move")
        print(state, f'(chose {move})')
        state = state.make_move(move)
    print(state)
