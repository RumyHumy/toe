#!/usr/bin/python3

# EXAMPLE:
# ./toe.py 1 2 U 5, 2 3 R 2, 3 1 R 3, 1 2 R 3

# nnoremap <F9> <cmd>w<bar>:!./toe.py 1 2 U 5, 2 3 R 2, 3 1 R 3, 1 2 R 3 <CR>

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

class Node:
    ein = []
    eout = []
    def __str__(self):
        sin = ", ".join([e.etype for e in ein])
        sout = ", ".join([e.etype for e in eout])
        return f'Node(in: {sin}; out: {sout})'

class Circuit:
    
    elements = []
    nodes = []

    def __init__(self, textCirc):

        eData = [e.strip().split() for e in textCirc.split(',')]
        eData = [e for e in eData if len(e) != 1 or e != '']
        nodeCount = 0
        for i, e in enumerate(eData):
            if len(e) != 4:
                print(f'Wrong amout of arguments in element {i+1}')
                exit(1)
            e[0] = int(e[0]) # Error handling
            e[1] = int(e[1])
            e[2] = e[2].lower()
            e[3] = float(e[3])
            if e[0] < 1 or e[1] < 1:
                print(f'Invalid node index in element {i+1}')
                exit(1)
            nodeCount = max(nodeCount, e[0], e[1])

        self.elements = [None]*len(eData)
        self.nodes = [Node() for i in range(nodeCount)]
        for i, e in enumerate(eData):
            print(self.elements)

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
                
            self.nodes[e[0]-1].ein.append(self.elements[i])
            self.nodes[e[1]-1].eout.append(self.elements[i])

    def Solve(self): # Mooon

        print(G)
        exit(0)

    def Log(self):
        print('Elements:')
        for i, e in enumerate(self.elements):
            print(f'    {e.etype}{i+1}\t{e}')
        print('Nodes:')
        for i, e in enumerate(self.elements):
            print(f'    {i+1}\t{e}')


if __name__ == "__main__":

    circ = Circuit(' '.join(sys.argv[1:]))
    print()
    print('B E F O R E')
    print()
    circ.Log()
    print()
    print('A F T E R')
    print()
    circ.Log()
