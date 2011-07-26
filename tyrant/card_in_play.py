
from string import join

class CardInPlay:
    def __init__(self, card):
        self._card = card
        self._cur_health = card.health()

    def type(self):
        return self._card.type()

    def health(self):
        return self._cur_health

    def take_damage(self, amount):
        self._cur_health -= amount

    def heal(self, amount):
        self._cur_health = min(self._card.health(), self._cur_health + amount)

    def perform_regenerate(self, amount):
        self._cur_health = amount

    def suffer_immobilize(self):
        pass

    def suffer_poison(self, amount):
        pass

    def is_dead(self):
        return self.health() <= 0

    def enfeebled(self):
        return 0

    def flying(self):
        return self._card.flying()

    def armored(self):
        return self._card.armored()

    def regenerate(self):
        return self._card.regenerate()

    def counter(self):
        return self._card.counter()

    def cannot_use_skills(self):
        if self.is_dead():
            print "    Can't use skills: {" + self.description() + "} is DEAD"
            return True
        if self.is_jammed():
            print "    Can't use skills: {" + self.description() + "} is JAMMED"
            return True
        return False


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
        return self._card.fear()

    def swipe(self):
        return self._card.swipe()

    def flurry(self):
        return self._card.flurry()

    def valor(self):
        return self._card.valor()

    def antiair(self):
        return self._card.antiair()

    def pierce(self):
        return self._card.pierce()

    def immobilize(self):
        return self._card.immobilize()

    def poison(self):
        return self._card.poison()

    def crush(self):
        return self._card.crush()

    def leech(self):
        return self._card.leech()

    def siphon(self):
        return self._card.siphon()

    def reset_status(self):
        self._cur_attack = self._card.attack()
        self._jammed = False
        self._immobilized = False
        self._enfeebled = 0

    def apply_poison(self):
        self.take_damage(self._poisoned)

    def suffer_immobilize(self):
        self._immobilized = True

    def suffer_poison(self, amount):
        self._poisoned = max(self._poisoned, amount)

    def cannot_attack(self):
        if self.is_dead():
            print "    Can't attack: {" + self.description() + "} is DEAD"
            return True
        if self.is_jammed():
            print "    Can't attack: {" + self.description() + "} is JAMMED"
            return True
        if self.is_immobilized():
            print "    Can't attack: {" + self.description() + "} is IMMOBILIZED"
            return True
        if self.attack() <= 0:
            print "    Can't attack: {" + self.description() + "} has attack " + str(self.attack())
            return True
        return False

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
        return self._card.is_wall()

    def description(self):
        return self._card.description() + " cur: " + str(self.health()) + "hp / " + str(self.delay());
