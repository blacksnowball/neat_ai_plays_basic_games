import random, pygame

class Cactus:

    def __init__(self, sprites, y, initial_previous_x , APP_WIDTH):
        self.y = y
        self.x = 0
        self.initial_previous_x = initial_previous_x
        self.sprites = sprites
        self.img = self.sprites[random.randint(0, 4)]
        self.velX = 8
        self.passed = False
        self.set_x(APP_WIDTH)


    def set_x(self, APP_WIDTH):
        possible_x = [i for i in range(APP_WIDTH, APP_WIDTH+400, 50)]
        random_x = random.choice(possible_x)
        if random_x == self.initial_previous_x:
            random_x += 25
        self.x = random_x
        self.initial_previous_x = random_x

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def collide_detect(self, dino):
        dino_mask = dino.get_mask()
        cactus_mask = self.get_mask()
        offset = (int(self.x - dino.x), int(self.y - dino.y))
        return dino_mask.overlap(cactus_mask, offset)

    def move(self):
        self.x -= self.velX

    def draw(self, window):
        window.blit(self.img, (self.x,self.y))