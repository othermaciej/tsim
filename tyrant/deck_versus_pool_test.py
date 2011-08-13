
from tyrant.deck_versus_deck_test import DeckVersusDeckTest

class DeckVersusPoolTest:
    def __init__(self, offense, defense_pool, surge, rounds):
        self._offense = offense
        self._defense_pool = defense_pool
        self._surge = surge
        self._rounds = rounds
        self._tests = []
        self._total_offense_wins = 0
        self._total_defense_wins = 0
        
    def run(self):
        for defense in self._defense_pool.decks():
            test = DeckVersusDeckTest(self._offense, defense, self._surge, self._rounds)
            test.run()
            self._tests.append(test)
            self._total_offense_wins += test.offense_wins()
            self._total_defense_wins += test.defense_wins()

    def total_offense_wins(self):
        return self._total_offense_wins

    def total_defense_wins(self):
        return self._total_defense_wins

    def tests(self):
        return self._tests

    def print_individual_matchups(self):
        for test in self._tests:
            print test.summary_line()


    def print_results(self):
        if self._surge:
            print "==== SURGING ===="
        else:
            print "==== FIGHTING ===="

        total_off_wins = self._total_offense_wins
        total_def_wins = self._total_defense_wins

        self.print_individual_matchups()

        print "Overall " + ("Surge" if self._surge else "Fight") + " offense rating for " + self._offense.name() + ": " + str(total_off_wins * 100.0 / (total_off_wins + total_def_wins)) + "%"

        
