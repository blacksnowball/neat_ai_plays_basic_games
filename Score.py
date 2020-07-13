import pygame

class Score:

    def __init__(self, app_height, app_width):
        self.font = pygame.font.Font('04B_19.TTF', 40)
        self.current_score = 0
        self.high_score = 0
        self.height = app_height
        self.width = app_width

    def display_score(self, window, game_active):

        if not game_active:
            score_img = self.font.render('Score: {}'.format(int(self.current_score)), True, (255, 255, 255))
            score_box = score_img.get_rect(center=(self.width / 2, 0.075 * self.height))
            window.blit(score_img, score_box)

            score_img_2 = self.font.render('High Score: {}'.format(int(self.high_score)), True, (255,255,255))
            score_box_2 = score_img_2.get_rect(center=(self.width / 2, 0.80 * self.height))
            window.blit(score_img_2, score_box_2)

        else:
            score_img = self.font.render('{}'.format(int(self.current_score)), True, (255, 255, 255))
            score_box = score_img.get_rect(center=(self.width / 2, 0.075 * self.height))
            window.blit(score_img, score_box)

    def update_score(self):
        self.current_score += 1

    def reset_score(self):
        self.current_score = 0

    def update_high_score(self):
        if self.current_score > self.high_score:
            self.high_score = self.current_score