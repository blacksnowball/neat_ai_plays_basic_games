import pygame

class Ptero:

    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        self.sprites = sprites
        self.current_state = 0
        self.counter = 0
        self.velX = 16

    def move(self):
        self.x -= self.velX
        if self.counter % 15 == 0:
            self.current_state = (self.current_state+1) % 2
        self.counter += 1

    def get_mask(self):
        return pygame.mask.from_surface(self.sprites[self.current_state])

    def get_rect(self):
        return self.sprites[self.current_state].get_rect()

    def collide_detect(self, dino):
        dino_mask = dino.get_mask()
        ptero_mask = self.get_mask()
        offset = (round(self.x - dino.x), round(self.y - dino.y-25))
        return dino_mask.overlap(ptero_mask, offset)

    def transition(self):
        if self.current_state < 1:
            self.current_state += 1
        else:
            self.current_state = 0

    def get_mask(self):
        return pygame.mask.from_surface(self.sprites[self.current_state])

    def draw(self, window):
        window.blit(self.sprites[self.current_state], (self.x, self.y))



