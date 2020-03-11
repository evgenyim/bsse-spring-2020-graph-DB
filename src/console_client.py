from rdflib import Graph, URIRef
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State, Epsilon, EpsilonNFA, Symbol
from src.automata import str_to_dfa
from networkx.drawing.nx_pydot import write_dot


def rdf_to_dfa(g: Graph):
    enfa = EpsilonNFA()
    start_state = State('start')
    enfa.add_start_state(start_state)
    for a, mark, b in g:
        enfa.add_transition(start_state, Epsilon(), State(a))
        enfa.add_transition(State(a), Symbol(mark), State(b))
        enfa.add_transition(start_state, Epsilon(), State(b))
        enfa.add_final_state(State(a))
        enfa.add_final_state(State(b))
        enfa.add_start_state(State(a))
        enfa.add_start_state(State(b))
    return enfa.to_deterministic()


def graph_query(g: Graph, query, fmt='Emptiness'):
    dfa1: DeterministicFiniteAutomaton = rdf_to_dfa(g)
    dfa2 = str_to_dfa(query)
    res = dfa1.get_intersection(dfa2)
    if fmt == 'Emptiness':
        return len(res.states) == 0
    elif fmt == 'DOT':
        write_dot(res.to_networkx(), '../res.dot')
        return len(res.to_networkx().nodes), len(res.to_networkx().edges)
    else:
        return 'Wrong format'


def load(g: Graph, path):
    try:
        g.parse(path)
    except Exception:
        print('Wrong path')
        return False
    else:
        print('file {} loaded'.format(path))
        return True


def marks(g: Graph):
    if len(g.all_nodes()) == 0:
        print('Graph is empty, try to load it')
    for subj, pred, obj in g:
        print(pred)


def main():
    g = Graph()
    running = True
    while running:
        cmd = input().split()
        if len(cmd) == 0:
            continue
        if cmd[0] == '-exit':
            running = False
        elif cmd[0] == '-load':
            load(g, cmd[1])
        elif cmd[0] == '-marks':
            marks(g)
        elif cmd[0] == '-query':
            print(graph_query(g, cmd[1], cmd[2]))
        elif cmd[0] == '-help':
            print(
                '-load [path] - load file\n' +
                '-marks - show marks on edges in loaded graph\n' +
                '-query [query] [format] - make query to graph\n'
                'formats: Emptiness(shows if intersection is empty), DOT (saves result into dot format)\n'
                '-exit - close client\n'
            )
        else:
            print('Wrong command, type -help')


if __name__ == "__main__":
    main()
