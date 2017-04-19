# In this program I use only pure functions, there are no side effects.

# You can change whole GUI only by modifying the display(ground) function.
# displaying function is slow in IDLE Shell, use Linux Shell instead.
# Tip: if you make the terminal window fit around the current state of the game,
#     it will look pretty interactive :)

# Tetromino is tuple of shape, position and color.
# Shape is list of four coordinates.
# Color is a character.
# Ground is list of lists of colors.

# Coordinates are in form of (x, y),
# you select a certain color in ground as ground[x][y].
# As ground[x] is drawn on one line in Python,
# x is index of row and y of column.
# It's swapped compared to mathematical representation.

from random import choice, randint

SHAPES = [[(0, 0), (0, 1), (0, 2), (0, 3)],
          [(0, 0), (0, 1), (0, 2), (1, 1)],
          [(0, 0), (0, 1), (1, 0), (1, 1)],
          [(0, 0), (0, 1), (1, 1), (1, 2)],
          [(0, 0), (1, 0), (2, 0), (2, 1)],
          [(0, 1), (0, 2), (1, 0), (1, 1)],
          [(0, 1), (1, 1), (2, 0), (2, 1)]]

COLORS, EMPTY = ['&', '%', '@', '#', '$'], ' '
LEFT, RIGHT, DOWN = (0, -1), (0, 1), (1, 0)

def init_copy(ground, tetromino):
    return ([x.copy() for x in ground], *tetromino)

def can_place(ground, tetromino):
    ground, shape, pos, color = init_copy(ground, tetromino)
    coords = [(c[0] + pos[0], c[1] + pos[1]) for c in shape]
    maxx, maxy = (max(c) for c in zip(*coords))
    minx, miny = (min(c) for c in zip(*coords))
    if minx >= 0 and miny >= 0 and maxx < len(ground) and maxy < len(ground[0]):
        if not list(filter(lambda c: ground[c[0]][c[1]] != EMPTY, coords)):
            return True
    return False

def place(ground, tetromino):
    ground, shape, pos, color = init_copy(ground, tetromino)
    for coord in shape:
        ground[pos[0] + coord[0]][pos[1] + coord[1]] = color
    return ground

def rotate_shape(shape):
    y = max([c[1] for c in shape])
    return sorted([(abs(c[1]-y), c[0]) for c in shape])

def rotate(ground, tetromino):
    ground, shape, pos, color = init_copy(ground, tetromino)
    new_tetromino = (rotate_shape(shape), pos, color)
    ground = remove(ground, tetromino)
    if can_place(ground, new_tetromino):
        tetromino = new_tetromino
    ground = place(ground, tetromino)
    return ground, tetromino

def remove(ground, tetromino):
    return place(ground, (tetromino[0], tetromino[1], EMPTY))

def move(ground, tetromino, direction):
    ground, shape, pos, color = init_copy(ground, tetromino)
    new_pos = (pos[0] + direction[0], pos[1] + direction[1])
    new_tetromino = (shape, new_pos, color)
    ground = remove(ground, tetromino)
    if can_place(ground, new_tetromino):
        tetromino = new_tetromino
    ground = place(ground, tetromino)
    return ground, tetromino

def line_away(ground):
    ground = [x.copy() for x in ground]
    ground.pop()
    ground.insert(0, [EMPTY for _ in range(len(ground[0]))])
    return ground

def random_shape():
    shape = choice(SHAPES).copy()
    for i in range(randint(0, 3)):
        shape = rotate_shape(shape)
    return shape

def game(sizes=(15, 10), startcoords=(0, 0)):
    ground = [[EMPTY for _ in range(sizes[1])] for _ in range(sizes[0])]
    score = 0
    next_tetromino = random_shape(), startcoords, choice(COLORS)
    while True:
        tetromino = next_tetromino
        next_tetromino = random_shape(), startcoords, choice(COLORS)
        if not can_place(ground, tetromino):
            break
        ground = place(ground, tetromino)

        # downfall of one tetromino
        old_state = ()
        while move(ground, tetromino, DOWN) != (ground, tetromino) or old_state != tetromino:
            display(ground, score, next_tetromino)
            old_state = tetromino
            dirs = {'s': DOWN, 'a': LEFT, 'd': RIGHT}
            action = input()
            if action is 'w':
                ground, tetromino = rotate(ground, tetromino)
            elif action in dirs.keys():
                ground, tetromino = move(ground, tetromino, dirs[action])
            else:
                ground, tetromino = move(ground, tetromino, DOWN)
        
        score += 1
        while EMPTY not in ground[-1]:
            ground = line_away(ground)
            score += 10

def display_ground(ground):
    for _ in range(len(ground[0])):
        print(' _', end='')
    print()
    for line in ground:
        print('|', end='')
        for char in line:
            print(char, end=' ')
        print('|')
    for _ in range(len(ground[0])):
        print(' *', end='')
    print()
    
def display_next(next_tetromino):
    ground = [[EMPTY for _ in range(4)] for _ in range(4)]
    tetromino = next_tetromino[0], (0,0), next_tetromino[2]
    ground = place(ground, tetromino)
    print("Next tetromino:")
    display_ground(ground)

def display(ground, score, next_tetromino):
    display_next(next_tetromino)
    print('Score: {}'.format(score))
    display_ground(ground)
    print()

if __name__ == "__main__":
    game()
