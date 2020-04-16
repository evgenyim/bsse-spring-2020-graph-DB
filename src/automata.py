from pyformlang.regular_expression import Regex
import networkx as nx


def str_to_dfa(s):
    regex = Regex(s)
    enfa = regex.to_epsilon_nfa()
    dfa = enfa.to_deterministic()
    return dfa.minimize()


def str_to_graph(s):
    r = Regex(s)
    a = r.to_epsilon_nfa().minimize()
    start_states = sorted(list(a.start_states))
    final_states = sorted(list(a.final_states))
    g = a.to_networkx()
    g2 = nx.convert_node_labels_to_integers(g, ordering="sorted")
    d = {}
    i = 0
    for node in sorted(g.nodes):
        d[node] = sorted(g2.nodes)[i]
        i += 1
    for i in range(len(start_states)):
        start_states[i] = d[start_states[i]]
    for i in range(len(final_states)):
        final_states[i] = d[final_states[i]]
    labels = nx.get_edge_attributes(g2, 'label')
    return labels, sorted(start_states), sorted(final_states)
