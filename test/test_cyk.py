import os
import tempfile

from src.cyk import *

graph = [('0', 'a', '1'),
         ('1', 'a', '2'),
         ('2', 'a', '0'),
         ('2', 'b', '3'),
         ('3', 'b', '2')]


def test_read_graph():
    gr = Graph()
    path = os.path.dirname(__file__) + '/resources/graph.txt'
    gr.read_graph(path)
    assert gr.vertices == {'0', '1', '2', '3'}
    assert gr.edges == graph


def test_cyk():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/test.txt'
    g.read_from_file(path)
    assert cyk(g, 'ab')
    assert cyk(g, 'aabb')
    assert cyk(g, 'abab')
    assert cyk(g, 'aabaabbb')
    assert not cyk(g, 'a')
    assert not cyk(g, 'aba')
    assert not cyk(g, 'aaba')


def test_cyk_empty():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/test.txt'
    g.read_from_file(path)
    assert cyk(g, '')


def test_cyk_empty2():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/test3.txt'
    g.read_from_file(path)
    assert not cyk(g, '')


def test_cyk_ambigious_grammar():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/ambiguous_grammar.txt'
    g.read_from_file(path)
    assert cyk(g, 'apapa')
    assert not cyk(g, 'papapa')
    assert cyk(g, 'amapa')
    assert not cyk(g, 'aapa')


def test_inh_amb_grammar():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/inh_amb_grammar.txt'
    g.read_from_file(path)
    # Grammar is union of (a^n b^n c^m d^m: n, m > 0) and (a^n b^m c^m d^n: n, m > 0)
    assert cyk(g, 'aabbccdd')
    assert cyk(g, 'aaabbbcccddd')
    assert cyk(g, 'abbccd')
    assert cyk(g, 'aabbcccddd')
    assert not cyk(g, 'abcccdd')


def test_cyk_from_file(capsys):
    g_path = os.path.dirname(__file__) + '/resources/test.txt'
    s_path = os.path.dirname(__file__) + '/resources/s.txt'
    cyk_from_file(g_path, s_path)
    assert capsys.readouterr().out == 'True\n'


def test_hellings():
    g = Grammar()
    g_path = os.path.dirname(__file__) + '/resources/test3.txt'
    g.read_from_file(g_path)
    gr = Graph()
    gr_path = os.path.dirname(__file__) + '/resources/graph.txt'
    gr.read_graph(gr_path)
    lines = hellings(g, gr)
    assert lines == [('A', '0', '1'), ('A', '1', '2'), ('A', '2', '0'), ('B', '2', '3'),
                     ('B', '3', '2'), ('S', '1', '3'), ('S1', '1', '2'), ('S', '0', '2'),
                     ('S1', '0', '3'), ('S', '2', '3'), ('S1', '2', '2'), ('S', '1', '2'),
                     ('S1', '1', '3'), ('S', '0', '3'), ('S1', '0', '2'), ('S', '2', '2'),
                     ('S1', '2', '3')]
    for left, rules in g.rules.items():
        for rule in rules:
            if len(rule) == 1:
                assert rule[0].islower()
            else:
                assert len(rule) == 2
                assert rule[0].isupper()
                assert rule[1].isupper()


def test_hellings_empty_graph():
    g = Grammar()
    g_path = os.path.dirname(__file__) + '/resources/test3.txt'
    g.read_from_file(g_path)
    temp = tempfile.NamedTemporaryFile()
    gr = Graph()
    gr_path = temp.name
    gr.read_graph(gr_path)
    lines = hellings(g, gr)
    assert lines == []


def test_hellings_amb_grammar():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/ambiguous_grammar.txt'
    g.read_from_file(path)
    gr = Graph()
    gr_path = os.path.dirname(__file__) + '/resources/graph2.txt'
    gr.read_graph(gr_path)
    lines = hellings(g, gr)
    assert sorted(lines) == [('A', '0', '1'), ('A', '0', '2'), ('Q2', '0', '1'), ('Q3', '0', '2')]


def test_hellings_inh_amb_grammar():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/inh_amb_grammar.txt'
    g.read_from_file(path)
    gr = Graph()
    gr_path = os.path.dirname(__file__) + '/resources/graph3.txt'
    gr.read_graph(gr_path)
    lines = hellings(g, gr)
    for N, a, b in lines:
        assert N != 'S'


def test_hellings_inh_amb_grammar2():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/inh_amb_grammar.txt'
    g.read_from_file(path)
    gr = Graph()
    gr_path = os.path.dirname(__file__) + '/resources/graph4.txt'
    gr.read_graph(gr_path)
    lines = hellings(g, gr)
    for N, a, b in lines:
        if N == 'S':
            assert a == '0' and b == '3'


def test_hellings_from_file():
    g_path = os.path.dirname(__file__) + '/resources/test3.txt'
    gr_path = os.path.dirname(__file__) + '/resources/graph.txt'
    key_path = os.path.dirname(__file__) + '/resources/test_key.txt'
    temp = tempfile.NamedTemporaryFile()
    hellings_from_file(g_path, gr_path, temp.name)
    assert open(temp.name).readlines() == open(key_path).readlines()

