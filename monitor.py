import pygame
import math

OFF = (0, 0, 0)
ON = (255, 255, 255)

class Monitor:
    '''
    Class used to generate graphics for emulator

    Attributes:
        col: display columns
        row: display rows
        display: where graphics is shown

    '''
    def __init__(self, scale: int):
        self.col = 64
        self.row = 32

        self.scale = scale

        self.display =  [0] * (self.row * self.col)
        
        self.win = pygame.display.set_mode((self.col * self.scale, self.row * self.scale))
        self.win.fill(OFF)

        pygame.display.flip()




    '''
    Toggles the pixel to 0 or 1
    '''
    def set_pixel(self, x: int, y: int) -> bool: 
        # ensure pixel is not out of bounds and if so wrap around
        if x >= self.col: x -= self.col
        elif x < 0: x += self.col

        if y >= self.row: y -= self.row
        elif y < 0: x += self.row

        pixel_location = x + (y * self.col);
        # set pixel by XORing with 1
        self.display[pixel_location] ^= 1;
        
        # check if pixel was erased
        return not self.display[pixel_location] 
        

    '''
    Clear the display 
    '''
    def clear(self):
        self.display = [[0] * self.row] * self.col

    def render(self):
        for i in range(self.col * self.row):
            x = (i % self.col) * self.scale

            y = math.floor(i / self.col) * self.scale

            colour = OFF

            if self.display[i]:
                colour = ON
            pygame.draw.rect(self.win, colour, [x, y, self.scale, self.scale], 0)
        pygame.display.flip()

    def test_render(self):
        self.set_pixel(0,0)
        self.set_pixel(61,31)


    