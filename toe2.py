#!/usr/bin/python3

# nnoremap <F9> <cmd>w<bar>:!./build.sh<CR>

import sys
import numpy as np

class Element:
    def __init__(self, etype, i, u, r):
        self.etype = etype
        self.i = i
        self.u = u
        self.r = r
    def __str__(self):
        return f'Element(type={self.etype}, i={self.i}, u={self.u}, R={self.r})'

class Circuit:
    elements    = []
    connections = []
    # nodesCount x elementsCount x [0/+-1, el]

    def __init__(self, textCirc):
        eData = [e.strip().split() for e in textCirc.split(',')]
        eData = [e for e in eData if len(e) != 1 or e != '']
        nodeCount = 0
        for i, e in enumerate(eData):
            if len(e) != 4:
                print(f'Wrong amout of arguments in element {i+1}.')
                exit(1)
            try:
                e[0] = int(e[0])
                e[1] = int(e[1])
                e[2] = e[2].lower()
                e[3] = float(e[3])
            except ValueError:
                print(f'Invalid number in element {i+1}.')
                exit(1)
            if e[0] < 1 or e[1] < 1:
                print(f'Invalid node index in element {i+1}.')
                exit(1)
            nodeCount = max(nodeCount, e[0], e[1])

        self.elements    = [None]*len(eData)
        self.connections = [[0]*len(eData) for i in range(nodeCount)]
        for i, e in enumerate(eData):
            self.elements[i] = Element(etype=e[2], i=None, u=None, r=None)
            if   e[2] == 'i':
                self.elements[i].i = e[3]
            elif e[2] == 'u':
                self.elements[i].u = e[3]
            elif e[2] == 'r':
                self.elements[i].r = e[3]
            else:
                print(f'Type "{e[2]}" is undefined in element {i+1}.')
                exit(1)
            self.connections[e[0]-1][i] = -1
            self.connections[e[1]-1][i] = +1

    def Solve(self):
        pass

    def Log(self, cmat=False):
        print('Elements:')
        for i, e in enumerate(self.elements):
            print(f'    {e.etype}{i+1}\t{e}')
            if not cmat:
                print(f'    Connections: {", ".join([str(j) for j in range(len(self.connections)) if self.connections[j][i] != 0])}')
        if cmat:
            print('Connection matrix: ')
            print(self.connections)

if __name__ == "__main__":
    circ = Circuit(' '.join(sys.argv[1:]))
    print()
    print('B E F O R E')
    print()
    circ.Log(cmat=True)
    circ.Solve()
    print()
    print('A F T E R')
    print()
    circ.Log()
