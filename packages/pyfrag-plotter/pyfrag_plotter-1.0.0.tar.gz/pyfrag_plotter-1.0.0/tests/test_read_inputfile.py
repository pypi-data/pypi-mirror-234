import pytest
import pyfrag_plotter.input.read_inputfile as input_reader
from pyfrag_plotter.errors import PyFragInputError


def test_check_line_length_valid():
    line = "bondlength 1 2 1.5"
    input_key = "bondlength"
    limits = (3, 4)
    expected_output = ["bondlength", "1", "2", "1.5"]
    assert input_reader._check_line_length(line, input_key, limits) == expected_output


def test_check_line_length_invalid():
    line = "bondlength 1 2 3 4"
    input_key = "bondlength"
    limits = (3, 4)
    with pytest.raises(PyFragInputError, match="bondlength is not valid. Length of the bondlength not correct. Make sure to specify the correct format"):
        input_reader._check_line_length(line, input_key, limits)


def test_read_bondlength_line_no_bondlength():
    line = "bondlength 1 2"
    expected_output = (1, 2, 0.0)
    assert input_reader._read_bondlength_line(line) == expected_output


def test_read_bondlength_line_with_bondlength():
    line = "bondlength 1 2 1.5"
    expected_output = (1, 2, 1.5)
    assert input_reader._read_bondlength_line(line) == expected_output


def test_read_bondangle_line_no_angle():
    line = "angle 1 2"
    expected_output = (1, 2, 0.0)
    assert input_reader._read_bondangle_line(line) == expected_output


def test_read_bondangle_line_with_angle():
    line = "angle 1 2 120.0"
    expected_output = (1, 2, 120.0)
    assert input_reader._read_bondangle_line(line) == expected_output


def test_read_dihedral_angle_no_angle():
    line = "dihedral 1 2 3"
    expected_output = (1, 2, 3, 0.0)
    assert input_reader._read_dihedral_angle(line) == expected_output


def test_read_dihedral_angle_with_angle():
    line = "dihedral 1 2 3 45.0"
    expected_output = (1, 2, 3, 45.0)
    assert input_reader._read_dihedral_angle(line) == expected_output


def test_read_overlap_line_no_irrep():
    line = "overlap frag1 HOMO frag2 LUMO"
    expected_output = ("frag1", "HOMO", "frag2", "LUMO")
    assert input_reader._read_overlap_line(line) == expected_output


def test_read_overlap_line_with_irrep():
    line = "overlap S frag1 5 AA frag2 4"
    expected_output = ("S", "frag1", "5", "AA", "frag2", "4")
    assert input_reader._read_overlap_line(line) == expected_output


def test_read_population_line_two_fragments_two_MOs():
    line = "population frag1 HOMO"
    expected_output = ("frag1", "HOMO")
    assert input_reader._read_population_line(line) == expected_output


def test_read_population_line_two_fragments_one_MO():
    line = "population frag2 HOMO-1"
    expected_output = ("frag2", "HOMO-1")
    assert input_reader._read_population_line(line) == expected_output


def test_read_population_line_with_irrep():
    line = "population AA frag2 5"
    expected_output = ("AA", "frag2", "5")
    assert input_reader._read_population_line(line) == expected_output


def test_read_orbitalenergy_line_two_fragments_two_MOs():
    line = "orbitalenergy frag1 HOMO"
    expected_output = ("frag1", "HOMO")
    assert input_reader._read_orbitalenergy_line(line) == expected_output


def test_read_orbitalenergy_line_two_fragments_one_MO():
    line = "orbitalenergy frag1 HOMO-2"
    expected_output = ("frag1", "HOMO-2")
    assert input_reader._read_orbitalenergy_line(line) == expected_output


def test_read_orbitalenergy_line_with_irrep():
    line = "ORBITALENERGY AA frag2 5"
    expected_output = ("AA", "frag2", "5")
    assert input_reader._read_orbitalenergy_line(line) == expected_output


def test_read_vdd_line():
    line = "vdd 1 2 3 4 #A comment"
    expected_output = [1, 2, 3, 4]
    assert input_reader._read_vdd_line(line) == expected_output


def test_read_irrep_line():
    line = "  irrepOI        AA #Hello"
    expected_output = ["AA"]
    assert input_reader._read_irrep_line(line) == expected_output
