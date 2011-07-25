
from string import atoi
import re

from tyrant.card_collection import print_cards

class Deck:
    def __init__(self, file, collection):
        self._collection = collection
        self._commander = None
        self._cards = []

        f = open(file)
        saw_legendary = False
        uniques = {}

        for line in f:
            line = line.strip()
            if line == "" or line[0] == "#":
                continue

            multiplier = 1
            multiplier_match = re.match(r"([0-9]*) *x +(.*)", line)
            if multiplier_match:
                multiplier = atoi(multiplier_match.group(1))
                line = multiplier_match.group(2)

            for i in range(multiplier):
                card = self._collection.card_by_name(line)
                if card == None:
                    raise Exception("Invalid deck", "Unknown card " + line)

                if card.rarity() == "Legenary":
                    raise Exception("Invalid deck", "Only one Legendary card allowed per deck")
                if card.type() == "commander":
                    if self._commander != None:
                        raise Exception("Invalid deck", "Only one commander card allowed per deck")
                    self._commander = card
                else:
                    if card.unique():
                        if card.name() in uniques:
                            raise Exception("Invalid deck", "Only one of Unique card " + card.name() + " allowed per deck")
                        else:
                            uniques[card.name()] = card
                    self._cards.append(card)

        if self._commander == None:
            raise Exception("Invalid deck", "Deck must have a commander")

        if len(self._cards) > 10:
            raise Exception("Invalid deck", "Deck must have no more than 10 cards")
            
    def dump(self):
        print_cards("Commander", [self._commander], False)
        print_cards("Units", self._cards, False)

