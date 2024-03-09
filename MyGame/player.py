import pygame.mouse
from Map import *
import math
from Sprites import Sprites


class Player:

    def __init__(self, sprites: Sprites) -> None:
        """
     Инициализирует игрока.

     Args:
         sprites (Список объектов): Спрайты игрока.

     Attributes:
         x (float): Координата x игрока.
         y (float): Координата y игрока.
         sprites (Список объектов): Спрайты игрока.
         angle (float): Угол поворота игрока.
         side (int): Длина стороны игрока.
         rect (pygame.Rect): Прямоугольник, представляющий игрока.
         sensitivity (float): Чувствительность игрока.
         shot (bool): Флаг выстрела.
         isDead (bool): Флаг состояния игрока (мертв/жив).
    """
        self.x, self.y = playerPos
        self.sprites = sprites
        self.angle = playerAngle
        self.side = 50
        self.rect = pygame.Rect(*playerPos, self.side, self.side)
        self.sensitivity = 0.004
        self.shot = False
        self.isDead = False
        self.kills = 0

    @property
    def pos(self) -> tuple:
        """
        Возвращает текущие координаты игрока.

        Returns:
            tuple: Кортеж с координатами x и y игрока.
        """
        return (self.x, self.y)

    @property
    def collisionList(self) -> list:
        """
        Возвращает список прямоугольников, с которыми может происходить коллизия.

        Returns:
            list: Список прямоугольников, представляющих объекты, с которыми может произойти коллизия.
        """
        return collisionsWalls + [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  self.sprites.listOfObjects if obj.blocked]

    def detectCollision(self, dx: int, dy: int) -> None:
        """
        Oбнаруживает коллизии и корректирует движение игрока.

        Args:
            dx (int): Изменение координаты X.
            dy (int): Изменение координаты Y.
        """
        nextRect = self.rect.copy()
        nextRect.move(dx, dy)
        hitIndexes = nextRect.collidelistall(self.collisionList)
        if len(hitIndexes):
            deltaX, deltaY = 0, 0
            for hitIndex in hitIndexes:
                hitRect = self.collisionList[hitIndex]
                if dx > 0:
                    deltaX += nextRect.right - hitRect.left
                else:
                    deltaX += hitRect.right - nextRect.left
                if dy > 0:
                    deltaY += nextRect.bottom - hitRect.top
                else:
                    deltaY += hitRect.bottom - nextRect.top
            if abs(deltaX - deltaY) < 10:
                dx, dy = 0, 0
            elif deltaX > deltaY:
                dy = 0
            elif deltaY > deltaX:
                dx = 0
        self.x += dx
        self.y += dy
        for obj in self.sprites.listOfObjects:
            obj.pathway.update((self.x, self.y))

    def movement(self):
        """
        Обработка движения игрока.
        """
        self.keysControl()
        self.mouseControl()
        self.angle %= doublePi

    def keysControl(self):
        """
        Управление игроком с помощью клавиш.
        """
        sinA = math.sin(self.angle)
        cosA = math.cos(self.angle)
        self.rect.center = self.x, self.y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()
        if keys[pygame.K_w]:
            dx = playerSpeed * cosA
            dy = playerSpeed * sinA
            self.detectCollision(dx, dy)
        if keys[pygame.K_s]:
            dx = -playerSpeed * cosA
            dy = -playerSpeed * sinA
            self.detectCollision(dx, dy)
        if keys[pygame.K_a]:
            dx = playerSpeed * sinA
            dy = -playerSpeed * cosA
            self.detectCollision(dx, dy)
        if keys[pygame.K_d]:
            dx = -playerSpeed * sinA
            dy = playerSpeed * cosA
            self.detectCollision(dx, dy)

        if keys[pygame.K_q]:
            self.angle -= 0.02
        if keys[pygame.K_e]:
            self.angle += 0.02
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.shot:
                    self.shot = True

    def mouseControl(self) -> None:
        """
        Управление игроком с помощью мыши.
        """
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - halfWidth
            pygame.mouse.set_pos((halfWidth, halfHeight))
            self.angle += difference * self.sensitivity
