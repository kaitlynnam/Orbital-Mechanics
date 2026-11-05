import matplotlib.pyplot as plt
import numpy as np
from body import Body
import math
from matplotlib.widgets import Button, Slider

import matplotlib.animation as animation

fig = plt.figure() 
ax = fig.add_subplot(projection='3d')

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 10)
# Set an equal aspect ratio
ax.set_aspect('equal')

# earth = Body(10, 0, 0, 40, 450, 5, 0.3)

# sun = Body(0, 0, 0, 1, 0, 50000, 1)

# mars = Body(5, 0, 0, 40, 900, 7, 0.3)


def init_planets():
     global earth, sun, mars

     earth = Body(10, 0, 0, 40, 450, 5, 0.3)

     sun = Body(0, 0, 0, 1, 0, 50000, 1)

     mars = Body(5, 0, 0, 40, 900, 7, 0.3)

body_shapes = []

orbital_path = []

init_planets()

bodies = [sun, earth, mars]

old_accelerations = []
new_accelerations = []

dt = 0.001

for body in bodies:
     body_shapes.append([body, None])

for body in bodies:
     path = [[], [], []]

     orbital_path.append((body, path))

def calculate_accelerations(bodies):
    old_accelerations.clear()
    for body in bodies:
         total_ax = 0
         total_ay = 0

         for other in bodies:
            if body is other:
                continue

            ax, ay = body.acceleration_from(other)

            total_ax += ax
            total_ay += ay

         old_accelerations.append((total_ax, total_ay))

    return old_accelerations     

def velocity_verlet(bodies, dt):
     old_accleration = calculate_accelerations(bodies).copy()

     for body, (ax, ay) in zip (bodies, old_accleration):
          body.center_x += body.vx * dt + 0.5 * ax * dt**2
          body.center_y += body.vy * dt + 0.5 * ay * dt**2

     new_acceleration = calculate_accelerations(bodies)
     
     for body, (ax_old, ay_old), (ax_new, ay_new) in zip (bodies, old_accleration, new_acceleration):

          body.vx += 0.5 * (ax_old + ax_new) * dt
          body.vy += 0.5 * (ay_old + ay_new) * dt
          new_accelerations.append((ax_new, ay_new))

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

arrows = []

def get_arrows(bodies):

  
     for arrow in arrows:
          arrow.remove()
     arrows.clear()

     
     for body in bodies:
          
          x, y, z = body.center_x, body.center_y, body.center_z

          vx, vy = body.vx, body.vy

          # return [ax.quiver(x, y, z, u, y, z, color='red', arrow_length_ratio=0.1), ax.quiver(x, y, z, x, v, z, color='red', arrow_length_ratio=0.1)]
          # arrow = ax.quiver(x, y, z, u, v, z, color='red', arrow_length_ratio=0.1)
          arrow = ax.quiver(x, y, z, 0.01 * vx, 0.01 * vy, 0, color='red', arrow_length_ratio=0.1)
          arrows.append(arrow)    



def sun_sliders():
     global sun_size
     slider_ax = fig.add_axes([0.2, 0.07, 0.6, 0.03])
     sun_size = Slider(
               ax=slider_ax,
               label='sun size',
               valmin=30000,
               valmax=100000,
               valinit=50000,
          )
     sun_size.on_changed(update_sun_radius)

def update_sun_radius(value):
     sun.mass = value 

sun_sliders()
     

def animate(i):
    velocity_verlet(bodies, dt)
    get_arrows(bodies)
    

    create_planets()

#     get_orbit()

    



anim = animation.FuncAnimation(fig, animate, 
                            frames = 3000,
                            interval = 20, 
                            blit = False) 

# saves the animation in our desktop 
# anim.save('growingCoil.gif', writer = 'pillow', fps = 30) 


if __name__ == "__main__":
     plt.show()
