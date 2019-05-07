# TODO in the far future: ------------------------------------------------------
# TextWindow object, Menu object extends TextWindow, HealthBar extends 
#    TextWindow for actually useful text handling
# Actually implement battle effects in a concise way
# Move ally, enemy, attack data to a separate file
# Allow combatants to be inflicted with multiple statuses
# Executing attacks actually executes Hit objects, allowing attacks to have
#    multiple hits and/or targets
#-------------------------------------------------------------------------------

# Imports ----------------------------------------------------------------------
import ai_v02 as ai
import pygame
import random as r
from helper import GameObject
from battleData import AttackType
from battleData import allAttackTypes
from battleData import allCounterattackTypes
from battleData import allAllies
from battleData import allEnemies
#-------------------------------------------------------------------------------


class Battle(object):
    def __init__(self, allies, enemies):
        self.allies = allies
        self.enemies = enemies
        self.displayText = ""
        self.displayText2 = ""
        self.displayText3 = ""
        self.displayingCursor = False
        self.battleOver = False
        self.winner = None
        self.actions = []
        self.state = "starting"
        self.counterattacks = []
    
    # Setter methods:
    def changeState(self, newState, lineNum=None):
        if lineNum != None:
            print("Changing battle state from", self.state, "to", newState, 
                "(Line", str(lineNum) + ")")
        else:
            print("Changing battle state from", self.state, "to", newState)
        # Since this method also serves for debug purposes,
        # there's no reason for me to *not* use this setter.
        self.state = newState
    
    def changeText(self, newText):
        self.displayText = newText
        
    def changeText2(self, newText):
        self.displayText2 = newText
        
    def changeText3(self, newText):
        self.displayText3 = newText
    
    def changeCursorDisplay(self, value):
        self.displayingCursor = value
    
    def addAction(self, action):
        self.actions.append(action)
    
    def clearText(self):
        self.displayText = ""
        self.displayText2 = ""
        self.displayText3 = ""
    # I ran into issues trying to change states and text directly,
    # so there are setter methods to get around that.
    
    def writeHistory(self, message, file="battleHistory.txt", end="\n"):
        f = open(file, "a")
        f.write(str(message) + str(end))
        f.close()
    
    # Write out everyone's actions to battle history.
    # Currently unused. Might be used in the future.
    def writeTurnHistory(self):
        history = ""
        def getLowHPCombatants(self):
            weakCombatants = set()
            for combatant in (self.allies + self.enemies):
                if combatant.HP <= combatant.maxHP * 0.3:
                    weakCombatants.add(combatant)
            return weakCombatants
        weakCombatants = getLowHPCombatants(self)
        history += str(weakCombatants)
        history += ", " + str(self.actions)[1:-1].reverse()
        self.writeHistory(history)
    
    def engage(self):
        if len(self.enemies) == 1:
            self.displayText = self.enemies[0].name + " engages you!"
        else:
            self.displayText = self.enemies[0].name + \
                " and its cohorts engage you!"
        self.displayText2 = ""
        self.changeState("text0")
        self.writeHistory("!startOfBattle")
    
    def turn(self):
        # Following wasn't necessary before...
        # Considering I'm having problems with non-menu battle state changes
        # inside battle_vXX.py, I should probably forbid this.
        if len(self.actions) <= 0:
            self.counterattacks = []
            self.changeState("enemyTurn")
            return
        action = self.actions.pop()
        print(action)
        # Don't execute counterattacks when they're popped.
        # They'll get executed later.
        if type(action) == Counterattack:
            pass
        elif len(self.counterattacks) > 0:
            attackWasCountered = False
            for i in range(len(self.counterattacks)-1, -1, -1):
                counterattack = self.counterattacks[i]
                print(counterattack.targetAttack)
                if counterattack.targetAttack == action:
                    print("Someone countered this, executing counterattack")
                    attackWasCountered = True
                    counterattack.executeCounterattack(self)
                    self.actions.append(counterattack.userAttack)
                    self.counterattacks.pop(i)
            if not attackWasCountered:
                print("Nobody countered this, executing attack")
                action.executeAttack(self)
        # Program hangs if I don't do this. Weird.
        else:
            print("There are no counterattacks waiting, executing attack")
            action.executeAttack(self)
        for combatant in self.enemies + self.allies:
            combatant.updateStatMods()
        
    # Check if either side has been defeated.
    # The order is important. If everyone has been defeated, then the 
    # player still loses.
    def checkEndOfBattle(self):
        alliesAlive = False
        for ally in self.allies:
            if ally.HP > 0:
                alliesAlive = True
        enemiesAlive = False
        for enemy in self.enemies:
         if enemy.HP > 0:
            enemiesAlive = True
        if not alliesAlive:
            self.battleOver = True
            self.winner = "enemies"
            self.writeHistory("!w:enemies")
        elif not enemiesAlive:
            self.battleOver = True
            self.winner = "allies"
            self.writeHistory("!w:allies")
        return self.battleOver
    
    
    def getEnemyAttacks(self):
        for enemy in self.enemies:
            insights = ai.makePredictions()
            print(enemy, "is deciding what to do...")
            attack = enemy.makeDecision(self.allies, self.enemies, insights)
            enemy.SP -= attack.attackType.spCost
            # Counterattacks have to be handled specially.
            if isinstance(attack, Counterattack):
                self.counterattacks.append(attack)
            self.actions.append(attack)
            print(enemy, "made up its mind.")
    
    def getPlayerAttacks(self):
        self.clearText()
        for ally in self.allies:
            print(str(ally) + "\'s turn.")
            self.displayText = "What will " + ally.name + " do?"
            self.changeState("menu1", lineNum=175)
            self.changeCursorDisplay(True)
            
            #ally.SP -= attack.attackType.spCost
            #self.actions.append(attack)
            pass
    
    # Sort everyone's actions by everyone's speed.
    def sortActions(self):
        def getActSpd(attack):
            return attack.user.speed * attack.user.speedMod
        self.actions.sort(key=getActSpd)
        self.writeHistory(str(self.actions)[1:-1])
    
    def endOfBattle(self):
        self.writeHistory("-")
        if self.winner == "allies":
            self.clearText()
            self.displayText = "You won!"
            expTotal = 0
            for enemy in self.enemies:
                expTotal += enemy.expYield
            if len(self.allies) > 1:
                self.displayText += " " + self.allies[0].name + \
                " and co. gained " + str(expTotal) + " exp."
            else:
                self.displayText += " " + self.allies[0].name + " gained " \
                + str(expTotal) + " exp."
            for ally in self.allies:
                ally.exp += expTotal
                while ally.exp >= ally.nextLevelExp:
                    ally.levelUp(self)
        # Otherwise, game over sequence
        elif self.winner == "enemies":
            self.clearText()
            if len(self.allies) > 1:
                self.displayText = self.allies[0].name + \
                    " and co. were defeated..."
            else:
                self.displayText = self.allies[0].name + \
                    " was defeated..."
        else:
            print("Error: reached end of battle without winner determined", 
                file=sys.stderr)
            exit(1)
        self.changeState("text2")

