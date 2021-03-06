
from random import choice, shuffle, randint
from tyrant.card_in_play import CommanderCardInPlay, AssaultCardInPlay, StructureCardInPlay, coin_toss
from tyrant.log import log_enabled, log

class Board:
    def __init__(self, deck):
        self._deck = deck
        self._commander = CommanderCardInPlay(deck.commander())
        self._draw_pile = deck.cards()[:]
        shuffle(self._draw_pile)
        self._hand = []
        self._active_structures = []
        self._active_assault_units = []
        self._active_action = None

    def draw(self):
        if self._draw_pile:
            self._hand.append(self._draw_pile.pop())
            if log_enabled(): 
                log("    Drew: {" + self._hand[-1].description() + "}")
                log("    Hand size: " + str(len(self._hand)) + " | Draw pile size: "  + str(len(self._draw_pile)))

    def tick_timers(self):
        if log_enabled(): log("  Ticking Timers")
        for card in self._active_structures:
            card.tick()
        for card in self._active_assault_units:
            card.tick()

    def activate_action(self, opposing_board):
        if self._active_action:
            if log_enabled(): log("    Activating Action {" + self._active_action.description() + "}")
            self.perform_activation_skills(self._active_action, opposing_board)

    def activate_commander(self, opposing_board):
        if log_enabled(): log("    Activating Commander {" + self._commander.description() + "}")
        self.perform_activation_skills(self._commander, opposing_board)

    def activate_structures(self, opposing_board):
        for i in range(0, len(self._active_structures)):
            card = self._active_structures[i]
            if log_enabled(): 
                log("    Activating Structure [" + str(i) + "] {" + card.description() + "}")
            if card.is_active():
                self.perform_activation_skills(card, opposing_board)
            elif log_enabled():
                log("      (structure is not ready)")

    def activate_assault_units(self, opposing_board):
        for i in range(0, len(self._active_assault_units)):
            card = self._active_assault_units[i]
            if log_enabled(): 
                log("    Activating Assault Unit [" + str(i) + "] {" + card.description() + "}")
            if card.is_active() and card.can_use_skills():
                self.perform_activation_skills(card, opposing_board)
                self.perform_attack(i, card, opposing_board)
            elif log_enabled():
                log("      (unit is not ready)")

    def reset_status(self):
        for card in self._active_assault_units:
            card.reset_status()

    def activate_cards(self, opposing_board):
        if log_enabled(): log("  Activating cards")
        self.activate_action(opposing_board)
        self.activate_commander(opposing_board)
        self.activate_structures(opposing_board)
        self.activate_assault_units(opposing_board)

    def perform_activation_skills(self, card, opposing_board):
        self.perform_activation_skill_list(card, card.activation_skills(), opposing_board)

    def perform_activation_skill_list(self, card, skills, opposing_board):
        for skill in skills:
            self.perform_one_activation_skill(card, skill, opposing_board)

    def perform_one_activation_skill(self, card, skill, opposing_board):
        if log_enabled(): log("      Performing skill " + skill.description())
        targets = self.get_target_list_for_skill(skill, opposing_board)
        if log_enabled():
            if not targets:
                if log_enabled(): log("        (No valid targets)")
        
        if skill.all():
            for target in targets:
                self.perform_activation_skill_on_target(card, skill, target, opposing_board)
        elif targets:
                self.perform_activation_skill_on_target(card, skill, choice(targets), opposing_board)

    def get_target_list_for_skill(self, skill, opposing_board):
        targeting = skill.targeting()

        if targeting == "hostile":
            targets = [card for card in opposing_board.active_assault_units() if not card.is_dead()]
        elif targeting == "friendly wounded":
            targets = [card for card in self._active_assault_units if card.is_wounded()]
        elif targeting == "hostile attack-ready":
            targets = [card for card in opposing_board.active_assault_units() if card.is_ready_to_attack_next_turn()]
        elif targeting == "friendly attack-ready":
            targets = [card for card in self._active_assault_units if card.is_ready_to_attack()]
        elif targeting == "hostile ready":
            targets = [card for card in opposing_board.active_assault_units() if card.is_ready_next_turn()]
        elif targeting == "hostile structure":
            targets = [card for card in opposing_board.active_structures() if not card.is_dead()]

        target_faction = skill.target_faction()
        if target_faction:
            targets = [card for card in targets if card.faction() == target_faction]

        return targets
        
    def perform_activation_skill_on_target(self, card, skill, target, opposing_board, can_payback=True):
        # Enfeeble, Heal, Jam, Mimic, Rally, Siege, Strike, Weaken
        # Account for: Evade, Payback, Regenerate

        if log_enabled(): log("        Skill target is: {" + target.description() + "}")
        hostile = skill.is_hostile_activation_skill()
        if hostile and target.evade():
            if coin_toss():
                if log_enabled(): log("        Evade! {" + target.description() + "} evaded " + skill.description())
                if log_enabled(): log("      --Final skill target status: {" + target.description() + "}")
                return

        can_payback = can_payback and hostile and card.type() == "assault"

        skill_name = skill.name()
        if skill_name == "heal":
            target.heal(skill.value())
        elif skill_name == "weaken":
            target.weaken(skill.value())
        elif skill_name == "rally":
            target.rally(skill.value())
        elif skill_name == "strike":
            damage = skill.value()
            enfeebled = target.enfeebled()
            if enfeebled > 0:
                damage += enfeebled
                if log_enabled(): log("        Enfeeble bonus damage: " + str(enfeebled))
            target.take_damage(damage)
        elif skill_name == "siege":
            target.take_damage(skill.value())
            can_payback = False
        elif skill_name == "jam":
            if coin_toss():
                target.suffer_jam()
            else:
                if log_enabled(): log("        Jam failed on {" + target.description() + "}")
                # no chance for payback if it misses
                can_payback = False
        elif skill_name == "enfeeble":
            target.suffer_enfeeble(skill.value())
        elif skill_name == "mimic":
            mimiced_skills = target.activation_skills_for_mimic()
            self.perform_activation_skill_list(card, mimiced_skills, opposing_board)
            can_payback = False

        if log_enabled(): log("      --Final skill target status: {" + target.description() + "}")

        if target.payback() and can_payback:
            if coin_toss():
                if log_enabled(): log("        Payback! {" + target.description() + "} will attempt " + skill.description() + " on {" + card.description() + "}")
                opposing_board.perform_activation_skill_on_target(target, skill, card, self, can_payback=False)

    def commander_target(self):
        for card in self._active_structures:
            if card.is_wall() and not card.is_dead():
                return card
        return self._commander

    def non_commander_target_for_index(self, index):
        if index < 0 or index >= len(self._active_assault_units):
            return None
        target = self._active_assault_units[index]
        if not target or target.is_dead():
            return None
        return target

    def target_for_index(self, index):
        target = self.non_commander_target_for_index(index)
        if target: return target
        return self.commander_target()

    def assault_count(self):
        return len(self._active_assault_units)

    def perform_attack(self, index, attacker, opposing_board):
        # Attack Jammed = Attacker Immobilized = Attacker weakened to 0 > Swipe check > Flurry check > Fear >  Enfeeble = Valor > Flying = Antiair > Armored = Pierce > Immobilize = Poison > Count Damage > Crush > Defender Regenerate > Counter > Attacker Regenerate = Leech > Siphon > Flurry Repeat > Swipe Repeat

        if log_enabled(): log("      Performing attack")

        if attacker.cannot_attack():
            return

        if attacker.fear():
            self.perform_attack_on_target(opposing_board.commander_target(), attacker, opposing_board)

        elif attacker.swipe():
            main_target = opposing_board.non_commander_target_for_index(index)
            if main_target:
                left_target = opposing_board.non_commander_target_for_index(index - 1)
                right_target = opposing_board.non_commander_target_for_index(index + 1)
                if left_target:
                    if log_enabled(): log("      === Swipe Attack left ===")
                    self.perform_attack_on_target(left_target, attacker, opposing_board)

                if left_target or right_target:
                    if log_enabled(): log("      === Swipe Attack center ===")
                    if attacker.cannot_attack():
                        return
                self.perform_attack_on_target(main_target, attacker, opposing_board)

                if right_target:
                    if log_enabled(): log("      === Swipe Attack right ===")
                    if attacker.cannot_attack():
                        return
                    self.perform_attack_on_target(right_target, attacker, opposing_board)
            else:
                self.perform_attack_on_target(opposing_board.commander_target(), attacker, opposing_board)

        else:
            self.perform_attack_on_target(opposing_board.target_for_index(index), attacker, opposing_board)

    def perform_attack_on_target(self, target, attacker, opposing_board):
        attacks = 1
        flurry = attacker.flurry()
        if flurry > 0 and coin_toss():
            attacks += flurry
            if log_enabled(): log("      Flurry! performing " + str(attacks) + " total attacks")

            for i in range(1, attacks + 1):
                if i > 0 and attacker.cannot_attack():
                    return
                if log_enabled(): log("      === Attack \#" + str(i) + " ===")
                self.perform_single_attack_on_target(target, attacker, opposing_board)
                if target.is_dead():
                    target = opposing_board.commander_target()
        else:
            self.perform_single_attack_on_target(target, attacker, opposing_board)

    def perform_single_attack_on_target(self, target, attacker, opposing_board):
        if log_enabled(): log("        Attack target is: {" + target.description() + "}")

        damage = attacker.attack()
        if log_enabled(): log("        Base damage (including rally/weaken): " + str(damage))

        enfeebled = target.enfeebled()
        if enfeebled > 0:
            damage += enfeebled
            if log_enabled(): log("         Enfeeble bonus damage: " + str(enfeebled))

        valor = attacker.valor()
        if valor > 0 and self.assault_count() < opposing_board.assault_count():
            damage += valor
            if log_enabled(): log("        Valor bonus damage: " + str(valor))

        if target.flying():
            antiair = attacker.antiair()
            if antiair:
                damage += antiair
                if log_enabled(): log("        Antiair bonus damage: " + str(antiair))
            elif not attacker.flying():
                if coin_toss():
                    if log_enabled(): log("         Flying! Unit {" + attacker.description() + "} missed {" + target.description() + "}")
                    return

        armor = target.armored()
        if armor > 0:
            pierce = attacker.pierce()
            if pierce:
                if log_enabled(): log("        Armor reduced from " + str(armor) + " by pierce " + str(pierce))
                armor = max(0, armor - pierce)
            if log_enabled(): log("        Damage reduced by armor: " + str(armor))
            damage -= armor

        if damage <= 0:
            if log_enabled(): log("        Blocked: {" + attacker.description() + "} has modified damage " + str(damage))
            return

        if attacker.immobilize():
            if coin_toss():
                if log_enabled(): log("        Immobilize! Unit {" + attacker.description() + "} immobilizes {" + target.description() + "}")
                target.suffer_immobilize()
    
        poison = attacker.poison()
        if poison > 0:
            if log_enabled(): log("        Poison! Unit {" + attacker.description() + "} inflicts " + str(poison) + " poison on target {" + target.description() + "}")
            target.suffer_poison(poison)

        target_died = target.take_damage(damage)
        if log_enabled(): log("        Unit {" + attacker.description() + "} does " + str(damage) + " attack damage to {" + target.description() + "}")

        crush = attacker.crush()
        if crush > 0 and target_died:
            crush_target = opposing_board.commander_target()
            if log_enabled(): log("        Crush! Unit {" + attacker.description() + "} does {" + str(damage) + "} crush damage to {" + crush_target.description() + "}")
            crush_target.take_damage(damage)
            if log_enabled(): log("      --Final crushed unit status: {" + crush_target.description() + "}")

        counter = target.counter()
        if counter > 0:
            if log_enabled(): log("        Unit {" + attacker.description() + "} suffers " + str(counter) + " counter damage from {" + target.description() + "}")
            attacker.take_damage(counter)

        target_is_assault = target.type() == "assault"
        leech = attacker.leech()
        if leech > 0 and target_is_assault and not attacker.is_dead():
            if log_enabled(): log("        Leech! Unit {" + attacker.description() + "} leeches for " + str(leech) + "hp")
            attacker.heal(leech)

        siphon = attacker.siphon()
        if siphon > 0 and target_is_assault:
            if log_enabled(): log("        Siphon! Commander {" + self._commander.description() + "} receives siphon for " + str(siphon) + "hp from {" + attacker.description() + "}")
            self._commander.heal(siphon)

        if log_enabled(): log("      --Final attacking unit status: {" + attacker.description() + "}")
        if log_enabled(): log("      --Final defending unit status: {" + target.description() + "}")

    def apply_poison(self):
        # FIXME: when exactly is poison applied?
        for card in self._active_assault_units:
            if card.poisoned() > 0:
                if log_enabled(): log("        Poison damage! Poisoned unit {" + card.description() + "} will suffer " + str(card.poisoned()) + " poison damage")
                card.apply_poison()
                if log_enabled(): log("      --Final poisoned unit status: {" + card.description() + "}")

    def bury_the_dead(self):
        for card in self._active_structures:
            if card.is_dead():
                self._active_structures.remove(card)
                if log_enabled(): log("    Removed dead structure card: {" + card.description() + "}")

        for card in self._active_assault_units:
            if card.is_dead():
                self._active_assault_units.remove(card)
                if log_enabled(): log("    Removed dead assault card: {" + card.description() + "}")

    def clean_up(self, opposing_board):
        if log_enabled(): log("  Cleaning up")
        self.bury_the_dead()
        opposing_board.bury_the_dead()
        self._active_action = None
        self.reset_status();

    def commander(self):
        return self._commander
    
    def active_assault_units(self):
        return self._active_assault_units

    def active_structures(self):
        return self._active_structures
    
    def play_random_turn(self, opposing_board):
        self.apply_poison()
        self.tick_timers()
        if log_enabled(): log("  Drawing")
        while len(self._hand) < 3 and self._draw_pile: 
            self.draw()
        if self._hand:
            self.play_from_hand(choice(self._hand))

        self.activate_cards(opposing_board)
        self.clean_up(opposing_board)
        return opposing_board.commander().is_dead()

    def play_from_hand(self, card_to_play):
        self._hand.remove(card_to_play)
        if log_enabled(): log("  Playing card: {" + card_to_play.description() + "}")
        if card_to_play.type() == "assault":
            self._active_assault_units.append(AssaultCardInPlay(card_to_play))
        elif card_to_play.type() == "structure":
            self._active_structures.append(StructureCardInPlay(card_to_play))
        else:
            self._active_action = card_to_play

    def log_as_offense(self):
        self.log_front_row()
        self.log_back_row()

    def log_as_defense(self):
        self.log_back_row()
        self.log_front_row()

    def log_front_row(self):
        self.log_cards(self._active_assault_units)

    def log_back_row(self):
        back_row = [self._commander] + self._active_structures + ([self._active_action] if self._active_action else [])
        self.log_cards(back_row)

    def log_cards(self, card_list):
        line = ""
        for card in card_list:
            line += "+----------+ "
        print line;

        line = ""
        for card in card_list:
            line += "|       ";
            if card.type() == "action" or card.type() == "commander":
                line += "  "
            else:
                line += "{0:>2}".format(card.delay())
            line += " | "
        print line;

        line = ""
        for card in card_list:
            line += "|";
            line += "{0: ^10.10}".format(card.name())
            line += "| "
        print line;

        line = ""
        for card in card_list:
            line += "| ";
            if card.type() == "assault":
                line += "{0:<2}".format(card.attack())
            else:
                line += "  "

            line += "    "
            if card.type() == "action":
                line += "  "
            else:
                line += "{0:>2}".format(card.health())
            line += " | "
        print line;


        line = ""
        for card in card_list:
            line += "+----------+ "
        print line;
