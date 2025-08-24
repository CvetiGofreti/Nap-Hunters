import pygame
from abc import ABC, abstractmethod

class BaseScreen(ABC):
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> str | tuple | None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass
