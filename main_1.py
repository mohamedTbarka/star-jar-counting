import pygame
import math
import random
import sys
import numpy as np


class GodelianJar:
    def __init__(self, num_objects=None, debug_mode=False):
        """
        Initialize the PyGame jar visualization with a "indecidable" number of objects

        Parameters:
        num_objects (int): Number of objects to create (if None, creates a random "indecidable" number)
        debug_mode (bool): Enable debugging output
        """
        self.debug_mode = debug_mode

        # Initialize Pygame
        pygame.init()
        self.display_width = 800
        self.display_height = 600

        # Create display surface
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Gödelian Jar: The Indecidable Counting Problem")

        # Set background color
        self.background_color = (0, 0, 0)  # Black
        self.display.fill(self.background_color)

        # Jar dimensions (in pixels for 2D)
        self.jar_center_x = self.display_width // 2
        self.jar_center_y = self.display_height // 2
        self.jar_width = 300
        self.jar_height = 400
        self.jar_bottom_y = self.jar_center_y + self.jar_height // 2

        # If no specific count, make it "indecidable"
        if num_objects is None:
            # Base count with deliberate uncertainty
            self.num_objects = random.randint(35, 65)
            self.uncertainty = random.randint(10, 20)
            print(f"Attempting to visualize approximately {self.num_objects} ± {self.uncertainty} objects...")
        else:
            self.num_objects = num_objects
            self.uncertainty = 10

        # Generate objects (stars) in the jar
        self.generate_objects()

        # Visualization parameters
        self.rotation_angle = 0
        self.rotation_speed = 1
        self.apparent_count = self.num_objects
        self.display_font = pygame.font.SysFont('Arial', 24)
        self.display_small_font = pygame.font.SysFont('Arial', 18)
        self.count_update_interval = 10  # Frames between count updates

        # Define colors
        self.jar_color = (100, 100, 255, 128)  # Light blue, semi-transparent
        self.jar_outline_color = (150, 150, 255)  # Lighter blue for outlines
        self.star_color = (184, 115, 51)  # Copper color for stars
        self.text_color = (255, 255, 255)  # White for text

        # Track FPS
        self.clock = pygame.time.Clock()

    def generate_objects(self):
        """Generate coordinates for objects within the jar"""
        self.stars = []
        self.star_visibility = []
        self.star_depths = []  # For pseudo-3D effect
        self.star_sizes = []  # Size for each star

        # Calculate jar boundaries
        jar_left = self.jar_center_x - self.jar_width // 2
        jar_right = self.jar_center_x + self.jar_width // 2
        jar_top = self.jar_center_y - self.jar_height // 2
        jar_bottom = self.jar_center_y + self.jar_height // 2

        # Generate stars
        for _ in range(self.num_objects):
            # Generate position inside jar
            # Use an elliptical distribution to simulate 3D cylinder
            angle = random.uniform(0, 2 * math.pi)
            radius_factor = random.uniform(0, 1) ** 0.5  # Square root for uniform distribution in circle

            # Depth in the jar (for pseudo-3D)
            depth = random.uniform(-1.0, 1.0)  # -1 is back, 1 is front

            # Adjust radius based on depth to create 3D cylinder illusion
            effective_width = self.jar_width * (0.5 + 0.5 * (1 - abs(depth)) ** 2)

            # Calculate position
            x = self.jar_center_x + radius_factor * effective_width / 2 * math.cos(angle)
            y = jar_top + random.uniform(0.1, 0.9) * self.jar_height

            self.stars.append((x, y))
            self.star_depths.append(depth)

            # Size varies with depth
            size = random.uniform(3, 6) * (1 - 0.5 * abs(depth))
            self.star_sizes.append(size)

            # Initial visibility (some stars may be temporarily invisible)
            self.star_visibility.append(random.random() > 0.1)  # 90% initially visible

    def update_object_visibility(self):
        """Update which objects are visible (simulating quantum indeterminacy)"""
        # Update based on the rotation angle
        angle_factor = abs(math.sin(math.radians(self.rotation_angle)))

        for i in range(self.num_objects):
            # Make visibility depend on viewing angle and a random factor
            if random.random() < 0.05 or (i % 10 == 0 and angle_factor > 0.7):
                # 5% random chance to flip visibility, plus angle-dependent changes
                self.star_visibility[i] = not self.star_visibility[i]

    def update_apparent_count(self):
        """Update the apparent count based on current view and Gödelian indecidability"""
        # Count actually visible objects
        true_visible = sum(self.star_visibility)

        # Add Gödelian indeterminacy that depends on viewing angle
        angle_factor = math.sin(math.radians(self.rotation_angle * 2))
        count_variation = int(angle_factor * self.uncertainty)

        # The apparent count fluctuates around true_visible
        self.apparent_count = true_visible + count_variation

        # Ensure non-negative
        self.apparent_count = max(1, self.apparent_count)

    def draw_star(self, x, y, size, depth):
        """Draw a 2D star with pseudo-3D effect based on depth"""
        # Adjust color based on depth for 3D effect
        brightness = int(200 * (0.5 + 0.5 * depth))  # Brighter in front
        color = (min(255, self.star_color[0] + brightness // 3),
                 min(255, self.star_color[1] + brightness // 3),
                 min(255, self.star_color[2] + brightness // 3))

        # Draw a star shape
        points = []
        num_points = 5
        inner_radius = size * 0.4
        outer_radius = size

        for i in range(num_points * 2):
            angle = math.pi / num_points * i
            radius = inner_radius if i % 2 else outer_radius
            points.append((x + radius * math.sin(angle), y + radius * math.cos(angle)))

        pygame.draw.polygon(self.display, color, points)

    def draw_jar(self):
        """Draw a pseudo-3D jar"""
        jar_left = self.jar_center_x - self.jar_width // 2
        jar_right = self.jar_center_x + self.jar_width // 2
        jar_top = self.jar_center_y - self.jar_height // 2
        jar_bottom = self.jar_center_y + self.jar_height // 2

        # Calculate the jar's elliptical appearance based on rotation angle
        squeeze_factor = 0.25 * (1 - abs(math.sin(math.radians(self.rotation_angle))))
        effective_width = int(self.jar_width * (1 - squeeze_factor))

        # Calculate new left and right positions
        jar_left_adjusted = self.jar_center_x - effective_width // 2
        jar_right_adjusted = self.jar_center_x + effective_width // 2

        # Draw jar outline
        pygame.draw.ellipse(self.display, self.jar_outline_color,
                            (jar_left_adjusted, jar_top, effective_width, 20))  # Top rim

        # Draw left and right sides
        pygame.draw.line(self.display, self.jar_outline_color,
                         (jar_left_adjusted, jar_top + 10), (jar_left_adjusted, jar_bottom), 2)
        pygame.draw.line(self.display, self.jar_outline_color,
                         (jar_right_adjusted, jar_top + 10), (jar_right_adjusted, jar_bottom), 2)

        # Draw elliptical bottom
        pygame.draw.ellipse(self.display, self.jar_outline_color,
                            (jar_left_adjusted, jar_bottom - 10, effective_width, 20))

        # Draw some horizontal lines to enhance the 3D appearance
        for i in range(1, 10):
            y = jar_top + (jar_bottom - jar_top) * (i / 10)
            width_adjustment = effective_width * (0.9 + 0.1 * (i / 10))
            x_left = self.jar_center_x - width_adjustment // 2
            line_color = (50, 50, min(255, 100 + i * 15))
            pygame.draw.line(self.display, line_color,
                             (x_left, y), (x_left + width_adjustment, y), 1)

    def render_text(self, text, position, font=None, color=None):
        """Render text on the pygame surface"""
        if font is None:
            font = self.display_font
        if color is None:
            color = self.text_color

        text_surface = font.render(text, True, color)
        self.display.blit(text_surface, position)

    def render_frame(self):
        """Render a single frame of the animation"""
        # Clear the screen
        self.display.fill(self.background_color)

        # Draw the jar
        self.draw_jar()

        # Sort stars by depth for proper rendering (paint back to front)
        depth_sorted_indices = sorted(range(len(self.stars)),
                                      key=lambda i: self.star_depths[i])

        # Draw the stars
        for idx in depth_sorted_indices:
            if self.star_visibility[idx]:
                x, y = self.stars[idx]
                size = self.star_sizes[idx]
                depth = self.star_depths[idx]

                # Adjust x position based on rotation to simulate 3D
                rotation_offset = 30 * math.sin(math.radians(self.rotation_angle)) * self.star_depths[idx]
                x_adjusted = x + rotation_offset

                self.draw_star(x_adjusted, y, size, depth)

        # Render text
        self.render_text(
            f"Current view shows: {self.apparent_count} objects",
            (20, self.display_height - 40)
        )

        self.render_text(
            "Gödelian Indecidability: The exact count cannot be determined",
            (20, self.display_height - 80),
            self.display_small_font
        )

        self.render_text(
            "as the observation itself affects what is countable",
            (20, self.display_height - 110),
            self.display_small_font
        )

        # Update the display
        pygame.display.flip()

    def run_animation(self):
        """Run the main animation loop"""
        running = True
        frame_count = 0

        print("\nGödelian Jar Animation")
        print("=" * 40)
        print("The animation illustrates Gödel's incompleteness theorem:")
        print("Just as there exist statements that cannot be proven true or false")
        print("within a formal system, the exact count of objects in this jar")
        print("is fundamentally indecidable - it changes based on perspective.")
        print("\nControls: ESC to exit")

        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # Update rotation
            self.rotation_angle += self.rotation_speed
            if self.rotation_angle >= 360:
                self.rotation_angle = 0

            # Update object visibility and count periodically
            if frame_count % self.count_update_interval == 0:
                self.update_object_visibility()
                self.update_apparent_count()

            # Render the frame
            self.render_frame()

            frame_count += 1
            self.clock.tick(60)  # Limit to 60 FPS

            # Print debug info occasionally
            if self.debug_mode and frame_count % 120 == 0:
                print(f"Frame {frame_count}, Angle {self.rotation_angle:.1f}°, Count {self.apparent_count}")

        pygame.quit()


if __name__ == "__main__":
    # Check if debug mode is requested
    debug_mode = "--debug" in sys.argv

    # Create and run the animation
    jar_animation = GodelianJar(debug_mode=debug_mode)
    jar_animation.run_animation()