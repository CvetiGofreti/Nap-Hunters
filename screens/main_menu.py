import pygame
import others.global_values
from others.button import Button
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
        self.nextScreen = None

        totalHeight = 3 * buttonHeight + 2 * buttonSpacing
        startX = (screenWidth - buttonWidth) // 2
        startY = (screenHeight - totalHeight) // 2

        self.levelSelectButton = Button(
            pos = (startX, startY),
            size = (buttonWidth, buttonHeight),
            label = "Play",
            onClick = lambda: self._set_next("levelSelect"),
            font = fontMain
        )

        self.levelBuilderButton = Button(
            pos = (startX, startY + buttonHeight + buttonSpacing),
            size = (buttonWidth, buttonHeight),
            label = "Build Level",
            onClick = lambda: self._set_next("levelBuilder"),
            font = fontMain
        )

        self.leaderboardButton = Button(
            pos = (startX, startY + 2 * (buttonHeight + buttonSpacing)),
            size = (buttonWidth, buttonHeight),
            label = "Leaderboard",
            onClick = lambda: self._set_next("leaderboard"),
            font = fontMain
        )

        inputWidth = 260
        inputHeight = 50
        inputTeamNameX = screenWidth // 2 - inputWidth // 2
        inputTeamNameY = 20
        self.teamNameBox = TextInputBox(inputTeamNameX, inputTeamNameY, inputWidth, inputHeight, fontSmall, "Enter team name")

    def _set_next(self, screenName):
        self.nextScreen = screenName

    def handle_event(self, event):
        self.teamNameBox.handle_event(event)
        self.nextScreen = None

        self.levelSelectButton.handle_event(event)
        self.levelBuilderButton.handle_event(event)
        self.leaderboardButton.handle_event(event)

        return self.nextScreen

    def update(self, dt):
        self.teamNameBox.update(dt)
        others.global_values.currentTeamName = self.teamNameBox.label.strip()

    def draw(self, screen):
        self.teamNameBox.draw(screen)

        self.levelSelectButton.draw(screen)
        self.levelBuilderButton.draw(screen)
        self.leaderboardButton.draw(screen)