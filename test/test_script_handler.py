import tempfile

from src.script_handler import *
from src.cyk import cyk


def run_script(s):
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write(s)
    f.close()
    return handle_script_from_file(temp.name)


def test_list_all_graphs(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'list all graphs;'.format(path + '/test_dir'))
    lines = open(path + '/script_out.txt').read()
    assert capsys.readouterr().out == lines


def test_named_pattern(capsys):
    path = os.path.dirname(__file__) + '/resources'
    h = run_script('connect to [{}];\n'
                   'S = a S b S | ();'.format(path + '/test_dir'))
    assert h.g.rules == {'Q0': [['a', 'S', 'b', 'S'], ['eps']], 'S': [['Q0']]}


def test_named_pattern2():
    h = run_script('S = a b + | ();')
    assert cyk(h.g, 'a b')
    assert cyk(h.g, 'a b b b b')
    assert cyk(h.g, '')
    assert not cyk(h.g, 'a')


def test_named_pattern3():
    h = run_script('S = a ? b;')
    assert cyk(h.g, 'a b')
    assert cyk(h.g, 'b')
    assert not cyk(h.g, 'a')
    assert not cyk(h.g, 'a b b')
    assert not cyk(h.g, 'a a b')


def test_named_pattern4():
    h = run_script('S = (a b)* | c;')
    assert cyk(h.g, 'a b')
    assert cyk(h.g, 'a b a b')
    assert cyk(h.g, 'c')
    assert not cyk(h.g, 'a')
    assert not cyk(h.g, 'a b b')
    assert not cyk(h.g, 'a a b')
    assert not cyk(h.g, 'a b c')


