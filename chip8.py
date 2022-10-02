import pygame
from monitor import Monitor 
from keyboard import Keyboard
from cpu import CPU

pygame.display.set_caption("Chip8")

FPS = 60

run = True

    

def main():
    monitor = Monitor(30)
    keyboard = Keyboard()
    cpu = CPU(monitor, keyboard)
    cpu.load_sprites_into_memory()
    cpu.load_rom("./roms/Pong.ch8")
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        cpu.event_handler()
        cpu.cycle()
  

if __name__ == "__main__": main()