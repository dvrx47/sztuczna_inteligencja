#!/usr/bin/env python3
import random

numberOfGames = 10
winTable = [ 0 for i in range(numberOfGames) ]
gameMap =     [ '..#*#..',
		'...#...',
		'.......',
		'.~~.~~.',
		'.~~.~~.',
		'.~~.~~.',
		'.......',
		'...#...',
		'..#*#..' ]
N = 2000
DEBUG = False

class Agent(object):
    def __init__(self, pets, target):
        self.mapChar = ['.', '#', '*']
        self.pets = pets
        invert = (1<<5)
        self.oponent_pets = list(map(lambda x : chr(ord(x)^invert), pets))
        self.hierarchy = {}
        self.hierarchy['r'] = 8
        self.hierarchy['c'] = 1
        self.hierarchy['d'] = 2
        self.hierarchy['w'] = 3
        self.hierarchy['j'] = 4
        self.hierarchy['t'] = 5
        self.hierarchy['l'] = 6
        self.hierarchy['e'] = 7
        self.target = target

    def confirmMove(self, m, board):
        f = m[0]
        y1, x1 = m[1]
        y2, x2 = m[2]
        r = list(board[y1])
        r[x1] = gameMap[y1][x1]
        board[y1] = ''.join(r)
        r = list(board[y2])
        r[x2] = f
        board[y2] = ''.join(r)
        return board, m[3]

    def makeMove(self, board):
        pass

class AgentEx3(Agent):
    def makeRatMove(self,y,x, board):
        yt, xt = self.target
        if y < yt:
            if board[y+1][x] in gameMap:
                return (board[y][x], (y,x), (y+1,x), 0)
            else:
                return (board[y][x], (y,x), (y+1,x), 1)
        elif y > yt:
            if board[y-1][x] in gameMap:
                return (board[y][x], (y,x), (y-1,x), 0)
            else:
                return (board[y][x], (y,x), (y-1,x), 1)


        if x < xt:
            if board[y][x+1] in gameMap:
                return (board[y][x], (y,x), (y,x+1), 0)
            else:
                return (board[y][x], (y,x), (y,x+1), 1)
        elif x > xt:
            if board[y][x-1] in gameMap:
                return (board[y][x], (y,x), (y,x-1), 0)
            else:
                return (board[y][x], (y,x), (y,x-1), 1)

    def makeMove(self, board):
        for y in range(9):
            for x in range(7):
                if board[y][x] in self.pets:
                    if board[y][x].lower() == 'r':
                        m = self.makeRatMove(y,x, board)
                        return self.confirmMove(m, board)

