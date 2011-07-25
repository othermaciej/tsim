
from tyrant.card_file_parser import parse_card_file

def print_cards(label, cardList, showCount = True):
    print label + ":" + (" " + str(len(cardList)) if showCount else "")
    for card in cardList:
        print "    " + card.description()

class CardCollection:
    def __init__(self, filename):
        self._cards = parse_card_file(filename)
        self._cards_by_name = dict([(card.name(), card) for card in self._cards])

    def card_by_name(self, name):
        if name not in self._cards_by_name:
            return None
        return self._cards_by_name[name]

    def dump(self):
        commanderCards = [card for card in self._cards if card.type() == "commander"]
        assaultCards = [card for card in self._cards if card.type() == "assault"]
        structureCards = [card for card in self._cards if card.type() == "structure"]
        actionCards = [card for card in self._cards if card.type() == "action"]

        print_cards("Commander Cards", commanderCards)
        print_cards("Assault Cards", assaultCards)
        print_cards("Structure Cards", structureCards)
        print_cards("Action Cards", actionCards)

