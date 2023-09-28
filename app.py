import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from flask import Flask, render_template

from generate_maze import MazeGenerator
from solve_maze import MazeSolver

app = Flask(__name__)

maze = np.loadtxt("maze.txt", dtype=int)

@app.route('/')
def index():
    solver = MazeSolver(maze)
    solver.set_start((0, 0))
    solver.set_end((maze.shape[0] - 1, maze.shape[1] - 1))

    path = solver.astar()
    if path:
        print("Path found!")

        # Specify the mistakes made by the robot (example)
        solver.mistakes = [(0, 2, 1, 2), (1, 4, 2, 4)]  # Format: (x1, y1, x2, y2)

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
            for mistake in solver.mistakes:
                x1, y1, x2, y2 = mistake
                ax.plot([y1, y2], [x1, x2], color='y', linestyle='dotted')
            return robot_marker,

        ani = FuncAnimation(fig, update, frames=len(path), interval=200, repeat=False)

        # Save the animation as a temporary file
        ani.save('static/animation.gif', writer='pillow', fps=5)
        
        return render_template('index.html')
    else:
        return "No path found."

if __name__ == "__main__":
    app.run(debug=True)