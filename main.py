import pygame
from screens.main_menu import MainMenu
from screens.level_builder import LevelBuilder

def main():
    pygame.init()
    screenWidth = 960
    screenHeight = 960
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Nap Hunters")
    clock = pygame.time.Clock()

    fontMain = pygame.font.Font(None, 48)
    fontSmall = pygame.font.Font(None, 24)

    currentScreen = MainMenu(fontMain, fontSmall)

    backgroundImage = pygame.image.load("graphics/levels/wall.png").convert()
    backgroundImage = pygame.transform.scale(backgroundImage, screen.get_size())

    running = True
    while running:
        deltaTime = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                action = currentScreen.handle_event(event)
                if action == "quit":
                    running = False
                elif action == "levelBuilder":
                    currentScreen = LevelBuilder(fontMain, fontSmall)
                elif action == "mainMenu":
                    currentScreen = MainMenu(fontMain, fontSmall)

        currentScreen.update(deltaTime)
        screen.blit(backgroundImage, (0, 0))
        currentScreen.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()