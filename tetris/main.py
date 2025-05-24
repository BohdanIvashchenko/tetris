import tkinter as tk
from config import WIDTH, HEIGHT, BACKGROUND_COLOR
from game import Tetris

def main():
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

if __name__ == "__main__":
    main()
