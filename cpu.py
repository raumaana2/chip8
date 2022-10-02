import random
import pygame
import sys


class CPU:
    '''
    Class used to for handling instructions 

    Attributes:
       monitor: display of emulator
       keyoard: keyboard of emulator
       memory: 4KB of memory 
       v: 16 8bit registers 
       i: stores memory address
       pc: Program counter which stores current instruction
       stack: store return addresses
       speed: determines how many instructions are executed per cycle

    '''

    def __init__(self, monitor, keyboard):
        self.monitor = monitor
        self.keyboard = keyboard

        self.memory = [0x0 for x in range(4096)] 

        self.v = [0x0 for x in range(16)]

        self.i = 0

        # timers
        self.delay_timer = 0
        self.sound_timer = 0

        
        self.pc = 0x200

        self.stack = []

        self.speed = 10


    def load_sprites_into_memory(self):
        '''Hex values that represent groups of 8x5 sprites which are then
        loaded into memory'''

        sprites = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,   # 0
            0x20, 0x60, 0x20, 0x20, 0x70,   # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0,   # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0,   # 3
            0x90, 0x90, 0xF0, 0x10, 0x10,   # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0,   # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0,   # 6
            0xF0, 0x10, 0x20, 0x40, 0x40,   # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0,   # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0,   # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90,   # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,   # B
            0xF0, 0x80, 0x80, 0x80, 0xF0,   # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,   # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0,   # E
            0xF0, 0x80, 0xF0, 0x80, 0x80    # F
        ]

        # sprites stored in interpreter section of memory starting at 0x000
        for i, s in enumerate(sprites):
            self.memory[i] = s


    def load_rom(self, rom_name):
        '''Load the rom into memory starting from memory location 0x200'''

        rom = open(rom_name, "rb")
        for i, r in enumerate(rom.read()):
            self.memory[0x200 + i] = r

    def cycle(self):
        '''executes a number of instructions according to speed'''

        for i in range(self.speed):
            '''
                instructions are 16bits long but each index in memory is 
                8 bits so we have to combine 2 piecese of memory to get the
                opcode

                Take the first piece as 0xnn then we shift 8 bits left to get
                0xnn00 which we then OR with the second piece to get the full
                opcode
            '''
            opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]
            self.execute_instruction(opcode)

        self.update_timers()

        self.monitor.render()

    def update_timers(self):
        '''
        Delay timer decrements by 1 at a rate of 60Hz until it reaches 0
        where it deactivates

        Sound timer also decrements by 1 at a rate of 60Hz and as long as
        it is non zero, sound plays.
        '''

        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1

    def draw(self, x, y, n):
        '''
        Display n-byte sprite starting at memory location I at (Vx, Vy),
        set VF = collision
        '''

        self.v[0xF] = 0

        for i in range(n):
            sprite = self.memory[self.i + i]

            for j in range(8):
                if (sprite & 0x80):
                    if self.monitor.set_pixel(self.v[x] + j, self.v[y] + i):
                        self.v[0xF] = 1

                sprite <<= 1


    def event_handler(self):
        '''event handler to deal with closing the app and key events'''

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT: 
                    sys.exit()
                case pygame.KEYDOWN:
                    self.keyboard.key_down(event.key)
                case pygame.KEYUP:
                    self.keyboard.key_up(event.key)


    def execute_instruction(self, opcode):
        '''instructions are executed here and after each execution,
        program counter incremented by 2 to fetch next full instruction'''

        self.pc += 2

        x = (opcode & 0x0F00) >> 8 # 2nd nibble
        y = (opcode & 0x00F0) >> 4 # 3rd nibble
        nnn = (opcode & 0x0FFF) # lowest 12 bits, address
        kk = (opcode & 0x00FF) # lowest 8 bits
        n = (opcode & 0x000F) # lowest nibble
        op = (opcode & 0xF000) # operation
        match op:
            case 0x0000:
                match opcode:
                    case 0x00E0:
                        '''CLS
                        Clear display'''

                        self.monitor.clear()
                    case 0x00EE:
                        '''RET
                        Return from subroutine'''

                        self.pc = self.stack.pop()
            case 0x1000:
                '''JP addr
                jump to location nnn'''

                self.pc = nnn
            case 0x2000:
                '''CALL addr
                Call subroutine at nnn'''

                self.stack.append(self.pc)
                self.pc = nnn
            case 0x3000:
                '''SE Vx, byte
                skip next instruction if Vx = kk'''

                if self.v[x] == kk:
                    self.pc += 2
            case 0x4000:
                '''SNE Vx, byte
                skip next instruction if Vx != kk'''

                if self.v[x] != kk:
                    self.pc += 2
            case 0x5000:
                '''SE Vx, Vy
                skip next instruction if Vx = Vy'''

                if self.v[x] == self.v[y]:
                    self.pc += 2
            case 0x6000:
                '''LD Vx, byte
                set Vx = kk'''

                self.v[x] = kk
            case 0x7000:
                '''ADD Vx, byte
                set Vx = Vx + kk'''

                self.v[x] = (self.v[x] + kk) % 256
            case 0x8000:
                match n:
                    case 0x0:
                        '''LD Vx, Vy
                        set Vx = Vy'''

                        self.v[x] = self.v[y]
                    case 0x1:
                        '''OR Vx, Vy
                        set Vx = Vx OR Vy'''

                        self.v[x] = self.v[x] | self.v[y]
                    case 0x2:
                        '''AND Vx, Vy
                        set Vx = Vx AND Vy'''

                        self.v[x] = self.v[x] & self.v[y]
                    case 0x3:
                        '''XOR Vx, Vy
                        set Vx = Vx XOR Vy'''

                        self.v[x] = self.v[x] ^ self.v[y]
                    case 0x4:
                        '''ADD Vx, Vy
                        set Vx = Vx + Vy, VF = carry'''

                        sum = (self.v[x] + self.v[y])

                        self.v[0xF] = 0

                        if sum > 0xFF:
                            self.v[0xF] = 1

                        self.v[x] = sum % 256

                    case 0x5:
                        '''SUB Vx, Vy
                        set Vx = Vx - Vy, VF = NOT borrow'''

                        self.v[0xF] = 0

                        if self.v[x] > self.v[y]:
                            self.v[0xF] = 1

                        res = self.v[x] - self.v[y]

                        self.v[x] = res % 256

                    case 0x6:
                        '''SHR Vx {, Vy}
                        set Vx = SHR 1'''

                        self.v[0xF] = self.v[x] & 0x1

                        self.v[x] >>= 1
                    case 0x7:
                        '''SUBN Vx, Vy
                        set Vx = Vy - Vx, set VF = NOT borrow'''

                        res = self.v[y] - self.v[x]

                        self.v[0xF] = 1 if res > 0 else 0

                        self.v[x] = res % 256

                    case 0xE:
                        '''SHL Vx {, Vy}
                        set Vx = Vx SHL 1'''

                        self.v[0xF] = (self.v[x] & 0x80) >> 7
                        self.v[x] = (self.v[x] << 1) % 256
            case 0x9000:
                '''SNE Vx, Vy
                skip next instruction if Vx != Vy'''

                if self.v[x] != self.v[y]:
                    self.pc += 2
            case 0xA000:
                '''LD I, addr
                set I = nn'''

                self.i = nnn
            case 0xB000:
                '''JP V0, addr
                jump to location nnn + V0'''

                self.pc = nnn + self.v[0]
            case 0xC000:
                '''RND Vx, byte
                set Vx = random byte AND kk'''

                self.v[x] = random.randint(0, 255) & kk
            case 0xD000:
                '''DRW Vx, Vy, nibble
                Display n-byte sprite starting at 
                memory location I at (Vx, Vy), set VF = collision'''

                self.draw(x, y, n)
            case 0xE000:
                match kk:
                    case 0x9E:
                        '''SKP Vx
                        skip next instruction if key with value of Vx
                        is pressed'''

                        if self.keyboard.is_key_pressed(self.v[x]):
                            self.pc += 2
                    case 0xA1:
                        '''SKNP Vx
                        skip next instruction if key with the value of Vx
                        is not pressed'''

                        if not self.keyboard.is_key_pressed(self.v[x]):
                            self.pc += 2
            case 0xF000:
                match kk:
                    case 0x07:
                        '''LD Vx, DT
                        set Vx = delay timer value'''

                        self.v[x] = self.delay_timer
                    case 0x0A:
                        '''LD Vx, K
                        wait for key press, store the value of the key in Vx'''

                        is_key_pressed = True
                        while is_key_pressed:
                            self.event_handler()
                            for i, k in enumerate(self.keyboard.key_pressed):
                                if k:
                                    self.v[x] = i
                                    is_key_pressed = False
                                    break
                    case 0x15:
                        '''LD DT, Vx
                        set delay timer = Vx'''

                        self.delay_timer = self.v[x]
                    case 0x18:
                        '''LD ST, Vx
                        set sound timer = Vx'''

                        self.sound_timer = self.v[x]
                    case 0x1E:
                        '''ADD I, Vx
                        set I = I + Vx'''

                        self.i += self.v[x] 
                    case 0x29:
                        '''LD F, Vx
                        set I = loation of sprite for digit Vx'''

                        self.i = self.v[x] * 5
                    case 0x33:
                        '''LD B, Vx
                        store BCD representation of Vx in memory locations
                        I, I+1, I+2'''

                        self.memory[self.i + 2] = self.v[x] % 10
                        self.memory[self.i + 1] = self.v[x] % 100 // 10
                        self.memory[self.i ] = self.v[x] // 100
                    case 0x55:
                        '''LD [I], Vx
                        store register V0 through Vx in memory starting at
                        location I'''

                        for register_index in range(x + 1):
                            self.memory[self.i +
                                        register_index] = self.v[register_index]
                    case 0x65:
                        '''LD Vx, [I]
                        read registers V0 through Vx from memory starting at
                        location I'''

                        for register_index in range(x + 1):
                            self.v[register_index] = self.memory[self.i +
                                                                 register_index]
