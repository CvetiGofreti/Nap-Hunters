import pygame, os, json
from others.tile_type import TileType
from others.floor_type import FloorType
from datetime import datetime
from others.text_input import TextInputBox
from others.button import Button
from others.spray_type import SprayType

tileSize = 64
paletteWidth = 192

class LevelBuilder:
    def __init__(self, fontMain, fontSmall, assets):
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        pygame.display.set_mode((self.screenWidth + paletteWidth, self.screenHeight))
        self.fontMain = fontMain
        self.fontSmall = fontSmall
        self.tileCountWidth = self.screenWidth // tileSize
        self.tileCountHeight = self.screenHeight // tileSize
        self.grid = [[TileType.EMPTY for _ in range(self.tileCountWidth)] for _ in range(self.tileCountHeight)]
        self.assets = assets

        self.grid[self.tileCountHeight - 1][0] = TileType.BLUE_PLAYER
        self.grid[self.tileCountHeight - 1][1] = TileType.RED_PLAYER
        self.grid[1][self.tileCountWidth - 2] = TileType.BLUE_BED
        self.grid[1][self.tileCountWidth - 1] = TileType.BLUE_BED
        self.grid[1][self.tileCountWidth - 5] = TileType.RED_BED
        self.grid[1][self.tileCountWidth - 4] = TileType.RED_BED

        self.dragging = None
        self.leftDown = False
        self.rightDown = False

        self.paletteRect = pygame.Rect(self.screenWidth, 0, paletteWidth, self.screenHeight)
        #todo - positions not hard coded
        x0, y0 = self.screenWidth + 16, 16
        self.items = [{"type": TileType.FLOOR, "name": "Floor", "rect": pygame.Rect(x0, y0, tileSize, tileSize), "asset": assets.floorVariants[FloorType.MID]},
                      {"type": TileType.SNACK, "name": "Snack", "rect": pygame.Rect(x0 + 64 + 16, y0, tileSize, tileSize), "asset": assets.entities[TileType.SNACK]},
                      {"type": TileType.BOOKS, "name": "Books", "rect": pygame.Rect(x0, y0 + 64 + 32, tileSize, tileSize), "asset": assets.entities[TileType.BOOKS]},
                      {"type": TileType.SPRAY, "name": "Water spray", "rect": pygame.Rect(x0 + 64 + 16, y0 + 64 + 32, tileSize, tileSize), "asset": assets.sprays[SprayType.OFF]},
                      {"type": TileType.BUTTON, "name": "Button", "rect": pygame.Rect(x0, y0 + 64 + 32 + 64 + 32, tileSize, tileSize), "asset": assets.entities[TileType.BUTTON]}]
        
        self.selectedItemType = TileType.FLOOR
        self.hoverCell = None

        saveButtonHeight = 40
        saveButtonMargin = 16
        buttonPos = (self.screenWidth + 16, self.screenHeight - saveButtonHeight - saveButtonMargin)  # bottom left corner of palette
        buttonSize = (paletteWidth - 32, saveButtonHeight)

        self.saveButton = Button(
            pos = buttonPos,
            size = buttonSize,
            label = "Save Level",
            onClick = self._save_level,
            font = self.fontSmall
        )

        inputWidth = paletteWidth - 32
        inputHeight = 32
        inputLevelNameX = self.screenWidth + 16
        inputLevelNameY = self.saveButton.rect.y - inputHeight - 8
        self.levelNameBox = TextInputBox(inputLevelNameX, inputLevelNameY, inputWidth, inputHeight, fontSmall, "Enter level name", pygame.Color("white"))

    def _pick_floor_variant(self, x, y):
        left  = (x > 0 and self._get_tyle_type_at(x - 1, y) == TileType.FLOOR)
        right = (x < self.tileCountWidth - 1 and self._get_tyle_type_at(x + 1, y) == TileType.FLOOR)
        if left and right: return FloorType.MID
        if not left and right: return FloorType.LEFT
        if left and not right: return FloorType.RIGHT
        return FloorType.FLOOR_SINGLE

    def _is_bed_tile(self, x, y):
        if 0 <= y < self.tileCountHeight and 0 <= x < self.tileCountWidth:
            t = self._get_tyle_type_at(x, y)
            if t in (TileType.BLUE_BED, TileType.RED_BED):
                return True
        return False

    def _is_player_tile(self, x, y):
        if 0 <= y < self.tileCountHeight and 0 <= x < self.tileCountWidth:
            t = self._get_tyle_type_at(x, y)
            if t in (TileType.BLUE_PLAYER, TileType.RED_PLAYER):
                return True
        return False

    def _entity_at(self, x, y):
        if self._is_bed_tile(x, y):
            return self._get_tyle_type_at(x, y)
        if self._is_player_tile(x, y):
            return self._get_tyle_type_at(x, y)
        return None
    
    def _get_tyle_type_at(self, x, y):
        if 0 <= y < self.tileCountHeight and 0 <= x < self.tileCountWidth:
            return self.grid[y][x]
        return TileType.INVALID

    def _save_level(self):
        os.makedirs("levels", exist_ok=True)
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_level.json"
        path = os.path.join("levels", filename)
        data = {
            "name": self.levelNameBox.label,
            "grid": [[cell.value for cell in row] for row in self.grid]
        }
        with open(path, "w") as file:
            json.dump(data, file, indent=2)
        print(f"Level saved: {path}")

    def _handle_click_event(self, event):
        mouseX, mouseY = event.pos
        if event.button == 1: self.leftDown = True
        if event.button == 3: self.rightDown = True

        if event.button == 2 and mouseX < self.screenWidth and mouseY < self.screenHeight:
            gridX, gridY = mouseX // tileSize, mouseY // tileSize
            entityType = self._entity_at(gridX, gridY)
            if entityType is not None:
                self.dragging = (entityType , gridX, gridY)

        if self.paletteRect.collidepoint(mouseX, mouseY) and event.button == 1:
            for item in self.items:
                if item["rect"].collidepoint(mouseX, mouseY):
                    self.selectedItemType = item["type"]
                    return None

        if mouseX < self.screenWidth and mouseY < self.screenHeight:
            gridX, gridY = mouseX // tileSize, mouseY // tileSize
            if self._entity_at(gridX, gridY) is None:
                if event.button == 1:
                    self.grid[gridY][gridX] = self.selectedItemType
                elif event.button == 3:
                    self.grid[gridY][gridX] = TileType.EMPTY

        self.saveButton.handle_event(event)

    def _handle_unclick_event(self, event):
        if event.button == 1: self.leftDown = False
        if event.button == 3: self.rightDown = False
        if event.button == 2: self.dragging = None
        
    def _handle_drag_event(self, event):
        mouseX, mouseY = event.pos
        if mouseX < self.screenWidth and mouseY < self.screenHeight:
            gridX, gridY = mouseX // tileSize, mouseY // tileSize
            self.hoverCell = (gridX, gridY)
        else:
            self.hoverCell = None

        if mouseX < self.screenWidth and mouseY < self.screenHeight:
            gridX, gridY = mouseX // tileSize, mouseY // tileSize
            if self.leftDown and self._entity_at(gridX, gridY) is None:
                self.grid[gridY][gridX] = self.selectedItemType
            elif self.rightDown and self._entity_at(gridX, gridY) is None:
                self.grid[gridY][gridX] = TileType.EMPTY

        if self.dragging and mouseX < self.screenWidth and mouseY < self.screenHeight:
            gridX, gridY = mouseX // tileSize, mouseY // tileSize
            kind, oldX, oldY = self.dragging

            if kind in (TileType.BLUE_PLAYER, TileType.RED_PLAYER):
                gridX = max(0, min(self.tileCountWidth - 1, gridX))
                gridY = max(0, min(self.tileCountHeight - 1, gridY))

                if not self._is_bed_tile(gridX, gridY) and self._get_tyle_type_at(gridX, gridY) == TileType.EMPTY:
                    self.grid[oldY][oldX] = TileType.EMPTY
                    self.grid[gridY][gridX] = kind
                    self.dragging = (kind, gridX, gridY)

            elif kind in (TileType.BLUE_BED, TileType.RED_BED):
                gridX = max(0, min(self.tileCountWidth - 2, gridX))
                gridY = max(0, min(self.tileCountHeight - 1, gridY))

                if (self._get_tyle_type_at(gridX, gridY) == TileType.EMPTY and
                    self._get_tyle_type_at(gridX + 1, gridY) == TileType.EMPTY):
                    self.grid[oldY][oldX] = TileType.EMPTY
                    self.grid[oldY][oldX + 1] = TileType.EMPTY
                    self.grid[gridY][gridX] = kind
                    self.grid[gridY][gridX + 1] = kind
                    self.dragging = (kind, gridX, gridY)

    def handle_event(self, event):
        self.levelNameBox.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.display.set_mode((self.screenWidth, self.screenHeight))
            return "mainMenu"

        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_click_event(event)

        elif event.type == pygame.MOUSEBUTTONUP:
            self._handle_unclick_event(event)

        elif event.type == pygame.MOUSEMOTION:
            self._handle_drag_event(event)

        return None

    def update(self, dt):
        self.levelNameBox.update(dt)

    def _draw_grid(self, screen):
        gridColor = pygame.Color("dimgray")
        for x in range(self.tileCountWidth + 1):
            pygame.draw.line(screen, gridColor, (x*tileSize, 0), (x*tileSize, self.screenHeight))
        for y in range(self.tileCountHeight + 1):
            pygame.draw.line(screen, gridColor, (0, y*tileSize), (self.screenWidth, y*tileSize))

        if self.hoverCell:
            gx, gy = self.hoverCell
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(gx*tileSize, gy*tileSize, tileSize, tileSize), 2)

                   
    def _draw_items(self, screen):
        for y in range(self.tileCountHeight):
            for x in range(self.tileCountWidth):
                if self._get_tyle_type_at(x, y) == TileType.FLOOR:
                    chosenVariant = self._pick_floor_variant(x, y)
                    screen.blit(self.assets.floorVariants[chosenVariant], (x*tileSize, y*tileSize))
                if self._get_tyle_type_at(x, y) == TileType.SNACK:
                    screen.blit(self.assets.entities[TileType.SNACK], (x*tileSize, y*tileSize))
                if self._get_tyle_type_at(x, y) == TileType.BOOKS:
                    screen.blit(self.assets.entities[TileType.BOOKS], (x*tileSize, y*tileSize))
                if self._get_tyle_type_at(x, y) == TileType.SPRAY:
                    screen.blit(self.assets.sprays[SprayType.OFF], (x*tileSize, y*tileSize))
                if self._get_tyle_type_at(x, y) == TileType.BUTTON:
                    screen.blit(self.assets.entities[TileType.BUTTON], (x*tileSize, y*tileSize))

    def _draw_players(self, screen):
        for y in range(self.tileCountHeight):
            for x in range(self.tileCountWidth):
                if self._get_tyle_type_at(x, y) == TileType.RED_PLAYER:
                    screen.blit(self.assets.playerImages[TileType.RED_PLAYER], (x*tileSize, y*tileSize))
                if self._get_tyle_type_at(x, y) == TileType.BLUE_PLAYER:
                    screen.blit(self.assets.playerImages[TileType.BLUE_PLAYER], (x*tileSize, y*tileSize))

    def _draw_beds(self, screen):
        for y in range(self.tileCountHeight):
            for x in range(self.tileCountWidth):
                if self._get_tyle_type_at(x, y) == TileType.RED_BED and self._get_tyle_type_at(x + 1, y) == TileType.RED_BED:
                    screen.blit(self.assets.beds[TileType.RED_BED], (x*tileSize, y*tileSize))
                if self._get_tyle_type_at(x, y) == TileType.BLUE_BED and self._get_tyle_type_at(x + 1, y) == TileType.BLUE_BED:
                    screen.blit(self.assets.beds[TileType.BLUE_BED], (x*tileSize, y*tileSize))

    def _draw_palette(self, screen):
        pygame.draw.rect(screen, pygame.Color("black"), self.paletteRect)
        for item in self.items:
            tileType = item["type"]
            rect = item["rect"]
            image = item["asset"]

            if image:
                screen.blit(image, rect.topleft)

            label = self.fontSmall.render(item["name"], True, pygame.Color("white"))
            screen.blit(label, (rect.x, rect.bottom + 4))

            if tileType == self.selectedItemType:
                pygame.draw.rect(screen, pygame.Color("yellow"), rect, 3)
            else:
                pygame.draw.rect(screen, pygame.Color("white"), rect, 3)


        self.levelNameBox.draw(screen)

        self.saveButton.draw(screen)

    def draw(self, screen):
        self._draw_items(screen)
        self._draw_grid(screen)
        self._draw_players(screen)
        self._draw_beds(screen)
        self._draw_palette(screen)
