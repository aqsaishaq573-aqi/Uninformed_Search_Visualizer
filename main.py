import tkinter as tk
import random
import time

from search_algorithms import bfs, dfs, ucs, dls, iddfs, bidirectional

# -------- CONFIG --------
ROWS = 20
COLS = 20
CELL_SIZE = 30
DELAY = 0.03
DYNAMIC_PROBABILITY = 0.03


class PathfinderApp:

    def __init__(self, root):
        self.root = root
        self.root.title("GOOD PERFORMANCE TIME APP")

        self.canvas = tk.Canvas(root,
                                width=COLS * CELL_SIZE,
                                height=ROWS * CELL_SIZE)
        self.canvas.pack()

        self.start = (0, 0)
        self.goal = (ROWS - 1, COLS - 1)

        self.create_buttons()
        self.reset()

    # ---------------- GUI ----------------

    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack()

        tk.Button(frame, text="BFS",
                  command=lambda: self.run("BFS")).pack(side="left")

        tk.Button(frame, text="DFS",
                  command=lambda: self.run("DFS")).pack(side="left")

        tk.Button(frame, text="UCS",
                  command=lambda: self.run("UCS")).pack(side="left")

        tk.Button(frame, text="DLS",
                  command=lambda: self.run("DLS")).pack(side="left")

        tk.Button(frame, text="IDDFS",
                  command=lambda: self.run("IDDFS")).pack(side="left")

        tk.Button(frame, text="Bidirectional",
                  command=lambda: self.run("BID")).pack(side="left")

        tk.Button(frame, text="Reset",
                  command=self.reset).pack(side="left")

    def reset(self):
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")

        for r in range(ROWS):
            for c in range(COLS):
                color = "white"

                if self.grid[r][c] == 1:
                    color = "black"

                if (r, c) == self.start:
                    color = "orange"
                elif (r, c) == self.goal:
                    color = "red"

                self.canvas.create_rectangle(
                    c * CELL_SIZE, r * CELL_SIZE,
                    (c + 1) * CELL_SIZE, (r + 1) * CELL_SIZE,
                    fill=color, outline="gray"
                )

    def color_cell(self, node, color):
        r, c = node
        self.canvas.create_rectangle(
            c * CELL_SIZE, r * CELL_SIZE,
            (c + 1) * CELL_SIZE, (r + 1) * CELL_SIZE,
            fill=color, outline="gray"
        )
        self.root.update()

    # ---------------- DYNAMIC OBSTACLE ----------------

    def spawn_dynamic_obstacle(self):
        if random.random() < DYNAMIC_PROBABILITY:
            r = random.randint(0, ROWS - 1)
            c = random.randint(0, COLS - 1)

            if (r, c) != self.start and (r, c) != self.goal:
                self.grid[r][c] = 1
                self.color_cell((r, c), "black")

    # ---------------- CONTROLLER ----------------

    def run(self, algorithm):

        while True:

            self.spawn_dynamic_obstacle()

            if algorithm == "BFS":
                path = bfs(self.start, self.goal,
                           self.grid, ROWS, COLS)

            elif algorithm == "DFS":
                path = dfs(self.start, self.goal,
                           self.grid, ROWS, COLS)

            elif algorithm == "UCS":
                path = ucs(self.start, self.goal,
                           self.grid, ROWS, COLS)

            elif algorithm == "DLS":
                path = dls(self.start, self.goal,
                           self.grid, ROWS, COLS, limit=15)

            elif algorithm == "IDDFS":
                path = iddfs(self.start, self.goal,
                             self.grid, ROWS, COLS)

            else:
                path = bidirectional(self.start, self.goal,
                                     self.grid, ROWS, COLS)

            if not path:
                return

            blocked = False
            for node in path:
                if self.grid[node[0]][node[1]] == 1:
                    blocked = True
                    break

            if blocked:
                continue  # re-plan

            for node in path:
                self.color_cell(node, "green")
                time.sleep(DELAY)

            return


# -------- RUN PROGRAM --------
if __name__ == "__main__":
    root = tk.Tk()
    app = PathfinderApp(root)
    root.mainloop()
