import tkinter as tk
import random

CELL_SIZE = 30
ROWS = 20
COLUMNS = 10
WIDTH = COLUMNS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
TOP_PANEL_HEIGHT = 60
FPS = 500

THEMES = {
    "dark": {
        "background": "#1a1a1a",
        "text": "#B0FFB0",
        "grid": "#333",
        "block_outline": "#111",
        "button_bg": "#333",
        "button_fg": "#B0FFB0"
    },
    "light": {
        "background": "#f4f4f4",
        "text": "#202020",
        "grid": "#cccccc",
        "block_outline": "#999",
        "button_bg": "#dddddd",
        "button_fg": "#202020"
    }
}

COLORS = [
    "#1E90FF",  # Яскравий кобальтовий синій — насичений і чистий, без зеленуватих відтінків
    "#FF6F61",  # Теплий кораловий — яскравий і помітний, червоно-помаранчевий відтінок
    "#FFD23F",  # Сонячний жовтий — теплий, не надто насичений, але яскравий
    "#6B4226",  # Землистий теракотовий — глибокий і природний коричневий (теплий і контрастний)
    "#2E8B57",  # Морський зелений — насичений, з більш «холодним» зеленим відтінком, не близький до синього
    "#9B2D30",  # Темний рубіновий — багатий, глибокий червоний, що контрастує з іншими кольорами
    "#4B0082"   # Індиго — темний фіолетово-синій, віддалений від зеленого і жовтого
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
    def __init__(self, canvas, root, theme_name="light"):
        self.canvas = canvas
        self.root = root
        self.theme_name = theme_name
        self.theme = THEMES[theme_name]
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
            10, 20, text=f"Score: {self.score}",
            font=("Arial", 14, "bold"),
            fill=self.theme["text"], anchor="w"
        )
        self.level_text = self.canvas.create_text(
            WIDTH - 10, 20, text=f"Level: {self.level}",
            font=("Arial", 14, "bold"),
            fill=self.theme["text"], anchor="e"
        )

        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("grid")
        for row in range(ROWS):
            for col in range(COLUMNS):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE + TOP_PANEL_HEIGHT
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             outline=self.theme["grid"],
                                             tags="grid")

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
        self.draw_grid()
        self.spawn_new_shape()
        self.update()

    def spawn_new_shape(self):
        for block in self.shape_id:
            self.canvas.delete(block)
        self.shape_id = []
        shape_index = random.randint(0, len(SHAPES) - 1)
        self.current_shape = SHAPES[shape_index]
        self.shape_color = random.choice(COLORS)
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
            self.restart_button = tk.Button(self.root, text="Грати знову", font=("Arial", 14, "bold"),
                                            command=self.start,
                                            bg=self.theme["button_bg"],
                                            fg=self.theme["button_fg"])
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
                        fill=self.shape_color,
                        outline=self.theme["block_outline"]
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
        rotated = list(zip(*self.current_shape[::-1]))
        rotated = [list(row) for row in rotated]
        old_shape = self.current_shape
        self.current_shape = rotated
        if self.can_move(0, 0):
            self._redraw_rotated_shape()
        elif self.can_move(-1, 0):
            self.shape_x -= 1
            self._redraw_rotated_shape()
        elif self.can_move(1, 0):
            self.shape_x += 1
            self._redraw_rotated_shape()
        else:
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
                            fill=self.shape_color,
                            outline=self.theme["block_outline"],
                            tags="block"
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
        self.score += lines_cleared * 10 if lines_cleared < 4 else 4 * 10 * 10
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
                        fill=color, outline=self.theme["block_outline"],
                        tags="block"
                    )

    def set_theme(self, theme_name):
        self.theme_name = theme_name
        self.theme = THEMES[theme_name]
        self.canvas.itemconfig(self.score_text, fill=self.theme["text"])
        self.canvas.itemconfig(self.level_text, fill=self.theme["text"])
        self.canvas.config(bg=self.theme["background"])
        if self.restart_button:
            self.restart_button.config(bg=self.theme["button_bg"], fg=self.theme["button_fg"])
        self.redraw_board()
        self.draw_grid()

# GUI Setup
root = tk.Tk()
root.title("Tetris")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT + TOP_PANEL_HEIGHT,
                   bg=THEMES["light"]["background"], highlightthickness=0)
canvas.pack()

game = Tetris(canvas, root, theme_name="light")
current_theme = ["dark"]

def toggle_theme():
    current_theme[0] = "light" if current_theme[0] == "dark" else "dark"
    game.set_theme(current_theme[0])
    theme_button.config(bg=game.theme["button_bg"], fg=game.theme["button_fg"])

theme_button = tk.Button(root, text="Toggle Theme", command=toggle_theme,
                         bg=THEMES["light"]["button_bg"],
                         fg=THEMES["light"]["button_fg"],
                         font=("Arial", 10, "bold"))
theme_button.pack(pady=10)

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
