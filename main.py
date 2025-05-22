import turtle
import time
import random

# --- Налаштування ---
GRID_SIZE = 30
COLUMNS = 10
ROWS = 20
START_X = -GRID_SIZE * COLUMNS // 2
START_Y = GRID_SIZE * ROWS // 2

# --- Екран ---
wn = turtle.Screen()
wn.title("Tetris on Turtle")
wn.bgcolor("black")
wn.setup(width=GRID_SIZE*COLUMNS + 40, height=GRID_SIZE*ROWS + 40)
wn.tracer(0)

# --- Сітка та рахунок ---
grid = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
score = 0

# --- Відображення балів ---
score_writer = turtle.Turtle()
score_writer.hideturtle()
score_writer.penup()
score_writer.color("white")
score_writer.goto(0, START_Y - GRID_SIZE // 2)

def update_score():
    score_writer.clear()
    score_writer.write(f"Score: {score}", align="center", font=("Arial", 16, "normal"))

update_score()

# --- Клас блоку ---
class Block(turtle.Turtle):
    def __init__(self, color="white"):
        super().__init__()
        self.shape("square")
        self.color(color)
        self.penup()
        self.speed(0)
        self.shapesize(stretch_wid=GRID_SIZE / 20 * 0.9, stretch_len=GRID_SIZE / 20 * 0.9)

# --- Клас фігури ---
class Piece:
    SHAPES = {
        "I": [[1, 1, 1, 1]],
        "O": [[1, 1], [1, 1]],
        "T": [[0, 1, 0], [1, 1, 1]],
        "L": [[1, 0], [1, 0], [1, 1]],
        "J": [[0, 1], [0, 1], [1, 1]],
        "S": [[0, 1, 1], [1, 1, 0]],
        "Z": [[1, 1, 0], [0, 1, 1]],
    }

    COLORS = {
        "I": "cyan",
        "O": "yellow",
        "T": "purple",
        "L": "orange",
        "J": "blue",
        "S": "green",
        "Z": "red"
    }

    def __init__(self):
        self.name = random.choice(list(Piece.SHAPES.keys()))
        self.shape = Piece.SHAPES[self.name]
        self.color = Piece.COLORS[self.name]
        self.x = COLUMNS // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.blocks = []
        self.create_blocks()

    def create_blocks(self):
        self.blocks.clear()
        for i, row in enumerate(self.shape):
            for j, val in enumerate(row):
                if val:
                    block = Block(self.color)
                    block.goto(self.to_screen(self.x + j, self.y + i))
                    self.blocks.append([block, j, i])

    def to_screen(self, x, y):
        return START_X + x * GRID_SIZE + GRID_SIZE / 2, START_Y - y * GRID_SIZE - GRID_SIZE / 2

    def move(self, dx, dy):
        if self.valid_move(dx, dy):
            self.x += dx
            self.y += dy
            for block, j, i in self.blocks:
                block.goto(self.to_screen(self.x + j, self.y + i))

    def valid_move(self, dx, dy):
        for _, j, i in self.blocks:
            new_x = self.x + dx + j
            new_y = self.y + dy + i
            if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS:
                return False
            if new_y >= 0:
                if 0 <= new_y < ROWS and 0 <= new_x < COLUMNS:
                    if grid[new_y][new_x]:
                        return False
        return True

    def freeze(self):
        for block, j, i in self.blocks:
            gx = self.x + j
            gy = self.y + i
            if 0 <= gy < ROWS and 0 <= gx < COLUMNS:
                grid[gy][gx] = block

def draw_grid():
    drawer = turtle.Turtle()
    drawer.hideturtle()
    drawer.color("gray")
    drawer.speed(0)
    drawer.penup()
    for r in range(ROWS + 1):
        y = START_Y - r * GRID_SIZE
        drawer.goto(START_X, y)
        drawer.setheading(0)
        drawer.pendown()
        drawer.forward(GRID_SIZE * COLUMNS)
        drawer.penup()
    for c in range(COLUMNS + 1):
        x = START_X + c * GRID_SIZE
        drawer.goto(x, START_Y)
        drawer.setheading(-90)
        drawer.pendown()
        drawer.forward(GRID_SIZE * ROWS)
        drawer.penup()

def clear_lines():
    global score
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    cleared = ROWS - len(new_grid)
    for _ in range(cleared):
        new_grid.insert(0, [0] * COLUMNS)
    if cleared > 0:
        for r in range(ROWS):
            for c in range(COLUMNS):
                if grid[r][c] and not new_grid[r][c]:
                    grid[r][c].hideturtle()
        for r in range(ROWS):
            for c in range(COLUMNS):
                grid[r][c] = new_grid[r][c]
        score += cleared * 100
        update_score()

def spawn_piece():
    global current_piece
    current_piece = Piece()
    if not current_piece.valid_move(0, 0):
        print("Game Over")
        wn.bye()

def game_loop():
    wn.update()
    if current_piece.valid_move(0, 1):
        current_piece.move(0, 1)
    else:
        current_piece.freeze()
        clear_lines()
        spawn_piece()
    wn.ontimer(game_loop, 500)

# --- Управління ---
def left(): current_piece.move(-1, 0)
def right(): current_piece.move(1, 0)
def down(): current_piece.move(0, 1)

wn.listen()
wn.onkeypress(left, "Left")
wn.onkeypress(right, "Right")
wn.onkeypress(down, "Down")

# --- Запуск ---
draw_grid()
spawn_piece()
wn.ontimer(game_loop, 500)
wn.mainloop()
