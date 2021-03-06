import math
import random

from render import Renderer
from entity import Enemy, Player, Projectile

from shapely.geometry import Polygon

import pygame
import os

pygame.init()
pygame.joystick.init()

s_width = 600
s_height = 600

windowX = 1000
windowY = 200
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (windowX,windowY)


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Asteroids")


class Asteroids(object):
    def __init__(self, win):
        self.run = True
        self.win = win
        
        self.pause = False
        
        self.using_joystick = False
        
        self.joystick_connected = pygame.joystick.get_count() > 0
        self.joystick = None
        
        self.clock = pygame.time.Clock()
        self.clock.tick()
        
        self.speed = 300
        self.rotate_speed = 360

        self.player = Player()
        
        self.keys_pressed = [False, False, False, False, False]
        
        
        self.enemies = []
        self.enemy_spawn_time = 3
        self.enemy_last_spawn = self.enemy_spawn_time
        
        self.projectiles = []
        self.time_last_shot = 0
        
        self.renderer = Renderer(win, self)
    
    def init_joystick(self):
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
    
    def render(self):
        self.win.fill((0, 0, 0))
        self.renderer.draw_player()
        self.renderer.draw_projectile(self.projectiles)
        self.renderer.draw_enemy(self.enemies)
    
    def gen_enemy(self, x=None, y=None, size=None):
        if not x:
            x = random.randint(-100, -20) if random.random() < 0.5 else random.randint(s_width + 20, s_width + 100)
        if not y:
            y = random.randint(-100, -20) if random.random() < 0.5 else random.randint(s_height + 20, s_height + 100)
        if not size:
            size = 40
        velX = self.player.x - x
        velY = self.player.y - y
        dist = math.sqrt((self.player.x - x) ** 2 + (self.player.y - y) ** 2)
        velX, velY = velX / dist, velY / dist
        self.enemies.append(Enemy(x, y, (velX, velY), size))    
    
    def is_inside_polygon(self, points, p):
        
        INT_MAX = 10000
 
        def onSegment(p:tuple, q:tuple, r:tuple) -> bool:
            
            if ((q[0] <= max(p[0], r[0])) &
                (q[0] >= min(p[0], r[0])) &
                (q[1] <= max(p[1], r[1])) &
                (q[1] >= min(p[1], r[1]))):
                return True
                
            return False   
    
        def orientation(p:tuple, q:tuple, r:tuple) -> int:
            
            val = (((q[1] - p[1]) *
                    (r[0] - q[0])) -
                ((q[0] - p[0]) *
                    (r[1] - q[1])))
                    
            if val == 0:
                return 0
            if val > 0:
                return 1 
            else:
                return 2 
        
        def doIntersect(p1, q1, p2, q2):
            o1 = orientation(p1, q1, p2)
            o2 = orientation(p1, q1, q2)
            o3 = orientation(p2, q2, p1)
            o4 = orientation(p2, q2, q1)
            
            if (o1 != o2) and (o3 != o4):
                return True
                    
            if (o1 == 0) and (onSegment(p1, p2, q1)):
                return True
            
            if (o2 == 0) and (onSegment(p1, q2, q1)):
                return True
            
            if (o3 == 0) and (onSegment(p2, p1, q2)):
                return True
            
            if (o4 == 0) and (onSegment(p2, q1, q2)):
                return True
        
            return False
        
        n = len(points)
        
        if n < 3:
            return False
            
        extreme = (INT_MAX, p[1])
        count = i = 0
        
        while True:
            next = (i + 1) % n
            
            
            if (doIntersect(points[i],
                            points[next],
                            p, extreme)):

                if orientation(points[i], p,
                            points[next]) == 0:
                    return onSegment(points[i], p,
                                    points[next])
                                    
                count += 1                
            i = next
            if (i == 0):
                break
            
        return (count % 2 == 1)
    
    def frame(self):
        delta = self.clock.get_rawtime() / 1000
        
        if self.enemy_last_spawn > self.enemy_spawn_time:
            self.gen_enemy()
            self.enemy_last_spawn = 0
            self.enemy_spawn_time *= 0.9
            self.enemy_spawn_time = max(1, self.enemy_spawn_time)
        
        self.enemy_last_spawn += delta
        
        for obj in self.projectiles:
            for el in self.enemies:
                shape = el.shape.copy()
                for i, point in enumerate(shape):
                    shape[i] = point[0] + el.x, point[1] + el.y
                
                if self.is_inside_polygon(points = shape, p = (obj.x, obj.y)):
                    self.enemies.remove(el)
                    if el.size == 40:
                        self.gen_enemy(el.x - 20, el.y - 20, 20)
                        self.gen_enemy(el.x + 20, el.y + 20, 20)
                    try:
                        self.projectiles.remove(obj)
                    except:
                        pass
            obj.update(delta)
            if obj.x < 0 or obj.x > s_width or obj.y < 0 or obj.y > s_height:
                self.projectiles.remove(obj)
        
        for obj in self.enemies:
            shape = ((-10, 10), (10, 0), (-10, -10), (-5, 0))
            
            shape = self.renderer.rotate_shape(shape, self.player.angle)
            for i, coord in enumerate(shape):
                shape[i] = coord[0] + self.player.x, coord[1] + self.player.y
            player = Polygon(shape)
            
            shape = obj.shape.copy()
            for i, coord in enumerate(shape):
                shape[i] = coord[0] + obj.x, coord[1] + obj.y
            
            enemy = Polygon(shape)
            
            
            for i, other in enumerate(self.enemies):
                if not i < len(self.enemies):
                    break
                if other == obj:
                    continue
                shape = other.shape.copy()
                for ind, coord in enumerate(shape):
                    shape[ind] = coord[0] + other.x, coord[1] + other.y
                other = Polygon(shape)
                
                if enemy.intersects(other):
                    try:
                        self.enemies.remove(obj)
                        self.enemies.remove(other)
                        # if obj.size == 40:
                        #     self.gen_enemy(obj.x - 20, obj.y - 20, 20)
                        #     self.gen_enemy(obj.x + 20, obj.y + 20, 20)
                    except:
                        print(i, len(self.enemies))
            
            if enemy.intersects(player):
                self.pause = True
            
            obj.update(delta)
                    
        self.time_last_shot += delta
        self.clock.tick()
        if self.keys_pressed[0]:
            x = delta * self.speed * math.cos(self.player.angle * math.pi / 180)
            y = delta * self.speed * math.sin(self.player.angle * math.pi / 180)
            self.player.x += x
            self.player.y += y
        if self.keys_pressed[1]:
            x = delta * self.speed * math.cos(self.player.angle * math.pi / 180)
            y = delta * self.speed * math.sin(self.player.angle * math.pi / 180)
            self.player.x -= x
            self.player.y -= y

        if self.keys_pressed[4]:
            if self.time_last_shot > 0.3:
                velX = math.cos(self.player.angle * math.pi / 180)
                velY = math.sin(self.player.angle * math.pi / 180)

                self.projectiles.append(Projectile(self.player.x, self.player.y, (velX, velY)))
                self.time_last_shot = 0
        
        if self.player.x < 0:
            self.player.x = s_width
        if self.player.y < 0:
            self.player.y = s_height
        
        if self.player.x > s_width:
            self.player.x = self.player.x % s_width
        if self.player.y > s_height:
            self.player.y = self.player.y % s_height
        
        if self.keys_pressed[2]:
            self.player.angle -= delta * self.rotate_speed
        if self.keys_pressed[3]:
            self.player.angle += delta * self.rotate_speed
    
    def keys(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                self.joystick_connected = True
                self.using_joystick = True
                self.init_joystick()
            
            if event.type == pygame.JOYDEVICEREMOVED:
                self.joystick = None
                self.joystick_connected = False
                self.using_joystick = False
            
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()
            
            if self.joystick_connected:
                
                joy_activation = 0.7
                up_down = self.joystick.get_axis(1)
                
                if abs(up_down) > joy_activation:
                    self.using_joystick = True
                
                if self.using_joystick:
                    if up_down < -joy_activation:
                        self.keys_pressed[0] = True
                    else:
                        self.keys_pressed[0] = False
                    
                    if up_down > joy_activation:
                        self.keys_pressed[1] = True
                    else:
                        self.keys_pressed[1] = False
                
                rigth_left = self.joystick.get_axis(2)
                
                if abs(rigth_left) > joy_activation:
                    self.using_joystick = True
                        
                if self.using_joystick:
                    
                    if rigth_left < -joy_activation:
                        self.keys_pressed[2] = True
                    else:
                        self.keys_pressed[2] = False
                    
                    if rigth_left > joy_activation:
                        self.keys_pressed[3] = True
                    else:
                        self.keys_pressed[3] = False
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.keys_pressed[0] = False
                if event.key == pygame.K_s:
                    self.keys_pressed[1] = False
                
                if event.key == pygame.K_a:
                    self.keys_pressed[2] = False
                if event.key == pygame.K_d:
                    self.keys_pressed[3] = False
                
                if event.key == pygame.K_SPACE:
                    self.keys_pressed[4] = False
            
            if event.type == pygame.KEYDOWN:
                self.using_joystick = False
                if event.key == pygame.K_SPACE:
                    self.keys_pressed[4] = True
                
                if event.key == pygame.K_w:
                    self.keys_pressed[0] = True
                if event.key == pygame.K_s:
                    self.keys_pressed[1] = True
                
                if event.key == pygame.K_a:
                    self.keys_pressed[2] = True
                if event.key == pygame.K_d:
                    self.keys_pressed[3] = True


def main(win):
    Game = Asteroids(win)
    
    while Game.run:
        
        Game.keys()
        if not Game.pause:
            Game.frame()   
        Game.render()
        
        pygame.display.flip()
        
        
if __name__ == "__main__":
    main(win)