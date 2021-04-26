# Una implementacion muy simplificada de DFS
import sys
from node import Node

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

class OrderedQueue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        i = 0
        while i < len(self.items):
            if item.key <= self.items[i].key:
                break
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


class GenericSearch:
    def __init__(self, initial_state, strategy='bfs'):
        self.expansions = 0
        self.initial_state = initial_state
        self.strategy = strategy
        self.max_depth = 0  # estadistica que muestra que profundidad máxima
                            # ha descendido el algoritmo
    def _newopen(self):
        if self.strategy == 'bfs':
            return Queue()
        elif self.strategy == 'dfs':
            return Stack()
        elif self.strategy == 'greedy':
            return OrderedQueue()
        else:
            print(type, 'is not supported')
            sys.exit(1)

    def search(self, steps=False):
        self.steps = steps
        self.open = self._newopen()
        self.expansions = 0  # contador de expansiones
        init_node = Node(self.initial_state)
        init_node.key = self.initial_state.distance() ## solo usado en greedy
        self.open.insert(init_node)
        self.generated = set()  ## generated mantiene la union entre OPEN y CLOSED
        self.generated.add(self.initial_state)
        while not self.open.is_empty():
#            print(self.open)      # muestra open list
            n = self.open.extract()   # extrae n de la open
            if self.steps: # Si queremos dibujar paso por paso
                trace = n.trace()
                open_positions = set()
                for c in self.open.items: # agregamos estados de la open
                    open_positions.add((c.state.x, c.state.y))
                generated_positions = set()
                for c in self.generated:
                    pos = (c.x, c.y)
                    if pos not in open_positions: # agregamos de la closed
                        generated_positions.add(pos)
                n.state.map.draw_solution(trace, generated_positions, open_positions)
                stop = input()
                if stop:
                    self.steps = False
#            print(n.state)   # muestra el estado recien expandido
            if n.depth > self.max_depth:
                self.max_depth = n.depth
            succ = n.state.successors()
            self.expansions += 1
            for child_state, action in succ:
                if child_state in self.generated:  # en DFS este chequeo se puede hacer sobre la rama
                    continue
                child_node = Node(child_state, n, action)
                if child_state.is_goal():
                    return child_node
#                child_node.key = child_node.depth + child_state.distance() ## solo usado en greedy
                child_node.key = child_state.distance() ## solo usado en greedy
                self.generated.add(child_state)
                self.open.insert(child_node)
        return None
