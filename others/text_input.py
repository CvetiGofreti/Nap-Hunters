import pygame

class TextInputBox:
    def __init__(self, x, y, width, height, font, placeholder, colorText = pygame.Color("black"), colorInactive = pygame.Color('dodgerblue'), colorActive = pygame.Color('blue'), ):
        self.rect = pygame.Rect(x, y, width, height)
        self.colorInactive = colorInactive
        self.colorActive = colorActive
        self.outlineColor = self.colorInactive
        self.font = font
        self.label = ''
        self.hint = placeholder
        self.active = False
        self.backspaceHeld = False
        self.backspaceTimer = 0
        self.repeatDelay = 0.4
        self.repeatInterval = 0.05
        self.backspaceFirstDelete = True
        self.colorText = colorText

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.outlineColor = self.colorActive if self.active else self.colorInactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.outlineColor = self.colorInactive
            elif event.key == pygame.K_BACKSPACE:
                self.backspaceHeld = True
                self.backspaceFirstDelete = True
                self.backspaceTimer = 0
                self.label = self.label[:-1]
            else:
                newLabel = self.label + event.unicode
                newWidth, _ = self.font.size(newLabel)
                if newWidth <= self.rect.width - 16:
                    self.label = newLabel
                
        elif event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
            self.backspaceHeld = False

    def update(self, dt):
        if self.active and self.backspaceHeld:
            self.backspaceTimer += dt
    
            if self.backspaceFirstDelete:
                if self.backspaceTimer >= self.repeatDelay:
                    self.backspaceFirstDelete = False
                    self.backspaceTimer = 0
            else:
                while self.backspaceTimer >= self.repeatInterval:
                    self.backspaceTimer -= self.repeatInterval
                    self.label = self.label[:-1]

    def draw(self, screen):
        displayLabel = self.label if self.label or self.active else self.hint
        labelColor = self.colorText if self.label else self.colorInactive
        textSurface = self.font.render(displayLabel, True, labelColor)
        textX = self.rect.centerx - textSurface.get_width() // 2
        textY = self.rect.centery - textSurface.get_height() // 2
        screen.blit(textSurface, (textX, textY))
        pygame.draw.rect(screen, self.outlineColor, self.rect, 2, 8)
