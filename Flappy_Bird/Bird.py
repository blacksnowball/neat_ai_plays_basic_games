import pygame

class Bird:

    GRAVITY = 0.3

    def __init__(self, sprites, x, y, APP_HEIGHT):
        self.x = x
        self.y = y
        self.sprites = sprites
        self.current_state = 0
        self.velY = 0
        self.height_limit = APP_HEIGHT
        self.dead = False

    def window_collide_check(self):
        return self.y <= -150 or self.y >= .85 * self.height_limit

    def death_event(self, death_sound):
        if not self.dead:
            death_sound.play()
        self.dead = True

    def flap(self, flap_sound):
        if not self.dead:
            flap_sound.play()
            self.velY = 0
            self.velY -= 6
            self.y += self.velY

    def move(self):
        self.velY += Bird.GRAVITY
        if self.dead:
            self.velY += 1
        self.y += self.velY

    def transition(self):
        if self.current_state < 2:
            self.current_state += 1
        else:
            self.current_state = 0

    def get_mask(self):
        return pygame.mask.from_surface(self.sprites[self.current_state])

    def draw(self, window):
        window.blit(pygame.transform.rotozoom(self.sprites[self.current_state], max(- self.velY * 2.5, -90), 1), (self.x, self.y))







