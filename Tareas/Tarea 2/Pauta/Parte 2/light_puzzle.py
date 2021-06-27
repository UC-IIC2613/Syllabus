import sys
import random
import copy
import numpy as np


class Puzzle:
    goal24 = list(range(25))
    goal15 = list(range(16))
    goal8 = list(range(9))
    MaxPDB = 5
    pdb = []
    pdb_pattern = []
    for i in range(MaxPDB):
        pdb.append({})
        pdb_pattern.append(None)

    def __init__(self, board=None, blank=-1):
        if not board:
            self.x = 4
            self.size = 16
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

    # Pregunta 2
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
                num += abs(i % self.x - self.board[i] % self.x) * 1/self.board[i]
                num += abs(i // self.x - self.board[i] // self.x) * 1/self.board[i]
        return num

    # Pregunta 2
    def manhattan15(self):
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
        return num/15


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
            newblank = self.blank-self.x
            c = create_child(newblank)
            succ.append((c, 'up', 1/self.board[newblank]))
        if self.blank % self.x > 0:
            newblank = self.blank-1
            c = create_child(newblank)
            succ.append((c, 'left', 1/self.board[newblank]))
        if self.blank % self.x < self.x - 1:
            newblank = self.blank+1
            c = create_child(newblank)
            succ.append((c, 'right', 1/self.board[newblank]))
        if self.blank < self.size - self.x:
            newblank = self.blank+self.x
            c = create_child(newblank)
            succ.append((c, 'down', 1/self.board[newblank]))
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
