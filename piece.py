import copy
import math

import pygame

from block import Block
from settings import GRID_SIZE, GRID_WIDTH, GRID_TOP, DEBUG, MOVE_LEFT, MOVE_RIGHT, GRID_LEFT, GRID_RIGHT, GRID_BOTTOM
from custom_timer import CustomTimer
import random

class Piece:

    # how long the player has to move the piece before it gets
    TOUCHING_MOVE_TIME = 2

    SEQUENCE_H_TIME = 0.1
    FIRST_H_TIME = 0.25

    SRS_GENERAL = {
        (0, 1):[(-1, 0), (-1, -1), ( 0, 2), (-1, 2)],
        (1, 0):[(1, 0), (1, 1), (0, -2), (1, -2)],
        (1, 2):[(1, 0), (1,1), (0, -2), (1, -2)],
        (2, 1):[(-1, 0), (-1, -1), (0, 2), (-1, 2)],
        (2, 3):[(1, 0), (1, -1), (0, 2), (1, 2)],
        (3, 2):[(-1, 0), (-1, 1), (0, -2), (-1, -2)],
        (3, 0):[(-1, 0), (-1, 1), (0, -2), (-1, -2)],
        (0, 3):[(1, 0), (1, -1), (0, 2), (1, 2)]
    }

    SRS_I = {
        (0, 1): [(-2, 0), (1, 0), (-2, 1), (1, -2)],
        (1, 0): [(2, 0), (-1, 0), (2, -1), (-1, 2)],
        (1, 2): [(-1, 0), (2, 0), (-1, -2), (2, 1)],
        (2, 1): [(1, 0), (-2, 0), (1, 2), (-2, -1)],
        (2, 3): [(2, 0), (-1, 0), (2, -1), (-1, 2)],
        (3, 2): [(-2, 0), (1, 0), (-2, 1), (1, -2)],
        (3, 0): [(1, 0), (-2, 0), (1, 2), (-2, -1)],
        (0, 3): [(-1, 0), (2, 0), (-1, -2), (2, 1)]
    }

    def __init__(self, piece_map:list, piece_type:str, color):
        # index in list of rotation
        self.rotation_ind = 0

        self.piece_map = piece_map
        self.piece_type = piece_type
        self.color = color

        self.block_length = len(piece_map[0])

        self.started_moving_horizontally = False

        self.started_moving_horizontally_timer = CustomTimer(Piece.FIRST_H_TIME)
        self.moving_horizontally_timer = CustomTimer(Piece.SEQUENCE_H_TIME)

        self.SRS_SYSTEM = Piece.SRS_I if piece_type == "I" else Piece.SRS_GENERAL

        self.piece_edges = {
            "left":math.inf,
            "right":0,
            "top":math.inf,
            "bottom":0,
        }

        self.gen_start_conditions()

    def gen_start_conditions(self):
        # rect of rotation rectangle (outer shell of piece, used only for rotation)
        rotate_rect_width = self.block_length * GRID_SIZE
        # create rotate rectangle

        # start position of each piece
            # X: HALF OF GRID WIDTH (rounded to nearest GRID_SIZE) - HALF OF PIECE WIDTH (rounded to nearest GRID_SIZE)
            # Y: TOP OF PIECE - GRID_SIZE (IF THE TOP ROW IS ALL 0s)
        # round number a to the nearest number b
        def round_to_nearest(a, b):
            return b * round(a/b)

        start_pos = pygame.Vector2(round_to_nearest(GRID_WIDTH // 2, GRID_SIZE)
                                   - round_to_nearest((len(self.piece_map[0]) * GRID_SIZE) // 2, GRID_SIZE),
                                   (GRID_TOP - GRID_SIZE * (set(self.piece_map[0]) == {0})))

        self.rotate_rect = pygame.Rect(start_pos.x, start_pos.y, rotate_rect_width, rotate_rect_width)

        # generates rotations in order of Z presses
        self._rotations = self.generate_rotations(self.piece_map)

        # dictionary of all blocks
        self.blocks = {}

        # takes piece map and adds each letter of the map to a dictionary with an associated block piece
        for y, row in enumerate(self.piece_map):
            for x, letter in enumerate(row):
                if letter != 0:
                    self.blocks[letter] = Block(x * GRID_SIZE + start_pos.x,
                                                y * GRID_SIZE + start_pos.y,
                                                GRID_SIZE, GRID_SIZE,
                                                self.color)

        self.calculate_piece_edges()

    def move_horizontally(self, placed_blocks:list[Block]):
        # gets all the pressed keys
        keys = pygame.key.get_pressed()

        self.calculate_piece_edges()

        def move_in_dir(direction:str):
            for b in self.blocks.values():
                b.move_to_side(direction)

            self.rotate_rect.x -= GRID_SIZE if direction == "left" else -GRID_SIZE

        def allow_move_directions():
            move_left_allowed = True
            move_right_allowed = True

            # Test moving left
            move_in_dir("left")
            for b in self.blocks.values():
                for p in placed_blocks:
                    if b.rect.colliderect(p.rect):
                        move_left_allowed = False
                        break
                if not move_left_allowed:
                    break
            move_in_dir("right")  # Revert to the original position

            # Test moving right
            move_in_dir("right")
            for b in self.blocks.values():
                for p in placed_blocks:
                    if b.rect.colliderect(p.rect):
                        move_right_allowed = False
                        break
                if not move_right_allowed:
                    break
            move_in_dir("left")  # Revert to the original position

            return move_left_allowed, move_right_allowed

        if not self.started_moving_horizontally:
            can_move_left, can_move_right = allow_move_directions()
            if keys[MOVE_LEFT] and self.piece_edges["left"] > GRID_LEFT and can_move_left:
                move_in_dir('left')
                self.started_moving_horizontally = True

            elif keys[MOVE_RIGHT] and self.piece_edges["right"] < GRID_RIGHT and can_move_right:
                move_in_dir('right')
                self.started_moving_horizontally = True

        time_up = self.started_moving_horizontally_timer.check_for_time_up()

        if self.started_moving_horizontally and time_up:
            if self.moving_horizontally_timer.check_for_time_up():
                can_move_left, can_move_right = allow_move_directions()
                if keys[MOVE_LEFT] and self.piece_edges["left"] > GRID_LEFT and can_move_left:
                    move_in_dir('left')

                elif keys[MOVE_RIGHT] and self.piece_edges["right"] < GRID_RIGHT and can_move_right:
                    move_in_dir('right')
                self.moving_horizontally_timer.reset_timer()

        # player has stopped moving horizontally
        if not keys[MOVE_LEFT] and not keys[MOVE_RIGHT]:
            self.started_moving_horizontally = False
            self.started_moving_horizontally_timer.reset_timer()
            self.moving_horizontally_timer.reset_timer()

        self.calculate_piece_edges()

    def move_down(self, placed_blocks:list[Block]):
        self.calculate_piece_edges()

        touching_block = False

        for p in placed_blocks:
            for b in self.blocks.values():
                b.rect.y += 3
                if p.rect.colliderect(b.rect) and p.rect.top == b.rect.bottom - 3:
                    b.rect.y -= 3
                    touching_block = True
                    break

                b.rect.y -= 3

            if touching_block: break

        if self.piece_edges["bottom"] != GRID_BOTTOM and not touching_block:
            # move rotate rect down
            self.rotate_rect.y += GRID_SIZE
            # move all the blocks down
            for b in self.blocks.values():
                b.move_down()
            self.calculate_piece_edges()
        else:
            return True, list(self.blocks.values())

        return False, []

    def rotate(self, direction:str, placed_blocks:list[Block]):
        previous = copy.copy(self.rotation_ind)
        match direction:
            case "left":
                # increment rotation index by 1 (move to next rotation)
                self.rotation_ind -= 1
                # if rotation index equals length of negative
                if self.rotation_ind == -1: self.rotation_ind = len(self._rotations) - 1
            case "right":
                # increment rotation index by 1 (move to next rotation)
                self.rotation_ind += 1
                # if rotation index equals length of rotations list, then go back to starting rotation index (full rotation complete)
                if self.rotation_ind == len(self._rotations): self.rotation_ind = 0

        # go through all blocks in current rotation
        for y, row in enumerate(self._rotations[self.rotation_ind]):
            for x, item in enumerate(row):
                # if item is not a 0 (it is a letter which maps to a piece)
                if item != 0:
                    # rotating piece = moving around the blocks to it shifts by 90˚
                    # use the next rotation index to rotate the piece
                    self.blocks[item].rect.topleft = pygame.Vector2(self.rotate_rect.topleft) + pygame.Vector2(x * GRID_SIZE, y * GRID_SIZE)

        # TODO: Handle the SRS system here
        def check_invalid_rotation():
            # determine where rotated piece bounds are
            self.calculate_piece_edges()

            collision_found = False

            for b in self.blocks.values():
                for p in placed_blocks:
                    if b.rect.colliderect(p.rect):
                        collision_found = True
                        break

                if collision_found: break

            return collision_found or self.piece_edges["left"] < GRID_LEFT or \
                    self.piece_edges["right"] > GRID_RIGHT or \
                    self.piece_edges["bottom"] > GRID_BOTTOM or \
                    self.piece_edges["top"] < GRID_TOP

        if check_invalid_rotation():
            SRS_key = (previous, self.rotation_ind)
            possible_moves = self.SRS_SYSTEM[SRS_key]
            
            valid_kick_found = False

            for pos in possible_moves:
                for b in self.blocks.values():
                    b.move_piece(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE)

                if check_invalid_rotation():
                    for b in self.blocks.values():
                        b.move_piece(-pos[0] * GRID_SIZE, -pos[1] * GRID_SIZE)
                else:
                    self.rotate_rect.topleft += pygame.Vector2(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE)
                    valid_kick_found = True
                    break
                    
            if not valid_kick_found:
                if previous > self.rotation_ind:
                    self.rotate('left', placed_blocks)
                else:
                    self.rotate('right', placed_blocks)

    def calculate_piece_edges(self):
        self.piece_edges = {
            "left":math.inf,
            "right":0,
            "top":math.inf,
            "bottom":0,
        }

        for b in self.blocks.values():
            if b.rect.left < self.piece_edges["left"]:
                self.piece_edges["left"] = b.rect.left
            if b.rect.top < self.piece_edges["top"]:
                self.piece_edges["top"] = b.rect.top

            if b.rect.right > self.piece_edges["right"]:
                self.piece_edges["right"] = b.rect.right
            if b.rect.bottom > self.piece_edges["bottom"]:
                self.piece_edges["bottom"] = b.rect.bottom

    def draw(self, surface:pygame.Surface):
        # show rotation box
        if DEBUG:
            pygame.draw.rect(surface, (0, 255, 255), self.rotate_rect)

        # draw all blocks on grid
        for b in self.blocks.values():
            b.draw(surface)

    def generate_rotations(self, piece_map:list) -> list:
        rotations = [piece_map]

        # rotate right
        rot_right = [[0 for _ in range(self.block_length)] for __ in range(self.block_length)]
        for y in range(len(piece_map)):
            for x in range(len(piece_map[0])):
                rot_right[y][x] = piece_map[x][y]
            rot_right[y] = rot_right[y][::-1]

        rotations.append(rot_right)

        def double_reverse(map):
            rev_map = list(map)
            for i in range(len(rev_map)):
                rev_map[i] = rev_map[i][::-1]
            rev_map = rev_map[::-1]

            return rev_map

        rotations.append(double_reverse(piece_map))
        rotations.append(double_reverse(rot_right))

        return rotations

    @staticmethod
    def generate_piece(piece_type = None):
        piece_options = [
            {"piece_type": "I", "piece_map": [[0, 0, 0, 0], ['A', 'B', 'C', 'D'], [0, 0, 0, 0], [0, 0, 0, 0]],
             "color": "cyan"},
            {"piece_type": "J", "piece_map": [[0, 0, 'A'], ['B', 'C', 'D'], [0, 0, 0]], "color": "blue"},
            {"piece_type": "L", "piece_map": [["A", 0, 0], ['B', 'C', 'D'], [0, 0, 0]], "color": "orange"},
            {"piece_type": "O", "piece_map": [['A', 'B'], ['C', 'D']], "color": "yellow"},
            {"piece_type": "S", "piece_map": [[0, 'A', 'B'], ['C', 'D', 0], [0, 0, 0]], "color": "green"},
            {"piece_type": "Z", "piece_map": [['A', 'B', 0], [0, 'C', 'D'], [0, 0, 0]], "color": "red"},
            {"piece_type": "T", "piece_map": [[0, 'A', 0], ['B', 'C', 'D'], [0, 0, 0]], "color": "purple"},
        ]

        piece_choice = None

        if piece_type is None:
            piece_choice = random.choice(piece_options)
        else:
            for p in piece_options:
                if p["piece_type"] == piece_type:
                    piece_choice = p
                    break

        return Piece(piece_choice["piece_map"], piece_choice["piece_type"], piece_choice["color"])