from dataclasses import dataclass
import keyboard

@dataclass
class Position() :
    maxY: int
    maxX: int
    y: int # y
    x: int # x

    def moveXTo(self, x: int) :
        self.x = x

    def moveYTo(self, y: int) :
        self.y = y

    def moveXBy(self, x: int) :
        to = (self.x + x) % self.maxX
        self.x = self.maxX if to == 0 else to

    def moveYBy(self, y: int) :
        to = (self.y + y) % self.maxY
        self.y = self.maxY if to == 0 else to

pos = Position(16, 16, 8, 8)

def __movePoint(key) :
    match key :
        case 'left' :
            pos.moveXBy(-1)
        case 'right' :
            pos.moveXBy(1)
        case 'up' :
            pos.moveYBy(-1)
        case 'down' :
            pos.moveYBy(1)

    print('X: {0} Y: {1}'.format(pos.x, pos.y))

keyboard.on_press_key('left', (lambda _ : __movePoint('left')))
keyboard.on_press_key('right', (lambda _ : __movePoint('right')))
keyboard.on_press_key('up', (lambda _ : __movePoint('up')))
keyboard.on_press_key('down', (lambda _ : __movePoint('down')))

pos.moveXBy(33)
print('X: {0} Y: {1}'.format(pos.x, pos.y))

while True :
    try :
        key = keyboard.read_key();
        
        if key == 'esc' :
            break
    except :
        print('Invalid commend. Retry')
    
