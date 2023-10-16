# pylint: disable=missing-module-docstring,missing-function-docstring

import pytest


@pytest.mark.parametrize("option", ["-od", "--output-dir"])
def test_debug_logs(cli_runner, csv_file, tmpdir, option):
    csv = csv_file("sample.csv")
    ret = cli_runner(csv, "-d", option, tmpdir, "-wk", "42")

    assert f"{tmpdir}/001_2023_week_42_RdYlGn_r_heatmap_" in ret.stderr
