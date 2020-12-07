import igraph
import pandas as pd

# ***** Constants *****

OR, AND, NOT, NAND, NOR, XOR = range(6)

# ***** Functions *****

def id_generator():
    id = 0

    while True:
        yield id
        id += 1

# ***** Inputs and outputs *****

class Input:
    def __init__(self, gen, name):
        self.id = next(gen)
        self.name = name

    def label(self):
        return self.name

    def color(self):
        return 'red'

    def calc(self, *inputs):
        return False


class Output:
    def __init__(self, gen, name):
        self.id = next(gen)
        self.name = name

    def label(self):
        return self.name

    def color(self):
        return 'blue'

    def calc(self, *inputs):
        return any(inputs)

# ***** Logic gates *****

class LogicGate:
    def __init__(self, gen, gate):
        self.id = next(gen)
        self.gate = gate

    def label(self):
        return ''

    def color(self):
        return 'green'


class OrGate(LogicGate):
    def __init__(self, gen):
        super().__init__(gen, OR)

    def calc(self, *inputs):
        return any(inputs)


class AndGate(LogicGate):
    def __init__(self, gen):
        super().__init__(gen, AND)

    def calc(self, *inputs):
        return all(inputs)


class NotGate(LogicGate):
    def __init__(self, gen):
        super().__init__(gen, NOT)

    def calc(self, input):
        return not input


class NandGate(LogicGate):
    def __init__(self, gen):
        super().__init__(gen, NAND)

    def calc(self, *inputs):
        return not all(inputs)


class NorGate(LogicGate):
    def __init__(self, gen):
        super().__init__(gen, NOR)

    def calc(self, *inputs):
        return not any(inputs)


class XorGate(LogicGate):
    def __init__(self, gen):
        super().__init__(gen, XOR)

    def calc(self, *inputs):
        return bool(sum(inputs) % 2)

# ***** Circuit *****

class Circuit:
    def __init__(self, inputs, outputs):
        self.id_gen = id_generator()

        self.inputs = inputs
        self.outputs = outputs
        self.gates = []
        self.corr = {}

        if isinstance(self.inputs, int):
            self.inputs = [Input(self.id_gen, f'I_{i}') for i in range(self.inputs)]

        if isinstance(self.outputs, int):
            self.outputs = [Output(self.id_gen, f'O_{i}') for i in range(self.outputs)]

        for i in self.inputs:
            self.corr[i.id] = i

        for i in self.outputs:
            self.corr[i.id] = i

        self.graph = igraph.Graph(directed=True)
        self.graph.add_vertices([i.id for i in self.inputs])
        self.graph.add_vertices([i.id for i in self.outputs])

    # ***** Circuit operations *****

    def add_gate(self, gate):
        self.graph.add_vertex(gate.id)
        
        self.gates.append(gate)
        self.corr[gate.id] = gate

    def connect(self, a, b):
        self.graph.add_edge(a.id, b.id)

    # ***** Logic gates *****

    def gate_wrapper(self, gate, *inputs):
        self.add_gate(gate)
        
        for i in inputs:
            self.connect(i, gate)

        return gate

    def and_gate(self, *inputs):
        return self.gate_wrapper(AndGate(self.id_gen), *inputs)

    def or_gate(self, *inputs):
        return self.gate_wrapper(OrGate(self.id_gen), *inputs)

    def not_gate(self, input):
        return self.gate_wrapper(NotGate(self.id_gen), input)

    def xor_gate(self, *inputs):
        return self.gate_wrapper(XorGate(self.id_gen), *inputs)

    def nor_gate(self, *inputs):
        return self.gate_wrapper(NorGate(self.id_gen), *inputs)

    # ***** Simulation *****

    def init_sim(self):
        self.node_values = {i: False for i in self.graph.vs['name']}

    def get_value(self, vertex):
        return self.node_values[vertex.id]

    def get_values(self):
        return [self.node_values[i] for i in self.graph.vs['name']]

    def feed(self, input, value):
        self.node_values[input.id] = value

    def simulate_cycle(self):
        node_outs = {i: len(self.graph.neighbors(i, mode=igraph.OUT)) for i in self.graph.vs['name']}
        new_values = {i: j for i, j in self.node_values.items()}

        for i in self.graph.vs['name']:
            if not isinstance(self.corr[i], Input):
                inputs = self.graph.neighbors(i, mode=igraph.IN)
                i_vals = [self.node_values[j] for j in inputs]
                new_val = self.corr[i].calc(*i_vals)
                
                new_values[i] = new_val

        change = new_values != self.node_values

        self.node_values = new_values

        return change

    def simulate(self, max_cycles=1, generate_table=False):
        it = 0

        if generate_table:
            table = [self.get_values()]

        while True:
            if max_cycles > 0 and it >= max_cycles:
                break

            change = self.simulate_cycle()

            if not change: break

            if generate_table:
                table.append(self.get_values())

            it += 1

        if generate_table:
            cols = []

            for i in self.graph.vs['name']:
                l = self.corr[i].label()

                cols.append(l if l else i)

            return pd.DataFrame(table, columns=cols)

    def simulate_and_return(self, inputs, debug=False):
        self.init_sim()

        for n, i in enumerate(self.inputs):
            self.feed(i, bool(inputs[n]))

        out = self.simulate(0, debug)

        if debug:
            print(out)

        return [self.get_value(i) for i in self.outputs]

    # ***** Plotting *****

    def plot(self, size=600):
        self.graph.vs['color'] = [self.corr[i].color() for i in self.graph.vs['name']]
        self.graph.vs['label'] = [self.corr[i].label() for i in self.graph.vs['name']]

        return igraph.plot(self.graph, layout=self.graph.layout_sugiyama(), bbox=(0, 0, size, size))