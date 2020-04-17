import os
import tempfile

from src.matrix_algorithms import *


def test_evalCFPQ():
    g = Grammar()
    g_path = os.path.dirname(__file__) + '/resources/test3.txt'
    g.read_from_file(g_path)
    gr = Graph()
    gr_path = os.path.dirname(__file__) + '/resources/graph.txt'
    gr.read_graph(gr_path)
    t = evalCFPQ(g, gr)
    for left, rules in g.rules.items():
        for rule in rules:
            if len(rule) == 1:
                assert rule[0].islower()
            else:
                assert len(rule) == 2
                assert rule[0].isupper()
                assert rule[1].isupper()
    m = {}
    for term in g.nonterminals:
        m[term] = t[term].toarray()
    pairsS = [(0, 2), (0, 3), (1, 2), (1, 3), (2, 2), (2, 3)]
    pairsA = [(0, 1), (1, 2), (2, 0)]
    pairsB = [(2, 3), (3, 2)]
    pairsS1 = [(0, 2), (0, 3), (1, 2), (1, 3), (2, 2), (2, 3)]
    n = len(gr.vertices)
    for i in range(n):
        for j in range(n):
            for term in g.nonterminals:
                if term == 'S' and (i, j) in pairsS:
                    assert m[term].item((i, j))
                elif term == 'A' and (i, j) in pairsA:
                    assert m[term].item((i, j))
                elif term == 'B' and (i, j) in pairsB:
                    assert m[term].item((i, j))
                elif term == 'S1' and (i, j) in pairsS1:
                    assert m[term].item((i, j))
                else:
                    assert not m[term].item((i, j))


def test_evalCFPQ_empty_graph():
    g = Grammar()
    g_path = os.path.dirname(__file__) + '/resources/test3.txt'
    g.read_from_file(g_path)
    temp = tempfile.NamedTemporaryFile()
    gr = Graph()
    gr_path = temp.name
    gr.read_graph(gr_path)
    t = evalCFPQ(g, gr)
    assert t['S'].toarray().size == 0


def test_evalCFPQ_amb_grammar():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/ambiguous_grammar.txt'
    g.read_from_file(path)
    gr = Graph()
    gr_path = os.path.dirname(__file__) + '/resources/graph2.txt'
    gr.read_graph(gr_path)
    t = evalCFPQ(g, gr)
    m = {}
    for term in g.nonterminals:
        m[term] = t[term].toarray()
    pairsA = [(0, 1), (0, 2)]
    pairsQ2 = [(0, 1)]
    pairsQ3 = [(0, 2)]
    n = len(gr.vertices)
    for i in range(n):
        for j in range(n):
            for term in g.nonterminals:
                if term == 'A' and (i, j) in pairsA:
                    assert m[term].item((i, j))
                elif term == 'Q2' and (i, j) in pairsQ2:
                    assert m[term].item((i, j))
                elif term == 'Q3' and (i, j) in pairsQ3:
                    assert m[term].item((i, j))
                else:
                    assert not m[term].item((i, j))


def test_evalCFPQ_inh_amb_grammar():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/inh_amb_grammar.txt'
    g.read_from_file(path)
    gr = Graph()
    gr_path = os.path.dirname(__file__) + '/resources/graph3.txt'
    gr.read_graph(gr_path)
    t = evalCFPQ(g, gr)
    m = {}
    for term in g.nonterminals:
        m[term] = t[term].toarray()
    n = len(gr.vertices)
    for i in range(n):
        for j in range(n):
            assert not m['S'].item((i, j))


def test_evalCFPQ_inh_amb_grammar2():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/inh_amb_grammar.txt'
    g.read_from_file(path)
    gr = Graph()
    gr_path = os.path.dirname(__file__) + '/resources/graph4.txt'
    gr.read_graph(gr_path)
    t = evalCFPQ(g, gr)
    m = {}
    for term in g.nonterminals:
        m[term] = t[term].toarray()
    n = len(gr.vertices)
    for i in range(n):
        for j in range(n):
            if i == 0 and j == 3:
                assert m['S'].item((i, j))
            else:
                assert not m['S'].item((i, j))


def test_evalCFPQ_from_file():
    g_path = os.path.dirname(__file__) + '/resources/test3.txt'
    gr_path = os.path.dirname(__file__) + '/resources/graph.txt'
    key_path = os.path.dirname(__file__) + '/resources/test_key_evalCPFQ.txt'
    temp = tempfile.NamedTemporaryFile()
    evalCFPQ_from_file(g_path, gr_path, temp.name)
    assert open(temp.name).readlines() == open(key_path).readlines()


