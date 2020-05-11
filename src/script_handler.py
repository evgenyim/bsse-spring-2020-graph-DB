import os
from copy import deepcopy

from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl
from src.grammar import Grammar
from src.matrix_algorithms import evalCFPQ
from src.cyk import Graph

from antlr.GrammarLexer import GrammarLexer
from antlr.GrammarParser import GrammarParser
from antlr.MyGrammarListener import MyGrammarListener
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
                self.handle_list_stmt(ctx)

    def exitStmt(self, ctx: GrammarParser.StmtContext):
        pass

    def enterNamed_pattern_stmt(self, ctx: GrammarParser.Named_pattern_stmtContext):
        self.cur_left = ctx.children[0].symbol.text

    def exitNamed_pattern_stmt(self, ctx: GrammarParser.Named_pattern_stmtContext):
        self.cur_left = None

    def enterSelect_stmt(self, ctx: GrammarParser.Select_stmtContext):
        self.cur_graph = ctx.children[3].symbol.text[1:-1]

    def exitSelect_stmt(self, ctx: GrammarParser.Select_stmtContext):
        if self.cur_op == 'exists':
            self.handle_exist()
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
        if type(ctx.children[0]) is TerminalNodeImpl and type(ctx.children[1]) is TerminalNodeImpl:
            if ctx.children[0].symbol.text == '(' and ctx.children[1].symbol.text == ')':
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
        if ctx.children[0].symbol.text == 'connect' and ctx.children[1].symbol.text == 'to':
            self.graphs_path = ctx.children[2].symbol.text[1:-1]

    def handle_list_stmt(self, ctx: GrammarParser.StmtContext):
        if ctx.children[0].symbol.text == 'list' and ctx.children[1].symbol.text == 'all' and \
                ctx.children[2].symbol.text == 'graphs':
            self.list_all_graphs()

    def list_all_graphs(self):
        for file in sorted(os.listdir(self.graphs_path)):
            cur_file = open(self.graphs_path + '/' + file)
            self.print_file(file, cur_file)
            cur_file.close()

    def handle_exist(self):
        new_g = Grammar()
        new_g.rules = deepcopy(self.g.rules)
        new_g.nonterminals = self.g.nonterminals.copy()
        new_g.added_nonterminals = self.g.added_nonterminals
        new_start = new_g.add_nonterminal()
        new_g.start = new_start
        new_g.add_antlr_rule(new_start + ' ' + self.cur_right)
        graph_path = self.graphs_path + '/' + self.cur_graph
        gr = Graph()
        gr.read_graph(graph_path)
        vs_len = len(gr.vertices)
        if self.start_id is not None and self.start_id >= vs_len:
            raise Exception('wrong ID')
        if self.finish_id is not None and self.finish_id >= vs_len:
            raise Exception('wrong ID')
        if (self.start_v not in self.vs and self.start_v != '_') or \
           (self.finish_v not in self.vs and self.finish_v != '_'):
            raise Exception('wrong vertice name')
        t = evalCFPQ(new_g, gr)
        ret = False
        m = t[new_g.start].toarray()
        if len(self.vs) == 1:
            is_start = self.start_v == self.vs[0]
            is_finish = self.finish_v == self.vs[0]

            if is_start and is_finish:
                for i in range(vs_len):
                    if m[i][i] == 1:
                        ret = True
            elif is_start and self.start_id is not None:
                i = self.start_id
                if self.finish_id is None:
                    for j in range(vs_len):
                        if m[i][j] == 1:
                            ret = True
                else:
                    ret = m[i][self.finish_id] == 1
            elif is_finish and self.finish_id is not None:
                j = self.finish_id
                if self.start_id is None:
                    for i in range(vs_len):
                        if m[i][j] == 1:
                            ret = True
                else:
                    ret = m[self.start_id][j] == 1
            elif is_start:
                if self.finish_id is None:
                    for i in range(vs_len):
                        for j in range(vs_len):
                            if m[i][j] == 1:
                                ret = True
                else:
                    j = self.finish_id
                    for i in range(vs_len):
                        if m[i][j] == 1:
                            ret = True
            elif is_finish:
                if self.start_id is None:
                    for i in range(vs_len):
                        for j in range(vs_len):
                            if m[i][j] == 1:
                                ret = True
                else:
                    j = self.start_id
                    for i in range(vs_len):
                        if m[i][j] == 1:
                            ret = True
        else:
            if self.start_id is not None and self.finish_id is not None:
                ret = m[self.start_id][self.finish_id]
            elif self.start_v in self.vs and self.finish_v in self.vs:
                if self.start_id is not None:
                    for j in range(vs_len):
                        if m[self.start_id][j] == 1:
                            ret = True
                elif self.finish_id is not None:
                    for i in range(vs_len):
                        if m[i][self.finish_id] == 1:
                            ret = True
                else:
                    for i in range(vs_len):
                        for j in range(vs_len):
                            if m[i][j] == 1:
                                ret = True
        print(ret)

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
