import pygame

class Score:

    def __init__(self, app_height, app_width):
        self.font = pygame.font.Font('04B_19.TTF', 40)
        self.current_score = 0
        self.high_score = 0
        self.height = app_height
        self.width = app_width
        self.ptero_spawn_threshold = 0

    def set_ptero_spawn_threshold(self, threshold):
        self.ptero_spawn_threshold = threshold

    def display_score(self, window):

        score_img = self.font.render('{}'.format(int(self.current_score)), True, ((0,0,0)))
        score_box = score_img.get_rect(center=(self.width / 2, 0.1 * self.height))
        window.blit(score_img, score_box)

    def report_stats(self, window, gen, dinos, deaths, next_ptero_spawn):
        # generations
        score_label = self.font.render("Gens: " + str(gen-1), 1, (0, 0, 0))
        window.blit(score_label, (10, 10))

        # alive
        alive_label = self.font.render("Alive: " + str(len(dinos)), 1, (0, 0, 0))
        window.blit(alive_label, (10, 50))

        death_label = self.font.render("Deaths: " + str(deaths), 1, (0, 0, 0))
        window.blit(death_label, (10, 90))

        best_score_label = self.font.render("Best: " + str(int(self.high_score)), 1, (0, 0, 0))
        window.blit(best_score_label, (10, 130))

        if next_ptero_spawn == 0:
            next_ptero_spawn_label = self.font.render("Next ptero: Not yet", 1, (0, 0, 0))
            window.blit(next_ptero_spawn_label, (.7 * self.width, .04 * self.height))
        else:
            next_ptero_spawn_label = self.font.render("Next ptero: " + str(int(next_ptero_spawn)), 1, (0, 0, 0))
            window.blit(next_ptero_spawn_label, (.77 * self.width, .04 * self.height))


    def update_score(self):
        self.current_score += 0.2

    def reset_score(self):
        self.current_score = 0

    def update_high_score(self):
        if self.current_score > self.high_score:
            self.high_score = self.current_score