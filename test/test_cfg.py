import io
from src.cfg import factory_rules, factory_terminal, split_cfg, write_cfg
from grammpy import Nonterminal
from grammpy.transforms import ContextFree
from grammpy.parsers import cyk
from pytest import raises


def test_factory_terminal():
    t = factory_terminal('a')
    assert t.__name__ == 'a'


def test_factory_rules():
    class A(Nonterminal):
        pass
    rules = [[A], ['a', A]]
    t = factory_rules(rules)
    assert t.rule == rules
    assert t.__name__ == A.__name__


# Checks if split read all symbols
def test_split_cfg():
    lines = ['S a S b S', 'S eps']
    g, symbols = split_cfg(lines)
    assert 'S' in symbols
    assert 'a' in symbols
    assert 'b' in symbols


# Checks if split forms grammar
def test_split_cfg_grammar():
    lines = ['S a S b S', 'S eps']
    g, symbols = split_cfg(lines)
    assert len(g.terminals) == 3
    assert len(g.nonterminals) == 1
    assert len(g.rules) == 2

    # Checks if grammar accepts right words using library methods
    new_g = ContextFree.prepare_for_cyk(g)
    assert cyk(new_g, 'abab')
    assert cyk(new_g, 'aabb')
    with raises(Exception):
        cyk(new_g, 'aba')
    with raises(Exception):
        cyk(new_g, 'abba')


# Checks that library function which transforms grammar to cnf works correctly
def test_cnf_grammar_is_equiv():
    lines = ['S a S b S', 'S eps']
    g, symbols = split_cfg(lines)

    tmp_g = ContextFree.transform_to_chomsky_normal_form(g)
    new_g = ContextFree.prepare_for_cyk(tmp_g)
    assert cyk(new_g, 'abab')
    assert cyk(new_g, 'aabb')
    with raises(Exception):
        cyk(new_g, 'aba')
    with raises(Exception):
        cyk(new_g, 'abba')


# Checks that output grammar is the same as input one
def test_write_cfg():
    lines = ['S a S b S', 'S eps']
    g, symbols = split_cfg(lines)
    with io.StringIO() as output:
        write_cfg(g, symbols, output)
        assert output.getvalue() == 'S a S b S \nS eps \n' or \
            output.getvalue() == 'S eps \nS a S b S \n'
