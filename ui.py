import pygame

from piece import Piece
from settings import GRID_SIZE
from settings import FONT, FONT_SIZE

class Text:
    def __init__(self, pos:pygame.Vector2, text, color):
        self._color = color
        self._font = FONT.render(text, True, color)
        self._pos = pos

    def set_text(self, new_text:str):
        self._font = FONT.render(new_text, True, self._color)

    def draw(self, surface:pygame.Surface):
        surface.blit(self._font, self._pos)

class PieceDisplay:
    def __init__(self, pos:pygame.Vector2, w, h, color, description):
        self._border = self.generate_border(w, h, color)
        self.rect = self._border.get_rect(x=pos.x, y=pos.y)
        self.held_img = None
        self.description = description
        self.text = FONT.render(description, True, color)
        self.piece_offset = pygame.Vector2(0, 0)

    def new_hold(self, to_hold:Piece):
        self.held_img = pygame.Surface((self.rect.w, self.rect.h))
        # go through all rows
        for y, row in enumerate(to_hold.piece_map):
            print(y, row)
            # go through each block in the row
            for x, block in enumerate(row):
                if block != 0:
                    block_img = pygame.Surface((GRID_SIZE, GRID_SIZE))
                    block_img.fill(to_hold.color)
                    self.held_img.blit(block_img, (x * GRID_SIZE, y * GRID_SIZE))

        if len(to_hold.piece_map) == 4:
            self.piece_offset = pygame.Vector2(0, GRID_SIZE/2)
        elif len(to_hold.piece_map) == 3:
            self.piece_offset = pygame.Vector2(GRID_SIZE / 1.5, GRID_SIZE / 1.25)
        else:
            self.piece_offset = pygame.Vector2(GRID_SIZE, GRID_SIZE)

    def draw(self, surface):
        surface.blit(self.text, pygame.Vector2(self.rect.x + FONT_SIZE * len(self.description) / 2 - 13, self.rect.y - FONT_SIZE))
        if self.held_img is not None: surface.blit(self.held_img, pygame.Vector2(self.rect.topleft) + self.piece_offset)
        surface.blit(self._border, self.rect.topleft)

    @staticmethod
    def generate_border(w, h, color):
        border_surf = pygame.Surface((w + 2, h + 2), pygame.SRCALPHA)

        pygame.draw.line(border_surf, color, pygame.Vector2(1, 1), pygame.Vector2(w - 1, 1))
        pygame.draw.line(border_surf, color, pygame.Vector2(1, h - 1), pygame.Vector2(w - 1, h - 1))

        pygame.draw.line(border_surf, color, pygame.Vector2(1, 1), pygame.Vector2(1, h - 1))
        pygame.draw.line(border_surf, color, pygame.Vector2(w - 1, 1), pygame.Vector2(w - 1, h - 1))

        return border_surf