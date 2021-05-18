from silence_tensorflow import silence_tensorflow
silence_tensorflow()
import sys
import random
import copy
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from litemodel import *

class Puzzle:
    goal24 = list(range(25))
    goal15 = list(range(16))
    goal8 = list(range(9))
    model = keras.models.load_model('15puzzle_solver_model.h5')
    lmodel = LiteModel.from_keras_model(model)

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
            elif len(self.board) == 25:
                self.x = 5
                self.size = 25
            else:
                print('puzzle size not supported')
                sys.exit(1)
            if blank == -1:
                self.blank = board.index(0)
        self.preferred = False

    def initialize_pdb(id):
        f = open("pdb"+str(id)+".txt", 'r')
        print('Reading PDB '+str(id))
        line = f.readline(100)
        line = line.rstrip()
        numbers = line.split(' ')
        Puzzle.pdb_pattern[id] = [int(x) for x in numbers]  # los valores incluidos en el patron
        while f:
            line = f.readline(100)
            line = line.rstrip()
            numbers = line.split(' ')
            if len(numbers) < 9: break
            tup = tuple([int(x) for x in numbers[:-1]])
            value = int(numbers[-1])
#            print(tup, value)
            Puzzle.pdb[id][tup] = value


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

    def linear_conflicts(self):
        # fuente: https://github.com/asarandi/n-puzzle/blob/master/npuzzle/heuristics.py
        def count_conflicts(candidate_row, solved_row, size, ans=0):
            counts = [0 for x in range(size)]
            for i, tile_1 in enumerate(candidate_row):
                if tile_1 in solved_row and tile_1 != 0:
                    for j, tile_2 in enumerate(candidate_row):
                        if tile_2 in solved_row and tile_2 != 0:
                            if tile_1 != tile_2:
                                if (solved_row.index(tile_1) > solved_row.index(tile_2)) and i < j:
                                    counts[i] += 1
                                if (solved_row.index(tile_1) < solved_row.index(tile_2)) and i > j:
                                    counts[i] += 1
            if max(counts) == 0:
                return ans * 2
            else:
                i = counts.index(max(counts))
                candidate_row[i] = -1
                ans += 1
                return count_conflicts(candidate_row, solved_row, size, ans)

        if self.size == 16:
            goal = Puzzle.goal15
        elif self.size == 9:
            goal = Puzzle.goal8
        solved = goal
        candidate = self.board
        size = int(np.sqrt(self.size))

        res = self.manhattan() #manhattan(candidate, solved, size)
        candidate_rows = [[] for y in range(size)]
        candidate_columns = [[] for x in range(size)]
        solved_rows = [[] for y in range(size)]
        solved_columns = [[] for x in range(size)]
        for y in range(size):
            for x in range(size):
                idx = (y * size) + x
                candidate_rows[y].append(candidate[idx])
                candidate_columns[x].append(candidate[idx])
                solved_rows[y].append(solved[idx])
                solved_columns[x].append(solved[idx])
        for i in range(size):
                res += count_conflicts(candidate_rows[i], solved_rows[i], size)
        for i in range(size):
                res += count_conflicts(candidate_columns[i], solved_columns[i], size)
        return res

    def nn_repr(self):
        str = ''
        for n in self.board:
            str += '0'*n + '1' + '0'*(15-n)
        return np.array([list(str)]).astype('f')

    def successors(self): # successors
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
            child.preferred = False
            return child

        #prediction = Puzzle.model.predict_step(self.nn_repr()).numpy()
        prediction = Puzzle.lmodel.predict(self.nn_repr())
        #prediction = Puzzle.model.predict(self.nn_repr())
        best = np.argmax(prediction)


#        print('myself:',self)
#        print('my preferred child:')

        succ = []
        if self.blank > self.x - 1:
            c = create_child(self.blank-self.x)
            succ.append((c, 'up', 1))
            if best == 3:
                c.preferred = True
#                print(c)  Puzzle.u
        if self.blank % self.x > 0:
            c = create_child(self.blank-1)
            succ.append((c, 'left', 1))
            if best == 0:
                c.preferred = True
#                print(c)
        if self.blank % self.x < self.x - 1:
            c = create_child(self.blank+1)
            succ.append((c, 'right', 1))
            if best == 2:
                c.preferred = True
#                print(c)
        if self.blank < self.size - self.x:
            c = create_child(self.blank+self.x)
            succ.append((c, 'down', 1))
            if best == 1:
                c.preferred = True
#                print(c)
        return succ




    # ---- SUCESORES QUE RETORNAN TRUST
    def k_accs_successors(self):
        '''
            Crea una lista de tuplas de la forma (estado, accion, costo, trust)
            donde estado es el estado sucesor de self que se genera al ejecutar
            accion (un string) y costo (un numero real) es el costo de accion
        '''
        def create_child(newblank):
            child = copy.deepcopy(self)
            child.blank = newblank
            child.board[child.blank] = 0
            child.board[self.blank] = self.board[newblank]
            child.preferred = False
            return child

        #W, A, S, D = Puzzle.predict(self.board)
        #3up, 0lef, 2right,1down
        #A,S,D,W = Puzzle.model.predict_step(self.nn_repr()).numpy().squeeze() # Orden correcto
        A,S,D,W = Puzzle.lmodel.predict(self.nn_repr()).squeeze() # Orden correcto
        #A,S,D,W = Puzzle.model.predict(self.nn_repr()).squeeze()
        #ldur
        #print(A,S,D,W)


        succ = []
        if self.blank > self.x - 1:
            c = create_child(self.blank-self.x)
            succ.append((c, 'up', 1, W))
#                print(c)  Puzzle.u
        if self.blank % self.x > 0:
            c = create_child(self.blank-1)
            succ.append((c, 'left', 1, A))
#                print(c)
        if self.blank % self.x < self.x - 1:
            c = create_child(self.blank+1)
            succ.append((c, 'right', 1, D))
#                print(c)
        if self.blank < self.size - self.x:
            c = create_child(self.blank+self.x)
            succ.append((c, 'down', 1, S))
#                print(c)
        return succ






    def is_goal(self):
        return self.size == 16 and Puzzle.goal15 == self.board or self.size==9 and Puzzle.goal8 == self.board

    def random_walk(self, steps):
        state = self
        seen = [self]
        for i in range(0, steps):
            state = random.choice(state.successors())[0]
            while state in seen:
                state = random.choice(state.successors())[0]
            seen.append(state)
        return state
