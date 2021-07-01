import sys
import random
import copy


class Puzzle:
    goal15 = list(range(16))  # objetivo del 15-puzzle
    goal8 = list(range(9))    # objetivo del 8-puzzle
    MaxPDB = 5
    pdb = []           ## en mí código, yo usé estas líneas, si te hacen sentido, úsalas
    pdb_pattern = []   # si no te hacen sentido, haz lo que tú quieras
    pdbs_heuristics = []
    for i in range(MaxPDB):
        pdb.append({})
        #pdb_pattern.append(None)

    def __init__(self, board=None, blank=-1):
        if not board:
            self.x = 3
            self.size = 9
            self.board = [i for i in range(0, self.size)]
            self.blank = 0
        else:
            self.board = board
            if len(self.board) == 9:
                self.x = 3
                self.size = 9
            elif len(self.board) == 16:
                self.x = 4
                self.size = 16
            else:
                print('puzzle size not supported')
                sys.exit(1)
            if blank == -1:
                self.blank = board.index(0)

    def initialize_pdb(nro):
        """Cargamos la base de datos pdb """
        pdb = open(f'pdb{nro}.txt', 'r')
        pattern = pdb.readline().strip("\n")
        Puzzle.pdb_pattern.append(pattern) #guardamos el pattern
        for i in range(len(Puzzle.pdb)):
            if Puzzle.pdb[i] == {}: #si diccionario esta vacio
                for line in pdb: # guardamos cada problema relajado con su
                    # heuristica
                    line_1 = line.strip("\n")
                    line_2 = line_1.split(" ") #convertimos en lista
                    h = int(line_2[-1]) #sacamos la profundidad
                    l = line_2[:-1]
                    sub_problema  =" ".join(l)#guardamos en formato para que
                    # se mas facil buscarlo
                    Puzzle.pdb[i][sub_problema] = h
        pdb.close()

    def pdb_heuristic(self, id):
        """Retorna la máx heuristica """
        dict_base = Puzzle.pdb[id-1] #obtenemos la base del id querido
        pattern = Puzzle.pdb_pattern[id-1].split(" ") #obtenemos el pattern
        estado_relajado = []
        for i, tile in enumerate(self.board):
            if (str(tile) not in pattern) and not(str(tile) == "0"):
                estado_relajado.append(-1)
            else:
                estado_relajado.append(tile)
        board = [str(tile) for tile in estado_relajado]
        estado_actual = " ".join(board)  # relajado
        h = dict_base[estado_actual]
        h_manhattan = self.manhattan()
        heuristic = max(h, h_manhattan)

        return heuristic

    def pdb_1(self):
        return self.pdb_heuristic(1)

    def pdb_2(self):
        return self.pdb_heuristic(2)

    def pdb_3(self):
        return self.pdb_heuristic(3)

    ## acá, agrega más llamados si lo deseas!

    def pdb_best(self):
        return max([self.pdb_heuristic(1), self.pdb_heuristic(2),
                    self.pdb_heuristic(3)])
        ## esta es la mejor combinación que encontraste!

    def __hash__(self):
        return hash(tuple(self.board))

    def __eq__(self, other):
        return self.board == other.board

    def __repr__(self):
        def tostr(d):
            if d > 0:
                return "%2d" % (d)
            else:
                return "  "

        s = '\n'
        for i in range(0, self.x):
            s += "|"
            s += "|".join([tostr(d) for d in self.board[i*self.x:i*self.x+self.x]])
            s += "|\n"
        return s

    def zero_heuristic(self):
        return 0

    def incorrect_tiles(self):
        '''
            retorna el numero de piezas que no estan en la posicion correcta
        '''
        num = 0
        for i in range(0, self.size):
            if self.board[i] == 0:
                continue
            else:
                if self.board[i] != i:
                    num += 1
        return num

    def manhattan(self):
        '''
            retorna la suma de distancias manhattan de cada pieza a su
            posicion final
        '''
        num = 0
        for i in range(0, self.size):
            if self.board[i] == 0:
                continue
            else:
                num += abs(i % self.x - self.board[i] % self.x)
                num += abs(i // self.x - self.board[i] // self.x)
        return num

    def successors(self):
        '''
            Crea una lista de tuplas de la forma (estado, accion, costo)
            donde estado es el estado sucesor de self que se genera al ejecutar
            accion (un string) y costo (un numero real) es el costo de accion
        '''
        def create_child(newblank):
            child = copy.deepcopy(self)
            child.blank = newblank
            child.board[child.blank] = 0
            child.board[self.blank] = self.board[newblank]
            return child

        succ = []
        if self.blank > self.x - 1:
            c = create_child(self.blank-self.x)
            succ.append((c, 'up', 1))
        if self.blank % self.x > 0:
            c = create_child(self.blank-1)
            succ.append((c, 'left', 1))
        if self.blank % self.x < self.x - 1:
            c = create_child(self.blank+1)
            succ.append((c, 'right', 1))
        if self.blank < self.size - self.x:
            c = create_child(self.blank+self.x)
            succ.append((c, 'down', 1))
        return succ

    def is_goal(self):
        return self.size == 16 and Puzzle.goal15 == self.board or \
               self.size == 9 and Puzzle.goal8 == self.board
