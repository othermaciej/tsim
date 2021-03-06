
from string import atoi
import re

from tyrant.card_collection import print_cards
from tyrant.card_aliases import CardAliases

class Deck:
    def __init__(self, file, collection):
        self._collection = collection
        self._commander = None
        self._cards = []
        self._name = re.sub(r"\.deck$", "", file)
        self._name = re.sub(r"^.*/", "", self._name)

        f = open(file)
        saw_legendary = False
        uniques = {}

        for line in f:
            line = line.strip()
            if line == "" or line[0] == "#":
                continue

            multiplier = 1
            multiplier_match = re.match("([0-9]*) *x +(.*)", line)
            if multiplier_match:
                multiplier = atoi(multiplier_match.group(1))
                line = multiplier_match.group(2)

            for i in range(multiplier):
                true_name = CardAliases.true_name(line)
                card = self._collection.card_by_name(true_name)
                if card == None:
                    raise Exception("Invalid deck", self._name + ": Unknown card " + line)

                if card.rarity() == "Legenary":
                    raise Exception("Invalid deck", self._name + ": Only one Legendary card allowed per deck")
                if card.type() == "commander":
                    if self._commander != None:
                        raise Exception("Invalid deck", self._name + ": Only one commander card allowed per deck")
                    self._commander = card
                else:
                    if card.unique():
                        if card.name() in uniques:
                            raise Exception("Invalid deck", self._name + ": Only one of Unique card " + card.name() + " allowed per deck")
                        else:
                            uniques[card.name()] = card
                    self._cards.append(card)

        if self._commander == None:
            raise Exception("Invalid deck", self._name + ": Deck must have a commander")

        if len(self._cards) > 10:
            raise Exception("Invalid deck", self._name + ": Deck must have no more than 10 cards")

    def name(self):
        return self._name

    def dump(self):
        print_cards("Commander", [self._commander], False)
        print_cards("Units", self._cards, False)

    def commander(self):
        return self._commander

    def cards(self):
        return self._cards

    def count_descriptor(self, name, count):
        return str(count) + "x " + name if count > 1 else name

    def contents_summary(self):
        counts = {}
        unique_cards = []
        for card in self._cards:
            count = counts.get(card, 0)
            if count == 0:
                unique_cards.append(card)
            counts[card] = count + 1

        name_list = [CardAliases.preferred_name(self._commander.name())]
        name_list.extend([self.count_descriptor(CardAliases.preferred_name(card.name()), counts[card]) for card in unique_cards])
        return  ", ".join(name_list)

