
import random
from tyrant.card_in_play import CommanderCardInPlay, AssaultCardInPlay, StructureCardInPlay

class Board:
    def __init__(self, deck):
        self._deck = deck
        self._commander = CommanderCardInPlay(deck.commander())
        self._draw_pile = deck.cards()[:]
        random.shuffle(self._draw_pile)
        self._hand = []
        self._active_structures = []
        self._active_assault_units = []
        self._active_action = None

    def draw(self):
        print "  About to draw - draw pile size is " + str(len(self._draw_pile))
        if self._draw_pile:
            self._hand.append(self._draw_pile.pop())
            print "  Drew: " + self._hand[-1].description()
            print "   - hand size is now " + str(len(self._hand))

    def tick_timers(self):
        print "  Ticking timers"
        for card in self._active_structures:
            card.tick()
        for card in self._active_assault_units:
            card.tick()

    def activate_action(self, opposing_board):
        if self._active_action:
            self.perform_activation_skills(self._active_action, opposing_board)

    def activate_commander(self, opposing_board):
        self.perform_activation_skills(self._commander, opposing_board)

    def activate_structures(self, opposing_board):
        for card in self._active_structures:
            if card.delay() == 0:
                self.perform_activation_skills(card, opposing_board)

    def activate_assault_units(self, opposing_board):
        for i in range(0, len(self._active_assault_units)):
            card = self._active_assault_units[i]
            if card and card.delay() == 0:
                self.perform_activation_skills(card, opposing_board)
                self.perform_attack(i, card, opposing_board)

    def reset_status(self):
        for card in self._active_assault_units:
            card.reset_status()

    def activate_cards(self, opposing_board):
        print "  Activating cards"
        self.activate_action(opposing_board)
        self.activate_commander(opposing_board)
        self.activate_structures(opposing_board)
        self.activate_assault_units(opposing_board)

    def perform_activation_skills(self, card, opposing_board):
        # XXX
        # Enfeeble, Heal, Jam, Mimic, Rally, Siege, Strike, Weaken
        # Account for: Evade, Payback, Regenerate
        return False

    def commander_target(self):
        for card in self._active_structures:
            if card.is_wall() and not card.is_dead():
                return card
        return self._commander

    def target_for_index(self, index):
        if len(self._active_assault_units) <= index:
            return self.commander_target()
        target = self._active_assault_units[index]
        if not target or target.is_dead():
            return self.commander_target()
        return target

    def perform_attack(self, index, card, opposing_board):
        # Attack Jammed = Attacker Immobilized > Flurry check > Flying = Antiair > Armored = Pierce > Immobilize = Poison > Count Damage > Crush > Defender Regenerate > Counter > Attacker Regenerate = Leech > Siphon > Flurry Repeat
        # Swipe, Valor?
        if card.is_jammed():
            return
        if card.is_immobilized():
            return
        if card.attack() == 0:
            return

        target = opposing_board.target_for_index(index)
        target.take_damage(card.attack())

        print "    Unit " + card.description() + " did " + str(card.attack()) + " damage to " + target.description() 

        
    def apply_poison(self):
        # FIXME: when exactly is poison applied?
        return False

    def bury_the_dead(self):
        for card in self._active_structures:
            if card.is_dead():
                print "    Removing dead structure card: " + card.description()
                self._active_structures.remove(card)

        for card in self._active_assault_units:
            if card.is_dead():
                print "    Removing dead assault card: " + card.description()
                self._active_assault_units.remove(card)

    def clean_up(self, opposing_board):
        print "  Cleaning up"
        self.bury_the_dead()
        opposing_board.bury_the_dead()
        self.action_card = None
        self.reset_status();

    def commander(self):
        return self._commander
    
    def play_random_turn(self, opposing_board):
        self.apply_poison()
        self.tick_timers()
        while len(self._hand) < 3 and self._draw_pile: 
            self.draw()
        if self._hand:
            self.play_from_hand(random.randint(0, len(self._hand) - 1))
        self.activate_cards(opposing_board)
        self.clean_up(opposing_board)
        return opposing_board.commander().is_dead()

    def play_from_hand(self, index):
        card_to_play = self._hand[index]
        self._hand.remove(card_to_play)
        print "  Playing card: " + card_to_play.description()
        if card_to_play.type() == "action":
            self._active_action = card_to_play
        elif card_to_play.type() == "structure":
            self._active_structures.append(StructureCardInPlay(card_to_play))
        else:
            self._active_assault_units.append(AssaultCardInPlay(card_to_play))
