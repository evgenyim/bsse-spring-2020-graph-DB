import os
from src.grammar import *


rules1 = {'S': [['a', 'S', 'b', 'S'], ['eps']]}


def test_read_from_file():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/test.txt'
    g.read_from_file(path)
    assert g.start == 'S'
    assert g.nonterminals == ['S']
    assert g.rules == rules1


def test_add_rule():
    g = Grammar()
    g.add_rule('S', ['a', 'b'])
    assert g.rules == {'S': [['a', 'b']]}


def test_delete_rule():
    g = Grammar()
    g.add_rule('S', ['a', 'b'])
    g.delete_rule('S', ['a', 'b'])
    assert g.rules == {'S': []}


def test_add_nonterminal():
    g = Grammar()
    g.nonterminals = ['Q0']
    t = g.add_nonterminal()
    assert t in g.nonterminals
    assert t != 'Q0'
    assert t == 'Q1'


def test_del_long_rules():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/test.txt'
    g.read_from_file(path)
    g.del_long_rules()
    for left, rules in g.rules.items():
        for rule in rules:
            assert len(rule) <= 2


def test_get_eps_gen_nonterminals():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/test2.txt'
    g.read_from_file(path)
    n = g.get_eps_gen_nonterminals()
    assert n == ['X', 'Y']


def test_del_eps_rules():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/test2.txt'
    g.read_from_file(path)
    g.del_eps_rules()
    for left, rules in g.rules.items():
        if g.start == left:
            continue
        for rule in rules:
            for s in rule:
                assert s != 'eps'


def test_gen_rules():
    g = Grammar()
    g.gen_rules('Z', [], ['a', 'X', 'b', 'Y'], ['X', 'Y'])
    assert ['a', 'b'] in g.rules['Z']
    assert ['a', 'b', 'Y'] in g.rules['Z']
    assert ['a', 'X', 'b'] in g.rules['Z']
    assert ['a', 'X', 'b', 'Y'] in g.rules['Z']


def test_del_chain_rules():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/test2.txt'
    g.read_from_file(path)
    g.del_chain_rules()
    for left, rules in g.rules.items():
        for rule in rules:
            if len(rule) == 1:
                assert rule[0] not in g.nonterminals


def test_find_chain_pairs():
    g = Grammar()
    path = os.path.dirname(__file__) + '/resources/test2.txt'
    g.read_from_file(path)
    n = g.find_chain_pairs()
    assert n == [('S', 'S'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z'), ('Y', 'X')]


def test_del_non_generating_terminals():
    g = Grammar()
    g.nonterminals = ['S', 'X', 'Y']
    g.start = 'S'
    g.rules = {'S': [['a']], 'X': [['Y']], 'Y': [['X']]}
    g.del_non_generating_terminals()
    assert g.rules == {'S': [['a']]}


def test_find_gen_terms():
    g = Grammar()
    g.nonterminals = ['S', 'X', 'Y']
    g.start = 'S'
    g.rules = {'S': [['a']], 'X': [['Y']], 'Y': [['X']]}
    n = g.find_gen_terms()
    assert n == ['S']


def test_del_non_reachable_terminals():
    g = Grammar()
    g.nonterminals = ['S', 'X', 'Y']
    g.start = 'S'
    g.rules = {'S': [['a']], 'X': [['a']], 'Y': [['b']]}
    g.del_nonreachable_terms()
    assert g.rules == {'S': [['a']]}


def test_find_reachable_terms():
    g = Grammar()
    g.nonterminals = ['S', 'X', 'Y']
    g.start = 'S'
    g.rules = {'S': [['a']], 'X': [['a']], 'Y': [['b']]}
    n = g.find_reachable_terms()
    assert n == ['S']


def test_split_terminals():
    g = Grammar()
    g.nonterminals = ['S', 'X', 'Y']
    g.start = 'S'
    g.rules = {'S': [['a']], 'X': [['a', 'b']], 'Y': [['b']]}
    g.split_terminals()
    assert g.rules['Q0'] == [['a']]
    assert g.rules['Q1'] == [['b']]
    assert g.rules['X'] == [['Q0', 'Q1']]
