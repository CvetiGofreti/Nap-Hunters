import pygame

from others.text_input import TextInputBox

defaultButtonSize = (0, 0, 260, 70)

class MainMenu:
    def __init__(self, fontMain, fontSmall, assets):
        self.fontMain = fontMain
        self.fontSmall = fontSmall
        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        self.levelBuilderButton = pygame.Rect(*defaultButtonSize)
        self.levelSelectButton = pygame.Rect(*defaultButtonSize)

        self.levelBuilderButton.center = (screenWidth // 2, screenHeight // 2 - 50)
        self.levelSelectButton.center = (screenWidth // 2, screenHeight // 2 + 50)

        inputWidth = 260
        inputHeight = 50
        inputTeamNameX = screenWidth // 2 - inputWidth // 2
        inputTeamNameY = 20
        self.teamNameBox = TextInputBox(inputTeamNameX, inputTeamNameY, inputWidth, inputHeight, fontSmall, "Enter team name")

    def handle_event(self, event):
        self.teamNameBox.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.levelBuilderButton.collidepoint(event.pos):
                return "levelBuilder"
            if self.levelSelectButton.collidepoint(event.pos):
                return "levelSelect"
        return None

    def update(self, dt):
        self.teamNameBox.update(dt)

    def draw(self, screen):
        self.teamNameBox.draw(screen)

        levelBuilderButtonColor = pygame.Color("royalblue3")
        pygame.draw.rect(screen, levelBuilderButtonColor, self.levelBuilderButton, border_radius=12)
        levelBuildlabel = self.fontMain.render("Build Level", True, pygame.Color("white"))
        screen.blit(levelBuildlabel, (self.levelBuilderButton.centerx - levelBuildlabel.get_width() // 2,
                            self.levelBuilderButton.centery - levelBuildlabel.get_height() // 2))
        
        levelSelectButtonColor = pygame.Color("royalblue3")
        pygame.draw.rect(screen, levelSelectButtonColor, self.levelSelectButton, border_radius=12)
        levelSelectlabel = self.fontMain.render("Select Level", True, pygame.Color("white"))
        screen.blit(levelSelectlabel, (self.levelSelectButton.centerx - levelSelectlabel.get_width() // 2,
                            self.levelSelectButton.centery - levelSelectlabel.get_height() // 2))