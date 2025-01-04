import pygame
from settings import *

class Block:
    def __init__(self, x, y, width, height, color):
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

    def move_down(self):
        self.rect.y += GRID_SIZE

    def move_piece(self, x_amt, y_amt):
        self.rect.x += x_amt
        self.rect.y += y_amt

    def move_to_side(self, direction:str):
        match direction:
            case "left":
                self.rect.x -= GRID_SIZE
            case "right":
                self.rect.x += GRID_SIZE

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)