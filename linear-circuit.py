#!/usr/bin/python3

# nnoremap <F9> <cmd>w<bar>:!./build.sh<CR>

import sys
import numpy as np

if __name__ == "__main__":

    # P A R S E

    textCirc = ' '.join(sys.argv[1:])
    eData = [e.strip().split() for e in textCirc.split(',') if len(e) != 0]
    try:
        eData = [[int(e[0]), int(e[1]), e[2].lower(), float(e[3])] for e in eData]
    except ValueError:
        print('Invalid value.'); exit(1)
    except IndexError:
        print('Not enough arguments for element.'); exit(1)

    eCount = len(eData)
    nCount = max([max(e[0], e[1]) for e in eData])

    cVec = [0]*eCount
    vVec = [0]*eCount
    gVec = [0]*eCount
    connections = [[0]*eCount for i in range(nCount)]

    for i, e in enumerate(eData):
        if   e[2] == 'i':
            cVec[i] = e[3]
        elif e[2] == 'u':
            vVec[i] = e[3]
        elif e[2] == 'r':
            gVec[i] = 1/e[3]
        else:
            print(f'Unknown type in element {i+1}.'); exit(1)
        connections[e[0]-1][i] = -1
        connections[e[1]-1][i] = +1

    # S O L V E

    # A * Y * AT * Un = -A * (J + Y * E)
    # A - cons, Y - condd, J - csrc, E - vsrc
    cons = np.array(connections)
    cond = np.array(gVec)
    csrc = np.array(cVec)
    vsrc = np.array(vVec)

    # R E P L A C E   V - S O U R C E S

    addedNodes = []
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

        addedNode = cons.shape[0]-1
        addedNodes.append(addedNode)
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
        cons[addedNode][cons.shape[1]-1] = +1
        cons[addedNode][cons.shape[1]-2] = -1

    cons = cons[:len(cons)-1]
    if len(addedNodes) > 0:
        addedNodes.pop()

    # C O N S T R U C T   L I N E A R

    condd = np.diag(cond)
    left = cons @ condd @ np.transpose(cons)
    right = cons @ (csrc + condd @ vsrc)

    try:
        nodeVoltages = list(np.linalg.solve(left, right))
    except np.linalg.LinAlgError:
        print("Linear system is singular or ill-conditioned; solution not found."); exit(1)

    for i in range(len(addedNodes)-1, -1, -1):
        nodeVoltages.pop(addedNodes[i]-1)

    if nCount == cons.shape[0]: # Has added nodes
        nodeVoltages = [e-nodeVoltages[-1] for e in nodeVoltages]
    else:
        nodeVoltages.append(0.0)

    print(f"NODE VOLTAGES: {nodeVoltages}")
