from binary_heap import BinaryHeap
from node import Node
import time


class Astar:
    def __init__(self, initial_state, heuristic, weight=1):
        self.expansions = 0
        self.generated = 0
        self.initial_state = initial_state
        self.weight = weight
        self.heuristic = heuristic
        self.solution = None

    # Pregunta 5
    def estimate_suboptimality(self):
        fmin = 100000000
        if self.solution is not None:
            for node in self.open:
                if fmin > node.g + node.h:
                    fmin = node.g + node.h
            return self.solution.g/fmin

    # Pregunta 4
    def fvalue(self, g, h):
        return (g + h, -g)

    def search(self):
        self.start_time = time.process_time()
        self.open = BinaryHeap()
        self.expansions = 0
        self.solution = None
        initial_node = Node(self.initial_state)
        initial_node.g = 0
        initial_node.h = self.heuristic(self.initial_state)
        initial_node.key = 10000*self.weight*initial_node.h  # asignamos el valor f
        self.open.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        while not self.open.is_empty():
            n = self.open.extract()   # extrae n de la open
            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution = n
                return n
            succ = n.state.successors()
            self.expansions += 1
            for child_state, action, cost in succ:
                child_node = self.generated.get(child_state)
                is_new = child_node is None  # es la primera vez que veo a child_state
                path_cost = n.g + cost  # costo del camino encontrado hasta child_state
                if is_new or path_cost < child_node.g:
                    # si vemos el estado child_state por primera vez o lo vemos por
                    # un mejor camino, entonces lo agregamos a open
                    if is_new:  # creamos el nodo de child_state
                        child_node = Node(child_state, n)
                        child_node.h = self.heuristic(child_state)
                        self.generated[child_state] = child_node
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost

                    ## SOLUCIÓN ALTERNATIVA PARTE 4
                    child_node.key = 10000*(child_node.g + self.weight*child_node.h) - child_node.g # actualizamos el f de child_node
                    self.open.insert(child_node) # inserta child_node a la open si no esta en la open
        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        return None
