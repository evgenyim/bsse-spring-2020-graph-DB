from copy import deepcopy
from lark.tree import *
from lark.lexer import Token
from src.parser import parse_line, parse_antlr_line

class Grammar:

    def __init__(self):
        self.rules = {}
        self.nonterminals = []
        self.start = ''
        self.added_nonterminals = 0

    def read_from_file(self, file_name):
        file = open(file_name)
        lines = file.readlines()
        start_symb = ''
        for line in lines:
            s = line.split()
            rule_left = s[0]
            rule_right = s[1:]
            self.add_rule(rule_left, rule_right)
            if start_symb == '':
                start_symb = rule_left
                self.start = start_symb

    def add_rule(self, left, right):
        if left not in self.nonterminals:
            self.nonterminals += [left]
        for a in right:
            if a.isupper() and a not in self.nonterminals:
                self.nonterminals += [a]
        if left not in self.rules:
            self.rules[left] = [right]
        else:
            if right not in self.rules[left]:
                self.rules[left] += [right]

    def delete_rule(self, left, rule):
        self.rules[left].remove(rule)

    def add_nonterminal(self):
        while 'Q' + str(self.added_nonterminals) in self.nonterminals:
            self.added_nonterminals += 1
        self.nonterminals += ['Q' + str(self.added_nonterminals)]
        return 'Q' + str(self.added_nonterminals)

    def del_long_rules(self):
        g = deepcopy(self.rules)
        for left, rules in g.items():
            for rule in rules:
                a = left
                if len(rule) > 2:
                    for s in rule[:-2]:
                        new_nonterm = self.add_nonterminal()
                        self.add_rule(a, [s, new_nonterm])
                        a = new_nonterm
                    self.add_rule(a, rule[-2:])
                    self.delete_rule(left, rule)

    def get_eps_gen_nonterminals(self):
        gen_nonterms = []
        for left, rules in self.rules.items():
            for rule in rules:
                if rule == ['eps']:
                    gen_nonterms += [left]
        added = True
        while added:
            added = False
            for left, rules in self.rules.items():
                for rule in rules:
                    if left in gen_nonterms:
                        continue
                    if all(s in gen_nonterms for s in rule):
                        gen_nonterms += [left]
                        added = True
        return gen_nonterms

    def del_eps_rules(self):
        gen_nonterms = self.get_eps_gen_nonterminals()
        for left, rules in self.rules.items():
            for rule in rules:
                if len(list(filter(lambda x: x in gen_nonterms, rule))) == 0:
                    continue
                self.delete_rule(left, rule)
                self.gen_rules(left, [], rule, gen_nonterms)
        eps_deduced = False
        for left, rules in self.rules.items():
            for rule in rules:
                if rule == ['eps']:
                    eps_deduced = True
                    self.delete_rule(left, rule)
        if eps_deduced:
            new_start = self.add_nonterminal()
            self.add_rule(new_start, [self.start])
            self.add_rule(new_start, ['eps'])
            self.start = new_start

    def gen_rules(self, left, left_rule, right_rule, gen_nonterms):
        first_eps = -1
        for r in range(len(right_rule)):
            if right_rule[r] in gen_nonterms:
                first_eps = r
                break
        if first_eps == -1:
            first_eps = len(right_rule)
        left_rule += right_rule[0:first_eps]
        right_rule = right_rule[first_eps:]
        if len(right_rule) == 0 and len(left_rule) == 0:
            return
        if len(right_rule) == 0:
            self.add_rule(left, left_rule)
            return
        eps_t = right_rule[0]
        right_rule = right_rule[1:]
        self.gen_rules(left, left_rule.copy(), right_rule.copy(), gen_nonterms)
        self.gen_rules(left, left_rule.copy() + [eps_t], right_rule.copy(), gen_nonterms)

    def del_chain_rules(self):
        chain_pairs = self.find_chain_pairs()
        new_rules = {}
        for A, B in chain_pairs:
            for rule in self.rules[B]:
                if len(rule) > 1 or (len(rule) == 1 and (A, rule[0]) not in chain_pairs):
                    if new_rules.get(A) is None:
                        new_rules[A] = [rule]
                    else:
                        new_rules[A] = new_rules[A] + [rule]
        self.rules = new_rules

    def find_chain_pairs(self):
        chain_pairs = []
        nonterms = []
        for left, rules in self.rules.items():
            nonterms += [left]
            chain_pairs += [(left, left)]

        for A, B in chain_pairs:
            for rule in self.rules[B]:
                if len(rule) == 1 and rule[0].isupper():
                    if (A, rule[0]) not in chain_pairs:
                        chain_pairs += [(A, rule[0])]
        return chain_pairs

    def del_non_generating_terminals(self):
        gen_terms = self.find_gen_terms()
        rules_ = deepcopy(self.rules)
        for left, rules in rules_.items():
            if left not in gen_terms:
                self.rules.pop(left)
                continue
            for rule in rules:
                if left not in gen_terms or len(list(filter(lambda x: x not in gen_terms and x.isupper(), rule))) > 0:
                    self.delete_rule(left, rule)

    def find_gen_terms(self):
        gen_terms = []
        for left, rules in self.rules.items():
            for rule in rules:
                if len(list(filter(lambda x: x.islower(), rule))) == len(rule):
                    if left not in gen_terms:
                        gen_terms += [left]
        added = True
        while added:
            added = False
            for left, rules in self.rules.items():
                for rule in rules:
                    if len(list(filter(lambda x: x.islower() or x in gen_terms, rule))) == len(rule):
                        if left not in gen_terms:
                            gen_terms += [left]
                            added = True
        return gen_terms

    def del_nonreachable_terms(self):
        reachable_terms = self.find_reachable_terms()
        rules_ = deepcopy(self.rules)
        for left, rules in rules_.items():
            if left not in reachable_terms:
                self.rules.pop(left)
                continue
            for rule in rules:
                if left not in reachable_terms or \
                        len(list(filter(lambda x: x not in reachable_terms and x.isupper(), rule))) > 0:
                    self.delete_rule(left, rule)

    def find_reachable_terms(self):
        reachable_terms = [self.start]
        added = True
        while added:
            added = False
            for left, rules in self.rules.items():
                if left in reachable_terms:
                    for rule in rules:
                        for s in rule:
                            if s.isupper() and s not in reachable_terms:
                                reachable_terms += [s]
                                added = True
        return reachable_terms

    def split_terminals(self):
        rules_ = deepcopy(self.rules)
        terms_map = {}
        for left, rules in rules_.items():
            for rule in rules:
                if len(rule) > 1:
                    changed = False
                    if rule[0].islower():
                        if rule[0] in terms_map:
                            t1 = terms_map[rule[0]]
                        else:
                            t1 = self.add_nonterminal()
                            terms_map[rule[0]] = t1
                        self.add_rule(t1, [rule[0]])
                        changed = True
                    else:
                        t1 = rule[0]
                    if rule[1].islower():
                        if rule[1] in terms_map:
                            t2 = terms_map[rule[1]]
                        else:
                            t2 = self.add_nonterminal()
                            terms_map[rule[1]] = t2
                        self.add_rule(t2, [rule[1]])
                        changed = True
                    else:
                        t2 = rule[1]
                    if changed:
                        self.delete_rule(left, rule)
                        self.add_rule(left, [t1, t2])

    def read_hard_from_file(self, file_name):
        file = open(file_name)
        lines = file.read().splitlines()
        self.split_hard_lines(lines)

    def split_hard_lines(self, lines):
        start_symb = self.start
        for line in lines:
            tree = parse_line(line)
            term = tree.children[0]
            if start_symb == '':
                start_symb = term.value
                self.start = term.value
            self.add_rule(term.value, self.split_tree(tree.children[1]))

    def add_antlr_rule(self, line):
        tree = parse_antlr_line(line)
        term = tree.children[0]
        if self.start == '':
            self.start = term.value
        self.add_rule(term.value, self.split_tree(tree.children[1]))

    def split_tree(self, tree: Tree):
        tree_type = tree.data
        if tree_type == 'expr':
            c = tree.children[0]
            if type(c) == Token:
                return [self.split_token(c)]
            return self.split_tree(c)
        if tree_type == 'or_expr':
            return self.split_or_expr(tree)
        if tree_type == 'star_expr':
            return self.split_star_expr(tree)
        if tree_type == 'plus_expr':
            return self.split_plus_expr(tree)
        if tree_type == 'q_expr':
            return self.split_q_expr(tree)
        if tree_type == 'ready_expr':
            ret = []
            for token in tree.children:
                ret += [token.value]
            return ret
        if tree_type == 'set_expr':
            ret = []
            for c in tree.children:
                if type(c) == Tree:
                    ret += self.split_tree(c)
                else:
                    ret += self.split_token(c)
            return ret

    def split_or_expr(self, tree):
        t1 = tree.children[0]
        t2 = tree.children[1]
        term = self.add_nonterminal()
        self.add_rule(term, self.split_tree(t1))
        self.add_rule(term, self.split_tree(t2))
        return [term]

    def split_star_expr(self, tree):
        if type(tree.children[0]) == Token:
            token = tree.children[0]
            term = self.add_nonterminal()
            self.add_rule(term, [token.value, term])
            self.add_rule(term, ['eps'])
            return [term]
        else:
            rule = self.split_tree(tree.children[0])
            term = self.add_nonterminal()
            self.add_rule(term, rule + [term])
            self.add_rule(term, ['eps'])
            return [term]

    def split_plus_expr(self, tree):
        if type(tree.children[0]) == Token:
            token = tree.children[0]
            term = self.add_nonterminal()
            self.add_rule(term, [token.value, term])
            self.add_rule(term, [token.value])
            return [term]
        else:
            rule = self.split_tree(tree.children[0])
            term = self.add_nonterminal()
            self.add_rule(term, rule + [term])
            self.add_rule(term, rule)
            return [term]

    def split_q_expr(self, tree):
        if type(tree.children[0]) == Token:
            token = tree.children[0]
            term = self.add_nonterminal()
            self.add_rule(term, [token.value])
            self.add_rule(term, ['eps'])
            return [term]
        else:
            rule = self.split_tree(tree.children[0])
            term = self.add_nonterminal()
            self.add_rule(term, rule)
            self.add_rule(term, ['eps'])
            return [term]

    def split_token(self, t):
        return t.value

    def print_grammar(self, file_name):
        file = open(file_name, 'w')
        start = self.start
        rules_ = self.rules[start]
        ret = ''
        for rule in rules_:
            ret += start + ' '
            for s in rule:
                ret += s + ' '
            ret = ret[:-1]
            ret += '\n'
        for left, rules in self.rules.items():
            if left == start:
                continue
            for rule in rules:
                ret += left + ' '
                for s in rule:
                    ret += s + ' '
                ret = ret[:-1]
                ret += '\n'
        file.write(ret)
        file.close()

    def to_cnf(self):
        self.del_long_rules()
        self.del_eps_rules()
        self.del_chain_rules()
        self.del_non_generating_terminals()
        self.del_nonreachable_terms()
        self.split_terminals()

    def to_reduced_cnf(self):
        self.del_long_rules()
        self.del_chain_rules()
        self.del_non_generating_terminals()
        self.del_nonreachable_terms()
        self.split_terminals()

    def file_to_cnf(self, in_file, out_file):
        self.read_from_file(in_file)
        self.to_cnf()
        self.print_grammar(out_file)
