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

class Node:
    def __init__(self):
        self.ein = []
        self.eout = []
    def __str__(self):
        sin = ", ".join([str(e) for e in self.ein])
        sout = ", ".join([str(e) for e in self.eout])
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
                
            self.nodes[e[0]-1].ein.append(i)
            self.nodes[e[1]-1].eout.append(i)

    def Solve(self): # Mooon

        # A * Y * AT * Un = -A * (J + Y * E)
        # A - cons, Y - cond, J - csrc, E - vsrc

        cons = np.zeros([len(self.nodes)-1, len(self.elements)])       
        cond = np.zeros([len(self.elements), len(self.elements)])
        csrc = np.zeros([len(self.elements), 1])
        vsrc = np.zeros([len(self.elements), 1])

        for i in range(len(self.nodes)-1):
            node = self.nodes[i]
            for e in node.ein:  cons[i][e] = +1
            for e in node.eout: cons[i][e] = -1

        for i, e in enumerate(self.elements):
            if e.etype == 'r':
                cond[i][i] = 1/e.r

        _left = np.matmul(cons, cond)
        left = np.matmul(_left, np.transpose(cons))

        #print(f'A = {cons}')
        #print(f'Y = {cond}')
        #print(f'_left = A * Y =\n{_left}')
        #print(f'left = A * Y * AT =\n{left}')

        for i, e in enumerate(self.elements):
            if e.etype == 'i':
                csrc[i][0] = e.i
        for i, e in enumerate(self.elements):
            if e.etype == 'u':
                vsrc[i][0] = e.u

        _right = csrc + np.matmul(cond, vsrc)
        right = np.matmul(-cons, _right)
        sol = np.linalg.solve(left, right)

        #print(f'_right: J + Y * E =\n{_right}')
        #print(f'right: -A * (J + Y * E) =\n{right}')
        #print(sol)

        #for i, n in enumrate(self.nodes):
        #    for e in n.ein:
        #        pass
        print(sol)

    def Log(self):
        print('Elements:')
        for i, e in enumerate(self.elements):
            print(f'    {e.etype}{i+1}\t{e}')
        print('Nodes:')
        for i, e in enumerate(self.nodes):
            print(f'    {i+1}\t{e}')


if __name__ == "__main__":

    circ = Circuit(' '.join(sys.argv[1:]))
    print()
    print('B E F O R E')
    print()
    circ.Log()
    circ.Solve()
    print()
    print('A F T E R')
    print()
    circ.Log()
