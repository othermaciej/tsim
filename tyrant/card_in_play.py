
from string import join
from random import getrandbits

from log import log_enabled, log


def coin_toss():
    "Return True 50% of the time"
    return getrandbits(1) == 1

class CardInPlay:
    def __init__(self, card):
        self._card = card
        self._cur_health = card.health()

    def name(self):
        return self._card.name()

    def type(self):
        return self._card._type

    def health(self):
        return self._cur_health

    def take_damage(self, amount):
        self._cur_health -= amount
        died = self._cur_health <= 0
        regenerate = self.regenerate()
        if died:
            # make dead cards appear to have a very large cooldown,
            # to reduce the need to check in quite so many places
            # whether a card is dead.
            self._cur_cd = 999
            if regenerate > 0 and coin_toss():                
                if log_enabled(): log("        Regenerate! Unit {" + self.description() + "} will regenerate to " + str(regenerate))
                self.perform_regenerate(regenerate)

    def heal(self, amount):
        self._cur_health = min(self._card._health, self._cur_health + amount)

    def perform_regenerate(self, amount):
        self._cur_health = amount

    def suffer_immobilize(self):
        pass

    def suffer_poison(self, amount):
        pass

    def is_dead(self):
        return self._cur_health <= 0

    def is_wounded(self):
        return self._cur_health > 0 and self._cur_health < self._card._health

    def enfeebled(self):
        return 0

    def is_jammed(self):
        return 0

    def faction(self):
        return self._card._faction

    def evade(self):
        return self._card._evade

    def payback(self):
        return self._card._payback

    def flying(self):
        return self._card._flying

    def armored(self):
        return self._card._armored

    def regenerate(self):
        return self._card._regenerate

    def counter(self):
        return self._card._counter

    def activation_skills(self):
        return self._card._activation_skills

class CommanderCardInPlay(CardInPlay):
    def __init__(self, card):
        CardInPlay.__init__(self, card)

    def description(self):
        return self._card.description() + " cur: " + str(self.health()) + "hp";

class AssaultCardInPlay(CardInPlay):
    def __init__(self, card):
        CardInPlay.__init__(self, card)
        self._cur_delay = card.delay()
        self._cur_attack = card.attack()
        self._jammed = False
        self._immobilized = False
        self._enfeebled = 0
        self._poisoned = 0

    def health(self):
        return self._cur_health

    def attack(self):
        return self._cur_attack

    def delay(self):
        return self._cur_delay

    def is_active(self):
        return self._cur_delay == 0

    def is_ready_next_turn(self):
        return self._cur_delay <= 1 and not self._jammed

    def is_ready_to_attack_next_turn(self):
        return self._cur_delay <= 1 and not self._jammed and not self._immobilized and self._cur_attack > 0

    def is_ready_to_attack(self):
        return self._cur_delay == 0 and not self._jammed and not self._immobilized

    def tick(self):
        if self._cur_delay > 0:
            self._cur_delay -= 1

    def is_jammed(self):
        return self._jammed

    def is_immobilized(self):
        return self._immobilized

    def enfeebled(self):
        return self._enfeebled

    def poisoned(self):
        return self._poisoned

    def fear(self):
        return self._card._fear

    def swipe(self):
        return self._card._swipe

    def flurry(self):
        return self._card._flurry

    def valor(self):
        return self._card._valor

    def antiair(self):
        return self._card._antiair

    def pierce(self):
        return self._card._pierce

    def immobilize(self):
        return self._card._immobilize

    def poison(self):
        return self._card._poison

    def crush(self):
        return self._card._crush

    def leech(self):
        return self._card._leech

    def siphon(self):
        return self._card._siphon

    def reset_status(self):
        self._cur_attack = self._card._attack
        self._jammed = False
        self._immobilized = False
        self._enfeebled = 0

    def apply_poison(self):
        self.take_damage(self._poisoned)

    def suffer_immobilize(self):
        self._immobilized = True

    def suffer_poison(self, amount):
        self._poisoned = max(self._poisoned, amount)

    def suffer_enfeeble(self, amount):
        self._enfeebled += amount

    def suffer_jam(self):
        self._jammed = True

    def rally(self, amount):
        self._cur_attack += amount

    def weaken(self, amount):
        if self._cur_attack > 0:
            self._cur_attack -= amount

    def activation_skills_for_mimic(self):
        return self._card._activation_skills_for_mimic

    def cannot_attack(self):
        if self._cur_health <= 0:
            if log_enabled(): log("        Can't attack: {" + self.description() + "} is DEAD")
            return True
        if self._jammed:
            if log_enabled(): log("        Can't attack: {" + self.description() + "} is JAMMED")
            return True
        if self._immobilized:
            if log_enabled(): log("        Can't attack: {" + self.description() + "} is IMMOBILIZED")
            return True
        if self._cur_attack <= 0:
            if log_enabled(): log("        Can't attack: {" + self.description() + "} has attack " + str(self.attack()))
            return True
        return False

    def can_use_skills(self):
        if self._cur_health <= 0:
            if log_enabled(): log("        Can't use skills: {" + self.description() + "} is DEAD")
            return False
        if self._jammed:
            if log_enabled(): log("        Can't use skills: {" + self.description() + "} is JAMMED")
            return False
        return True

    def status_effects_description(self):
        status_list = []
        if self._immobilized:
            status_list.append("immobilize")
        if self._jammed:
            status_list.append("jammed")
        if self._poisoned > 0:
            status_list.append("poisoned " + str(self._poisoned))
        if self._enfeebled > 0:
            status_list.append("enfeebled " + str(self._enfeebled))
        if status_list:
            return " (" + join(status_list, " ") + ")"
        return ""

    def description(self):
        return self._card.description() + " cur: " + str(self.health()) + "hp " + str(self.attack()) + "atk / " + str(self.delay()) + self.status_effects_description();


class StructureCardInPlay(CardInPlay):
    def __init__(self, card):
        CardInPlay.__init__(self, card)
        self._cur_delay = card.delay()

    def delay(self):
        return self._cur_delay

    def is_active(self):
        return self._cur_delay == 0

    def tick(self):
        if self._cur_delay > 0:
            self._cur_delay -= 1

    def is_wall(self):
        return self._card._wall

    def description(self):
        return self._card.description() + " cur: " + str(self.health()) + "hp / " + str(self.delay());