def test_evalCFPQ_tensor():
    g_path = os.path.dirname(__file__) + '/resources/test_tensor.txt'
    file = open(g_path)
    lines = file.read().splitlines()
    gr = Graph()
    gr_path = os.path.dirname(__file__) + '/resources/graph.txt'
    gr.read_graph(gr_path)
    t_gr, _, terms, _ = evalCFPQ_tensor(lines, gr)
    m = {}
    for term in terms:
        m[term] = t_gr[term].toarray()
    pairsS = [(0, 2), (0, 3), (1, 2), (1, 3), (2, 2), (2, 3)]
    pairsA = [(0, 1), (1, 2), (2, 0)]
    pairsB = [(2, 3), (3, 2)]
    n = len(gr.vertices)
    for i in range(n):
        for j in range(n):
            for term in terms:
                if term == 'S' and (i, j) in pairsS:
                    assert m[term].item((i, j))
                elif term == 'a' and (i, j) in pairsA:
                    assert m[term].item((i, j))
                elif term == 'b' and (i, j) in pairsB:
                    assert m[term].item((i, j))
                else:
                    assert not m[term].item((i, j))


def test_evalCFPQ_tensor_empty_graph():
    g_path = os.path.dirname(__file__) + '/resources/test_tensor.txt'
    file = open(g_path)
    lines = file.read().splitlines()
    temp = tempfile.NamedTemporaryFile()
    gr = Graph()
    gr_path = temp.name
    gr.read_graph(gr_path)
    t_gr, _, terms, _ = evalCFPQ_tensor(lines, gr)
    assert t_gr['S'].nnz == 0


def test_evalCFPQ_tensor_amb_grammar():
    path = os.path.dirname(__file__) + '/resources/tensor_ambiguous_grammar.txt'
    file = open(path)
    lines = file.read().splitlines()
    gr = Graph()
    gr_path = os.path.dirname(__file__) + '/resources/graph2.txt'
    gr.read_graph(gr_path)
    t_gr, _, terms, _ = evalCFPQ_tensor(lines, gr)
    m = {}
    for term in terms:
        m[term] = t_gr[term].toarray()
    pairsA = [(0, 1), (0, 2)]
    pairsp = [(0, 1)]
    pairsm = [(0, 2)]
    n = len(gr.vertices)
    for i in range(n):
        for j in range(n):
            for term in terms:
                if (term == 'A' or term == 'a') and (i, j) in pairsA:
                    assert m[term].item((i, j))
                elif term == 'p' and (i, j) in pairsp:
                    assert m[term].item((i, j))
                elif term == 'm' and (i, j) in pairsm:
                    assert m[term].item((i, j))
                else:
                    assert not m[term].item((i, j))


def test_evalCFPQ_tensor_inh_amb_grammar():
    path = os.path.dirname(__file__) + '/resources/tensor_inh_amb_grammar.txt'
    file = open(path)
    lines = file.read().splitlines()
    gr = Graph()
    gr_path = os.path.dirname(__file__) + '/resources/graph3.txt'
    gr.read_graph(gr_path)
    t_gr, _, terms, _ = evalCFPQ_tensor(lines, gr)
    m = {}
    for term in terms:
        m[term] = t_gr[term].toarray()
    n = len(gr.vertices)
    for i in range(n):
        for j in range(n):
            assert not m['S'].item((i, j))


def test_evalCFPQ_tensor_inh_amb_grammar2():
    path = os.path.dirname(__file__) + '/resources/tensor_inh_amb_grammar.txt'
    file = open(path)
    lines = file.read().splitlines()
    gr = Graph()
    gr_path = os.path.dirname(__file__) + '/resources/graph4.txt'
    gr.read_graph(gr_path)
    t_gr, _, terms, _ = evalCFPQ_tensor(lines, gr)
    m = {}
    for term in terms:
        m[term] = t_gr[term].toarray()
    n = len(gr.vertices)
    for i in range(n):
        for j in range(n):
            if i == 0 and j == 3:
                assert m['S'].item((i, j))
            else:
                assert not m['S'].item((i, j))


def test_evalCFPQ_tensor_from_file():
    g_path = os.path.dirname(__file__) + '/resources/test_tensor.txt'
    gr_path = os.path.dirname(__file__) + '/resources/graph.txt'
    key_path = os.path.dirname(__file__) + '/resources/test_key_evalCPFQ_tensor.txt'
    temp = tempfile.NamedTemporaryFile()
    evalCFPQ_tensor_from_file(g_path, gr_path, temp.name)
    assert open(temp.name).readlines() == open(key_path).readlines()
