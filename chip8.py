import pygame
from monitor import Monitor 
from keyboard import Keyboard
from cpu import CPU
import sys
from os.path import exists

pygame.display.set_caption("Chip8")


run = True

    

def main():
    '''
    Where monitor with a scale, keyboard and cpu are initialised,
    rom is loaded into memory, where the rom filename is provided
    via a CLI argument, sprites are loaded into memory and then we
    begin the main loop.

    Inside the main loop we run emulation cycles and the event handler
    '''

    file_name = sys.argv[1]

    if not exists(f"roms/{file_name}"):
        print(f"Nonexistent ROM \"{file_name}\"")
        sys.exit()


    monitor = Monitor(30)
    keyboard = Keyboard()
    cpu = CPU(monitor, keyboard)
    cpu.load_sprites_into_memory()
    
    cpu.load_rom(f"./roms/{file_name}")
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(300)
        cpu.event_handler()
        cpu.cycle()
  

if __name__ == "__main__": main()