import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.rows, self.cols = maze.shape
        self.start = None
        self.end = None
        self.robot = None

    def set_start(self, start):
        self.start = start

    def set_end(self, end):
        self.end = end

    def set_robot(self, robot):
        self.robot = robot

    def is_valid(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols and self.maze[x, y] == 0

    def heuristic(self, node):
        return abs(node[0] - self.end[0]) + abs(node[1] - self.end[1])

    def astar(self):
        if self.start is None or self.end is None:
            raise ValueError("Start and end points must be set.")

        open_set = [(0, self.start)]
        came_from = {}
        g_score = {node: float("inf") for node in np.ndindex(self.maze.shape)}
        g_score[self.start] = 0

        while open_set:
            _, current = open_set.pop(0)

            if current == self.end:
                return self.reconstruct_path(came_from, current)

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                x, y = current[0] + dx, current[1] + dy
                neighbor = (x, y)

                if self.is_valid(x, y):
                    tentative_g_score = g_score[current] + 1

                    if tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + self.heuristic(neighbor)

                        # Add neighbor to the open set
                        open_set.append((f_score, neighbor))
                        open_set.sort(key=lambda x: x[0])  # Sort by f_score

        return None  # No path found

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]

    def visualize_solution(self, solution, animation_interval=50):
        fig, ax = plt.subplots()
        ax.imshow(self.maze, cmap='binary')
        ax.set_xticks([]), ax.set_yticks([])

        # Show starting and ending points with larger markers
        ax.plot(self.start[1], self.start[0], marker='s', color='g', markersize=10)
        ax.plot(self.end[1], self.end[0], marker='s', color='r', markersize=10)

        if solution:
            path = np.array(solution)
            robot_marker, = ax.plot([], [], marker='o', color='b', markersize=15)

            def update(frame):
                x, y = path[frame]
                robot_marker.set_data(y, x)
                self.highlight_visited_cells(ax, path[:frame + 1])
                return robot_marker,

            ani = FuncAnimation(fig, update, frames=len(path), interval=animation_interval, repeat=False)
            plt.show()
        else:
            print("No path found.")
            plt.show()
    
    def highlight_visited_cells(self, ax, visited_cells):
        for cell in visited_cells:
            x, y = cell
            ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='yellow', alpha=0.5))
            plt.pause(0.1)


if __name__ == "__main__":
    rows, cols = 50, 50  # 

    maze = np.loadtxt("maze.txt", dtype=int)

    solver = MazeSolver(maze)
    solver.set_start((0, 0))
    solver.set_end((rows - 1, cols - 1))
    solution = solver.astar()

    if solution:
        solver.visualize_solution(solution)
    else:
        print("No path found.")