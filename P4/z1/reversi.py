#!/usr/bin/env python
import random
import sys
from collections import defaultdict as dd
import copy


M = 8
GAMES = 1000
DEBUG = 0
# AGENT: '1' means '#'
AGENT_NR = 1

#####################################################

def initial_board():
    B = [ [None] * M for i in range(M)]
    B[3][3] = 1
    B[4][4] = 1
    B[3][4] = 0
    B[4][3] = 0
    return B


class Board:
    dirs  = [ (0,1), (1,0), (-1,0), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1) ]


    def __init__(self):
        self.board = initial_board()
        self.fields = set()
        self.move_list = []
        self.history = []
        for i in range(M):
            for j in range(M):
                if self.board[i][j] == None:
                    self.fields.add( (j,i) )

    def draw(self):
        for i in range(M):
            res = []
            for j in range(M):
                b = self.board[i][j]
                if b == None:
                    res.append('.')
                elif b == 1:
                    res.append('#')
                else:
                    res.append('o')
            print ''.join(res)
        print


    def moves(self, player):
        res = []
        for (x,y) in self.fields:
            if any( self.can_beat(x,y, direction, player) for direction in Board.dirs):
                res.append( (x,y) )
        if not res:
            return [None]
        return res


    def can_beat(self, x, y, d, player):
        dx,dy = d
        x += dx
        y += dy
        cnt = 0
        while self.get(x,y) == 1-player:
            x += dx
            y += dy
            cnt += 1
        return cnt > 0 and self.get(x,y) == player

    def get(self, x,y):
        if 0 <= x < M and 0 <=y < M:
            return self.board[y][x]
        return None

    def do_move(self, move, player):
        self.history.append([x[:] for x in self.board])
        self.move_list.append(move)

        if move == None:
            return
        x,y = move
        x0,y0 = move
        self.board[y][x] = player
        self.fields -= set([move])
        for dx,dy in self.dirs:
            x,y = x0,y0
            to_beat = []
            x += dx
            y += dy
            while self.get(x,y) == 1-player:
              to_beat.append( (x,y) )
              x += dx
              y += dy
            if self.get(x,y) == player:
                for (nx,ny) in to_beat:
                    self.board[ny][nx] = player

    def result(self):
        res = 0
        for y in range(M):
            for x in range(M):
                b = self.board[y][x]
                if b == 0:
                    res -= 1
                elif b == 1:
                    res += 1
        return res

    def terminal(self):
        if not self.fields:
            return True
        if len(self.move_list) < 2:
            return False
        return self.move_list[-1] == self.move_list[-2] == None

    def random_move(self, player):
        ms = self.moves(player)
        if ms:
            return random.choice(ms)
        return None


##############################################
def get_game_phase(board):
    if len(board.fields) > 40:
        return 0
    if len(board.fields) > 30:
        return 1
    return 2

def random_choice(moves, board, player):
    return random.choice(moves)


def get_field_weight(move):
    x, y = move
    weights = [ [3,0,2,0,0,2,0,3],
                [0,0,2,0,0,2,0,0],
                [2,2,2,0,0,2,2,2],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [2,2,2,0,0,2,2,2],
                [0,0,2,0,0,2,0,0],
                [3,0,2,0,0,2,0,3] ]

    return weights[x][y]


def weight_move(moves, board, player):
    best_move = [None]
    best_val = -200
    for m in moves:
        mval = get_field_weight(m)
        if mval > best_val:
            best_val = mval
            best_move = m
    return best_move


ai_func = [weight_move, weight_move, weight_move]
def agent_move(board, player):
    game_phase = get_game_phase(board)
    moves = board.moves(player)
    if moves and moves != [None]:
        return ai_func[game_phase](moves, board,player)
    return None


##############################################

def random_agent_move(board, player):
    m = board.random_move(player)
    board.do_move(m, player)


random_agent = 0
my_agent = 0

for g in range(GAMES):
    player = 0
    B = Board()

    while True:
        DEBUG and B.draw()
        if player == AGENT_NR:
            #my agent
            m = agent_move(B, player)
            B.do_move(m, player)
        else:
            random_agent_move(B, player)
        player = 1-player
        DEBUG and raw_input()
        if B.terminal():
            break

    if B.result() > 0:
        my_agent += 1
    elif B.result() < 0:
        random_agent += 1

DEBUG and B.draw()

print 'my agent', str(my_agent) + ':' + str(random_agent), 'random agent'

sys.exit(0)
