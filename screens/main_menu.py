import pygame
import others.global_values

from others.text_input import TextInputBox

buttonHeight = 70
buttonWidth = 260
buttonSpacing = 20
defaultButtonSize = (0, 0, buttonWidth, buttonHeight)

class MainMenu:
    def __init__(self, fontMain, fontSmall, assets):
        self.fontMain = fontMain
        self.fontSmall = fontSmall
        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        self.levelBuilderButton = pygame.Rect(*defaultButtonSize)
        self.levelSelectButton = pygame.Rect(*defaultButtonSize)
        self.leaderboardButton = pygame.Rect(*defaultButtonSize)

        totalHeight = 3 * buttonHeight + 2 * buttonSpacing
        startX = (screenWidth - buttonWidth) // 2
        startY = (screenHeight - totalHeight) // 2

        self.levelSelectButton.topleft = (startX, startY)
        self.levelBuilderButton.topleft = (startX, startY + buttonHeight + buttonSpacing)
        self.leaderboardButton.topleft = (startX, startY + 2 * (buttonHeight + buttonSpacing))

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
            if self.leaderboardButton.collidepoint(event.pos):
                return "leaderboard"
        return None

    def update(self, dt):
        self.teamNameBox.update(dt)
        others.global_values.currentTeamName = self.teamNameBox.label.strip()

    def draw(self, screen):
        self.teamNameBox.draw(screen)

        buttonColor = pygame.Color("royalblue3")
        borderRadius = 12
        textColor = pygame.Color("white")

        pygame.draw.rect(screen, buttonColor, self.levelBuilderButton, border_radius = borderRadius)
        levelBuildLabel = self.fontMain.render("Build Level", True, textColor)
        screen.blit(levelBuildLabel, (self.levelBuilderButton.centerx - levelBuildLabel.get_width() // 2,
                            self.levelBuilderButton.centery - levelBuildLabel.get_height() // 2))
        
        pygame.draw.rect(screen, buttonColor, self.levelSelectButton, border_radius = borderRadius)
        levelSelectLabel = self.fontMain.render("Play", True, textColor)
        screen.blit(levelSelectLabel, (self.levelSelectButton.centerx - levelSelectLabel.get_width() // 2,
                            self.levelSelectButton.centery - levelSelectLabel.get_height() // 2))
        
        pygame.draw.rect(screen, buttonColor, self.leaderboardButton, border_radius = borderRadius)
        leaderboardLabel = self.fontMain.render("Leaderboard", True, textColor)
        screen.blit(leaderboardLabel, (self.leaderboardButton.centerx - leaderboardLabel.get_width() // 2,
                            self.leaderboardButton.centery - leaderboardLabel.get_height() // 2))