class Combatant(GameObject):
    def __init__(self, name, stats, attacks, \
    image=pygame.image.load("enemies/empty.gif")):
        self.name = name
        self.initStats(stats)
        self.attacks = attacks # Attacks is a list of AttackTypes.
        self.status = "none"
        self.r = 4
        self.c = 4
        self.image = image
        super().__init__(self.r, self.c, self.image)
    
    def initStats(self, stats):
        assert(len(stats) >= 7)
        self.stats = stats
        self.HP = int(stats[0]) # Stats is a list, but is deconstructed here
        self.maxHP = int(stats[0])
        self.SP = int(stats[1])
        self.maxSP = int(stats[1])
        self.strength = int(stats[2])
        self.strengthMod = 1
        self.defense = int(stats[3])
        self.defenseMod = 1
        self.intelligence = int(stats[4])
        self.intellMod = 1
        self.wisdom = int(stats[5])
        self.wisdomMod = 1
        self.speed = int(stats[6])
        self.speedMod = 1
    
    def __repr__(self):
        return self.name
    
    def updateStatMods(self):
        buffRatio = 3/2
        debuffRatio = 2/3
        self.strengthMod = 1
        self.defenseMod = 1
        self.intellMod = 1
        self.wisdomMod = 1
        self.speedMod = 1
        self.strengthMod = 1
        self.defenseMod = 1
        self.intellMod = 1
        self.wisdomMod = 1
        self.speedMod = 1
        if self.status == "strengthUp": self.strengthMod = buffRatio
        elif self.status == "defenseUp": self.defenseMod = buffRatio
        elif self.status == "intelligenceUp": self.intellMod = buffRatio
        elif self.status == "wisdomUp": self.wisdomMod = buffRatio
        elif self.status == "speedUp": self.speedMod = buffRatio
        elif self.status == "strengthDown": self.strengthMod = debuffRatio
        elif self.status == "defenseDown": self.defenseMod = debuffRatio
        elif self.status == "intelligenceDown": self.intellMod = debuffRatio
        elif self.status == "wisdomDown": self.wisdomMod = debuffRatio
        elif self.status == "speedDown": self.speedMod = debuffRatio
        else: pass

