import pygame
from variables import *
vec = pygame.math.Vector2

class Player:
    def __init__(self, app, pos):
        self.app = app
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1, 0)
        self.listDir = None
        self.canMove = True
        self.orbLeft = 10
        self.speed = 2

    def draw(self):
        pygame.draw.circle(self.app.screen, PLAYER_COLOUR, (int(self.pix_pos.x), int(self.pix_pos.y)), self.app.cell_width // 2 - 1)

    def get_pix_pos(self):
        return vec((self.grid_pos[0] * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2, (self.grid_pos[1] * self.app.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)
    
    def move(self, direction):
        self.listDir = direction

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self. direction == vec (0, -1) or self.direction == vec(0, 0):
                return True
    
    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
            return True
        
    def on_orb(self):
        if self.grid_pos in self.app.orbs:
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False
    
    def eat_orb(self):
        self.app.orbs.remove(self.grid_pos)
        self.orbLeft -= 1
            
    def update(self):
        if self.canMove:
            self.pix_pos += self.direction * self.speed
        if self.time_to_move():
            if self.listDir != None:
                self.direction = self.listDir
            self.canMove = self.can_move()
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + self.app.cell_height // 2) // self.app.cell_height + 1
        if self.on_orb():
            self.eat_orb()