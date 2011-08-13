
from tyrant.deck_versus_pool_test import DeckVersusPoolTest

class PoolVersusPoolTest:
    def __init__(self, offense_pool, defense_pool, surge, rounds):
        self._offense_pool = offense_pool
        self._defense_pool = defense_pool
        self._surge = surge
        self._rounds = rounds
        self._offense_wins = []
        self._defense_wins = []
        self._tests = []
        
    def run(self):
        for offense in self._offense_pool.decks():
            test = DeckVersusPoolTest(offense, self._defense_pool, self._surge, self._rounds)
            test.run()
            self._tests.append(test)

    def print_results(self):
        if self._surge:
            print "==== SURGING ===="
        else:
            print "==== FIGHTING ===="

        # for test in self._tests:
        #    test.print_individual_matchups()
        #    print ""

        self.print_top_offenses()
        print ""
        self.print_top_defenses()

    def print_top_offenses(self):
        print "Top Offenses:"
        decks_and_scores = [(self._offense_pool.decks()[i], self._tests[i].total_offense_wins(), self._tests[i].total_defense_wins()) for i in range(0, len(self._offense_pool.decks()))]
        self.print_decks_and_scores(decks_and_scores)

    def defense_decks_and_scores(self):
        decks_and_scores = []
        for i in range(0, len(self._defense_pool.decks())):
            offense_wins = 0
            defense_wins = 0           
            for test in self._tests:
                offense_wins += test.tests()[i].offense_wins()
                defense_wins += test.tests()[i].defense_wins()
            decks_and_scores.append((self._defense_pool.decks()[i], defense_wins, offense_wins))
        return decks_and_scores

    def print_top_defenses(self):
        print "Top Defenses:"
        self.print_decks_and_scores(self.defense_decks_and_scores())

    def score_for_tuple(self, tuple):
        return tuple[1] * 100.0 / (tuple[1] + tuple[2])
        
    def print_decks_and_scores(self, decks_and_scores):
        decks_and_scores = sorted(decks_and_scores, key=lambda tuple: tuple[2])
        for tuple in decks_and_scores:
            print "    " + str(round(self.score_for_tuple(tuple), 2)) + " - " + tuple[0].name() + ":    " + tuple[0].contents_summary()
        
    def print_best_overall_defenses(self, surge_test):
        print "==== OVERALL ===="
        print "Top Defenses - (Fight + 1.5 * Surge)/2.5:"
        fight_decks_and_scores = self.defense_decks_and_scores()
        surge_decks_and_scores = surge_test.defense_decks_and_scores()
        
        overall_decks_and_scores = []
        for i in range(0, len(fight_decks_and_scores)):
            fight_score = self.score_for_tuple(fight_decks_and_scores[i])
            surge_score = self.score_for_tuple(surge_decks_and_scores[i])
            score = fight_score + 1.5 * surge_score
            overall_decks_and_scores.append((fight_decks_and_scores[i][0], score, 250-score))
        self.print_decks_and_scores(overall_decks_and_scores)

    def print_top_defenses(self):
        print "Top Defenses:"
        decks_and_scores = []
        for i in range(0, len(self._defense_pool.decks())):
            offense_wins = 0
            defense_wins = 0            
            for test in self._tests:
                offense_wins += test.tests()[i].offense_wins()
                defense_wins += test.tests()[i].defense_wins()
            decks_and_scores.append((self._defense_pool.decks()[i], defense_wins, offense_wins))
        self.print_decks_and_scores(decks_and_scores)
