from model import Circuit
from circuits import *


def adder_tests(width: int):
    print(f'* Testing full adder with {width} bit numbers...')

    c = full_adder_circuit(width)

    # Tests

    for a in range(2**width):
        for b in range(2**width):
            ba = list(map(int, bin(a)[2:].zfill(width)))
            bb = list(map(int, bin(b)[2:].zfill(width)))

            res = c.simulate_and_return(ba + bb)

            bres = int(''.join(map(lambda i: str(int(i)), res)), 2)

            if a + b != bres:
                print(f'  - ERROR: {a} + {b} != {bres}')
                return

    print(f'  - Results were correct!')

def subtractor_tests(width: int):
    print(f'* Testing full subtractor with {width} bit numbers...')

    c = full_subtractor_circuit(width)

    # Tests

    for a in range(2**width):
        for b in range(2**width):
            if a >= b:
                ba = list(map(int, bin(a)[2:].zfill(width)))
                bb = list(map(int, bin(b)[2:].zfill(width)))

                res = c.simulate_and_return(ba + bb)

                bres = int(''.join(map(lambda i: str(int(i)), res)), 2)

                if a - b != bres:
                    print(f'  - ERROR: {a} - {b} != {bres}')
                    return

    print(f'  - Results were correct!')

def sr_nor_latch_tests():
    print('* Testing NOR latch...')

    c = Circuit(2, 2)
    s, r = c.inputs
    q, nq = c.outputs

    n1 = c.nor_gate(r)
    n2 = c.nor_gate(s)

    c.connect(n1, n2)
    c.connect(n2, n1)

    c.connect(n1, q)
    c.connect(n2, nq)

    # Tests

    vals = lambda: (c.get_value(q), c.get_value(nq))

    c.init_sim()

    for i in range(10):
        c.feed(s, True)
        c.feed(r, False)
        out = c.simulate(0)
        
        if vals() != (True, False):
            print(f'  - ERROR: invalid latch state {vals()}')
            return

        c.feed(s, False)    
        out = c.simulate(0)
        
        if vals() != (True, False):
            print(f'  - ERROR: invalid latch state {vals()}')
            return

        c.feed(s, False)
        c.feed(r, True)
        out = c.simulate(0, True)

        if vals() != (False, True):
            print(f'  - ERROR: invalid latch state {vals()}')
            return

        c.feed(r, False)    
        out = c.simulate(0)

        if vals() != (False, True):
            print(f'  - ERROR: invalid latch state {vals()}')
            return

    print(f'  - Results were correct!')

def sr_and_or_latch_tests():
    print('* Testing AND-OR latch...')

    c = Circuit(2, 1)
    s, r = c.inputs
    q = c.outputs[0]

    n1 = c.or_gate(s)
    n2 = c.not_gate(r)
    n3 = c.and_gate(n1, n2)
    
    c.connect(n3, n1)
    c.connect(n3, q)

    # Tests

    c.init_sim()

    for i in range(10):
        c.feed(s, True)
        c.feed(r, False)
        out = c.simulate(0)
        
        if not c.get_value(q):
            print(f'  - ERROR: invalid latch state {c.get_value(q)}')
            return

        c.feed(s, False)    
        out = c.simulate(0)
        
        if not c.get_value(q):
            print(f'  - ERROR: invalid latch state {c.get_value(q)}')
            return

        c.feed(s, False)
        c.feed(r, True)
        out = c.simulate(0, True)

        if c.get_value(q):
            print(f'  - ERROR: invalid latch state {c.get_value(q)}')
            return

        c.feed(r, False)    
        out = c.simulate(0)

        if c.get_value(q):
            print(f'  - ERROR: invalid latch state {c.get_value(q)}')
            return

    print(f'  - Results were correct!')
