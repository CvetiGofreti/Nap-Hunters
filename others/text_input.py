import pygame

class TextInputBox:
    def __init__(self, x, y, width, height, font, placeholder, colorText = pygame.Color("black"), colorInactive = pygame.Color('dodgerblue'), colorActive = pygame.Color('blue'), ):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = colorInactive
        self.color_active = colorActive
        self.outline_color = self.color_inactive
        self.font = font
        self.label = ''
        self.hint = placeholder
        self.active = False
        self.backspace_held = False
        self.backspace_timer = 0
        self.repeat_delay = 0.4
        self.repeat_interval = 0.05
        self.backspace_first_delete = True
        self.color_text = colorText

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.outline_color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.outline_color = self.color_inactive
            elif event.key == pygame.K_BACKSPACE:
                self.backspace_held = True
                self.backspace_first_delete = True
                self.backspace_timer = 0
                self.label = self.label[:-1]
            else:
                newLabel = self.label + event.unicode
                newWidth, _ = self.font.size(newLabel)
                if newWidth <= self.rect.width - 16:
                    self.label = newLabel
                
        elif event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
            self.backspace_held = False

    def update(self, dt):
        if self.active and self.backspace_held:
            self.backspace_timer += dt
    
            if self.backspace_first_delete:
                if self.backspace_timer >= self.repeat_delay:
                    self.backspace_first_delete = False
                    self.backspace_timer = 0
            else:
                while self.backspace_timer >= self.repeat_interval:
                    self.backspace_timer -= self.repeat_interval
                    self.label = self.label[:-1]

    def draw(self, screen):
        display_label = self.label if self.label or self.active else self.hint
        label_color = self.color_text if self.label else self.color_inactive
        text_surface = self.font.render(display_label, True, label_color)
        text_x = self.rect.centerx - text_surface.get_width() // 2
        text_y = self.rect.centery - text_surface.get_height() // 2
        screen.blit(text_surface, (text_x, text_y))
        pygame.draw.rect(screen, self.outline_color, self.rect, 2, 8)
