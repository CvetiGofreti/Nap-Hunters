
from typing import Callable, Optional, Tuple

import pygame
from pygame.surface import Surface


class Button:
    def __init__(
        self,
        pos: Tuple[int, int],
        size: Tuple[int, int],
        label: str,
        on_click: Optional[Callable[[], None]] = None,
        font: Optional[pygame.font.Font] = None,
        text_color: pygame.Color = pygame.Color("white"),
        background_color: pygame.Color = pygame.Color("royalblue3"),
        show_check: bool = False,
        check_image: Optional[Surface] = None
    ) -> None:
        self.rect: pygame.Rect = pygame.Rect(pos, size)
        self.label: str = label
        self.on_click: Optional[Callable[[], None]] = on_click
        self.font: pygame.font.Font = font or pygame.font.Font(None, 24)
        self.text_color: pygame.Color = text_color
        self.background_color: pygame.Color = background_color
        self.show_check: bool = show_check
        self.check_image: Optional[Surface] = check_image
        self.rendered_label: Surface = self.font.render(self.label, True, self.text_color)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click is not None:
                    self.on_click()

    def draw(self, screen: Surface) -> None:
        pygame.draw.rect(screen, self.background_color, self.rect, border_radius=8)

        label_pos = (
            self.rect.centerx - self.rendered_label.get_width() // 2,
            self.rect.centery - self.rendered_label.get_height() // 2,
        )
        screen.blit(self.rendered_label, label_pos)

        if self.show_check and self.check_image is not None:
            check_rect = self.check_image.get_rect()
            check_rect.centery = self.rect.centery
            check_rect.right = self.rect.right - 10
            screen.blit(self.check_image, check_rect)
