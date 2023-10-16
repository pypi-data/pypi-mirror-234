# Copyright 2020-2022 Louis Paternault
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Tests"""

import pathlib
import subprocess
import sys

import pytest

import spix

BIN = spix.__file__
DATADIR = pathlib.Path(__file__).parent / "compile_data"
TESTFILES = list(path.stem for path in DATADIR.glob("*.tex"))


@pytest.mark.parametrize(
    "name", (name for name in TESTFILES if not name.startswith("error"))
)
def test_parse(name):
    """Test that snippets in tex files are correctly extracted."""
    # With suffix
    with open((DATADIR / name).with_suffix(".stdout"), encoding="utf8") as stdout:
        assert (
            subprocess.check_output(
                [sys.executable, BIN, (DATADIR / name).with_suffix(".tex")], text=True
            )
            == stdout.read()
        )

    # Without suffix
    with open((DATADIR / name).with_suffix(".stdout"), encoding="utf8") as stdout:
        assert (
            subprocess.check_output([sys.executable, BIN, DATADIR / name], text=True)
            == stdout.read()
        )


@pytest.mark.parametrize(
    "name", (name for name in TESTFILES if not name.startswith("error"))
)
def test_dryrun(name):
    """Test that snippets in tex files are correctly extracted."""
    with open((DATADIR / name).with_suffix(".dryrun"), encoding="utf8") as stdout:
        assert (
            subprocess.check_output(
                [
                    sys.executable,
                    BIN,
                    "--dry-run",
                    (DATADIR / name).with_suffix(".tex"),
                ],
                text=True,
            )
            == stdout.read()
        )


@pytest.mark.parametrize(
    "name",
    [name for name in TESTFILES if name.startswith("error")]
    + ["error_does_not_exist.tex"],
)
def test_errors(name):
    """Test that errors are raised."""
    assert subprocess.call([sys.executable, BIN, DATADIR / name]) == 1
