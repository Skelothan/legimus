import random

def mazeGen(r, c):
    maze = [[0 for i in range(c)] for i in range(r)]
    visited = [[False for i in range(c)] for i in range(r)]
    maze = doMazeGen(maze, visited, (r-1, c//2))
    maze[r-1][0] += 2
    maze[0][c-1] += 1
    # printMaze(maze)
    return maze

def getAdjacentCells(maze, cell):
    r = cell[0]
    c = cell[1]
    cells = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
    for i in range(len(cells)-1, -1, -1):
        if any((
        cells[i][0] < 0,
        cells[i][0] >= len(maze),
        cells[i][1] < 0,
        cells[i][1] >= len(maze[0])
        )):
            cells.pop(i)
    random.shuffle(cells)
    return cells

def doMazeGen(maze, visited, cell):
    isDone = True
    for row in maze:
        if 0 in row:
            isDone = False
    if isDone:
        return maze
    visited[cell[0]][cell[1]] = True
    for adjCell in getAdjacentCells(maze, cell):
        if not visited[adjCell[0]][adjCell[1]]:
            connectCells(maze, cell, adjCell, 1)
            tempMaze = doMazeGen(maze, visited, adjCell)
            if tempMaze != None:
                return tempMaze
    return None

# mode = 1 for forwards, mode = -1 for backwards
def connectCells(maze, cell, adjCell, mode):
    directions = {
    (-1, 0):1, # up
    (1, 0): 2, # down
    (0, -1):4, # left
    (0, 1): 8  # right
    }
    direction = (adjCell[0] - cell[0], adjCell[1] - cell[1])
    maze[cell[0]][cell[1]] += directions[direction] * mode
    maze[adjCell[0]][adjCell[1]] += \
        directions[(direction[0] * -1, direction[1] * -1)] * mode

def printMaze(lst):
    boxes = {
    0: "#",
    1: "╨",
    2: "╥",
    3: "║",
    4: "╡",
    5: "╝",
    6: "╗",
    7: "╣",
    8: "╞",
    9: "╚",
    10: "╔",
    11: "╠",
    12: "═",
    13: "╩",
    14: "╦",
    15: "╬",
    }
    for row in lst:
        for space in row:
            print(boxes[space], end="")
        print("")


