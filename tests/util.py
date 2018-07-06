
import filecmp
import imp
import os
import pytest
import shutil
import sys

import facsimile
from facsimile.base import Facsimile


this_dir = os.path.dirname(__file__)
data_dir = os.path.join(this_dir, 'data')
top_parent_dir = os.path.join(this_dir, 'gen')
top_state_dir = os.path.join(this_dir, 'state')

class ProjBase(Facsimile):
    # required for subclasses
    required_attrs=('name', 'TEST_CURVER')


    def __init__(self, **kwargs):

        for attr in self.required_attrs:
            if not hasattr(self, attr):
                raise Exception("required attr %s not set on object" % attr)

        if 'debug' not in kwargs:
            kwargs['debug'] = True
        if 'clean' not in kwargs:
            kwargs['clean'] = True
        if 'state_dir' not in kwargs:
            kwargs['state_dir'] = os.path.join(top_state_dir, self.name)

        self.repo = os.path.join(this_dir, 'data', self.name, 'repo')
        self.top_dir = os.path.join(top_parent_dir, 'tmp', self.name)
        super(ProjBase, self).__init__(**kwargs)

def mk_proj(cls, release_environment, **kwargs):
    kwargs['release_environment'] = release_environment
    if not 'version' in kwargs:
        kwargs['version'] = cls.TEST_CURVER

    fax = cls(**kwargs)
    return fax



