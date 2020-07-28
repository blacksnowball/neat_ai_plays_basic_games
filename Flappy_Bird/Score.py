import pygame

class Score:

    def __init__(self, app_height, app_width):
        self.font = pygame.font.Font('04B_19.TTF', 40)
        self.current_score = 0
        self.high_score = 0
        self.height = app_height
        self.width = app_width

    def display_score(self, window):

        score_img = self.font.render('{}'.format(int(self.current_score)), True, (255, 255, 255))
        score_box = score_img.get_rect(center=(self.width / 2, 0.95 * self.height))
        window.blit(score_img, score_box)

    def report_stats(self, window, gen, birds, deaths):
        # generations
        score_label = self.font.render("Gens: " + str(gen-1), 1, (0, 0, 0))
        window.blit(score_label, (10, 10))

        # alive
        alive_label = self.font.render("Alive: " + str(len(birds)), 1, (0, 0, 0))
        window.blit(alive_label, (10, 50))

        death_label = self.font.render("Deaths: " + str(deaths), 1, (0, 0, 0))
        window.blit(death_label, (10, 90))

        best_score_label = self.font.render("Best: " + str(self.high_score), 1, (0, 0, 0))
        window.blit(best_score_label, (10, 130))

    def update_score(self):
        self.current_score += 1

    def reset_score(self):
        self.current_score = 0

    def update_high_score(self):
        if self.current_score > self.high_score:
            self.high_score = self.current_score