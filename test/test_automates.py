from src.automates import str_to_dfa, a_intersection
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, finite_automaton


def test_str_to_dfa():
    str1 = '0*1(0|1)*'
    dfa1 = str_to_dfa(str1)
    assert(len(dfa1.states) == 2)
    assert(len(dfa1.final_states) == 1)
    assert(len(dfa1.to_networkx().edges) == 4)
    assert(dfa1.accepts('00010101'))
    assert(not dfa1.accepts('000'))

    str2 = "1* 0 0* 1 (0|1)*"
    dfa2 = str_to_dfa(str2)
    assert (len(dfa2.states) == 3)
    assert (len(dfa2.final_states) == 1)
    assert (len(dfa2.to_networkx().edges) == 6)
    assert (dfa2.accepts('11010101'))
    assert (not dfa2.accepts('10000'))


def test_a_intersection_dfa():
    dfa1 = str_to_dfa('0* 1 (0|1)*')
    dfa2 = str_to_dfa('1* 0 0* 1 (0|1)*')
    dfa3 = a_intersection(dfa1, dfa2)
    assert (len(dfa3.states) == 5)
    assert (len(dfa3.final_states) == 1)
    assert (len(dfa3.to_networkx().edges) == 10)
    assert (dfa3.accepts('001001010'))
    assert (dfa3.accepts('111001001'))


def test_a_intersection_nfa():
    symb_0 = finite_automaton.Symbol('0')
    symb_1 = finite_automaton.Symbol('1')

    nfa1 = NondeterministicFiniteAutomaton()
    nfa1.add_transition(finite_automaton.State(1), symb_1, finite_automaton.State(2))
    nfa1.add_transition(finite_automaton.State(1), symb_0, finite_automaton.State(2))
    nfa1.add_transition(finite_automaton.State(2), symb_0, finite_automaton.State(2))
    nfa1.add_transition(finite_automaton.State(1), symb_1, finite_automaton.State(3))
    nfa1.add_transition(finite_automaton.State(2), symb_1, finite_automaton.State(3))
    nfa1.add_final_state(finite_automaton.State(3))
    nfa1.add_start_state(finite_automaton.State(1))
    assert not nfa1.accepts('1011')

    nfa2 = NondeterministicFiniteAutomaton()
    nfa2.add_transition(finite_automaton.State(1), symb_1, finite_automaton.State(2))
    nfa2.add_transition(finite_automaton.State(2), symb_0, finite_automaton.State(3))
    nfa2.add_transition(finite_automaton.State(3), symb_1, finite_automaton.State(3))
    nfa2.add_transition(finite_automaton.State(3), symb_1, finite_automaton.State(4))
    nfa2.add_transition(finite_automaton.State(1), symb_1, finite_automaton.State(4))
    nfa2.add_transition(finite_automaton.State(1), symb_0, finite_automaton.State(4))
    nfa2.add_final_state(finite_automaton.State(4))
    nfa2.add_start_state(finite_automaton.State(1))
    assert nfa2.accepts('1011')

    nfa3 = a_intersection(nfa1, nfa2)
    assert nfa3.accepts('1')
    assert nfa3.accepts('101')
    assert not nfa3.accepts('1011')
