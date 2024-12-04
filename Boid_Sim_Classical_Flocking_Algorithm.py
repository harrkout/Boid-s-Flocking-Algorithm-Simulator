
import pygame
import random
import math

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Boid settings
NUM_BOIDS = 50
MAX_SPEED = 4
MAX_FORCE = 0.1
BOID_RADIUS = 5
PERCEPTION_RADIUS = 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)

# Flags for features
mouse_attraction = False
show_metrics = False
enable_predator = False


class Boid:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity.scale_to_length(MAX_SPEED)
        self.acceleration = pygame.Vector2(0, 0)

    def edges(self):
        """Wrap around the screen."""
        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y > HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = HEIGHT

    def align(self, boids):
        """Steer towards the average heading of nearby boids."""
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in boids:
            if other != self and self.position.distance_to(other.position) < PERCEPTION_RADIUS:
                steering += other.velocity
                total += 1
        if total > 0:
            steering /= total
            steering.scale_to_length(MAX_SPEED)
            steering -= self.velocity
            steering = self.limit_force(steering)
        return steering

    def cohesion(self, boids):
        """Move towards the center of mass of nearby boids."""
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in boids:
            if other != self and self.position.distance_to(other.position) < PERCEPTION_RADIUS:
                steering += other.position
                total += 1
        if total > 0:
            steering /= total
            steering -= self.position
            steering.scale_to_length(MAX_SPEED)
            steering -= self.velocity
            steering = self.limit_force(steering)
        return steering

    def separation(self, boids):
        """Avoid crowding nearby boids."""
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in boids:
            distance = self.position.distance_to(other.position)
            if other != self and distance < PERCEPTION_RADIUS / 2:
                diff = self.position - other.position
                diff /= distance
                steering += diff
                total += 1
        if total > 0:
            steering /= total
            steering.scale_to_length(MAX_SPEED)
            steering -= self.velocity
            steering = self.limit_force(steering)
        return steering

    def seek_mouse(self, mouse_pos, repel=False):
        """Attract or repel boids to/from the mouse."""
        target = pygame.Vector2(mouse_pos)
        direction = target - self.position if not repel else self.position - target
        if direction.length() > 0:
            direction.scale_to_length(MAX_SPEED)
            steering = direction - self.velocity
            steering = self.limit_force(steering)
            self.acceleration += steering

    def avoid_predator(self, predator_pos):
        """Avoid a predator boid."""
        if self.position.distance_to(predator_pos) < PERCEPTION_RADIUS:
            diff = self.position - predator_pos
            diff.scale_to_length(MAX_SPEED)
            steering = diff - self.velocity
            self.acceleration += self.limit_force(steering)

    def limit_force(self, force):
        """Limit the magnitude of a steering force."""
        if force.length() > MAX_FORCE:
            force.scale_to_length(MAX_FORCE)
        return force

    def flock(self, boids):
        """Apply the three rules of flocking."""
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)
        self.acceleration += alignment + cohesion + separation

    def update(self):
        """Update position, velocity, and acceleration."""
        self.velocity += self.acceleration
        if self.velocity.length() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)
        self.position += self.velocity
        self.acceleration *= 0

    def draw(self, screen):
        """Draw the boid as a triangle."""
        angle = math.atan2(self.velocity.y, self.velocity.x)
        point1 = self.position + pygame.Vector2(math.cos(angle), math.sin(angle)) * BOID_RADIUS
        point2 = self.position + pygame.Vector2(math.cos(angle + 2.5), math.sin(angle + 2.5)) * BOID_RADIUS
        point3 = self.position + pygame.Vector2(math.cos(angle - 2.5), math.sin(angle - 2.5)) * BOID_RADIUS
        pygame.draw.polygon(screen, BLUE, [point1, point2, point3])


def calculate_metrics(boids):
    """Calculate and return metrics for the flock."""
    total_speed = sum(boid.velocity.length() for boid in boids)
    average_speed = total_speed / len(boids)

    center_of_mass = pygame.Vector2(
        sum(boid.position.x for boid in boids) / len(boids),
        sum(boid.position.y for boid in boids) / len(boids),
    )
    cohesion_measure = sum(boid.position.distance_to(center_of_mass) for boid in boids) / len(boids)

    return average_speed, cohesion_measure


def display_menu(screen, font):
    """Display the menu for toggling features."""
    menu_texts = [
        "Press 1: Toggle Mouse Attraction",
        "Press 2: Toggle Predator",
        "Press 3: Show Metrics",
        "Press Esc: Quit",
    ]
    for i, text in enumerate(menu_texts):
        menu_surface = font.render(text, True, WHITE)
        screen.blit(menu_surface, (10, 10 + i * 20))


def display_metrics(screen, font, average_speed, cohesion_measure):
    """Display real-time metrics on the screen."""
    metrics_texts = [
        f"Average Speed: {average_speed:.2f}",
        f"Cohesion Measure: {cohesion_measure:.2f}",
    ]
    for i, text in enumerate(metrics_texts):
        metrics_surface = font.render(text, True, YELLOW)
        screen.blit(metrics_surface, (10, HEIGHT - 40 + i * 20))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Interactive Boid Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Create boids
    boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_BOIDS)]

    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    global mouse_attraction
                    mouse_attraction = not mouse_attraction
                elif event.key == pygame.K_2:
                    global enable_predator
                    enable_predator = not enable_predator
                elif event.key == pygame.K_3:
                    global show_metrics
                    show_metrics = not show_metrics
                elif event.key == pygame.K_ESCAPE:
                    running = False

        mouse_pos = pygame.mouse.get_pos()
        for boid in boids:
            boid.edges()
            boid.flock(boids)
            if mouse_attraction:
                boid.seek_mouse(mouse_pos)
            if enable_predator:
                boid.avoid_predator(mouse_pos)
            boid.update()
            boid.draw(screen)

        if enable_predator:
            pygame.draw.circle(screen, RED, mouse_pos, 10)

        if show_metrics:
            average_speed, cohesion_measure = calculate_metrics(boids)
            display_metrics(screen, font, average_speed, cohesion_measure)

        display_menu(screen, font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
