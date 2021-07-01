# Implementacion de un Heap binario en donde cada elemento del heap
# tiene la propiedad heap_index que corresponde a su posicion en el heap

import sys


class BinaryHeap:
    def __init__(self, max_size=10000000):
        self.items = [None]*(max_size+1)
        self.size = 0
        self.max_size = max_size

    def clear(self):  # clears the content of the heap
        self.size = 0

    def percolatedown(self, position, element):
        if self.size == 0:
            return
        while 2*position <= self.size:
            child = 2*position
            if child != self.size and self.items[child+1].key < self.items[child].key:
                child += 1
            if self.items[child].key < element.key:
                self.items[position] = self.items[child]
                self.items[position].heap_index = position
            else:
                break
            position = child
        self.items[position] = element
        element.heap_index = position

    def percolateup(self, position, element):
        if self.size == 0:
            return
        while position > 1 and element.key < self.items[position//2].key:
            self.items[position] = self.items[position//2]
            self.items[position].heap_index = position
            position //= 2
        self.items[position] = element
        element.heap_index = position

    def percolateupordown(self, position, element):
        if self.size == 0:
            return
        if position > 1 and element.key < self.items[position//2].key:
            self.percolateup(position, element)
        else:
            self.percolatedown(position, element)

    def top(self):
        if self.size == 0:
            return None
        else:
            return self.items[1]

    def extract(self):
        if self.size == 0:
            return None
        element = self.items[1]
        element.heap_index = 0
        self.percolatedown(1, self.items[self.size])
        self.size -= 1
        return element

    def insert(self, element):
        if element.heap_index == 0:  # element no esta en el heap
            self.size += 1
            if self.size == self.max_size - 1:
                self.items.extend([None]*10000)
                self.max_size += 10000
            self.percolateup(self.size, element)
        else:  # element esta en el heap; suponemos que su key ha cambiado
            self.percolateupordown(element.heap_index, element)

    def is_empty(self):
        return self.size == 0

    def __iter__(self):
        return (self.items[i] for i in range(1, self.size))

    def reorder(self):
        for i in range(2, self.size+1):
            self.percolateup(i, self.items[i])
