import random, pygame

class Pipe:

    def __init__(self, x, bot_img, top_img):
        # pipes will be stored as their hitboxes
        # we then generate them visually by superimposition later
        self.x = x
        self.velX = 3
        self.bot_img = bot_img
        self.top_img = top_img

        self.height = 0
        # where pipes are in y-axis
        self.bot_pipe_y = 0
        self.top_pipe_y = 0
        self.bird_passed = False

        self.GAP = random.randrange(150, 200)
        self.set_pipe_heights()

    def set_pipe_heights(self):

        #possible_heights = [i for i in range(50, 450, 50)]
        #self.height = random.choice(possible_heights)

        self.height = random.randint(50, 450)

        self.bot_pipe_y = self.height + self.GAP
        self.top_pipe_y = self.height - self.top_img.get_height()

    def move(self):
        self.x -= self.velX

    def bird_pass(self, score_sound):
        self.bird_passed = True
        score_sound.play()

    def collision_detect(self, bird):
        bird_mask = bird.get_mask()
        bot_pipe_mask = pygame.mask.from_surface(self.bot_img)
        top_pipe_mask = pygame.mask.from_surface(self.top_img)

        bot_pipe_offset = (int(self.x - bird.x), int(self.bot_pipe_y - bird.y))
        top_pipe_offset = (int(self.x - bird.x), int(self.top_pipe_y - bird.y))

        return bird_mask.overlap(bot_pipe_mask, bot_pipe_offset) or bird_mask.overlap(top_pipe_mask, top_pipe_offset)

    def draw(self, window):
        # draw bot pipe if the bottom of the hitbox overlaps with the floor area
        window.blit(self.bot_img, (self.x, self.bot_pipe_y))
        window.blit(self.top_img, (self.x, self.top_pipe_y))
