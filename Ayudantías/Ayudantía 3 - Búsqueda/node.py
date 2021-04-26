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

    def print_trace(self):
        s = ''
        if self.parent:
            s = self.parent.print_trace()
            s += '-' + self.action + '->'
        s += str(self.state)
        return s

    def trace(self):
        trace = []
        n = self
        while n:
            trace.insert(0, n.state)
            n = n.parent
        return trace