class AgentEx2(Agent):
    def canCapture(self, a, b):
        if self.hierarchy[a] >= self.hierarchy[b]:
            return True
        return False

    def getRatMoves(self, x,y,board):
        moves = []
        if x > 0:
            if board[y][x-1] in self.mapChar:
                if board[y][x-1] == '*':
                    if (y,x-1) == self.target:
                        moves.append((board[y][x],(y,x),(y,x-1),0))
                else:
                    moves.append((board[y][x],(y,x),(y,x-1),0))
            else:
                if board[y][x-1] in self.oponent_pets:
                    if board[y][x] == '~' and  board[y][x-1] == '.':
                        pass
                    elif self.canCapture('r', board[y][x-1].lower()):
                        moves.append(('r',(y,x),(y,x-1),1))

        if x < 6:
            if board[y][x+1] in self.mapChar:
                if board[y][x+1] == '*':
                    if (y,x+1) == self.target:
                        moves.append((board[y][x],(y,x),(y,x+1),0))
                else:
                    moves.append((board[y][x], (y,x), (y,x+1),0))
            else:
                if board[y][x+1] in self.oponent_pets:
                    if board[y][x] == '~' and  board[y][x+1] == '.':
                        pass
                    elif self.canCapture('r', board[y][x+1].lower()):
                        moves.append((board[y][x],(y,x),(y,x+1),1))

        if y > 0:
            if board[y-1][x] in self.mapChar:
                if board[y-1][x] == '*':
                    if (y-1,x) == self.target:
                        moves.append((board[y][x],(y,x),(y-1,x),0))
                else:
                    moves.append((board[y][x], (y,x), (y-1,x),0))
            else:
                if board[y-1][x] in self.oponent_pets:
                    if board[y][x] == '~' and  board[y-1][x] == '.':
                        pass
                    elif self.canCapture('r', board[y-1][x].lower()):
                        moves.append((board[y][x],(y,x),(y-1,x),1))

        if y < 8:
            if board[y+1][x] in self.mapChar:
                if board[y+1][x] == '*':
                    if (y+1,x) == self.target:
                        moves.append((board[y][x],(y,x),(y+1,x),0))
                else:
                    moves.append((board[y][x], (y,x), (y+1,x),0))
            else:
                if board[y+1][x] in self.oponent_pets:
                    if board[y][x] == '~' and  board[y+1][x] == '.':
                        pass
                    elif self.canCapture('r', board[y+1][x].lower()):
                        moves.append((board[y][x],(y,x),(y+1,x),1))

        return moves


    def getCatMoves(self, x, y,board):
        moves = []
        if x > 0:
            if board[y][x-1] in self.mapChar:
                if board[y][x-1] == '*':
                    if (y,x-1) == self.target:
                        moves.append((board[y][x], (y,x), (y,x-1), 0))
                elif board[y][x-1] != '~':
                    moves.append((board[y][x], (y,x), (y,x-1), 0))
            elif board[y][x-1] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y][x-1].lower()) or gameMap[y][x-1] == '#':
                    moves.append((board[y][x], (y,x), (y,x-1), 1))

        if x < 6:
            if board[y][x+1] in self.mapChar:
                if board[y][x+1] == '*':
                    if (y,x+1) == self.target:
                        moves.append((board[y][x], (y,x), (y,x+1), 0))
                elif board[y][x+1] != '~':
                    moves.append((board[y][x], (y,x), (y,x+1), 0))
            elif board[y][x+1] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y][x+1].lower()) or gameMap[y][x+1] == '#':
                    moves.append((board[y][x], (y,x), (y,x+1), 1))

        if y > 0:
            if board[y-1][x] in self.mapChar:
                if board[y-1][x] == '*':
                    if (y-1,x) == self.target:
                        moves.append((board[y][x], (y,x), (y-1,x), 0))
                elif board[y-1][x] != '~':
                    moves.append((board[y][x], (y,x), (y-1,x), 0))
            elif board[y-1][x] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y-1][x].lower()) or gameMap[y-1][x] == '#':
                    moves.append((board[y][x], (y,x), (y-1,x), 1))

        if y < 8:
            if board[y+1][x] in self.mapChar:
                if board[y+1][x] == '*':
                    if (y+1,x) == self.target:
                        moves.append((board[y][x], (y,x), (y+1,x), 0))
                elif board[y+1][x] != '~':
                    moves.append((board[y][x], (y,x), (y+1,x), 0))
            elif board[y+1][x] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y+1][x].lower()) or gameMap[y+1][x] == '#':
                    moves.append((board[y][x], (y,x), (y+1,x), 1))
        return moves

    def getDogMoves(self, x, y, board):
        moves = []
        if x > 0:
            if board[y][x-1] in self.mapChar:
                if board[y][x-1] == '*':
                    if (y,x-1) == self.target:
                        moves.append((board[y][x], (y,x), (y,x-1), 0))
                elif board[y][x-1] != '~':
                    moves.append((board[y][x], (y,x), (y,x-1), 0))
            elif board[y][x-1] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y][x-1].lower()) or gameMap[y][x-1] == '#':
                    moves.append((board[y][x], (y,x), (y,x-1), 1))

        if x < 6:
            if board[y][x+1] in self.mapChar:
                if board[y][x+1] == '*':
                    if (y,x+1) == self.target:
                        moves.append((board[y][x], (y,x), (y,x+1), 0))
                elif board[y][x+1] != '~':
                    moves.append((board[y][x], (y,x), (y,x+1), 0))
            elif board[y][x+1] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y][x+1].lower()) or gameMap[y][x+1] == '#':
                    moves.append((board[y][x], (y,x), (y,x+1), 1))

        if y > 0:
            if board[y-1][x] in self.mapChar:
                if board[y-1][x] == '*':
                    if (y-1,x) == self.target:
                        moves.append((board[y][x], (y,x), (y-1,x), 0))
                elif board[y-1][x] != '~':
                    moves.append((board[y][x], (y,x), (y-1,x), 0))
            elif board[y-1][x] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y-1][x].lower()) or gameMap[y-1][x] == '#':
                    moves.append((board[y][x], (y,x), (y-1,x), 1))

        if y < 8:
            if board[y+1][x] in self.mapChar:
                if board[y+1][x] == '*':
                    if (y+1,x) == self.target:
                        moves.append((board[y][x], (y,x), (y+1,x), 0))
                elif board[y+1][x] != '~':
                    moves.append((board[y][x], (y,x), (y+1,x), 0))
            elif board[y+1][x] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y+1][x].lower()) or gameMap[y+1][x] == '#':
                    moves.append((board[y][x], (y,x), (y+1,x), 1))
        return moves

    def getWolfMoves(self, x, y, board):
        moves = []
        if x > 0:
            if board[y][x-1] in self.mapChar:
                if board[y][x-1] == '*':
                    if (y,x-1) == self.target:
                        moves.append((board[y][x], (y,x), (y,x-1), 0))
                elif board[y][x-1] != '~':
                    moves.append((board[y][x], (y,x), (y,x-1), 0))
            elif board[y][x-1] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y][x-1].lower()) or gameMap[y][x-1] == '#':
                    moves.append((board[y][x], (y,x), (y,x-1), 1))

        if x < 6:
            if board[y][x+1] in self.mapChar:
                if board[y][x+1] == '*':
                    if (y,x+1) == self.target:
                        moves.append((board[y][x], (y,x), (y,x+1), 0))
                elif board[y][x+1] != '~':
                    moves.append((board[y][x], (y,x), (y,x+1), 0))
            elif board[y][x+1] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y][x+1].lower()) or gameMap[y][x+1] == '#':
                    moves.append((board[y][x], (y,x), (y,x+1), 1))

        if y > 0:
            if board[y-1][x] in self.mapChar:
                if board[y-1][x] == '*':
                    if (y-1,x) == self.target:
                        moves.append((board[y][x], (y,x), (y-1,x), 0))
                elif board[y-1][x] != '~':
                    moves.append((board[y][x], (y,x), (y-1,x), 0))
            elif board[y-1][x] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y-1][x].lower()) or gameMap[y-1][x] == '#':
                    moves.append((board[y][x], (y,x), (y-1,x), 1))

        if y < 8:
            if board[y+1][x] in self.mapChar:
                if board[y+1][x] == '*':
                    if (y+1,x) == self.target:
                        moves.append((board[y][x], (y,x), (y+1,x), 0))
                elif board[y+1][x] != '~':
                    moves.append((board[y][x], (y,x), (y+1,x), 0))
            elif board[y+1][x] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y+1][x].lower()) or gameMap[y+1][x] == '#':
                    moves.append((board[y][x], (y,x), (y+1,x), 1))
        return moves

    def getPantheraMoves(self, x, y, board):
        moves = []
        if x > 0:
            if board[y][x-1] in self.mapChar:
                if board[y][x-1] == '*':
                    if (y,x-1) == self.target:
                        moves.append((board[y][x], (y,x), (y,x-1), 0))
                elif board[y][x-1] != '~':
                    moves.append((board[y][x], (y,x), (y,x-1), 0))
            elif board[y][x-1] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y][x-1].lower()) or gameMap[y][x-1] == '#':
                    moves.append((board[y][x], (y,x), (y,x-1), 1))

        if x < 6:
            if board[y][x+1] in self.mapChar:
                if board[y][x+1] == '*':
                    if (y,x+1) == self.target:
                        moves.append((board[y][x], (y,x), (y,x+1), 0))
                elif board[y][x+1] != '~':
                    moves.append((board[y][x], (y,x), (y,x+1), 0))
            elif board[y][x+1] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y][x+1].lower()) or gameMap[y][x+1] == '#':
                    moves.append((board[y][x], (y,x), (y,x+1), 1))

        if y > 0:
            if board[y-1][x] in self.mapChar:
                if board[y-1][x] == '*':
                    if (y-1,x) == self.target:
                        moves.append((board[y][x], (y,x), (y-1,x), 0))
                elif board[y-1][x] != '~':
                    moves.append((board[y][x], (y,x), (y-1,x), 0))
            elif board[y-1][x] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y-1][x].lower()) or gameMap[y-1][x] == '#':
                    moves.append((board[y][x], (y,x), (y-1,x), 1))

        if y < 8:
            if board[y+1][x] in self.mapChar:
                if board[y+1][x] == '*':
                    if (y+1,x) == self.target:
                        moves.append((board[y][x], (y,x), (y+1,x), 0))
                elif board[y+1][x] != '~':
                    moves.append((board[y][x], (y,x), (y+1,x), 0))
            elif board[y+1][x] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y+1][x].lower()) or gameMap[y+1][x] == '#':
                    moves.append((board[y][x], (y,x), (y+1,x), 1))
        return moves

    def getTigerMoves(self, x, y, board):
        moves = []
        if x > 0:
            if board[y][x-1] in self.mapChar:
                if board[y][x-1] == '*':
                    if (y,x-1) == self.target:
                        moves.append((board[y][x], (y,x), (y,x-1), 0))
                elif board[y][x-1] != '~':
                    moves.append((board[y][x], (y,x), (y,x-1), 0))
                else:
                    if board[y][x-2] == '~':
                        if board[y][x-3] in self.mapChar:
                            moves.append((board[y][x], (y,x), (y,x-3), 0))
                        elif board[y][x-3] in self.oponent_pets:
                            if self.canCapture(board[y][x].lower(), board[y][x-3].lower()):
                                moves.append((board[y][x], (y,x), (y,x-3), 1))
            elif board[y][x-1] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y][x-1].lower()) or gameMap[y][x-1] == '#':
                    moves.append((board[y][x], (y,x), (y,x-1), 1))

        if x < 6:
            if board[y][x+1] in self.mapChar:
                if board[y][x+1] == '*':
                    if (y,x+1) == self.target:
                        moves.append((board[y][x], (y,x), (y,x+1), 0))
                elif board[y][x+1] != '~':
                    moves.append((board[y][x], (y,x), (y,x+1), 0))
                else:
                    if board[y][x+2] == '~':
                        if board[y][x+3] in self.mapChar:
                            moves.append((board[y][x], (y,x), (y,x+3), 0))
                        elif board[y][x+3] in self.oponent_pets:
                            if self.canCapture(board[y][x].lower(), board[y][x+3].lower()):
                                moves.append((board[y][x], (y,x), (y,x+3), 1))
            elif board[y][x+1] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y][x+1].lower()) or gameMap[y][x+1] == '#':
                    moves.append((board[y][x], (y,x), (y,x+1), 1))


        if y > 0:
            if board[y-1][x] in self.mapChar:
                if board[y-1][x] == '*':
                    if (y-1,x) == self.target:
                        moves.append((board[y][x], (y,x), (y-1,x), 0))
                elif board[y-1][x] != '~':
                    moves.append((board[y][x], (y,x), (y-1,x), 0))
                else:
                    if board[y-2][x] == '~' and board[y-3][x] == '~':
                        if board[y-4][x] in self.mapChar:
                            moves.append((board[y][x], (y,x), (y-4,x), 0))
                        elif board[y-4][x] in self.oponent_pets:
                            if self.canCapture(board[y][x].lower(), board[y-4][x].lower()):
                                moves.append((board[y][x], (y,x), (y-4,x), 1))
            elif board[y-1][x] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y-1][x].lower()) or gameMap[y-1][x] == '#':
                    moves.append((board[y][x], (y,x), (y-1,x), 1))

        if y < 8:
            if board[y+1][x] in self.mapChar:
                if board[y+1][x] == '*':
                    if (y+1,x) == self.target:
                        moves.append((board[y][x], (y,x), (y+1,x), 0))
                elif board[y+1][x] != '~':
                    moves.append((board[y][x], (y,x), (y+1,x), 0))
                else:
                     if board[y+2][x] == '~' and board[y+3][x] == '~':
                        if board[y+4][x] in self.mapChar:
                            moves.append((board[y][x], (y,x), (y+4,x), 0))
                        elif board[y+4][x] in self.oponent_pets:
                            if self.canCapture(board[y][x].lower(), board[y+4][x].lower()):
                                moves.append((board[y][x], (y,x), (y+4,x), 1))
            elif board[y+1][x] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y+1][x].lower()) or gameMap[y+1][x] == '#':
                    moves.append((board[y][x], (y,x), (y+1,x), 1))
        return moves

    def getLionMoves(self, x, y, board):
        moves = []
        if x > 0:
            if board[y][x-1] in self.mapChar:
                if board[y][x-1] == '*':
                    if (y,x-1) == self.target:
                        moves.append((board[y][x], (y,x), (y,x-1), 0))
                elif board[y][x-1] != '~':
                    moves.append((board[y][x], (y,x), (y,x-1), 0))
                else:
                    if board[y][x-2] == '~':
                        if board[y][x-3] in self.mapChar:
                            moves.append((board[y][x], (y,x), (y,x-3), 0))
                        elif board[y][x-3] in self.oponent_pets:
                            if self.canCapture(board[y][x].lower(), board[y][x-3].lower()):
                                moves.append((board[y][x], (y,x), (y,x-3), 1))
            elif board[y][x-1] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y][x-1].lower()) or gameMap[y][x-1] == '#':
                    moves.append((board[y][x], (y,x), (y,x-1), 1))

        if x < 6:
            if board[y][x+1] in self.mapChar:
                if board[y][x+1] == '*':
                    if (y,x+1) == self.target:
                        moves.append((board[y][x], (y,x), (y,x+1), 0))
                elif board[y][x+1] != '~':
                    moves.append((board[y][x], (y,x), (y,x+1), 0))
                else:
                    if board[y][x+2] == '~':
                        if board[y][x+3] in self.mapChar:
                            moves.append((board[y][x], (y,x), (y,x+3), 0))
                        elif board[y][x+3] in self.oponent_pets:
                            if self.canCapture(board[y][x].lower(), board[y][x+3].lower()):
                                moves.append((board[y][x], (y,x), (y,x+3), 1))
            elif board[y][x+1] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y][x+1].lower()) or gameMap[y][x+1] == '#':
                    moves.append((board[y][x], (y,x), (y,x+1), 1))


        if y > 0:
            if board[y-1][x] in self.mapChar:
                if board[y-1][x] == '*':
                    if (y-1,x) == self.target:
                        moves.append((board[y][x], (y,x), (y-1,x), 0))
                elif board[y-1][x] != '~':
                    moves.append((board[y][x], (y,x), (y-1,x), 0))
                else:
                    if board[y-2][x] == '~' and board[y-3][x] == '~':
                        if board[y-4][x] in self.mapChar:
                            moves.append((board[y][x], (y,x), (y-4,x), 0))
                        elif board[y-4][x] in self.oponent_pets:
                            if self.canCapture(board[y][x].lower(), board[y-4][x].lower()):
                                moves.append((board[y][x], (y,x), (y-4,x), 1))
            elif board[y-1][x] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y-1][x].lower()) or gameMap[y-1][x] == '#':
                    moves.append((board[y][x], (y,x), (y-1,x), 1))

        if y < 8:
            if board[y+1][x] in self.mapChar:
                if board[y+1][x] == '*':
                    if (y+1,x) == self.target:
                        moves.append((board[y][x], (y,x), (y+1,x), 0))
                elif board[y+1][x] != '~':
                    moves.append((board[y][x], (y,x), (y+1,x), 0))
                else:
                     if board[y+2][x] == '~' and board[y+3][x] == '~':
                        if board[y+4][x] in self.mapChar:
                            moves.append((board[y][x], (y,x), (y+4,x), 0))
                        elif board[y+4][x] in self.oponent_pets:
                            if self.canCapture(board[y][x].lower(), board[y+4][x].lower()):
                                moves.append((board[y][x], (y,x), (y+4,x), 1))
            elif board[y+1][x] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y+1][x].lower()) or gameMap[y+1][x] == '#':
                    moves.append((board[y][x], (y,x), (y+1,x), 1))
        return moves

    def getElephantMoves(self, x, y, board):
        moves = []
        if x > 0:
            if board[y][x-1] in self.mapChar:
                if board[y][x-1] == '*':
                    if (y,x-1) == self.target:
                        moves.append((board[y][x], (y,x), (y,x-1), 0))
                elif board[y][x-1] != '~':
                    moves.append((board[y][x], (y,x), (y,x-1), 0))
            elif board[y][x-1] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y][x-1].lower()) or gameMap[y][x-1] == '#':
                    moves.append((board[y][x], (y,x), (y,x-1), 1))

        if x < 6:
            if board[y][x+1] in self.mapChar:
                if board[y][x+1] == '*':
                    if (y,x+1) == self.target:
                        moves.append((board[y][x], (y,x), (y,x+1), 0))
                elif board[y][x+1] != '~':
                    moves.append((board[y][x], (y,x), (y,x+1), 0))
            elif board[y][x+1] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y][x+1].lower()) or gameMap[y][x+1] == '#':
                    moves.append((board[y][x], (y,x), (y,x+1), 1))

        if y > 0:
            if board[y-1][x] in self.mapChar:
                if board[y-1][x] == '*':
                    if (y-1,x) == self.target:
                        moves.append((board[y][x], (y,x), (y-1,x), 0))
                elif board[y-1][x] != '~':
                    moves.append((board[y][x], (y,x), (y-1,x), 0))
            elif board[y-1][x] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y-1][x].lower()) or gameMap[y-1][x] == '#':
                    moves.append((board[y][x], (y,x), (y-1,x), 1))

        if y < 8:
            if board[y+1][x] in self.mapChar:
                if board[y+1][x] == '*':
                    if (y+1,x) == self.target:
                        moves.append((board[y][x], (y,x), (y+1,x), 0))
                elif board[y+1][x] != '~':
                    moves.append((board[y][x], (y,x), (y+1,x), 0))
            elif board[y+1][x] in self.oponent_pets:
                if self.canCapture(board[y][x].lower(), board[y+1][x].lower()) or gameMap[y+1][x] == '#':
                    moves.append((board[y][x], (y,x), (y+1,x), 1))
        return moves

    def getFigureMoves(self, x, y, board):
        if board[y][x].lower() == 'r':
            return self.getRatMoves(x,y,board)
        elif board[y][x].lower() == 'c':
            return self.getCatMoves(x,y,board)
        elif board[y][x].lower() == 'd':
            return self.getDogMoves(x,y,board)
        elif board[y][x].lower() == 'w':
            return self.getWolfMoves(x,y,board)
        elif board[y][x].lower() == 'j':
            return self.getPantheraMoves(x,y,board)
        elif board[y][x].lower() == 't':
            return self.getTigerMoves(x,y,board)
        elif board[y][x].lower() == 'l':
            return self.getLionMoves(x,y,board)
        elif board[y][x].lower() == 'e':
            return self.getElephantMoves(x,y,board)


    def genMoves(self, board):
        moves = []
        for i in range(9):
            for j in range(7):
                if board[i][j] in self.pets:
                    current_moves = self.getFigureMoves(j,i,board)
                    moves += current_moves
        return moves

    def swapData(self):
        self.pets, self.oponent_pets = self.oponent_pets, self.pets
        if self.target[0] == 0:
            self.target = (8,3)
        else:
            self.target = (0,3)

    def computeFactor(self, board):
        oponent_points = 1
        my_points = 1
        for y in range(9):
            for x in range(7):
                if board[y][x] in self.pets:
                    my_points += self.hierarchy[board[y][x].lower()]
                elif board[y][x] in self.oponent_pets:
                    oponent_points += self.hierarchy[board[y][x].lower()]
        y1, x1 = self.target
        if board[y1][x1] != '*':
            my_points += 100

        if y1 == 0:
            y1 = 8
        else:
            y1 = 0

        if board[y1][x1] != '*':
            oponent_points += 100

        return my_points/oponent_points

    def getBestIndex(self, boards):
        bestIndex = -1
        bestVal = -1
        for i in range(len(boards)):
            factor = self.computeFactor(boards[i])
            if factor > bestVal:
                bestIndex = i
                bestVal = factor
        return bestIndex

    def makeOponentRandomMove(self, b):
        self.swapData()
        moves = self.genMoves(b)
        if moves:
            self.confirmMove(random.choice(moves), b)
        self.swapData()

    def makeRandomMove(self, b):
        moves = self.genMoves(b)
        if moves:
            self.confirmMove(random.choice(moves), b)

    def randomGames(self, board, moves):
        boards = []
        for m in moves:
            b, _ = self.confirmMove(m, list(board))
            boards.append(b)
        for turn in range(N):
            index = random.randrange(0, len(boards))
            self.makeOponentRandomMove(boards[index])
            self.makeRandomMove(boards[index])
        return moves[self.getBestIndex(boards)]

    def makeMove(self, board):
        moves = self.genMoves(board)
        m = self.randomGames(board, moves)
        return self.confirmMove(m, board)


