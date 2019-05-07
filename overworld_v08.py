# Imports ----------------------------------------------------------------------
import pygame
from pygamegame import PygameGame # Framework by Lukas Peraza
import copy
import random as r
import rooms_v05 as rooms
import battle_v08 as battle
from helper import GameObject
#-------------------------------------------------------------------------------



class Player(GameObject):
    @staticmethod
    def init():
        Player.images = {}
        Player.images["up 0"] = pygame.image.load(
            "player sprite/lilith_walk_u1.gif")
        Player.images["down 0"] = pygame.image.load(
            "player sprite/lilith_walk_d1.gif")
        Player.images["left 0"] = pygame.transform.flip(pygame.image.load(
            "player sprite/lilith_walk_s1.gif"), True, False)
        Player.images["right 0"] = pygame.image.load(
            "player sprite/lilith_walk_s1.gif")
        Player.images["up 1"] = pygame.image.load(
            "player sprite/lilith_walk_u2.gif")
        Player.images["down 1"] = pygame.image.load(
            "player sprite/lilith_walk_d2.gif")
        Player.images["left 1"] = pygame.transform.flip(pygame.image.load(
            "player sprite/lilith_walk_s2.gif"), True, False)
        Player.images["right 1"] = pygame.image.load(
            "player sprite/lilith_walk_s2.gif")
        for value in Player.images.items():
            value[1].convert_alpha()
            pygame.transform.scale2x(value[1])
        
    def updateImage(self):
        self.image = Player.images[self.facing + " " + str(self.animFrame)]
    
    def __init__(self, r, c, facing="down"):
        self.facing = facing
        self.animFrame = 0
        self.updateImage()
        super().__init__(r, c, self.image)
        
    def update(self, scroll):
        super(Player, self).update(scroll)
        if self.timeAlive % 25 == 0:
            self.animFrame = (self.animFrame + 1) % 2
        self.updateImage()
    
    def move(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

class Tile(GameObject):
    @staticmethod
    def init():
        Tile.image = pygame.image.load("walls/debug.gif")
    
    def __init__(self, r, c, image=None):
        if image == None:
            self.image = Tile.image
        else:
            self.image = pygame.image.load(image)
        super().__init__(r, c, self.image)

class Cursor(GameObject):
    @staticmethod
    def init():
        Cursor.image = pygame.image.load("misc_sprites/cursor.gif")
    
    def __init__(self, position, allPositions):
        # position is an int corresponding to keys in allPositions below.
        # It's also used when the space bar is pressed to determine what should
        # be done.
        self.position = position
        # allPositions is a dict containing tuples of row/column coordinates.
        self.allPositions = allPositions
        self.image = Cursor.image
        super().__init__(self.allPositions[self.position][0], 
            self.allPositions[self.position][1], self.image)
    
    def update(self):
        self.r = self.allPositions[self.position][0]
        self.c = self.allPositions[self.position][1]
        super().update((0,0))

class Game(PygameGame):
    @staticmethod
    def loadImages():
        Player.init()
        Tile.init()
        Cursor.init()
        Game.tileSize = 32
        
        
    def init(self):
        Game.loadImages()
        self.titleCursor = Cursor(0, 
        {0:(10, 7), 
         1:(11, 7)})
        self.battleCursor0 = Cursor(0,
        {0:(9, 2), 
         1:(10, 2),
         2:(11, 2),
         3:(12, 2)})
        # In the future: store rooms constructed ahead of time in the rooms file
        self.activeRoom = rooms.Room(rooms.mazeRoomWalls, 
            rooms.mazeRoomEncounters, rooms.mazeRoomSpEncounters)
        self.titleCursorGroup = pygame.sprite.Group(self.titleCursor)
        self.battleCursor0Group = pygame.sprite.Group(self.battleCursor0)
        
        self.playerGroup = pygame.sprite.Group(Player(41, 2))
        self.tileGroup = pygame.sprite.Group()
        self.allyGroup = pygame.sprite.Group()
        self.allyList = []
        self.enemyGroup = pygame.sprite.Group()
        self.enemyList = []
        self.loadRoom(self.activeRoom, self.tileGroup)
        self.framesPassed = 0
        self.state = "title"
        self.scroll = [Game.tileSize * 34,Game.tileSize * -5]
        # Also in the future: store allies pre-constructed in a separate file
        # (probably battleData.py)
        lilith = battle.Ally(battle.allAllies["Lilith"][0], 
        battle.allAllies["Lilith"][1], battle.allAllies["Lilith"][2], 
        battle.allAllies["Lilith"][3], level=1, 
        exp=0)
        self.allyGroup.add(lilith)
        self.allyList.append(lilith)

        
    def loadRoom(self, room, tileGroup):
        # A dictionary that holds sprite data for floors.
        tileset = {
        -2: "walls/empty.gif",
        -1: "walls/redbrown_bevel.gif",
         0: "walls/bricks_dark.gif",
        16: "walls/bricks_dark.gif",
        32: "walls/bricks_dark.gif",
        65: "walls/bricks_wizard.gif"
        }
        for r in range(len(room.walls)):
            for c in range(len(room.walls[r])):
                tileGroup.add(Tile(r,c,tileset[room.walls[r][c]]))
    
    def keyPressed(self, keyCode, mod):
        if self.state == "title":
            if keyCode == pygame.K_UP or keyCode == pygame.K_w:
                for cursor in self.titleCursorGroup:
                    cursor.position -= 1
                    cursor.position %= 2
            elif keyCode == pygame.K_DOWN or keyCode == pygame.K_s:
                for cursor in self.titleCursorGroup:
                    cursor.position += 1
                    cursor.position %= 2
            elif keyCode == pygame.K_SPACE or keyCode == pygame.K_RETURN:
                assert(type(self.titleCursor.position) == int)
                assert(0 <= self.titleCursor.position <= 1)
                if self.titleCursor.position == 0:
                    self.state = "overworld"
                elif self.titleCursor.position == 1:
                    exit()
                else:
                    print("Error: Invalid title cursor position", 
                        file=sys.stderr)
                    exit(1)
    
        elif self.state == "overworld":
            if keyCode == pygame.K_UP or keyCode == pygame.K_w:
                for player in self.playerGroup:
                    player.facing = "up"
                    player.updateImage()
                    player.r -= 1
                    self.scroll[0] -= self.tileSize
                    if self.activeRoom.walls[player.r][player.c] < 0:
                        player.r += 1
                        self.scroll[0] += self.tileSize
            elif keyCode == pygame.K_DOWN or keyCode == pygame.K_s:
                for player in self.playerGroup:
                    player.facing = "down"
                    player.updateImage()
                    player.r += 1
                    self.scroll[0] += self.tileSize
                    if self.activeRoom.walls[player.r][player.c] < 0:
                        player.r -= 1
                        self.scroll[0] -= self.tileSize
            elif keyCode == pygame.K_LEFT or keyCode == pygame.K_a:
                for player in self.playerGroup:
                    player.facing = "left"
                    player.updateImage()
                    player.c -= 1
                    self.scroll[1] -= self.tileSize
                    if self.activeRoom.walls[player.r][player.c] < 0:
                        player.c += 1
                        self.scroll[1] += self.tileSize
            elif keyCode == pygame.K_RIGHT or keyCode == pygame.K_d:
                for player in self.playerGroup:
                    player.facing = "right"
                    player.updateImage()
                    player.c += 1
                    self.scroll[1] += self.tileSize
                    if self.activeRoom.walls[player.r][player.c] < 0:
                        player.c -= 1
                        self.scroll[1] -= self.tileSize
            elif keyCode == pygame.K_j:
                for ally in self.allyList:
                    ally.exp += 500
                    print(ally.name + "'s exp increased by 500")
            elif keyCode == pygame.K_k:
                for ally in self.allyList:
                    ally.HP = ally.maxHP
                    ally.SP = ally.maxSP
                    print(ally.name + " fully healed.")
            
            # Random encounter code:
            for player in self.playerGroup:
                randEncounter = r.randrange(1,128)
                print("randEncounter:", randEncounter)
                if self.activeRoom.walls[player.r][player.c] <= 64:
                    if randEncounter <= \
                    self.activeRoom.walls[player.r][player.c]:
                        print("Random encounter, starting battle now")
                        self.state = "battle"
                        encounter = r.choice(self.activeRoom.encounters)
                        self.enemyGroup = pygame.sprite.Group()
                        self.enemyList = []
                        for enemy in encounter:
                            self.enemyGroup.add(enemy)
                            self.enemyList.append(copy.copy(enemy))
                        self.ongoingBattle = battle.Battle(self.allyList, 
                            self.enemyList)
                elif self.activeRoom.walls[player.r][player.c] == 65:
                    print("Special encounter, starting battle now")
                    self.state = "battle"
                    encounter = self.activeRoom.specialEncounters[0]
                    self.enemyGroup = pygame.sprite.Group()
                    self.enemyList = []
                    for enemy in encounter:
                        self.enemyGroup.add(enemy)
                        self.enemyList.append(copy.copy(enemy))
                        self.ongoingBattle = battle.Battle(self.allyList, 
                            self.enemyList)
        
        elif self.state == "battle":
            if self.ongoingBattle.state == "text0":
                if keyCode == pygame.K_SPACE or keyCode == pygame.K_RETURN:
                    self.ongoingBattle.clearText()
                    self.ongoingBattle.changeState("enemyTurn")
                    print(self.ongoingBattle.state)
            elif self.ongoingBattle.state == "menu1":
                if keyCode == pygame.K_UP or keyCode == pygame.K_w:
                    for cursor in self.battleCursor0Group:
                        cursor.position -= 1
                        cursor.position %= 4
                elif keyCode == pygame.K_DOWN or keyCode == pygame.K_s:
                    for cursor in self.battleCursor0Group:
                        cursor.position += 1
                        cursor.position %= 4
                # This 80-character limit is really inconvenient...
                # I _really_ should have made a TextWindow object.
                # Better yet, a whole text processing package...
                elif keyCode == pygame.K_SPACE or keyCode == pygame.K_RETURN:
                    for cursor in self.battleCursor0Group:
                        # Don't do anything if you don't have the SP for it.
                        currAlly = self.ongoingBattle.allies[0]
                        if currAlly.attacks[cursor.position].spCost > \
                        currAlly.SP:
                            pass
                        elif currAlly.attacks[cursor.position].kind == "heal":
                            self.ongoingBattle.addAction(battle.Attack(
                            currAlly.attacks[cursor.position], currAlly, 
                            currAlly))
                            currAlly.SP -= \
                                currAlly.attacks[cursor.position].spCost
                            self.ongoingBattle.changeCursorDisplay(False)
                            self.ongoingBattle.changeState("sorting")
                        else:
                            self.ongoingBattle.addAction(
                            battle.Attack(currAlly.attacks\
                            [cursor.position], currAlly, 
                            r.choice(self.ongoingBattle.enemies)))
                            currAlly.SP -= \
                                currAlly.attacks[cursor.position].spCost
                            self.ongoingBattle.changeCursorDisplay(False)
                            self.ongoingBattle.changeState("sorting")
                    
            elif self.ongoingBattle.state == "text1":
                if keyCode == pygame.K_SPACE or keyCode == pygame.K_RETURN:
                    if len(self.ongoingBattle.actions) <= 0:
                        self.ongoingBattle.changeState("enemyTurn")
                    else:
                        self.ongoingBattle.changeState("executing")
            elif self.ongoingBattle.state == "text2":
                if keyCode == pygame.K_SPACE or keyCode == pygame.K_RETURN:
                    self.state = "overworld"
            elif self.ongoingBattle.state == "text3":
                if keyCode == pygame.K_SPACE or keyCode == pygame.K_RETURN:
                    isEndOfBattle = self.ongoingBattle.checkEndOfBattle()
                    if isEndOfBattle:
                        self.ongoingBattle.changeState("ending")
                    elif len(self.ongoingBattle.actions) <= 0:
                        self.ongoingBattle.changeState("enemyTurn")
                    else:
                        self.ongoingBattle.changeState("executing")
            
            else:
                pass
        
    
    def timerFired(self, dt):
        self.framesPassed += 1
        if self.state == "title":
            self.titleCursorGroup.update()
        elif self.state == "overworld":
            self.playerGroup.update(self.scroll)
            self.tileGroup.update(self.scroll)
        elif self.state == "battle":
            self.allyGroup.update()
            self.enemyGroup.update()
            self.battleCursor0Group.update()
            self.battleStep()
            
    def battleStep(self):
        if self.ongoingBattle.state[0:4] == "text" \
        or self.ongoingBattle.state[0:4] == "menu":
            # Hang the battle if text is being displayed.
            # This state is only removed by the space bar/enter key.
            pass
        elif self.ongoingBattle.state == "starting":
            self.ongoingBattle.engage()
        elif self.ongoingBattle.state == "enemyTurn":
            self.ongoingBattle.getEnemyAttacks()
            self.ongoingBattle.changeState("playerTurn")
        elif self.ongoingBattle.state == "playerTurn":
            self.ongoingBattle.getPlayerAttacks()
        elif self.ongoingBattle.state == "sorting":
            self.ongoingBattle.sortActions()
            self.ongoingBattle.changeState("executing")
        elif self.ongoingBattle.state == "executing":
            self.ongoingBattle.turn()
        elif self.ongoingBattle.state == "ending":
            self.ongoingBattle.endOfBattle()
        else:
            print("Error: battle in invalid state", file=sys.stderr)
            exit(1)
    
    
    # I'm under the impression that the SysFonts here aren't actually doing
    # anything for some reason, but I'd need to test this to confirm.
    def redrawAll(self, screen):
        pygame.draw.rect(screen, (0,0,0), 
            pygame.Rect(0, 0, self.width, self.height))
        
        WHITE = (255,255,255)
        NAVY = (0,0,63)
        GRAY = (127, 127, 127)
        
        
        def drawHealthbar(screen, r, c, ally):
            pygame.draw.rect(screen, GRAY, 
                pygame.Rect(self.tileSize * c - 4, self.tileSize * r - 4, 
                self.tileSize * (c + 4) + 8, self.tileSize * (r + 1.5) + 4))
            pygame.draw.rect(screen, NAVY, 
                pygame.Rect(self.tileSize * c, self.tileSize * r, 
                self.tileSize * (c + 4), self.tileSize * (r + 1.5)))
            healthbarFont = pygame.font.Font("Andale Mono.ttf", 18)
            hbNameText = healthbarFont.render(ally.name + " Lv." + 
                str(ally.level), True, WHITE)
            hbHPText = healthbarFont.render("HP: " + str(ally.HP) + "/" + 
                str(ally.maxHP), True, WHITE)
            hbSPText = healthbarFont.render("SP: " + str(ally.SP) + "/" + 
                str(ally.maxSP), True, WHITE)
            screen.blit(hbNameText, (self.tileSize * c + 8, 
                self.tileSize * r + 8))
            screen.blit(hbHPText, (self.tileSize * c + 8, 
                self.tileSize * (r + 1) + 8))
            screen.blit(hbSPText, (self.tileSize * c + 8, 
                self.tileSize * (r + 2) + 8))
        
        
        if self.state == "title":
            titleFont = pygame.font.SysFont("Arial", 72)
            menuFont = pygame.font.SysFont("Arial", 32)
            titleText = titleFont.render("Legimus", True, WHITE)
            screen.blit(titleText, (self.width / 2, self.height / 3))
            menuText0 = menuFont.render("Start Game", True, WHITE)
            menuText1 = menuFont.render("Quit", True, WHITE)
            screen.blit(menuText0, (self.tileSize * 8 + 8, 
                self.tileSize * 10 + 8))
            screen.blit(menuText1, (self.tileSize * 8 + 8, 
                self.tileSize * 11 + 8))
            self.titleCursorGroup.draw(screen)
        elif self.state == "overworld":
            self.tileGroup.draw(screen)
            self.playerGroup.draw(screen)
            drawHealthbar(screen, 14, 1, self.allyList[0])
        elif self.state == "battle":
            # Should be replaced with individual draw functions for each enemy.
            # If an enemy is KO'd, it should not be drawn.
            if not self.ongoingBattle.winner == "allies":
                self.enemyGroup.draw(screen)
            battleFont = pygame.font.SysFont("Arial", 24)
            battleText = battleFont.render(self.ongoingBattle.displayText, 
                True, WHITE)
            battleText2 = battleFont.render(self.ongoingBattle.displayText2, 
                True, WHITE)
            battleText3 = battleFont.render(self.ongoingBattle.displayText3, 
                True, WHITE)
            pygame.draw.rect(screen, (0,0,0), 
                pygame.Rect(0, 0, self.tileSize * 2, self.tileSize * 2))
            screen.blit(battleText, (self.tileSize * 2 + 8, 
                self.tileSize * 1 + 8))
            screen.blit(battleText2, (self.tileSize * 2 + 8, 
                self.tileSize * 2 + 8))
            screen.blit(battleText3, (self.tileSize * 2 + 8, 
                self.tileSize * 3 + 8))
            if self.ongoingBattle.displayingCursor:
                self.battleCursor0Group.draw(screen)
                battleMenuText1 = \
                battleFont.render(self.ongoingBattle.allies[0].attacks[0].name, 
                    True, WHITE)
                battleMenuText2 = \
                battleFont.render(self.ongoingBattle.allies[0].attacks[1].name,
                    True, WHITE)
                battleMenuText3 = \
                battleFont.render(
                    str(self.ongoingBattle.allies[0].attacks[2]), 
                    True, WHITE)
                battleMenuText4 = \
                battleFont.render(
                    str(self.ongoingBattle.allies[0].attacks[3]), 
                    True, WHITE)
                screen.blit(battleMenuText1, (self.tileSize * 3 + 8, 
                    self.tileSize * 9 + 8))
                screen.blit(battleMenuText2, (self.tileSize * 3 + 8, 
                    self.tileSize * 10 + 8))
                screen.blit(battleMenuText3, (self.tileSize * 3 + 8, 
                    self.tileSize * 11 + 8))
                screen.blit(battleMenuText4, (self.tileSize * 3 + 8, 
                    self.tileSize * 12 + 8))
            drawHealthbar(screen, 14, 1, self.allyList[0])
        
Game(32*15, 32*17).run()
    