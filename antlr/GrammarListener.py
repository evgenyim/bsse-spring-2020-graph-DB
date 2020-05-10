# Generated from Grammar.g4 by ANTLR 4.7.2
from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl
if __name__ is not None and "." in __name__:
    from .GrammarParser import GrammarParser
else:
    from antlr.GrammarParser import GrammarParser

# This class defines a complete listener for a parse tree produced by GrammarParser.
class GrammarListener(ParseTreeListener):
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


    # Enter a parse tree produced by GrammarParser#complete_script.
    def enterComplete_script(self, ctx:GrammarParser.Complete_scriptContext):
        self.visit_rule(ctx, 'complete_script')

    # Exit a parse tree produced by GrammarParser#complete_script.
    def exitComplete_script(self, ctx:GrammarParser.Complete_scriptContext):
        pass

    # Enter a parse tree produced by GrammarParser#script.
    def enterScript(self, ctx:GrammarParser.ScriptContext):
        self.visit_rule(ctx, 'script')

    # Exit a parse tree produced by GrammarParser#script.
    def exitScript(self, ctx:GrammarParser.ScriptContext):
        pass

    # Enter a parse tree produced by GrammarParser#stmt.
    def enterStmt(self, ctx:GrammarParser.StmtContext):
        self.visit_rule(ctx, 'stmt')


    # Exit a parse tree produced by GrammarParser#stmt.
    def exitStmt(self, ctx:GrammarParser.StmtContext):
        pass
    # Enter a parse tree produced by GrammarParser#named_pattern_stmt.
    def enterNamed_pattern_stmt(self, ctx:GrammarParser.Named_pattern_stmtContext):
        self.visit_rule(ctx, 'named_pattern_stmt')

    # Exit a parse tree produced by GrammarParser#named_pattern_stmt.
    def exitNamed_pattern_stmt(self, ctx:GrammarParser.Named_pattern_stmtContext):
        pass


    # Enter a parse tree produced by GrammarParser#select_stmt.
    def enterSelect_stmt(self, ctx:GrammarParser.Select_stmtContext):
        self.visit_rule(ctx, 'select_stmt')

    # Exit a parse tree produced by GrammarParser#select_stmt.
    def exitSelect_stmt(self, ctx:GrammarParser.Select_stmtContext):
        pass

    # Enter a parse tree produced by GrammarParser#obj_expr.
    def enterObj_expr(self, ctx:GrammarParser.Obj_exprContext):
        self.visit_rule(ctx, 'obj_expr')

    # Exit a parse tree produced by GrammarParser#obj_expr.
    def exitObj_expr(self, ctx:GrammarParser.Obj_exprContext):
        pass

    # Enter a parse tree produced by GrammarParser#vs_info.
    def enterVs_info(self, ctx:GrammarParser.Vs_infoContext):
        self.visit_rule(ctx, 'vs_info')

    # Exit a parse tree produced by GrammarParser#vs_info.
    def exitVs_info(self, ctx:GrammarParser.Vs_infoContext):
        pass


    # Enter a parse tree produced by GrammarParser#where_expr.
    def enterWhere_expr(self, ctx:GrammarParser.Where_exprContext):
        self.visit_rule(ctx, 'where_expr')

    # Exit a parse tree produced by GrammarParser#where_expr.
    def exitWhere_expr(self, ctx:GrammarParser.Where_exprContext):
        pass

    # Enter a parse tree produced by GrammarParser#v_expr.
    def enterV_expr(self, ctx:GrammarParser.V_exprContext):
        self.visit_rule(ctx, 'v_expr')

    # Exit a parse tree produced by GrammarParser#v_expr.
    def exitV_expr(self, ctx:GrammarParser.V_exprContext):
        pass


    # Enter a parse tree produced by GrammarParser#pattern.
    def enterPattern(self, ctx:GrammarParser.PatternContext):
        self.visit_rule(ctx, 'pattern')

    # Exit a parse tree produced by GrammarParser#pattern.
    def exitPattern(self, ctx:GrammarParser.PatternContext):
        pass

    # Enter a parse tree produced by GrammarParser#alt_elem.
    def enterAlt_elem(self, ctx:GrammarParser.Alt_elemContext):
        self.visit_rule(ctx, 'alt_elem')

    # Exit a parse tree produced by GrammarParser#alt_elem.
    def exitAlt_elem(self, ctx:GrammarParser.Alt_elemContext):
        pass

    # Enter a parse tree produced by GrammarParser#seq_elem.
    def enterSeq_elem(self, ctx:GrammarParser.Seq_elemContext):
        self.visit_rule(ctx, 'seq_elem')

    # Exit a parse tree produced by GrammarParser#seq_elem.
    def exitSeq_elem(self, ctx:GrammarParser.Seq_elemContext):
        pass

    # Enter a parse tree produced by GrammarParser#prim_pattern.
    def enterPrim_pattern(self, ctx:GrammarParser.Prim_patternContext):
        self.visit_rule(ctx, 'prim_pattern')

    # Exit a parse tree produced by GrammarParser#prim_pattern.
    def exitPrim_pattern(self, ctx:GrammarParser.Prim_patternContext):
        pass


