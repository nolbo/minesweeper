import random

ground = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
viewPoint = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

def printGround() :
    rowNum = '  '
    for i in range(16) :
        rowNum += chr(9312 + i) + ' '
    print(rowNum)

    for i in range(16) :
        r = chr(9312 + i) + ' '
        for j in range(16) :
            match viewPoint[i][j] :
                case 0 :
                    r += '■'    
                case 1 :
                    r += '□' if ground[i][j] == 0 else ('★' if ground[i][j] == 'm' else str(ground[i][j]))
                case 2 :
                    r += '▶'
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
        if (i[0] > 15 or i[0] < 0) or (i[1] > 15 or i[1] < 0) :
            continue
        if i in check :
            continue
        openBlankTile(i[1], i[0], check)

def openAllTile() :
    _i = 0
    for i in viewPoint :
        _j = 0
        for j in i :
            viewPoint[_i][_j] = 1
            _j += 1
        _i += 1

def isGameEnded() :
    for i in range(16) :
        for j in range(16) :
            match viewPoint[i][j] :
                case 0 :
                    return False
                case 2 :
                    if ground[i][j] != 'm' :
                        return False
    
    return True

def createGround(startX, startY, _count_mine = 40) :
    count_mine = _count_mine

    while count_mine > 0 :
        [y, x] = [random.randrange(0, 16), random.randrange(0, 16)]
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

                for i in range(y - 1 if y > 0 else 0, y + 2 if y < 15 else 16) : # y축
                    for j in range(x - 1 if x > 0 else 0, x + 2 if x < 15 else 16) : # x축
                        if ground[i][j] == 'm' or (startX == j and startY == i) :
                            continue
                        ground[i][j] += 1
                count_mine -= 1

playCount = 0
while True :
    #try :
        pos = input().split(' ')
        pos[0] = int(pos[0])
        pos[1] = int(pos[1])

        if (pos[0] > 16 or pos[0] < 0) or (pos[1] > 16 or pos[1] < 0) :
            print('1~16 사이의 정수만 인정')
            continue
        playCount += 1
        if playCount == 1 :
            createGround(pos[1] - 1, pos[0] - 1)
        
        if len(pos) == 3 and (pos[2] == 'f' or pos[2] == 'F') :
            if viewPoint[pos[1] - 1][pos[0] - 1] != 1 :
                if viewPoint[pos[1] - 1][pos[0] - 1] == 2 :
                    viewPoint[pos[1] - 1][pos[0] - 1] = 0
                else :
                    viewPoint[pos[1] - 1][pos[0] - 1] = 2
        else :
            if viewPoint[pos[1] - 1][pos[0] - 1] == 2 :
                continue

            match ground[pos[1] - 1][pos[0] - 1] :
                case 'm' :
                    openAllTile()
                    printGround()
                    print('Game Over')
                    break
                case 0 :
                    openBlankTile(pos[0] - 1, pos[1] - 1)
                case _ :
                    viewPoint[pos[1] - 1][pos[0] - 1] = 1
                    if viewPoint[pos[1] - 1][pos[0] - 1] == 2 :
                        viewPoint[pos[1] - 1][pos[0] - 1] = 0

        printGround()
        if isGameEnded() == True :
            print('Win!')
            break
    #except :
        #print('invalid command')
    
