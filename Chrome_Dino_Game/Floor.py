class Floor:
    """
    Draws and animates the floor which the cacti spawn on
    and the dino runs along
    """
    def __init__(self, img, y):
        self.img = img
        self.floor_width = self.img.get_width()
        self.x1 = 0
        self.x2 = self.img.get_width()
        self.y = y
        self.velX = 8

    def move(self):
        self.x1 -= self.velX
        self.x2 -= self.velX

        if self.x1 + self.floor_width < 0:
            self.x1 = self.x2 + self.floor_width

        if self.x2 + self.floor_width < 0:
            self.x2 = self.x1 + self.floor_width

    def draw(self, window):
        window.blit(self.img, (self.x1, self.y))
        window.blit(self.img, (self.x2, self.y))