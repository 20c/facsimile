
import filecmp
import imp
import os
import pytest
import shutil
import sys

import util


@pytest.yield_fixture(autouse=True)
def clean_gen():
    gen_tmp = os.path.join(util.top_parent_dir, 'tmp')
    if os.path.exists(gen_tmp):
        shutil.rmtree(gen_tmp)
    yield
    #assert "RM" == util.top_parent_dir

