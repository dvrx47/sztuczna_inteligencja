#!/usr/bin/env python3


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

class Agent(object):
    def __init__(self, pets):
        self.pets = pets

    def makeMove(self, board):
        pass


class AgentEx2(Agent):
    def makeMove(self, board):
        return board, 0


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

                self.player0 = player0(['R', 'C', 'D', 'W', 'J', 'T', 'L', 'E'])
                self.player1 = player1(['r', 'c', 'd', 'w', 'j', 't', 'l', 'e'])
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
            return 1

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
                self.debug and self.printBoard()
                if capture :
                    self.movesWithoutCapture = 0
                else:
                    self.movesWithoutCapture += 1

                if self.isEnd():
                    break

                self.board, capture = self.player1.makeMove(self.board)
                self.debug and self.printBoard()
                if capture :
                    self.movesWithoutCapture = 0
                else:
                    self.movesWithoutCapture += 1
            self.fillWinTable()


game = Game(AgentEx2, AgentEx2, 0, True)
game.runGame()
