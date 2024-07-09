import matplotlib.pyplot as plt
import numpy as np

# Define Ball Class
class Ball:
    def __init__(self, position, mass=1.0, radius=0.05, coeff_visco=0.001):
        self.position = np.array(position, dtype=float)
        self.velocity = np.zeros(2)
        self.acceleration = np.zeros(2)
        self.mass = mass
        self.radius = radius
        self.coeff_visco = 6*np.pi*radius*coeff_visco

    def applyForce(self, force):
        self.acceleration += force / self.coeff_visco

    def update(self):
        #random force normally distributed
        random_force = np.random.normal(loc=0, scale=1e-3, size=2)
        self.applyForce(random_force)
        self.velocity = self.acceleration
        self.position += self.velocity
        self.acceleration *= 0
        self.velocity *= 0

    def display(self, ax):
        circle = plt.Circle(self.position, self.radius, color='r', fill=True)
        ax.add_artist(circle)

# Define Spring Class
class Spring:
    def __init__(self, ball1, ball2, k=1e-4, rest_length=1.0):
        self.ball1 = ball1
        self.ball2 = ball2
        self.k = k
        self.rest_length = rest_length

    def update(self):
        force_dir = self.ball2.position - self.ball1.position
        distance = np.linalg.norm(force_dir)
        force_dir /= distance  # Normalize
        force_magnitude = self.k * (distance - self.rest_length)
        force = force_dir * force_magnitude

        self.ball1.applyForce(force)
        self.ball2.applyForce(-force)
        self.ball1.update()
        self.ball2.update()

    def display(self, ax):
        ax.plot([self.ball1.position[0], self.ball2.position[0]], [self.ball1.position[1], self.ball2.position[1]], 'k-')

# # Initialize System
# balls = [Ball([0.5, 0.5]), Ball([0.6, 0.5])]
# spring = Spring(balls[0], balls[1])

# # Simulation Loop (simplified for demonstration)
# fig, ax = plt.subplots()
# #ax.set_xlim(0, 1)
# #ax.set_ylim(0, 1)
# time = []
# ball1_posx = []
# for t in range(100):  # Simulate 100 steps
#     for ball in balls:
#         ball.applyForce(np.array([0,-0.01]))  # Gravity
#         ball.update()
#         #ball.display(ax)
#         spring.update()
#         #spring.display(ax)
#     ball1_posx.append(ball.position[1])
#     time.append(t)
# plt.plot(time,ball1_posx, 'k-')
# plt.show()