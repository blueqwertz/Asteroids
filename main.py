from render import Renderer

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

        self.player = Player()
        
        self.renderer = Renderer(win, self)
    
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
        

class Player(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0
        
        


def main(win):
    Game = Asteroids(win)
    
    while Game.run:
        
        Game.keys()
        Game.renderer.draw_player()
        
        pygame.display.flip()
        
        
if __name__ == "__main__":
    main(win)