class Enemy(Combatant):
    def __init__(self, name, stats, expYield, attacks, 
                personality, x, y, image):
        super().__init__(name, stats, attacks, image)
        self.personality = personality
        # For graphics:
        self.x = x
        self.y = y
        self.expYield = expYield
    
    def makeDecision(self, allies, enemies, insights):
        def pickRandomLegalMove(enemy, listActions, targets="allies"):
            if targets == "allies":
                target = r.choice(allies)
            elif targets == "enemies":
                target = r.choice(enemies)
            elif targets == "self":
                target == enemy
            else:
                print("Error: enemy", self.name, 
                    "tried to attack invalid target type", targets, 
                        file=sys.stderr)
                exit()
            listLegalActions = []
            for action in listActions:
                if enemy.SP >= action.spCost:
                    listLegalActions.append(action)
            action = r.choice(listActions)
            return Attack(action, self, target)
        
        def hasLegalSPMoves(enemy, listMoves=None):
            if listMoves == None: listMoves = enemy.attacks
            for action in listMoves:
                if action.spCost < enemy.SP:
                    return True
            return False
        
        def makeAlliesDict(allies):
            d = {}
            for ally in allies:
                d.update({ally.name: ally})
            return d
        
        # i hate that i had to do this:
        alliesByName = makeAlliesDict(allies)
        
        lAAttacks = []
        # If you don't play RPGs: a "buff" is a positive status effect.
        # It can also refer to a move that causes such an effect.
        lABuffs = [] # _l_ ist _A_ ttackBuffs, that is
        
        for action in self.attacks:
            if action.kind == "attack":
                lAAttacks.append(action)
            elif action.kind == "buff":
                lABuffs.append(action)
        
        # Erratic personalities attack at random. They never counterattack.
        if self.personality == "erratic":
            return pickRandomLegalMove(enemy, self.attacks)
        # Offensive personalities power themselves up, then attack away.
        elif self.personality == "offensive":
            # If it's the start of the battle, and you have a buff, and can
            # afford it:
            if insights[0] == True and len(lABuffs) > 0 and \
            hasLegalSPMoves(self, lABuffs): 
                # use a buff. Prefer buffs to offensive stats.
                    for buff in lABuffs:
                        if (buff.effect == "strengthUp" or \
                        buff.effect == "intelligenceUp") and \
                        buff.spCost <= self.SP:
                            return Attack(buff, self, self)
                    return pickRandomLegalMove(self, lABuffs, targets="self")
            else:
                for ally in insights[1].keys(): 
                    for action in insights[1][ally].keys():
                        # If the player is 75% likely to use a certain move,
                        # and that move targets enemies, counter it.
                        if insights[1][ally][action] > 0.75 and \
                        allAttackTypes[action].numTargets[1] == "e":
                            print("I'm gonna counter your", action)
                            if not hasLegalSPMoves(self):
                                return Counterattack(
                                Attack(lAAttacks[0], self, r.choice(allies)),
                                Attack(allAttackTypes[action], 
                                    alliesByName[ally], self)
                                )
                            return Counterattack(
                                pickRandomLegalMove(self, lAAttacks),
                                Attack(allAttackTypes[action], 
                                    alliesByName[ally], self)
                                )
                # else, there's nothing interesting going on, attack!
                return pickRandomLegalMove(self, lAAttacks)
        # Aggressive personalities only ever attack. They avoid the basic attack
        # if possible. In the future, will target allies with the lowest health.
        elif self.personality == "aggressive":
            for ally in insights[1].keys(): 
                for action in insights[1][ally].keys():
                    # If the player is 90% likely to use a certain move,
                    # and that move targets enemies, counter it.
                    # The aggressive type would rather just attack you first...
                    if insights[1][ally][action] > 0.90 and \
                    allAttackTypes[action].numTargets[1] == "e":
                        print("I'm gonna counter your", action)
                        if not hasLegalSPMoves(self):
                            return Counterattack(
                            Attack(lAAttacks[0], self, r.choice(allies)),
                            Attack(allAttackTypes[action], 
                                alliesByName[ally], self)
                            )
                        return Counterattack(
                            pickRandomLegalMove(self, lAAttacks),
                            Attack(allAttackTypes[action], 
                                alliesByName[ally], self)
                            )
            # Only use the regular attack if you've run out of other options.
            if not hasLegalSPMoves(self):
                return Attack(lAAttacks[0], self, r.choice(allies))
            return pickRandomLegalMove(self, lAAttacks[1:])
        # The Grand Wizard has its own personality.
        # On the first turn, it will buff itself with Focus.
        # Then, it will try to counter something if possible, else attack with
        # Ball Lightning, Flame Column or casting.
        # Once its HP drops to half, it will put up a Barrier whenever it's
        # Defense isn't raised.
        # Then, if it has the SP, it will Chant, and then use Arcane Laser.
        # After that, it will return to its behavior before, but not cast.
        elif self.personality == "grand_wizard":
            if insights[0] == True:
                return Attack(self.attacks[1], self, self)
            elif "Grand Wizard>Chant" in insights[3]:
                    return Attack(self.attacks[6], self, r.choice(allies))
            elif self.HP < self.maxHP // 2:
                if self.status != "defenseUp":
                    return Attack(self.attacks[4], self, self)
                elif self.SP > self.attacks[6].spCost:
                    return Attack(self.attacks[5], self, self)
                else:
                    # Counter:
                    for ally in insights[1].keys(): 
                        for action in insights[1][ally].keys():
                            if insights[1][ally][action] > 0.85 and \
                            allAttackTypes[action].numTargets[1] == "e":
                                print("I'm gonna counter your", action)
                                if not hasLegalSPMoves(self):
                                    return Counterattack(
                                    Attack(lAAttacks[0], self, 
                                        r.choice(allies)),
                                    Attack(allAttackTypes[action], 
                                        alliesByName[ally], self)
                                    )
                                return Counterattack(
                                    pickRandomLegalMove(self, lAAttacks[:-1]),
                                    Attack(allAttackTypes[action], 
                                        alliesByName[ally], self)
                                    )
                    if not hasLegalSPMoves(self):
                        return Attack(lAAttacks[0], self, r.choice(allies))
                    return pickRandomLegalMove(self, lAAttacks[1:-1])
            else:
                # Counter:
                for ally in insights[1].keys(): 
                    for action in insights[1][ally].keys():
                        if insights[1][ally][action] > 0.75 and \
                        allAttackTypes[action].numTargets[1] == "e":
                            print("I'm gonna counter your", action)
                            if not hasLegalSPMoves(self):
                                return Counterattack(
                                Attack(lAAttacks[0], self, 
                                    r.choice(allies)),
                                Attack(allAttackTypes[action], 
                                    alliesByName[ally], self)
                                )
                            return Counterattack(
                                pickRandomLegalMove(self, lAAttacks[:-1]),
                                Attack(allAttackTypes[action], 
                                    alliesByName[ally], self)
                                )
                return pickRandomLegalMove(self, lAAttacks[:-1])
                
        else:
            print("Error: enemy personality ", "\"" + self.personality + "\"", 
                "does not have defined behavior in battle.", file=sys.stderr)
            exit(1)
    
    def update(self):
        super().update((0,0))

