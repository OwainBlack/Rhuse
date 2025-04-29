import pygame

pygame.font.init()



class MousePos():  # Mouse position to inherit
    def get_mouse_pos(self):
        return pygame.mouse.get_pos()



class Player(pygame.sprite.Sprite, MousePos):
    def __init__(self, screen, radius, color):
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.Surface((radius * 2, radius * 2), pygame.HWSURFACE)
        self.surface.set_colorkey((0, 0, 0))
        self.color = color
        self.rect = self.surface.get_rect()
        self.radius = radius
        self.screen = screen
    
    def draw_circle(self):
        pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)
    
    def new_color(self, new_color):
        self.color = new_color
        self.draw_circle()
    
    def update(self):
        mouse_x, mouse_y = self.get_mouse_pos()
        self.rect.center = (mouse_x, mouse_y)
        self.screen.blit(self.surface, self.rect)



class LaggingPlayer(pygame.sprite.Sprite, MousePos):
    def __init__(self, screen, radius, color, lag):
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.Surface((radius * 2, radius * 2), pygame.HWSURFACE)
        self.surface.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.surface, color, (radius, radius), radius)
        self.rect = self.surface.get_rect()
        self.lag = lag
        self.target_x = 0
        self.target_y = 0
        self.screen = screen

    def update(self):
        mouse_x, mouse_y = self.get_mouse_pos()
        self.target_x = mouse_x
        self.target_y = mouse_y

        self.rect.centerx += (self.target_x - self.rect.centerx) * self.lag
        self.rect.centery += (self.target_y - self.rect.centery) * self.lag

        self.screen.blit(self.surface, self.rect)



class Text(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, size, font=None, color=(255,255,255), text='placeholder'):  # Compile-Time Polymorphism
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(text, True, color)
        self.rect = self.text.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.screen = screen
    
    def update(self):
        self.screen.blit(self.text, self.rect)




class Button(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, size, font=None, color=(255,255,255), text='placeholder'):  # Compile-Time Polymorphism
        pygame.sprite.Sprite.__init__(self)
        if font != None:
            self.font = pygame.font.Font(font, size)
        else:
            self.font = pygame.font.SysFont('segoeui', size)
        self.text = self.font.render(text, True, color)
        self.rect = self.text.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        self.mouse_down = False
        self.screen = screen

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_down:
                self.mouse_down = True
            elif not pygame.mouse.get_pressed()[0] and self.mouse_down:
                self.clicked = True
                self.mouse_down = False
        self.screen.blit(self.text, self.rect)