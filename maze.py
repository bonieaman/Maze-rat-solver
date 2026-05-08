import tkinter as tk
import random
import time

# SETTINGS
ROWS = 15
COLS = 20
CELL_SIZE = 35
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
MOUSE_SPEED = 0.05  # Faster for testing

# WINDOW
root = tk.Tk()
root.title("Maze Rat Solver")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

# MAZE DATA
maze = []
for row in range(ROWS):                        
    maze_row = []
    for col in range(COLS):
        cell = {
            "top": True, "bottom": True, "left": True, "right": True, "visited": False
        }
        maze_row.append(cell)
    maze.append(maze_row)

def draw_maze():
    # Only draw walls and background once or when specifically needed
    for row in range(ROWS):
        for col in range(COLS):
            x1, y1 = col * CELL_SIZE, row * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            cell = maze[row][col]
            if cell["top"]: canvas.create_line(x1, y1, x2, y1, width=2)
            if cell["bottom"]: canvas.create_line(x1, y2, x2, y2, width=2)
            if cell["left"]: canvas.create_line(x1, y1, x1, y2, width=2)
            if cell["right"]: canvas.create_line(x2, y1, x2, y2, width=2)

def remove_walls(r1, c1, r2, c2):
    if r1 == r2:
        if c1 < c2:
            maze[r1][c1]["right"] = False
            maze[r2][c2]["left"] = False
        else:
            maze[r1][c1]["left"] = False
            maze[r2][c2]["right"] = False
    if c1 == c2:
        if r1 < r2:
            maze[r1][c1]["bottom"] = False
            maze[r2][c2]["top"] = False
        else:
            maze[r1][c1]["top"] = False
            maze[r2][c2]["bottom"] = False

def generate_maze():
    stack = []
    current_row, current_col = 0, 0
    maze[0][0]["visited"] = True
    while True:
        neighbors = []
        if current_row > 0 and not maze[current_row - 1][current_col]["visited"]:
            neighbors.append((current_row - 1, current_col))
        if current_row < ROWS - 1 and not maze[current_row + 1][current_col]["visited"]:
            neighbors.append((current_row + 1, current_col))
        if current_col > 0 and not maze[current_row][current_col - 1]["visited"]:
            neighbors.append((current_row, current_col - 1))
        if current_col < COLS - 1 and not maze[current_row][current_col + 1]["visited"]:
            neighbors.append((current_row, current_col + 1))

        if neighbors:
            next_row, next_col = random.choice(neighbors)
            stack.append((current_row, current_col))
            remove_walls(current_row, current_col, next_row, next_col)
            current_row, current_col = next_row, next_col
            maze[current_row][current_col]["visited"] = True
        elif stack:
            current_row, current_col = stack.pop()
        else:
            break

def color_cell(row, col, color):
    x1, y1 = col * CELL_SIZE + 3, row * CELL_SIZE + 3
    x2, y2 = x1 + CELL_SIZE - 6, y1 + CELL_SIZE - 6
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

def draw_rat(row, col):
    # Remove old rat before drawing new one
    canvas.delete("rat")
    
    x1 = col * CELL_SIZE + 10
    y1 = row * CELL_SIZE + 10
    x2 = x1 + CELL_SIZE - 20
    y2 = y1 + CELL_SIZE - 20

    # Draw the mouse with a tag "rat" so we can find it later
    canvas.create_oval(x1, y1, x2, y2, fill="red", outline="black", width=2, tags="rat")
    root.update()

# SOLVE MAZE
visited_solve = set()

def solve_maze(row, col):
    # Mark path
    color_cell(row, col, "#e0e0e0") # Light trail
    draw_rat(row, col)
    time.sleep(MOUSE_SPEED)

    if row == ROWS - 1 and col == COLS - 1:
        color_cell(row, col, "orange")
        return True

    visited_solve.add((row, col))

    # Directions: Down, Right, Up, Left (Ordering can change behavior)
    directions = [
        (row + 1, col, "bottom"), # Down
        (row, col + 1, "right"),  # Right
        (row - 1, col, "top"),    # Up
        (row, col - 1, "left")    # Left
    ]

    for nr, nc, wall in directions:
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            if not maze[row][col][wall] and (nr, nc) not in visited_solve:
                if solve_maze(nr, nc):
                    return True

    # Backtracking (Dead end)
    color_cell(row, col, "#ffcccc") # Reddish for dead end
    draw_rat(row, col)
    time.sleep(MOUSE_SPEED)
    return False

# RUN PROGRAM
generate_maze()
draw_maze()
color_cell(0, 0, "green")
color_cell(ROWS - 1, COLS - 1, "yellow")

# Start solving
solve_maze(0, 0)
root.mainloop()