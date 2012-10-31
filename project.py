#music, sound fx, acceleration, pixel collision checking, wind
#difficulty level, fullscreen
import pyglet
from pyglet.window import key
from random import randint


from plane import PlaneSprite
from bullets import BulletSprite
from functions import in_bounds, highscore, detect_collision
from enemy import Enemy1, Enemy2, Enemy3, Enemy4, spawn_enemy
from effects import BackGround, EnemyExplosion, EndExplosion

class Window(pyglet.window.Window):
    def __init__(self):
        # Call the superclass's constructor.
        super(Window, self).__init__()
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule_interval(self.update, 0.05)
        self.set_fullscreen()
        self.prev = 0
#sound
        self.explosionplayer = pyglet.media.Player()
        self.explosion1 = pyglet.media.load('sounds/Enemy.wav', streaming = False)
        #self.music = pyglet.media.load('sounds/background.mp3')
        #self.player = pyglet.media.Player()
        #self.player.queue(self.music)
        #self.player.eos_action = 'loop'
        #self.player.play()
#plane
        self.plane = PlaneSprite()
        self.plane.x = self.width / 2
        self.plane.y = self.height / 2
#bullets        
        self.bullets = []
        self.can_shoot = 1.0
        self.enemyshots = []
#enemies
        self.enemies = []
        self.pts = {"Enemy1": 5,"Enemy2": 10, "Enemy3": 20 ,"Enemy4": 40}
#background
        self.backs = []
        back = BackGround()
        for x in xrange(0, self.width, back.width):
            for y in xrange(0, self.height, back.height):
                back = BackGround()
                back.x, back.y = x, y
                self.backs.append(back)
#labels
        self.score = 0
        self.scorelabel = pyglet.text.Label("Score: 0",
            anchor_y = 'top', y = self.height,
            color = (255, 0, 0, 255), font_size = 16)
        
        self.health = 100
        self.healthlabel = pyglet.text.Label("Health: " + str(self.health),
            anchor_x = 'right', anchor_y = 'top', x = self.width,
            y = self.height, color = (255, 0, 0, 255), font_size = 16)
#explosions
        self.explosions = []
        self.will_close = 0
###############################################################################
    def update(self, dt):
#features
        if self.keys[key.F4] and not self.prev:
            oldx, oldy = self.plane.x/(self.width * 1.0), self.plane.y/(self.height * 1.0)
            olds = []
            for enemy in self.enemies:
                olds.append([enemy[1].x/(self.width * 1.0), enemy[1].y/(self.height * 1.0)])
            if self.fullscreen: self.set_fullscreen(fullscreen = False)
            else: self.set_fullscreen()
            self.prev = 1
            self.healthlabel.y = self.scorelabel.y = self.height
            self.healthlabel.x = self.width
            self.plane.x, self.plane.y = oldx * self.width, oldy * self.height
            for enemy in self.enemies:
                [oldx, oldy] = olds[self.enemies.index(enemy)]
                enemy[1].x, enemy[1].y = oldx * self.width, oldy * self.height                
        else: self.prev = 0
#explosions
        explosionremove = []
        for explosion in self.explosions:
            delete = explosion.update()
            if delete:
                explosionremove.append(explosion)
        for removal in explosionremove:
            self.explosions.remove(removal)
#plane
        self.plane.update(self.keys)
        inside = in_bounds(self.plane, self.height, self.width)
        if not inside[0]:
            self.plane.x, self.plane.y = inside[1], inside[2]
#us shooting    
        self.can_shoot += 0.1
        if self.keys[key.SPACE] and self.can_shoot >= 1.0:
            self.can_shoot = 0
            bullet = BulletSprite()
            bullet.rotation = self.plane.rotation
            bullet.x = self.plane.x
            bullet.y = self.plane.y
            self.bullets.append(bullet)
