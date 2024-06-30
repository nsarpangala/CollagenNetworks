import numpy as np
from ball_spring_class import Ball, Spring
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

class FilamentNetwork:
    def __init__(self, num_balls, area_size, max_connections=3):
        self.balls = [Ball(np.random.rand(2) * area_size) for _ in range(num_balls)]
        self.filaments = []
        # Connect balls with filaments randomly
        for ball in self.balls:
            connections = np.random.choice(self.balls, max_connections, replace=False)
            for connection in connections:
                if ball != connection:  # Avoid connecting a ball to itself
                    self.filaments.append(Spring(ball, connection))

    def update(self):
        for ball in self.balls:
            ball.applyForce(np.array([0, -0.01]))  # Example: gravity
            ball.acceleration = np.zeros(2)  # Reset acceleration after applying force
            ball.velocity *= 0.99  # Damping
            ball.position += ball.velocity  # Update position based on velocity

        for filament in self.filaments:
            filament.update()

    def display(self, ax):
        ax.clear()
        ax.set_xlim(0, 3)
        ax.set_ylim(0, 3)
        for ball in self.balls:
            circle = plt.Circle(ball.position, ball.radius, color='r')
            ax.add_artist(circle)
        for filament in self.filaments:
            line = plt.Line2D((filament.ball1.position[0], filament.ball2.position[0]),
                              (filament.ball1.position[1], filament.ball2.position[1]), lw=1)
            ax.add_artist(line)


# class Fiber:
#     def __init__(self, start_pos, num_segments, segment_length):
#         self.segments = [Ball(start_pos + np.array([segment_length * i, 0])) for i in range(num_segments)]
#         self.filaments = [Spring(self.segments[i], self.segments[i+1]) for i in range(num_segments - 1)]

#     def update(self):
#         for filament in self.filaments:
#             filament.update()

class FiberNetwork:
    def __init__(self, num_fibers, num_segments_per_fiber, segment_length, area_size):
        self.fibers = [Fiber(area_size, num_segments_per_fiber, segment_length) for _ in range(num_fibers)]
        self.area_size = area_size
        self.color_map = get_cmap('viridis', num_fibers)

    def update(self):
        for fiber in self.fibers:
            fiber.update()

    def display(self, ax):
        ax.clear()
        ax.set_xlim(0, self.area_size)
        ax.set_ylim(0, self.area_size)

        for idx, fiber in enumerate(self.fibers):
            color = self.color_map(idx) 
            # for segment in fiber.segments:
            #     circle = plt.Circle(segment.position, segment.radius, color='r')
            #     ax.add_artist(circle)
            for filament in fiber.springs:
                line = plt.Line2D((filament.ball1.position[0], filament.ball2.position[0]),
                                  (filament.ball1.position[1], filament.ball2.position[1]), lw=1, color=color)
                ax.add_artist(line)


# class Network:
#     def __init__(self, num_fibers, fiber_length=10):
#         self.fibers = []
#         for _ in range(num_fibers):
#             segments = [Ball(np.random.rand(2) * 100, np.random.rand() * 0.5 + 0.1) for _ in range(fiber_length)]
#             filaments = [Filament(segments[i], segments[i+1]) for i in range(fiber_length-1)]
#             self.fibers.append(Fiber(segments, filaments))

#     def display(self):
#         fig, ax = plt.subplots()
#         for fiber in self.fibers:
#             for segment in fiber.segments:
#                 circle = plt.Circle(segment.position, segment.radius, color='r')
#                 ax.add_artist(circle)
#             for filament in fiber.filaments:
#                 line = plt.Line2D((filament.ball1.position[0], filament.ball2.position[0]),
#                                   (filament.ball1.position[1], filament.ball2.position[1]), lw=1)
#                 ax.add_artist(line)
#         ax.set_xlim(0, 100)
#         ax.set_ylim(0, 100)
#         plt.show()

class Fiber:
    def __init__(self, area_size, num_segments, segment_length, deviation=0.75):
        self.balls = [Ball(np.random.rand(2) * area_size)]
        self.springs = []
        current_direction = np.array([np.random.random(), np.random.random()])

        for i in range(1, num_segments):
            # Add randomness to the direction
            angle = np.random.uniform(-deviation, deviation)
            rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
            current_direction = np.dot(rotation_matrix, current_direction)
            
            # Calculate the new position based on the direction and segment length
            new_position = self.balls[-1].position + current_direction * segment_length
            new_ball = Ball(new_position)
            self.balls.append(new_ball)
            
            # Connect the new ball with a spring to the previous ball
            new_spring = Spring(self.balls[-2], self.balls[-1])
            self.springs.append(new_spring)

    def update(self):
        ball1 = self.balls[0]
        ball1.applyForce(np.array([1e-3, 0.0]))  # Example: External force
        for spring in self.springs:
            spring.update()