
from tyrant.skill import Skill
from string import join

class Card:
    "A Tyrant card"
    def __init__(self, name, faction, type, skills, rarity, unique):
        self._name = name
        self._type = type
        self._faction = faction
        self._skills = skills
        self._rarity = rarity
        self._unique = unique

    def type(self):
        return self._type

    def name(self):
        return self._name

    def faction(self):
        return self._faction

    def skills(self):
        return self._skills

    def rarity(self):
        return self._rarity

    def unique(self):
        return self._unique

    def skill_value(self, skill_name):
        skill = next((skill for skill in self._skills if skill.name() == skill_name), None)
        if skill:
            return skill.value()
        else:
            return 0

    def has_skill(self, skill_name):
        return next((skill for skill in self._skills if skill.name() == skill_name), None) != None

    def flying(self):
        return self.has_skill("flying")

    def armored(self):
        return self.skill_value("armored")

    def regenerate(self):
        return self.skill_value("regenerate")

    def counter(self):
        return self.skill_value("counter")

    def rarity_and_faction_string(self):
        if self.rarity() == "Legendary":
            return "Legendary " + self.faction()
        elif self.unique():
            return "Unique " + self.faction()
        else:
            return self.faction()
        
    def skill_description(self):
        return join([skill.description() for skill in self.skills()], ", ")

    def description(self):
        return self.name()

class ActionCard(Card):
    "A Tyrant action card"
    def __init__(self, name, faction, skills, rarity, unique):
        Card.__init__(self, name, faction, "action", skills, rarity, unique)

    def description(self):
        return self.name() + "  [" + self.skill_description() + "]"

class AssaultCard(Card):
    "A Tyrant assault card"
    def __init__(self, name, faction, health, attack, delay, skills, rarity, unique):
        Card.__init__(self, name, faction, "assault", skills, rarity, unique)
        self._health = health
        self._attack = attack
        self._delay = delay

    def fear(self):
        return self.has_skill("fear")

    def swipe(self):
        return self.has_skill("swipe")

    def flurry(self):
        return self.skill_value("flurry")

    def valor(self):
        return self.skill_value("valor")

    def antiair(self):
        return self.skill_value("antiair")

    def pierce(self):
        return self.skill_value("pierce")

    def immobilize(self):
        return self.has_skill("immobilize")

    def poison(self):
        return self.skill_value("poison")

    def crush(self):
        return self.skill_value("crush")

    def leech(self):
        return self.skill_value("leech")

    def siphon(self):
        return self.skill_value("siphon")

    def health(self):
        return self._health

    def attack(self):
        return self._attack

    def delay(self):
        return self._delay

    def description(self):
        return self.name() + " (" + str(self.rarity_and_faction_string()) + ")  [" + str(self.health()) + "hp " + str(self.attack()) + "atk / " + str(self.delay()) + " | " + self.skill_description() + "]"

class CommanderCard(Card):
    "A Tyrant commander card"
    def __init__(self, name, faction, health, skills, rarity, unique):
        Card.__init__(self, name, faction, "commander", skills, rarity, unique)
        self._health = health

    def health(self):
        return self._health

    def description(self):
        return self.name() + " (" + str(self.rarity_and_faction_string()) + ")  [" + str(self.health()) + "hp | " + self.skill_description() + "]"

class StructureCard(Card):
    "A Tyrant structure card"
    def __init__(self, name, faction, health, delay, skills, rarity, unique):
        Card.__init__(self, name, faction, "structure", skills, rarity, unique)
        self._health = health
        self._delay = delay

    def health(self):
        return self._health

    def delay(self):
        return self._delay

    def is_wall(self):
        return self.has_skill("wall")

    def description(self):
        return self.name() + " (" + str(self.rarity_and_faction_string()) + ")  [" + str(self.health()) + "hp / " + str(self.delay()) + " | "  + self.skill_description() + "]"
