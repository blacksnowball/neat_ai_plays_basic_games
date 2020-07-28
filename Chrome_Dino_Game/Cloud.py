class Cloud:
    def __init__(self, img, x, y, APP_WIDTH):
        self.x = x
        self.y = y
        self.img = img
        self.img_width = img.get_width()
        self.reset_point = APP_WIDTH
        self.velX = 5

    def move(self):
        self.x -= self.velX
        if self.x + self.img_width < 0:
            self.x = self.reset_point + self.img_width

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))