from __future__ import annotations

import pytest

from variables import Variables


@pytest.fixture(autouse=True)
def reset_variables_registry():
    """Reset the class-level global variable registry around every test.

    Both ``Variables`` and ``Compile`` mutate the class attribute
    ``Variables.memory`` as global compiler state. Tests must never leak
    variables between each other, so we clear it before and after.
    """
    Variables.memory = []
    yield
    Variables.memory = []