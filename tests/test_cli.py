
import filecmp
import functools
import imp
import os
import pytest
import sys

import facsimile
from facsimile import base
from facsimile import cli
from facsimile import facs
from facsimile.base import Base
from proj0 import Proj0


def test_parse_options():
    cls=Proj0
    (status, options) = cli.parse_options(cls, ['beta', cls.TEST_CURVER, '--write-codec=json'])
    assert 0 == status
    assert isinstance(options, dict)

    (status, options) = cli.parse_options(cls, ['beta', cls.TEST_CURVER, '--none-existant'])
    assert 2 == status
    assert isinstance(options, dict)

    # no release_environment
    (status, options) = cli.parse_options(cls, [])
    assert 64 == status
    assert isinstance(options, dict)

    # no version
    (status, options) = cli.parse_options(cls, ['beta'])
    assert 0 == status
    assert isinstance(options, dict)

def test_parse_options_usage():
    cls=Proj0
    (status, options) = cli.parse_options(cls, ['beta'], usage="usage")
    assert 0 == status
    assert isinstance(options, dict)

def test_codec_options():
    cls=Proj0
    (status, options) = cli.parse_options(cls, ['beta', cls.TEST_CURVER, '--write-codec=CODEC'])
    assert 0 == status
    inst = cli.instantiate(cls, options)
    assert 'CODEC' == inst.write_codec

def test_pop_first_arg():
    argv = ['project_name', 'release_environment', 'version']
    (release_environment, argv) = cli.pop_first_arg(argv)
    assert 'project_name' == release_environment
    assert ['release_environment', 'version'] == argv

    argv = ['--first-opt', 'project_name', 'release_environment', 'version']
    (release_environment, argv) = cli.pop_first_arg(argv)
    assert 'project_name' == release_environment
    assert ['--first-opt', 'release_environment', 'version'] == argv

    argv = ['project_name', 'release_environment', '--middle-opt', 'version']
    (release_environment, argv) = cli.pop_first_arg(argv)
    assert 'project_name' == release_environment
    assert ['release_environment', '--middle-opt', 'version'] == argv

    (release_environment, argv) = cli.pop_first_arg([])
    assert None == release_environment
    assert [] == argv

def test_get_cls():
    obj = facs.get_cls(None, {})
    assert base.Facsimile == obj
    assert 'facsimile' == obj.name

    obj = facs.get_cls('venv', {'class': 'VirtualEnv'})
    assert base.VirtualEnv == obj
    assert 'venv' == obj.name

# assert expected from both cli and facs mains
def assert_main(expected, cls, argv, run=True, run_facs=False):
    assert expected == cli.main(cls, argv, run=run)

    # TODO force run to False for facs testing until able to instantiate object correctly
    run=run_facs

    package_name = getattr(cls, 'name', cls.__name__)
    assert package_name
    argv.insert(0, package_name)
    assert argv
    assert expected == facs.main(argv, run=run)

def test_main_init():
    assert os.EX_USAGE == cli.main(Base, [], run=False)
    assert_main(os.EX_USAGE, Base, [], run=False)

def test_main_run():
    cls=Proj0
    assert_main(0, cls, ['beta', cls.TEST_CURVER, '--end=checkout'])

def test_main_info_options():
    cls=Proj0
    assert_main(0, cls, ['beta', cls.TEST_CURVER, '--summary'], run_facs=True)
    # needs define dir
    #assert 0 == facsimile.main(cls, ['beta', cls.TEST_CURVER, '--list-nodes'], run=False)

