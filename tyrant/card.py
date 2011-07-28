
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
        self._activation_skills = [skill for skill in self._skills if skill.is_activation_skill()]
        self._evade = self.has_skill("evade")
        self._payback = self.has_skill("payback")
        self._flying = self.has_skill("flying")
        self._armored = self.skill_value("armored")
        self._regenerate = self.skill_value("regenerate")
        self._counter = self.skill_value("counter")

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

    def activation_skills(self):
        return self._activation_skills

    def evade(self):
        return self._evade

    def payback(self):
        return self._payback

    def flying(self):
        return self._flying

    def armored(self):
        return self._armored

    def regenerate(self):
        return self._regenerate

    def counter(self):
        return self._counter

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
        self._fear = self.has_skill("fear")
        self._swipe = self.has_skill("swipe")
        self._flurry = self.skill_value("flurry")
        self._valor = self.skill_value("valor")
        self._antiair = self.skill_value("antiair")
        self._pierce = self.skill_value("pierce")
        self._immobilize = self.has_skill("immobilize")
        self._poison = self.skill_value("poison")
        self._crush = self.skill_value("crush")
        self._leech = self.skill_value("leech")
        self._siphon = self.skill_value("siphon")
        self._activation_skills_for_mimic = [skill.unrestricted_version() for skill in self.activation_skills()]

    def activation_skills_for_mimic(self):
        return self._activation_skills_for_mimic

    def fear(self):
        return self._fear

    def swipe(self):
        return self._swipe

    def flurry(self):
        return self._flurry

    def valor(self):
        return self._valor

    def antiair(self):
        return self._antiair

    def pierce(self):
        return self._pierce

    def immobilize(self):
        return self._immobilize

    def poison(self):
        return self._poison

    def crush(self):
        return self._crush

    def leech(self):
        return self._leech

    def siphon(self):
        return self._siphon

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
        self._wall = self.has_skill("wall")

    def health(self):
        return self._health

    def delay(self):
        return self._delay

    def is_wall(self):
        return self._wall

    def description(self):
        return self.name() + " (" + str(self.rarity_and_faction_string()) + ")  [" + str(self.health()) + "hp / " + str(self.delay()) + " | "  + self.skill_description() + "]"
