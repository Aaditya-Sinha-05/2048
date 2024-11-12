import pygame
import random
import math

from pygame.display import update

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

    def set_pos(self, ceil=False):
        if ceil: #TODO try to understand this again
            self.row = math.ceil(self.y / RECT_HEIGHT) #to make sure row is always int
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move_tile(self, delta):
        self.x += delta[0] #it gives x coordinate
        self.y += delta[1] #it gives y coordinate

def move_tiles(window, tiles, clock, direction):
    updated = True
    blocks = set()

    if direction == "left":
        sort_func = lambda x: x.col #lambda is function syntax, x is the parameter, x.col is the returning value
        reverse = False
        delta = (-MOVE_VEL, 0) #changing coordinates: we move -(left) MOVE_VEL(speed) in x axis and 0 in y axis(no movement)
        boundary_check = lambda tile: tile.col == 0 #true if tile is at boundary
        get_next_tile = lambda tile: tiles.get("{}{}".format(tile.row, tile.col - 1)) #get is a function for dictionary
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL #checks the x-coordinate of current tile(right-side) and next tile(left side) + MOVE_VEL(speed): this tells if the current tile is enough into the next tile that it can be merged SMOOTHLY(hence we use speed)
        move_check = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL #x-coordinate(leftmost/starting coordinate) of current tile, x-coordinate + RECT_WIDTH + MOVE_VEL(rightmost/ending coordinate) of next tile
        ceil = True #rounding of coordinate, true for left to get round up on coordinate
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get("{}{}".format(tile.row, tile.col + 1))
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        ceil = False
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get("{}{}".format(tile.row - 1, tile.col))
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        ceil = True
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get("{}{}".format(tile.row + 1, tile.col))
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
        ceil = False


    while updated:
        clock.tick(FPS)
        updated = False #false to stop updating, change value again to keep looping until no more updates are there(speed movement is also an update)
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse) #gives a sorted list: iterables are keys(because they give coordinate in ROW-COL), key tells the basis to sort on

        for i, tile in enumerate(sorted_tiles): #enumerate returns the counter(iteration index) as the key and value of iteration as the key's value
            if boundary_check(tile): #if tile is at boundary, do nothing
                continue

            next_tile = get_next_tile(tile)
            if not next_tile: #if tile is not at boundary but no next tile, move
                tile.move_tile(delta)
            elif (tile.value == next_tile.value) and (tile not in blocks) and (next_tile not in blocks): #if next tile is found and both are eligible(merge only once per move) for merging, check values, if equal, merge
                if merge_check(tile, next_tile): #returns True as long as we are in the process of merging aka tiles are not overlapping
                    tile.move_tile(delta) #keep moving to overlap
                else: #once they are overlapping completely
                    next_tile.value *= 2 #merge the values
                    sorted_tiles.pop(i) #remove the current tile
                    blocks.add(next_tile) #adding to exception so it doesn't merge again, might change #TODO
            elif move_check(tile, next_tile): #if not merging, just move
                tile.move_tile(delta)
            else:
                continue

            tile.set_pos(ceil)
            updated = True

        update_tiles(window, tiles, sorted_tiles)
    return end_move(tiles)

def end_move(tiles):
    if len(tiles) == 16:
        return "Lost"

    row, col = get_random_position(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2,4]), row, col)
    return "continue"


def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles["{}{}".format(tile.row, tile.col)] = tile

    draw(window, tiles)

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
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    move_tiles(window, all_tiles, clock, "left")
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    move_tiles(window, all_tiles, clock, "right")
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    move_tiles(window, all_tiles, clock, "up")
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    move_tiles(window, all_tiles, clock, "down")

        draw(window, all_tiles)

    pygame.quit()

if __name__ == "__main__":
    game_loop(WINDOW)