import math

# Размеры экрана
width = 1200
height = 800
halfWidth = width // 2
halfHeight = height // 2
pentaHeight = 5 * height
doubleHeight = 2 * height

# Параметры игрового цикла
FPS = 60
tile = 100
FPSPos = (width - 65, 5)

# Параметры миникарты
miniMapScale = 5
miniMapRes = (width // miniMapScale, height // miniMapScale)
mapScale = 2 * miniMapScale
mapTile = int(tile / mapScale)
mapPos = 0, height - height // miniMapScale

# Параметры лучевого отображения
fov = math.pi / 3
halfFov = fov / 2
numRays = 300
maxDepth = 800
deltaAngle = fov / numRays
dist = numRays / (2 * math.tan(halfFov))
projCoeff = 3 * dist * tile
scale = width // numRays

# Другие параметры для лучевого отображения
doublePi = 2 * math.pi
centerRay = numRays // 2 - 1
fakeRays = 100
fakeRaysRange = numRays - 1 + 2 * fakeRays

# Параметры текстур
textureWidth = 1200
textureHeight = 1200
halfTextureHeight = textureHeight // 2
textureScale = textureWidth // tile

# Начальные параметры игрока
playerPos = (2250, 1450)
playerAngle = 0
playerSpeed = 7

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
red = (220, 0, 0)
green = (0, 80, 0)
blue = (0, 0, 220)
darkGray = (110, 110, 110)
purple = (120, 0, 120)
skyBlue = (135, 206, 235)
yellow = (220, 220, 0)
