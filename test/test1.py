import pygame
import time
from math import floor

pygame.init()
pygame.font.init()

font = pygame.font.SysFont('Comic Sans MS', 30)
WINDOW = pygame.display.set_mode((1280, 720))
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 120

def main():
    run = True
    clock = pygame.time.Clock()
    
    class Board:
        def __init__(self):
            self.board = [[0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0]] #5*5
            
        def draw_cubes(self, win):
            win.fill((255, 255, 255))
            for row in range(5):
                for col in range(5):
                    if self.board[col][row] == 0:
                        pygame.draw.rect(win, GREEN, (row*100, col*100, 100, 100))
                    if self.board[col][row] == 1:
                        pygame.draw.rect(win, RED, (row*100, col*100, 100, 100))
                    if self.board[col][row] == 2:
                        pygame.draw.rect(win, BLUE, (row*100, col*100, 100, 100))
                  
    def show_fps():
        fpst = floor(clock.get_fps())
        fps = font.render(f"{fpst}", 1, pygame.Color("Coral"))
        return fps
                   
    board = Board()
    check = 0
    while run:
        fps = show_fps()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    

        board.draw_cubes(WINDOW)
        WINDOW.blit(fps, (0, 100*(5-1)+100/2)) #gridsize - 1
        clock.tick(FPS)
        pygame.display.update()
        if check == 0:
            check = 1
            board.board[0][0] = 2
        elif check == 1:
            check = 0
            board.board[0][0] = 1

    pygame.quit()
    
main()