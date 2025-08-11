import pygame, os, json
from tile_type import TileType
from floor_type import FloorType
from datetime import datetime

tileSize = 64
paletteWidth = 192

class LevelBuilder:
    def __init__(self, fontMain, fontSmall):
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        pygame.display.set_mode((self.screenWidth + paletteWidth, self.screenHeight))
        self.fontMain = fontMain
        self.fontSmall = fontSmall
        self.tileCountWidth = self.screenWidth // tileSize
        self.tileCountHeight = self.screenHeight // tileSize
        self.grid = [[TileType.EMPTY for _ in range(self.tileCountWidth)] for _ in range(self.tileCountHeight)]

        def loadInTileSize(path):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (tileSize, tileSize))

        self.floorVariants = {
            FloorType.MID: loadInTileSize("graphics/levels/floor.png"),
            FloorType.LEFT: loadInTileSize("graphics/levels/floor_left.png"),
            FloorType.RIGHT: loadInTileSize("graphics/levels/floor_right.png"),
            FloorType.FLOOR_SINGLE: loadInTileSize("graphics/levels/floor_both.png"),
        }

        self.playerImages = [
            loadInTileSize("graphics/players/playerBlue.png"),
            loadInTileSize("graphics/players/playerRed.png"),
        ]

        self.players = [
            {"name": "blue", "pos": [0, self.tileCountHeight - 1]},
            {"name": "red",  "pos": [1, self.tileCountHeight - 1]},
        ]

        def load_bed(path):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (2*tileSize, tileSize))

        bedBlue = load_bed("graphics/players/bedBlue.png")
        bedRed = load_bed("graphics/players/bedRed.png")
        
        self.beds = [
            {"name": "bedBlue", "pos": [self.tileCountWidth - 2, 1], "size": (2, 1), "img": bedBlue},
            {"name": "bedRed",  "pos": [self.tileCountWidth - 5, 1], "size": (2, 1), "img": bedRed},
        ]

        self.dragging = None
        self.leftDown = False
        self.rightDown = False

        #todo - make this easily expandable
        self.paletteRect = pygame.Rect(self.screenWidth, 0, paletteWidth, self.screenHeight)
        x0, y0 = self.screenWidth + 16, 16
        self.items = [{"id": TileType.FLOOR, "name": "Floor", "rect": pygame.Rect(x0, y0, tileSize, tileSize)}]
        self.item_icon = self.floorVariants[FloorType.MID]
        self.selectedItemId = TileType.FLOOR
        self.hover_cell = None

        #todo - make this not so hard coded
        saveButtonHeight = 40
        saveButtonMargin = 16
        self.saveButtonRect = pygame.Rect(
            self.screenWidth + 16,
            self.screenHeight - saveButtonHeight - saveButtonMargin,
            paletteWidth - 32,
            saveButtonHeight
        )
        
        #todo - make this not so hard coded
        self.levelName = "Untitled"
        self.inputActive = False
        inputHeight = 32
        self.inputRect = pygame.Rect(
            self.screenWidth + 16,
            self.saveButtonRect.y - inputHeight - 8,
            paletteWidth - 32,
            inputHeight
        )

    def _pick_floor_variant(self, x, y):
        left  = (x > 0 and self.grid[y][x-1] == TileType.FLOOR)
        right = (x < self.tileCountWidth - 1 and self.grid[y][x+1] == TileType.FLOOR)
        if left and right: return FloorType.MID
        if not left and right: return FloorType.LEFT
        if left and not right: return FloorType.RIGHT
        return FloorType.FLOOR_SINGLE

    def _player_index_at(self, x, y):
        for index, player in enumerate(self.players):
            if player["pos"][0] == x and player["pos"][1] == y:
                return index
        return None

    def _bed_index_at(self, x, y):
        for index, bed in enumerate(self.beds):
            bedX, bedY = bed["pos"]
            bedWidth, bedHeight = bed["size"]
            if (bedX <= x < bedX + bedWidth) and (bedY <= y < bedY + bedHeight):
                return index
        return None

    def _entity_at(self, x, y):
        bedIndex = self._bed_index_at(x, y)
        if bedIndex is not None:
            return ("bed", bedIndex)
        playerIndex = self._player_index_at(x, y)
        if playerIndex is not None:
            return ("player", playerIndex)
        return None
    
    def _save_level(self):
        os.makedirs("levels", exist_ok=True)
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_level.json"
        path = os.path.join("levels", filename)
        data = {
            "name": self.levelName,
            "grid": [[cell.value for cell in row] for row in self.grid],
            "players": [{"name": player["name"], "pos": player["pos"]} for player in self.players],
            "beds": [{"name": bed["name"], "pos": bed["pos"], "size": bed["size"]} for bed in self.beds]
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
            entity = self._entity_at(gridX, gridY)
            if entity is not None:
                self.dragging = entity

        if self.paletteRect.collidepoint(mouseX, mouseY) and event.button == 1:
            for item in self.items:
                if item["rect"].collidepoint(mouseX, mouseY):
                    self.selectedItemId = item["id"]
                    return None

        if mouseX < self.screenWidth and mouseY < self.screenHeight:
            gridX, gridY = mouseX // tileSize, mouseY // tileSize
            if self._entity_at(gridX, gridY) is None:
                if event.button == 1:
                    self.grid[gridY][gridX] = self.selectedItemId
                elif event.button == 3:
                    self.grid[gridY][gridX] = TileType.EMPTY

        if self.inputRect.collidepoint(mouseX, mouseY):
            self.inputActive = True
        else:
            self.inputActive = False

        if self.saveButtonRect.collidepoint(mouseX, mouseY):
            self._save_level()

    def _handle_unclick_event(self, event):
        if event.button == 1: self.leftDown = False
        if event.button == 3: self.rightDown = False
        if event.button == 2: self.dragging = None
        
    def _handle_drag_event(self, event):
        mouseX, mouseY = event.pos
        if mouseX < self.screenWidth and mouseY < self.screenHeight:
            gridX, gridY = mouseX // tileSize, mouseY // tileSize
            self.hover_cell = (gridX, gridY)
        else:
            self.hover_cell = None

        if mouseX < self.screenWidth and mouseY < self.screenHeight:
            gridX, gridY = mouseX // tileSize, mouseY // tileSize
            if self.leftDown and self._entity_at(gridX, gridY) is None:
                self.grid[gridY][gridX] = self.selectedItemId
            elif self.rightDown and self._entity_at(gridX, gridY) is None:
                self.grid[gridY][gridX] = TileType.EMPTY

        if self.dragging and mouseX < self.screenWidth and mouseY < self.screenHeight:
            gridX, gridY = mouseX // tileSize, mouseY // tileSize
            kind, index = self.dragging

            if kind == "player":
                gridX = max(0, min(self.tileCountWidth - 1, gridX))
                gridY = max(0, min(self.tileCountHeight - 1, gridY))
                other = 1 - index
                if not (self.players[other]["pos"][0] == gridX and self.players[other]["pos"][1] == gridY) \
                   and self._bed_index_at(gridX, gridY) is None:
                    self.players[index]["pos"] = [gridX, gridY]

            elif kind == "bed":
                gridX = max(0, min(self.tileCountWidth - 2, gridX))
                gridY = max(0, min(self.tileCountHeight - 1, gridY))
                occupiedByPlayer = (
                    self._player_index_at(gridX, gridY) is not None or
                    self._player_index_at(gridX + 1, gridY) is not None
                )
                occupiedByOtherBed = False
                for j, bed in enumerate(self.beds):
                    if j == index: continue
                    bedX, bedY = bed["pos"]
                    if (gridX <= bedX + 1 and gridX + 1 >= bedX) and (gridY == bedY):
                        occupiedByOtherBed = True
                        break
                if not occupiedByPlayer and not occupiedByOtherBed:
                    self.beds[index]["pos"] = [gridX, gridY]

    def _handle_key_click_event(self, event):
        if event.key == pygame.K_RETURN:
            self.inputActive = False
        elif event.key == pygame.K_BACKSPACE:
            self.levelName = self.levelName[:-1]
        else:
            self.levelName += event.unicode

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.display.set_mode((self.screenWidth, self.screenHeight))
            return "mainMenu"

        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_click_event(event)

        elif event.type == pygame.MOUSEBUTTONUP:
            self._handle_unclick_event(event)

        elif event.type == pygame.MOUSEMOTION:
            self._handle_drag_event(event)

        elif event.type == pygame.KEYDOWN and self.inputActive:
            self._handle_key_click_event(event)

        return None

    def update(self, dt):
        pass

    def _draw_grid(self, screen):
        gridColor = pygame.Color("dimgray")
        for x in range(self.tileCountWidth + 1):
            pygame.draw.line(screen, gridColor, (x*tileSize, 0), (x*tileSize, self.screenHeight))
        for y in range(self.tileCountHeight + 1):
            pygame.draw.line(screen, gridColor, (0, y*tileSize), (self.screenWidth, y*tileSize))

        if self.hover_cell:
            gx, gy = self.hover_cell
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(gx*tileSize, gy*tileSize, tileSize, tileSize), 2)

                   
    def _draw_floor(self, screen):
        for y in range(self.tileCountHeight):
            for x in range(self.tileCountWidth):
                if self.grid[y][x] == TileType.FLOOR:
                    chosenVariant = self._pick_floor_variant(x, y)
                    screen.blit(self.floorVariants[chosenVariant], (x*tileSize, y*tileSize))

    def _draw_players(self, screen):
        for i, p in enumerate(self.players):
            px, py = p["pos"]
            screen.blit(self.playerImages[i], (px*tileSize, py*tileSize))

    def _draw_beds(self, screen):
        for bed in self.beds:
            bedX, bedY = bed["pos"]
            screen.blit(bed["img"], (bedX*tileSize, bedY*tileSize))

    def _draw_palette(self, screen):
        #todo - make this easily expandable
        pygame.draw.rect(screen, (22, 22, 28), self.paletteRect)
        it = self.items[0]
        screen.blit(self.item_icon, it["rect"].topleft)
        label = self.fontSmall.render(it["name"], True, (220,220,225))
        screen.blit(label, (it["rect"].x, it["rect"].bottom + 4))
        pygame.draw.rect(screen, (255, 215, 0), it["rect"], 3)

        inputOutlineColor = pygame.Color("yellow") if self.inputActive else pygame.Color("white")
        pygame.draw.rect(screen, inputOutlineColor, self.inputRect, 2)
        nameSurface = self.fontSmall.render(self.levelName, True, pygame.Color("white"))
        screen.blit(nameSurface, (self.inputRect.x + 4, self.inputRect.y + 5))

        pygame.draw.rect(screen, pygame.Color("royalblue3"), self.saveButtonRect, border_radius=6)
        save_text = self.fontSmall.render("Save Level", True, pygame.Color("white"))
        screen.blit(
            save_text,
            (self.saveButtonRect.centerx - save_text.get_width() // 2,
             self.saveButtonRect.centery - save_text.get_height() // 2)
        )

    def draw(self, screen):
        self._draw_floor(screen)
        self._draw_grid(screen)
        self._draw_players(screen)
        self._draw_beds(screen)
        self._draw_palette(screen)
