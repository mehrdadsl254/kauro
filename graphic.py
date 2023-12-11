import pygame


def display_nn_matrix(nn_matrix, screen):
    # Set up the grid parameters

    # Set up the screen

    # Define colors
    gray = (128, 128, 128)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Set up the font
    font = pygame.font.Font(None, 24)

    rows = len(nn_matrix)
    cols = len(nn_matrix[0])
    cell_size = 50.
    # Main game loop

    # Clear the screen

    # Draw the grid
    for row in range(rows):
        for col in range(cols):
            value = nn_matrix[row][col]
            cell_x = col * cell_size + 1 * col
            cell_y = row * cell_size + 1 * row
            # Draw the cell
            # Draw the value in the cell
            if isinstance(value, int):
                pygame.draw.rect(screen, WHITE, (cell_x, cell_y, cell_size, cell_size))
                pygame.draw.rect(screen, BLACK, (cell_x, cell_y, cell_size, cell_size), 2)
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=(cell_x + cell_size // 2, cell_y + cell_size // 2))
                screen.blit(text, text_rect)
            elif isinstance(value, str) and '\\' in value:
                pygame.draw.rect(screen, gray, (cell_x, cell_y, cell_size, cell_size))
                pygame.draw.rect(screen, BLACK, (cell_x, cell_y, cell_size, cell_size))
                parts = value.split('\\')
                text1 = font.render(parts[0], True, WHITE)
                text2 = font.render(parts[1], True, WHITE)
                text1_rect = text1.get_rect(center=(cell_x + cell_size // 4, cell_y + cell_size // 2 + cell_size // 4))
                text2_rect = text2.get_rect(
                    center=(cell_x + 3 * cell_size // 4, cell_y + cell_size // 2 - cell_size // 4))
                pygame.draw.line(screen, WHITE, (cell_x, cell_y), (cell_x + cell_size, cell_y + cell_size), 2)
                screen.blit(text1, text1_rect)
                screen.blit(text2, text2_rect)
            elif value == 'X':
                pygame.draw.rect(screen, gray, (cell_x, cell_y, cell_size, cell_size))
                pygame.draw.rect(screen, BLACK, (cell_x, cell_y, cell_size, cell_size), 2)
            else:
                pygame.draw.rect(screen, WHITE, (cell_x, cell_y, cell_size, cell_size))
                pygame.draw.rect(screen, BLACK, (cell_x, cell_y, cell_size, cell_size), 2)

                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=(cell_x + cell_size // 2, cell_y + cell_size // 2))
                screen.blit(text, text_rect)

        # Update the display