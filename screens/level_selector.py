import pygame, os, json

levelbuttonHeight = 56
levelbuttonPadding = 20
levelbuttonVerticalPadding = 10
levelListStartPos = 100

class LevelSelect:
    def __init__(self, fontMain, fontSmall, assets):
        self.fontMain = fontMain
        self.fontSmall = fontSmall
        self.levels = []
        self._scan_levels()

    def _scan_levels(self):
        self.levels.clear()
        os.makedirs("levels", exist_ok=True)
        filePaths = [file for file in os.listdir("levels") if file.endswith(".json")]
        filePaths.sort()
        y = levelListStartPos
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
            self.levels.append({"rect": rect, "path": fullPath, "name": name})
            y += levelbuttonHeight + levelbuttonVerticalPadding

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "mainMenu"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for level in self.levels:
                if level["rect"].collidepoint(event.pos):
                    return ("playLevel", level["path"])
        return None

    def update(self, dt):
        pass

    def draw(self, screen):
        screenWidth = screen.get_width()
        title = self.fontMain.render("Select Level", True, pygame.Color("royalblue3"))
        screen.blit(title, ((screenWidth - title.get_width()) // 2, levelListStartPos - title.get_height() - 10))
        for level in self.levels:
            pygame.draw.rect(screen, pygame.Color("royalblue3"), level["rect"], border_radius=8)
            label = self.fontSmall.render(level["name"], True, pygame.Color("white"))
            labelX = level["rect"].centerx - label.get_width() // 2
            labelY = level["rect"].centery - label.get_height() // 2
            screen.blit(label, (labelX, labelY))
