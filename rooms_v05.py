import mazegen
import battle_v08 as battle
import battleData

class Room(object):
    def __init__(self, walls, encounters, specialEncounters = []):
        self.walls = walls # A 2D list containing positions of walls, items, etc
        self.encounters = encounters # A list containing potential encounters as
                                  # lists of enemies.
        self.specialEncounters = specialEncounters


def makeMazeBlock(cell):
    hallways = {
    1: (0,1), # up
    2: (2,1), # down
    4: (1,0), # left
    8: (1,2)  # right
    }
    block = [[-1 for i in range(3)] for i in range(3)]
    block[1][1] = 16
    for key, value in hallways.items():
        if cell & key == key:
            block[value[0]][value[1]] = 16
    return block

def makeMazeRoom(mazeData):
    tempRow = [[],[],[]]
    room = []
    for dataRow in mazeData:
        for dataCell in dataRow:
            block = makeMazeBlock(dataCell)
            for i in range(3):
                tempRow[i] += block[i]
        room += tempRow
        tempRow = [[],[],[]]
    return room

mazeData = mazegen.mazeGen(12,7)
mazeRoomWalls = makeMazeRoom(mazeData)


# TODO: rewrite the Enemy constructor so that this thing will look neater.
# Also: move these to the battleData file? Or premake each enemy type?
mazeRoomEncounters = [
[battle.Enemy(
battleData.allEnemies["Pyromancer"][0],
battleData.allEnemies["Pyromancer"][1],
battleData.allEnemies["Pyromancer"][2],
battleData.allEnemies["Pyromancer"][3],
battleData.allEnemies["Pyromancer"][4], 512, 512, 
battleData.allEnemies["Pyromancer"][5]
)],
[battle.Enemy(
battleData.allEnemies["Construct"][0],
battleData.allEnemies["Construct"][1],
battleData.allEnemies["Construct"][2],
battleData.allEnemies["Construct"][3],
battleData.allEnemies["Construct"][4], 512, 512, 
battleData.allEnemies["Construct"][5]
)],
[battle.Enemy(
battleData.allEnemies["Electromancer"][0],
battleData.allEnemies["Electromancer"][1],
battleData.allEnemies["Electromancer"][2],
battleData.allEnemies["Electromancer"][3],
battleData.allEnemies["Electromancer"][4], 512, 512, 
battleData.allEnemies["Electromancer"][5]
)]
]

mazeRoomSpEncounters = [
[battle.Enemy(
battleData.allEnemies["Grand Wizard"][0],
battleData.allEnemies["Grand Wizard"][1],
battleData.allEnemies["Grand Wizard"][2],
battleData.allEnemies["Grand Wizard"][3],
battleData.allEnemies["Grand Wizard"][4], 512, 512, 
battleData.allEnemies["Grand Wizard"][5]
)]
]

startingArea = [[-1, 0, 0, 0, -1] for i in range(3)]
startingArea.append([-1 for i in range(5)])

bossRow = [-2 for i in range(11)] + [-1] + [0 for i in range(8)] + [-1]
bossArea = [[-2 for i in range(11)] + [-1] + [-1 for i in range(8)] + [-1]]
for i in range(3):
    bossArea.append(bossRow.copy())
bossArea[2][13] = 65

mazeRoomWalls = bossArea + mazeRoomWalls + startingArea


#TODO: Maze generator

demoRoom1Walls = [
[-1, -1, -1, -1, -1, -1, -1, -1],
[-1,  0,  0,  0,  0,  0,  0, -1],
[-1,  0,  0,  0,  0,  0,  0, -1],
[-1,  0,  0, 32, 32,  0,  0, -1],
[-1,  0,  0, 32, 32,  0,  0, -1],
[-1,  0,  0,  0,  0,  0,  0, -1],
[-1,  0,  0,  0,  0,  0,  0, -1],
[-1, -1, -1, -1, -1, -1, -1, -1]
]

demoRoom1Enemies = {}

demoRoom1Warps = {}

demoRoom2Walls = [
[-1, -1, -1, -1, -1, -1, -1, -1],
[-1,  0,  0,  0,  0,  0,  0, -1],
[-1,  0,  0,  0,  0,  0,  0, -1],
[-1,  0,  0, 32, 32,  0,  0, -1],
[-1,  0,  0, 32, 32,  0,  0, -1],
[-1,  0,  0,  0,  0,  0,  0, -1],
[-1,  0,  0,  0,  0,  0,  0, -1],
[-1, -1, -1, -1, -1, -1, -1, -1]
]