def test_select_exists(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C;'
               'C = S b;'
               'select exists u from [graph.txt] where (u) - S -> (_);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == 'True\n'


def test_select_exists2(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C;'
               'C = S b;'
               'select exists u from [graph.txt] where (_) - S -> (u);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == 'True\n'


def test_select_exists3(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C;'
               'C = S b;'
               'select exists (u, v) from [graph.txt] where (u) - S -> (v);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == 'True\n'


def test_select_exists4(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C;'
               'C = S b;'
               'select exists (u, v) from [graph.txt] where (u.ID = 1) - S -> (v);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == 'True\n'


def test_select_exists5(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C;'
               'C = S b;'
               'select exists (u, v) from [graph.txt] where (u.ID = 1) - S -> (v.ID = 3);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == 'True\n'


def test_select_exists6(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C;'
               'C = S b;'
               'select exists (u, v) from [graph.txt] where (u.ID = 1) - S -> (v.ID = 0);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == 'False\n'


def test_select_exists7(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a S| ();'
               'select exists (u, v) from [graph.txt] where (u.ID = 1) - S b b b -> (v.ID = 3);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == 'True\n'


def test_select_exists8(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a S| ();'
               'select exists (u, v) from [graph.txt] where (u.ID = 1) - S b b -> (v.ID = 3);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == 'False\n'


def test_select_exists9(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a S | ();'
               'select exists (u, v) from [graph.txt] where (u.ID = 1) - S b b -> (v.ID = 3);'
               'S = a S b;'
               'select exists (u, v) from [graph.txt] where (u.ID = 1) - S b b -> (v.ID = 3);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == 'False\nTrue\n'


def test_select_exists10(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];'
               'S = a S | ();'
               'select exists (u, v) from [graph.txt] where (u.ID = 1) - S c c c -> (v.ID = 3);'
               'connect to [{}];'
               'select exists (u, v) from [graph.txt] where (u.ID = 1) - S c c c -> (v.ID = 3);'.format(path + '/test_dir', path + '/test_dir2'))
    assert capsys.readouterr().out == 'False\nTrue\n'


def test_select_count(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C;'
               'C = S b;'
               'select count u from [graph.txt] where (u) - S -> (_);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == '3\n'


def test_select_count2(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C;'
               'C = S b;'
               'select count u from [graph.txt] where (_) - S -> (u);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == '2\n'


def test_select_count3(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C;'
               'C = S b;'
               'select count (u, v) from [graph.txt] where (u) - S -> (v);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == '6\n'


def test_select_count4(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C;'
               'C = S b;'
               'select count (u, v) from [graph.txt] where (u.ID = 1) - S -> (v);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == '2\n'


def test_select_count5(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C;'
               'C = S b;'
               'select count (u, v) from [graph.txt] where (u.ID = 1) - S -> (v.ID = 3);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == '1\n'


def test_select_count6(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C;'
               'C = S b;'
               'select count (u, v) from [graph.txt] where (u.ID = 1) - S -> (v.ID = 0);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == '0\n'


def test_select_count7(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a S| ();'
               'select count (u, v) from [graph.txt] where (u.ID = 1) - S b b b -> (v.ID = 3);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == '1\n'


def test_select_count8(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a S | ();'
               'select count (u, v) from [graph.txt] where (u.ID = 1) - S b b -> (v.ID = 3);'
               'S = a S b;'
               'select count (u, v) from [graph.txt] where (u.ID = 1) - S b b -> (v.ID = 3);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == '0\n1\n'


def test_select_count9(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];'
               'S = a S | ();'
               'select count u from [graph.txt] where (u.ID = 1) - S c c c -> (v.ID = 3);'
               'connect to [{}];'
               'select count u from [graph.txt] where (u) - S c c c -> (v.ID = 3);'.format(path + '/test_dir', path + '/test_dir2'))
    assert capsys.readouterr().out == '0\n3\n'


def test_select(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C;'
               'C = S b;'
               'select u from [graph.txt] where (u) - S -> (_);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == '[0, 1, 2]\n'


def test_select2(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C;'
               'C = S b;'
               'select u from [graph.txt] where (_) - S -> (u);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == '[2, 3]\n'


def test_select3(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C;'
               'C = S b;'
               'select (u, v) from [graph.txt] where (u) - S -> (v);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == '[(0, 2), (0, 3), (1, 2), (1, 3), (2, 2), (2, 3)]\n'


def test_select4(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C;'
               'C = S b;'
               'select (u, v) from [graph.txt] where (u.ID = 1) - S -> (v);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == '[(1, 2), (1, 3)]\n'


def test_select5(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C;'
               'C = S b;'
               'select (u, v) from [graph.txt] where (u.ID = 1) - S -> (v.ID = 3);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == '[(1, 3)]\n'


def test_select6(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C;'
               'C = S b;'
               'select (u, v) from [graph.txt] where (u.ID = 1) - S -> (v.ID = 0);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == '[]\n'


def test_select7(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a S | ();'
               'select (u, v) from [graph.txt] where (u.ID = 1) - S b b -> (v.ID = 3);'
               'S = a S b;'
               'select (u, v) from [graph.txt] where (u.ID = 1) - S b b -> (v.ID = 3);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == '[]\n[(1, 3)]\n'


def test_select8(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];'
               'S = a S | ();'
               'select u from [graph.txt] where (u.ID = 1) - S c c c -> (v.ID = 3);'
               'connect to [{}];'
               'select u from [graph.txt] where (u) - S c c c -> (v.ID = 3);'.format(path + '/test_dir', path + '/test_dir2'))
    assert capsys.readouterr().out == '[]\n[0, 1, 2]\n'


def test_select9(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];'
               'S = a S | ();'
               'select u from [graph.txt] where (u.ID = 1) - a ? c + -> (v.ID = 3);'
               'connect to [{}];'
               'select u from [graph.txt] where (u) - a ? c + -> (v.ID = 3);'.format(path + '/test_dir', path + '/test_dir2'))
    assert capsys.readouterr().out == '[]\n[1, 2, 3]\n'


def test_select10(capsys):
    path = os.path.dirname(__file__) + '/resources'
    run_script('connect to [{}];\n'
               'S = a b | a C | ();'
               'C = S b;'
               'select u from [graph.txt] where (u) - S C -> (v.ID = 2);'.format(path + '/test_dir'))
    assert capsys.readouterr().out == '[0, 1, 2, 3]\n'
