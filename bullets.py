import pyglet
from functions import rotate_movement

class BulletSprite(pyglet.sprite.Sprite):
    def __init__(self):
        image = pyglet.resource.image('images/bullet.png')
        image.anchor_x = image.width / 2
        image.anchor_y = image.height / 2
        super(BulletSprite, self).__init__(image)
    def update(self):
        self.x, self.y = rotate_movement(self.rotation, self.x, self.y, 3)
class EnemyBullet(pyglet.sprite.Sprite):
    def __init__(self):
        image = pyglet.resource.image('images/ball.png')
        image.anchor_x = image.width / 2
        image.anchor_y = image.height / 2
        super(EnemyBullet, self).__init__(image)
    def update(self, movex, movey):
        self.x += movex
        self.y += movey
