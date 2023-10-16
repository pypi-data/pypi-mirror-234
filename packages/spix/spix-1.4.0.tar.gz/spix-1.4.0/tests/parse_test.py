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

import pytest

import spix

DATADIR = pathlib.Path(__file__).parent / "parse_data"
TESTFILES = list(path.stem for path in DATADIR.glob("*.tex"))


@pytest.mark.parametrize("texname", TESTFILES)
def test_parse(texname):
    """Test that snippets in tex files are correctly extracted."""

    # When python3.7 and python3.8 are outdated, we can replace the two
    # following "with" with a single "with" with parentheses
    with open((DATADIR / texname).with_suffix(".tex"), encoding="utf8") as texfile:
        with open(
            (DATADIR / texname).with_suffix(".snippets"), encoding="utf8"
        ) as snippetfile:
            assert list(spix.parse_lines(texfile.readlines())) == list(
                line.strip().replace(r"\n", "\n") for line in snippetfile.readlines()
            )
