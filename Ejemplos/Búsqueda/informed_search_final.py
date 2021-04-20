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


class OrderedQueue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        i = 0
        while i < len(self.items) and item.key >= self.items[i].key:
            i += 1
        self.items.insert(i, item)

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
    def __init__(self, search_state, parent=None, action='', key=10000):
        self.state = search_state
        self.parent = parent
        self.action = action
        self.key = key
        self.depth = 0
        self.heap_index = 0
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

    def set_heuristic(self, heur='incorrect'):
        if heur == 'incorrect':
            Puzzle.heuristic = Puzzle.incorrect_tiles
        else:
            Puzzle.heuristic = Puzzle.manhattan

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

    def incorrect_tiles(self):
        num = 0
        for i in range(0, Puzzle.size):
            if self.board[i] == 0:
                continue
            else:
                if self.board[i] != i:
                    num += 1
        return num

    def manhattan(self):
        num = 0
        for i in range(0, Puzzle.size):
            if self.board[i] == 0:
                continue
            else:
                num += abs(i % Puzzle.x - self.board[i] % Puzzle.x)
                num += abs(i // Puzzle.x - self.board[i] // Puzzle.x)
        return num


    def successors(self, r=False):
        def create_child(newblank):
            child = Puzzle(list(self.board), self.blank)
            child.blank = newblank
            child.board[child.blank] = 0
            child.board[self.blank] = self.board[newblank]
            return child

        succ = []
        if self.blank > Puzzle.x - 1:
            c = create_child(self.blank-Puzzle.x)
            succ.append((c, 'up', c.heuristic()))
        if self.blank % Puzzle.x > 0:
            c = create_child(self.blank-1)
            succ.append((c, 'left', c.heuristic()))
        if self.blank % Puzzle.x < Puzzle.x - 1:
            c = create_child(self.blank+1)
            succ.append((c, 'right', c.heuristic()))
        if self.blank < Puzzle.size - Puzzle.x:
            c = create_child(self.blank+Puzzle.x)
            succ.append((c, 'down', c.heuristic()))
        succ.sort(key=lambda x: x[2], reverse=r)
        return succ

    def is_goal(self):
        return self.board == Puzzle.goal

    def random_walk(self, steps):
        state = self
        seen = [self]
        for i in range(0, steps):
            state = random.choice(state.successors())[0]
            while state in seen:
                state = random.choice(state.successors())[0]
            seen.append(state)
        return state


class GenericSearch:
    def __init__(self, initial_state, strategy='bfs'):
        self.expansions = 0
        self.initial_state = initial_state
        self.strategy = strategy
        self.max_depth = 0

    def _newopen(self):
        if self.strategy == 'gbfs':
            return OrderedQueue()
        elif self.strategy == 'bfs':
            return Queue()
        elif self.strategy == 'dfs':
            return Stack()
        else:
            print(type, 'is not supported')
            sys.exit(1)

    def search(self):
        self.open = self._newopen()
        self.expansions = 0
        self.open.insert(Node(self.initial_state))
        self.generated = set()
        self.generated.add(self.initial_state)
        r = self.strategy == 'dfs'
        while not self.open.is_empty():
#            print(self.open)      # muestra open list
            n = self.open.extract()   # extrae n de la open
#            print(n.state)   # muestra el estado recien expandido
            if n.depth > self.max_depth:
                self.max_depth = n.depth
            succ = n.state.successors(r)
            self.expansions += 1
            for child_state, action, h in succ:
                if child_state in self.generated:
                    continue
                child_node = Node(child_state, n, action, h)
                if child_state.is_goal():
                    return child_node
                self.generated.add(child_state)
                self.open.insert(child_node)


# s1 = GenericSearch(State(1), 'dfs')
# result = s1.search()
# print("Expansions:", s1.expansions)
# print("Generated nodes:", s1.generated_nodes)
# print("Size of Open:", len(s1.open))
# print("Size of Closed:", len(s1.closed))
# if result:
#     print('Solution depth:', result.depth)
#     print(result.trace())
#
# s2 = GenericSearch(State(1), 'bfs')
# result = s2.search()
# print("expansions:", s2.expansions)
# print("generated nodes:", s2.generated_nodes)
# print("Size of Open:", len(s2.open))
# print("Size of Closed:", len(s2.closed))
# if result:
#     print('Solution depth:', result.depth)
#     print(result.trace())



# goal = Puzzle()  # crea un puzle con el estado objetivo
# init = goal.random_walk(5)  # caminata aleatoria de 5 pasos
# print('Initial state', init)
# s = GenericSearch(init, 'dfs')
# result = s.search()
# if result:
#     print('Found state at depth ',result.depth)
# #    print(result.trace())

#search = GenericSearch(init, 'dfs')
#result = search.search()
#print(result.trace())



## Problemas interesantes

problems = []
init = Puzzle([0, 1, 5, 3, 6, 2, 7, 8, 4])  # a profundidad 14
problems.append(init)
init = Puzzle([0, 1, 8, 6, 2, 7, 5, 4, 3])  # a profundidad 18
problems.append(init)
init = Puzzle([5, 8, 0, 3, 7, 4, 6, 1, 2])  # a profundidad 22
problems.append(init)
init = Puzzle([5, 2, 1, 8, 7, 3, 4, 6, 0])  # a profundidad 26
problems.append(init)
init = Puzzle([0, 7, 6, 1, 4, 3, 2, 5, 8])  # a profundidad 30
problems.append(init)


print('%10s%10s%10s' % ('#exp', '#gen', '|sol|'))
for init in problems:
    s = GenericSearch(init, 'gbfs')
    init.set_heuristic('manhattan')
#    init.set_heuristic('incorrect')
    result = s.search()
    print('%10d%10d%10d' % (s.expansions, len(s.generated), result.depth))
