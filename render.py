from types import coroutine
import pygame
import math

class Renderer(object):
    def __init__(self, win, game):
        self.win = win
        
        self.game = game
        self.player = game.player
        
    def render(self):
        self.win.fill((0, 0, 0))
        self.draw_player()
        
    def rotate_shape(self, polygon, theta):
        """Rotates the given polygon which consists of corners represented as (x,y),
        around the ORIGIN, clock-wise, theta degrees"""
        theta = math.radians(theta)
        rotatedPolygon = []
        for corner in polygon :
            rotatedPolygon.append(( corner[0]*math.cos(theta)-corner[1]*math.sin(theta) , corner[0]*math.sin(theta)+corner[1]*math.cos(theta)) )
        return rotatedPolygon
    
    def draw_player(self):
        shape = ((-10, 10), (10, 0), (-10, -10), (-5, 0))
        shape = self.rotate_shape(shape, self.player.angle)
        for i, coord in enumerate(shape):
            shape[i] = coord[0] + self.player.x + 10, coord[1] + self.player.y + 10
        pygame.draw.polygon(self.win, (255, 255, 255), shape, 2)
    
    def update_screen():
        pygame.display.flip()