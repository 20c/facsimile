#!/usr/bin/env python

import filecmp
import imp
import os
import pytest
import sys

import facsimile
from facsimile.base import Facsimile

import util


class Proj0(util.ProjBase):
    name = 'proj0'

    # helpers for tests
    TEST_CURVER='0.6.0'

    def build(self):
        self.status_msg("building...")

    def deploy(self):
        self.status_msg("deploying...")

if __name__ == '__main__':
    sys.exit(facsimile.main(Proj0))

