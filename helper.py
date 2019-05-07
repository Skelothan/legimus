# I ran into circular import problems with these objects, so I stuck them in
# this helper file to get around the issue.
# I feel like there should be a better way to structure everything, but I guess
# not...

import pygame

tileSize = 32

class GameObject(pygame.sprite.Sprite):
    def __init__(self, r, c, image):
        super(GameObject, self).__init__()
        self.tileSize = tileSize
        self.r = r
        self.c = c
        self.x = tileSize * c + tileSize//2
        self.y = tileSize * r + tileSize//2
        self.baseimage = image.copy()
        self.image = image.copy()
        self.updateRect()
        self.velocity = [0,0]
        self.timeAlive = 0
        
        
    # Copied from pygame asteroids demo
    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)
        
    def update(self, scroll):
        self.timeAlive += 1
        vx, vy = self.velocity
        self.x = self.tileSize * self.c + self.tileSize//2 - scroll[1]
        self.y = self.tileSize * self.r + self.tileSize//2 - scroll[0]
        self.updateRect()
    
# Honestly, I should just put this in the battleData file.
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