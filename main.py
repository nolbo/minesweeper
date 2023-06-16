import random
import time
import os
import sys
import keyboard
from typing import Final

MAP_WIDTH: Final = 35
MAP_HEIGHT: Final = 16
NUM_OF_MINESWEEPER: Final = (MAP_WIDTH * MAP_HEIGHT) // 100 * 20

ground = [[0 for i in range(MAP_WIDTH)] for j in range(MAP_HEIGHT)]
viewPoint = [[0 for i in range(MAP_WIDTH)] for j in range(MAP_HEIGHT)]
minesweeperPoint = []
playCount = 0
end = False
startTime = time.time()
pos = [MAP_WIDTH // 2, MAP_HEIGHT // 2] # [x, y]

def numOfMinesweeperAsPercentageOfMapSize(percentage) :
    return (MAP_WIDTH * MAP_HEIGHT) // 100 * percentage

def printGround(x = -1, y = -1) :
    os.system('cls')
    rowNum = '     '
    for i in range(MAP_WIDTH) :
        if ((i + 1) // 10) % 2 == 0 : 
            rowNum += '\033[95m{0}\033[0m '.format((i + 1) // 10)
        else :
            rowNum += '\033[35m{0}\033[0m '.format((i + 1) // 10)
    
    rowNum += '\n     '
    for i in range(MAP_WIDTH) :
        if ((i + 1) // 10) % 2 == 0 : 
            rowNum += '\033[95m{0}\033[0m '.format((i + 1) % 10)
        else :
            rowNum += '\033[35m{0}\033[0m '.format((i + 1) % 10)
    rowNum += '\n     ' + '━' * (MAP_WIDTH * 2 - 1)
    print(rowNum)
    
    for i in range(MAP_HEIGHT) :
        if ((i + 1) // 10) % 2 == 0 : 
            r = '\033[95m{0}\033[0m │ '.format(str(i + 1).zfill(2))
        else :
            r = '\033[35m{0}\033[0m │ '.format(str(i + 1).zfill(2))
        
        for j in range(MAP_WIDTH) :
            if (x != -1 and y != -1 and x == j and y == i)  :
                r += '\033[1m\033[7m'
            match viewPoint[i][j] :
                case 0 :
                    r += '■'    
                case 1 :
                    if ground[i][j] == 0 :
                        r += '\033[90m□\033[0m'
                    else :
                        if ground[i][j] == 'm' :
                            r += '\033[31m●\033[0m'
                        else :
                            match ground[i][j] :
                                case 1 : r += '\033[96m'
                                case 2 : r += '\033[94m'
                                case 3 : r += '\033[92m'
                                case 4 : r += '\033[93m'
                                case 5 : r += '\033[91m'
                                case 6 : r += '\033[95m'
                                case 7 : r += '\033[35m'
                                case 8 : r += '\033[97m'
                            r += str(ground[i][j]) + '\033[0m'
                case 2 :
                    r += '\033[33m▶\033[0m'
            if (x != -1 and y != -1 and x == j and y == i)  :
                r += '\033[0m'
            r += ' '
        print(r)

def openBlankTile(x, y, _check = []) :
    check = _check
    check.append([y, x])

    if ground[y][x] != 0 :
        viewPoint[y][x] = 1
        return
    viewPoint[y][x] = 1
    recursionPos = [[y - 1, x - 1], [y - 1, x], [y - 1, x + 1], [y, x - 1], [y, x + 1], [y + 1, x - 1], [y + 1, x], [y + 1, x + 1]]

    for i in recursionPos :
        if (i[0] > (MAP_HEIGHT - 1) or i[0] < 0) or (i[1] > (MAP_WIDTH - 1) or i[1] < 0) :
            continue
        if i in check :
            continue
        openBlankTile(i[1], i[0], check)

def openAllTile() :
    global viewPoint
    viewPoint = [[1 for i in range(MAP_WIDTH)] for j in range(MAP_HEIGHT)]
    for [y, x] in minesweeperPoint :
        viewPoint[y][x] = 2

def isGameEnded() :
    for i in range(MAP_HEIGHT) :
        for j in range(MAP_WIDTH) :
            match viewPoint[i][j] :
                case 0 :
                    if ground[i][j] != 'm' : 
                        return False
                case 2 :
                    if ground[i][j] != 'm' :
                        return False
    global end
    end = True
    return True

def createGround(startX, startY, _count_mine = NUM_OF_MINESWEEPER) :
    count_mine = _count_mine
    
    while count_mine > 0 :
        [y, x] = [random.randrange(0, MAP_HEIGHT), random.randrange(0, MAP_WIDTH)]
        if x == startX and y == startY :
            continue

        if ground[y][x] != 'm' : 
            recursionPos = [
                [startY - 1, startX - 1], [startY - 1, startX], [startY - 1, startX + 1], 
                [startY,     startX - 1], [startY,     startX], [startY,     startX + 1], 
                [startY + 1, startX - 1], [startY + 1, startX], [startY + 1, startX + 1]
            ]
            if not [y, x] in recursionPos :
                ground[y][x] = 'm'
                minesweeperPoint.append([y, x])

                for i in range(y - 1 if y > 0 else 0, y + 2 if y < (MAP_HEIGHT - 1) else MAP_HEIGHT) : # y축
                    for j in range(x - 1 if x > 0 else 0, x + 2 if x < (MAP_WIDTH - 1) else MAP_WIDTH) : # x축
                        if ground[i][j] == 'm' or (startX == j and startY == i) :
                            continue
                        ground[i][j] += 1
                count_mine -= 1

def printGameInfoMsg(_playCount, _startTime, msg = 'default') :
    DEFAULT_LENGTH_OF_LINE: Final = 23 + (MAP_WIDTH * 2 - 1)
    endTime = time.time()
    _playTime = int(endTime - _startTime)
    countMsg = 'Count(s): \033[33m{0}\033[0m'.format(_playCount)
    timeMsg = 'Playtime: \033[35m{0:02d}:{1:02d}:{2:02d}\033[0m'.format(_playTime // 3600, _playTime % 3600 // 60, _playTime % 3600 % 60)
    
    match msg :
        case 'default' :
            print('=' * (DEFAULT_LENGTH_OF_LINE - 18))
            print(countMsg, timeMsg.rjust(DEFAULT_LENGTH_OF_LINE - len(countMsg) - 1))
            print('Point: \033[1m\033[36m({0:02d}, {1:02d})\033[0m'.format(pos[0], pos[1]))
        case 'win' :
            print('=' * (MAP_WIDTH - 1), '\033[94mWIN!\033[0m', '=' * (MAP_WIDTH - 1))
            print(countMsg, timeMsg.rjust(DEFAULT_LENGTH_OF_LINE - len(countMsg) - 1))
            print('Last: \033[1m\033[36m({0}, {1})\033[0m'.format(pos[0], pos[1]))
        case 'gameover' :
            print('=' * (MAP_WIDTH - 3), '\033[90mGameOver\033[0m', '=' * (MAP_WIDTH - 3))
            print(countMsg, timeMsg.rjust(DEFAULT_LENGTH_OF_LINE - len(countMsg) - 1))
            print('Last: \033[1m\033[36m({0}, {1})\033[0m'.format(pos[0], pos[1]))
    if playCount == 0 :
        print('=' * (DEFAULT_LENGTH_OF_LINE - 18))
        print('Move     ', '\033[44m[←]\033[0m \033[44m[→]\033[0m \033[44m[↑]\033[0m \033[44m[↓]\033[0m'.rjust(DEFAULT_LENGTH_OF_LINE + 8))
        print('Open Tile', '\033[42m\033[30m[SpaceBar]\033[0m'.rjust(DEFAULT_LENGTH_OF_LINE - 14))
        print('Flag     ', '\033[43m\033[30m[F]\033[0m'.rjust(DEFAULT_LENGTH_OF_LINE - 14))
        print('Exit Game', '\033[101m\033[30m[Esc]\033[0m'.rjust(DEFAULT_LENGTH_OF_LINE - 13))
        # print('Restart  ', '\033[105m\033[30m[F5]\033[0m'.rjust(DEFAULT_LENGTH_OF_LINE - 13))

def movePoint(key) :
    match key :
        case 'left' :
            if pos[0] != 1 :
                pos[0] -= 1
            else :
                pos[0] = MAP_WIDTH
        case 'right' :
            if pos[0] != MAP_WIDTH :
                pos[0] += 1
            else :
                pos[0] = 1
        case 'up' :
            if pos[1] != 1 :
                pos[1] -= 1
            else :
                pos[1] = MAP_HEIGHT
        case 'down' :
            if pos[1] != MAP_HEIGHT :
                pos[1] += 1
            else :
                pos[1] = 1

    didChangeBoard()

def willChangeBoard() :
    global playCount
    playCount += 1
    if playCount == 1 :
        createGround(pos[0] - 1, pos[1] - 1)

def didChangeBoard() :
    if isGameEnded() == True :
        openAllTile()
        printGround(pos[0] - 1, pos[1] - 1)
        printGameInfoMsg(playCount, startTime, 'win')
    else :
        printGround(pos[0] - 1, pos[1] - 1)
        printGameInfoMsg(playCount, startTime)

def openTile() :
    willChangeBoard()
    
    if viewPoint[pos[1] - 1][pos[0] - 1] != 1 :
        if viewPoint[pos[1] - 1][pos[0] - 1] == 2 :
            viewPoint[pos[1] - 1][pos[0] - 1] = 0
        else :
            match ground[pos[1] - 1][pos[0] - 1] :
                case 'm' :
                    openAllTile()
                    printGround()
                    printGameInfoMsg(playCount, startTime, 'gameover')
                    global end
                    end = True
                    return
                case 0 :
                    openBlankTile(pos[0] - 1, pos[1] - 1)
                case _ :
                    viewPoint[pos[1] - 1][pos[0] - 1] = 1
                    if viewPoint[pos[1] - 1][pos[0] - 1] == 2 :
                        viewPoint[pos[1] - 1][pos[0] - 1] = 0

    didChangeBoard()

def setFlag() :
    willChangeBoard()

    if viewPoint[pos[1] - 1][pos[0] - 1] != 1 :
        if viewPoint[pos[1] - 1][pos[0] - 1] == 2 :
            viewPoint[pos[1] - 1][pos[0] - 1] = 0
        else :
            viewPoint[pos[1] - 1][pos[0] - 1] = 2

    didChangeBoard()

keyboard.on_press_key('left', (lambda _ : movePoint('left')))
keyboard.on_press_key('right', (lambda _ : movePoint('right')))
keyboard.on_press_key('up', (lambda _ : movePoint('up')))
keyboard.on_press_key('down', (lambda _ : movePoint('down')))
keyboard.on_press_key('space', (lambda _ : openTile()))
keyboard.on_press_key('f', (lambda _ : setFlag()))
# keyboard.on_press_key('F5', (lambda _ : os.execl(sys.executable, sys.executable, *sys.argv)))


printGround(pos[0] - 1, pos[1] - 1)
printGameInfoMsg(playCount, startTime)

while True :
    try :
        key = keyboard.read_key();
        
        if key == 'esc' or end == True :
            break
    except :
        print('Invalid commend. Retry')
    
