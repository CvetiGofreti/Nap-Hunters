import os
import json
import pygame
import others.global_values
from others.tile_type import TileType
from others.floor_type import FloorType
from others.controls_type import ControlsType
from entities.player import Player
from entities.snack import Snack
from others.level_history_manager import LevelHistoryManager
from entities.books import MovableBooks
from entities.button import Button
from entities.spray import Spray

tileSize = 64

class GameScreen:
    def __init__(self, fontMain, fontSmall, assets):
        self.fontMain = fontMain
        self.fontSmall = fontSmall
        self.assets = assets
        self.grid = []
        self.levelName = "Level"
        self.players = []
        self.hasError = False
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        self.tileCountWidth = self.screenWidth // tileSize
        self.tileCountHeight = self.screenHeight // tileSize
        self.levelPath = ""
        self.levelComplete = False
        self.levelStartTime = 0
        self.snacks = []
        self.movableBooks = []
        self.buttons = []
        self.sprays = []

    def _get_tyle_type_at(self, x, y):
        if 0 <= y < self.tileCountHeight and 0 <= x < self.tileCountWidth:
            return self.grid[y][x]
        return TileType.INVALID

    def load_level(self, levelPath):
        self.levelPath = levelPath
        self.movableBooks = []
        try:
            with open(levelPath, "r", encoding="utf-8") as level:
                data = json.load(level)
        except Exception as exeption:
            print(f"Failed to load level {levelPath}: {exeption}")
            self.hasError = True
            return

        self.levelName = data.get("name", "Level")
        grid = data.get("grid", [])
        self.grid = [[TileType(value) for value in row] for row in grid]
        self.players = []

        for y in range(self.tileCountHeight):
            for x in range(self.tileCountWidth):
                tileType = self._get_tyle_type_at(x, y)
                if tileType == TileType.BLUE_PLAYER:
                    image = self.assets.playerImages[tileType]
                    controls = {ControlsType.LEFT: pygame.K_a, ControlsType.RIGHT: pygame.K_d, ControlsType.JUMP: pygame.K_w}
                    self.players.append(Player(image, (x, y) , controls, TileType.BLUE_BED))
                if tileType == TileType.RED_PLAYER:
                    image = self.assets.playerImages[tileType]
                    controls = {ControlsType.LEFT: pygame.K_LEFT, ControlsType.RIGHT: pygame.K_RIGHT, ControlsType.JUMP: pygame.K_UP}
                    self.players.append(Player(image, (x, y) , controls, TileType.RED_BED))
                if tileType == TileType.SNACK:
                    snack = Snack(x, y, self.assets.entities[tileType])
                    self.snacks.append(snack)
                if tileType == TileType.BOOKS:
                    book = MovableBooks(x, y, self.assets.entities[tileType])
                    self.movableBooks.append(book)
                if tileType == TileType.BUTTON:
                    self.buttons.append(Button(x, y, self.assets))
                if tileType == TileType.SPRAY:
                    height = 1
                    while y - height >= 0:
                        aboveTile = self._get_tyle_type_at(x, y - height)
                        if aboveTile == TileType.EMPTY or aboveTile == TileType.SNACK:
                            height += 1
                        else:
                            break
                    self.sprays.append(Spray(x, y, height, self.assets))

        self._validate_loaded_level()
        self.levelStartTime = pygame.time.get_ticks() / 1000

    def _pick_floor_variant(self, grid, x, y):
        gridWidth, gridHight = len(grid[0]), len(grid)
        left = (x > 0 and self._get_tyle_type_at(x - 1, y) == TileType.FLOOR)
        right = (x < gridWidth - 1 and self._get_tyle_type_at(x + 1, y) == TileType.FLOOR)
        if left and right: return FloorType.MID
        if not left and right: return FloorType.LEFT
        if left and not right: return FloorType.RIGHT
        return FloorType.FLOOR_SINGLE

    #todo - add more validations
    def _validate_loaded_level(self):
        tileCountHeight = len(self.grid)
        tileCountWidth = len(self.grid[0])
        if (self.tileCountWidth != tileCountWidth or self.tileCountHeight != tileCountHeight):
            self.hasError = True

    def handle_event(self, event):
        if self.levelComplete:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.levelComplete = False
                return "levelSelect"
            return None
            
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            return "levelSelect"
        
        if not self.hasError:
            for player in self.players:
                player.handle_event(event)

        return None
    
    def _on_level_complete(self):
        if self.levelComplete is False:
            elapsedTime = pygame.time.get_ticks() / 1000 - self.levelStartTime
            for player in self.players:
                    player.on_level_complete()

            totalPoints = 0
            for player in self.players:
                    totalPoints += player.points

            historyManager = LevelHistoryManager()
            historyManager.record_attempt(
                others.global_values.currentTeamName,
                self.levelName,
                elapsedTime,
                totalPoints
            )
        self.levelComplete = True

    def update(self, dt):
        if self.hasError:
            return
        
        bookRects = [book.rect for book in self.movableBooks]

        for book in self.movableBooks:
            book.update(dt, self.grid, self.players)

        anyButtonPressed = any(button.is_pressed(self.players) for button in self.buttons)
        for spray in self.sprays:
            spray.update(anyButtonPressed)

        for player in self.players:
            player.update(dt, self.grid, bookRects)
            for snack in self.snacks[:]:
                if snack.is_colliding_with(player.rect):
                    player.points += 1
                    self.snacks.remove(snack)
        if all(player.is_near_bed(self.grid) for player in self.players):
            self._on_level_complete()

    def draw_completion_popup(self, screen):
        popupWidth = 400
        popupHeight = 200
        popupRect = pygame.Rect(
            (self.screenWidth - popupWidth) // 2,
            (self.screenHeight - popupHeight) // 2,
            popupWidth,
            popupHeight
        )

        pygame.draw.rect(screen, pygame.Color("black"), popupRect)
        pygame.draw.rect(screen, pygame.Color("white"), popupRect, 4)
        messageText = self.fontMain.render("Level Complete!", True, pygame.Color("white"))
        screen.blit(messageText, (popupRect.centerx - messageText.get_width() // 2, popupRect.y + 30))
        hintText = self.fontSmall.render("Press any key to continue...", True, pygame.Color("gray"))
        screen.blit(hintText, (popupRect.centerx - hintText.get_width() // 2, popupRect.bottom - 50))

    def draw(self, screen):
        if self.hasError:
            text = self.fontMain.render("Error in level data", True, pygame.Color("red"))
            rect = text.get_rect(center=screen.get_rect().center)
            screen.blit(text, rect)
            return
        
        if self.grid:
            tileCountHeight = len(self.grid)
            tileCountWidth = len(self.grid[0])
            for y in range(tileCountHeight):
                for x in range(tileCountWidth):
                    tileType = self._get_tyle_type_at(x, y)
                    match tileType:
                        case TileType.FLOOR:
                            floorVariant = self._pick_floor_variant(self.grid, x, y)
                            screen.blit(self.assets.floorVariants[floorVariant], (x * tileSize, y * tileSize))
                        case TileType.RED_BED:
                            if(self._get_tyle_type_at(x + 1, y) == tileType):
                                bedImage = self.assets.beds[tileType]
                                screen.blit(bedImage, (x * tileSize, y * tileSize))
                        case TileType.BLUE_BED:
                            if(self._get_tyle_type_at(x + 1, y) == tileType):
                                bedImage = self.assets.beds[tileType]
                                screen.blit(bedImage, (x * tileSize, y * tileSize))


        for player in self.players:
            player.draw(screen, self.grid)

        if self.levelComplete:
            self.draw_completion_popup(screen)

        for book in self.movableBooks:
            book.draw(screen)

        for button in self.buttons:
            button.draw(screen, self.players)

        for spray in self.sprays:
            spray.draw(screen)

        for snack in self.snacks:
            snack.draw(screen)
