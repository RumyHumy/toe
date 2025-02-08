#!/usr/bin/python3

# nnoremap <F9> <cmd>w<bar>:!./build.sh<CR>

import sys
import numpy as np

if __name__ == "__main__":

    # P R E P A R E

    textCirc = ' '.join(sys.argv[1:])
    eData = [e.strip().split() for e in textCirc.split(',') if len(e) != 0]
    eData = [[int(e[0]), int(e[1]), e[2].lower(), float(e[3])] for e in eData]
    eCount = len(eData)
    nCount = max([max(e[0], e[1]) for e in eData])

    # C I R C U I T

    cVec = [0]*eCount
    vVec = [0]*eCount
    gVec = [0]*eCount
    connections = [[0]*eCount for i in range(nCount)]

    # P A R S E

    for i, e in enumerate(eData):
        if   e[2] == 'i':
            cVec[i] = e[3]
        elif e[2] == 'u':
            vVec[i] = e[3]
        elif e[2] == 'r':
            gVec[i] = 1/e[3]
        connections[e[0]-1][i] = -1
        connections[e[1]-1][i] = +1

    # S O L V E

    # A * Y * AT * Un = -A * (J + Y * E)
    # A - cons, Y - condd, J - csrc, E - vsrc
    cons = np.array(connections[0:nCount-1])
    cond = np.array(gVec)
    csrc = np.array(cVec)
    vsrc = np.array(vVec)

    # R E P L A C E   V - S O U R C E S

    for i in range(cons.shape[1]):
        if vsrc[i] == 0:
            continue

        csrc[i] = vsrc[i]
        vsrc[i] = 0

        cons = np.concatenate((cons, np.zeros((1, cons.shape[1]))), axis=0)
        cons = np.concatenate((cons, np.zeros((cons.shape[0], 2))), axis=1)
        csrc = np.concatenate((csrc, [ 0,  0]))
        vsrc = np.concatenate((vsrc, [ 0,  0]))
        cond = np.concatenate((cond, [-1, +1]))

        srcNode, dstNode = None, None
        for j in range(cons.shape[0]):
            if cons[j][i] == +1:
                cons[j][i] = 0
                dstNode = j
            elif cons[j][i] == -1:
                srcNode = j
        
        cons[dstNode][i] =  0
        cons[srcNode][i] = +1
        cons[dstNode][cons.shape[1]-2] = +1
        cons[srcNode][cons.shape[1]-1] = -1
        cons[cons.shape[0]-1][cons.shape[1]-1] = +1
        cons[cons.shape[0]-1][cons.shape[1]-2] = -1

    # C O N S T R U C T   L I N E A R

    condd = np.diag(cond)
    left = cons @ condd @ np.transpose(cons)
    right = -cons @ (csrc + condd @ vsrc)


    
    sol = np.linalg.solve(left, right)

    print(sol)
