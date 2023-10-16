cdef class GameState:
    def get_current_team(self)
    def get_legal_moves(self)
    def make_move(self, move)
    def is_terminal(self)
    def get_reward(self)
    def simulate(self)
