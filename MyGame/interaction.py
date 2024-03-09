from Sprites import *
from Map import *
from RayCasting import mapping
import math
import pygame
import random
from player import Player
from Draw import Drawing


def rayCastingNpcPlayer(npcX: float, npc_y: float, worldMap: set, playerPos: tuple) -> bool:
    """
    Эта функция проверяет, видит ли спрайт раньше стены.

    Args:
        npcX (float): Координата X NPC.
        npc_y (float): Координата Y NPC.
        worldMap (set): Множество координат стен на карте.
        playerPos (tuple): Кортеж с координатами игрока (X, Y).

    Returns:
        bool: True, если игрок видит спрайт раньше стены, иначе False.
    """
    ox, oy = playerPos
    xm, ym = mapping(ox, oy)
    deltaX, delta_y = ox - npcX, oy - npc_y
    curAngle = math.atan2(delta_y, deltaX)
    curAngle += math.pi

    sinA = math.sin(curAngle)
    sinA = sinA if sinA else 0.000001
    cosA = math.cos(curAngle)
    cosA = cosA if cosA else 0.000001

    x, dx = (xm + tile, 1) if cosA >= 0 else (xm, -1)
    for i in range(0, int(abs(deltaX)) // tile):
        depthV = (x - ox) / cosA
        yv = oy + depthV * sinA
        tileV = mapping(x + dx, yv)
        if tileV in worldMap:
            return False
        x += dx * tile

    y, dy = (ym + tile, 1) if sinA >= 0 else (ym, -1)
    for i in range(0, int(abs(delta_y)) // tile):
        depthH = (y - oy) / sinA
        xh = ox + depthH * cosA
        tileH = mapping(xh, y + dy)
        if tileH in worldMap:
            return False
        y += dy * tile
    return True


class Interaction:
    def __init__(self, player: Player, sprites: Sprites, drawing: Drawing):
        """
        Инициализирует класс взаимодействия.

        Args:
            player (Player): Объект игрока.
            sprites (Sprites): Экземпляр класса спрайтов.
            drawing (Drawing): Экземпляр класса отрисовки.
        """
        self.player = player
        self.sprites = sprites
        self.drawing = drawing
        self.painSound = pygame.mixer.Sound('sound/pain.wav')

    def getRandomPos(self) -> tuple:
        """
        Возвращает рандомную позицию для спрайта на координатах worldMap.

        Returns:
            tuple: Кортеж с рандомными координатами (X, Y).
        """
        playerX, playerY = int(self.player.x // tile), int(self.player.y // tile)

        freeSpaceCopy = freeSpace.copy()
        freeSpaceCopy.remove((playerX, playerY))

        x, y = random.choice(freeSpaceCopy)
        x, y = x + 0.5, y + 0.5

        dx, dy = playerX - x, playerY - y
        distanceToPlayer = math.sqrt(dx ** 2 + dy ** 2)

        if distanceToPlayer >= 3 and not rayCastingNpcPlayer(x * tile, y * tile, worldMap,
                                                             (self.player.x, self.player.y)):
            return x, y
        return self.getRandomPos()

    def interactionObjects(self) -> None:
        """
        Запускает действия спрайтов
        """
        if self.player.shot and self.drawing.shotAnimationTrigger:
            for obj in sorted(self.sprites.listOfObjects, key=lambda obj: obj.distanceToSprite):
                if obj.isOnFire[1]:
                    if obj.isDead != 'immortal' and not obj.isDead:
                        if rayCastingNpcPlayer(obj.x, obj.y,
                                               worldMap, self.player.pos):
                            self.painSound.play()
                            self.sprites.listOfObjects.append(
                                SpriteObject(self.getRandomPos(), (self.player.x, self.player.y)))
                            self.player.kills += 1
                            obj.isDead = True
                            obj.blocked = None
                            self.drawing.shotAnimationTrigger = False

    def npcAction(self) -> None:
        """
        Действия спрайта
        """
        for obj in self.sprites.listOfObjects:
            if not obj.isDead:
                self.npcMove(obj)
                self.npsAttack(obj)
                if rayCastingNpcPlayer(obj.x, obj.y,
                                       worldMap, self.player.pos):
                    obj.npcActionTrigger = True
                else:
                    obj.npcActionTrigger = False

    def npsAttack(self, obj: SpriteObject) -> None:
        """
        Атака спрайта на игрока

        :param obj: Объект спрайта
        """
        playerX, playerY = obj.pathway.playerPos
        dx, dy = playerX - obj.x, playerY - obj.y
        distanceToPlayer = math.sqrt(dx ** 2 + dy ** 2)
        if distanceToPlayer <= 60:
            self.player.isDead = True

    def npcMove(self, obj: SpriteObject) -> None:
        """
        Движение спрайта к игроку

        :param obj: Объект - спрайт
        """
        playerX, playerY = obj.pathway.playerPos
        dx, dy = playerX - obj.x, playerY - obj.y
        distanceToPlayer = math.sqrt(dx ** 2 + dy ** 2)
        if distanceToPlayer > 50 and len(obj.pathway.pathway) > 1:
            x, y = obj.pathway.pathway[obj.pathway.index]
            x, y = x * tile + tile // 2, y * tile + tile // 2
            dx, dy = x - obj.x, y - obj.y
            distanceToPoint = math.sqrt(dx ** 2 + dy ** 2)

            a = math.atan2(dy, dx)
            obj.x += obj.speed * math.cos(a)
            obj.y += obj.speed * math.sin(a)

            if distanceToPoint < obj.side // 2 and obj.pathway.index < len(obj.pathway.pathway) - 1:
                obj.pathway.index += 1

    def clearWorld(self) -> None:
        """
        Удаление всех спрайтов
        """
        deletedObjects = self.sprites.listOfObjects[:]
        [self.sprites.listOfObjects.remove(obj) for obj in deletedObjects if obj.delete]

    def playMusic(self) -> None:
        """
        Воспроизведение музыки
        """
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load('sound/theme.mp3')
        pygame.mixer.music.play(10)

    def checkWin(self) -> None:
        """
        Проверка на победу и проигрыш
        """
        if self.player.kills >= 32:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('sound/win.mp3')
            pygame.mixer.music.play()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                self.drawing.win()
        elif self.player.isDead:
            pygame.mixer.music.stop()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                self.drawing.losing()
