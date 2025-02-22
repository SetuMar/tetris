import pygame.draw

from settings import *

def get_grid(width, height, color):
    grid_surface = pygame.Surface((width + 1, height + 1), pygame.SRCALPHA, 32)

    for y in range(GRID_SIZE, height, GRID_SIZE):
        pygame.draw.line(grid_surface, color, (0, y), (width, y))

    pygame.draw.line(grid_surface, color, (0, 0), (width, 0))
    pygame.draw.line(grid_surface, color, (0, y), (width, y))

    for x in range(0, width, GRID_SIZE):
        pygame.draw.line(grid_surface, color, (x, 0), (x, height - GRID_SIZE))

    pygame.draw.line(grid_surface, color, (x + GRID_SIZE, 0), (x + GRID_SIZE, height - GRID_SIZE))

    grid_surface = grid_surface.convert_alpha()

    return grid_surface

def check_cleared_row(placed_blocks, level, score, total_cleared_lines):
    placed_rows = {}
    for b in placed_blocks:
        placed_rows[b.rect.y] = placed_rows.get(b.rect.y, []) + [b]

    removed_row_values = set()

    blocks_to_remove = []
    for r, l in placed_rows.items():
        if len(l) == NUM_X_GRIDS:
            for inner in l:
                blocks_to_remove.append(inner)
                removed_row_values.add(r)

    for block in blocks_to_remove:
        placed_blocks.remove(block)

    print(sorted(removed_row_values))

    for val in sorted(removed_row_values):
        for p in placed_blocks:
            if p.rect.y <= val:
                p.rect.y += GRID_SIZE

    # total_cleared_lines += len(removed_row_values)

    # Update level only when a multiple of 10 lines are cleared
    # if total_cleared_lines % 10 == 0 and total_cleared_lines > 0:
    #     level += 1

    # Update score based on the number of rows cleared
    # if len(removed_row_values) == 1:
    #     score += level * 40
    # elif len(removed_row_values) == 2:
    #     score += level * 100
    # elif len(removed_row_values) == 3:
    #     score += level * 300
    # elif len(removed_row_values) == 4:
    #     score += level * 1200

    return placed_blocks, level, score, total_cleared_lines
