import pygame, os, json
from others.button import Button
import others.global_values

levelbuttonHeight = 56
levelbuttonPadding = 20
levelbuttonVerticalPadding = 10
levelListStartPos = 100

class LevelSelect:
    def __init__(self, fontMain, fontSmall, assets):
        self.fontMain = fontMain
        self.fontSmall = fontSmall
        self.assets = assets
        self.levelButtons = []
        self.nextScreen = None
        self._scan_levels()

    def _scan_levels(self):
        self.levelButtons.clear()
        os.makedirs("levels", exist_ok=True)
        filePaths = sorted([file for file in os.listdir("levels") if file.endswith(".json")])
        y = levelListStartPos
        passedLevels = self._load_passed_levels()

        for filePath in filePaths:
            fullPath = os.path.join("levels", filePath)
            name = filePath
            try:
                with open(fullPath, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    name = data.get("name", filePath)
            except Exception as exeption:
                print(f"Failed to load {fullPath}: {exeption}")
            rect = pygame.Rect(levelbuttonPadding, y, pygame.display.get_surface().get_width() - 2 * levelbuttonPadding, levelbuttonHeight)

            wasPassed = name in passedLevels
            button = Button(
                pos = (rect.x, rect.y),
                size = (rect.width, rect.height),
                label = name,
                onClick = lambda path = fullPath: self._set_next(path),
                font = self.fontSmall,
                showCheck = wasPassed,
                checkImage = self.assets.passedLevelImage
            )
            self.levelButtons.append(button)
            y += levelbuttonHeight + levelbuttonVerticalPadding

    def _load_passed_levels(self):
        teamName = others.global_values.currentTeamName
        try:
            with open("history.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                return set(data.get("teams", {}).get(teamName, {}).get("completed_levels", {}).keys())
        except Exception as e:
            print(f"Could not read history.json: {e}")
            return set()

    def _set_next(self, levelPath):
        self.nextScreen = ("playLevel", levelPath)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "mainMenu"

        self.nextScreen = None
        for button in self.levelButtons:
            button.handle_event(event)
        return self.nextScreen

    def update(self, dt):
        pass

    def draw(self, screen):
        screenWidth = screen.get_width()
        title = self.fontMain.render("Select Level", True, pygame.Color("royalblue3"))
        screen.blit(title, ((screenWidth - title.get_width()) // 2, levelListStartPos - title.get_height() - 10))

        for button in self.levelButtons:
            button.draw(screen)
