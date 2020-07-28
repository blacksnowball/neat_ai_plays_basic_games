class Floor:

    def __init__(self, y, img):
        self.WIDTH = img.get_width()
        self.img = img
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        self.velX = 5

    def move(self):
        # have two floors that continuously alternate in position
        # once their end-points go pass x = 0
        self.x1 -= self.velX
        self.x2 -= self.velX

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw_floor(self, window):
        window.blit(self.img, (self.x1, self.y))
        window.blit(self.img, (self.x2, self.y))