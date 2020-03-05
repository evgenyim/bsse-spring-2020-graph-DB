from pyformlang.regular_expression import Regex


def str_to_dfa(s):
    regex = Regex(s)
    enfa = regex.to_epsilon_nfa()
    dfa = enfa.to_deterministic()
    return dfa.minimize()

