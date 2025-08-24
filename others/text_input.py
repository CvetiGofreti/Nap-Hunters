import pygame


class TextInputBox:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        font: pygame.font.Font,
        placeholder: str,
        color_text: pygame.Color = pygame.Color("black"),
        color_inactive: pygame.Color = pygame.Color("dodgerblue"),
        color_active: pygame.Color = pygame.Color("blue"),
    ) -> None:
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.color_inactive: pygame.Color = color_inactive
        self.color_active: pygame.Color = color_active
        self.outline_color: pygame.Color = self.color_inactive
        self.font: pygame.font.Font = font
        self.label: str = ""
        self.hint: str = placeholder
        self.active: bool = False
        self.backspace_held: bool = False
        self.backspace_timer: float = 0.0
        self.repeat_delay: float = 0.4
        self.repeat_interval: float = 0.05
        self.backspace_first_delete: bool = True
        self.color_text: pygame.Color = color_text

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.outline_color = (
                self.color_active if self.active else self.color_inactive
            )

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.outline_color = self.color_inactive
            elif event.key == pygame.K_BACKSPACE:
                self.backspace_held = True
                self.backspace_first_delete = True
                self.backspace_timer = 0.0
                self.label = self.label[:-1]
            else:
                new_label = self.label + event.unicode
                new_width, _ = self.font.size(new_label)
                if new_width <= self.rect.width - 16:
                    self.label = new_label

        elif event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
            self.backspace_held = False

    def update(self, dt: float) -> None:
        if self.active and self.backspace_held:
            self.backspace_timer += dt

            if self.backspace_first_delete:
                if self.backspace_timer >= self.repeat_delay:
                    self.backspace_first_delete = False
                    self.backspace_timer = 0.0
            else:
                while self.backspace_timer >= self.repeat_interval:
                    self.backspace_timer -= self.repeat_interval
                    self.label = self.label[:-1]

    def draw(self, screen: pygame.Surface) -> None:
        display_label = self.label if self.label or self.active else self.hint
        label_color = self.color_text if self.label else self.color_inactive
        text_surface = self.font.render(display_label, True, label_color)
        text_x = self.rect.centerx - text_surface.get_width() // 2
        text_y = self.rect.centery - text_surface.get_height() // 2
        screen.blit(text_surface, (text_x, text_y))
        pygame.draw.rect(screen, self.outline_color, self.rect, 2, 8)
