# pylint: disable=missing-module-docstring,missing-function-docstring

import pytest

from heatmap_cli import __version__


@pytest.mark.parametrize("option", ["-V", "--version"])
def test_version(cli_runner, option):
    ret = cli_runner(option)
    assert f"heatmap_cli {__version__}" in ret.stdout
