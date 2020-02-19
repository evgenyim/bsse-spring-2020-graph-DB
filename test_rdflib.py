from rdflib import Graph, Literal, BNode, RDF, URIRef
from rdflib.namespace import FOAF


def test_rdflib():
    bob = URIRef("http://example.org/people/Bob")
    linda = BNode()

    name = Literal('Bob')

    g = Graph()

    g.add((bob, RDF.type, FOAF.Person))
    g.add((bob, FOAF.name, name))
    g.add((bob, FOAF.knows, linda))
    g.add((linda, RDF.type, FOAF.Person))
    g.add((linda, FOAF.name, Literal('Linda')))
    g.add((bob, FOAF.age, Literal(42)))
    assert g.value(bob, FOAF.age) == Literal(42)
    assert g.value(bob, FOAF.name) == Literal('Bob')
    assert len(g) == 6
