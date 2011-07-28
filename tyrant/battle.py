
from tyrant.board import Board
from log import log_enabled, log

class Battle:
    def __init__(self, offense_deck, defense_deck, surge):
        self._surge = surge
        if log_enabled(): log("Setting up offense board")
        self._offense_board = Board(offense_deck)
        if log_enabled(): log("Setting up defense board")
        self._defense_board = Board(defense_deck)

    def is_offense_turn(self, turn):
        return (turn % 2 == 0 and not self._surge) or (turn % 2 == 1 and self._surge)

    def simulate(self):
        turn = 0
        commander_killed = False
        while turn <= 50 and not commander_killed:
            if self.is_offense_turn(turn):
                if log_enabled(): log("Turn " + str(turn) + " | Offense plays ------------------------")
                commander_killed = self._offense_board.play_random_turn(self._defense_board)
            else:
                if log_enabled(): log("Turn " + str(turn) + " | Defense plays ------------------------")
                commander_killed = self._defense_board.play_random_turn(self._offense_board)
            turn += 1
        if log_enabled():
            if commander_killed and self.is_offense_turn(turn - 1):
                log("OFFENSE wins")
            else:
                log("DEFENSE wins")

        return commander_killed and self.is_offense_turn(turn - 1)
