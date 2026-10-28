import numpy as np
import math

class Body:

    G = 6.6743 * 10

    def __init__(self, center_x, center_y, center_z, vx, vy, mass, radius):
        self.center_x = center_x
        self.center_y = center_y
        self.center_z = center_z
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.radius = radius
        # self.color = color
        self.orbit = []

    def get_planet(self):
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)

        
        x = self.radius * np.outer(np.cos(u), np.sin(v))
        y = self.radius * np.outer(np.sin(u), np.sin(v))
        z = self.radius * np.outer(np.ones(np.size(u)), np.cos(v))

        return [x + self.center_x, y + self.center_y, z + self.center_z]


    def calculate_interactions(self, other_body, timestep):

        dx = other_body.center_x - self.center_x
        dy = other_body.center_y - self.center_y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        force = (self.G * self.mass * other_body.mass) / distance ** 2

        theta = math.atan2(dy, dx)
        fx = force * math.cos(theta)
        fy = force * math.sin(theta)

        ax = fx / self.mass
        ay = fy / self.mass

        self.vx += ax * timestep
        self.vy += ay * timestep

        self.center_x += self.vx * timestep
        self.center_y += self.vy * timestep
