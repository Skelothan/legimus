import pygame

class AttackType(object):
    def __init__(self, kind, name, power, isMagic, spCost, numTargets, 
    text="", effect="none", effectChance=0):
        # kind is for enemies to roughly choose what kind of action they want to 
        # do. Values: "attack", "heal", "buff", "debuff", "waste", "counter"
        self.kind = kind                # String. 
        self.name = name                # String
        self.power = power              # Int
        self.isMagic = isMagic          # Bool
        self.spCost = spCost            # String
        self.numTargets = numTargets    # String
        self.text = text                # String
        self.effect = effect            # String
        self.effectChance = effectChance # Int from 1-128
    
    def __repr__(self):
        return self.name + " " + str(self.spCost) + "SP"

allAttackTypes = {
"Bash": AttackType("attack", "Bash", 5, False, 0, "1e", text="[u] bashes!", 
    effect="none", effectChance=0),
"Cast": AttackType("attack", "Cast", 5, True, 0, "1e", 
    text="[u] is casting!", effect="none", effectChance=0),
"Fireball": AttackType("attack", "Fireball", 15, True, 7, "1e", 
    text="[u] cast forth a fireball!", effect="none", effectChance=0),
"Invigorate": AttackType("buff", "Invigorate", 0, True, 4, "1a", 
    text="[u] cast an invigorating spell!", effect="strengthUp", 
    effectChance=128),
"Focus": AttackType("buff", "Focus", 0, True, 4, "1a", 
    text="[u] focused intently!", effect="intelligenceUp", 
    effectChance=128),
"Flame Column": AttackType("attack", "Flame Column", 24, True, 14, 
    "1e", text="[u] raised a column of flame!", effect="defenseDown", 
    effectChance=24),
"Blood Ritual": AttackType("buff", "Blood Ritual", 10, True, 14, 
    "1s", text="[u] performed a blood ritual!", effect="strengthUp", 
    effectChance=128),
"Shadow Spear": AttackType("attack", "Shadow Spear", 19, False, 9, 
    "1e", text="[u] lunged forward with a shadowy spear!", 
    effect="strengthDown", effectChance=36),
"Healing Shadow": AttackType("heal", "Healing Shadow", 60, False, 6, 
    "1s", text="[u] put up a healing shadow!", effect="none", 
    effectChance=0),
"Spin Tackle": AttackType("attack", "Spin Tackle", 10, False, 3, 
    "1e", text="[u] did a spinning tackle!", effect="defenseDown", 
    effectChance=60),
"Rush Forward": AttackType("attack", "Rush Forward", 28, False, 16, 
    "1e", text="[u] rushed forward!", effect="none", 
    effectChance=0),
"Ball Lightning": AttackType("attack", "Ball Lightning", 11, True, 6, 
    "1e", text="[u] generated ball lightning!", effect="wisdomDown", 
    effectChance=28),
"Thunderbolt": AttackType("attack", "Thunderbolt", 28, True, 14, 
    "1e", text="[u] called down a thunderbolt!", effect="none", 
    effectChance=0),
"Barrier": AttackType("buff", "Barrier", 0, True, 14, 
    "1s", text="[u] cast up a barrier!", effect="defenseUp", 
    effectChance=128),
"Chant": AttackType("waste", "Chant", 0, False, 0, 
    "1s", text="[u] chants strange words...", effect="none", 
    effectChance=0),
"Arcane Laser": AttackType("attack", "Arcane Laser", 70, True, 100, 
    "1e", text="[u] fired off its Arcane Laser!", effect="defenseDown", 
    effectChance=128),
"Consult Tome": AttackType("waste", "Consult Tome", 0, False, 0, 
    "1s", text="[u] consulted a tome.", effect="none", 
    effectChance=0)
}

