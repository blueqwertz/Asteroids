import math
import random
from typing import Sized

class Player(object):
    def __init__(self):
        self.x = 300
        self.y = 300
        self.angle = 0
        self.hit_box = [(-10, 10), (10, 10), (10, -10), (-10, -10)]
        

class Projectile(object):
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel
        self.speed = 400
    
    def update(self, delta):
        self.x += self.vel[0] * delta * self.speed
        self.y += self.vel[1] * delta * self.speed
        
        
class Enemy(object):
    def __init__(self, x, y, vel, size):
        self.x = x
        self.y = y
        self.size = size
        self.shape = self.gen_shape()
        self.vel = vel
        self.speed = 50
        self.remove = False
    
    def update(self, delta):
        self.x += self.vel[0] * delta * self.speed
        self.y += self.vel[1] * delta * self.speed
        
    def gen_shape(self):
        points = []
        max = 10
        
        for i in range(max + 1):
            x, y = math.cos(i / max * math.pi * 2) * self.size, math.sin(i / max * math.pi * 2) * self.size * random.uniform(0.5, 1)
            points.append([x, y])
        
        return points