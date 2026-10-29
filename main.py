import matplotlib.pyplot as plt
import numpy as np
from body import Body

import matplotlib.animation as animation

fig = plt.figure() 
ax = fig.add_subplot(projection='3d')

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 10)
# Set an equal aspect ratio
ax.set_aspect('equal')

earth = Body(10, 0, 0, 90, 450, 5, 0.3)

sun = Body(0, 0, 0, 1, 0, 50000, 1)

mars = Body(5, 0, 0, 40, 900, 7, 0.3)


body_shapes = []

orbital_path = []

bodies = [sun, earth, mars]

accelerations = []

dt = 0.001

for body in bodies:
     body_shapes.append([body, None])

for body in bodies:
     path = [[], [], []]

     orbital_path.append((body, path))

def calculate_accelerations(bodies):
    accelerations.clear()
    for body in bodies:
         total_ax = 0
         total_ay = 0

         for other in bodies:
            if body is other:
                continue

            ax, ay = body.acceleration_from(other)

            total_ax += ax
            total_ay += ay

         accelerations.append((total_ax, total_ay))


def update_positions():
     for body, (ax, ay) in zip(bodies, accelerations):
          body.vx += ax * dt
          body.vy += ay * dt

          body.center_x += body.vx * dt
          body.center_y += body.vy * dt

def create_planets():

    color = ["gold", "blue", "red"]

    for entry, color, path in zip(body_shapes, color, orbital_path):
         body, shape = entry

         if shape is not None:
                shape.remove()

         x, y, z = body.get_planet()
         entry[1] = ax.plot_surface(x, y, z, color=color)

         orbit_x, orbit_y, orbit_z = body.get_planet_orbit()

         path[1][0].append(orbit_x)
         path[1][1].append(orbit_y)
         path[1][2].append(orbit_z)

def get_orbit():
     for planet in orbital_path:

          x = planet[1][0]
          y = planet[1][1]
          z = planet[1][2]
          ax.plot( x, y, z, linewidth= '1', color="black")

def animate(i):
    calculate_accelerations(bodies)
    update_positions()

    create_planets()

    get_orbit()


anim = animation.FuncAnimation(fig, animate, 
                            frames = 3000,
                            interval = 20, 
                            blit = False) 

# saves the animation in our desktop 
# anim.save('growingCoil.gif', writer = 'pillow', fps = 30) 


if __name__ == "__main__":
     plt.show()
