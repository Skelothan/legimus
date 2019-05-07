#-------------------------------------------------------------------------------
# TODO, in the far, far future:
#-------------------------------------------------------------------------------
# > Validate history file, ensure it's not corrupt
#   > Building off that, if it's a common error fix the error.
# > Predictions based on target (this demo is 1-on-1, so it doesn't matter)
# > In conjunction with above, predictions based on player and enemy health
# > A "smarter" prediction/decision system that also takes into account 
# everyone's stats, especially speed, remaining HP, and remaining SP. Knowing
# this would be great asset to decision-making: can I KO this player before they 
# can heal themself? What's the chance my allies get KO'd?
# > Maybe take into account my allies' abilities, and whether the player's seen 
# them or not. The player might target enemies they know have healing 
# abilities, for example.
# > Take into account insufficient data when deciding to attack. The AI can
# use attack types as a secondary source if, for example, the player's never 
# fought a Pyromancer before and a Pyromancer needs to predict what the player's # about to do.
# > Weight enemy behavior in battles that they won more. (this will make it
# easier for the player switch strategies after losing many fights)
# > tbh as battles gets more complicated just train a neural net to win them
#-------------------------------------------------------------------------------

import math
import random

def getFileText(file="battleHistory.txt"):
    f = open(file, "rt")
    fileText = f.read()
    f.close()
    return fileText

# Weights battles according to the function e**(-x/e),
# where x is the number of battles ago the battle occurred
def getDataWeight(battles, battleIndex):
    x = len(battles) - battleIndex - 1
    return math.e ** (-1 * x / math.e)

# Takes in a list of tuples. The first is the move. The second is the weight.
# Returns a dictionary with probabilities of each move.
def weightedAverage(lst):
    output = {}
    sumWeights = 0
    for thing, weight in lst:
        output[thing] = output.get(thing, 0) + weight
        sumWeights += weight
    for key in output.keys():
        output[key] /= sumWeights
    return output

# Takes a string that looks like a set of strings and returns a set based on it.
# Set up so that strToSet(b) == b, given type(b) == set.
# (Why this was so difficult, I have no idea.)
def strToSet(s):
    return set(str(s)[1:-1].replace("\'","").split(", "))

# Returns some insights about previous battles...
# specifically, what the player is likely to do based on what happened last turn
# or whether it's the beginning of the battle.
# The AI bases its decisions on these insights.
def makePredictions(file="battleHistory.txt"):
    # Format the datafile into a list of turns.
    allData = getFileText(file)
    battles = allData.split("-\n")
    battlesTurns = []
    for battle in battles:
        battlesTurns.append(battle.splitlines())
    # Get everyone with low HP from a set.
    # Not implemented yet.
    lowHPCombatants = set()
    # If it's the start of battle, say so.
    if battlesTurns[-1] == ["!startOfBattle"]: isStartOfBattle = True
    else: isStartOfBattle = False
    # Figure the probability of each of the player's next moves, based on their
    # previous battles with the same encounter.
    if battlesTurns[-1] == []: lastTurn = None  # This if is here because of an 
    else: lastTurn = battlesTurns[-1][-1]       # IndexError without it on run.
    nextMoveOccur = {"Lilith":[]} # Could be expanded for new characters.
    nextKindOccur = {"Lilith":[]}
    # Count up the each player action after similar previous turns...
    for b in range(len(battlesTurns)-1, -1, -1):
        for t in range(len(battlesTurns[b])):
            if battlesTurns[b][t] == lastTurn:
                try: nextTurn = battlesTurns[b][t+1]
                except: continue
                # Don't consider this data point if someone fainted on 
                # the next turn.
                if nextTurn[0:3] == "!w:":
                    continue
                allCharsNextTurns = nextTurn.split(", ")
                for charNextTurn in allCharsNextTurns:
                    if charNextTurn.split(">")[0] in nextMoveOccur.keys():
                        weight = getDataWeight(battles, b)
                        charNextTurnDetails = charNextTurn.split(">")
                        char = charNextTurnDetails[0]# Good thing it's not C
                        nextMoveOccur[char].append((charNextTurnDetails[1], 
                            weight))
                        nextKindOccur[char].append((charNextTurnDetails[2], 
                            weight))
    # ...then, do a weighted average to determine likeliness of each move.
    for key in nextMoveOccur.keys():
        nextMoveOccur[key] = weightedAverage(nextMoveOccur[key])
        nextKindOccur[key] = weightedAverage(nextKindOccur[key])
    return isStartOfBattle, nextMoveOccur, nextKindOccur, lastTurn, \

#-------------------------------------------------------------------------------
# A bit about the battleHistory.txt file format:
# Battles are separated by "-\n". Each turn in the battle is a separate line,
# except lines that begin with "!". Those lines refer to other data, such as 
# the start of the battle or who won each battle.
# Within a turn, each Combatant's actions are separated by ", ".
# Each action is formatted like so:
#     Attacker>Attack Name>type>Target(s)
#-------------------------------------------------------------------------------