#bullets and boundaries
        bulletremove = []
        shotsremove = []
        enemyremove = []
        for bullet in self.bullets:
            bullet.update()
            if not in_bounds(bullet, self.height, self.width, bullet.width / 2, bullet.height / 2)[0]:
                bulletremove.append(bullet)
        for [shot, x, y] in self.enemyshots:
            shot.update(x, y)
            if not in_bounds(shot, self.height, self.width, shot.width / 2, shot.height / 2)[0]:
                shotsremove.append([shot, x, y])
        for kind, enemy in self.enemies:
            off = 0
            if kind == "Enemy4":
                if enemy.y > self.height + enemy.height / 2:
                    enemy.y = randint(-100, 0)
                    enemy.x = randint(0, self.width)
            else:
                if enemy.y < 0 - enemy.height / 2:
                    enemy.y = randint(self.height, self.height + 100)
                    enemy.x = randint(0, self.width)
#enemies
        enemy1 = spawn_enemy("Enemy1", 5, self.width, self.height)
        if enemy1: self.enemies.append(["Enemy1", enemy1])
        enemy2 = spawn_enemy("Enemy2", 8, self.width, self.height)
        if enemy2: self.enemies.append(["Enemy2", enemy2])
        enemy3 = spawn_enemy("Enemy3", 12, self.width, self.height)
        if enemy3: self.enemies.append(["Enemy3", enemy3])
        enemy4 = spawn_enemy("Enemy4", 16, self.width, 0 - 32)
        if enemy4: self.enemies.append(["Enemy4", enemy4])
        
        for kind, enemy in self.enemies:
            if kind != "Enemy4":
                status = enemy.update(3, kind, self.plane)
                if status:
                    self.enemyshots.append(status)
            else:
                enemy.update(-5, kind)
#collision
        for kind, enemy in self.enemies:
            for bullet in self.bullets:
                if detect_collision(enemy, bullet):
                    if bullet not in bulletremove:
                        bulletremove.append(bullet)
                    if enemy not in enemyremove:
                        enemyremove.append([kind, enemy])
                    self.score += self.pts[kind]
            if detect_collision(self.plane, enemy):
                self.health -= 15
                if enemy not in enemyremove:
                    enemyremove.append([kind, enemy])
        for shot, x, y in self.enemyshots:
            if detect_collision(self.plane, shot):
                if [shot, x, y] not in shotsremove:
                    shotsremove.append([shot, x, y])
                self.health -= 2

        for enemy in enemyremove:
            explosion = EnemyExplosion()
            explosion.x = enemy[1].x - explosion.width / 2
            explosion.y = enemy[1].y - explosion.height / 2
            self.explosions.append(explosion)
            self.enemies.remove(enemy)
            self.explosion1.play()
            
        for bullet in bulletremove:
            self.bullets.remove(bullet)
        for shot in shotsremove:
            self.enemyshots.remove(shot)
#labels
        self.scorelabel.text = "Score: " + str(self.score)
        self.healthlabel.text = "Health: " + str(self.health)
#closing window
        if self.will_close:
            self.will_close += 1
            if self.will_close == 30:
                pyglet.window.Window.on_close(self)
                highscore(self.score)
        if self.health <= 0 and not self.will_close:
            self.will_close = 1
            self.health = 0
            end = EndExplosion()
            end.x, end.y = self.plane.x - end.width / 2, self.plane.y - end.height / 2
            self.plane = end
            self.explosion2 = pyglet.media.load('sounds/Plane.wav')
            self.health = 0
            #self.player.pause()
            self.explosion2.play()

            

################################################################################
    def on_draw(self):
        # Clear what was drawn last frame.
        self.clear()
        for back in self.backs:
            back.draw()
        for enemy in self.enemies:
            enemy[1].draw()
        for shot in self.enemyshots:
            shot[0].draw()
        for bullet in self.bullets:
            bullet.draw()
        if self.will_close < 10:
            self.plane.draw()
        for explosion in self.explosions:
            explosion.draw()
        self.scorelabel.draw()
        self.healthlabel.draw()
        
win = Window()
pyglet.app.run()
