import pygame

class Dino:

    GRAVITY = 1.1

    def __init__(self, x, y, running_sprites, ducking_sprites, jumping_sprite):
        self.x = x
        self.y = y
        self.floor_y = y
        self.running_sprites = running_sprites
        self.ducking_sprites = ducking_sprites
        self.jumping_sprite = jumping_sprite
        self.current_state = 0
        self.velY = 0
        self.is_ducking = False
        self.is_jumping = False
        self.is_dead = False
        self.counter = 0

    def move(self):
        if self.is_jumping:
            self.velY -= Dino.GRAVITY

        self.y -= self.velY

        if (self.y >= self.floor_y):
            self.is_jumping = False
            self.velY = 0

    def jump(self, jump_sound):
        if not self.is_jumping:
            #jump_sound.play()
            self.is_jumping = True
            self.velY = 18

    def run_transition(self):
        if not self.is_dead:
            if self.counter % 20 == 0:
                self.current_state = (self.current_state + 1) % 2
            self.counter += 1

    def duck_transition(self):
        if not self.is_dead:

            self.is_ducking = True
            if self.counter % 20 == 0:
                self.current_state = (self.current_state + 1) % 2
            self.counter += 1

    def death_event(self, death_sound):
        if not self.is_dead:
            self.is_dead = True
            #death_sound.play()

    def get_mask(self):
        if self.is_jumping:
            return pygame.mask.from_surface(self.jumping_sprite)
        elif self.is_ducking:
            return pygame.mask.from_surface(self.ducking_sprites[self.current_state])
        return pygame.mask.from_surface(self.running_sprites[self.current_state])

    def get_rect(self):
        if self.is_jumping:
            return self.jumping_sprite.get_rect()
        elif self.is_ducking:
            return self.ducking_sprites[self.current_state].get_rect()
        return self.running_sprites[self.current_state].get_rect()

    def draw(self, window):
        if self.is_jumping:
            window.blit(self.jumping_sprite, (self.x, self.y))
        elif self.is_ducking:
            window.blit(self.ducking_sprites[self.current_state], (self.x, self.y+25))
        else:
            window.blit(self.running_sprites[self.current_state], (self.x, self.y))



