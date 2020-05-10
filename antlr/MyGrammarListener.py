from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl


class MyGrammarListener(ParseTreeListener):
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.cur_node = 0

    def visit_rule(self, ctx, name):
        if id(ctx) not in self.nodes:
            self.nodes[id(ctx)] = (self.cur_node, name)
            self.cur_node += 1
        for child in ctx.children:
            if type(child) is TerminalNodeImpl:
                self.nodes[id(child)] = (self.cur_node, child.symbol.text)
                self.cur_node += 1
                if id(ctx) not in self.edges:
                    self.edges[id(ctx)] = [id(child)]
                else:
                    self.edges[id(ctx)] += [id(child)]
            else:
                if id(ctx) not in self.edges:
                    self.edges[id(ctx)] = [id(child)]
                else:
                    self.edges[id(ctx)] += [id(child)]

    def enterComplete_script(self, ctx):
        self.visit_rule(ctx, 'complete_script')

    def enterScript(self, ctx):
        self.visit_rule(ctx, 'script')

    def enterStmt(self, ctx):
        self.visit_rule(ctx, 'stmt')

    def enterNamed_pattern_stmt(self, ctx):
        self.visit_rule(ctx, 'named_pattern_stmt')

    def enterSelect_stmt(self, ctx):
        self.visit_rule(ctx, 'select_stmt')

    def enterObj_expr(self, ctx):
        self.visit_rule(ctx, 'obj_expr')

    def enterVs_info(self, ctx):
        self.visit_rule(ctx, 'vs_info')

    def enterWhere_expr(self, ctx):
        self.visit_rule(ctx, 'where_expr')

    def enterV_expr(self, ctx):
        self.visit_rule(ctx, 'v_expr')

    def enterPattern(self, ctx):
        self.visit_rule(ctx, 'pattern')

    def enterAlt_elem(self, ctx):
        self.visit_rule(ctx, 'alt_elem')

    def enterSeq_elem(self, ctx):
        self.visit_rule(ctx, 'seq_elem')

    def enterPrim_pattern(self, ctx):
        self.visit_rule(ctx, 'prim_pattern')
