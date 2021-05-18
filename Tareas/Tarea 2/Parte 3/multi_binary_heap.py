# Implementacion de un Heap binario en donde cada elemento del heap
# tiene la propiedad heap_index que corresponde a su posicion en el heap

import sys


class MultiBinaryHeap:
    Max = 10  # Máximo número de heaps que pueden existir

    def __init__(self, id=0, max_size=10000000):
        self.items = [None]*(max_size+1)
        self.size = 0
        self.id = id
        assert(self.id < MultiBinaryHeap.Max)
        self.max_size = max_size

    def clear(self):  # clears the content of the heap
        self.size = 0

    def percolatedown(self, hole, element):
        if self.size == 0:
            return
        while 2*hole <= self.size:
            child = 2*hole
            if child != self.size and self.items[child+1].key[self.id] < self.items[child].key[self.id]:
                child += 1
            if self.items[child].key[self.id] < element.key[self.id]:
                self.items[hole] = self.items[child]
                self.items[hole].heap_index[self.id] = hole
            else:
                break
            hole = child
        self.items[hole] = element
        element.heap_index[self.id] = hole

    def percolateup(self, hole, element):
        if self.size == 0:
            return
        while hole > 1 and element.key[self.id] < self.items[hole//2].key[self.id]:
            self.items[hole] = self.items[hole//2]
            self.items[hole].heap_index[self.id] = hole
            hole //= 2
        self.items[hole] = element
        element.heap_index[self.id] = hole

    def percolateupordown(self, hole, element):
        if self.size == 0:
            return
        if hole > 1 and element.key[self.id] < self.items[hole//2].key[self.id]:
            self.percolateup(hole, element)
        else:
            self.percolatedown(hole, element)

    def top(self):
        if self.size == 0:
            return None
        else:
            return self.items[1]

    def extract(self):
        if self.size == 0:
            return None
        element = self.items[1]
        element.heap_index[self.id] = 0
        self.percolatedown(1, self.items[self.size])
        self.size -= 1
        return element

    def insert(self, element):
        if element.heap_index[self.id] == 0:  # element no esta en el heap
            self.size += 1
            if self.size == self.max_size - 1:
                self.items.extend([None]*10000)
                self.max_size += 10000
            self.percolateup(self.size, element)
        else:  # element esta en el heap; suponemos que su key ha cambiado
            self.percolateupordown(element.heap_index[self.id], element)

    def is_empty(self):
        return self.size == 0

    def __iter__(self):
        return (self.items[i] for i in range(1, self.size))
