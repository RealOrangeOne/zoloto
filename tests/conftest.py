import os
from tempfile import mkstemp

import pytest


@pytest.fixture
def make_temp_file(request):
    temp_file = None

    def clean_temp_file():
        nonlocal temp_file
        if temp_file is not None:
            os.remove(temp_file)

    def _make_temp_file(*args, **kwargs):
        nonlocal temp_file
        handle, temp_file = mkstemp(*args, **kwargs)
        os.close(handle)
        return temp_file

    request.addfinalizer(clean_temp_file)
    return _make_temp_file
