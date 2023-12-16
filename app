import pygame
import sys
import copy
from variables import *
from player import *
from enemy import *

pygame.init()
vec = pygame.math.Vector2

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.run = True
        self.state = "start"
        self.cell_width = MAZE_WIDTH//COLS
        self.cell_height = MAZE_HEIGHT//ROWS
        self.walls = []
        self.orbs = []
        self.enemies = []
        self.enemy_pos = []
        self.player_pos = None
        self.load()
        self.player = Player(self, vec(self.player_pos))
        self.make_enemies()

    def run(self):
        while self.run:
            if self.state == 'start':
                self.start_event()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_event()
                self.playing_update()
                self.playing_draw()