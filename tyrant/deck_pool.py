
import re
from tyrant.deck import Deck

class DeckPool:

    def __init__(self, file, collection):
        self._decks = []
        self._name = re.sub(r"\.deckpool$", "", file)
        
        f = open(file)

        for line in f:
            line = line.strip()
            if line == "" or line[0] == "#":
                continue

            self._decks.append(Deck(line, collection))

    def name(self):
        return self._name

    def contents_summary(self):
        return "\n".join([deck.name() for deck in self._decks])

    def decks(self):
        return self._decks
