import tkinter as tk
import random


CELL_SIZE = 30

ROWS = 20
COLUMNS = 10

WIDTH = COLUMNS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

BACKGROUND_COLOR = "beige"

FPS = 500

COLORS = [
    "cyan",
    "blue",
    "orange",
    "yellow",
    "green",
    "purple",
    "red" ]

SHAPES = [
    # I
    [[1, 1, 1, 1]],

    # J
    [[1, 0, 0],
     [1, 1, 1]],

    # L
    [[0, 0, 1],
     [1, 1, 1]],

    # O
    [[1, 1],
     [1, 1]],

    # S
    [[0, 1, 1],
     [1, 1, 0]],

    # T
    [[0, 1, 0],
     [1, 1, 1]],

    # Z
    [[1, 1, 0],
     [0, 1, 1]]
]

class Tetris:
    def __init__(self, canvas):
        self.canvas = canvas
        self.running = False
        self.board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_shape = None
        self.shape_x = 0
        self.shape_y = 0
        self.shape_color = None
        self.shape_id = []

        self.draw_grid()

    def draw_grid(self):
        for row in range(ROWS):
            for col in range(COLUMNS):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline="gray", width=1
                )

    def start(self):
        self.running = True
        self.spawn_new_shape()
        self.update()

    def spawn_new_shape(self):
        shape_index = random.randint(0, len(SHAPES) - 1)
        self.current_shape = SHAPES[shape_index]
        self.shape_color = COLORS[shape_index]
        self.shape_y = 0
        self.shape_x = COLUMNS // 2 - len(self.current_shape[0]) // 2
        self.shape_id = []
        self.draw_shape()

    def draw_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    x_coord = (self.shape_x + x) * CELL_SIZE
                    y_coord = (self.shape_y + y) * CELL_SIZE
                    block = self.canvas.create_rectangle(
                        x_coord, y_coord,
                        x_coord + CELL_SIZE, y_coord + CELL_SIZE,
                        fill=self.shape_color, outline="black"
                    )
                    self.shape_id.append(block)

    def move_shape_down(self):
        if not self.can_move(0, 1):
            self.lock_shape()
            self.spawn_new_shape()
            return

        for block in self.shape_id:
            self.canvas.move(block, 0, CELL_SIZE)
        self.shape_y += 1

    def move_shape(self, dx):
        if self.can_move(dx, 0):
            for block in self.shape_id:
                self.canvas.move(block, dx * CELL_SIZE, 0)
            self.shape_x += dx

    def can_move(self, dx, dy):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.shape_x + x + dx
                    new_y = self.shape_y + y + dy
                    if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS:
                        return False
                    if new_y >= 0 and self.board[new_y][new_x]:
                        return False
        return True

    def lock_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.shape_x + x
                    board_y = self.shape_y + y
                    if 0 <= board_y < ROWS and 0 <= board_x < COLUMNS:
                        self.board[board_y][board_x] = self.shape_color
                        x1 = board_x * CELL_SIZE
                        y1 = board_y * CELL_SIZE
                        self.canvas.create_rectangle(
                            x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE,
                            fill=self.shape_color, outline="black"
                        )

    def update(self):
        if not self.running:
            return
        self.move_shape_down()
        self.canvas.after(FPS, self.update)


root = tk.Tk()
root.title("Тетріс")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BACKGROUND_COLOR)
canvas.pack()

game = Tetris(canvas)
game.start()

def on_key(event):
    if event.keysym == "Left":
        game.move_shape(-1)
    elif event.keysym == "Right":
        game.move_shape(1)
    elif event.keysym == "Down":
        game.move_shape_down()

root.bind("<Key>", on_key)

root.mainloop()
