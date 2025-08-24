import pygame
import json

columnWidth = 160
startX = 20
startY = 60
labelHeight = 30

class Leaderboard:
    def __init__(self, fontMain, fontSmall, assets):
        self.fontMain = fontMain
        self.fontSmall = fontSmall
        self.scrollOffset = 0
        self.sortKey = "timestamp"
        self.sortAscending = False
        self.headers = ["team", "level", "time", "points", "timestamp"]
        self.entries = self._load_entries()
        self._sort()

    def _load_entries(self):
        try:
            with open("history.json", "r", encoding="utf-8") as file:
                data = json.load(file)
        except:
            return []

        entries = []
        for team, teamData in data.get("teams", {}).items():
            for levelName, completions in teamData.get("completed_levels", {}).items():
                for completion in completions:
                    entries.append({
                        "team": team,
                        "level": levelName,
                        "time": completion.get("time", 0),
                        "points": completion.get("points", 0),
                        "timestamp": completion.get("timestamp", "")
                    })
        return entries

    def _sort(self):
        self.entries.sort(key = lambda entry: entry[self.sortKey], reverse = not self.sortAscending)

    def handle_event(self, event):
        maxVisibleEntries = (pygame.display.get_surface().get_height() - 60) // labelHeight
        maxScroll = max(len(self.entries) - maxVisibleEntries, 0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "mainMenu"
            elif event.key == pygame.K_DOWN:
                self.scrollOffset = min(self.scrollOffset + 1, maxScroll)
            elif event.key == pygame.K_UP:
                self.scrollOffset = max(self.scrollOffset - 1, 0)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            #scroll up
            if event.button == 4:
                self.scrollOffset = max(self.scrollOffset - 1, 0)
            # scroll down
            elif event.button == 5:
                self.scrollOffset = min(self.scrollOffset + 1, maxScroll)
            elif event.button == 1:
                x, y = event.pos
                labelTop = 20
                if labelTop <= y <= labelTop + labelHeight:
                    index = (x - startX) // columnWidth
                    if 0 <= index < len(self.headers):
                        header = self.headers[index]
                        if self.sortKey == header:
                            self.sortAscending = not self.sortAscending
                        else:
                            self.sortAscending = True
                        self.sortKey = header
                        self._sort()
        return None

    def update(self, dt):
        pass

    def _draw_scroll(self, screen, maxVisibleEntries, visibleEntries):
        totalEntries = len(self.entries)
        if totalEntries > maxVisibleEntries:
            scrollbarHeight = screen.get_height() - startY
            scrollbarWidth = 8
            scrollbarX = screen.get_width() - scrollbarWidth - 4
            scrollbarY = startY

            thumbHeight = max(int(scrollbarHeight * (maxVisibleEntries / totalEntries)), 20)
            maxScroll = totalEntries - maxVisibleEntries
            scrollRatio = self.scrollOffset / maxScroll if maxScroll > 0 else 0
            thumbY = scrollbarY + int((scrollbarHeight - thumbHeight) * scrollRatio)

            pygame.draw.rect(screen, pygame.Color("dimgray"), (scrollbarX, scrollbarY, scrollbarWidth, scrollbarHeight))
            pygame.draw.rect(screen, pygame.Color("lightgray"), (scrollbarX, thumbY, scrollbarWidth, thumbHeight))

    def _draw_enrties(self, screen, visibleEntries):
        currentY = startY
        for entry in visibleEntries:
            for index, key in enumerate(self.headers):
                text = str(entry[key])
                if key == "time":
                    text = f"{entry[key]:.2f}s"
                if text == "":
                    text = "N\A"
                label = self.fontSmall.render(text, True, pygame.Color("lightgray"))
                screen.blit(label, (startX + index * columnWidth, currentY))
            currentY += labelHeight

    def _draw_labels(self, screen):
        labelYpos = 20
        for index, header in enumerate(self.headers):
            labelText = header.capitalize()
            if(header == "timestamp"):
                labelText = "Completed at"

            if header == self.sortKey:
                arrow = "^" if self.sortAscending else "v"
                labelText += f" {arrow}"

            label = self.fontMain.render(labelText, True, pygame.Color("white"))
            screen.blit(label, (startX + index * columnWidth, labelYpos))

    def draw(self, screen):
        maxVisibleEntries = (screen.get_height() - startY) // labelHeight
        visibleEntries = self.entries[self.scrollOffset:self.scrollOffset + maxVisibleEntries]
        screen.fill(pygame.Color("black"))
        self._draw_labels(screen)
        self._draw_enrties(screen, visibleEntries)
        self._draw_scroll(screen, maxVisibleEntries, visibleEntries)