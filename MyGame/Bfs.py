from collections import deque
from Settings import *
from Map import map, graph


def findWay(x: int, y: int, toX: int, toY: int) -> list:
    """
    Возвращает список координат, по которым спрайт может прийти к игроку.

    Args:
        x (int): Координата X спрайта.
        y (int): Координата Y спрайта.
        toX (int): Координата X цели (игрока).
        toY (int): Координата Y цели (игрока).

    Returns:
        list: Список координат пути к игроку.
    """
    x, y, toX, toY = int(x / tile), int(y / tile), int(toX / tile), int(toY / tile)
    start = (x, y)
    goal = start
    visited = {start: None}
    mouse_pos = toX, toY

    if mouse_pos and not map[toY][toX]:
        queue, visited = bfs(start, mouse_pos)
        goal = mouse_pos
    answer = []

    path_head, path_segment = goal, goal
    while path_segment and path_segment in visited:
        answer.append((path_segment[0], path_segment[1]))
        path_segment = visited[path_segment]
    return answer[-1::-1]


def bfs(start: tuple, goal: tuple) -> tuple:
    """
    Выполняет поиск в ширину от стартовой точки до цели.

    Args:
        start (tuple): Начальная точка.
        goal (tuple): Целевая точка.

    Returns:
        tuple: Очередь пути и словарь посещенных точек.
    """
    queue = deque([start])
    visited = {start: None}

    while queue:
        cur_node = queue.popleft()
        if cur_node == goal:
            break
        next_nodes = graph[cur_node]

        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node
    return queue, visited


class Pathway:
    def __init__(self, obj, playerPos: tuple) -> None:
        """
        Инициализирует экземпляр класса Pathway.

        Args:
            sprites (SpriteObject): Экземпляр спрайта.
            playerPos (tuple): Позиция игрока (X, Y).
        """
        self.index = 1
        self.playerPos = playerPos
        self.obj = obj
        self.pathway = findWay(obj.x, obj.y, *playerPos)

    def update(self, newPlayerPos: tuple) -> None:
        """
        Обновляет путь.

        Args:
            newPlayerPos (tuple): Новая позиция игрока (X, Y).
        """
        if (self.obj.x // tile, self.obj.y // tile) in graph:
            self.index = 1
            self.playerPos = newPlayerPos
            self.pathway = findWay(self.obj.x, self.obj.y, *newPlayerPos)
