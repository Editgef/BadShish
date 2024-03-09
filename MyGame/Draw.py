from Map import miniMap
from RayCasting import *
from collections import deque
from random import randrange
import sys


class Drawing:
    def __init__(self, screen: pygame.Surface, screenMap: pygame.Surface, player: Player,
                 clock: pygame.time.Clock) -> None:
        """
         Инициализирует класс Drawing.

         Args:
             screen (pygame.Surface): Поверхность экрана Pygame.
             screenMap (pygame.Surface): Поверхность для миникарты Pygame.
             player (player): Объект игрока.
             clock (pygame.time.Clock): Часы Pygame.
         """
        self.screen = screen
        self.screenMap = screenMap
        self.player = player
        self.clock = clock
        self.font = pygame.font.SysFont("Arial", 36, bold=True)
        self.fontWin = pygame.font.Font('font/font.ttf', 144)
        self.textures = {1: pygame.image.load('img/wall3.png').convert(),
                         'S': pygame.image.load('img/sky2.png').convert()
                         }

        self.menuTrigger = True
        self.menuPicture = pygame.image.load('img/bg.jpg').convert()

        self.weaponBaseSprite = pygame.image.load("sprites/weapons/shotgun/base/0.png").convert_alpha()
        self.weaponShotAnimation = deque([pygame.image.load(f"sprites/weapons/shotgun/shot/{i}.png").convert_alpha()
                                          for i in range(20)])
        self.weaponRect = self.weaponBaseSprite.get_rect()
        self.weaponPos = (halfWidth - self.weaponRect.width // 2, height - self.weaponRect.height)
        self.shotLength = len(self.weaponShotAnimation)
        self.shotLengthCount = 0
        self.shotAnimationSpeed = 3
        self.shotAnimationCount = 0
        self.shotAnimationTrigger = True
        self.shotSound = pygame.mixer.Sound('sound/shotgun.wav')

        self.sfx = deque([pygame.image.load(f'sprites/weapons/sfx/{i}.png').convert_alpha() for i in range(9)])
        self.sfxLengthCount = 0
        self.sfxLength = len(self.sfx)

    def backGround(self, angle: int) -> None:
        """
        Отрисовывает небо и пол.

        :param angle: Угол обзора игрока
        """
        skyOffset = -10 * math.degrees(angle) % width
        self.screen.blit(self.textures['S'], (skyOffset, 0))
        self.screen.blit(self.textures['S'], (skyOffset - width, 0))
        self.screen.blit(self.textures['S'], (skyOffset + width, 0))
        pygame.draw.rect(self.screen, darkGray, (0, halfHeight, width, halfHeight))

    def world(self, worldObjects: list) -> None:
        """
        Отрисовывает объекты мира.

        :param worldObjects: Список объектов для отрисовки
        """
        for obj in sorted(worldObjects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, objectPos = obj
                self.screen.blit(object, objectPos)

    def fps(self, clock: pygame.time.Clock) -> None:
        """
        Прорисовывает счетчик FPS.

        Args:
            clock (pygame.time.Clock): Экземпляр объекта Clock для измерения FPS.
        """
        displayFPS = str(int(clock.get_fps()))
        render = self.font.render(displayFPS, 0, red)
        self.screen.blit(render, FPSPos)

    def kills(self, kills) -> None:
        render = self.font.render(f"KIllS {kills}", 0, red)
        self.screen.blit(render, (0, 0))

    def minMap(self, player: Player) -> None:
        """
        Отрисовывает миникарту на экране.

        Args:
            player (Player): Объект игрока.

        Returns:
            None
        """
        self.screenMap.fill(black)
        mapX, mapY = int(player.x / mapScale), int(player.y / mapScale)
        pygame.draw.line(self.screenMap, yellow, (mapX, mapY), (mapX + 12 * math.cos(player.angle),
                                                                mapY + 12 * math.sin(player.angle)), 2)
        pygame.draw.circle(self.screenMap, red, (int(mapX), int(mapY)), 5)
        for obj in player.sprites.listOfObjects:
            if obj.isDead:
                pygame.draw.circle(self.screenMap, green, (int(obj.x / mapScale), int(obj.y / mapScale)), 5)
            else:
                pygame.draw.circle(self.screenMap, red, (int(obj.x / mapScale), int(obj.y / mapScale)), 5)
        for x, y in miniMap:
            pygame.draw.rect(self.screenMap, green, (x, y, mapTile, mapTile))
        self.screen.blit(self.screenMap, mapPos)

    def playerWeapon(self, shots: list) -> None:
        """
        Отрисовывает оружие игрока и анимацию выстрела.

        Args:
            shots (list): Список выстрелов игрока.
        """
        if self.player.shot:
            if not self.shotLengthCount:
                self.shotSound.play()
            self.shotProjection = min(shots)[1] // 2
            self.bulletSfx()
            shotSprite = self.weaponShotAnimation[0]
            self.screen.blit(shotSprite, self.weaponPos)
            self.shotAnimationCount += 1
            if self.shotAnimationCount == self.shotAnimationSpeed:
                self.weaponShotAnimation.rotate(-1)
                self.shotAnimationCount = 0
                self.shotLengthCount += 1
                self.shotAnimationTrigger = False
            if self.shotLengthCount == self.shotLength:
                self.player.shot = False
                self.shotLengthCount = 0
                self.sfxLengthCount = 0
                self.shotAnimationTrigger = True
        else:
            self.screen.blit(self.weaponBaseSprite, self.weaponPos)

    def bulletSfx(self) -> None:
        """
        Проигрывает анимацию выстрела.
        """
        if self.sfxLengthCount < self.sfxLength:
            sfx = pygame.transform.scale(self.sfx[0], (self.shotProjection, self.shotProjection))
            sfxRect = sfx.get_rect()
            self.screen.blit(sfx, (halfWidth - sfxRect.w // 2, halfHeight - sfxRect.h // 2))
            self.sfxLengthCount += 1
            self.sfx.rotate(-1)

    def win(self) -> None:
        """
        Отрисовывает экран победы.

        Returns:
            None
        """
        render = self.fontWin.render('YOU WIN!!!', 1, (randrange(40, 120), 0, 0))
        rect = pygame.Rect(0, 0, 1000, 300)
        rect.center = halfWidth, halfHeight
        pygame.draw.rect(self.screen, black, rect, border_radius=50)
        self.screen.blit(render, (rect.centerx - 430, rect.centery - 140))
        pygame.display.flip()
        self.clock.tick(15)

    def losing(self) -> None:
        """
        Отрисовывает экран проигрыша.

        Returns:
            None
        """
        render = self.fontWin.render('you lost.', 1, (randrange(40, 120), 0, 0))
        rect = pygame.Rect(0, 0, 1000, 300)
        rect.center = halfWidth, halfHeight
        pygame.draw.rect(self.screen, black, rect, border_radius=50)
        self.screen.blit(render, (rect.centerx - 430, rect.centery - 140))
        pygame.display.flip()
        self.clock.tick(15)

    def menu(self) -> None:
        """
        Отрисовывает меню.
        """
        x = 0
        buttonFont = pygame.font.Font('font/font.ttf', 72)
        labelFont = pygame.font.Font('font/font1.otf', 400)
        start = buttonFont.render('START', 1, pygame.Color('lightgray'))
        buttonStart = pygame.Rect(0, 0, 400, 150)
        buttonStart.center = halfWidth, halfHeight
        exit = buttonFont.render('EXIT', 1, pygame.Color('lightgray'))
        buttonExit = pygame.Rect(0, 0, 400, 150)
        buttonExit.center = halfWidth, halfHeight + 200

        while self.menuTrigger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.menuPicture, (0, 0), (x % width, halfHeight, width, height))
            x += 1

            pygame.draw.rect(self.screen, black, buttonStart, border_radius=25, width=10)
            self.screen.blit(start, (buttonStart.centerx - 130, buttonStart.centery - 70))

            pygame.draw.rect(self.screen, black, buttonExit, border_radius=25, width=10)
            self.screen.blit(exit, (buttonExit.centerx - 85, buttonExit.centery - 70))

            color = randrange(40)
            label = labelFont.render('DOOMPy', 1, (color, color, color))
            self.screen.blit(label, (15, -30))

            mousePos = pygame.mouse.get_pos()
            mouseClick = pygame.mouse.get_pressed()
            if buttonStart.collidepoint(mousePos):
                pygame.draw.rect(self.screen, black, buttonStart, border_radius=25)
                self.screen.blit(start, (buttonStart.centerx - 130, buttonStart.centery - 70))
                if mouseClick[0]:
                    self.menuTrigger = False
            elif buttonExit.collidepoint(mousePos):
                pygame.draw.rect(self.screen, black, buttonExit, border_radius=25)
                self.screen.blit(exit, (buttonExit.centerx - 85, buttonExit.centery - 70))
                if mouseClick[0]:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(20)
