import pygame

from piece import Piece
from settings import GRID_SIZE
from settings import FONT, FONT_SIZE


class PieceDisplay:
    def __init__(self, x, y, w, h, color, description):
        self.border = self.generate_border(w, h, color)
        self.rect = self.border.get_rect(x=x, y=y)
        self.held_img = None
        self.description = description
        self.text = FONT.render(description, True, color)

    def new_hold(self, to_hold:Piece):
        self.held_img = pygame.Surface((self.rect.w, self.rect.h))
        for y, row in enumerate(to_hold.piece_map):
            for x, block in enumerate(row):
                if block != 0:
                    block_img = pygame.Surface((GRID_SIZE, GRID_SIZE))
                    block_img.fill(to_hold.color)
                    self.held_img.blit(block_img, pygame.Vector2(x * GRID_SIZE, y * GRID_SIZE) +
                                       pygame.Vector2((self.rect.w - (to_hold.piece_edges["right"] - to_hold.piece_edges["left"])) / 2,
                                                      (self.rect.h - (to_hold.piece_edges["bottom"] - to_hold.piece_edges["top"])) / 2 -
                                                      GRID_SIZE * int(to_hold.piece_type == "I")))

    def draw(self, surface):
        surface.blit(self.text, pygame.Vector2(self.rect.x + FONT_SIZE * len(self.description) / 2 - 13, self.rect.y - FONT_SIZE))
        if self.held_img is not None: surface.blit(self.held_img, self.rect.topleft)
        surface.blit(self.border, self.rect.topleft)

    @staticmethod
    def generate_border(w, h, color):
        border_surf = pygame.Surface((w + 2, h + 2), pygame.SRCALPHA)

        pygame.draw.line(border_surf, color, pygame.Vector2(1, 1), pygame.Vector2(w - 1, 1))
        pygame.draw.line(border_surf, color, pygame.Vector2(1, h - 1), pygame.Vector2(w - 1, h - 1))

        pygame.draw.line(border_surf, color, pygame.Vector2(1, 1), pygame.Vector2(1, h - 1))
        pygame.draw.line(border_surf, color, pygame.Vector2(w - 1, 1), pygame.Vector2(w - 1, h - 1))

        return border_surf

class Text:
    def __init__(self, pos:pygame.Vector2, text, color):
        self._color = color
        self._font = FONT.render(text, True, color)
        self._pos = pos

    def set_text(self, new_text:str):
        self._font = FONT.render(new_text, True, self._color)

    def draw(self, surface:pygame.Surface):
        surface.blit(self._font, self._pos)