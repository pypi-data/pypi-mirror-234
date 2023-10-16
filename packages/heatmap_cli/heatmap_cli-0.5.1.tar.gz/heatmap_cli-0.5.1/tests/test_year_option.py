# pylint: disable=missing-module-docstring,missing-function-docstring

import pytest


@pytest.mark.parametrize("option", ["-yr", "--year"])
def test_debug_logs(cli_runner, csv_file, option):
    csv = csv_file("sample.csv")
    ret = cli_runner(csv, "-d", option, "2023")
    assert "year=2023" in ret.stderr


def test_raise_exception_no_data_from_csv(cli_runner, csv_file):
    csv = csv_file("sample.csv")
    ret = cli_runner(csv, "-yr", "2099")
    assert "error: no data extracted from csv file" in ret.stderr
