from ursina import *
from ursina.shaders import lit_with_shadows_shader
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import random
import datetime
from shader import *









app = Ursina()
window.borderless = False
Entity.default_shader = lit_with_shadows_shader

seed = input("Seed: ")


try: seed = int(seed)
except ValueError: seed = random.randint(-9999,9999)

try: LOD = int(input("Level of Detail: "))
except ValueError: LOD = 4

try: octaveIncrease = int(input("Octave increase: "))
except ValueError: octaveIncrease = 3

try: skip = int(input("Skip value: "))
except ValueError: skip = 1

try: multip = int(input("Noise multiplier: "))
except ValueError: multip = 255

noise = []
prev = octaveIncrease
for i in range(LOD):
    val = prev*2
    noise.append(PerlinNoise(octaves = val))
    prev = val

#noise1 = PerlinNoise(octaves=3, seed = seed)
#noise2 = PerlinNoise(octaves=6, seed = seed)
#noise3 = PerlinNoise(octaves=12, seed = seed)
#noise4 = PerlinNoise(octaves=24, seed = seed)


#tree = Entity(model = Cone(3))


xpix, ypix = 200, 200
pic = []
for i in range(xpix):
    row = []
    for j in range(ypix):
        noise_val = noise[0]([i/xpix, j/ypix])
        #noise_val += 0.5 * noise2([i/xpix, j/ypix])
        #noise_val += 0.25 * noise3([i/xpix, j/ypix])
        #noise_val += 0.125 * noise4([i/xpix, j/ypix])
        for b in noise:
            noise_val += 0.75/(noise.index(b)+1) * b([i/xpix, j/ypix])

        row.append(noise_val*multip+170)
    pic.append(row)
print("\n\nGenerated noise map with the following settings:", "\nSeed:",seed, "\nLevel of Detail:",LOD, "\nOctave increase:",octaveIncrease, "\nNoise multiplier:",multip, "\nResolution:",str(xpix)+","+str(ypix), "\n\n")

lowVal = 0
highVal = 0
unclamp = pic
for i in pic:
    for b in i:

        if b >= 255:
            pic[pic.index(i)][i.index(b)] = 255
        elif b <= 0:
            pic[pic.index(i)][i.index(b)] = 0
        
        if b >= highVal:
            highVal = b
        elif b <= lowVal:
            lowVal = b

#plt.imshow(pic, cmap = "gray")
#plt.show()


water = Entity(model = "plane", scale_x = 100, scale_z = 100,
               shader= water_shader, y = 10, color = color.blue)
water.set_shader_input("time", 0)
water.set_shader_input('dark_color', color.rgba(0,.6,1, .5))
water.set_shader_input('light_color', color.rgba(0,1,1,.4))
water.set_shader_input('s', .59)
water.set_shader_input('mod', .5)
water.set_shader_input('mod2', .43)
water.set_shader_input('mody', .27)

tm = 0

    

pic2 = []
for i in pic:
    r = []
    for b in i:
        r.append(b)
    pic2.append(r)
pice = np.array(pic2)
pice = pice.astype(np.uint8)
image = Image.fromarray(pice, 'P')

im = image.convert('RGBA')

data = np.array(im)
red, green, blue, alpha = data.T

dark_areas = ((red <= 130) & (blue <= 130) & (green <= 130))
gr = data[..., :-1][dark_areas.T]

data[..., :-1][dark_areas.T] = (0,150,0)

im2 = Image.fromarray(data)
im2 = im2.rotate(90, Image.Resampling.NEAREST, expand = 1)
im2.save('output.png')

g = Entity(model = Terrain("output.png", skip=skip), scale_x = 100, scale_z = 100, scale_y = 31.55,
           texture = "output.png", texture_scale = (1,1), shader = lit_with_shadows_shader)
g.model.height_values = unclamp
g.model.generate()
g.collider = "mesh"


        

        
def toggle():
    water.enabled = not water.enabled
Button("Toggle water", on_click = toggle, scale_y = .1, scale_x = .4, position = (-.45, -.4))


gf = True
def r():
    global gf
    gf = not gf
    pice = np.array(pic2)
    pice = pice.astype(np.uint8)
    image = Image.fromarray(pice, 'P')
    
    im = image.convert('RGBA')

    data = np.array(im)
    red, green, blue, alpha = data.T

    dark_areas = ((red <= 130) & (blue <= 130) & (green <= 130))
    if gf:
        data[..., :-1][dark_areas.T] = (0,150,0)


    im2 = Image.fromarray(data)
    im2 = im2.rotate(-270, Image.Resampling.NEAREST, expand = 1)
    im2.save('output.png')

    g.texture = "output.png"
    g.texture.apply()

b = Button("Toggle grass", on_click = r,
           scale_y = .1, scale_x = .4, position = (.45, -.4))

def c():
    g.scale_y = s.value
    water.y = s2.value



s = ThinSlider(dynamic = True, on_value_changed = c, max = 100, position = (-.7,-.35,0), min = .1, value = g.scale_y)
s2 = ThinSlider(dynamic = True, on_value_changed = c, max = 100, position = (-.7,-.3,0), min = .1, value = water.y)

trees = []
trees_mesh = Entity(model = "cube", parent = scene)
for posx in range(int(g.scale_x/10)):
    for posz in range(int(g.scale_z/10)):
        if random.randint(1,1) == 1:
            trees.append(Entity(model = Cone(3), position = (posx, pic[posx][posz]/15, posz), parent = trees_mesh))

pivot = Entity()
l = DirectionalLight(parent=pivot, y=50, z=3, shadows=True, rotation=(45, -45, 45), shadow_map_resolution = (4000,4000))

trees_mesh.combine()
trees_mesh.rotation.y= 90
trees_mesh.disable()


#def gb():
#    trees_mesh.rotation_y = t.value
#t = ThinSlider(max = 360, dynamic = True, on_value_changed = gb)

spee = ThinSlider(value = .01, min = -1, max = 10, position = (-.7, .4))
def update():
    global tm
    tm += time.dt
    water.set_shader_input("time", tm)
    l.rotation_x += spee.value



def input(key):
    global seed, tm
    if key == "f3":
        pice2 = np.array(pic)
        pice2 = pice2.astype(np.uint8)
        img = Image.fromarray(pice, "P")
        
        img.save(f"saved_heightmaps\\map_{seed}__{datetime.datetime.now().strftime('%f')}.png")
    
EditorCamera()
app.run()
