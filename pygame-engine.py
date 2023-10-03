import numpy as np
import pygame
import time

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.rows, self.cols = maze.shape
        self.start = None
        self.end = None
        self.robot = None

        pygame.init()
        self.screen = pygame.display.set_mode((self.cols * 20, self.rows * 20))
        pygame.display.set_caption("Maze Solver")
        self.clock = pygame.time.Clock()

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

    def visualize_solution(self, solution):
        if solution:
            path = np.array(solution)

            robot_pos = path[0]  # Initialize robot position

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                self.screen.fill((255, 255, 255))  # Clear the screen
                self.draw_maze()
                self.draw_trail(path[:np.where((path == robot_pos).all(axis=1))[0][-1] + 1], (255, 0, 0))
                self.draw_robot(robot_pos)
                pygame.display.flip()

                if len(path) > 1:
                    robot_pos = path[1]  # Move the robot to the next position
                    path = path[1:]

                self.clock.tick(30)  # Adjust the frame rate

        else:
            print("No path found.")

    def draw_maze(self):
        for i in range(self.rows):
            for j in range(self.cols):
                color = (0, 0, 0) if self.maze[i, j] == 1 else (255, 255, 255)
                pygame.draw.rect(self.screen, color, pygame.Rect(j * 20, i * 20, 20, 20))

    def draw_robot(self, position):
        x, y = position
        pygame.draw.circle(self.screen, (0, 0, 255), (y * 20 + 10, x * 20 + 10), 8)

    def draw_trail(self, path, color):
        for i in range(len(path) - 1):
            start = (path[i][1] * 20 + 10, path[i][0] * 20 + 10)
            end = (path[i + 1][1] * 20 + 10, path[i + 1][0] * 20 + 10)
            pygame.draw.line(self.screen, color, start, end, 2)

if __name__ == "__main__":
    rows, cols = 50, 50

    maze = np.loadtxt("maze.txt", dtype=int)

    solver = MazeSolver(maze)
    solver.set_start((0, 0))
    solver.set_end((rows - 1, cols - 1))
    solution = solver.astar()

    if solution:
        solver.visualize_solution(solution)
    else:
        print("No path found.")
