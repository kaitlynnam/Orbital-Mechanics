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

earth = Body(10, 0, 0, 90, 578, 5, 0.3)

sun = Body(0, 0, 0, 1, 0, 50000, 1)

mars = Body(5, 0, 0, 40, 900, 7, 0.3)

earth_shape = None
sun_shape = None
mars_shape = None

def create_planets():

    global earth_shape
    global sun_shape
    global mars_shape

    

    if earth_shape is not None:
        earth_shape.remove()

    if sun_shape is not None:
        sun_shape.remove()

    if mars_shape is not None:
            mars_shape.remove()

    earth_x, earth_y, earth_z = earth.get_planet()
    earth_shape = ax.plot_surface(earth_x, earth_y, earth_z, color="blue")

    sun_x, sun_y, sun_z = sun.get_planet()
    sun_shape = ax.plot_surface(sun_x, sun_y, sun_z, color="gold")

    mars_x, mars_y, mars_z = mars.get_planet()
    mars_shape = ax.plot_surface(mars_x, mars_y, mars_z, color="red")


def animate(i):
    


    # sphere.remove()

    # t = i * 0.05

    

    # center_x = 8 * np.cos(t)
    # center_y = 8 * np.sin(t)
    # center_z = 0


    # sphere = ax.plot_surface(x + center_x,
    #                         y + center_y,
    #                         z + center_z)
    # return sphere

    
    earth.calculate_interactions(sun, 0.001)
    sun.calculate_interactions(earth, 0.001)
    mars.calculate_interactions(sun, 0.001)

    create_planets()


anim = animation.FuncAnimation(fig, animate, 
                            frames = 3000,
                            interval = 20, 
                            blit = False) 

# saves the animation in our desktop 
# anim.save('growingCoil.gif', writer = 'pillow', fps = 30) 


if __name__ == "__main__":
     plt.show()
