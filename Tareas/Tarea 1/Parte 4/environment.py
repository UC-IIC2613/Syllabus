import sys
import copy

class Environment:
    def __init__(self, filename, obs=False):
        # inicializa la clase, leyendo el mundo desde filename
        file  = open(filename, 'r')
        lines = file.readlines()
        dimensions = [int(x) for x in lines[0].split(',')]
        self.size_x = dimensions[0] #filas
        self.size_y = dimensions[1] #columnas
        self.__map = []
        self.__num_pits = 0
        self.__num_wumpus = 0
        self.shots = 0
        self.__visited = set()
        for x in range(0, self.size_x):
            self.__map.append(['']*self.size_y)
        for x in range(0, self.size_x):
            for y in range(0, self.size_y):
                c = lines[1+x][y]
                self.__map[x][y] = c
                if c == '@':
                    self.__num_pits += 1
                if c == 'W':
                    self.__num_wumpus += 1
                if c == 'I':
                    self.__map[x][y] = '.'
                    self.init_x = x
                    self.init_y = y
        self.__num_wumpus_initial = self.__num_wumpus
        self.agent_x = self.init_x
        self.agent_y = self.init_y
        self.frontier = set()
        self.visited  = set()
        self.observable = obs

    def is_observable(self):  # retorna si es que es posible observar el número de pozos
        return self.observable
    
    def get_num_pits(self):
        if self.observable:
            return self.__num_pits
        else:
            return None
    
    def get_num_wumpus(self):
        if self.observable:
            return self.__num_wumpus
        else:
            return None
        
    def show_map(self):
        map = copy.deepcopy(self.__map)
        map[self.agent_x][self.agent_y] = 'A'
        for m in map:
            print(m)

    def in_grid(self, x, y):
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    def get_size_x(self):
        # retorna el tamaño de x
        return self.size_x

    def get_size_y(self):
        # retorna el tamaño de y
        return self.size_y

    def get_visited(self):
        return self.visited

    def is_neighbor(self, x1, y1, x2, y2):
        return self.in_grid(x1,y1) and self.in_grid(x2,y2) and abs(x1-x2)+ abs(y1-y2) == 1

    def neighbors(self, x, y):
        n = []
        for nx in range(x-1, x+2):
            for ny in range(y-1, y+2):
                if self.is_neighbor(x, y, nx, ny) and self.in_grid(nx, ny):
                    n.append((nx, ny))
        return n

    def execute(self, action):
        if action[0] == 'goto':
            _, x, y = action
            self.agent_x = x
            self.agent_y = y
            self.visited.add((x,y))
            current_state = self.__map[x][y]
            if current_state == 'W' or current_state == '@':
                return 'dead'
            elif current_state == 'G':
                return 'gold'

        if action[0] == 'shoot':
            _, x, y = action
            self.shots += 1
            if self.shots > self.__num_wumpus_initial:
                return 'illegal_shooting'
            if self.__map[x][y] == 'W':
                print('AAAAHHH!')
                self.__map[x][y] = '.'
                self.__num_wumpus -= 1
        return ''

    def get_perceptions(self):        
        perception = set()
        for (x, y) in self.visited: 
            for (nx, ny) in self.neighbors(x, y):
                if self.__map[nx][ny] == 'W':
                    perception.add('sense_stench({},{})'.format(x, y))
                if self.__map[nx][ny] == '@':
                    perception.add('sense_breeze({},{})'.format(x, y))
        return list(perception)