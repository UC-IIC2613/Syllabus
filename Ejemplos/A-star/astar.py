from binary_heap import BinaryHeap
from node import Node
import time


class Astar:
    def __init__(self, initial_state, heuristic):
        self.expansions = 0
        self.generated = 0
        self.initial_state = initial_state
        initial_state.set_heuristic(heuristic)

    def search(self):
        self.start_time = time.process_time()
        self.open = BinaryHeap()
        self.expansions = 0
        initial_node = Node(self.initial_state)
        initial_node.g = 0
        initial_node.h = self.initial_state.heuristic()
        initial_node.key = 1000*1*initial_node.h # asignamos el valor f
        self.open.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        while not self.open.is_empty():
            n = self.open.extract()   # extrae n de la open
            if n.state.is_goal():
                self.end_time = time.process_time()
                return n
            succ = n.state.successors()
            self.expansions += 1
            for child_state, action, cost in succ:
                child_node = self.generated.get(child_state)
                is_new = child_node is None  # es la primera vez que veo a child_state
                path_cost = n.g + cost # costo del camino encontrado hasta child_state
                if is_new or path_cost < child_node.g:
                    # si vemos este estado por primera vez o lo vemos por
                    # un mejor camino, entonces lo agregamos a open
                    if is_new:  # creamos el nodo si no existe
                        child_node = Node(child_state, n)
                        child_node.h = child_state.heuristic()
                        self.generated[child_state] = child_node
                    child_node.action = action
                    child_node.g = path_cost
                    child_node.key = 1000*(child_node.g + 1*child_node.h) - child_node.g # actualizamos el f de child_node
                    self.open.insert(child_node) # inserta child_node a la open si no esta en la open
        self.end_time = time.process_time()      # en caso contrario actualiza la prioridad de child_node
        return None                              # es como que 'fisicamente' child_node se cambia de puesto en la open
