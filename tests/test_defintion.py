
import filecmp
import imp
import os
import pytest
import sys

import facsimile
from facsimile.base import Facsimile

from proj0 import Proj0
from util import mk_proj


def obj(release_environment, **kwargs):
    kwargs['clean'] = True
    return mk_proj(Proj0, release_environment, **kwargs)

def test_def_list():
    fax = obj('beta')
    fax.run()
    assert ['facsimile', fax.name, 'beta'] == fax.defined.def_list()

def test_def_list_sub():
    fax = obj('dev.dev0')
    fax.run()
    assert ['facsimile', fax.name, 'dev', 'dev0'] == fax.defined.def_list()

def test_def_file_not_found():
    fax = obj('nonexistant')
    with pytest.raises(IOError):
        fax.defined.def_file_list()

def test_def_file_list_before_checkout():
    # version to non existant since clean doesn't occur until checkout
    fax = obj('beta', version='0.0.0')
    with pytest.raises(IOError):
        fax.defined.def_file_list()

def test_def_file_list():
    fax = obj('beta', only='checkout')
    fax.run()
    data_list = fax.defined.def_file_list()
    assert ['facsimile.json', 'beta.json'] == [os.path.basename(t[1]) for t in data_list]
    for t in data_list:
        assert 'Json' == t[0].__name__

def test_def_file_list_sub():
    fax = obj('dev.dev0', only='checkout')
    fax.run()
    data_list = fax.defined.def_file_list()
    assert ['facsimile.json', 'dev.json', 'dev0.json'] == [os.path.basename(t[1]) for t in data_list]

def test_def_file_load():
    fax = obj('dev.dev0')
    fax.run()

    assert "dev0-out" == fax.defined['home']
    assert "json" == fax.defined.data_ext

def test_def_readonly():
    fax = obj('dev.dev0')
    fax.run()

    with pytest.raises(TypeError):
        fax.defined['home'] = 'overwrite'
    assert "dev0-out" == fax.defined['home']

def test_def_readonly_del():
    fax = obj('dev.dev0')
    fax.run()

    with pytest.raises(TypeError):
        del fax.defined['home']
    assert "dev0-out" == fax.defined['home']

def test_def_data():
    fax = obj('dev.dev0')
    fax.run()

    data = fax.defined.data
    for (k, v) in fax.defined.iteritems():
        assert data[k] == v

def test_def_iter():
    fax = obj('dev.dev0')
    fax.run()
    for (k, v) in fax.defined.iteritems():
        assert fax.defined[k] == v

def test_def_len():
    fax = obj('dev.dev0')
    fax.run()
    assert 6 == len(fax.defined)

def test_modules_none():
    fax = obj('dev.dev0', version='0.3.0', end='checkout')
    fax.run()

    assert isinstance(fax.defined.modules(), list)
    assert 0 == len(fax.defined.modules())

def test_modules():
    fax = obj('dev.dev0')
    fax.run()

    assert isinstance(fax.defined.modules(), list)
    assert 1 == len(fax.defined.modules())

