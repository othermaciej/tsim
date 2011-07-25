
from tyrant.board import Board

class Battle:
    def __init__(self, offense_deck, defense_deck, surge):
        self._surge = surge
        print "Setting up offense board"
        self._offense_board = Board(offense_deck)
        print "Setting up defense board"
        self._defense_board = Board(defense_deck)

    def is_offense_turn(self, turn):
        return (turn % 2 == 0 and not self._surge) or (turn % 2 == 1 and self._surge)

    def simulate(self):
        turn = 0
        commander_killed = False
        while turn <= 50 and not commander_killed:
            print "Turn " + str(turn)
            if self.is_offense_turn(turn):
                print "Offense plays..."
                commander_killed = self._offense_board.play_random_turn(self._defense_board)
            else:
                print "Defense plays..."
                commander_killed = self._defense_board.play_random_turn(self._offense_board)
            turn += 1
        return commander_killed and self.is_offense_turn(turn - 1)
