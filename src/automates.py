from pyformlang.regular_expression import Regex


def str_to_dfa(s):
    regex = Regex(s)
    enfa = regex.to_epsilon_nfa()
    dfa = enfa.to_deterministic()
    return dfa.minimize()


def a_intersection(a1, a2):
    return a1.get_intersection(a2).to_deterministic()
