import tkinter as tk
import random

CELL_SIZE = 30
ROWS = 20
COLUMNS = 10
WIDTH = COLUMNS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
TOP_PANEL_HEIGHT = 60
BACKGROUND_COLOR = "#1a1a1a"
FPS = 500
TEXT_COLOR = "#B0FFB0"

COLORS = [
    "#4B6EAF",  # темно-синій
    "#6B4226",  # коричневий
    "#3C6E71",  # зелено-блакитний
    "#A9A9A9",  # темно-сірий
    "#6C584C",  # болотний
    "#7E57C2",  # фіолетовий
    "#9E2A2B"   # бордовий
]

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 0, 0],
     [1, 1, 1]],
    [[0, 0, 1],
     [1, 1, 1]],
    [[1, 1],
     [1, 1]],
    [[0, 1, 1],
     [1, 1, 0]],
    [[0, 1, 0],
     [1, 1, 1]],
    [[1, 1, 0],
     [0, 1, 1]]
]

class Tetris:
    def __init__(self, canvas, root):
        self.canvas = canvas
        self.root = root
        self.running = False
        self.board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_shape = None
        self.shape_x = 0
        self.shape_y = 0
        self.shape_color = None
        self.shape_id = []
        self.score = 0
        self.lines_cleared_total = 0
        self.level = 1
        self.fps = FPS
        self.restart_button = None
        self.game_over_text = None

        self.score_text = self.canvas.create_text(
            10, 20,
            text=f"Score: {self.score}",
            font=("Arial", 14, "bold"),
            fill=TEXT_COLOR,
            anchor="w"
        )
        self.level_text = self.canvas.create_text(
            WIDTH - 10, 20,
            text=f"Level: {self.level}",
            font=("Arial", 14, "bold"),
            fill=TEXT_COLOR,
            anchor="e"
        )

        self.draw_grid()

    def draw_grid(self):
        for row in range(ROWS):
            for col in range(COLUMNS):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE + TOP_PANEL_HEIGHT
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="#333")

    def start(self):
        if self.restart_button:
            self.restart_button.destroy()
        if self.game_over_text:
            self.canvas.delete(self.game_over_text)
        self.running = True
        self.score = 0
        self.level = 1
        self.lines_cleared_total = 0
        self.fps = FPS
        self.board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.canvas.delete("block")
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.level_text, text=f"Level: {self.level}")
        self.spawn_new_shape()
        self.update()

    def spawn_new_shape(self):
        for block in self.shape_id:
            self.canvas.delete(block)
        self.shape_id = []
        shape_index = random.randint(0, len(SHAPES) - 1)
        self.current_shape = SHAPES[shape_index]
        self.shape_color = COLORS[shape_index]
        self.shape_y = 0
        self.shape_x = COLUMNS // 2 - len(self.current_shape[0]) // 2
        if not self.can_move(0, 0):
            self.running = False
            self.game_over_text = self.canvas.create_text(
                WIDTH // 2, HEIGHT // 2,
                text="GAME OVER",
                font=("Arial", 28, "bold"),
                fill="red"
            )
            self.restart_button = tk.Button(self.root, text="Грати знову", font=("Arial", 14, "bold"), command=self.start)
            self.restart_button.place(x=WIDTH // 2 - 60, y=HEIGHT // 2 + 40)
            return
        self.draw_shape()

    def draw_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    x_coord = (self.shape_x + x) * CELL_SIZE
                    y_coord = (self.shape_y + y) * CELL_SIZE + TOP_PANEL_HEIGHT
                    block = self.canvas.create_rectangle(
                        x_coord, y_coord,
                        x_coord + CELL_SIZE, y_coord + CELL_SIZE,
                        fill=self.shape_color, outline="#111"
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

    def fall_shape(self):
        while self.can_move(0, 1):
            self.move_shape_down()

    def rotate_shape(self):
        rotated = list(zip(*self.current_shape))
        rotated = [list(row)[::-1] for row in rotated]
        old_shape = self.current_shape
        self.current_shape = rotated
        if self.can_move(0, 0):
            self._redraw_rotated_shape()
            return
        if self.can_move(-1, 0):
            self.shape_x -= 1
            self._redraw_rotated_shape()
            return
        if self.can_move(1, 0):
            self.shape_x += 1
            self._redraw_rotated_shape()
            return
        self.current_shape = old_shape

    def _redraw_rotated_shape(self):
        for block in self.shape_id:
            self.canvas.delete(block)
        self.shape_id = []
        self.draw_shape()

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
                        y1 = board_y * CELL_SIZE + TOP_PANEL_HEIGHT
                        self.canvas.create_rectangle(
                            x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE,
                            fill=self.shape_color, outline="#111", tags="block"
                        )
        self.clear_lines()

    def update(self):
        if not self.running:
            return
        self.move_shape_down()
        self.canvas.after(self.fps, self.update)

    def clear_lines(self):
        new_board = []
        lines_cleared = 0
        for row in self.board:
            if None not in row:
                lines_cleared += 1
            else:
                new_board.append(row)
        for _ in range(lines_cleared):
            new_board.insert(0, [None for _ in range(COLUMNS)])
        self.board = new_board
        self.redraw_board()
        if lines_cleared == 4:
            self.score += 4 * 10 * 10
        else:
            self.score += lines_cleared * 10
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.lines_cleared_total += lines_cleared
        if self.lines_cleared_total >= 10:
            self.level += 1
            self.lines_cleared_total = 0
            self.fps = max(100, FPS - (self.level - 1) * 50)
            self.canvas.itemconfig(self.level_text, text=f"Level: {self.level}")

    def redraw_board(self):
        self.canvas.delete("block")
        for y, row in enumerate(self.board):
            for x, color in enumerate(row):
                if color:
                    x1 = x * CELL_SIZE
                    y1 = y * CELL_SIZE + TOP_PANEL_HEIGHT
                    self.canvas.create_rectangle(
                        x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE,
                        fill=color, outline="#111", tags="block"
                    )


# --- Створення вікна та запуск гри ---
root = tk.Tk()
root.title("Tetris")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT + TOP_PANEL_HEIGHT, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.pack()

game = Tetris(canvas, root)
game.start()

def on_key(event):
    if game.running:
        if event.keysym == "Left":
            game.move_shape(-1)
        elif event.keysym == "Right":
            game.move_shape(1)
        elif event.keysym == "Down":
            game.move_shape_down()
        elif event.keysym == "Up":
            game.rotate_shape()
        elif event.keysym == "space":
            game.fall_shape()

root.bind("<Key>", on_key)
root.mainloop()
