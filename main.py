import pygame
from sys import exit

pygame.init()

width = 960
height = 960
floorsCount = 5
hightDistance = height / (floorsCount + 1)
jumpGap = 192
defaultHeight = 64
speed = 3
gravityRed = 0
gravityBlue = 0
jumpSize = -17
gameName = 'Nap Hunters'
delayRespawn = 200

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(gameName)

clock = pygame.time.Clock()

wallSurface = pygame.image.load('graphics/levels/wall.png').convert_alpha()
wallSurface = pygame.transform.scale(wallSurface, (width, height))


tableSurface = pygame.image.load('graphics/levels/startTable.png').convert_alpha()
tableSurface = pygame.transform.scale(tableSurface, (jumpGap, defaultHeight - 20))
tableRect = tableSurface.get_rect(bottomleft = (0, height))

playerRedSurface = pygame.image.load('graphics/players/playerRed.png').convert_alpha()
playerRedSurface = pygame.transform.scale(playerRedSurface, (50, 64))
playerRedRect = playerRedSurface.get_rect(bottomleft = tableRect.topleft)

playerBlueSurface = pygame.image.load('graphics/players/playerBlue.png').convert_alpha()
playerBlueSurface = pygame.transform.scale(playerBlueSurface, (50, 64))
initialBluePosition = (tableRect.topleft[0] + 64, tableRect.topleft[1])
playerBlueRect = playerBlueSurface.get_rect(bottomleft = initialBluePosition)

floorSurface = pygame.image.load('graphics/levels/floor.png').convert_alpha()
floorSurface = pygame.transform.scale(floorSurface, (width - jumpGap, 64))
floors = []

for i in range(floorsCount):
    isEven = (i % 2 == 0)
    align = 'topright' if isEven else 'topleft'
    pos = (width, height - (i + 1) * hightDistance) if isEven else (0, height - (i + 1) * hightDistance)
    
    floorRect = floorSurface.get_rect(**{align: pos})
    floors.append((floorSurface, floorRect))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
        playerBlueRect.x += speed

    if keys[pygame.K_a]:
        playerBlueRect.x -= speed

    if keys[pygame.K_w] and playerBlueRect.bottom >= tableRect.top:
        gravityRed = jumpSize

    if keys[pygame.K_RIGHT]:
        playerRedRect.x += speed

    if keys[pygame.K_LEFT]:
        playerRedRect.x -= speed

    gravityRed += 1
    playerBlueRect.y += gravityRed

    if playerBlueRect.bottom > tableRect.top and playerBlueRect.left < tableRect.right:
        playerBlueRect.bottom = tableRect.top
        gravityRed = 0

    if playerBlueRect.bottom >= height + delayRespawn:
        playerBlueRect.bottomleft = initialBluePosition

    screen.blit(wallSurface, (0,0))
    screen.blit(tableSurface, tableRect)
    screen.blit(playerRedSurface, playerRedRect)
    screen.blit(playerBlueSurface, playerBlueRect)

    for surface, rect in floors:
        screen.blit(surface, rect)

    pygame.display.update()
    clock.tick(60)