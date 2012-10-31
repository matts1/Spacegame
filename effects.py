import pyglet

class BackGround(pyglet.sprite.Sprite):
    def __init__(self):
        image = pyglet.resource.image('images/back.jpg')
        super(BackGround, self).__init__(image)

class EnemyExplosion(pyglet.sprite.Sprite):
    def __init__(self):
        image = pyglet.resource.image('images/Enemy/1.png')
        self.frame = 1
        super(EnemyExplosion, self).__init__(image)
    def update(self):
        self.frame += 1
	try:
            self.image = pyglet.resource.image('images/Enemy/' + str(self.frame) + '.png')
        except pyglet.resource.ResourceNotFoundException:
            return 1
        return 0
class EndExplosion(pyglet.sprite.Sprite):
    def __init__(self):
        image = pyglet.resource.image('images/Plane/1.png')
        self.frame = 0
        super(EndExplosion, self).__init__(image)
    def update(self, a = 1):
        self.frame += 1
        try:
            self.image = pyglet.resource.image('images/Plane/' + str(self.frame) + '.png')
        except pyglet.resource.ResourceNotFoundException:
            pass
        return 0

