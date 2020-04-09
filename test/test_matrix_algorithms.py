import os
import tempfile
import numpy as np

from src.matrix_algorithms import *


def test_evalCPFQ():
    g = Grammar()
    g_path = os.path.dirname(__file__) + '/resources/test3.txt'
    g.read_from_file(g_path)
    gr = Graph()
    gr_path = os.path.dirname(__file__) + '/resources/graph.txt'
    gr.read_graph(gr_path)
    t = evalCPFQ(g, gr)
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
    assert np.array_equal(m['S'], np.array([[False, False, True, True],
                                            [False, False, True, True],
                                            [False, False, True, True],
                                            [False, False, False, False]]))
    assert np.array_equal(m['A'], np.array([[False, True, False, False],
                                            [False, False, True, False],
                                            [True, False, False, False],
                                            [False, False, False, False]]))
    assert np.array_equal(m['B'], np.array([[False, False, False, False],
                                            [False, False, False, False],
                                            [False, False, False, True],
                                            [False, False, True, False]]))
    assert np.array_equal(m['S1'], np.array([[False, False, True, True],
                                             [False, False, True, True],
                                             [False, False, True, True],
                                             [False, False, False, False]]))


def test_evalCPFQ_empty_graph():
    g = Grammar()
    g_path = os.path.dirname(__file__) + '/resources/test3.txt'
    g.read_from_file(g_path)
    temp = tempfile.NamedTemporaryFile()
    gr = Graph()
    gr_path = temp.name
    gr.read_graph(gr_path)
    t = evalCPFQ(g, gr)
    assert t['S'].toarray().size == 0


def test_evalCPFQ_amb_grammar():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/ambiguous_grammar.txt'
    g.read_from_file(path)
    gr = Graph()
    gr_path = os.path.dirname(__file__) + '/resources/graph2.txt'
    gr.read_graph(gr_path)
    t = evalCPFQ(g, gr)
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


def test_evalCPFQ_inh_amb_grammar():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/inh_amb_grammar.txt'
    g.read_from_file(path)
    gr = Graph()
    gr_path = os.path.dirname(__file__) + '/resources/graph3.txt'
    gr.read_graph(gr_path)
    t = evalCPFQ(g, gr)
    m = {}
    for term in g.nonterminals:
        m[term] = t[term].toarray()
    n = len(gr.vertices)
    for i in range(n):
        for j in range(n):
            assert not m['S'].item((i, j))


def test_evalCPFQ_inh_amb_grammar2():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/inh_amb_grammar.txt'
    g.read_from_file(path)
    gr = Graph()
    gr_path = os.path.dirname(__file__) + '/resources/graph4.txt'
    gr.read_graph(gr_path)
    t = evalCPFQ(g, gr)
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


def test_evalCPFQ_from_file():
    g_path = os.path.dirname(__file__) + '/resources/test3.txt'
    gr_path = os.path.dirname(__file__) + '/resources/graph.txt'
    key_path = os.path.dirname(__file__) + '/resources/test_key_evalCPFQ.txt'
    temp = tempfile.NamedTemporaryFile()
    evalCPFQ_from_file(g_path, gr_path, temp.name)
    assert open(temp.name).readlines() == open(key_path).readlines()

