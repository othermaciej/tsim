
from tyrant.deck_versus_deck_test import DeckVersusDeckTest

class DeckVersusPoolTest:
    def __init__(self, offense, defense_pool, surge, rounds):
        self._offense = offense
        self._defense_pool = defense_pool
        self._surge = surge
        self._rounds = rounds
        self._offense_wins = []
        self._defense_wins = []
        self._tests = []
        
    def run(self):
        for defense in self._defense_pool.decks():
            test = DeckVersusDeckTest(self._offense, defense, self._surge, self._rounds)
            test.run()
            self._tests.append(test)

    def print_results(self):
        if self._surge:
            print "==== SURGING ===="
        else:
            print "==== FIGHTING ===="

        total_offense_wins = 0
        total_defense_wins = 0
        for test in self._tests:
            print test.summary_line()
            total_offense_wins += test.offense_wins()
            total_defense_wins += test.defense_wins()
        print "Overall " + ("Surge" if self._surge else "Fight") + " offense rating for " + self._offense.name() + ": " + str(total_offense_wins * 100.0 / (total_offense_wins + total_defense_wins)) + "%"

        
