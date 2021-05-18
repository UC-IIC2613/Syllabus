from multi_binary_heap import MultiBinaryHeap
from multi_node import MultiNode
import time
import sys


class PrefAstar:
    def __init__(self, initial_state, heuristic, num_pref=10, out_of=10, suboptimality=1.5):
        self.expansions = 0
        self.generated = 0
        self.initial_state = initial_state
        self.heuristic = heuristic
        self.num_pref = num_pref
        self.out_of = out_of
        self.suboptimality = suboptimality


    def estimate_suboptimality(self):
        # impleméntame!
        return 0

    def fvalue(self, g, h):
        return g + h  # Optimízame, dado lo que aprendiste en Parte 1!!!

    def search(self):
        self.start_time = time.process_time()
        self.preferred = MultiBinaryHeap(0)
        self.open = MultiBinaryHeap(1)
        self.expansions = 0
        self.open_extractions = 0
        self.preferred_extractions = 0
        incumbent_cost = 10000000
        initial_node = MultiNode(self.initial_state)
        initial_node.g = 0
        initial_node.h[0] = self.heuristic(self.initial_state)
        initial_node.h[1] = initial_node.h[0]
        initial_node.key[0] = self.fvalue(initial_node.g,initial_node.h[0])  # asignamos el valor f
        initial_node.key[1] = self.fvalue(initial_node.g,initial_node.h[1])
        self.open.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        self.incumbent = None
        counter = 0
        while not self.open.is_empty() or not self.preferred.is_empty():
            if self.preferred.is_empty():
                queue = self.open
                self.open_extractions += 1
            elif self.open.is_empty():
                queue = self.preferred
                self.preferred_extractions += 1
            elif counter % self.out_of < self.num_pref:
                queue = self.preferred
                self.preferred_extractions += 1
            else:
                queue = self.open
                self.open_extractions += 1

            counter += 1
            n = queue.extract()

            if n.h[0] == 0:
                self.end_time = time.process_time()
                self.solution = n
                return self.solution

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
                        child_node = MultiNode(child_state, n)
                        child_node.h[0] = self.heuristic(child_state)
                        child_node.h[1] = child_node.h[0]
                        self.generated[child_state] = child_node
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.key[0] =  self.fvalue(child_node.g, child_node.h[0])
                    child_node.key[1] =  self.fvalue(child_node.g, child_node.h[0]) # actualizamos el f de child_node
                    if child_node.state.preferred:
                        self.preferred.insert(child_node) # inserta child_node a la open si no esta en la open
                    else:
                        self.open.insert(child_node)
        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        return None
