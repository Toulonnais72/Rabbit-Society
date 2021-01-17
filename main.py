
import Terrain_Generator as tg
from ursina import *
from ursina.shaders import basic_lighting_shader
from ursina.light import DirectionalLight
from ursina.prefabs import button
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import camera_vertical_blur_shader

import time

app = Ursina()
ntime = time.clock()
# Dimensions of our bunny world
X = 64
Y = 64
# some colors
sand_color = color.rgb(223,227,141)
water_color = color.rgb(124, 208, 222)
dirt_color = color.rgb(115, 118, 83)
land_color = color.rgb(140,200,0)
snow_color = color.rgb(232,232,233)
leaf_color = color.rgb(89,143,113)

land = tg.Terrain(X, Y)
land.generate()
land.save_image(str(ntime))

#player = FirstPersonController()
window.title = 'Rabbit Society'                # The window title
window.borderless = False               # Show a border
window.fullscreen = False               # Do not go Fullscreen
window.exit_button.visible = True      # Show the in-game red X that loses the window
window.fps_counter.enabled = True       # Show the FPS (Frames per second) counter

ec = EditorCamera(rotation_smoothing=2,
                  enabled=True,
                  zoom_speed=5,
                  hotkeys={'toggle_orthographic':'p', 'center':'f'},
                  rotation=(10, -220, 0),
                  pan_speed=(15,15))
camera_info = Text(position=window.top_left, size = 1 / 70)
camera.z = -450 #set the zoom to see the whole terrain
#camera.shader = camera_vertical_blur_shader
#camera.set_shader_input('blur_size', .0)
#camera.blur_amount = 0

map = []
bunnies = []
initial_pos = []
oscilly = 5

#Start the Scene
Light(type='ambient', color=(0.95,0.8,0.95,1))
Sky(rotation_y=125)
#pivot = Entity()
#DirectionalLight(parent=pivot)

def generate_land():
    '''global map
    map = []
    col = water_color
    for x in range(X):
        for y in range(Y):
            land_type = land.biome[x][y]
            if land_type == "Land":
                col = land_color
            elif land_type == "Water":
                col = water_color
            elif land_type == "Dirt":
                col = dirt_color
            elif land_type == "Snow":
                col = snow_color
            loc = Entity(model="cube", position=(5 * x, 50 * int(land.elevation[x][y]), 5 * y), scale=(5,5,5), color = col, shader=colored_lights_shader)
            map.append(loc)'''

    e = Entity(model=Terrain("./images/height_field" + str(ntime)), scale=(X * 5, 50, Y * 5), texture="./images/" + str(ntime)+'.png', double_sided = True)
    sea = Entity(model='plane', scale = X * 5, position = (0, int(land.water_level * 255 / 5), 0), color = water_color, double_sided = True)

    for x in range(X):
        for y in range(Y):
            land_type = land.biome[x][y]
            if land_type == "Land":
                if land.trees[x][y] >= 0:
                    tree = Entity(model = Cone(8, direction=(0,1,0)),
                                  position = (5*(y-Y) + Y*5/2 + random.randint(1,5), 1.5+land.elevation[x][y]*50, 5*(X-x) - X*5/2 + random.randint(1,5)),
                                  color = leaf_color,
                                  scale = X / random.randint(20,50),
                                  shader = basic_lighting_shader)

def update():
    #player.x += held_keys['d'] * time.dt * 1
    ec.rotation += (0, time.dt,0)
    if camera.z > 0 : camera.z = -100
    camera_info.text = "Camera rotation:" + str(ec.rotation) + '\n'\
                       + "Camera pos: " + str(ec.position) + '\n' \
                       + "PanSpeed: " + str(ec.pan_speed) + '\n' \
                       + "Z: " + str(camera.z)
    if held_keys['8']:  # If 4 is pressed
        ec.position += (0, time.dt*5, 0)  # move up vertically
    if held_keys['2']:  # If 6 is pressed
        ec.position -= (0, time.dt*5, 0)  # move down vertically
    if held_keys['1']:  # If 4 is pressed
        ec.position += (time.dt*5, 0, 0)  # move up vertically
    if held_keys['7']:  # If 6 is pressed
        ec.position -= (time.dt*5, 0, 0)  # move down vertically
    if held_keys['9']:  # If 4 is pressed
        ec.position += (0, 0, time.dt*5)  # move up vertically
    if held_keys['3']:  # If 6 is pressed
        ec.position -= (0, 0, time.dt*5)  # move down vertically
    if held_keys['escape']:
        quit()
    #new_time = time.clock()

def input(key):
    if key == 'space':
        quit()

generate_land()
app.run()


