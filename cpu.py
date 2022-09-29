import math

class CPU:
    def __init__(self, monitor, keyboard):
        self.monitor = monitor
        self.keyboard = keyboard

        self.memory = [0x0] * 4096

        self.v = [0] * 16

        self.i = 0

        self.delay_timer = 0
        self.sound_timer = 0

        self.pc = 0x200

        self.stack = []

        self.paused = []

        self.speed = 10

    def load_sprites_into_memory(self):
        sprites = [
            0xF0, 0x90, 0x90, 0x90, 0xF0, 
            0x20, 0x60, 0x20, 0x20, 0x70, 
            0xF0, 0x10, 0xF0, 0x80, 0xF0, 
            0xF0, 0x10, 0xF0, 0x10, 0xF0, 
            0x90, 0x90, 0xF0, 0x10, 0x10, 
            0xF0, 0x80, 0xF0, 0x10, 0xF0, 
            0xF0, 0x80, 0xF0, 0x90, 0xF0, 
            0xF0, 0x10, 0x20, 0x40, 0x40, 
            0xF0, 0x90, 0xF0, 0x90, 0xF0, 
            0xF0, 0x90, 0xF0, 0x10, 0xF0, 
            0xF0, 0x90, 0xF0, 0x90, 0x90, 
            0xE0, 0x90, 0xE0, 0x90, 0xE0, 
            0xF0, 0x80, 0x80, 0x80, 0xF0, 
            0xE0, 0x90, 0x90, 0x90, 0xE0, 
            0xF0, 0x80, 0xF0, 0x80, 0xF0, 
            0xF0, 0x80, 0xF0, 0x80, 0x80  
        ]

        for i in range(len(sprites)): self.memory[i] = sprites[i] 
        

    def load_program_into_memory(self, program):
        for loc in range(len(program)): self.memory[0x200 + loc] = program[loc]
        print("program loaded into memory")

    def load_rom(self, rom_name):
        r = open(rom_name, "rb")
        self.load_program_into_memory([i for i in r.read()])
        
        

    def cycle(self):
        for i in range(self.speed):
            if not self.paused:
                opcode = self.memory[self.pc] << 8 or self.memory[self.pc + 1]
                print(opcode)
                self.execute_instruction(opcode)

        if not self.paused: self.update_timers()


        self.monitor.render()


    def update_timers(self):
        if self.delay_timer > 0: self.delay_timer -= 1
        if self.sound_timer > 0: self.sound_timer -= 1

    

    def execute_instruction(self, opcode):
        self.pc += 2

        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        match (opcode & 0xF000):
            case 0x0000:
                match opcode:
                    case 0x00E0:
                        self.monitor.clear()
                    case 0x00EE:
                        self.stack.pop()
            case 0x1000:
                self.pc = (opcode & 0xFFF)
            case 0x2000:
                self.stack.append(self.pc)
                self.pc = opcode & 0xFFF
            case 0x3000:
                if self.v[x] == (opcode & 0xFF):
                    self.pc += 2
            case 0x4000:
                if self.v[x] != (opcode & 0xFF):
                    self.pc += 2
            case 0x5000:
                if self.v[x] == self.v[y]:
                    self.pc += 2
            case 0x6000:
                self.v[x] = opcode & 0xFF
            case 0x7000:
                self.v[x] += opcode & 0xFF
            case 0x8000:
                match (opcode & 0xF):
                    case 0x0:
                        self.v[x] = self.v[y]
                    case 0x1:
                        self.v[x] |= self.v[y]     
                    case 0x2:
                        self.v[x] &= self.v[y]
                    case 0x3:
                        self.v[x] ^= self.v[y]
                    case 0x4:
                        sum = (self.v[x] + self.v[y])

                        self.v[0xF] = 0

                        if sum > 0xFF: self.v[0xF] = 1

                        self.v[x] = sum

                    case 0x5:
                        self.v[0xF] = 0

                        if self.v[x] > self.v[y]: self.v[0xF] = 1

                        self.v[x] -= self.v[y]
                    case 0x6:
                        self.v[0xF] = self.v[x] & 0x1

                        self.v[x] >>= 1
                    case 0x7:
                        self.v[0xF] = 0

                        if self.v[y] > self.v[x]: self.v[0xF] = 1

                        self.v[x] = self.v[y] - self.v[x]
                    case 0xE:
                        self.v[0xF] = self.v[x] & 0x80
                        self.v[x] <<= 1
            case 0x9000:
                if self.v[x] != self.v[y]: self.pc += 2 
            case 0xA000:
                self.i = (opcode & 0xFFF)
            case 0xB000:
                self.pc = (opcode & 0xFFF) + self.v[0]
            case 0xC000:
                rand = math.floor(math.random() * 0xFF)
                self.v[x] = rand & (opcode & 0xFF)
            case 0xD000:

                
                width = 8
                height = (opcode & 0xF)

                self.v[0xF] = 0

                for row in range(height):
                    sprite = self.memory[self.i + row]

                    for col in range(width):
                        if (sprite & 0x80) > 0:
                            if self.monitor.set_pixel(self.v[x] + col, self.v[y] + row):
                                self.v[0xF] = 1
                    
                    sprite <<= 1

            case 0xE000:
                match (opcode & 0xFF):
                    case 0x9E:
                        if self.keyboard.key_pressed[self.v[x]]: self.pc += 2 
                    case 0xA1:
                        if not self.keyboard.key_pressed[self.v[x]]: self.pc += 2
            case 0xF000:
                match (opcode & 0xFF):
                    case 0x07:
                        self.v[x] = self.delay_timer
                    case 0x0A:
                        self.paused = True
                        
                        key = None

                        while self.paused: 
                            key_down = False

                            for i, k in enumerate(self.keys):
                                if k:
                                    key = i
                                    key_down = True
                            
                            if key_down: break
                        
                        self.v[x] = key
                        
                    case 0x15:
                        self.delay_timer = self.v[x]
                    case 0x18:
                        self.sound_timer = self.v[x]
                    case 0x1E:
                        self.i += self.v[x]
                    case 0x29:
                        self.i = self.v[x] * 5
                    case 0x33:
                        self.memory[self.i] = int(self.v[x] // 100)

                        self.memory[self.i + 1] = int((self.v[x] % 10) // 10)

                        self.memory[self.i + 2] = int(self.v[x] % 10)

                    case 0x55:
                        for register_index in range(x):
                            self.memory[self.i + register_index] = self.v[register_index]
                    case 0x65:
                        for register_index in range(x):
                            self.v[register_index] = self.memory[self.i + register_index]
                    
            
            
            

