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
        self.enemy_pos = None
        self.player_pos = None
        self.goal_pos = None
        # self.load()
        # self.enemy = Enemy(self, vec(self.enemy_pos))
        # self.player = Player(self, vec(self.player_pos))

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
        self.draw_text('AI HORROR GAME', self.screen, [WIDTH//2, 400], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        self.draw_text('GOAL', self.screen, [WIDTH//2, HEIGHT//2-50], START_TEXT_SIZE, (44, 167, 198), START_FONT, centered=True)
        self.draw_text('COLLECT THE ORBS TO WIN', self.screen, [WIDTH//2, HEIGHT//2], START_TEXT_SIZE, (44, 167, 198), START_FONT, centered=True)
        self.draw_text('PUSH ANY KEY TO START', self.screen, [WIDTH//2, HEIGHT//2+75], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        pygame.display.update()

        
############################# PLAYING EVENTS ##################################

    def playing_event(self):
        if len(self.orbs) == 0:
            self.state = 'game over'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runned = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
    
    def playing_update(self):
        self.player.update()
        self.enemy.update()
        if self.enemy.grid_pos == self.player.grid_pos:
                self.state = 'game over'
    