import pygame
import math
import random
import sys
import numpy as np
from pygame import gfxdraw


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

        # Get screen info for fullscreen
        screen_info = pygame.display.Info()
        self.display_width = screen_info.current_w
        self.display_height = screen_info.current_h

        # Create fullscreen display surface
        self.display = pygame.display.set_mode((self.display_width, self.display_height), pygame.FULLSCREEN)
        pygame.display.set_caption("Gödelian Jar: The Undecidable Counting Problem")

        # Set background color
        self.background_color = (0, 0, 0)  # Black
        self.display.fill(self.background_color)

        # Calculate jar dimensions based on screen size
        jar_height_ratio = 0.6  # Jar takes up 60% of screen height
        self.jar_height = int(self.display_height * jar_height_ratio)
        self.jar_width = int(self.jar_height * 0.5)  # Width is half of height

        # Center the jar horizontally, position it in upper part of screen
        self.jar_center_x = self.display_width // 2
        jar_top_margin = int(self.display_height * 0.15)  # 15% from top of screen
        self.jar_center_y = jar_top_margin + self.jar_height // 2
        self.jar_bottom_y = self.jar_center_y + self.jar_height // 2

        # Calculate text area boundaries
        self.text_top = self.jar_center_y + self.jar_height // 2 + 20  # Start text 20px below jar

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

        # Create fonts with sizes relative to screen resolution
        font_size_large = max(24, int(self.display_height * 0.03))
        font_size_normal = max(18, int(self.display_height * 0.022))
        font_size_small = max(16, int(self.display_height * 0.018))

        self.display_font = pygame.font.SysFont('Arial', font_size_large)
        self.display_small_font = pygame.font.SysFont('Arial', font_size_normal)
        self.display_title_font = pygame.font.SysFont('Arial', int(font_size_large * 1.2), bold=True)
        self.display_explanation_font = pygame.font.SysFont('Arial', font_size_small)

        self.count_update_interval = 10  # Frames between count updates

        # Define colors
        self.jar_color = (70, 130, 180, 128)  # Steel blue, semi-transparent
        self.jar_outline_color = (135, 206, 250)  # Light sky blue for outlines
        self.star_color = (218, 165, 32)  # Golden color for stars
        self.text_color = (255, 255, 255)  # White for text
        self.highlight_color = (255, 215, 0)  # Gold for highlights
        self.grid_color = (50, 50, 120)  # Dark blue for grid

        # Gödel's Theorem References
        self.godel_statements = [
            "Formal system cannot prove its own consistency",
            "Self-reference creates paradoxes that are undecidable",
            "What can be counted depends on the counting system",
            "The observer affects the observation",
            "Truth exists beyond what can be proven"
        ]
        self.current_statement = 0
        self.statement_fade = 255  # For fading effects
        self.statement_change_interval = 180  # Change statement every 3 seconds

        # Additional visualization features
        self.show_counting_attempt = False
        self.counting_progress = 0
        self.counting_target = 0
        self.counting_error = False

        # Store formal system boundaries (axiomatic visualization)
        self.axiom_boundaries = []
        for _ in range(4):
            self.axiom_boundaries.append({
                'x': random.randint(int(self.display_width * 0.1), int(self.display_width * 0.9)),
                'y': random.randint(int(self.display_height * 0.1), int(self.display_height * 0.9)),
                'size': random.randint(20, 50),
                'speed': random.uniform(0.2, 0.7)
            })

        # Track FPS
        self.clock = pygame.time.Clock()

    def generate_objects(self):
        """Generate coordinates for objects within the jar"""
        self.stars = []
        self.star_visibility = []
        self.star_depths = []  # For pseudo-3D effect
        self.star_sizes = []  # Size for each star
        self.star_flicker = []  # For quantum uncertainty visualization
        self.star_godel_status = []  # Stars that illustrate Gödel's theorem

        # Calculate jar boundaries
        jar_left = self.jar_center_x - self.jar_width // 2
        jar_right = self.jar_center_x + self.jar_width // 2
        jar_top = self.jar_center_y - self.jar_height // 2
        jar_bottom = self.jar_center_y + self.jar_height // 2

        # Generate stars
        for i in range(self.num_objects):
            # Generate position inside jar
            # Use an elliptical distribution to simulate 3D cylinder
            angle = random.uniform(0, 2 * math.pi)
            radius_factor = random.uniform(0, 0.95) ** 0.5  # Square root for uniform distribution in circle

            # Depth in the jar (for pseudo-3D)
            depth = random.uniform(-1.0, 1.0)  # -1 is back, 1 is front

            # Adjust radius based on depth to create 3D cylinder illusion
            effective_width = self.jar_width * (0.5 + 0.5 * (1 - abs(depth)) ** 2)

            # Calculate position
            x = self.jar_center_x + radius_factor * effective_width / 2 * math.cos(angle)
            y = jar_top + random.uniform(0.1, 0.9) * self.jar_height

            self.stars.append((x, y))
            self.star_depths.append(depth)

            # Size varies with depth and screen resolution
            base_size = self.display_height * 0.005  # Base size relative to screen height
            size = random.uniform(base_size, base_size * 2) * (1 - 0.5 * abs(depth))
            self.star_sizes.append(size)

            # Initial visibility (some stars may be temporarily invisible)
            self.star_visibility.append(random.random() > 0.1)  # 90% initially visible

            # Flicker rate for quantum uncertainty visualization
            self.star_flicker.append(random.uniform(0.02, 0.1))

            # Mark some stars as special "Gödel stars" that behave paradoxically
            # These stars will change in ways that contradict counting logic
            self.star_godel_status.append(i % 8 == 0)  # Every 8th star is a "Gödel star"

    def update_object_visibility(self):
        """Update which objects are visible (simulating quantum indeterminacy)"""
        # Update based on the rotation angle
        angle_factor = abs(math.sin(math.radians(self.rotation_angle)))

        for i in range(self.num_objects):
            # Regular quantum indeterminacy
            if random.random() < self.star_flicker[i]:
                self.star_visibility[i] = not self.star_visibility[i]

            # Special behavior for "Gödel stars" - they behave paradoxically
            if self.star_godel_status[i]:
                # These stars are more likely to appear/disappear when you try to count them
                if self.show_counting_attempt and random.random() < 0.2:
                    self.star_visibility[i] = not self.star_visibility[i]

                # They also respond to viewing angle in counter-intuitive ways
                if angle_factor > 0.7 and random.random() < 0.15:
                    self.star_visibility[i] = not self.star_visibility[i]

    def update_apparent_count(self):
        """Update the apparent count based on current view and Gödelian undecidability"""
        # Count actually visible objects
        true_visible = sum(self.star_visibility)

        # Base angle-dependent factor
        angle_factor = math.sin(math.radians(self.rotation_angle * 2))

        # Gödel factor: the more precisely we try to count, the more uncertain it becomes
        godel_factor = 1.0
        if self.show_counting_attempt:
            # As counting progresses, uncertainty increases
            godel_factor = 1.0 + (self.counting_progress / 100) * 0.5

        # The apparent count fluctuates with multiple factors
        count_variation = int(angle_factor * self.uncertainty * godel_factor)

        # The apparent count fluctuates around true_visible
        self.apparent_count = true_visible + count_variation

        # Ensure non-negative
        self.apparent_count = max(1, self.apparent_count)

        # Decide if we should show counting error (occurs when trying to count)
        if self.show_counting_attempt and self.counting_progress > 50:
            self.counting_error = random.random() < 0.2  # 20% chance of counting error

    def draw_star(self, x, y, size, depth, is_godel_star=False):
        """Draw a 2D star with pseudo-3D effect based on depth"""
        # Adjust color based on depth for 3D effect
        brightness = int(200 * (0.5 + 0.5 * depth))  # Brighter in front

        if is_godel_star:
            # Gödel stars are golden/yellow to highlight their special nature
            base_color = self.highlight_color
        else:
            base_color = self.star_color

        color = (min(255, base_color[0] + brightness // 3),
                 min(255, base_color[1] + brightness // 3),
                 min(255, base_color[2] + brightness // 3))

        # Draw a star shape
        points = []
        num_points = 5
        inner_radius = size * 0.4
        outer_radius = size

        for i in range(num_points * 2):
            angle = math.pi / num_points * i
            radius = inner_radius if i % 2 else outer_radius
            points.append((x + radius * math.sin(angle), y + radius * math.cos(angle)))

        # Draw the star
        if is_godel_star and self.show_counting_attempt:
            # Add a subtle glow effect for Gödel stars when counting
            glow_color = (min(255, color[0]), min(255, color[1]), min(255, color[2]))
            glow_radius = outer_radius * 2
            pygame.draw.circle(self.display, (glow_color[0] // 8, glow_color[1] // 8, glow_color[2] // 8),
                               (int(x), int(y)), int(glow_radius))

        pygame.draw.polygon(self.display, color, points)

        # For Gödel stars, add a small indicator when counting
        if is_godel_star and self.show_counting_attempt:
            # Add a small dot in the center to mark it
            gfxdraw.filled_circle(self.display, int(x), int(y), 1, (255, 255, 255))

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

        # Draw jar - semitransparent blue
        s = pygame.Surface((effective_width, self.jar_height), pygame.SRCALPHA)
        s.fill((70, 130, 180, 50))  # Semi-transparent blue
        self.display.blit(s, (jar_left_adjusted, jar_top))

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

        # Draw a grid inside the jar to represent "formal system boundaries"
        # This grid represents the axiomatic framework we're working within
        if random.random() < 0.3:  # Only show occasionally for effect
            grid_spacing = 30
            grid_alpha = 40 + int(15 * math.sin(math.radians(self.rotation_angle * 3)))

            for x in range(jar_left_adjusted + 20, jar_right_adjusted, grid_spacing):
                # Vertical lines
                pygame.draw.line(self.display, self.grid_color + (grid_alpha,),
                                 (x, jar_top + 20), (x, jar_bottom - 20), 1)

            for y in range(jar_top + 20, jar_bottom, grid_spacing):
                # Horizontal lines
                line_width = jar_right_adjusted - jar_left_adjusted - 40
                pygame.draw.line(self.display, self.grid_color + (grid_alpha,),
                                 (jar_left_adjusted + 20, y), (jar_left_adjusted + line_width, y), 1)

    def draw_axiom_boundaries(self):
        """Draw visualization of formal system boundaries"""
        # Update the positions of the axiom boundaries
        for boundary in self.axiom_boundaries:
            boundary['x'] += math.cos(math.radians(self.rotation_angle * boundary['speed'])) * 0.5
            boundary['y'] += math.sin(math.radians(self.rotation_angle * boundary['speed'])) * 0.5

        # Draw the boundaries as shimmering circles that intersect
        for i, boundary in enumerate(self.axiom_boundaries):
            color_pulse = int(127 + 127 * math.sin(math.radians(self.rotation_angle * boundary['speed'] * 5)))
            boundary_color = (30, 30, min(200, 50 + color_pulse))

            pygame.draw.circle(self.display, boundary_color,
                               (int(boundary['x']), int(boundary['y'])), boundary['size'], 1)

            # Connect axioms with lines to show their relationships
            if i < len(self.axiom_boundaries) - 1:
                next_boundary = self.axiom_boundaries[i + 1]
                pygame.draw.line(self.display, (20, 20, 80, 100),
                                 (int(boundary['x']), int(boundary['y'])),
                                 (int(next_boundary['x']), int(next_boundary['y'])), 1)

    def draw_undecidability_visualization(self):
        """Draw additional visual elements to represent undecidability"""
        # Only show during counting attempts to illustrate the paradox
        if not self.show_counting_attempt:
            return

        # Draw a "counting path" that tries to count stars but gets confused
        jar_center_x = self.jar_center_x
        jar_center_y = self.jar_center_y

        # Calculate the percentage of stars we've attempted to count
        count_percentage = self.counting_progress / 100.0

        # Draw an increasingly chaotic counting path
        points = []
        radius = self.jar_width * 0.3
        for i in range(20):
            angle = i / 20 * count_percentage * math.pi * 4
            # As count progresses, the path gets more chaotic
            chaos = 1.0 + count_percentage * 5.0 * (i / 20)
            x = jar_center_x + radius * math.cos(angle) * (1 + 0.2 * math.sin(chaos * angle))
            y = jar_center_y + radius * math.sin(angle) * (1 + 0.2 * math.cos(chaos * angle))
            points.append((x, y))

        # Draw lines connecting the points
        if len(points) > 1:
            # Make line fade as the counting error increases
            line_color = (200, 200, 200, max(50, 255 - int(self.counting_progress * 2)))
            for i in range(len(points) - 1):
                pygame.draw.line(self.display, line_color, points[i], points[i + 1], 1)

        # If counting error, draw error indicators
        if self.counting_error:
            error_alpha = int(127 + 127 * math.sin(math.radians(self.rotation_angle * 10)))
            error_color = (255, 50, 50, error_alpha)

            # Draw X symbols to indicate counting errors
            for _ in range(3):
                x = jar_center_x + random.randint(-self.jar_width // 3, self.jar_width // 3)
                y = jar_center_y + random.randint(-self.jar_height // 3, self.jar_height // 3)

                # Draw X
                size = random.randint(5, 15)
                pygame.draw.line(self.display, error_color, (x - size, y - size), (x + size, y + size), 2)
                pygame.draw.line(self.display, error_color, (x - size, y + size), (x + size, y - size), 2)

    def render_text(self, text, position, font=None, color=None, align='left'):
        """Render text on the pygame surface"""
        if font is None:
            font = self.display_font
        if color is None:
            color = self.text_color

        text_surface = font.render(text, True, color)

        # Adjust position based on alignment
        if align == 'center':
            position = (position[0] - text_surface.get_width() // 2, position[1])
        elif align == 'right':
            position = (position[0] - text_surface.get_width(), position[1])

        self.display.blit(text_surface, position)
        return text_surface.get_height()

    def render_frame(self):
        """Render a single frame of the animation"""
        # Clear the screen
        self.display.fill(self.background_color)

        # Draw axiom boundaries in the background
        self.draw_axiom_boundaries()

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
                is_godel_star = self.star_godel_status[idx]

                # Adjust x position based on rotation to simulate 3D
                rotation_offset = 30 * math.sin(math.radians(self.rotation_angle)) * self.star_depths[idx]
                x_adjusted = x + rotation_offset

                self.draw_star(x_adjusted, y, size, depth, is_godel_star)

        # Draw undecidability visualization
        self.draw_undecidability_visualization()

        # Render title at top
        title_height = self.render_text(
            "Gödelian Jar: The Undecidable Counting Problem",
            (self.display_width // 2, int(self.display_height * 0.05)),
            self.display_title_font,
            align='center'
        )

        # Calculate text positions based on screen height
        # Start text area at the bottom of the jar
        text_start_y = self.jar_center_y + (self.jar_height // 2) + int(self.display_height * 0.05)

        # Calculate spacing between text sections
        section_spacing = int(self.display_height * 0.03)

        # Render the current object count
        count_height = self.render_text(
            f"Current view shows: {self.apparent_count} objects",
            (int(self.display_width * 0.05), text_start_y),
            self.display_font,
            self.highlight_color if self.show_counting_attempt else self.text_color
        )

        # Show counting status if active
        if self.show_counting_attempt:
            progress_text = f"Counting attempt: {self.counting_progress:.1f}% complete"
            if self.counting_error:
                progress_text += " - COUNTING ERROR DETECTED"
                color = (255, 100, 100)
            else:
                color = (100, 255, 100)

            count_status_height = self.render_text(
                progress_text,
                (int(self.display_width * 0.05), text_start_y + count_height + 10),
                self.display_small_font,
                color
            )
            # Adjust next text position if showing counting status
            next_section_y = text_start_y + count_height + count_status_height + section_spacing
        else:
            next_section_y = text_start_y + count_height + section_spacing

        # Render the current Gödel statement with fading effect
        statement = self.godel_statements[self.current_statement]
        statement_height = self.render_text(
            f"Gödel's Insight: {statement}",
            (self.display_width // 2, next_section_y),
            self.display_font,
            (self.text_color[0], self.text_color[1], self.text_color[2], self.statement_fade),
            align='center'
        )

        # Render explanation
        explanation = [
            "This jar contains objects that resist being counted precisely.",
            "As you try to observe and count them, their very nature changes.",
            "Just as Gödel proved some mathematical truths cannot be proven,",
            "the exact count in this jar is fundamentally undecidable."
        ]

        explanation_start_y = next_section_y + statement_height + section_spacing
        line_spacing = int(self.display_height * 0.025)

        for i, line in enumerate(explanation):
            self.render_text(
                line,
                (self.display_width // 2, explanation_start_y + i * line_spacing),
                self.display_explanation_font,
                align='center'
            )

        # Render controls at the bottom
        controls_y = self.display_height - int(self.display_height * 0.05)
        self.render_text(
            "Controls: SPACE - Start/stop counting attempt | R - Reset | ESC - Exit",
            (self.display_width // 2, controls_y),
            self.display_small_font,
            align='center'
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
        print("is fundamentally undecidable - it changes based on perspective.")
        print("\nControls:")
        print("  ESC - Exit")
        print("  SPACE - Start/stop counting attempt (illustrates undecidability)")
        print("  R - Reset simulation")

        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        # Toggle counting attempt visualization
                        self.show_counting_attempt = not self.show_counting_attempt
                        if self.show_counting_attempt:
                            self.counting_progress = 0
                            self.counting_error = False
                    elif event.key == pygame.K_r:
                        # Reset the simulation
                        self.show_counting_attempt = False
                        self.counting_progress = 0
                        self.counting_error = False
                        self.generate_objects()
                    elif event.key == pygame.K_f:
                        # Toggle fullscreen
                        pygame.display.toggle_fullscreen()

            # Update rotation
            self.rotation_angle += self.rotation_speed
            if self.rotation_angle >= 360:
                self.rotation_angle = 0

            # Update object visibility and count periodically
            if frame_count % self.count_update_interval == 0:
                self.update_object_visibility()
                self.update_apparent_count()

            # Update Gödel statement periodically
            if frame_count % self.statement_change_interval == 0:
                self.current_statement = (self.current_statement + 1) % len(self.godel_statements)
                self.statement_fade = 255  # Reset fade

            # Fade the statement over time
            if frame_count % 2 == 0 and self.statement_fade > 180:
                self.statement_fade -= 1

            # Update counting progress if active
            if self.show_counting_attempt and self.counting_progress < 100:
                # Increase counting progress, but slow down as it approaches 100%
                # This represents increasing difficulty in completing the count
                progress_increment = 0.5 * (1.0 - self.counting_progress / 200)
                self.counting_progress = min(100, self.counting_progress + progress_increment)

                # If we're getting close to 100%, increase chance of counting error
                if self.counting_progress > 90 and random.random() < 0.1:
                    self.counting_error = True

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