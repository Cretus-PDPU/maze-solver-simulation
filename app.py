import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from flask import Flask, render_template

from generate_maze import MazeGenerator
from solve_maze import MazeSolver

app = Flask(__name__)

# Load maze data from a text file (assuming the file exists)

print("Generating maze")
generator = MazeGenerator(30, 30)
maze = generator.generate_maze()
generator.save_maze("maze.txt")
maze = np.loadtxt("maze.txt", dtype=int)
fig, ax = plt.subplots(figsize=(3, 3), dpi=100)
ax.imshow(maze, cmap='binary')
ax.set_xticks([]), ax.set_yticks([])
ax.set_xticklabels([]), ax.set_yticklabels([])
plt.savefig('static/maze.png', bbox_inches='tight', pad_inches=0, dpi=100)

@app.route('/')
def index():
    if maze is None:
        return "Maze data not available. Check if 'maze.txt' exists and contains valid data."

    # Initialize the solver and set start and end points
    solver = MazeSolver(maze)
    solver.set_start((0, 0))
    solver.set_end((maze.shape[0] - 1, maze.shape[1] - 1))

    # Attempt to find a path in the maze
    path = solver.astar()
    if path:
        print("Path found!")

        # Create the animation
        fig, ax = plt.subplots()
        ax.imshow(maze, cmap='binary')
        ax.set_xticks([]), ax.set_yticks([])
        ax.plot(solver.start[1], solver.start[0], marker='s', color='g', markersize=10)
        ax.plot(solver.end[1], solver.end[0], marker='s', color='r', markersize=10)
        path = np.array(path)
        robot_marker, = ax.plot([], [], marker='o', color='b', markersize=15)

        def update(frame):
            x, y = path[frame]
            robot_marker.set_data(y, x)
            return robot_marker,

        ani = FuncAnimation(fig, update, frames=len(path), interval=50, repeat=False)

        try:
            # Save the animation as a temporary file
            ani.save('static/animation.gif', writer='pillow', fps=10)
            return render_template('index.html')
        except Exception as e:
            return f"Error saving animation: {str(e)}"
    else:
        return "No path found."

if __name__ == "__main__":
    app.run(debug=True)
