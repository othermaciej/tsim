
from tyrant.battle import Battle

class DeckVersusDeckTest:
    def __init__(self, offense, defense, surge, rounds):
        self._offense = offense
        self._defense = defense
        self._surge = surge
        self._rounds = rounds
        self._offense_wins = 0
        self._defense_wins = 0
        
    def run(self):
        for i in range(0, self._rounds):
            battle = Battle(self._offense, self._defense, self._surge)
            offense_won = battle.simulate()
            if offense_won:
                self._offense_wins += 1
            else:
                self._defense_wins += 1

    def summary_line(self):
        return  "  Offense \"" + self._offense.name() + "\" wins " + str(self._offense_wins * 100.0 / self._rounds) + "%, " + "Defense \"" + self._defense.name() + "\" wins " + str(self._defense_wins * 100.0 / self._rounds) + "% "

    def offense_wins(self):
        return self._offense_wins

    def defense_wins(self):
        return self._defense_wins

    def print_results(self):
        if self._surge:
            print "==== SURGING ===="
        else:
            print "==== FIGHTING ===="
        print self.summary_line()

