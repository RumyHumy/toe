#!/usr/bin/python3
# nnoremap 9 <cmd>w<bar>:!./test.sh<CR>

import sys
import numpy as np

if __name__ ==  "__main__":

    # P A R S E

    circ = [e.strip().split() for e in ' '.join(sys.argv[1:]).split(',')]

    vsrcCount = 0
    nodeCount = 0

    nodeSet = set()
    for e in circ:
        e[0] = int(e[0])
        e[1] = int(e[1])
        e[2] = e[2].lower()
        e[3] = float(e[3])
        if   e[2] == 'u':
            vsrcCount += 1
        nodeSet.add(e[0])
        nodeSet.add(e[1])
    nodeNames = sorted(nodeSet)
    nodeCount = len(nodeNames)
    for e in circ:
        e[0] = nodeNames.index(e[0])
        e[1] = nodeNames.index(e[1])

    # S O L V E

    # AX = Z, X - unknowns
    unknownCount = nodeCount+vsrcCount
    A = np.zeros((unknownCount, unknownCount))
    Z = np.zeros((unknownCount, 1))
    
    currentVsrc = 0
    for e in circ:
        if e[2] == 'r':
            A[e[0]][e[0]] += 1/e[3]
            A[e[1]][e[1]] += 1/e[3]
            A[e[0]][e[1]] -= 1/e[3]
            A[e[1]][e[0]] -= 1/e[3]
        elif e[2] == 'u':
            i = nodeCount+currentVsrc
            A[i][e[0]] = -1
            A[e[0]][i] = -1
            A[i][e[1]] = +1
            A[e[1]][i] = +1
            Z[i] = e[3]
            currentVsrc += 1
        elif e[2] == 'i':
            Z[e[0]] = -e[3]
            Z[e[1]] = +e[3]

    try:
        X = np.linalg.solve(A, Z)
        print(X.transpose())
    except:
        print('Ill-formed matrix.')
