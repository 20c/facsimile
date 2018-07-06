
import filecmp
import imp
import os
import pytest
import sys

import facsimile
from facsimile.base import Facsimile
import munge
from proj0 import Proj0
from util import mk_proj
import util


def obj(release_environment, **kwargs):
    return mk_proj(Proj0, release_environment, **kwargs)

def test_state_nomod():
    fax = obj('beta', version="0.3.0")
    fax.run()
    assert fax.state
    assert isinstance(fax.state.passwd(), dict)
    assert isinstance(fax.state.instances(), dict)
    assert isinstance(fax.state.tree(), dict)

def test_state():
    fax = obj('beta', version="0.4.0")
    fax.run()
    assert fax.state
    assert os.path.join(util.top_state_dir, fax.name, 'beta') == fax.state_dir
    #assert os.path.join(util.top_parent_dir, "beta", "state.json") == fax.state.state_file
    assert isinstance(fax.state.passwd(), dict)
    assert 1 == len(fax.state.passwd())
    assert fax.state.passwd()['proj0']
    assert isinstance(fax.state.instances(), dict)
    assert isinstance(fax.state.tree(), dict)

def test_write():
    fax = obj('beta', version="0.4.0")
    fax.run()
    assert os.path.exists(os.path.join(fax.state.state_file))
    data = fax.codec.load(open(fax.state.state_file))
    assert data == fax.state.state

    fax = obj('beta', version="0.4.0")
    fax.run()
    assert data == fax.state.state

