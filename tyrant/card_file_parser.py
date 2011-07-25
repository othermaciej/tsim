
import xml.dom.minidom
from string import atoi

from tyrant.skill import Skill
from tyrant.card import ActionCard, AssaultCard, CommanderCard, StructureCard


def parse_card_file(filename):
    document = xml.dom.minidom.parse(filename)
    return [parse_unit(node) for node in document.documentElement.childNodes if node.nodeName == "unit" and extract_field(node, "set") != None]
    
def extract_field(node, name):
    nodeList = node.getElementsByTagName(name)
    if nodeList.length == 0:
        return None
    return nodeList[0].firstChild.data

def extract_numeric_field(node, name):
    field = extract_field(node, name)
    if field == None:
        return field;
    return atoi(field)

def extract_boolean_field(node, name):
    return extract_field(node, name) != None

def type_code_to_faction(type_code):
    if type_code == 1:
        return "Imperial"
    elif type_code == 3:
        return "Bloodthirsty"
    elif type_code == 4:
        return "Xeno"
    elif type_code == 9:
        return "Raider"
    else:
        return None

def rarity_code_to_rarity(code):
    if code == 1:
        return "Common"
    elif code == 2:
        return "Uncommon"
    elif code == 3:
        return "Rare"
    elif code == 4:
        return "Legendary"
    else:
        return None

def extract_faction_field(node, name):
    field = extract_numeric_field(node, name)
    if field == None:
        return field;
    return type_code_to_faction(field)

def extract_rarity_field(node, name):
    field = extract_numeric_field(node, name)
    if field == None:
        return field;
    return rarity_code_to_rarity(field)

def parse_skill_node(node):
    name = node.getAttribute("id").capitalize()
    value = node.getAttribute("x")
    value = value if value != "" else None
    all = node.getAttribute("all") != ""
    target_faction_type_code = node.getAttribute("y")
    target_faction = type_code_to_faction(atoi(target_faction_type_code)) if target_faction_type_code != "" else None

    return Skill(name, value, all, target_faction)

def extract_skills(node, name):
    nodeList = node.getElementsByTagName(name)
    return [parse_skill_node(skill_node) for skill_node in nodeList]
    
def parse_unit(node):
    name = extract_field(node, "name")
    health = extract_numeric_field(node, "health")
    attack = extract_numeric_field(node, "attack")
    delay = extract_numeric_field(node, "cost")
    set = extract_field(node, "set")
    faction = extract_faction_field(node, "type")
    rarity = extract_rarity_field(node, "rarity")
    unique = extract_boolean_field(node, "unique")
    skills = extract_skills(node, "skill")

    if set == None:
        # Not a real card
        return None
    if health == None:
        # Actions are the only cards that have no health
        return ActionCard(name, faction, skills, rarity, unique)
    elif attack == None and delay != None:
        # Commanders for some reason show up as attack 0 but structures have no attack
        # Also check cost just in case
        return StructureCard(name, faction, health, delay, skills, rarity, unique)
    elif delay == None and health != None:
        # Commanders have no delay but unlike actions have health
        return CommanderCard(name, faction, health, skills, rarity, unique)
    else:
        # If it's notanything else, it's an assault card
        return AssaultCard(name, faction, health, attack, delay, skills, rarity, unique)
