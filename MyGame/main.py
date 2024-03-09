from player import Player
from Draw import Drawing
from Sprites import *
from RayCasting import rayCastingWalls
from interaction import Interaction

pygame.init()
screen = pygame.display.set_mode((width, height))
screenMap = pygame.Surface(miniMapRes)

sprites = Sprites()
clock = pygame.time.Clock()
player = Player(sprites)
drawing = Drawing(screen, screenMap, player, clock)
interaction = Interaction(player, sprites, drawing)

drawing.menu()
pygame.mouse.set_visible(False)
interaction.playMusic()

while True:
    # Обработка движения игрока и взаимодействия с объектами
    player.movement()

    # Отрисовка фона и стен
    drawing.backGround(player.angle)
    walls, wallShot = rayCastingWalls(player, drawing.textures)
    drawing.world(walls + [obj.objectLocate(player) for obj in sprites.listOfObjects])

    # Отрисовка информации о FPS и миникарты
    drawing.fps(clock)
    drawing.kills(player.kills)
    drawing.minMap(player)

    # Отрисовка оружия и взаимодействия с объектами
    drawing.playerWeapon([wallShot, sprites.spriteShot])
    interaction.interactionObjects()
    interaction.npcAction()
    interaction.clearWorld()
    interaction.checkWin()

    pygame.display.flip()
    clock.tick(FPS)
