import math

from render import Renderer
from player import Player

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
        
        self.keys_pressed = [False, False, False, False]
        
        self.renderer = Renderer(win, self)
    
    def frame(self):
        delta = self.clock.get_rawtime() / 1000
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
            
            if event.type == pygame.KEYDOWN:
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
        Game.renderer.render()
        
        pygame.display.flip()
        
        
if __name__ == "__main__":
    main(win)