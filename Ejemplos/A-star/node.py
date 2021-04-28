class Node:
    def __init__(self, search_state, parent=None, action=''):
        self.state = search_state
        self.parent = parent
        self.action = action   # es el nombre de la accion
        self.key = -1          # es la funcion f
        self.g = 10000000000   # la funcion g de A*
        self.heap_index = 0
        self.h = -1            # la funcion h de A*

    def __repr__(self):
        return self.state.__repr__()

    def trace(self):
        s = ''
        if self.parent:
            s = self.parent.trace()
            s += '-' + self.action + '->'
        s += str(self.state)
        return s
