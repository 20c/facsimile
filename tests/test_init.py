
import filecmp
import imp
import os
import pytest
import sys

# XXX
import pprint

import facsimile
from facsimile.base import Facsimile

from proj0 import Proj0
from util import mk_proj


def obj(release_environment, **kwargs):
    return mk_proj(Proj0, release_environment, **kwargs)

def test_init_empty():
    with pytest.raises(NotImplementedError):
        fax = Facsimile()


def test_init_main_empty():
    assert os.EX_USAGE == facsimile.main(Facsimile, [], run=False)


def test_init_main_name():
    assert 0 == facsimile.main(Facsimile, ['beta'], run=False)


def test_init_main_version():
    assert 0 == facsimile.main(Facsimile, ['beta', '1.0.0'], run=False)


def test_init_dict():
    opt = {
        'name': 'test',
        'release_environment': 'test',
        'dry_run': True
        }
    fax = Facsimile(**opt)
    assert True == fax.dry_run


def test_init_debuginfo():
    opt = {
        'name': 'test',
        'release_environment': 'test',
        'debuginfo': True
        }
    fax = Facsimile(**opt)
    assert True == fax.with_debuginfo


def test_top_dir_from_class():
    fax = obj(release_environment="beta")
    assert hasattr(fax, 'top_dir')


def test_top_dir_opt():
    fax = obj(release_environment="beta", top_dir='TOPDIR')
    assert hasattr(fax, 'top_dir')
    assert 'TOPDIR' == fax.top_dir

def test_stage_only():
    fax = obj(release_environment="beta", only='checkout')
    assert 0 == fax.stage_start
    assert 1 == fax.stage_end

def test_stage_start():
    fax = obj(release_environment="beta", start='build')
    assert 1 == fax.stage_start
    assert 4 == fax.stage_end

def test_stage_end():
    fax = obj(release_environment="beta", end='build')
    assert 0 == fax.stage_start
    assert 2 == fax.stage_end

def test_stage_only_nonexistant():
    with pytest.raises(ValueError):
        fax = obj(release_environment="beta", only='nonexistant')

def test_devel():
    fax = obj(release_environment="beta", devel=True)
    assert True == fax.is_devel

def test_src_dir():
    src_dir='nonexistant'
    assert False == os.path.exists(src_dir)

    fax = obj(release_environment="beta", devel=False, src_dir=src_dir)
    assert True == fax.is_devel
    assert 'nonexistant' == fax.src_dir

    # make sure gitcheckout does not populate dir
    fax.git_checkout('')
    assert False == os.path.exists(src_dir)

    # error define_dir does not exist
    with pytest.raises(IOError):
        fax.run()

def test_summary():
    fax = obj(release_environment="beta", src_dir='none', dry_run=True)
    fax.print_summary()

def test_get_defined_targets():
    fax = obj(release_environment="beta")
    fax.run()
    assert ['gateway'] == fax.get_defined_targets()

def test_deployment_list():
    fax = obj(release_environment="beta")
    fax.run()
    assert set(['localhost']) == fax.deployment_set('gateway')



