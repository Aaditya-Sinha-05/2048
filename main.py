import pygame
import random
import math

pygame.init()

# variables

FPS = 60
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 4, 4
RECT_WIDTH, RECT_HEIGHT  = WIDTH // COLS, HEIGHT // ROWS
OUTLINE_COLOR = (187,173,160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)
FONT = pygame.font.SysFont("comicsans", 60, bold=True)
MOVE_VEL = 20 #speed of tiles

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

class Tile:
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80)
    ]

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT

    def get_color(self):
        index = int(math.log2(self.value))
        color = self.COLORS[index - 1] #to get index starting from 0
        return color

    def draw_tile(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        text = FONT.render(str(self.value), 1, FONT_COLOR)
        window.blit(
            text,
            (
                    self.x + (RECT_WIDTH / 2 - text.get_width() / 2), #get center of tile, then get center of number and subtract/add it to get START/END axis
                    self.y + (RECT_HEIGHT / 2 - text.get_height() / 2)  #get center of tile, then get center of number and subtract/add it to get START/END axis
            ),
        )

    def set_pos(self):
        pass

    def move_tile(self, delta):
        pass

def get_random_position(all_tiles):
    while True:
        row, col = random.randint(0, 3), random.randint(0, 3)
        if str(row) + str(col) in all_tiles:
            row, col = random.randint(0, 3), random.randint(0, 3)
        else:
            return row, col


def generate_tiles():
    all_tiles = {}
    for _ in range(2):
        row, col = get_random_position(all_tiles)
        all_tiles[f"{row}{col}"] = Tile(2, row, col)

    return all_tiles


def draw_grid(window):

    for i in range(1, ROWS): #could be rows or color since it's a square 4x4, two loops if rows and columns are different
        coordinate = i * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (0, coordinate), (WIDTH, coordinate), OUTLINE_THICKNESS) #horizontal
        pygame.draw.line(window, OUTLINE_COLOR, (coordinate, 0), (coordinate, HEIGHT), OUTLINE_THICKNESS) #vertical

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS) #where, color, coordinates, thickness

def draw(window, tiles):
    window.fill(BACKGROUND_COLOR)

    for tile in tiles.values():
        tile.draw_tile(window)

    draw_grid(window)
    pygame.display.update()

def game_loop(window):
    clock = pygame.time.Clock()
    run = True

    all_tiles = generate_tiles()

    while run:
        clock.tick(FPS) #to maintain a stable fps, only run 60 times per second

        for event in pygame.event.get(): #to get events
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    all_tiles = generate_tiles()

        draw(window, all_tiles)

    pygame.quit()

if __name__ == "__main__":
    game_loop(WINDOW)