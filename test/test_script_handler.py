import tempfile

from src.script_handler import *
from src.cyk import cyk


def test_list_all_graphs(capsys):
    path = os.path.dirname(__file__) + '/resources'
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('connect to [{}];\n'
            'list all graphs;'.format(path + '/test_dir'))
    f.close()
    handle_script_from_file(temp.name)
    lines = open(path + '/script_out.txt').read()
    assert capsys.readouterr().out == lines


def test_named_pattern(capsys):
    path = os.path.dirname(__file__) + '/resources'
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('connect to [{}];\n'
            'S = a S b S | ();'.format(path + '/test_dir'))
    f.close()
    h = handle_script_from_file(temp.name)
    assert h.g.rules == {'Q0': [['a', 'S', 'b', 'S'], ['eps']], 'S': [['Q0']]}


def test_named_pattern2():
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('S = a b + | ();')
    f.close()
    h = handle_script_from_file(temp.name)
    assert cyk(h.g, 'a b')
    assert cyk(h.g, 'a b b b b')
    assert cyk(h.g, '')
    assert not cyk(h.g, 'a')


def test_named_pattern3():
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('S = a ? b;')
    f.close()
    h = handle_script_from_file(temp.name)
    assert cyk(h.g, 'a b')
    assert cyk(h.g, 'b')
    assert not cyk(h.g, 'a')
    assert not cyk(h.g, 'a b b')
    assert not cyk(h.g, 'a a b')


def test_named_pattern4():
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('S = (a b)* | c;')
    f.close()
    h = handle_script_from_file(temp.name)
    assert cyk(h.g, 'a b')
    assert cyk(h.g, 'a b a b')
    assert cyk(h.g, 'c')
    assert not cyk(h.g, 'a')
    assert not cyk(h.g, 'a b b')
    assert not cyk(h.g, 'a a b')
    assert not cyk(h.g, 'a b c')


def test_select_exists(capsys):
    path = os.path.dirname(__file__) + '/resources'
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('connect to [{}];\n'
            'S = a b | a C;'
            'C = S b;'
            'select exists u from [graph.txt] where (u) - S -> (_);'.format(path + '/test_dir'))
    f.close()
    h = handle_script_from_file(temp.name)
    assert capsys.readouterr().out == 'True\n'


def test_select_exists2(capsys):
    path = os.path.dirname(__file__) + '/resources'
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('connect to [{}];\n'
            'S = a b | a C;'
            'C = S b;'
            'select exists u from [graph.txt] where (_) - S -> (u);'.format(path + '/test_dir'))
    f.close()
    h = handle_script_from_file(temp.name)
    assert capsys.readouterr().out == 'True\n'


def test_select_exists3(capsys):
    path = os.path.dirname(__file__) + '/resources'
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('connect to [{}];\n'
            'S = a b | a C;'
            'C = S b;'
            'select exists (u, v) from [graph.txt] where (u) - S -> (v);'.format(path + '/test_dir'))
    f.close()
    h = handle_script_from_file(temp.name)
    assert capsys.readouterr().out == 'True\n'


def test_select_exists4(capsys):
    path = os.path.dirname(__file__) + '/resources'
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('connect to [{}];\n'
            'S = a b | a C;'
            'C = S b;'
            'select exists (u, v) from [graph.txt] where (u.ID = 1) - S -> (v);'.format(path + '/test_dir'))
    f.close()
    h = handle_script_from_file(temp.name)
    assert capsys.readouterr().out == 'True\n'


def test_select_exists5(capsys):
    path = os.path.dirname(__file__) + '/resources'
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('connect to [{}];\n'
            'S = a b | a C;'
            'C = S b;'
            'select exists (u, v) from [graph.txt] where (u.ID = 1) - S -> (v.ID = 3);'.format(path + '/test_dir'))
    f.close()
    h = handle_script_from_file(temp.name)
    assert capsys.readouterr().out == 'True\n'


def test_select_exists6(capsys):
    path = os.path.dirname(__file__) + '/resources'
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('connect to [{}];\n'
            'S = a b | a C;'
            'C = S b;'
            'select exists (u, v) from [graph.txt] where (u.ID = 1) - S -> (v.ID = 0);'.format(path + '/test_dir'))
    f.close()
    h = handle_script_from_file(temp.name)
    assert capsys.readouterr().out == 'False\n'


def test_select_exists7(capsys):
    path = os.path.dirname(__file__) + '/resources'
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('connect to [{}];\n'
            'S = a S| ();'
            'select exists (u, v) from [graph.txt] where (u.ID = 1) - S b b b -> (v.ID = 3);'.format(path + '/test_dir'))
    f.close()
    h = handle_script_from_file(temp.name)
    assert capsys.readouterr().out == 'True\n'


def test_select_exists8(capsys):
    path = os.path.dirname(__file__) + '/resources'
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('connect to [{}];\n'
            'S = a S| ();'
            'select exists (u, v) from [graph.txt] where (u.ID = 1) - S b b -> (v.ID = 3);'.format(path + '/test_dir'))
    f.close()
    h = handle_script_from_file(temp.name)
    assert capsys.readouterr().out == 'False\n'


def test_select_exists9(capsys):
    path = os.path.dirname(__file__) + '/resources'
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('connect to [{}];\n'
            'S = a S | ();'
            'select exists (u, v) from [graph.txt] where (u.ID = 1) - S b b -> (v.ID = 3);'
            'S = a S b;'
            'select exists (u, v) from [graph.txt] where (u.ID = 1) - S b b -> (v.ID = 3);'.format(path + '/test_dir'))
    f.close()
    h = handle_script_from_file(temp.name)
    assert capsys.readouterr().out == 'False\nTrue\n'


def test_select_exists10(capsys):
    path = os.path.dirname(__file__) + '/resources'
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('connect to [{}];'
            'S = a S | ();'
            'select exists (u, v) from [graph.txt] where (u.ID = 1) - S c c c -> (v.ID = 3);'
            'connect to [{}];'
            'select exists (u, v) from [graph.txt] where (u.ID = 1) - S c c c -> (v.ID = 3);'.format(path + '/test_dir', path + '/test_dir2'))
    f.close()
    h = handle_script_from_file(temp.name)
    assert capsys.readouterr().out == 'False\nTrue\n'
