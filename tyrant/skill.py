
activation_skills = {"heal", "rally", "enfeeble", "strike", "jam", "weaken", "siege", "mimic"}
hostile_activation_skills = {"enfeeble", "strike", "jam", "weaken", "siege", "mimic"}

skill_targeting = {"heal": "friendly wounded", 
                   "rally": "friendly active", 
                   "enfeeble": "hostile", 
                   "strike": "hostile",
                   "jam": "hostile ready", 
                   "weaken": "hostile ready", 
                   "siege": "hostile structure", 
                   "mimic": "hostile"}

class Skill:
    "A Tyrant card skill"
    def __init__(self, name, value, all, target_faction):
        self._name = name
        self._value = value
        self._all = all
        self._target_faction = target_faction

    def name(self):
        return self._name

    def value(self):
        return self._value

    def all(self):
        return self._all

    def target_faction(self):
        return self._target_faction

    def is_activation_skill(self):
        return self._name in activation_skills

    def is_hostile_activation_skill(self):
        return self._name in hostile_activation_skills

    def targeting(self):
        return skill_targeting[self.name()]
    
    def description(self):
        description = self.name().capitalize()
        description += " All" if self.all() else ""
        description += " " + self.target_faction() if self.target_faction() != None else ""
        description += " " + str(self.value()) if self.value() != None else ""
        return description
