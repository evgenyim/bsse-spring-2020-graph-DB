from src.grammar import Grammar


class Graph:
    def __init__(self):
        self.vertices = set()
        self.edges = []

    def read_graph(self, file_name):
        file = open(file_name)
        for line in file.readlines():
            s = line.split()
            v1 = s[0]
            label = s[1]
            v2 = s[2]
            if v1 not in self.vertices:
                self.vertices.add(v1)
            if v2 not in self.vertices:
                self.vertices.add(v2)
            self.edges += [(v1, label, v2)]


def cyk(g: Grammar, s: str):
    if len(s) == 0:
        deduce_eps = False
        for left, rules in g.rules.items():
            for rule in rules:
                if rule == ['eps']:
                    deduce_eps = True
                    break
        return deduce_eps
    g.to_cnf()
    d = []
    s = s.split()
    n = len(s)
    for i in range(n):
        d += [[]]
        for j in range(n):
            d[i] += [[]]
    for i in range(n):
        for left, rules in g.rules.items():
            for rule in rules:
                if s[i] in rule:
                    d[i][i] += [left]
    for m in range(1, n):
        for i in range(n):
            j = min(i + m, n - 1)
            for k in range(i, j):
                for left, rules in g.rules.items():
                    for rule in rules:
                        if len(rule) == 2:
                            if rule[0] in d[i][k] and rule[1] in d[k + 1][j]:
                                d[i][j] += [left]
    return g.start in d[0][n - 1]


def cyk_from_file(g_file, s_file):
    g = Grammar()
    g.read_from_file(g_file)
    s_f = open(s_file)
    s = s_f.readline().replace('\n', ' ')
    print(cyk(g, s))


def hellings(g: Grammar, gr: Graph):
    g.to_reduced_cnf()
    r = []
    m = []
    for v1, label, v2 in gr.edges:
        for left, rules in g.rules.items():
            for rule in rules:
                if len(rule) == 1 and rule[0] == label:
                    r += [(left, v1, v2)]
                    m += [(left, v1, v2)]
    for left, rules in g.rules.items():
        for rule in rules:
            if len(rule) == 1 and rule == ['eps']:
                for v in gr.vertices:
                    r += [(left, v, v)]
                    m += [(left, v, v)]
    while len(m) > 0:
        N, v, u = m.pop(0)
        for term, v1, v2 in r:
            if v2 != v:
                continue
            for left, rules in g.rules.items():
                for rule in rules:
                    if len(rule) == 2 and rule[0] == term and rule[1] == N and (left, v1, u) not in r:
                        m += [(left, v1, u)]
                        r += [(left, v1, u)]
        for term, v1, v2 in r:
            if v1 != u:
                continue
            for left, rules in g.rules.items():
                for rule in rules:
                    if len(rule) == 2 and rule[0] == N and rule[1] == term and (left, v, v2) not in r:
                        m += [(left, v, v2)]
                        r += [(left, v, v2)]
    return r


def hellings_from_file(grammar_file, graph_file, output_file):
    g = Grammar()
    g.read_from_file(grammar_file)
    gr = Graph()
    gr.read_graph(graph_file)
    lines = hellings(g, gr)
    g.print_grammar(output_file)
    out_file = open(output_file, 'a')
    s = '\n'
    for line in lines:
        if line[0] == g.start:
            s += line[1] + ' ' + line[2] + '\n'
    out_file.write(s)
