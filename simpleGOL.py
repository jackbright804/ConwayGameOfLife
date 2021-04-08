"""
Naive implementation of Conway's Game of Life.
The algorithm generates a set of candidate cells (the cells which are alive and 
cells adjacent to alive cells) and applies the transition rule to each individual
cell to obtain the next state of the game.
"""

import sys
import pygame
from pygame.locals import *
import copy

class Board:
    """Defines the board and its current state. Determines how the current
    board state derives the next.
    """
    def __init__(self, initial_cells):
        self.live = set(initial_cells)
        self.previous = set()
        self.state = 0
        
        self.min_x = 100
        self.max_x = -100
        self.min_y = 100
        self.max_y = -100
        self.update_boundaries()
        
        self.center_x = 0
        self.center_y = 0
        
    def Generate_next_state(self):
        if len(self.live) == 0:
            return #there are no live cells.
        
        self.state += 1
        self.previous = copy.copy(self.live)
        
        candidate = self.expansion(self.live)
        
        self.live = set()
        
        for cell in candidate:
            if self.transition(cell, self.previous): #if the cell is live according to the transition rules
                self.live.add(cell)
        
        self.update_boundaries()
        
    def expansion(self, positions):
        """Expands the set of candidate cells to include all dead cells
        which neighbour a living cell. Produces the set of all cells which need
        to be processed to producd the next board state correctly"""
        expanded_set = set()
        for cell in positions:
            expanded_set.update(self.expand(cell))
        
        return expanded_set
            
    def expand(self, cell):
        """Helper function for expansions and transtion"""
        x, y = cell #cell is defined by its xy position on the board
        return set([(x+a, y+b) for a in range(-1, 2) for b in range(-1, 2)])
    
    def transition(self, cell, state):
        """Decides whether or not the cell will be alive after the next transition
        according to the current state of the board"""
        neighbours = self.expand(cell)
        neighbours.remove(cell)
        
        neighbours.intersection_update(state) #leaves neighbours as the list of live neighbours
        
        return (len(neighbours) == 3 or (len(neighbours) == 2 and cell in state))
        
    def Draw(self, screen_width, screen_height, screen):
        min_dimension = 50
        width = self.max_x - self.min_x + 1
        height = self.max_y - self.min_y + 1
        center_x = (self.min_x + self.max_x) // 2
        center_y = (self.min_y + self.max_y) // 2
        # Artifically expand maximums so we get less bouncing around in the
        # early game
        if width < min_dimension or height < min_dimension:
            self.min_x = min(self.min_x, center_x - min_dimension // 2)
            self.max_x = max(self.max_x, center_x + min_dimension // 2)
            self.min_y = min(self.min_y, center_y - min_dimension // 2)
            self.max_y = max(self.max_y, center_y + min_dimension // 2)
        
        pixels = min(screen_width // (width+1), screen_height // (height+1))
        
        for (x,y) in self.live:
            box = pygame.Rect((screen_width // 2 + (x - center_x)*pixels,
                               screen_height // 2 + (y - center_y)*pixels),
                              (pixels, pixels))
            screen.fill((0,0,0), box)
        
    def update_boundaries(self):
        if len(self.live) == 0:
            return
            
        # Todo: ignore gliders in this
        min_x = min(map(lambda a: a[0], self.live))
        max_x = max(map(lambda a: a[0], self.live))
        min_y = min(map(lambda a: a[1], self.live))
        max_y = max(map(lambda a: a[1], self.live))
        self.min_x = min(self.min_x, min_x)
        self.max_x = max(self.max_x, max_x)
        self.min_y = min(self.min_y, min_y)
        self.max_y = max(self.max_y, max_y)
            
class Game:
    """Operates on the board states to produce the game"""
    def __init__(self, size, board):
        (self.width, self.height) = size
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.ttu = 2
        self.ttn = 100
        
        self.board = board
        
    def ProcessEvent(self, event):
        if event.type == pygame.QUIT:
            sys.exit()
    
    def Draw(self):
        self.screen.fill((255,255,255))
        self.board.Draw(self.width, self.height, self.screen)
        
    def Tick(self):
        if self.ttn:
            self.ttn -= 1
        else:
            self.board.Generate_next_state()
            self.ttn = self.ttu

    def RunGameLoop(self):
        while True:
            # Process any pending events.
            for event in pygame.event.get():
                self.ProcessEvent(event)
            
            # Update anything that happens over time. The first call waits until
            # it has been a 30th of a second since the last tick, then the
            # second call updates the program.
            self.clock.tick(30)
            self.Tick()
                
            # Re-draw the screen
            self.Draw()
            
            # Switch the current screen image for the one we just prepared.
            pygame.display.flip()  
            
def main():
    pygame.init()
    size = (800, 800)
    
    #initial_cells = [(-2,-2), (-2,-1), (-2,2), (-1,-2), (-1,1), (0,-2), (0,1),
    #                (0,2), (1,0), (2,-2), (2,0), (2,1), (2,2)]
    
    initial_cells = [(0,1), (1, 0), (-1, -1), (0, -1), (1, -1)]
    
    game = Game(size, Board(initial_cells))
    game.RunGameLoop()    
    
if __name__ == "__main__":
    main()