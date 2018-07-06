
import filecmp
import imp
import os
import pytest
import sys

import facsimile
from facsimile.base import Facsimile
from venv0 import Venv0
from util import mk_proj, data_dir


def obj(release_environment, **kwargs):
    if 'src_dir' not in kwargs:
        kwargs['src_dir'] = os.path.join(data_dir, 'venv0', 'repo')
    return mk_proj(Venv0, release_environment, **kwargs)

def test_init():
    fax = obj('beta', just_summary=True)

def test_no_src():
    fax = obj('beta', src_dir='nonexistant')
    with pytest.raises(IOError):
        fax.make_virtualenv()

    fax = obj('beta', summary=True)
    with pytest.raises(IOError):
        fax.make_virtualenv(src_dir='noneeistant')

def test_venv_fail():
    fax = obj('beta', end="checkout")
    # run to checkout src
    fax.run()
    with pytest.raises(RuntimeError):
        fax.make_virtualenv(req_file='noneeistant')

def test_venv_fail_cleanup():
    fax = obj('beta', end="checkout")
    # run to checkout src
    fax.run()
    with pytest.raises(RuntimeError):
        fax.make_virtualenv(req_file='noneeistant')

def SKIP_test_pip_fail():
    # FIXME - need to make a broken package for this now
    fax = obj('beta')
    fax.run()

