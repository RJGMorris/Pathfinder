# Pathfinder using pygame

import pygame

pygame.init()

# Main window setup
SQUARES = 31
SPACING = 15
WIDTH = SPACING * SQUARES
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinder by Rory")
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WIGHT = (255, 255, 255)


# Classes
class Node(object):

    def __init__(self, start=True, drag=False):
        self.start = start
        self.drag = drag
        if start:
            self.position = [(SQUARES//4) * SPACING, (SQUARES//4) * SPACING]
        else:
            self.position = [(SQUARES*3//4) * SPACING, (SQUARES*3//4) * SPACING]

    def draw_node(self):
        pygame.draw.rect(win, BLUE, (self.position[0] + 1, self.position[1] + 1, SPACING - 1, SPACING - 1))

    def on_click(self, mouse_event):

        if mouse_event.type == pygame.MOUSEBUTTONDOWN:
            x, y = (event.pos[0] // SPACING) * SPACING, (event.pos[1] // SPACING) * SPACING
            if x == self.position[0] and y == self.position[1]:
                self.drag = True

        elif mouse_event.type == pygame.MOUSEMOTION:
            if self.drag:
                if main_grid.grid[event.pos[0] // SPACING][event.pos[1] // SPACING] == 0:
                    self.position[0] = (event.pos[0] // SPACING) * SPACING
                    self.position[1] = (event.pos[1] // SPACING) * SPACING
                    win.fill(WIGHT)
                    redraw_game_window()

        elif mouse_event.type == pygame.MOUSEBUTTONUP:
            if main_grid.done:
                main_grid.draw_path()
            self.drag = False


class Grid(object):

    def __init__(self, grid):
        self.grid = grid
        self.seen_set = []
        self.neighbour_set = []
        self.current_node = []
        self.path = []
        self.walls = []
        self.drawing = False
        self.done = False

    def find_path(self, grid):
        self.current_node = find_start_node(grid)
        self.seen_set = []
        self.neighbour_set = []
        if self.path_found(grid, self.current_node):
            self.current_node = self.seen_set[len(self.seen_set) - 1]
            if self.done:
                self.draw_sets(self.current_node)
            if backtrack(self.seen_set, self.current_node):
                return self.seen_set
            else:
                return 0

    def draw_path(self):
        win.fill(WIGHT)
        self.path = self.find_path(self.grid)
        if self.path:
            self.path.reverse()
            for node in self.path:
                pygame.draw.rect(win, BLUE, (node[0] * SPACING, node[1] * SPACING, SPACING, SPACING))
                redraw_game_window()
                if not self.done:
                    wait(30)
            self.done = True
        else:
            win.fill(WIGHT)
            redraw_game_window()

    def path_found(self, grid, current_node):
        self.seen_set.append(current_node)
        if is_done(grid, self.seen_set):
            return True
        if not in_neighbour_set(current_node, self.neighbour_set, self.seen_set):
            self.neighbour_set.append([current_node[0] + 1, current_node[1], current_node[2] + 1])
        if not in_neighbour_set1(current_node, self.neighbour_set, self.seen_set):
            self.neighbour_set.append([current_node[0] - 1, current_node[1], current_node[2] + 1])
        if not in_neighbour_set2(current_node, self.neighbour_set, self.seen_set):
            self.neighbour_set.append([current_node[0], current_node[1] + 1, current_node[2] + 1])
        if not in_neighbour_set3(current_node, self.neighbour_set, self.seen_set):
            self.neighbour_set.append([current_node[0], current_node[1] - 1, current_node[2] + 1])
        if not self.neighbour_set:
            return False
        current_node = self.neighbour_set[0]
        for node in self.neighbour_set:
            if node[2] < current_node[2]:
                current_node = node
        self.neighbour_set.remove(current_node)
        if not self.done:
            self.draw_sets(current_node)
            wait(5)
        if self.path_found(grid, current_node):
            return True
        return False

    def draw_sets(self, current_node):
        for node in self.seen_set:
            pygame.draw.rect(win, YELLOW, (node[0] * SPACING, node[1] * SPACING, SPACING, SPACING))
        for node in self.neighbour_set:
            pygame.draw.rect(win, RED, (node[0] * SPACING, node[1] * SPACING, SPACING, SPACING))
        pygame.draw.rect(win, BLUE, (current_node[0] * SPACING, current_node[1] * SPACING, SPACING, SPACING))
        redraw_game_window()

    def draw_wall(self, mouse_event):
        if mouse_event.type == pygame.MOUSEBUTTONDOWN:
            x, y = (mouse_event.pos[0] // SPACING) * SPACING, (mouse_event.pos[1] // SPACING) * SPACING
            if not ((x == start_node.position[0] and y == start_node.position[1])
                    or (x == end_node.position[0] and y == end_node.position[1])):
                self.drawing = True

        elif mouse_event.type == pygame.MOUSEMOTION:
            if self.drawing:
                x, y = (mouse_event.pos[0] // SPACING), (mouse_event.pos[1] // SPACING)
                if [x, y] not in self.walls:
                    self.walls.append([mouse_event.pos[0] // SPACING, mouse_event.pos[1] // SPACING])
                    pygame.draw.rect(win, BLACK, (x * SPACING, y * SPACING, SPACING, SPACING))
                redraw_game_window()

        elif mouse_event.type == pygame.MOUSEBUTTONUP:
            self.drawing = False

    def reset(self):
        self.seen_set = []
        self.neighbour_set = []
        self.current_node = []
        self.path = []
        self.walls = []
        self.done = False


# Functions
def redraw_game_window():
    draw_grid()
    start_node.draw_node()
    end_node.draw_node()
    for wall in main_grid.walls:
        pygame.draw.rect(win, BLACK, (wall[0] * SPACING, wall[1] * SPACING, SPACING, SPACING))
    pygame.display.update()


def draw_grid():
    for line in range(0, WIDTH, SPACING):
        pygame.draw.line(win, BLACK, (line, 0), (line, WIDTH))
        pygame.draw.line(win, BLACK, (0, line), (WIDTH, line))


def create_grid():
    grid = []
    for r in range(SQUARES):
        grid_rows = []
        for c in range(SQUARES):
            grid_rows.append(0)
        grid.append(grid_rows)
    return grid


def find_start_node(grid):
    for x in range(SQUARES):
        for y in range(SQUARES):
            if grid[x][y] == 1:
                return [x, y, 0]


def is_done(grid, seen_set):
    for node in seen_set:
        if grid[node[0]][node[1]] == 2:
            return True
    return False


def in_neighbour_set(current_node, neighbour_set, seen_set):
    x, y = current_node[0] + 1, current_node[1]
    if SQUARES - 1 < x or x < 0:
        return True
    if main_grid.grid[x][y] == 3:
        return True
    for node in neighbour_set:
        if x == node[0] and y == node[1]:
            return True
    for node in seen_set:
        if x == node[0] and y == node[1]:
            return True
    return False


def in_neighbour_set1(current_node, neighbour_set, seen_set):
    x, y = current_node[0] - 1, current_node[1]
    if SQUARES - 1 < current_node[0] - 1 or current_node[0] - 1 < 0:
        return True
    if main_grid.grid[x][y] == 3:
        return True
    for node in neighbour_set:
        if current_node[0] - 1 == node[0] and current_node[1] == node[1]:
            return True
    for node in seen_set:
        if current_node[0] - 1 == node[0] and current_node[1] == node[1]:
            return True
    return False


def in_neighbour_set2(current_node, neighbour_set, seen_set):
    x, y = current_node[0], current_node[1] + 1
    if SQUARES - 1 < current_node[1] + 1 or current_node[1] + 1 < 0:
        return True
    if main_grid.grid[x][y] == 3:
        return True
    for node in neighbour_set:
        if current_node[0] == node[0] and current_node[1] + 1 == node[1]:
            return True
    for node in seen_set:
        if current_node[0] == node[0] and current_node[1] + 1 == node[1]:
            return True
    return False


def in_neighbour_set3(current_node, neighbour_set, seen_set):
    x, y = current_node[0], current_node[1] - 1
    if SQUARES - 1 < current_node[1] - 1 or current_node[1] - 1 < 0:
        return True
    if main_grid.grid[x][y] == 3:
        return True
    for node in neighbour_set:
        if current_node[0] == node[0] and current_node[1] - 1 == node[1]:
            return True
    for node in seen_set:
        if current_node[0] == node[0] and current_node[1] - 1 == node[1]:
            return True
    return False


def backtrack(seen_set, current_node):
    if current_node[2] == 0:
        return True
    temp = [node for node in seen_set]
    for node in temp:
        if node[2] == current_node[2] and node != current_node:
            seen_set.remove(node)
    for node in seen_set:
        if node[2] == (current_node[2] - 1):
            if (((node[0] == current_node[0] + 1 or node[0] == current_node[0] - 1) and node[1] == current_node[1]) or
                    ((node[1] == current_node[1] + 1 or node[1] == current_node[1] - 1) and node[0] == current_node[
                        0])):
                current_node = node
                if backtrack(seen_set, current_node):
                    return True
    return False


def wait(t):
    global run
    i = 0
    while i < t:
        pygame.time.wait(1)
        i += 1
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                run = False
                pygame.quit()


# Main loop setup
run = True
draw = False
main_grid = Grid(create_grid())
start_node = Node(True)
end_node = Node(False)
win.fill(WIGHT)

# Main loop
while run:

    # Set grid to 0
    for i in main_grid.grid:
        for j in range(SQUARES):
            i[j] = 0

    # Set node to 1
    main_grid.grid[start_node.position[0] // SPACING][start_node.position[1] // SPACING] = 1
    main_grid.grid[end_node.position[0] // SPACING][end_node.position[1] // SPACING] = 2

    # Set walls to 3
    for walls in main_grid.walls:
        main_grid.grid[walls[0]][walls[1]] = 3

    redraw_game_window()

    # Check for event - quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Dragging the nodes
        start_node.on_click(event)
        end_node.on_click(event)

        # Drawing walls
        main_grid.draw_wall(event)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        main_grid.done = False
        main_grid.draw_path()

    if keys[pygame.K_BACKSPACE]:
        main_grid.reset()
        win.fill(WIGHT)
        redraw_game_window()

pygame.quit()
