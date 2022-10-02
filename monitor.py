import pygame
import math

# black
OFF = (0, 0, 0)
#white
ON = (255, 255, 255)

WIDTH = 64
HEIGHT = 32

class Monitor:
    '''
    Class used to generate graphics for emulator

    Attributes:
        scale: scale of display 
        display: 2D list of pixels where 0 is off and 1 is on
        win: pygame window which is the display
    '''

    def __init__(self, scale: int):
        self.scale = scale

        self.display =  [[0 for x in range (WIDTH)] for y in range(HEIGHT)]
        
        self.win = pygame.display.set_mode((WIDTH * self.scale, HEIGHT * self.scale))
        self.win.fill(OFF)

        pygame.display.flip()

    def set_pixel(self, x: int, y: int) -> bool: 
        '''Toggles the pixel to 0 or 1'''

        # wrap around
        x %= WIDTH
        y %= HEIGHT
        
        # set pixel by XORing with 1
        self.display[y][x] ^= 1;
        
        # check if pixel was erased
        return not self.display[y][x]
        
    def clear(self):
        '''Clear the display '''

        self.display = [[0 for x in range (WIDTH)] for y in range(HEIGHT)]
        pygame.display.flip()

    def render(self):
        '''Render the display by checking which pixels are on and off'''

        for y in range(HEIGHT):
            for x in range(WIDTH):
                colour = OFF
                if self.display[y][x]:
                    colour = ON
                pygame.draw.rect(self.win, colour, [x * self.scale, y * self.scale, self.scale, self.scale], 0)
        pygame.display.flip()

