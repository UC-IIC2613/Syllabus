# Una implementacion muy simplificada de DFS
import sys
import random

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def insert(self, item):
        self.push(item)

    def extract(self):
        return self.pop()

    def is_empty(self):
        return (self.items == [])

    def __repr__(self):
        return str(self.items) + ' (top = final de la lista) '

    def __len__(self):
        return len(self.items)


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def is_empty(self):
        return (self.items == [])

    def __repr__(self):
        return str(self.items) + ' (el del principio se muestra primero) '

    def __len__(self):
        return len(self.items)

    def insert(self, item):
        self.enqueue(item)

    def extract(self):
        return self.dequeue()


class Node:
    def __init__(self, search_state, parent=None, action=''):
        self.state = search_state
        self.parent = parent
        self.action = action
        self.depth = 0
        if parent:
            self.depth += parent.depth + 1

    def __repr__(self):
        return self.state.__repr__()

    def trace(self):
        s = ''
        if self.parent:
            s = self.parent.trace()
            s += '-' + self.action + '->'
        s += str(self.state)
        return s


class State:
    def __init__(self, key):
        self.key = key

    def __eq__(self, other):
        return self.key == other.key

    def __repr__(self):
        return str(self.key)

    def __str__(self):
        return str(self.key)

    def __hash__(self):
        return hash(self.key)

    def successors(self):
        if self.key > 1 and self.key <= 5000:
            return [(State(2*self.key+1), 'right'),
                    (State(2*self.key), 'left'),
                    (State(self.key//2), 'back')]
        elif self.key == 1:
            return [(State(2*self.key+1), 'right'),
                    (State(2*self.key), 'left')]
        else:
            return []

    def is_goal(self):
        return self.key == 2040 or self.key == 5000


class Puzzle:
    x = 3
    size = x*x
    goal = list(range(0, size))

    def __init__(self, board=None, blank=-1):
        if not board:
            self.board = [i for i in range(0, Puzzle.size)]
            self.blank = 0
        else:
            if len(board) != Puzzle.size:
                print('Expecting list of size', Puzzle.size)
                sys.exit(1)
            self.board = board
            if blank == -1:
                self.blank = board.index(0)

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
        for i in range(0, Puzzle.x):
            s += "|"
            s += "|".join([tostr(d) for d in self.board[i*Puzzle.x:i*Puzzle.x+Puzzle.x]])
            s += "|\n"
        return s

    def successors(self):
        def create_child(newblank):
            child = Puzzle(list(self.board), self.blank)
            child.blank = newblank
            child.board[child.blank] = 0
            child.board[self.blank] = self.board[newblank]
            return child

        succ = []
        if self.blank > Puzzle.x - 1:
            succ.append((create_child(self.blank-Puzzle.x), 'up'))
        if self.blank % Puzzle.x > 0:
            succ.append((create_child(self.blank-1), 'left'))
        if self.blank % Puzzle.x < Puzzle.x - 1:
            succ.append((create_child(self.blank+1), 'right'))
        if self.blank < Puzzle.size - Puzzle.x:
            succ.append((create_child(self.blank+Puzzle.x), 'down'))
        return succ

    def is_goal(self):
        return self.board == Puzzle.goal


class GenericSearch:
    def __init__(self, initial_state, strategy='bfs'):
        self.expansions = 0    # cuenta el número de expansiones
        self.initial_state = initial_state
        self.strategy = strategy
        self.max_depth = 0

    def _newopen(self):
        if self.strategy == 'bfs':
            return Queue()
        elif self.strategy == 'dfs':
            return Stack()
        else:
            print(type, 'is not supported')
            sys.exit(1)

    def search(self):
        self.open = self._newopen()
        self.expansions = 0
        initial_node = Node(self.initial_state)
        if self.initial_state.is_goal():
            return initial_node
        self.open.insert(initial_node)
        self.generated = set()  # generated mantiene la union entre OPEN y CLOSED
        self.generated.add(self.initial_state)
        while not self.open.is_empty():
            n = self.open.extract()   # extrae n de la open
            if n.depth > self.max_depth:  # mantiene estadística sobre la prof máxima
                self.max_depth = n.depth  # a la que hemos llegado
            succ = n.state.successors()
            self.expansions += 1
            for child_state, action in succ:
                if child_state in self.generated:
                    continue
                child_node = Node(child_state, n, action)
                if child_state.is_goal():
                    return child_node
                self.generated.add(child_state)
                self.open.insert(child_node)
        return None

# s1 = GenericSearch(State(1), 'dfs')
# result = s1.search()
# print("Expansions:", s1.expansions)
# print("Size of Open:", len(s1.open))
# print("Size of Generated:", len(s1.generated))
# if result:
#     print('Solution depth:', result.depth)
#     print(result.trace())
#
#
# s2 = GenericSearch(State(1), 'bfs')
# result = s2.search()
# print("expansions:", s2.expansions)
# print("Size of Open:", len(s2.open))
# print("Size of Closed:", len(s2.generated))
# if result:
#     print('Solution depth:', result.depth)
#     print(result.trace())




## Problemas interesantes

problems = []
init = Puzzle([0, 1, 5, 3, 6, 2, 7, 8, 4]) # a profundidad 14
#sys.setrecursionlimit(20000)
#s = GenericSearch(init, 'dfs')
#result = s.search()
#print(result.trace())

problems.append(init)
init = Puzzle([0, 1, 8, 6, 2, 7, 5, 4, 3]) # a profundidad 18
problems.append(init)
init = Puzzle([5, 8, 0, 3, 7, 4, 6, 1, 2]) # a profundidad 22
problems.append(init)
init = Puzzle([5, 2, 1, 8, 7, 3, 4, 6, 0]) # a profundidad 26
problems.append(init)
init = Puzzle([0, 7, 6, 1, 4, 3, 2, 5, 8]) # a profundidad 30
problems.append(init)
print(init)

print('DFS:')
print('%10s%10s%10s'%('#exp','#gen','|sol|'))
for init in problems:
    s = GenericSearch(init, 'dfs')
    result = s.search()
    print('%10d%10d%10d'%(s.expansions,len(s.generated),result.depth))

print('\nBFS:')
print('%10s%10s%10s'%('#exp','#gen','|sol|'))
for init in problems:
    s = GenericSearch(init, 'bfs')
    result = s.search()
    print('%10d%10d%10d'%(s.expansions,len(s.generated),result.depth))
