import pygame

class Renderer(object):
    def __init__(self, win, game):
        self.win = win
        
        self.game = game
        
        self.player_points = ((0, 0), (20, 10), (0, 20), (5, 10))
        
    
    def draw_player(self):
        pygame.draw.polygon(self.win, (255, 255, 255), self.player_points)
    
    def update_screen():
        pygame.display.flip()