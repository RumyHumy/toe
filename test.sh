#/bin/sh

set -x

# falstad-test.txt
./linear-circuit.py 1 2 I 5, 2 3 R 2, 3 1 R 3
./linear-circuit.py 1 2 U 5, 2 3 R 2, 3 1 R 3
./linear-circuit.py 1 2 U 1, 2 3 R 2, 3 4 I 2, 4 1 R 1, 2 3 R 3
./linear-circuit.py 1 2 U 1, 2 3 R 2, 3 4 I 2, 4 5 I 2, 5 1 R 1
##./toe3.py 1 2 U 5, 2 3 R 2, 3 1 R 3, 1 2 R 3
#./toe3.py 2 1 i 1, 3 4 u 2, 2 3 r 1, 1 3 r 2, 4 5 r 3, 5 1 r 2
#./toe3.py 1 2 u 1, 2 3 r 2, 3 4 i 2, 4 1 r 1
#./toe3.py 2 1 i 1, 1 3 r 1, 3 4 i 2, 3 2 r 2, 4 2 r 2
