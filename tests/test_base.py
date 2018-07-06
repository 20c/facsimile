
import filecmp
import imp
import os
import pytest
import sys

import facsimile
from facsimile.base import Base

class Empty(Base):
    name='empty'
    release_environment='instance'
    pass


def test_init():
    with pytest.raises(NotImplementedError):
        fax = Base()


def test_init_main():
    assert os.EX_USAGE == facsimile.main(Base, [], run=False)


def test_init_Empty():
    with pytest.raises(NotImplementedError):
        Empty()

