from antlr4 import *
from antlr.GrammarLexer import GrammarLexer
from antlr.GrammarParser import GrammarParser
from antlr.MyGrammarListener import MyGrammarListener
from antlr.GrammarErrorListener import MyErrorListener


def read_from_file(file_name):
    input_stream = FileStream(file_name)
    lexer = GrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = GrammarParser(stream)
    parser.addErrorListener(MyErrorListener)
    try:
        tree = parser.complete_script()
        print('Script is correct')
        walker = ParseTreeWalker()
        collector = MyGrammarListener()
        walker.walk(collector, tree)
        listener_to_dot(collector)
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

read_from_file('/home/evgeny/spdu/formal-languages/bsse-spring-2020-graph-DB/s.txt')