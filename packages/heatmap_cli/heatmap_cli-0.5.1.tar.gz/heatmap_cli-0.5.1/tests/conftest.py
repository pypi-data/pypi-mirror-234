# pylint: disable=missing-module-docstring,missing-function-docstring

import os
from pathlib import Path
from shutil import copyfile

import pytest
from scripttest import TestFileEnvironment

FIXTURE_PATH = Path(os.getcwd(), "tests", "fixtures")


# See https://stackoverflow.com/a/62055409
@pytest.fixture(autouse=True)
def _change_test_dir(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)


@pytest.fixture(autouse=True, name="csv_file")
def fixture_csv_file(tmpdir):
    def csv_file(filename):
        src = Path(FIXTURE_PATH, filename)
        des = Path(tmpdir, src.name)
        copyfile(src, des)
        return des

    return csv_file


@pytest.fixture(autouse=True, name="cli_runner")
def fixture_cli_runner(tmpdir):
    def cli_runner(*args):
        env = TestFileEnvironment(tmpdir / "scripttest")
        return env.run(
            "heatmap_cli", *args, cwd=tmpdir / "scripttest", expect_error=True
        )

    return cli_runner
