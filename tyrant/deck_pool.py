
import re
from tyrant.deck import Deck

class DeckPool:

    def __init__(self, file, collection):
        self._decks = []
        self._name = re.sub(r"\.deckpool$", "", file)
        self._name = re.sub(r"^.*/", "", self._name)
        self._path = re.sub(r"[^/]*$", "", file)

        
        f = open(file)

        for line in f:
            line = line.strip()
            if line == "" or line[0] == "#":
                continue

            deckfile = self._path + line
            self._decks.append(Deck(deckfile, collection))

    def name(self):
        return self._name

    def contents_summary(self):
        return "\n".join([deck.name() + ":     " + deck.contents_summary() for deck in self._decks])

    def decks(self):
        return self._decks
