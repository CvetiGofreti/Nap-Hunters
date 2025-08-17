import pygame
from screens.main_menu import MainMenu
from screens.level_builder import LevelBuilder
from screens.level_selector import LevelSelect
from screens.gameplay import GameScreen
from others.graphics_loader import Assets

def main():
    pygame.init()
    screenWidth = 960
    screenHeight = 960
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Nap Hunters")
    clock = pygame.time.Clock()
    fontMain = pygame.font.Font(None, 48)
    fontSmall = pygame.font.Font(None, 24)
    assets = Assets()
    gameScreen = GameScreen(fontMain, fontSmall, assets)
    currentScreen = MainMenu(fontMain, fontSmall, assets)

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
                    currentScreen = LevelBuilder(fontMain, fontSmall, assets)
                elif action == "mainMenu":
                    currentScreen = MainMenu(fontMain, fontSmall, assets)
                elif action == "levelSelect":
                    currentScreen = LevelSelect(fontMain, fontSmall, assets)
                elif isinstance(action, tuple) and action[0] == "playLevel":
                    levelPath = action[1]
                    gameScreen.load_level(levelPath)
                    currentScreen = gameScreen

        currentScreen.update(deltaTime)
        screen.blit(assets.wall, (0, 0))
        currentScreen.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()