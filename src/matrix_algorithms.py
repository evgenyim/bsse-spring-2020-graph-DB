from src.grammar import Grammar
from src.cyk import Graph
from scipy import sparse
from scipy.sparse import *
from src.automata import *
from scipy.sparse.csgraph import floyd_warshall
import numpy as np


def evalCFPQ(g: Grammar, gr: Graph):
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


def evalCFPQ_from_file(grammar_file, graph_file, output_file):
    g = Grammar()
    g.read_from_file(grammar_file)
    gr = Graph()
    gr.read_graph(graph_file)
    t = evalCFPQ(g, gr)
    g.print_grammar(output_file)
    m = t[g.start].toarray()
    out_file = open(output_file, 'a')
    out_file.write('\n')
    for i in range(len(gr.vertices)):
        for j in range(len(gr.vertices)):
            if m[i][j] == 1:
                out_file.write(str(i) + ' ' + str(j) + '\n')


def get_total(i, totals):
    if i >= 2 ** len(totals):
        totals.append(totals[-1] ** 2)
    l = [int(x) for x in bin(i)[2:]]
    ret = False
    for j in range(1, len(l) + 1):
        if l[-j] == 1:
            if ret is False:
                ret = totals[j - 1]
            else:
                ret *= totals[j - 1]
    return ret


def evalCFPQ_tensor(g_lines, gr: Graph):
    my_g = Grammar()
    my_g.split_hard_lines(g_lines)
    t = {}
    rows = {}
    cols = {}
    data = {}
    vertices = 0
    vs = {}
    terms = {}
    S = {}
    F = {}
    for line in g_lines:
        left = line[0]
        if left not in terms:
            terms[left] = 1
        right = line[1:]
        a_graph, starts, finals = str_to_graph(right)
        g = set()
        for (u, v, _), label in sorted(a_graph.items()):
            if label not in terms:
                terms[label] = 1
            if u not in g:
                g.add(u)
                vs[(left, u)] = vertices
                vertices += 1
            if v not in g:
                g.add(v)
                vs[(left, v)] = vertices
                vertices += 1
            if label not in rows:
                rows[label] = []
                cols[label] = []
                data[label] = []
            rows[label] += [vs[(left, u)]]
            cols[label] += [vs[(left, v)]]
            data[label] += [True]
        for v in starts:
            if vs[(left, v)] not in S:
                if left not in S:
                    S[left] = []
                S[left] += [(vs[(left, v)])]
        for v in finals:
            if vs[(left, v)] not in F:
                if left not in F:
                    F[left] = []
                F[left] += [(vs[(left, v)])]
    n = vertices
    for term in terms.keys():
        if term not in rows:
            rows[term] = []
            cols[term] = []
            data[term] = []
        t[term] = csr_matrix((data[term], (rows[term], cols[term])), shape=(n, n), dtype=bool)
    eps_nonterms = my_g.get_eps_gen_nonterminals()
    gr_n = len(gr.vertices)
    rows_gr = {}
    cols_gr = {}
    data_gr = {}
    for u, label, v in gr.edges:
        if label not in rows_gr:
            rows_gr[label] = []
            cols_gr[label] = []
            data_gr[label] = []
        rows_gr[label] += [u]
        cols_gr[label] += [v]
        data_gr[label] += [True]
    for label in eps_nonterms:
        if label not in rows_gr:
            rows_gr[label] = []
            cols_gr[label] = []
            data_gr[label] = []
        for j in range(gr_n):
            rows_gr[label] += [j]
            cols_gr[label] += [j]
            data_gr[label] += [True]
    t_gr = {}
    for term in terms.keys():
        if term not in rows_gr:
            rows_gr[term] = []
            cols_gr[term] = []
            data_gr[term] = []
        t_gr[term] = csr_matrix((data_gr[term], (rows_gr[term], cols_gr[term])), shape=(gr_n, gr_n), dtype=bool)
    changed = True
    m = {}
    n1 = 0
    while changed:
        changed = False
        total = False
        for term in terms:
            m[term] = sparse.kron(t[term], t_gr[term]).astype(bool)
            n1, _ = m[term].shape
            if total is False:
                total = m[term]
            else:
                total = total + m[term]
        t_cl = total
        totals = [total, total * total]
        cnt = 2
        while (t_cl + get_total(cnt, totals) != t_cl).nnz > 0:
            t_cl += get_total(cnt, totals)
            cnt += 1
        for (u, v) in zip(*t_cl.nonzero()):
            s = u // gr_n
            f = v // gr_n
            for left in my_g.nonterminals:
                if left in S and s in S[left] and f in F[left]:
                    new_i = u % gr_n
                    new_j = v % gr_n
                    new_term = left
                    tmp = t_gr[new_term] + csr_matrix(
                        (np.array([True]), (np.array([new_i]), np.array([new_j]))),
                                                 shape=(gr_n, gr_n), dtype=bool)
                    if (tmp != t_gr[new_term]).nnz > 0:
                        t_gr[new_term] = tmp
                        changed = True
    return t_gr, t, terms, my_g.start


def evalCFPQ_tensor_from_file(grammar_file, graph_file, output_file):
    gr = Graph()
    gr.read_graph(graph_file)
    file = open(grammar_file)
    lines = file.read().splitlines()
    t_gr, t, terms, start = evalCFPQ_tensor(lines, gr)
    n, _ = t[start].shape
    gr_m = []
    for i in range(n):
        gr_m += [[]]
        for j in range(n):
           gr_m[i] += ['.']
    for term in terms:
        for (i, j) in zip(*t[term].nonzero()):
            if gr_m[i][j] == '.':
                gr_m[i][j] = term
            else:
                gr_m[i][j] += term
    out_file = open(output_file, 'w')
    w = ''
    for i in range(n):
        s = []
        for j in range(n):
            s += gr_m[i][j]
        w += ' '.join(s) + '\n'
    out_file.write(w)
    out_file.close()
    m = t_gr[start].toarray()
    out_file = open(output_file, 'a')
    w = '\n'
    n, _ = t_gr[start].shape
    for i in range(n):
        for j in range(n):
            if m[i][j] == 1:
                w += str(i) + ' ' + str(j) + '\n'
    out_file.write(w)
