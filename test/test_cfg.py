from src.cfg import factory_rules, factory_terminal, split_cfg
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


def test_split_cfg():
    lines = ['S a S b S', 'S eps']
    g, symbols = split_cfg(lines)
    assert 'S' in symbols
    assert 'a' in symbols
    assert 'b' in symbols
    new_g = ContextFree.prepare_for_cyk(g)

    assert cyk(new_g, 'abab')
    assert cyk(new_g, 'aabb')
    with raises(Exception):
        cyk(new_g, 'aba')
    with raises(Exception):
        cyk(new_g, 'abba')
