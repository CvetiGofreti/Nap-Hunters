import json
import pygame

from screens.interface import BaseScreen

COLUMN_WIDTH = 160
START_X = 20
START_Y = 60
LABEL_HEIGHT = 30


class Leaderboard(BaseScreen):
    def __init__(self, font_main: pygame.font.Font, font_small: pygame.font.Font, _assets) -> None:
        self.font_main: pygame.font.Font = font_main
        self.font_small: pygame.font.Font = font_small
        self.scroll_offset: int = 0
        self.sort_key: str = "timestamp"
        self.sort_ascending: bool = False
        self.headers: list[str] = ["team", "level", "time", "points", "timestamp"]
        self.entries: list[dict] = self._load_entries()
        self._sort()

    def _load_entries(self) -> list[dict]:
        try:
            with open("history.json", "r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError):
            return []

        return [
            {
                "team": team,
                "level": level_name,
                "time": completion.get("time", 0),
                "points": completion.get("points", 0),
                "timestamp": completion.get("timestamp", "")
            }
            for team, team_data in data.get("teams", {}).items()
            for level_name, completions in team_data.get("completed_levels", {}).items()
            for completion in completions
        ]

    def _sort(self) -> None:
        self.entries.sort(
            key = lambda entry: entry[self.sort_key],
            reverse = not self.sort_ascending
        )

    def handle_event(self, event: pygame.event.Event) -> str | None:
        max_visible = (pygame.display.get_surface().get_height() - 60) // LABEL_HEIGHT
        max_scroll = max(len(self.entries) - max_visible, 0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "mainMenu"
            if event.key == pygame.K_DOWN:
                self.scroll_offset = min(self.scroll_offset + 1, max_scroll)
            elif event.key == pygame.K_UP:
                self.scroll_offset = max(self.scroll_offset - 1, 0)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            #scroll up
            if event.button == 4:
                self.scroll_offset = max(self.scroll_offset - 1, 0)
            # scroll down
            elif event.button == 5:
                self.scroll_offset = min(self.scroll_offset + 1, max_scroll)
            elif event.button == 1:
                x, y = event.pos
                if 20 <= y <= 20 + LABEL_HEIGHT:
                    index = (x - START_X) // COLUMN_WIDTH
                    if 0 <= index < len(self.headers):
                        header = self.headers[index]
                        if self.sort_key == header:
                            self.sort_ascending = not self.sort_ascending
                        else:
                            self.sort_ascending = True
                        self.sort_key = header
                        self._sort()
        return None

    def update(self, dt: float) -> None:
        pass

    def _draw_scroll(self, screen: pygame.Surface, max_visible: int) -> None:
        total_entries = len(self.entries)
        if total_entries > max_visible:
            scrollbar_height = screen.get_height() - START_Y
            scrollbar_width = 8
            scrollbar_x = screen.get_width() - scrollbar_width - 4
            scrollbar_y = START_Y

            thumb_height = max(int(scrollbar_height * (max_visible / total_entries)), 20)
            max_scroll = total_entries - max_visible
            scroll_ratio = self.scroll_offset / max_scroll if max_scroll > 0 else 0
            thumb_y = scrollbar_y + int((scrollbar_height - thumb_height) * scroll_ratio)

            pygame.draw.rect(
                screen,
                pygame.Color("dimgray"),
                (scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height)
            )
            pygame.draw.rect(
                screen,
                pygame.Color("lightgray"),
                (scrollbar_x, thumb_y, scrollbar_width, thumb_height)
            )

    def _draw_entries(self, screen: pygame.Surface, entries: list[dict]) -> None:
        y = START_Y
        for entry in entries:
            for index, key in enumerate(self.headers):
                value = f"{entry[key]:.2f}s" if key == "time" else str(entry[key] or "N/A")
                label = self.font_small.render(value, True, pygame.Color("lightgray"))
                screen.blit(label, (START_X + index * COLUMN_WIDTH, y))
            y += LABEL_HEIGHT

    def _draw_labels(self, screen: pygame.Surface) -> None:
        y = 20
        for index, header in enumerate(self.headers):
            text = "Completed at" if header == "timestamp" else header.capitalize()
            if header == self.sort_key:
                arrow = "^" if self.sort_ascending else "v"
                text += f" {arrow}"
            label = self.font_main.render(text, True, pygame.Color("white"))
            screen.blit(label, (START_X + index * COLUMN_WIDTH, y))

    def draw(self, screen: pygame.Surface) -> None:
        max_visible = (screen.get_height() - START_Y) // LABEL_HEIGHT
        visible = self.entries[self.scroll_offset:self.scroll_offset + max_visible]
        screen.fill(pygame.Color("black"))
        self._draw_labels(screen)
        self._draw_entries(screen, visible)
        self._draw_scroll(screen, max_visible)
