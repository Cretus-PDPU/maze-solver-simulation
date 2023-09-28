import numpy as np
import random
import matplotlib.pyplot as plt

class MazeGenerator:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = np.ones((rows, cols), dtype=int)
        self.start = (0, 0)
        self.end = (rows - 1, cols - 1)

    def generate_maze(self):
        stack = [(self.start[0], self.start[1])]

        while stack:
            x, y = stack[-1]

            self.maze[x, y] = 0
            neighbors = []

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + 2 * dx, y + 2 * dy
                if 0 <= nx < self.rows and 0 <= ny < self.cols and self.maze[nx, ny] == 1:
                    neighbors.append((nx, ny))

            if neighbors:
                nx, ny = random.choice(neighbors)
                self.maze[(nx + x) // 2, (ny + y) // 2] = 0
                stack.append((nx, ny))
            else:
                stack.pop()

        return self.maze

    def visualize(self):
        plt.imshow(self.maze, cmap='binary')
        plt.xticks([]), plt.yticks([])

        # Show starting and ending points
        plt.plot(self.start[1], self.start[0], marker='s', color='g')
        plt.plot(self.end[1], self.end[0], marker='s', color='r')

        plt.show()

    def save_maze(self, filename):
        np.savetxt(filename, self.maze, fmt="%d")

if __name__ == "__main__":
    rows, cols = 50, 50  # Adjust maze size as needed

    generator = MazeGenerator(rows, cols)
    maze = generator.generate_maze()
    generator.visualize()
    
    # Save the generated maze to a file
    generator.save_maze("maze.txt")
