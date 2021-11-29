import pygame
import time
from math import floor
from constants import GREEN, RED, BLUE, FPS
pygame.init()
pygame.font.init()

font = pygame.font.SysFont('Comic Sans MS', 30)
WINDOW = pygame.display.set_mode((1280, 720))

def main():
    run = True
    clock = pygame.time.Clock()
             
    def show_fps():
        fpst = floor(clock.get_fps())
        fps = font.render(f"{fpst}", 1, pygame.Color("Coral"))
        return fps
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    run = False
                
        WINDOW.fill((255, 255, 255))
        WINDOW.blit(show_fps(), (0, 0)) #100*(5-1)+100/2)) #gridsize - 1
        clock.tick(FPS)
    
        pygame.display.update()
        
    pygame.quit()
    
main()