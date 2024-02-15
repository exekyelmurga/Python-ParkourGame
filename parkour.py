from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import ursina

app = Ursina(borderless=False)

random.seed(0)
window.size = (600, 600)
Entity.default_shader = lit_with_shadows_shader

player = FirstPersonController()
player.position=Vec3(0,2,0)

class Cubo(Entity):
    def __init__(self, position=(0,0,0), is_green=False):
        super().__init__(
            position = position, 
            model = 'cube',
            scale = (1,1),
            origin_y = -.5,
            color = color.light_gray if not is_green else color.green,
            collider = 'box',
        )
        self.is_green = is_green

cubos = []

Cubo(position=(0,1,0))


def input(key):
    if key == 'escape':
        quit()

for z in range(20):
    is_green = z == 19
    cubo = Cubo(position=(random.randint(1,3), 1, z), is_green=is_green)
    cubos.append(cubo)

ground = Entity(model = 'plane', collider='box', scale=64, color = color.red)
ground.position = Vec3(0, -20, 0)

def is_on_green_cubo():
    for cubo in cubos:
        if player.y <= 1 and player.intersects(cubo) and cubo.is_green:
            return True
    return False    

def update():
    global player
    if is_on_green_cubo():
        player.position = Vec3(0,2,0)

    if(player.position.y <= -10):
        player.position = Vec3(0,10,0)
Sky()


app.run()
