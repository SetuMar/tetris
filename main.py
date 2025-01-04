import pygame
import sys
import time

pygame.init()

import ui
import util
from piece import Piece
from settings import *
from block import Block

display = pygame.display.set_mode((500, 550))
width, height = (GRID_WIDTH - GRID_PADDING, GRID_HEIGHT - GRID_PADDING)

clock = pygame.time.Clock()

grid = util.get_grid(width, height, GRID_COLOR)

current_piece = Piece.generate_piece()

last_time = time.time()
current_time = time.time()

placed_blocks = []

placed = False

held_this_round = False
held_piece = None
held_piece_display = ui.PieceDisplay(300, 60, 4.2 * GRID_SIZE, 4.2 * GRID_SIZE, 'white', "HELD")

next_piece = Piece.generate_piece()
next_piece_display = ui.PieceDisplay(300, 200, 4.2 * GRID_SIZE, 4.2 * GRID_SIZE, 'white', "NEXT")

drop_time = TIME_BETWEEN_DROPS
just_let_go_of_drop_key = False

hard_drop_completed = False

pause_value = 1

while True:
    hard_drop_completed = False
    display.fill('BLACK')
    current_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            pause_value += event.key == PAUSE
            pause_value = pause_value % 2

            if pause_value > 0:
                if event.key == ROTATE_RIGHT:
                    current_piece.rotate('right', placed_blocks)
                elif event.key == ROTATE_LEFT:
                    current_piece.rotate('left', placed_blocks)

                if event.key == HOLD_KEY and not held_this_round:
                    if held_piece is None:
                        held_piece = Piece.generate_piece(current_piece.piece_type)
                        current_piece = next_piece
                        next_piece = Piece.generate_piece()
                    else:
                        current_piece, held_piece = held_piece, current_piece

                    current_time = time.time()
                    last_time = time.time()

                    held_this_round = True

                if event.key == HARD_DROP:
                    hard_drop_completed = False
                    while not hard_drop_completed:
                        move_to_next_piece, new_blocks_to_add = current_piece.move_down(placed_blocks)
                        if len(new_blocks_to_add) > 0: placed_blocks.extend(new_blocks_to_add)
                        last_time = current_time

                        if move_to_next_piece:
                            placed_blocks = util.check_cleared_row(placed_blocks)
                            current_piece = next_piece
                            next_piece = Piece.generate_piece()
                            held_this_round = False
                            hard_drop_completed = True

    if pause_value > 0:
        current_piece.move_horizontally(placed_blocks)

        held_keys = pygame.key.get_pressed()

        if held_keys[SOFT_DROP]:
            drop_time = SOFT_DROP_TIME
        else:
            drop_time = TIME_BETWEEN_DROPS

        if (current_time - last_time > drop_time) and not placed:
            move_to_next_piece, new_blocks_to_add = current_piece.move_down(placed_blocks)
            if len(new_blocks_to_add) > 0: placed_blocks.extend(new_blocks_to_add)
            last_time = current_time

            if move_to_next_piece:
                placed_blocks = util.check_cleared_row(placed_blocks)
                current_piece = next_piece
                next_piece = Piece.generate_piece()
                held_this_round = False

    current_piece.draw(display)

    if len(placed_blocks) > 0:
        for block in placed_blocks:
            block.draw(display)

    held_piece_display.draw(display)
    next_piece_display.draw(display)

    if held_piece is not None:
        held_piece_display.new_hold(held_piece)

    if next_piece is not None:
        held_piece_display.new_hold(next_piece)

    display.blit(grid, (GRID_PADDING / 2, GRID_PADDING / 2))

    pygame.display.update()
    clock.tick(60)