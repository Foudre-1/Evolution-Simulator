import pygame
import time
import numpy as np
import random
from math import floor #libraries imports

from test.constants import FPS, GREY1, GREY2, GREEN
from test.classes import Grid #files imports
pygame.init()
pygame.font.init() #modules initialisations

def main():
    WINDOW = pygame.display.set_mode() #create the window
    width = pygame.display.get_window_size()[0] #get width of the window
    height = pygame.display.get_window_size()[1] #get height of the window
    screen = pygame.Surface((width, height)) #create a surface on which every object will be displayed
    font = pygame.font.SysFont('Comic Sans MS', 25) #set the font
    print(font.size("120")) #120, 68
    font_size_x, font_size_y = font.size(f"{FPS}")
    
    grid = Grid(50) #initialise the main grid #test = 325
    print(grid.get()) #print the grid in its list form
    
    clock = pygame.time.Clock() #for the fps counter
    def show_fps():
        fpst = str(floor(clock.get_fps()))
        fps = font.render(fpst, 1, pygame.Color("Coral"))
        return fps
    
    WINDOW.fill(GREY2)
    run = True #condition to run the game loop
    grid.create_cell("blue")
    current_fps = 1
    frame = 1
    while run:
        #WINDOW.fill(GREY2)
        for event in pygame.event.get(): #key press check
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("K_ESCAPE pressed")
                    run = False
                if event.key == pygame.K_a:
                    print("K_a pressed")
                    grid.set(0, -1, -1)
                if event.key == pygame.K_z:
                    print("K_z pressed")
                    for column in range(0, grid.get_rows_columns()[1], 2):
                        for row in range(0, grid.get_rows_columns()[0], 2):
                            grid.set(column, row, -1)
                if event.key == pygame.K_e:
                    print("K_e pressed")
                    for column in range(0, grid.get_rows_columns()[1]):
                        for row in range(0, grid.get_rows_columns()[0]):
                            grid.set(column, row, 0)
                if event.key == pygame.K_r:
                    print("K_r pressed")
                    for i in range(1):
                        grid.create_cell("red")
                    print(grid.get_cell_list())
                    grid.update_cell()
                    grid.get()
                if event.key == pygame.K_RIGHT:
                    print("K_RIGHT pressed")
                    grid.old_move_cell("right")
                    grid.update_cell()  
                if event.key == pygame.K_LEFT:
                    print("K_LEFT pressed")
                    grid.old_move_cell("left")
                    grid.update_cell()
                if event.key == pygame.K_UP:
                    print("K_UP pressed")
                    grid.old_move_cell("up")
                    grid.update_cell()
                if event.key == pygame.K_DOWN:
                    print("K_DOWN pressed")
                    grid.old_move_cell("down")
                    grid.update_cell()
                if event.key == pygame.K_t:
                    print("K_t pressed")
                    print(grid.get())
                if event.key == pygame.K_c:
                    print("K_c pressed")
                    frame = frame - FPS//20
                    if frame <= 0:
                        frame = 1
                    print(frame)
                if event.key == pygame.K_x:
                    print("K_x pressed")
                    frame = 1
                    print(frame)
                if event.key == pygame.K_w:
                    print("K_w pressed")
                    frame = frame + FPS//20
                    if frame >= 240:
                        frame = 240
                    print(frame)
                if event.key == pygame.K_n:
                    print("K_n pressed")
                    grid.reverse_cell_list()
        
        if current_fps > FPS:
            current_fps = 1

        if current_fps in [i for i in range(1, FPS+1, frame)]:
            #WINDOW.fill(GREY2)
            grid.move_cell()
            grid.update_cell()
            
        screen.blit(grid.draw_cells(WINDOW), (0, 0)) #attach the grid to the screen
        
        pygame.draw.rect(screen, GREY1, (0, 0, font_size_x, font_size_y))
        pygame.draw.rect(screen, GREEN, (0, 0, font_size_x, font_size_y), width=5)
        screen.blit(show_fps(), (0, 0)) #attach the fps counter to the screen
        WINDOW.blit(screen, (0, 0)) #attach the screen to the main gaim window
        
        current_fps = current_fps + 1
        clock.tick(FPS) #update the fps counter
        pygame.display.update() #update everything (grid, fps, etc...)
    pygame.quit() #leave the program
    
main() #main function call