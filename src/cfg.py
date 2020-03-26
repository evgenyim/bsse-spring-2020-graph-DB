from grammpy import Nonterminal, Grammar, Rule, EPS
from grammpy.transforms import ContextFree


def factory_terminal(s):
    class NewClass(Nonterminal):
        pass
    NewClass.__name__ = s
    return NewClass


def factory_rules(rules):
    class NewClass(Rule):
        pass
    a, b = rules
    NewClass.__name__ = a[0].__name__
    NewClass.rule = rules
    return NewClass


def pretty_print(elem, symbols, cnt, file):
    if len(elem.__name__) > 10 and elem.__name__ not in symbols:
        while 'Q' + str(cnt) in symbols:
            cnt += 1
        symbols[elem.__name__] = 'Q' + str(cnt)
        file.write(symbols[elem.__name__] + ' ')
        cnt += 1
    elif len(elem.__name__) > 10:
        file.write(symbols[elem.__name__] + ' ')
    else:
        file.write(elem.__name__ + ' ')
    return cnt


def read_cfg(file_name):
    file = open(file_name)
    ret = split_cfg(file)
    file.close()
    return ret


def split_cfg(lines):
    non_terminals = {}
    terminals = {}
    symbols = {}
    rules = []
    for line in lines:
        s = line.split()
        rule_right = []
        for obj in s:
            if obj[0].isupper() and obj not in non_terminals:
                non_terminals[obj] = factory_terminal(obj)
                rule_right.append(non_terminals[obj])
                symbols[obj] = obj
            elif obj[0].isupper():
                rule_right.append(non_terminals[obj])
            elif obj not in terminals:
                terminals[obj] = obj
                symbols[obj] = obj
                if obj == 'eps':
                    rule_right.append(EPS)
                else:
                    rule_right.append(obj)
            else:
                if obj == 'eps':
                    rule_right.append(EPS)
                else:
                    rule_right.append(obj)
        rules.append(factory_rules(([non_terminals[s[0]]], rule_right[1:])))
    g = Grammar(terminals=terminals,
                nonterminals=list(non_terminals.values()),
                rules=rules, start_symbol=non_terminals['S'])
    return g, symbols


def write_cfg(g, symbols, file):
    cnt = 0
    for r in g.rules:
        a, b = r.rule
        cnt = pretty_print(a[0], symbols, cnt, file)
        for t in b:
            if type(t) is not str and t != EPS:
                cnt = pretty_print(t, symbols, cnt, file)
            elif t == EPS:
                file.write('eps ')
            else:
                file.write(t + ' ')
        file.write('\n')


def to_cnf_from_file(file_name):
    lines = read_cfg(file_name)
    g, symbols = split_cfg(lines)
    new_g = ContextFree.transform_to_chomsky_normal_form(g)
    file = open('../output.txt', 'w')
    write_cfg(new_g, symbols, file)