import pygame

class Button:
    def __init__(self, pos, size, label, onClick, font, textColor = pygame.Color("white"), backgroundColor = pygame.Color("royalblue3"), showCheck = False, checkImage = None):
        self.rect = pygame.Rect(pos, size)
        self.label = label
        self.onClick = onClick
        self.font = font
        self.textColor = textColor
        self.backgroundColor = backgroundColor
        self.showCheck = showCheck
        self.checkImage = checkImage
        self.renderedLabel = self.font.render(self.label, True, self.textColor)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if callable(self.onClick):
                    self.onClick()

    def draw(self, screen):
        pygame.draw.rect(screen, self.backgroundColor, self.rect, border_radius=8)

        labelPos = (
            self.rect.centerx - self.renderedLabel.get_width() // 2,
            self.rect.centery - self.renderedLabel.get_height() // 2
        )
        screen.blit(self.renderedLabel, labelPos)

        if self.showCheck and self.checkImage:
            checkRect = self.checkImage.get_rect()
            checkRect.centery = self.rect.centery
            checkRect.right = self.rect.right - 10
            screen.blit(self.checkImage, checkRect)