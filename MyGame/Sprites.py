from Map import *
from Bfs import Pathway


class Sprites:
    def __init__(self) -> None:
        """
        Инициализирует объекты спрайтов.
        """
        self.listOfObjects = [
            SpriteObject((7.5, 1.5), playerPos),
            SpriteObject((1.5, 4.5), playerPos),
        ]

    @property
    def spriteShot(self) -> tuple:
        """
        Возвращает информацию о спрайте, находящемся под огнём.

        Returns:
            tuple: Кортеж с информацией о спрайте (расстояние до спрайта, индекс спрайта),
                   если таковой имеется, иначе (float('inf'), 0).
        """
        return min([obj.isOnFire for obj in self.listOfObjects], default=(float('inf'), 0))


class SpriteObject:
    def __init__(self, pos: tuple, playerPos: tuple) -> None:
        """
        Инициализирует класс Sprites с списком экземпляров SpriteObject.

        Args:
            pos (tuple): Начальная позиция спрайта в виде кортежа (X, Y).
            playerPos (tuple): Позиция игрока в виде кортежа (X, Y).
        """
        self.object = [pygame.image.load("sprites/badshish.png").convert_alpha()]
        self.viewingAngles = False
        self.shift = 0.0
        self.scale = (1.1, 1.1)
        self.animation = []
        self.isDead = None
        self.animationSpeed = 10
        self.blocked = True
        self.x, self.y = pos[0] * tile, pos[1] * tile
        self.side = 50
        self.pathway = Pathway(self, playerPos)
        self.speed = 4
        self.delete = False

    @property
    def isOnFire(self) -> tuple:
        """
        Возвращает статус огня ближайшего спрайта.
        Если попал, возвращает расстояние и высоту проекции, иначе возвращает бесконечность и None.

        Returns:
            tuple: Кортеж с информацией о статусе огня спрайта.
                   Если попадание произошло, возвращается (расстояние до спрайта, высота проекции),
                   иначе возвращается (бесконечность, None).
        """
        if centerRay - self.side // 2 < self.currentRay < centerRay + self.side // 2 and self.blocked:
            return self.distanceToSprite, self.projHeight
        return float('inf'), None

    @property
    def pos(self) -> tuple:
        """
        Возвращает координаты спрайта.

        Returns:
            tuple: Кортеж с координатами спрайта (X, Y).
        """

        return self.x, self.y

    def objectLocate(self, player) -> tuple:
        """
        Инициализирует экземпляр SpriteObject.

        Args:
            player (Player): Объект игрока.

        Returns:
            tuple: Кортеж с информацией о спрайте. Если спрайт не виден, возвращается (False,).
                   Иначе возвращается кортеж с расстоянием до спрайта, изображением спрайта и его позицией.
        """
        dx, dy = self.x - player.x, self.y - player.y
        self.distanceToSprite = math.sqrt(dx ** 2 + dy ** 2)

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += doublePi
        self.theta -= 1.4 * gamma

        delta_rays = int(gamma / deltaAngle)
        self.currentRay = centerRay + delta_rays
        self.distanceToSprite *= math.cos(halfFov - self.currentRay * deltaAngle)

        fake_ray = self.currentRay + fakeRays
        if 0 <= fake_ray <= fakeRaysRange and self.distanceToSprite > 30:
            self.projHeight = min(int(projCoeff / self.distanceToSprite), height)
            spriteWidth = int(self.projHeight * self.scale[0])
            spriteHeight = int(self.projHeight * self.scale[1])
            halfSpriteWidth = spriteWidth // 2
            halfSpriteHeight = spriteHeight // 2
            shift = halfSpriteHeight * self.shift

            if self.isDead and self.isDead != 'immortal':
                return (False,)
            else:
                spriteObject = self.object[0]

            spritePos = (self.currentRay * scale - halfSpriteWidth, halfHeight - halfSpriteHeight + shift)
            sprite = pygame.transform.scale(spriteObject, (spriteWidth, spriteHeight))
            return (self.distanceToSprite, sprite, spritePos)
        else:
            return (False,)
