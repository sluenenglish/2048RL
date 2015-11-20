import numpy as np
import itertools
import random
import os



class Board():

    def __init__(self, size):
        self.board = np.array([[0] * size for i in range(size)])
        self.score = 0
        self.size = size
        for i in range(2):
            self.board[random.randint(0, size-1),random.randint(0, size-1)] = 1

    def print_board(self):
        for row in self.board:
            print row

    def remove_blank_tile(self, row, pos):
        row[pos] = 0
        return np.concatenate((row[:pos], row[pos+1:], np.array([0])))

    def swipe_without_merge(self, row):
        for i in range(len(row)-1):
            while row[i] == 0 and any([j !=0 for j in row[i:]]):
                row = self.remove_blank_tile(row, i)
        return row

    def swipe_row(self, row):
        row = self.swipe_without_merge(row)
        for i in range(len(row)-1):
            if row[i] == row[i+1]  and row[i] != 0:
                row[i] += 1
                row = self.remove_blank_tile(row, i+1)
        return row

    def swipe_board_left(self):
        for i, row in enumerate(self.board):
            self.board[i,:] = self.swipe_row(row)

    def swipe_board(self, direction):
        self.board = np.rot90(self.board, direction)
        old_board = np.copy(self.board)
        self.swipe_board_left()
        if not np.array_equal(old_board, self.board) and (self.board == 0).sum() > 0:
            self.random_insert()
        self.board = np.rot90(self.board, 4-direction)

    def random_insert(self):
        possible_inserts = [(y,x) for (y, x) in itertools.combinations_with_replacement(range(self.size), 2) if self.board[y, x] == 0]
        self.board[random.choice(possible_inserts)] = 1

    def game_over(self):
        if (self.board  == 0).sum() > 0:
            return False
        for row in self.board:
            if any([row[i]==row[i+1] for i in range(self.size-1)]):
                    return False
        for row in np.rot90(self.board, 1):
            if any([row[i]==row[i+1] for i in range(self.size-1)]):
                    return False
        return True


class Game():

    def __init__(self, size):
        self.board = Board(size)

    def play(self):
        while not self.board.game_over():
            self.board.print_board()
            choice = raw_input('')
            os.system('clear')
            self.board.swipe_board(int(choice))
        self.board.print_board()
        print 'Game Over'

    def random_play(self):
        self.board.print_board()
        while not self.board.game_over():
            choice = random.randint(1,4)
            print 'Direction', {1:'Up', 2:'Right', 3:'Down', 4:'Left'}[choice]
            self.board.swipe_board(choice)
            self.board.print_board()
            print
        print 'Game Over'




if __name__ == '__main__':
    game = Game(4)
    game.random_play()
#

