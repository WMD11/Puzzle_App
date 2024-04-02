import tkinter as tk
import random
from collections import deque

class PuzzleGame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Puzzle 8x8")
        self.geometry("400x400")

        self.label = tk.Label(self, text="Puzzle Game")
        self.label.grid(row=0, column=0, columnspan=3)

        self.shuffle_button = tk.Button(self, text="Amestecă", command=self.shuffle)
        self.shuffle_button.grid(row=1, column=0)

        self.solve_bfs_button = tk.Button(self, text="Rezolvă BFS", command=self.solve_bfs)
        self.solve_bfs_button.grid(row=1, column=1)

        self.tiles = list(range(1, 9)) + [0]  # Inițializăm configurația inițială a puzzle-ului
        self.empty_tile_index = 8  # Indexul casetei goale

        self.create_board()

    def create_board(self):
        self.board_buttons = []
        for i in range(3):
            for j in range(3):
                value = self.tiles[i * 3 + j]
                button = tk.Button(self, text=str(value), width=5, height=2, command=lambda idx=i*3+j: self.move(idx))
                button.grid(row=i + 2, column=j, sticky="nsew", ipadx=20, ipady=20)
                self.board_buttons.append(button)

    def shuffle(self):
        random.shuffle(self.tiles)
        self.update_board()

    def solve_bfs(self):
        # Inițializăm configurația țintă
        target = list(range(1, 9)) + [0]

        # Inițializăm coada pentru BFS
        queue = deque([(self.tiles[:], self.empty_tile_index, [])])
        visited = set()

        while queue:
            current_tiles, empty_index, path = queue.popleft()

            if current_tiles == target:
                self.show_solution(path)
                break

            if tuple(current_tiles) in visited:
                continue
            visited.add(tuple(current_tiles))

            # Generăm stările vecine
            neighbors = self.generate_neighbors(current_tiles, empty_index)

            for neighbor, new_empty_index, move in neighbors:
                queue.append((neighbor, new_empty_index, path + [move]))


    def generate_neighbors(self, tiles, empty_index):
        neighbors = []
        empty_row, empty_col = empty_index // 3, empty_index % 3

        for d_row, d_col, move_name in [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]:
            new_row, new_col = empty_row + d_row, empty_col + d_col

            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_index = new_row * 3 + new_col
                new_tiles = tiles[:]
                new_tiles[empty_index], new_tiles[new_index] = new_tiles[new_index], new_tiles[empty_index]
                neighbors.append((new_tiles, new_index, move_name))

        return neighbors

    def move(self, idx):
        empty_row, empty_col = self.empty_tile_index // 3, self.empty_tile_index % 3
        button_row, button_col = idx // 3, idx % 3

        if (abs(empty_row - button_row) == 1 and empty_col == button_col) or (abs(empty_col - button_col) == 1 and empty_row == button_row):
            self.tiles[self.empty_tile_index], self.tiles[idx] = self.tiles[idx], self.tiles[self.empty_tile_index]
            self.empty_tile_index = idx
            self.update_board()

    def update_board(self):
        for button, value in zip(self.board_buttons, self.tiles):
            button.config(text=str(value) if value != 0 else "")

    def show_solution(self, path):
        for move in path:
            self.move_tile_from_direction(move)
            self.update()
            self.after(500)  # Așteaptă 500 de milisecunde între fiecare mutare

    def move_tile_from_direction(self, direction):
        empty_row, empty_col = self.empty_tile_index // 3, self.empty_tile_index % 3
        if direction == "Up":
            idx = empty_row * 3 + empty_col - 3
        elif direction == "Down":
            idx = empty_row * 3 + empty_col + 3
        elif direction == "Left":
            idx = empty_row * 3 + empty_col - 1
        elif direction == "Right":
            idx = empty_row * 3 + empty_col + 1
        self.move(idx)

if __name__ == "__main__":
    app = PuzzleGame()
    app.mainloop()