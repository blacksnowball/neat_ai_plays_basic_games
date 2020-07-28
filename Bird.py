import pygame


class Bird:
    GRAVITY = 0.5

    def __init__(self, sprites, sprites_hitboxes):
        self.sprites = sprites
        self.sprites_hitboxes = sprites_hitboxes
        self.current_state = 0
        self.current_img = self.sprites[self.current_state]
        self.current_hitbox = self.sprites_hitboxes[self.current_state]
        self.velY = 0

    def rotate(self):
        return pygame.transform.rotozoom(self.sprites[self.current_state], - self.velY * 2.5, 1)

    def transition(self):
        if self.current_state < 2:
            self.current_state += 1
        else:
            self.current_state = 0

    def flap(self):
        # temporarily suspend effects of gravity by resetting Y velocity
        # otherwise spamming flap will send us flying off the screen
        self.velY = 0
        self.velY -= 12
        self.update_hitbox_centre()

    def reset(self, x, y):
        self.current_hitbox.center = (x, y)
        self.velY = 0

    def move(self):
        # when not flapping, experience gravity and update centre of hitbox
        self.velY += Bird.GRAVITY
        self.update_hitbox_centre()

    def collide_check(self):
        if self.current_hitbox.top <= -100 or self.current_hitbox.bottom >= 875:
            return True
        return False

    def update_hitbox_centre(self):
        # update centre of hitbox as we move coordinates of bird
        # occurs when we experience gravity or flap
        self.current_hitbox.centery += self.velY

    def draw_bird(self, window):
        window.blit(self.rotate(), self.current_hitbox)