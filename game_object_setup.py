import pygame
import random
import re

class GameObject:
    def __init__(self, screen, id, x, y, width, height, r, g, b, alpha, danger, parent, timestart, timestop, movex, movey):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.set_alpha(alpha)
        self.surface.fill((r, g, b, alpha))
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.movex = movex
        self.movey = movey
        self.danger = danger
        self.parent = parent
        self.parent_object = None
        self.timestart = timestart
        self.timestop = timestop
        self.movextimer = 0
        self.moveytimer = 0
        self.rotatetimer = 0
        self.screen = screen
        self.lifelost = False
        self.end_parent = False

    def update(self):
        self.lifelost = False
        if self.parent_object and not self.end_parent:  # Set coordinates to parent coordinates
            self.rect.x = self.parent_object.rect.x
            self.rect.y = self.parent_object.rect.y
            self.end_parent = True
        self.screen.blit(self.surface, self.rect)
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and self.danger == "yes":  # Lose a life when collided with
            self.lifelost = True



def create_game_objects(csv_data, screen):
    game_objects = []
    for row in csv_data:
        id, x, y, width, height, r, g, b, alpha, danger, parent, timestart, timestop, movex, movey = row  # Extract data from the row

        # Convert string values to appropriate types
        try:
            id = int(id)
        except ValueError:
            pass

        width = int(width)
        height = int(height)

        try:
            x = int(x)
        except ValueError:
            x = random.randint(150, (1760 - width))

        try:
            y = int(y)
        except ValueError:
            y = random.randint(90, (1000 - height))

        try:
            r = int(r)
        except ValueError:
            r = random.randint(0, 255)
        
        try:
            g = int(g)
        except ValueError:
            g = random.randint(0, 255)
        
        try:
            b = int(b)
        except ValueError:
            b = random.randint(0, 255)
        
        try:
            alpha = int(alpha)
        except ValueError:
            alpha = random.randint(0, 255)          
        
        game_object = GameObject(screen, id, x, y, width, height, r, g, b, alpha, danger, parent, timestart, timestop, movex, movey)
        game_objects.append(game_object)

        # Get the parent (if any) to determine x and y values
        parent_condition = re.search('n', parent, re.I)  # Find a null value with RegEx
        if parent_condition == None:
            parent = int(parent)
            for objects in game_objects:
                if objects.id == parent:
                    game_object.parent_object = objects
                    break
        
        timestart = float(timestart)
        timestop = float(timestop)

        movex = int(movex)
        movey = int(movey)

    return game_objects