class Ally(Combatant):
    def __init__(self, name, stats, growthRates, attacks, level=1, exp=0):
        super().__init__(name, stats, attacks)
        self.growthRates = growthRates
        self.level = level
        self.exp = exp
        self.nextLevelExp = self.getNextLevelExp(level)
    
    def levelUp(self, ongoingBattle):
        self.level += 1
        ongoingBattle.clearText()
        ongoingBattle.changeText(self.name + " grew to level " + 
            str(self.level) + "!")
        for i in range(len(self.stats)):
            self.stats[i] += self.growthRates[i]
        self.initStats(self.stats)
        self.nextLevelExp = self.getNextLevelExp(self.level)
    
    def update(self):
        super().update((0,0))
    
    def getNextLevelExp(self, level):
            return 25 * (level + 1) * (level + 2) - 50

# I might rename these next two objects to "ActionType" and "Action", since
# not all of them are attacks or do damage.

class Attack(object):
    def __init__(self, attackType, user, targets):
        self.attackType = attackType # An AttackType
        self.user = user # A Combatant
        if type(targets) != list: # A list
            self.targets = [targets]
        else:
            self.targets = targets
    
    def __repr__(self):
        def getName(combatant):
            try: return combatant.name
            except: return None
        return self.user.name + ">" + \
        str(self.attackType.name) + ">" + \
        str(self.attackType.kind) + ">" + \
        str(list(map(getName, self.targets)))[2:-2]
    
    def __eq__(self, other):
        if not isinstance(other, Attack): return False
        return all((
            self.attackType.name == other.attackType.name,
            self.attackType.kind == other.attackType.kind,
            self.user == other.user,
            self.targets == other.targets
        ))
    
    def executeAttack(self, battle):
        effectText = {
        "none": "If you're reading this text, something went horribly wrong",
        "sleep": "[t] fell asleep!",
        "poison": "[t] was poisoned!",
        "dizzy": "[t] suddenly became dizzy!",
        "strengthUp": "[t]'s Strength increased!",
        "defenseUp": "[t]'s Defense increased!",
        "intelligenceUp": "[t]'s Intelligence increased!",
        "wisdomUp": "[t]'s Wisdom increased!",
        "speedUp": "[t]'s Speed increased!",
        "strengthDown": "[t]'s Strength fell!",
        "defenseDown": "[t]'s Defense fell!",
        "intelligenceDown": "[t]'s Intelligence fell!",
        "wisdomDown": "[t]'s Wisdom fell!",
        "speedDown": "[t]'s Speed fell!"
        }
        
        # Calculate damage, deal it.
        battle.clearText()
        battle.changeText(self.attackType.text.replace("[u]", self.user.name))
        for target in self.targets:
            # Deal damage if applicable:
            if self.attackType.power > 0 and self.attackType.kind != "heal":
                if self.attackType.isMagic:
                    damage = self.attackType.power + self.user.intelligence * \
                        self.user.intellMod - target.wisdom * target.wisdomMod
                else:
                    damage = self.attackType.power + self.user.strength * \
                        self.user.strengthMod - target.defense * \
                        target.defenseMod
                damage = int(damage)
                # Prevent negative damage from being dealt.
                if damage < 0:
                    damage = 0
                battle.changeText2(target.name + " took " + str(damage) 
                    + " damage!")
                battle.changeState("text1", lineNum=535)
                target.HP -= damage
            # Or, heal:
            elif self.attackType.kind == "heal":
                if self.attackType.isMagic:
                    healing = self.attackType.power + self.user.intelligence * \
                        self.user.intellMod
                else:
                    healing = self.attackType.power + self.user.strength * \
                        self.user.strengthMod
                healing = int(healing)
                # Prevent negative healing from being applied.
                if healing < 0:
                    healing = 0
                battle.changeText2(target.name + " recovered " + str(healing)
                    + " HP!")
                battle.changeState("text1", lineNum=551)
                target.HP += healing
                # Prevent overhealing:
                if target.HP > target.maxHP:
                    target.HP = target.maxHP
            # If the target's HP falls below zero, they faint. 
            # Inflict no effects.
            if target.HP <= 0:
                # TODO: different messages for allies and enemies
                battle.changeText3(target.name + " was defeated!")
                battle.changeState("text3", lineNum=561)
                target.status = "none"
                return
            # If the RNG inflicts an effect, do so
            if self.attackType.effect != "none":
                randChance = r.randrange(1,128)
                if randChance <= self.attackType.effectChance:
                    target.status = self.attackType.effect
                    if battle.displayText2 == "":
                        battle.changeText2(
                            effectText[self.attackType.effect].replace("[t]", 
                            target.name))
                    else:
                        battle.changeText3(
                            effectText[self.attackType.effect].replace("[t]", 
                            target.name))
            battle.changeState("text1", lineNum=572)

