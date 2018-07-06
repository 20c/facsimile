
import filecmp
import imp
import os
import pytest
import sys

import facsimile
from facsimile.base import Facsimile
from facsimile.install import Install
import fstest
from proj0 import Proj0
import util

# TODO
#  - test dir type

def mk_fax(release_environment, **kwargs):
    return util.mk_proj(Proj0, release_environment, **kwargs)

@pytest.fixture
def fax():
    return mk_fax('beta')

@pytest.fixture
def install(fax):
    return Install(fax)

def test_init():
    fax = mk_fax('beta')

def test_os_path_transform(install):
    path = 'test/file'
    path_win = 'test\\file'

    assert path == install.os_path_transform(path, '/')
    assert path_win == install.os_path_transform(path_win, '/')

    assert path == install.os_path_transform(path, '\\')
    assert path == install.os_path_transform(path_win, '\\')

def test_transform(install):
    path = 'test/file'
    src_dir = '$SRCDIRNAME$'

    tr_list = [
        ('$SRC_DIR$', 'SRC_DIR'),
        ('$DEPLOY_DIR$', 'DEPLOY_DIR'),
        ('$BUILD_DIR$', 'BUILD_DIR'),
    ]

    assert 'SRC_DIR' == install.transform(tr_list, '$SRC_DIR$')
    assert '$SRC_DIR' == install.transform(tr_list, '$$SRC_DIR$')
    assert 'SRC_DIR$' == install.transform(tr_list, '$SRC_DIR$$')
    assert '$SRC_DIR$' == install.transform(tr_list, '$$SRC_DIR$$')

    assert 'BUILD_DIR' == install.transform(tr_list, '$BUILD_DIR$')
    assert '$BUILD_DIR' == install.transform(tr_list, '$$BUILD_DIR$')
    assert 'BUILD_DIR$' == install.transform(tr_list, '$BUILD_DIR$$')
    assert '$BUILD_DIR$' == install.transform(tr_list, '$$BUILD_DIR$$')

    assert 'DEPLOY_DIR' == install.transform(tr_list, '$DEPLOY_DIR$')
    assert '$DEPLOY_DIR' == install.transform(tr_list, '$$DEPLOY_DIR$')
    assert 'DEPLOY_DIR$' == install.transform(tr_list, '$DEPLOY_DIR$$')
    assert '$DEPLOY_DIR$' == install.transform(tr_list, '$$DEPLOY_DIR$$')

    assert '$NOPE$' == install.transform(tr_list, '$NOPE$')

def test_resolve_dst(install):
    dst_dir = '/test/dir'

    assert '/test/dir/relative/file' == install.resolve_dst(dst_dir, 'relative/file')
    assert '/test/dir/absolute' == install.resolve_dst(dst_dir, '/this/is/absolute')

def test_install(fax):
    fax.run()

    expected_dir = os.path.join(util.data_dir, 'proj0', 'expected.beta', 'proj0')

    print fax.release_dir
    fstest.cmpdirs(expected_dir, fax.release_dir)

