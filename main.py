import pygame
from sys import exit

pygame.init()

width = 960
height = 540
gameName = 'Nap Hunters'

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(gameName)

clock = pygame.time.Clock()

surface = pygame.Surface((width, height))
surface.fill('Red')

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(surface, (0,0))
    pygame.display.update()
    clock.tick(60)