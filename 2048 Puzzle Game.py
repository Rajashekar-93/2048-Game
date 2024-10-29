import tkinter as tk
import numpy as np
import random

class Game2048:
    def __init__(self):
        self.grid = np.zeros((4, 4), dtype=int)
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_tiles = list(zip(*np.where(self.grid == 0)))
        if empty_tiles:
            row, col = random.choice(empty_tiles)
            self.grid[row, col] = 4 if random.random() < 0.1 else 2

    def reset_game(self):
        self.grid = np.zeros((4, 4), dtype=int)
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def move(self, direction):
        if direction == 'left':
            self.grid = self.merge_left(self.grid)
        elif direction == 'right':
            self.grid = self.merge_left(np.fliplr(self.grid))
        elif direction == 'up':
            self.grid = self.merge_left(self.grid.T).T
        elif direction == 'down':
            self.grid = self.merge_left(np.flipud(self.grid)).T

        self.add_new_tile()
        if self.is_game_over():
            print("Game Over!")

    def merge_left(self, grid):
        new_grid = np.zeros((4, 4), dtype=int)
        for i in range(4):
            non_zero = grid[i][grid[i] != 0]
            merged = []
            skip = False
            for j in range(len(non_zero)):
                if skip:
                    skip = False
                    continue
                if j < len(non_zero) - 1 and non_zero[j] == non_zero[j + 1]:
                    merged.append(non_zero[j] * 2)
                    self.score += non_zero[j] * 2
                    skip = True
                else:
                    merged.append(non_zero[j])
            new_grid[i][:len(merged)] = merged
        return new_grid

    def is_game_over(self):
        if np.any(self.grid == 2048):
            print("You win!")
            return True
        if np.count_nonzero(self.grid == 0) > 0:
            return False
        for i in range(4):
            for j in range(4):
                if (i < 3 and self.grid[i][j] == self.grid[i + 1][j]) or \
                   (j < 3 and self.grid[i][j] == self.grid[i][j + 1]):
                    return False
        return True

class GameGUI(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.title("2048 Puzzle")
        self.grid_cells = []
        self.init_ui()

    def init_ui(self):
        for i in range(4):
            row = []
            for j in range(4):
                cell = tk.Label(self, text="", font=("Arial", 40), width=5, height=2, bg="#CCCCCC", borderwidth=1, relief="solid")
                cell.grid(row=i, column=j, padx=5, pady=5)
                row.append(cell)
            self.grid_cells.append(row)
        self.score_label = tk.Label(self, text="Score: 0", font=("Arial", 20))
        self.score_label.grid(row=4, column=0, columnspan=4)
        self.update_ui()

        self.bind("<Key>", self.key_pressed)

    def update_ui(self):
        for i in range(4):
            for j in range(4):
                self.grid_cells[i][j].config(text=str(self.game.grid[i][j]) if self.game.grid[i][j] != 0 else "", bg=self.get_color(self.game.grid[i][j]))
        self.score_label.config(text=f"Score: {self.game.score}")

    def get_color(self, value):
        # Color mapping for each tile value
        colors = {
            0: "#CCCCCC",  # Light Gray (or Off-White)
            2: "#E9E9E9",  # Very Light Gray
            4: "#E5E5E5",  # Light Gray
            8: "#F2A900",  # Gold
            16: "#F67C20",  # Orange
            32: "#F265A0",  # Dark Pink
            64: "#F23D1F",  # Red
            128: "#EDC22E", # Light Yellow
            256: "#EDC22E", # Light Yellow
            512: "#EDC22E", # Light Yellow
            1024: "#EDC22E",# Light Yellow
            2048: "#EDC22E" # Light Yellow
        }
        return colors.get(value, "#3C3A32")  # Default color for unrecognized values

    def key_pressed(self, event):
        key = event.keysym
        if key in ["Left", "Right", "Up", "Down"]:
            self.game.move(key.lower())
            self.update_ui()

if __name__ == "__main__":
    game = Game2048()
    gui = GameGUI(game)
    gui.mainloop()
