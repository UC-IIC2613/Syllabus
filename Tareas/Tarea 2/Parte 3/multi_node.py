from multi_binary_heap import MultiBinaryHeap


class MultiNode:
    def __init__(self, search_state, parent=None, action=''):
        self.state = search_state
        self.parent = parent
        if parent:             # compatibilidad con DFS/BFS
            self.depth = parent.depth + 1
        else:
            self.depth = 0
        self.action = action   # es el nombre de la accion
        self.key = [-1] * MultiBinaryHeap.Max  # un arreglo de valores-f
        self.g = 10000000000   # la funcion g de A*
        self.heap_index = [0] * MultiBinaryHeap.Max
        self.h = [-1] * MultiBinaryHeap.Max   # un arreglo de valores heurísticos

    def __repr__(self):
        return self.state.__repr__() + 'h=' + str(self.h) + '\n' +'key=' + str(self.key) + '\n'

    def trace(self):
        s = ''
        if self.parent:
            s = self.parent.trace()
            s += '-' + self.action + '->'
        s += str(self.state)
        return s
