from cell import Cell
from termcolor import colored
import colorama


colorama.init()

class Map:
    def __init__(self, filename='map.txt'):
        file = open(filename, 'r')
        lines = file.readlines()
        dimensions = [int(x) for x in lines[0].split(',')]
        self.size_x = dimensions[0]
        self.size_y = dimensions[1]
        self.map = []
        for x in range(0, self.size_x):
            self.map.append([False]*self.size_y)
        for y in range(0, self.size_y):
            for x in range(0, self.size_x):
                c = lines[1+y][x]
                if c == '.':
                    self.map[x][y] = True
                elif c == '@':
                    self.map[x][y] = False
                elif c == 'I':
                    self.map[x][y] = True
                    self.init_x = x
                    self.init_y = y
                elif c == 'G':
                    self.map[x][y] = True
                    self.goal_x = x
                    self.goal_y = y

    def inside(self, x, y):
        return x >= 0 and x < self.size_x and \
               y >= 0 and y < self.size_y

    def free(self, x, y):
        return self.map[x][y]

    def obstacle(self, x, y):
        return not self.map[x][y]

    def draw_solution(self, trace, generated_positions=[], open_positions=[]):
        for y in range(0, self.size_y):
            for x in range(0, self.size_x):
                if x == self.init_x and y == self.init_y:
                    print('I', end='')
                elif x == self.goal_x and y == self.goal_y:
                    print('G', end='')
                elif Cell(x, y, self) in trace:
                    print(colored('*', 'green'), end='')
                elif (x, y) in generated_positions:
                    print(colored('X', 'red'), end='')
                elif (x, y) in open_positions:
                    print(colored('o', 'yellow'), end='')
                elif self.map[x][y] == True:
                    print('.', end='')
                elif self.map[x][y] == False:
                    print(colored('@', 'cyan'), end='')
            print('')
