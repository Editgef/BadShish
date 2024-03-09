import pygame
from Settings import *
from Map import worldMap, mapWidth, mapHeight
from player import Player

def mapping(ox: float, oy: float) -> tuple:
    """
    Возвращает отображенные координаты на основе размера tile.

    Args:
        ox (float): Координата X.
        oy (float): Координата Y.

    Returns:
        tuple: Кортеж отображенных координат (X, Y).
    """
    return int(ox // tile) * tile, int(oy // tile) * tile


def rayCasting(playerPos: tuple, playerAngle: float, worldMap: dict) -> list:
    """
    Выполняет лучевое отображение для определения стен и их текстур.

    Args:
        playerPos (tuple): Кортеж с координатами игрока (X, Y).
        playerAngle (float): Угол игрока в радианах.
        worldMap (dict): Словарь с координатами стен.

    Returns:
        list: Список отображенных стен с глубиной, смещением, проекционной высотой и текстурой.
    """
    castedWalls = []
    ox, oy = playerPos
    textureV, textureH = 1, 1
    xm, ym = mapping(ox, oy)
    curAngle = playerAngle - halfFov
    for ray in range(numRays):
        sinA = math.sin(curAngle)
        sinA = sinA if sinA else 0.000001
        cosA = math.cos(curAngle)
        cosA = cosA if cosA else 0.000001


        x, dx = (xm + tile, 1) if cosA >= 0 else (xm, -1)
        for i in range(0, mapWidth, tile):
            depthV = (x - ox) / cosA
            yv = oy + depthV * sinA
            tileV = mapping(x + dx, yv)
            if tileV in worldMap:
                textureV = worldMap[tileV]
                break
            x += dx * tile



        y, dy = (ym + tile, 1) if sinA >= 0 else (ym, -1)
        for i in range(0, mapHeight, tile):
            depthH = (y - oy) / sinA
            xh = ox + depthH * cosA
            tileH = mapping(xh, y + dy)
            if tileH in worldMap:
                textureH = worldMap[tileH]
                break
            y += dy * tile

        depth, offset, texture = (depthV, yv, textureV) if depthV < depthH else (depthH, xh, textureH)
        offset = int(offset) % tile
        depth *= math.cos(playerAngle - curAngle)
        depth = max(depth, 0.00001)
        projHeight = int(projCoeff / depth)

        castedWalls.append((depth, offset, projHeight, texture))
        curAngle += deltaAngle
    return castedWalls
def rayCastingWalls(player: Player, textures: dict) -> tuple:
    """
    Выполняет лучевое отображение для определения стен и их текстур.

    Args:
        player (player): Объект игрока.
        textures (dict): Словарь текстур для стен.

    Returns:
        tuple: Кортеж, содержащий список информации о стенах и координаты попадания луча на стену.
    """
    castedWalls = rayCasting(player.pos, player.angle, worldMap)
    wallShot = castedWalls[centerRay][0], castedWalls[centerRay][2]
    walls = []
    for ray, castedValues in enumerate(castedWalls):
        depth, offset, projHeight, texture = castedValues
        if projHeight > height:
            coeff = projHeight / height
            textureHeight1 = textureHeight / coeff

            wallColumn = textures[texture].subsurface(offset * textureScale,
                                                       halfTextureHeight - textureHeight1 // 2,
                                                       textureScale, textureHeight1)
            wallColumn = pygame.transform.scale(wallColumn, (scale, height))
            wallPos = (ray * scale, 0)
        else:
            wallColumn = textures[texture].subsurface(offset * textureScale, 0, textureScale, textureHeight)
            wallColumn = pygame.transform.scale(wallColumn, (scale, projHeight))
            wallPos = (ray * scale, halfHeight - projHeight // 2)

        walls.append((depth, wallColumn, wallPos))
    return walls, wallShot
