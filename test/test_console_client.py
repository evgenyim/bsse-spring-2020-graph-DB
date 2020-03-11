from src.console_client import load, marks
from rdflib import Graph


def test_load():
    g = Graph()
    assert load(g, 'http://bigasterisk.com/foaf.rdf')
    assert len(g.all_nodes()) == 55


def test_marks(capsys):
    g = Graph()
    load(g, 'http://bigasterisk.com/foaf.rdf')
    marks(g)
    captured = capsys.readouterr()
    assert 'http://usefulinc.com/ns/doap#homepage' in captured.out
    assert 'http://www.w3.org/2000/01/rdf-schema#seeAlso' in captured.out
    assert 'http://www.w3.org/ns/auth/rsa#public_exponent' in captured.out