#-------------------------------------------------------------------------------
# Counterattacks can only be damaging effects.
# That might be reconsidered in the future, as defensive players/enemies don't
# benefit much from counters currently.
# At present, the benefits you get from counterattacking are:
# - Previous attack misses
# - One of the following:
#   - 2x power
#   - Triple effect chance, 1.5x power
#   - New effect chance, 1.5x power
#-------------------------------------------------------------------------------
allCounterattackTypes = {
"Bash": AttackType("counter", "Bash", 10, False, 0, "1e", text="[u] bashes!", 
    effect="none", effectChance=0),
"Cast": AttackType("counter", "Cast", 10, True, 0, "1e", 
    text="[u] is casting!", effect="none", effectChance=0),
"Fireball": AttackType("counter", "Fireball", 30, True, 7, "1e", 
    text="[u] cast forth a fireball!", effect="none", effectChance=0),
"Flame Column": AttackType("counter", "Flame Column", 36, True, 14, 
    "1e", text="[u] raised a column of flame!", effect="defenseDown", 
    effectChance=72),
"Shadow Spear": AttackType("counter", "Shadow Spear", 29, False, 9, 
    "1e", text="[u] lunged forward with a shadowy spear!", 
    effect="strengthDown", effectChance=108),
"Spin Tackle": AttackType("counter", "Spin Tackle", 20, False, 3, 
    "1e", text="[u] did a spinning tackle!", effect="defenseDown", 
    effectChance=60),
"Rush Forward": AttackType("counter", "Rush Forward", 56, False, 16, 
    "1e", text="[u] rushed forward!", effect="none", 
    effectChance=0),
"Ball Lightning": AttackType("counter", "Ball Lightning", 11, True, 6, 
    "1e", text="[u] generated ball lightning!", effect="wisdomDown", 
    effectChance=84),
"Thunderbolt": AttackType("counter", "Thunderbolt", 42, True, 14, 
    "1e", text="[u] called down a thunderbolt!", effect="wisdomDown", 
    effectChance=0),
# Exclusive attack of the Grand Wizard, so this pronoun is male.
# Might add a pronoun control code at a later date.
"Arcane Laser": AttackType("counter", "Arcane Laser", 140, True, 100, 
    "1e", text="[u] fired off his Arcane Laser!", effect="defenseDown", 
    effectChance=128)
}

allAllies = {
"Lilith":
    ["Lilith",
    [120, 35, 35, 20, 15, 20, 35],
    [8, 2.3, 1.2, 1.1, 0.6, 1.5, 0.1],
    [
        allAttackTypes["Bash"],
        allAttackTypes["Cast"],
        allAttackTypes["Shadow Spear"],
        allAttackTypes["Healing Shadow"]
    ]
    ]
}

allEnemies = {
"Pyromancer":
    ["Pyromancer", 
    [112, 45, 10, 10, 20, 13, 30], 
    61, 
    [
        allAttackTypes["Cast"],
        allAttackTypes["Fireball"],
        allAttackTypes["Focus"],
        allAttackTypes["Flame Column"]
    ],
    "offensive",
    pygame.image.load("enemies/fire_wizard.gif")
    ],
"Electromancer":
    ["Electromancer", 
    [54, 40, 10, 9, 30, 11, 52], 
    53, 
    [
        allAttackTypes["Cast"],
        allAttackTypes["Thunderbolt"],
        allAttackTypes["Ball Lightning"]
    ],
    "aggressive",
    pygame.image.load("enemies/electric_wizard.gif")
    ],
"Construct":
    ["Construct", 
    [32, 27, 22, 27, 10, 10, 22], 
    47, 
    [
        allAttackTypes["Bash"],
        allAttackTypes["Spin Tackle"],
        allAttackTypes["Rush Forward"],
    ],
    "offensive",
    pygame.image.load("enemies/construct_sprite.gif")
    ],
"Grand Wizard":
    ["Grand Wizard", 
    [350, 200, 15, 25, 26, 30, 32], 
    700, 
    [
        allAttackTypes["Cast"],
        allAttackTypes["Focus"],
        allAttackTypes["Ball Lightning"],
        allAttackTypes["Flame Column"],
        allAttackTypes["Barrier"],
        allAttackTypes["Chant"],
        allAttackTypes["Arcane Laser"]
    ],
    "grand_wizard",
    pygame.image.load("enemies/grand_wizard_big.png")
    ]

}

