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
        self.enemy_pos = None
        self.player_pos = None
        self.goal_pos = None
        self.load()
        self.enemy = Enemy(self, vec(self.enemy_pos))
        self.player = Player(self, vec(self.player_pos))
        # self.goal_grid_pos = vec(self.goal_pos)

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
            elif self.state == 'game over':
                self.game_over_event()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
                
    def load(self):
        self.background = pygame.image.load('map.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
        with open("map.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "X":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "O":
                        self.orbs.append(vec(xidx, yidx))
                    elif char == "P":
                        self.player_pos = [xidx, yidx]
                    elif char == "E":
                        self.enemy_pos = [xidx, yidx]
                    elif char == "G":
                        self.goal_pos = [xidx, yidx]
                    elif char == "1":
                        pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height,
                                                                  self.cell_width, self.cell_height))
    
    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)
        
    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0), (x*self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height), (WIDTH, x*self.cell_height))
            
    def draw_orbs(self):
        for orb in self.orbs:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(orb.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                int(orb.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)
    
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
        if len(self.orbs) == 0 and (self.player.grid_pos[0] == self.goal_pos[0] and self.player.grid_pos[1] == self.goal_pos[1]):
            self.state = 'game over'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))
    
    def playing_update(self):
        self.player.update()
        self.enemy.update()
        if self.enemy.grid_pos == self.player.grid_pos:
            self.state = 'game over'
                
    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_orbs()
        pygame.draw.rect(self.screen, (0, 255, 0), (self.goal_pos[1] * self.cell_width+39 + TOP_BOTTOM_BUFFER//2,
                                                self.goal_pos[0] * self.cell_height-39 + TOP_BOTTOM_BUFFER//2,
                                                self.cell_width, self.cell_height))
        self.draw_grid()
        self.draw_text('ORBS LEFT: {}'.format(self.player.orbLeft),
                       self.screen, [60, 15], 18, WHITE, START_FONT)
        
        self.player.draw()
        self.enemy.draw()
        pygame.display.update()
        
        
        
############################# GAME OVER EVENTS ##################################

    def game_over_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()
                
    def game_over_update(self):
        pass
    
    def game_over_draw(self):
        self.screen.fill(BLACK)
        if(len(self.orbs) == 0) and (self.player.grid_pos[0] == self.goal_pos[0] and self.player.grid_pos[1] == self.goal_pos[1]):
            banner = "YOU WIN!"
            warna = (0, 255, 0)
        else:
            banner = "GAME OVER"
            warna = (255, 0, 0)
        quit_text = "Press the escape button to QUIT"
        self.draw_text(banner, self.screen, [WIDTH//2, 100],  52, warna, "arial", centered=True)
        self.draw_text(quit_text, self.screen, [
                       WIDTH//2, HEIGHT//1.5],  36, (190, 190, 190), "arial", centered=True)
        pygame.display.update()
        
    