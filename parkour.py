# Import necessary modules and classes from the Ursina library
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import random

# Initialize the Ursina application with a visible border
app = Ursina(borderless=False)

# Set a random seed for reproducibility
random.seed(0)

# Set the default shader for entities to lit_with_shadows_shader
Entity.default_shader = lit_with_shadows_shader

# Define a custom class inheriting from FirstPersonController to extend its functionality
class MyFirstPersonController(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Method to check if the player is on a green cube
    def is_on_green_cubo(self, cubos):
        for cubo in cubos:
            if self.y <= 1 and self.intersects(cubo) and cubo.is_green:
                return True
        return False

# Create an instance of the custom first-person controller
player = MyFirstPersonController()
player.position = Vec3(0, 2, 0)  # Set the initial position of the player

# Define a class for cubes in the scene
class Cubo(Entity):
    def __init__(self, position=(0, 0, 0), is_green=False):
        super().__init__(
            position=position,
            model='cube',
            scale=(1, 1),
            origin_y=-.5,
            color=color.light_gray if not is_green else color.green,
            collider='box',
        )
        self.is_green = is_green

# Create a list to store instances of the Cubo class
cubos = []

# Create a single cube at the center of the scene
Cubo(position=(0, 1, 0))

# Function to handle user input
def input(key):
    if key == 'escape':  # If the 'escape' key is pressed, quit the application
        quit()

# Generate multiple cubes with random positions along the z-axis
for z in range(20):
    is_green = z == 19  # Make the last cube green
    cubo = Cubo(position=(random.randint(1, 3), 1, z), is_green=is_green)
    cubos.append(cubo)

# Create the ground entity
ground = Entity(model='plane', collider='box', scale=64, color=color.red)
ground.position = Vec3(0, -20, 0)  # Position the ground below the scene

# Function to update the game state each frame
def update():
    global player
    if player.is_on_green_cubo(cubos):  # If the player is on a green cube, reset the player's position
        player.position = Vec3(0, 2, 0)

    if player.position.y <= -10:  # If the player falls below a certain y-position, reset their position
        player.position = Vec3(0, 10, 0)

# Create a sky entity for the background
Sky()

# Run the Ursina application
app.run()
