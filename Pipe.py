import random


class Pipe:
    GAP = 250

    def __init__(self, bot_img, top_img):
        # pipes will be stored as their hitboxes
        # we then generate them visually by superimposition later
        self.random_height = random.randint(275, 800)
        self.bot_img = bot_img
        self.top_img = top_img
        self.bot_pipe_hitbox = bot_img.get_rect(midtop=(650, self.random_height))
        self.top_pipe_hitbox = top_img.get_rect(midbottom=(650, self.random_height - Pipe.GAP))
        self.passed = False

    def collision_detect(pipes, bird_hitbox):
        for pipe in pipes:
            if bird_hitbox.colliderect(pipe.bot_pipe_hitbox) or bird_hitbox.colliderect(pipe.top_pipe_hitbox):
                return True
        return False

    def remove_pipes(pipes, bird):
        pipes_to_del = []

        for pipe in pipes:
            if bird.current_hitbox.bottomleft[0] > pipe.bot_pipe_hitbox.bottomright[0] and pipe.bot_pipe_hitbox.bottomright[0] < 0:
                pipes_to_del.append(pipe)

        for pipe in pipes_to_del:
            pipes.remove(pipe)

    def move_pipe(self):
        self.bot_pipe_hitbox.centerx -= 5
        self.top_pipe_hitbox.centerx -= 5

    def draw_pipe(self, window):
        # draw bot pipe if the bottom of the hitbox overlaps with the floor area
        window.blit(self.bot_img, self.bot_pipe_hitbox)
        window.blit(self.top_img, self.top_pipe_hitbox)
