import pyglet
from random import randint
from functions import rotate_movement
from bullets import EnemyBullet
from math import sqrt

def spawn_enemy(enemy, avgsecs, width, spawn_y):
        if randint(0, 20*avgsecs)== 0:
            enemy = eval(enemy + "()")
            enemy.x = randint(0, width)
            enemy.y = spawn_y + enemy.height
            return enemy
        return 0

def spawn_bullet(kind, chance, enemyx, enemyy, planex = 0, planey = 0):
    if randint(0, chance) == 0:
        diffx = planex - enemyx
        diffy = planey - enemyy
        bullet = EnemyBullet()
        bullet.x, bullet.y = enemyx, enemyy
        if kind == 3:
            turns = sqrt((diffx)**2 + (diffy)**2)/ 4 * 1.5
            newshot=[bullet, diffx / turns * 3, diffy / turns * 3]
            return newshot
        else:
            return [bullet, 0, -6]
    return 0

class EnemyPlane(pyglet.sprite.Sprite):
    def update(self, speed, kind, plane = 0):
        self.y -= speed
        bullet = 0
        if kind == "Enemy2":
            bullet = spawn_bullet(2, 30, self.x, self.y)
        elif kind == "Enemy3":
            bullet = spawn_bullet(3, 80, self.x, self.y, plane.x, plane.y)
        return bullet
            

class Enemy1(EnemyPlane):
    def __init__(self):
        image = pyglet.resource.image('images/enemy1.png')
        image.anchor_x, image.anchor_y = image.width / 2, image.height / 2
        super(Enemy1, self).__init__(image)

class Enemy2(EnemyPlane):
    def __init__(self):
        image = pyglet.resource.image('images/enemy2.png')
        image.anchor_x, image.anchor_y = image.width / 2, image.height / 2
        super(Enemy2, self).__init__(image)
        
class Enemy3(EnemyPlane):
    def __init__(self):
        image = pyglet.resource.image('images/enemy3.png')
        image.anchor_x, image.anchor_y = image.width / 2, image.height / 2
        super(Enemy3, self).__init__(image)

class Enemy4(EnemyPlane):
    def __init__(self):
        image = pyglet.resource.image('images/enemy4.png')
        image.anchor_x, image.anchor_y = image.width / 2, image.height / 2
        super(Enemy4, self).__init__(image)
