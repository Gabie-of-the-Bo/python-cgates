from model import Circuit


def full_subtractor_circuit(width: int):
    res = Circuit(width*2, width)
    n1 = res.inputs[:width]
    n2 = res.inputs[width:]
    o = res.outputs
    
    bin = None

    for i in reversed(range(width)):
        s = res.xor_gate(n1[i], n2[i])
        b = res.and_gate(s, n2[i])

        if bin:
            b = res.or_gate(res.and_gate(res.not_gate(s), bin), b)
            s = res.xor_gate(s, bin)

        bin = b
        
        res.connect(s, o[i])

    return res


def full_adder_circuit(width: int):
    res = Circuit(width*2, width + 1)
    n1 = res.inputs[:width]
    n2 = res.inputs[width:]
    o = res.outputs
    
    cin = None

    for i in reversed(range(width)):
        s = res.xor_gate(n1[i], n2[i])
        c = res.and_gate(n1[i], n2[i])

        if cin:
            s2 = res.xor_gate(s, cin)
            c = res.or_gate(c, res.and_gate(cin, s))
            s = s2

        cin = c
        
        res.connect(s, o[i + 1])

    res.connect(cin, o[0])

    return res