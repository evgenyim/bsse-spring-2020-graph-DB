import os
import tempfile

from antlr.antlr_parser import *


def test_read_from_file(capsys):
    str_path = os.path.dirname(__file__) + '/resources/antlr_test_1.txt'
    read_from_file(str_path)
    assert capsys.readouterr().out == 'Script is correct\n'


def test_read_from_file2(capsys):
    str_path = os.path.dirname(__file__) + '/resources/antlr_test_2.txt'
    read_from_file(str_path)
    assert capsys.readouterr().out == 'Script is correct\n'


def test_read_from_file3(capsys):
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('connect to [asdq];\n')
    f.close()
    read_from_file(temp.name)
    assert capsys.readouterr().out == 'Script is correct\n'


def test_read_from_file4(capsys):
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('list all graphs ;')
    f.close()
    read_from_file(temp.name)
    assert capsys.readouterr().out == 'Script is correct\n'


def test_read_from_file_select_stmt(capsys):
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('\select vs from [hello] where (vsa)'
            '- S * | v ? ->  (u.ID = 366);')
    f.close()
    read_from_file(temp.name)
    assert capsys.readouterr().out == 'Script is correct\n'


def test_read_from_file_named_pattern_stmt(capsys):
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, 'w')
    f.write('Nt = v + | ( u * | t ) ;')
    f.close()
    read_from_file(temp.name)
    assert capsys.readouterr().out == 'Script is correct\n'


def test_read_from_file_fails(capsys):
    temp = tempfile.NamedTemporaryFile()
    read_from_file(temp.name)
    f = open(temp.name, 'w')
    f.write('\select vs from [hello] where (Nsa)'
            '- S * | v ? ->  (u.ID = 366);')
    f.close()
    assert capsys.readouterr().out == 'Script is incorrect\n'