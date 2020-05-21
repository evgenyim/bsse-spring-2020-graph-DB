import os
from copy import deepcopy

from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl
from src.grammar import Grammar
from src.matrix_algorithms import evalCFPQ
from src.cyk import Graph

from antlr.GrammarLexer import GrammarLexer
from antlr.GrammarParser import GrammarParser
from antlr.GrammarErrorListener import MyErrorListener


class ScriptHandler(ParseTreeListener):
    def __init__(self):
        self.graphs_path = None
        self.g = Grammar()
        self.cur_left = None
        self.cur_right = ''
        self.cur_graph = None
        self.cur_op = ''
        self.vs = []
        self.start_v = None
        self.start_id = None
        self.finish_v = None
        self.finish_id = None

    def enterComplete_script(self, ctx: GrammarParser.Complete_scriptContext):
        pass

    def exitComplete_script(self, ctx: GrammarParser.Complete_scriptContext):
        pass

    def enterScript(self, ctx: GrammarParser.ScriptContext):
        pass

    def exitScript(self, ctx: GrammarParser.ScriptContext):
        pass

    def enterStmt(self, ctx: GrammarParser.StmtContext):
        if type(ctx.children[0]) is TerminalNodeImpl:
            if ctx.children[0].symbol.text == 'connect':
                self.handle_connect_stmt(ctx)
            elif ctx.children[0].symbol.text == 'list':
                self.handle_list_stmt()

    def exitStmt(self, ctx: GrammarParser.StmtContext):
        pass

    def enterNamed_pattern_stmt(self, ctx: GrammarParser.Named_pattern_stmtContext):
        self.cur_left = ctx.children[0].symbol.text

    def exitNamed_pattern_stmt(self, ctx: GrammarParser.Named_pattern_stmtContext):
        self.cur_left = None

    def enterSelect_stmt(self, ctx: GrammarParser.Select_stmtContext):
        self.cur_graph = ctx.children[3].symbol.text[1:-1]

    def exitSelect_stmt(self, ctx: GrammarParser.Select_stmtContext):
        new_g = Grammar()
        new_g.rules = deepcopy(self.g.rules)
        new_g.nonterminals = self.g.nonterminals.copy()
        new_g.added_nonterminals = self.g.added_nonterminals
        new_start = new_g.add_nonterminal()
        new_g.start = new_start
        new_g.add_antlr_rule(new_start + ' ' + self.cur_right)
        if self.graphs_path is None:
            raise Exception('Graph is not loaded')
        graph_path = self.graphs_path + '/' + self.cur_graph
        gr = Graph()
        gr.read_graph(graph_path)
        vs_len = len(gr.vertices)
        if self.start_id is not None and self.start_id >= vs_len:
            raise Exception('wrong ID')
        if self.finish_id is not None and self.finish_id >= vs_len:
            raise Exception('wrong ID')
        t = evalCFPQ(new_g, gr)
        m = t[new_g.start].toarray()
        if self.cur_op == 'exists':
            self.handle_exist(m, vs_len)
        elif self.cur_op == 'count':
            self.handle_count(m, vs_len)
        else:
            self.handle_select(m, vs_len)
        self.cur_right = ''
        self.cur_op = ''
        self.start_v = None
        self.finish_v = None
        self.start_id = None
        self.finish_id = None
        self.vs = []
        self.cur_graph = None
        self.cur_left = None

    def enterObj_expr(self, ctx: GrammarParser.Obj_exprContext):
        pass

    def exitObj_expr(self, ctx: GrammarParser.Obj_exprContext):
        if len(ctx.children) > 1:
            self.cur_op = ctx.children[0].symbol.text

    def enterVs_info(self, ctx: GrammarParser.Vs_infoContext):
        if len(ctx.children) == 1:
            self.vs = [ctx.children[0].symbol.text]
        else:
            self.vs = [ctx.children[1].symbol.text, ctx.children[3].symbol.text]

    def exitVs_info(self, ctx: GrammarParser.Vs_infoContext):
        pass

    def enterWhere_expr(self, ctx: GrammarParser.Where_exprContext):
        pass

    def exitWhere_expr(self, ctx: GrammarParser.Where_exprContext):
        pass

    def enterV_expr(self, ctx: GrammarParser.V_exprContext):
        if ctx.parentCtx.children[1] == ctx:
            if len(ctx.children) == 1:
                self.start_v = ctx.children[0].symbol.text
            else:
                self.start_v = ctx.children[0].symbol.text
                self.start_id = int(ctx.children[4].symbol.text)
        else:
            if len(ctx.children) == 1:
                self.finish_v = ctx.children[0].symbol.text
            else:
                self.finish_v = ctx.children[0].symbol.text
                self.finish_id = int(ctx.children[4].symbol.text)

    def exitV_expr(self, ctx: GrammarParser.V_exprContext):
        pass

    def enterPattern(self, ctx: GrammarParser.PatternContext):
        pass

    def exitPattern(self, ctx: GrammarParser.PatternContext):
        if type(ctx.parentCtx) is GrammarParser.Named_pattern_stmtContext:
            self.g.add_antlr_rule(self.cur_left + ' ' + self.cur_right)
            self.cur_left = None
            self.cur_right = ''

    def enterAlt_elem(self, ctx: GrammarParser.Alt_elemContext):
        if type(ctx.children[0]) is TerminalNodeImpl:
            self.cur_right += 'eps '

    def exitAlt_elem(self, ctx: GrammarParser.Alt_elemContext):
        if len(ctx.parentCtx.children) > 1:
            self.cur_right += '| '

    def enterSeq_elem(self, ctx: GrammarParser.Seq_elemContext):
        pass

    def exitSeq_elem(self, ctx: GrammarParser.Seq_elemContext):
        if len(ctx.children) > 1:
            self.cur_right += ctx.children[1].symbol.text + ' '

    def enterPrim_pattern(self, ctx: GrammarParser.Prim_patternContext):
        if len(ctx.children) == 1:
            self.cur_right += ctx.children[0].symbol.text + ' '
        else:
            self.cur_right += '( '

    def exitPrim_pattern(self, ctx: GrammarParser.Prim_patternContext):
        if len(ctx.children) > 1:
            self.cur_right += ') '

    def handle_connect_stmt(self, ctx: GrammarParser.StmtContext):
        self.graphs_path = ctx.children[2].symbol.text[1:-1]

    def handle_list_stmt(self):
        for file in sorted(os.listdir(self.graphs_path)):
            cur_file = open(self.graphs_path + '/' + file)
            self.print_file(file, cur_file)
            cur_file.close()

    def handle_select(self, m, vs_len):
        if len(self.vs) == 1:
            ret = self.handle_select_v(m, vs_len)
        else:
            ret = self.handle_select_pair(m, vs_len)
        print(sorted(ret))

    def handle_select_v(self, m, vs_len):
        ret = set()
        is_start = self.start_v == self.vs[0]
        is_finish = self.finish_v == self.vs[0]

        if is_start and is_finish:
            for i in range(vs_len):
                if m[i][i] == 1:
                    ret.add(i)
                return ret
        if is_start and self.start_id is not None:
            if self.finish_id is None:
                for j in range(vs_len):
                    if m[self.start_id][j] == 1:
                        return set(self.start_id)
            elif m[self.start_id][self.finish_id] == 1:
                return set(self.start_id)
            return set()
        if is_finish and self.finish_id is not None:
            if self.start_id is None:
                for i in range(vs_len):
                    if m[i][self.finish_id] == 1:
                        return set(self.finish_id)
            elif m[self.start_id][self.finish_id] == 1:
                return set(self.finish_id)
            return set()
        if is_start:
            ret = set()
            if self.finish_id is None:
                for i in range(vs_len):
                    for j in range(vs_len):
                        if m[i][j] == 1:
                            ret.add(i)
                return ret
            for i in range(vs_len):
                if m[i][self.finish_id] == 1:
                    ret.add(i)
            return ret
        if is_finish:
            ret = set()
            if self.start_id is None:
                for i in range(vs_len):
                    for j in range(vs_len):
                        if m[i][j] == 1:
                            ret.add(j)
                return ret
            for j in range(vs_len):
                if m[self.start_id][j] == 1:
                    ret.add(j)
            return ret
        return set()

    def handle_select_pair(self, m, vs_len):
        ret = set()
        if self.start_v not in self.vs or self.finish_v not in self.vs:
            raise Exception('Wrong vertices')
        if self.start_id is not None and self.finish_id is not None:
            if m[self.start_id][self.finish_id]:
                ret.add((self.start_id, self.finish_id))
            return ret
        if self.start_id is not None:
            for j in range(vs_len):
                if m[self.start_id][j] == 1:
                    ret.add((self.start_id, j))
            return ret
        if self.finish_id is not None:
            for i in range(vs_len):
                if m[i][self.finish_id] == 1:
                    ret.add((i, self.finish_id))
        for i in range(vs_len):
            for j in range(vs_len):
                if m[i][j] == 1:
                    ret.add((i, j))
        return ret

    def handle_count(self, m, vs_len):
        if len(self.vs) == 1:
            ret = self.handle_count_v(m, vs_len)
        else:
            ret = self.handle_count_pair(m, vs_len)
        print(ret)

    def handle_count_v(self, m, vs_len):
        is_start = self.start_v == self.vs[0]
        is_finish = self.finish_v == self.vs[0]

        ret = 0
        if is_start and is_finish:
            for i in range(vs_len):
                ret += m[i][i]
                return ret
        if is_start and self.start_id is not None:
            if self.finish_id is None:
                return self.count_row(m, vs_len, self.start_id)
            return int(m[self.start_id][self.finish_id])
        if is_finish and self.finish_id is not None:
            if self.start_id is None:
                return self.count_column(m, vs_len, self.finish_id)
            return int(m[self.start_id][self.finish_id])
        if is_start:
            if self.finish_id is None:
                s = set()
                for i in range(vs_len):
                    for j in range(vs_len):
                        if m[i][j]:
                            s.add(i)
                return len(s)
            return self.count_column(m, vs_len, self.finish_id)
        if is_finish:
            if self.start_id is None:
                s = set()
                for i in range(vs_len):
                    for j in range(vs_len):
                        if m[i][j]:
                            s.add(j)
                return len(s)
            return self.count_column(m, vs_len, self.start_id)
        return 0

    def handle_count_pair(self, m, vs_len):
        if self.start_id is not None and self.finish_id is not None:
            return int(m[self.start_id][self.finish_id])
        if self.start_id is not None:
            return self.count_row(m, vs_len, self.start_id)
        if self.finish_id is not None:
            ret = 0
            for i in range(vs_len):
                ret += self.count_column(m, vs_len, self.finish_id)
            return ret
        if self.start_v in self.vs and self.finish_v in self.vs:
            ret = 0
            for i in range(vs_len):
                for j in range(vs_len):
                    ret += int(m[i][j])
            return ret
        return 0

    def count_row(self, m, vs_len, i):
        ret = 0
        for j in range(vs_len):
            ret += int(m[i][j])
        return ret

    def count_column(self, m, vs_len, j):
        ret = 0
        for i in range(vs_len):
            ret += int(m[i][j])
        return ret

    def handle_exist(self, m, vs_len):
        if len(self.vs) == 1:
            ret = self.handle_exists_v(m, vs_len)
        else:
            ret = self.handle_exists_pair(m, vs_len)
        print(ret)

    def handle_exists_v(self, m, vs_len):
        is_start = self.start_v == self.vs[0]
        is_finish = self.finish_v == self.vs[0]

        if is_start and is_finish:
            for i in range(vs_len):
                if m[i][i]:
                    return True
        elif is_start and self.start_id is not None:
            if self.finish_id is None:
                return self.check_row(m, vs_len, self.start_id)
            else:
                return m[self.start_id][self.finish_id]
        elif is_finish and self.finish_id is not None:
            if self.start_id is None:
                return self.check_column(m, vs_len, self.finish_id)
            else:
                return m[self.start_id][self.finish_id]
        elif is_start:
            if self.finish_id is None:
                return self.check_all(m, vs_len)
            else:
                return self.check_column(m, vs_len, self.start_id)
        elif is_finish:
            if self.start_id is None:
                return self.check_all(m, vs_len)
            else:
                return self.check_column(m, vs_len, self.start_id)

    def handle_exists_pair(self, m, vs_len):
        if self.start_id is not None and self.finish_id is not None:
            return m[self.start_id][self.finish_id]
        elif self.start_v in self.vs and self.finish_v in self.vs:
            if self.start_id is not None:
                return self.check_row(m, vs_len, self.start_id)
            elif self.finish_id is not None:
                for i in range(vs_len):
                    return self.check_column(m, vs_len, self.finish_id)
            else:
                return self.check_all(m, vs_len)

    def check_all(self, m, vs_len):
        for i in range(vs_len):
            for j in range(vs_len):
                if m[i][j]:
                    return True
        return False

    def check_row(self, m, vs_len, i):
        for j in range(vs_len):
            if m[i][j]:
                return True
        return False

    def check_column(self, m, vs_len, j):
        for i in range(vs_len):
            if m[i][j]:
                return True
        return False

    def print_file(self, name, lines):
        print('FILE ' + name + ':')
        s = ''
        for line in lines:
            s += line
        print(s + '\n')


def handle_script_from_file(file_name):
    input_stream = FileStream(file_name)
    lexer = GrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = GrammarParser(stream)
    parser.addErrorListener(MyErrorListener)
    try:
        tree = parser.complete_script()
        walker = ParseTreeWalker()
        collector = ScriptHandler()
        walker.walk(collector, tree)
        return collector
    except Exception as e:
        print(e)
