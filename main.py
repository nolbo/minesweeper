from typing import Final, List, Union
from dataclasses import dataclass
import random
import time
import os
import sys
import keyboard

# self.MAP_X_SIZE: Final = 35
# self.MAP_Y_SIZE: Final = 16
# NUM_OF_MINESWEEPER: Final = (self.MAP_X_SIZE * self.MAP_Y_SIZE) // 100 * 20

# ground: List[List[int]] = [[0 for i in range(self.MAP_X_SIZE)] for j in range(self.MAP_Y_SIZE)]
# view: List[List[int]] = [[0 for i in range(self.MAP_X_SIZE)] for j in range(self.MAP_Y_SIZE)]
# minesweeperPoint = []
# playCount = 0
# end = False
# startTime = time.time()
# pos = [self.MAP_X_SIZE // 2, self.MAP_Y_SIZE // 2]


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

class Game() :
    def __init__(self, x_size: int, y_size: int, numOfMinesweeper: int) -> None:
        self.VIEW_UNVISIBLE: Final = 0
        self.VIEW_VISIBLE: Final = 1
        self.VIEW_FLAG: Final = 2
        self.GROUND_VOID: Final = 0
        self.GROUND_MINESWEEPER: Final = -1
        self.GROUND_HINT1: Final = 1
        self.GROUND_HINT2: Final = 2
        self.GROUND_HINT3: Final = 3
        self.GROUND_HINT4: Final = 4
        self.GROUND_HINT5: Final = 5
        self.GROUND_HINT6: Final = 6
        self.GROUND_HINT7: Final = 7
        self.GROUND_HINT8: Final = 8
        self.MAP_X_SIZE: Final = x_size
        self.MAP_Y_SIZE: Final = y_size
        self.NUM_OF_MINESWEEPER: Final = numOfMinesweeper

        self.playCount: int = 0
        self.gameEnd: bool = False
        self.startTime: float = time.time()
        self.pos: Position = Position(self.MAP_Y_SIZE, self.MAP_X_SIZE, self.MAP_Y_SIZE // 2, self.MAP_X_SIZE // 2)
        self.ground: List[List[int]] = [[0 for _ in range(self.MAP_X_SIZE)] for _ in range(self.MAP_Y_SIZE)]
        self.view: List[List[int]]   = [[0 for _ in range(self.MAP_X_SIZE)] for _ in range(self.MAP_Y_SIZE)]
        self.minesweeperPoint: List[List[int]] = []

        keyboard.on_press_key('left',  (lambda _ : self.__movePoint('left')))
        keyboard.on_press_key('right', (lambda _ : self.__movePoint('right')))
        keyboard.on_press_key('up',    (lambda _ : self.__movePoint('up')))
        keyboard.on_press_key('down',  (lambda _ : self.__movePoint('down')))
        keyboard.on_press_key('space', (lambda _ : self.__openTile()))
        keyboard.on_press_key('f',     (lambda _ : self.__setFlag()))
        keyboard.on_press_key('F5',    (lambda _ : os.execl(sys.executable, sys.executable, *sys.argv)))

    def startGame(self) :
        self.__printGround(self.pos.y - 1, self.pos.x - 1)
        self.__printGameInfoMsg(self.playCount, self.startTime)

        while True :
            try :
                key = keyboard.read_key();

                if key == 'esc' or self.gameEnd == True :
                    break
            except :
                print('Invalid commend. Retry')

    def __printGround(self, y: int = -1, x: int = -1) :
        os.system('cls')
        yNum = '     '
        for i in range(self.MAP_X_SIZE) :
            if ((i + 1) // 10) % 2 == 0 : 
                yNum += '\033[95m{0}\033[0m '.format((i + 1) // 10)
            else :
                yNum += '\033[35m{0}\033[0m '.format((i + 1) // 10)

        yNum += '\n     '
        for i in range(self.MAP_X_SIZE) :
            if ((i + 1) // 10) % 2 == 0 : 
                yNum += '\033[95m{0}\033[0m '.format((i + 1) % 10)
            else :
                yNum += '\033[35m{0}\033[0m '.format((i + 1) % 10)
        yNum += '\n     ' + '━' * (self.MAP_X_SIZE * 2 - 1)
        print(yNum)

        for i in range(self.MAP_Y_SIZE) :
            if ((i + 1) // 10) % 2 == 0 : 
                r = '\033[95m{0}\033[0m │ '.format(str(i + 1).zfill(2))
            else :
                r = '\033[35m{0}\033[0m │ '.format(str(i + 1).zfill(2))

            for j in range(self.MAP_X_SIZE) :
                if (x != -1 and y != -1 and x == j and y == i)  :
                    r += '\033[1m\033[7m'
                match self.view[i][j] :
                    case self.VIEW_UNVISIBLE :
                        r += '■'    
                    case self.VIEW_VISIBLE :
                        if self.ground[i][j] == 0 :
                            r += '\033[90m□\033[0m'
                        else :
                            if self.ground[i][j] == -1 :
                                r += '\033[31m●\033[0m'
                            else :
                                match self.ground[i][j] :
                                    case self.GROUND_HINT1 : r += '\033[96m'
                                    case self.GROUND_HINT2 : r += '\033[94m'
                                    case self.GROUND_HINT3 : r += '\033[92m'
                                    case self.GROUND_HINT4 : r += '\033[93m'
                                    case self.GROUND_HINT5 : r += '\033[91m'
                                    case self.GROUND_HINT6 : r += '\033[95m'
                                    case self.GROUND_HINT7 : r += '\033[35m'
                                    case self.GROUND_HINT8 : r += '\033[97m'
                                r += str(self.ground[i][j]) + '\033[0m'
                    case self.VIEW_FLAG :
                        r += '\033[33m▶\033[0m'
                if (x != -1 and y != -1 and x == j and y == i)  :
                    r += '\033[0m'
                r += ' '
            print(r)

    def __willChangeBoard(self) :
        self.playCount += 1
        if self.playCount == 1 :
            self.__createGround(self.pos.y - 1, self.pos.x - 1)

    def __didChangeBoard(self) :
        if self.__isGameEnded() == True :
            self.__openAllTile(isWin=True)
            self.__printGround(self.pos.y - 1, self.pos.x - 1)
            self.__printGameInfoMsg(self.playCount, self.startTime, 'win')
        else :
            self.__printGround(self.pos.y - 1, self.pos.x - 1)
            self.__printGameInfoMsg(self.playCount, self.startTime)

    def __openTile(self) :
        self.__willChangeBoard()

        if self.view[self.pos.y - 1][self.pos.x - 1] != 1 :
            if self.view[self.pos.y - 1][self.pos.x - 1] == 2 :
                self.view[self.pos.y - 1][self.pos.x - 1] = 0
            else :
                match self.ground[self.pos.y - 1][self.pos.x - 1] :
                    case -1 :
                        self.__openAllTile(isWin=False)
                        self.__printGround()
                        self.__printGameInfoMsg(self.playCount, self.startTime, 'gameover')
                        self.gameEnd = True
                        return
                    case 0 :
                        self.__openBlankTile(self.pos.y - 1, self.pos.x - 1)
                    case _ :
                        self.view[self.pos.y - 1][self.pos.x - 1] = 1
                        if self.view[self.pos.y - 1][self.pos.x - 1] == 2 :
                            self.view[self.pos.y -1][self.pos.x - 1] = 0

        self.__didChangeBoard()

    def __openBlankTile(self, y: int, x: int, _check: List = []) :
        check = _check
        check.append([y, x])

        if self.ground[y][x] != 0 :
            self.view[y][x] = 1
            return
        self.view[y][x] = 1
        recursionPos = [[y - 1, x - 1], [y - 1, x], [y - 1, x + 1], [y, x - 1], [y, x + 1], [y + 1, x - 1], [y + 1, x], [y + 1, x + 1]]

        for i in recursionPos :
            if (i[0] > (self.MAP_Y_SIZE - 1) or i[0] < 0) or (i[1] > (self.MAP_X_SIZE - 1) or i[1] < 0) :
                continue
            if i in check :
                continue
            self.__openBlankTile(i[0], i[1], check)

    def __openAllTile(self, isWin: bool) :
        self.view = [[1 for _ in range(self.MAP_X_SIZE)] for _ in range(self.MAP_Y_SIZE)]

        for [y, x] in self.minesweeperPoint :
            self.view[y][x] = 2 if isWin else 1

    def __isGameEnded(self) :
        for i in range(self.MAP_Y_SIZE) :
            for j in range(self.MAP_X_SIZE) :
                match self.view[i][j] :
                    case 0 :
                        if self.ground[i][j] != -1 : 
                            return False
                    case 2 :
                        if self.ground[i][j] != -1 :
                            return False
        self.gameEnd = True
        return True

    def __createGround(self, startY: int, startX: int) :
        count_mine = self.NUM_OF_MINESWEEPER
    
        while count_mine > 0 :
            [y, x] = [random.randrange(0, self.MAP_Y_SIZE), random.randrange(0, self.MAP_X_SIZE)]
            if y == startY and x == startX :
                continue

            if self.ground[y][x] != -1 : 
                recursionPos = [
                    [startY - 1, startX - 1], [startY - 1, startX], [startY - 1, startX + 1], 
                    [startY,     startX - 1], [startY,     startX], [startY,     startX + 1], 
                    [startY + 1, startX - 1], [startY + 1, startX], [startY + 1, startX + 1]
                ]
                if not [y, x] in recursionPos :
                    self.ground[y][x] = -1
                    self.minesweeperPoint.append([y, x])

                    for i in range(y - 1 if y > 0 else 0, y + 2 if y < (self.MAP_Y_SIZE - 1) else self.MAP_Y_SIZE) : # y축
                        for j in range(x - 1 if x > 0 else 0, x + 2 if x < (self.MAP_X_SIZE - 1) else self.MAP_X_SIZE) : # x축
                            if self.ground[i][j] == -1 or (startX == j and startY == i) :
                                continue
                            self.ground[i][j] += 1
                    count_mine -= 1

    def __printGameInfoMsg(self, _playCount: int, _startTime: float, msg = 'default') :
        DEFAULT_LENGTH_OF_LINE: Final = 23 + (self.MAP_X_SIZE * 2 - 1)
        endTime = time.time()
        _playTime = int(endTime - _startTime)
        countMsg = 'Count(s): \033[33m{0}\033[0m'.format(_playCount)
        timeMsg = 'Playtime: \033[35m{0:02d}:{1:02d}:{2:02d}\033[0m'.format(_playTime // 3600, _playTime % 3600 // 60, _playTime % 3600 % 60)

        match msg :
            case 'default' :
                print('=' * (DEFAULT_LENGTH_OF_LINE - 18))
                print(countMsg, timeMsg.rjust(DEFAULT_LENGTH_OF_LINE - len(countMsg) - 1))
                print('Point: \033[1m\033[36m({0:02d}, {1:02d})\033[0m'.format(self.pos.x, self.pos.y))
            case 'win' :
                print('=' * (self.MAP_X_SIZE - 1), '\033[94mWIN!\033[0m', '=' * (self.MAP_X_SIZE - 1))
                print(countMsg, timeMsg.rjust(DEFAULT_LENGTH_OF_LINE - len(countMsg) - 1))
                print('Last: \033[1m\033[36m({0}, {1})\033[0m'.format(self.pos.x, self.pos.y))
            case 'gameover' :
                print('=' * (self.MAP_X_SIZE - 3), '\033[90mGameOver\033[0m', '=' * (self.MAP_X_SIZE - 3))
                print(countMsg, timeMsg.rjust(DEFAULT_LENGTH_OF_LINE - len(countMsg) - 1))
                print('Last: \033[1m\033[36m({0}, {1})\033[0m'.format(self.pos.x, self.pos.y))
        
        if self.playCount == 0 :
            print('=' * (DEFAULT_LENGTH_OF_LINE - 18))
            print('Move     ', '\033[44m[←]\033[0m \033[44m[→]\033[0m \033[44m[↑]\033[0m \033[44m[↓]\033[0m'.rjust(DEFAULT_LENGTH_OF_LINE + 8))
            print('Open Tile', '\033[42m\033[30m[SpaceBar]\033[0m'.rjust(DEFAULT_LENGTH_OF_LINE - 14))
            print('Flag     ', '\033[43m\033[30m[F]\033[0m'.rjust(DEFAULT_LENGTH_OF_LINE - 14))
            print('Exit Game', '\033[101m\033[30m[Esc]\033[0m'.rjust(DEFAULT_LENGTH_OF_LINE - 13))

    def __movePoint(self, key) :
        match key :
            case 'left' :
                self.pos.moveXBy(-1)
            case 'right' :
                self.pos.moveXBy(1)
            case 'up' :
                self.pos.moveYBy(-1)
            case 'down' :
                self.pos.moveYBy(1)

        self.__didChangeBoard()

    def __setFlag(self) :
        self.__willChangeBoard()

        if self.view[self.pos.y - 1][self.pos.x - 1] != 1 :
            if self.view[self.pos.y - 1][self.pos.x - 1] == 2 :
                self.view[self.pos.y - 1][self.pos.x - 1] = 0
            else :
                self.view[self.pos.y - 1][self.pos.x - 1] = 2

        self.__didChangeBoard()


game = Game(60, 28, 336).startGame()
