from types import coroutine
import pygame
import math

class Renderer(object):
    def __init__(self, win, game):
        self.win = win
        
        self.game = game
        self.player = game.player
        
    def rotate_shape(self, polygon, theta):
        theta = math.radians(theta)
        rotatedPolygon = []
        for corner in polygon :
            rotatedPolygon.append(( corner[0]*math.cos(theta)-corner[1]*math.sin(theta) , corner[0]*math.sin(theta)+corner[1]*math.cos(theta)) )
        return rotatedPolygon
    
    def draw_player(self):
        shape = ((-10, 10), (10, 0), (-10, -10), (-5, 0))
        shape = self.rotate_shape(shape, self.player.angle)
        for i, coord in enumerate(shape):
            shape[i] = coord[0] + self.player.x, coord[1] + self.player.y
        pygame.draw.polygon(self.win, (255, 255, 255), shape, 2)
    

    def draw_enemy(self, enemies):
        for obj in enemies:
            shape = obj.shape.copy()
            for i, point in enumerate(shape):
                shape[i] = point[0] + obj.x, point[1] + obj.y
            pygame.draw.polygon(self.win, (255, 255, 255), shape, 2)
    
    def draw_projectile(self, projectlies):
        for obj in projectlies:
            
            pygame.draw.circle(self.win, (255, 255, 255), (obj.x, obj.y), 5)
    
    def update_screen():
        pygame.display.flip()