import threading
import time
from pygame.locals import *
from Game import *
import graphic
import pygame
import datetime

game = Game()


pygame.init()
matrix =game.get_board() # Import the Game class from the Game module

game = Game('AC3','MCV','LCV')  # Instantiate the Game class
game.get_info()




def csp_calc():
    start = time.time()
    game.Back_track()
    end = time.time()
    print(game.counter, "\ntime: ", end - start)
csp_thread = threading.Thread(target=csp_calc)
csp_thread.start()



pygame.init()
matrix = game.get_board()
rows = len(matrix)
cols = len(matrix[0])
cell_size = 50
grid_width = cols * cell_size + (cols - 1) * 1
grid_height = rows * cell_size + (rows - 1) * 1
screen = pygame.display.set_mode((grid_width, grid_height))
pygame.display.set_caption('Neural Network Matrix')
screen.fill((100, 20, 20))
clock = pygame.time.Clock()
running = True
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    graphic.display_nn_matrix(game.get_board(), screen)
    pygame.display.flip()
    time.sleep(0.0001)
    clock.tick(1000000000)
pygame.quit()











def print_matrix(matrix):
    for row in matrix:
        for element in row:
            print(f"{element}\t", end="")
        print()