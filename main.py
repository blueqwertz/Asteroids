import math
import random

from render import Renderer
from entity import Enemy, Player, Projectile

import pygame
import os

pygame.init()

s_width = 600
s_height = 600

windowX = 1000
windowY = 200
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (windowX,windowY)

pygame.init()
pygame.joystick.init()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris")


class Asteroids(object):
    def __init__(self, win):
        self.run = True
        self.win = win
        
        self.joystickConnected = pygame.joystick.get_count() > 0
        self.joystick = None
        
        self.clock = pygame.time.Clock()
        self.clock.tick()
        
        self.speed = 300
        self.rotate_speed = 360

        self.player = Player()
        
        self.keys_pressed = [False, False, False, False, False]
        
        
        self.enemies = []
        self.projectiles = []
        self.time_last_shot = 0
        
        self.renderer = Renderer(win, self)
    
    def render(self):
        self.win.fill((0, 0, 0))
        self.renderer.draw_player()
        self.renderer.draw_projectile(self.projectiles)
        self.renderer.draw_enemy(self.enemies)
    
    def gen_enemy(self):
        x = random.randint(-100, -20) if random.random() < 0.5 else random.randint(s_width + 20, s_width + 100)
        y = random.randint(-100, -20) if random.random() < 0.5 else random.randint(s_height + 20, s_height + 100)
        self
    
    def frame(self):
        delta = self.clock.get_rawtime() / 1000
        
        for obj in self.projectiles:
            obj.update(delta)
            if obj.x < 0 or obj.x > s_width or obj.y < 0 or obj.y > s_height:
                self.projectiles.remove(obj)
        
        for obj in self.enemies:
            obj.update(delta)
            if obj.x < 0 or obj.x > s_width or obj.y < 0 or obj.y > s_height:
                self.enemies.remove(obj)
        
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
                self.init_joystick()
            
            if event.type == pygame.JOYDEVICEREMOVED:
                self.joystick = None
                self.joystick_connected = False
            
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()
                
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
        Game.frame()
        Game.render()
        
        pygame.display.flip()
        
        
if __name__ == "__main__":
    main(win)