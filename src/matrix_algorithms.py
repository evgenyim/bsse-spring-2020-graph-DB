from src.grammar import Grammar
from src.cyk import Graph
from scipy.sparse import *


def evalCPFQ(g: Grammar, gr: Graph):
    g.to_reduced_cnf()
    n = len(gr.vertices)
    t = {}
    rows = {}
    cols = {}
    data = {}
    for term in g.nonterminals:
        rows[term] = []
        cols[term] = []
        data[term] = []
    for i, x, j in gr.edges:
        for left, rules in g.rules.items():
            for rule in rules:
                if len(rule) == 1 and rule[0] == x:
                    rows[left] += [i]
                    cols[left] += [j]
                    data[left] += [True]
    for left, rules in g.rules.items():
        for rule in rules:
            if rule == ['eps']:
                for i in range(n):
                    rows[left] += [i]
                    cols[left] += [i]
                    data[left] += [True]
    for term in g.nonterminals:
        t[term] = csr_matrix((data[term], (rows[term], cols[term])), shape=(n, n), dtype=bool)
    good_rules = []
    for left, rules in g.rules.items():
        for rule in rules:
            if len(rule) == 2:
                good_rules += [(left, rule)]
    changed = True
    while changed:
        changed = False
        for left, rule in good_rules:
            tmp = t[left] + (t[rule[0]] * t[rule[1]])
            if (tmp != t[left]).nnz > 0:
                t[left] = tmp
                changed = True
    return t


def evalCPFQ_from_file(grammar_file, graph_file, output_file):
    g = Grammar()
    g.read_from_file(grammar_file)
    gr = Graph()
    gr.read_graph(graph_file)
    t = evalCPFQ(g, gr)
    g.print_grammar(output_file)
    m = t[g.start].toarray()
    out_file = open(output_file, 'a')
    out_file.write('\n')
    for i in range(len(g.nonterminals)):
        for j in range(len(g.nonterminals)):
            if m[i][j] == 1:
                out_file.write(str(i) + ' ' + str(j) + '\n')