class Game(object):
        def __init__(self, player0, player1, gameId = 0, debug=False):

                self.board =  [ 'L.#*#.T',
                                '.D.#.C.',
                                'R.J.W.E',
                                '.~~.~~.',
                                '.~~.~~.',
                                '.~~.~~.',
                                'e.w.j.r',
                                '.d.#.c.',
                                't.#*#.l' ]

                self.player0 = player0(['R', 'C', 'D', 'W', 'J', 'T', 'L', 'E'], (8,3))
                self.player1 = player1(['r', 'c', 'd', 'w', 'j', 't', 'l', 'e'], (0,3))
                self.movesWithoutCapture = 0
                self.gameId = gameId
                self.debug = debug

        def isEnd(self):
            if self.movesWithoutCapture >= 50 :
                return True

            if self.board[0][3] != '*':
                return True

            if self.board[8][3] != '*':
                return True
            return False

        def winnerExtraRules(self):
            return 0

        def getWinner(self):
            if self.board[0][3] != '*':
                return 1

            if self.board[8][3] != '*':
                return 0

            return self.winnerExtraRules()

        def fillWinTable(self):
            winner = self.getWinner()
            winTable[self.gameId] = winner

        def printBoard(self):
            for r in self.board:
                print(r)
            input()

        def runGame(self):
            while not self.isEnd():
                self.board, capture = self.player0.makeMove(self.board)
                self.debug and print('player0')
                self.debug and self.printBoard()
                if capture :
                    self.movesWithoutCapture = 0
                else:
                    self.movesWithoutCapture += 1

                if self.isEnd():
                    break

                self.board, capture = self.player1.makeMove(self.board)
                self.debug and print('player1')
                self.debug and self.printBoard()
                if capture :
                    self.movesWithoutCapture = 0
                else:
                    self.movesWithoutCapture += 1
            self.fillWinTable()

for i in range(numberOfGames):
    game = Game(AgentEx2, AgentEx3, i, DEBUG)
    game.runGame()
print(sum(winTable))
