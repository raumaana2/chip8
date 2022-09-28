import pygame

from monitor import Monitor 
from keyboard import Keyboard


pygame.display.set_caption("Chip8")

FPS = 60

def init():
    monitor = Monitor(20)
    keyboard = Keyboard()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT: 
                    run = False
                case pygame.KEYDOWN:
                    keyboard.key_down(event.key)
                case pygame.KEYUP:
                    keyboard.key_up(event.key)
        monitor.test_render()
        monitor.render()

    
    pygame.quit()
  

def main(): 
    init()

if __name__ == "__main__": main()