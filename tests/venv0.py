#!/usr/bin/env python

import filecmp
import imp
import os
import pytest
import sys

import facsimile
from facsimile.base import VirtualEnv

import util


class Venv0(util.ProjBase, VirtualEnv):
    name = 'venv0'

    # helpers for tests
    TEST_CURVER='0.4.0'

    def deploy(self):
        self.status_msg("deploying...")

if __name__ == '__main__':
    sys.exit(facsimile.main(Venv0))

