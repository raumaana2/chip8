# Chip 8 Emulator


![IBM logo](screenshots/IBM%20logo.png)
![IBM logo](screenshots/opcodecheck.png)
![IBM logo](screenshots/Pong.png)


## Description

A Chip 8 interpreter implemented in python and pygame.

The motivation for this project was to learn how emulators work as well as learning to make a graphical application using pygame.

## Installation

```
git clone https://github.com/arrrayyy/chip8
cd chip8
pip install -r requirements.txt
```

## Usage

``python chip8.py "ROMNAME"``

where ``"ROMNAME"`` is the name of the rom and its file extension

### e.g.

``python chip8.py IBMLogo.ch8``

Roms can be found all over online, some roms include BLITZ, Pong, IBM logo, op code tests etc.

## References

https://en.wikipedia.org/wiki/CHIP-8
http://devernay.free.fr/hacks/chip8/C8TECH10.HTM
https://www.freecodecamp.org/news/creating-your-very-own-chip-8-emulator/
