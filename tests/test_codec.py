
import filecmp
import imp
import os
import pytest
import sys

import facsimile
import facsimile.codec
import munge
import munge.codec.all

from util import mk_proj
from proj0 import Proj0

has_codecs = [exts[0] for exts in munge.get_codecs().keys()]

def obj(release_environment, **kwargs):
    return mk_proj(Proj0, release_environment, **kwargs)

def test_codec_init():
    codecs = facsimile.codec.get_codecs()
    assert len(codecs)
    assert len(has_codecs) == len(codecs)

def TODO_test_add_codec():
    with pytest.raises(ValueError):
        facsimile.codec.add_codec(['json'], None)

def test_get_codec():
    for each in has_codecs:
        assert facsimile.codec.get_codec(each)

    assert None == facsimile.codec.get_codec('nonexistant')

def test_list_codecs():
    assert has_codecs == facsimile.codec.list_codecs()

def test_find_datafile():
    fax = obj("beta", end='checkout')
    fax.run()

    #assert "x" == fax.define_dir
    files = fax.find_datafile('facsimile', fax.define_dir)
    assert 1 == len(files)
    load = files[0]
    assert os.path.join(fax.define_dir, 'facsimile.json') == load[1]
    assert hasattr(load[0], 'load')

    data = load[0]().load(open(load[1]))
    assert data
    assert "facsimile" in data

def test_load_datafile():
    fax = obj("beta", end='checkout')
    fax.run()

    with pytest.raises(IOError):
        fax.load_datafile('nonexistant', fax.define_dir)

    # default value
    assert None == fax.load_datafile('nonexistant', fax.define_dir, default=None)
    assert 'DEFAULT' == fax.load_datafile('nonexistant', fax.define_dir, default='DEFAULT')

    data = fax.load_datafile('facsimile', fax.define_dir)
    assert data

    with pytest.raises(IOError):
        fax.load_datafile('facsimile', fax.define_dir, codecs={})