# The combatant counterattacking is the "user" here.
class Counterattack(object):
    def __init__(self, userAttack, targetAttack):
        # You can only counterattack the combatant attacking you:
        def validateCounterattackTarget(userAttack, targetAttack):
            print("The counterattack\'s user:", userAttack.user.name)
            for target in targetAttack.targets:
                print("One of the incoming attack's targets:", target.name)
                if target.name == userAttack.user.name:
                    return
            print("Error: tried to counterattack an attack not", 
                "aimed at counterattacker", file=sys.stderr)
            exit(1)
        validateCounterattackTarget(userAttack, targetAttack)
        # Counterattacks have to be attacks, for now
        if userAttack.attackType.kind != "attack" \
        and userAttack.attackType.kind != "debuff":
            print("Error: tried to use non-attacking move as a counterattack", 
                file=sys.stderr)
            exit(1)
        self.userAttack = userAttack
        # Swap out the user's input attack for the powerful counter version
        self.userAttack.attackType = \
            allCounterattackTypes[self.userAttack.attackType.name]
        self.targetAttack = targetAttack
        self.attackType = self.userAttack.attackType
        self.user = self.userAttack.user
    
    def __repr__(self):
        def getName(combatant):
            try: return combatant.name
            except: return None
        return self.user.name + ">" + \
        str(self.userAttack.attackType.name) + ">" + \
        str(self.attackType.kind) + ">" + \
        str(list(map(getName, self.userAttack.targets)))[2:-2]
    
    
    def executeAttack(self, battle):
        pass
    
    def executeCounterattack(self, battle):
        battle.changeText(self.targetAttack.attackType.text.replace("[u]", 
            self.targetAttack.user.name))
        battle.changeText2("...but " + self.user.name + 
            " saw it coming and dodged!")
        battle.changeText3("Here is " + self.user.name + "\'s counterattack:")
        battle.changeState("text1")
