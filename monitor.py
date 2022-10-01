import pygame
import math

OFF = (22, 22, 40)
ON = (202, 202, 252)

WIDTH = 64
HEIGHT = 32

class Monitor:
    '''
    Class used to generate graphics for emulator

    Attributes:
        WIDTH: display WIDTHumns
        HEIGHT: display HEIGHTs
        display: where graphics is shown

    '''
    def __init__(self, scale: int):
        self.scale = scale
        self.win = pygame.display.set_mode((WIDTH * self.scale, HEIGHT * self.scale))
        pygame.display.set_caption("Chip8")
        self.win.fill(OFF)
        self.reset()
        self.render()


    '''
    Toggles the pixel to 0 or 1
    '''
    def set_pixel(self, x: int, y: int) -> bool: 
        # wrap around
        x %= WIDTH
        y %= HEIGHT
        
        # set pixel by XORing with 1
        self.display[y][x] ^= 1;
        
        # check if pixel was erased
        return not self.display[y][x]
        

    '''
    Reset & clear the display 
    '''
    def reset(self):
        self.display = [[0 for x in range(WIDTH)] for y in range(HEIGHT)]

    def render(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                colour = OFF
                if self.display[y][x]:
                    colour = ON
                pygame.draw.rect(self.win, colour, [x * self.scale, y * self.scale, self.scale, self.scale], 0)
        pygame.display.flip()
