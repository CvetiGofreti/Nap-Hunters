import pygame

class MainMenu:
    def __init__(self, fontMain, fontSmall):
        self.fontMain = fontMain
        self.fontSmall = fontSmall
        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        self.button = pygame.Rect(0, 0, 260, 70)
        self.button.center = (screenWidth // 2, screenHeight // 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button.collidepoint(event.pos):
                return "levelBuilder"
        return None

    def update(self, dt):
        pass

    def draw(self, screen):
        buttonColor = (60, 120, 220)
        pygame.draw.rect(screen, buttonColor, self.button, border_radius=12)
        label = self.fontMain.render("Build Level", True, (255, 255, 255))
        screen.blit(label, (self.button.centerx - label.get_width() // 2,
                            self.button.centery - label.get_height() // 2))