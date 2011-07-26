
import random
from tyrant.card_in_play import CommanderCardInPlay, AssaultCardInPlay, StructureCardInPlay

def coin_toss():
    return random.randint(0, 1) == 1

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
            print "  Drew: {" + self._hand[-1].description() + "}"
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
            if card.is_active():
                self.perform_activation_skills(card, opposing_board)

    def activate_assault_units(self, opposing_board):
        for i in range(0, len(self._active_assault_units)):
            card = self._active_assault_units[i]
            if card.is_active():
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

    def assault_count(self):
        return len(self._active_assault_units)

    def perform_attack(self, index, attacker, opposing_board):
        # Attack Jammed = Attacker Immobilized = Attacker weakened to 0 > Swipe check = Flurry check > Fear >  Enfeeble = Valor > Flying = Antiair > Armored = Pierce > Immobilize = Poison > Count Damage > Crush > Defender Regenerate > Counter > Attacker Regenerate = Leech > Siphon > Flurry Repeat

        # FIXME need to implement Swipe and Flurry
        flurry = attacker.flurry()
        if flurry > 0 and coin_toss():
            attacks = flurry + 1
            print "    Flurry! performing " + str(attacks) + " total attacks"
            for i in range(1, attacks + 1):
                print "=== Attack #" + str(i) + " ==="
                self.perform_single_attack(index, attacker, opposing_board)
        else:
            self.perform_single_attack(index, attacker, opposing_board)

    def perform_single_attack(self, index, attacker, opposing_board):

        if attacker.is_dead():
            print "    Can't attack: {" + attacker.description() + "} is DEAD"
            return
        if attacker.is_jammed():
            print "    Can't attack: {" + attacker.description() + "} is JAMMED"
            return
        if attacker.is_immobilized():
            print "    Can't attack: {" + attacker.description() + "} is IMMOBILIZED"
            return
        if attacker.attack() <= 0:
            print "    Can't attack: {" + attacker.description() + "} has attack " + str(attacker.attack())
            return

        if attacker.fear():
            target = opposing_board.commander_target()
        else:
            target = opposing_board.target_for_index(index)

        damage = attacker.attack()
        print "    Base damage (including rally/weaken): " + str(damage)

        enfeebled = target.enfeebled()
        if enfeebled > 0:
            damage += enfeebled
            print "    Enfeeble bonus damage: " + str(enfeebled)

        valor = attacker.valor()
        if valor > 0 and self.assault_count() < opposing_board.assault_count():
            damage += valor
            print "    Valor bonus damage: " + str(valor)

        if target.flying():
            antiair = attacker.antiair()
            if antiair:
                damage += antiair
                print "    Antiair bonus damage: " + str(antiair)
            else:
                if coin_toss():
                    print "    Flying! Unit {" + attacker.description() + "} missed {" + target.description() + "}"
                    return

        armor = target.armored()
        if armor > 0:
            pierce = attacker.pierce()
            if pierce:
                print "    Armor reduced from " + str(armor) + " by pierce " + str(pierce)
                armor = max(0, armor - pierce)
            print "    Damage reduced by armor: " + str(armor)
            damage -= armor

        if damage <= 0:
            print "    Blocked: {" + attacker.description() + "} has modified damage " + str(attacker.attack())
            return

        if attacker.immobilize():
            if coin_toss():
                target.suffer_immobilize()
                print "    Immobilize! Unit {" + attacker.description() + "} immobilized {" + target.description() + "}"
    
        poison = attacker.poison()
        if poison > 0:
            target.suffer_poison(poison)
            print "    Poison! Unit {" + attacker.description() + "} inflicted " + str(poison) + " poison on target {" + target.description() + "}"

        target.take_damage(damage)
        print "    Unit {" + attacker.description() + "} did " + str(damage) + " attack damage to {" + target.description() + "}"

        crush = attacker.crush()
        if crush > 0 and target.is_dead():
            crush_target = opposing_board.commander_target()
            crush_target.take_damage(damage)
            print "    Crush! Unit {" + attacker.description() + "} did {" + str(damage) + "} crush damage to {" + crush_target.description() + "}"
            crush_target_regenerate = crush_target.regenerate()
            if crush_target.is_dead() and crush_target_regenerate > 0:
                if coin_toss():                
                    crush_target.perform_regenerate(crush_target_regenerate)
                    print "    Regenerate! Crush target unit {" + crush_target.description() + "} regenerated to " + str(crush_target_regenerate)

        target_regenerate = target.regenerate()
        if target.is_dead() and target_regenerate > 0:
            if coin_toss():                
                target.perform_regenerate(target_regenerate)
                print "    Regenerate! Unit {" + target.description() + "} regenerated to {" + str(target_regenerate) + "}"

        counter = target.counter()
        if counter > 0:
            attacker.take_damage(counter)
            print "    Unit {" + attacker.description() + "} suffered " + str(counter) + " counter damage from {" + target.description() + "}"

        attacker_regenerate = attacker.regenerate()
        if attacker.is_dead() and attacker_regenerate > 0:
            if coin_toss():                
                attacker.perform_regenerate(attacker_regenerate)
                print "    Regenerate! Attacker unit {" + attacker.description() + "} regenerated to " + str(attacker_regenerate)

        target_is_assault = target.type() == "assault"
        leech = attacker.leech()
        if leech > 0 and target_is_assault and not attacker.is_dead():
            attacker.heal(leech)
            print "    Leech! Unit {" + attacker.description() + "} leech healed " + str(leech)

        siphon = attacker.siphon()
        if siphon > 0 and target_is_assault:
            self._commander.heal(siphon)
            print "    Siphon! Commander {" + self._commander.description() + "} siphon healed " + str(siphon) + " by {" + attacker.description() + "}"

    def apply_poison(self):
        # FIXME: when exactly is poison applied?
        for card in self._active_assault_units:
            card.apply_poison()
            if card.poisoned() > 0:
                print "    Poison damage! Poisoned unit {" + card.description() + "} suffered " + str(card.poisoned()) + " poison damage"
            regenerate = card.regenerate()
            if card.is_dead() and regenerate > 0:
                if coin_toss():                
                    card.perform_regenerate(regenerate)
                    print "    Regenerate! Poisoned unit {" + card.description() + "} regenerated to " + str(regenerate)

    def bury_the_dead(self):
        for card in self._active_structures:
            if card.is_dead():
                self._active_structures.remove(card)
                print "    Removed dead structure card: {" + card.description() + "}"

        for card in self._active_assault_units:
            if card.is_dead():
                self._active_assault_units.remove(card)
                print "    Removed dead assault card: {" + card.description() + "}"

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
        print "  Playing card: {" + card_to_play.description() + "}"
        if card_to_play.type() == "action":
            self._active_action = card_to_play
        elif card_to_play.type() == "structure":
            self._active_structures.append(StructureCardInPlay(card_to_play))
        else:
            self._active_assault_units.append(AssaultCardInPlay(card_to_play))
