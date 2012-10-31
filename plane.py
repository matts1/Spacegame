import pyglet
from pyglet.window import key
from functions import rotate_movement, in_bounds

ANGLE = 4

class PlaneSprite(pyglet.sprite.Sprite):
    def __init__(self):
        image = pyglet.resource.image('images/plane.png')
        image.anchor_x = image.width / 2
        image.anchor_y = image.height / 2
        super(PlaneSprite, self).__init__(image)

    def update(self, keys):
        for val, d in {"LEFT": -1, "RIGHT": 1}.items():
            if eval("keys[key." + val + "]"):
                self.rotation += d*ANGLE
        for val, m in {"UP": 1, "DOWN": -1}.items():
            if eval("keys[key." + val + "]"):  
                self.x, self.y = rotate_movement(self.rotation, self.x, self.y, m)
