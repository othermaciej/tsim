
class CommanderCardInPlay:
    def __init__(self, card):
        self._card = card
        self._cur_health = card.health()

    def health(self):
        return self._cur_health

    def take_damage(self, amount):
        self._cur_health -= amount

    def is_dead(self):
        return self.health() <= 0

    def description(self):
        return self._card.description() + "cur: " + str(self.health()) + "hp";

class AssaultCardInPlay:
    def __init__(self, card):
        self._card = card
        self._cur_health = card.health()
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

    def is_dead(self):
        return self.health() <= 0

    def take_damage(self, amount):
        self._cur_health -= amount

    def reset_status(self):
        self._cur_attack = self._card.attack()
        self._jammed = False
        self._immobilized = False
        self._enfeebled = 0

    def description(self):
        return self._card.description() + "cur: " + str(self.health()) + "hp " + str(self.attack()) + "atk / " + str(self.delay());


class StructureCardInPlay:
    def __init__(self, card):
        self._card = card
        self._cur_health = card.health()
        self._cur_delay = card.delay()

    def health(self):
        return self._cur_health

    def delay(self):
        return self._cur_delay

    def is_active(self):
        return self._cur_delay == 0

    def tick(self):
        if self._cur_delay > 0:
            self._cur_delay -= 1

    def is_dead(self):
        return self.health() <= 0

    def take_damage(self, amount):
        self._cur_health -= amount

    def description(self):
        return self._card.description() + "cur: " + str(self.health()) + "hp / " + str(self.delay());
