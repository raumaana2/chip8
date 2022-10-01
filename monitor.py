import pygame
import math

OFF = (0, 0, 0)
ON = (255, 255, 255)

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

        self.display =  [[0] * WIDTH for x in range(HEIGHT)]
        
        self.win = pygame.display.set_mode((WIDTH * self.scale, HEIGHT * self.scale))
        self.win.fill(OFF)

        pygame.display.flip()




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
    Clear the display 
    '''
    def clear(self):
        self.display = [[0] * WIDTH] * HEIGHT

    def render(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                colour = OFF
                if self.display[y][x]:
                    colour = ON
                pygame.draw.rect(self.win, colour, [x * self.scale, y * self.scale, self.scale, self.scale], 0)
        pygame.display.flip()

    def test(self):
        self.set_pixel(0,0)
        self.set_pixel(0,63)
        self.set_pixel(31,63)
        self.set_pixel(31, 0)

