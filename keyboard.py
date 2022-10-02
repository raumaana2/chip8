class Keyboard:
    def __init__(self):
        self.key_map = {
            49: 0x1,    #1
            50: 0x2,    #2
            51: 0x3,    #3
            52: 0xc,    #4
            113: 0x4,    #Q
            119: 0x5,    #W
            101: 0x6,    #E
            114: 0xD,    #R
            97: 0x7,    #A
            115: 0x8,    #S
            100: 0x9,    #D
            102: 0xE,    #F
            122: 0xA,    #Z
            120: 0x0,    #X
            99: 0xB,    #C
            118: 0xF     #V
        }
        
        self.key_pressed = [False for i in range(16)]


    def is_key_pressed(self, key_code):
        return self.key_pressed[key_code]


    def key_up(self, event_key):
        try:
            key = self.key_map[event_key]
            self.key_pressed[key] = False
        except: pass

    def key_down(self, event_key):
        try:
            key = self.key_map[event_key]
            self.key_pressed[key] = True
        except: pass
    

