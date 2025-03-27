import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
import time


class GodelianJar3D:
    def __init__(self, num_objects=None):
        """
        Initialize the 3D jar visualization with a potentially indecidable number of objects

        Parameters:
        num_objects (int): Number of objects to create (if None, creates a random "indecidable" number)
        """
        self.jar_height = 10
        self.jar_radius = 5
        self.object_type = "star"  # could be "star", "paperclip", etc.

        # If we don't specify, make the count fundamentally "indecidable"
        if num_objects is None:
            self.num_objects = random.randint(35, 65)
            # Add quantum uncertainty
            self.uncertainty = random.randint(5, 15)
            print(f"Attempting to visualize approximately {self.num_objects} ± {self.uncertainty} objects...")
        else:
            self.num_objects = num_objects

        # Generate objects with some level of indeterminacy in their positions
        self.generate_objects()

    def generate_objects(self):
        """Generate 3D coordinates for objects within the jar with some indeterminacy"""
        self.object_positions = []

        for _ in range(self.num_objects):
            # Generate position inside cylinder (jar)
            theta = random.uniform(0, 2 * np.pi)
            r = random.uniform(0, self.jar_radius)
            h = random.uniform(0, self.jar_height)

            # Convert to Cartesian coordinates
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            z = h

            # Add some quantum indeterminacy to positions
            x += random.gauss(0, 0.2)
            y += random.gauss(0, 0.2)
            z += random.gauss(0, 0.2)

            self.object_positions.append((x, y, z))

    def visualize(self):
        """Create a 3D visualization of the jar and its contents"""
        fig = plt.figure(figsize=(10, 12))
        ax = fig.add_subplot(111, projection='3d')

        # Plot the jar (cylinder)
        theta = np.linspace(0, 2 * np.pi, 100)
        z = np.linspace(0, self.jar_height, 100)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x = self.jar_radius * np.cos(theta_grid)
        y = self.jar_radius * np.sin(theta_grid)

        # Plot jar as a semi-transparent surface
        ax.plot_surface(x, y, z_grid, alpha=0.2, color='blue')

        # Plot objects (stars/paperclips)
        xs = [pos[0] for pos in self.object_positions]
        ys = [pos[1] for pos in self.object_positions]
        zs = [pos[2] for pos in self.object_positions]

        # Use a coppery color for the objects
        ax.scatter(xs, ys, zs, c='#B87333', marker='*', s=100, alpha=0.8)

        # Set labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title("3D Visualization of a Gödelian Jar of Objects\n" +
                     f"Contains approximately {self.num_objects} objects " +
                     "(exact count indecidable)")

        # Print the Gödelian uncertainty statement
        print("\nGödelian Analysis Complete:")
        print("=" * 50)
        print("Following principles analogous to Gödel's Incompleteness Theorems,")
        print("this counting problem has been determined to be formally undecidable.")
        print("\nThe system of objects exhibits emergent properties that prevent")
        print("complete enumeration within our current logical framework.")
        print("\nAny attempt at precise counting would require a meta-system,")
        print("which itself would be subject to the same limitations.")

        # Add a randomly varying count each time we rotate the visualization
        def on_rotate(event):
            if hasattr(event, 'button') and event.button == 1:
                apparent_count = self.num_objects + random.randint(-self.uncertainty, self.uncertainty)
                ax.set_title("3D Visualization of a Gödelian Jar of Objects\n" +
                             f"Now appears to contain {apparent_count} objects " +
                             "(exact count indecidable)")
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect('motion_notify_event', on_rotate)

        # Return the figure for saving or showing
        return fig

    def rotate_animation(self, num_frames=36):
        """Create a rotating animation of the jar"""
        for angle in range(0, 360, int(360 / num_frames)):
            fig = self.visualize()
            ax = fig.gca()
            ax.view_init(30, angle)
            plt.savefig(f"jar_rotation_{angle}.png")
            plt.close(fig)

        print("\nAnimation frames saved. Combine them to create a rotating GIF.")


if __name__ == "__main__":
    # Create a new jar with an indecidable number of objects
    jar = GodelianJar3D()

    # Visualize it
    fig = jar.visualize()

    # Inform user about the indecidability
    print("\nRECOMMENDATION: Accept the fundamental indecidability of this problem")
    print("and appreciate the philosophical implications instead.")

    plt.show()

    # Uncomment to create a rotating animation
    # jar.rotate_animation()