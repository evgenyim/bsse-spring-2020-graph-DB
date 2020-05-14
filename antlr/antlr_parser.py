from antlr4 import *
from antlr.GrammarLexer import GrammarLexer
from antlr.GrammarParser import GrammarParser
from antlr.MyGrammarListener import MyGrammarListener
from antlr.GrammarErrorListener import MyErrorListener
from src.script_handler import ScriptHandler


def read_from_file(file_name):
    input_stream = FileStream(file_name)
    lexer = GrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = GrammarParser(stream)
    parser.addErrorListener(MyErrorListener)
    try:
        tree = parser.complete_script()
        walker = ParseTreeWalker()
        collector = MyGrammarListener()
        walker.walk(collector, tree)
        listener_to_dot(collector)
        print('Script is correct')
        return tree
    except:
        print('Script is incorrect')


def listener_to_dot(listener):
    f = open('out.txt', 'w')
    f.write('digraph Q {\n'
            '\tordering = out;\n')
    for id, name in listener.nodes.items():
        f.write('\t{} [label= \"{}\"];\n'.format(id, name[1]))
    for left, vs in listener.edges.items():
        for v in vs:
            f.write('\t {} -> {};\n'.format(left, v))
    f.write('}')
    f.close()
