# Chip 8 Emulator


![IBM logo](screenshots/IBM%20logo.png)
![IBM logo](screenshots/opcodecheck.png)
![IBM logo](screenshots/Pong.png)


## Description

A Chip 8 interpreter implemented in python and pygame.

The motivation for this project was to learn how emulators work as well as learning to make a graphical application using python.

## Installation

```
git clone https://github.com/arrrayyy/chip8
cd chip8
pip install -r requirements.txt
```

## Usage

``python chip8.py "ROMNAME"``

where ``"ROMNAME"`` is the name of the rom and its file extension as well as the path to it

### e.g.

``python chip8.py IBMLogo.ch8``

``python chip8.py path/to/rom/Pong.ch8``

Roms can be stored in directory where emulator is or you could provide a path to the rom.

Roms can be found all over online, some roms include BLITZ, Pong, IBM logo, op code tests etc.

### Keys

#### Pygame

| 1 | 2 | 3 | 4 |
|---|---|---|---|
| q | w | e | r |
| a | s | d | f |
| z | x | c | v | 

#### Chip 8

| 1 | 2 | 3 | C |
|---|---|---|---|
| 4 | 5 | 6 | D |
| 7 | 8 | 9 | E |
| A | 0 | B | F |

## References

https://en.wikipedia.org/wiki/CHIP-8

http://devernay.free.fr/hacks/chip8/C8TECH10.HTM

https://www.freecodecamp.org/news/creating-your-very-own-chip-8-emulator/
