import pygame
import sys
import copy
from variables import *
from player import *
from enemy import *

pygame.init()
pygame.display.set_caption('AI Horror Game')
vec = pygame.math.Vector2

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.runned = True
        self.state = "start"
        self.cell_width = MAZE_WIDTH//COLS
        self.cell_height = MAZE_HEIGHT//ROWS
        self.walls = []
        self.orbs = []
        self.enemies = []
        self.enemy_pos = []
        self.player_pos = None
        # self.load()
        # self.player = Player(self, vec(self.player_pos))
        # self.make_enemies()

    def run(self):
        while self.runned:
            if self.state == 'start':
                self.start_event()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_event()
                self.playing_update()
                self.playing_draw()
                

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)
    
############################# START EVENTS ##################################

    def start_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runnned = False
            if event.type == pygame.KEYDOWN:
                self.state = 'playing'
    
    def start_update(self):
        pass
    
    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH ANY KEY TO START', self.screen, [WIDTH//2, HEIGHT//2], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        pygame.display.update()