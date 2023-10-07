"""Tests for sequence.py"""
import pytest
from .context import rpg
from rpg import core
from rpg import sequence

def test_peptide():
    """Test class 'Peptide'"""
    header = "fake_sequence"
    seq = "QWSDESDF"
    enz_name = "Pwet"
    aa_pka = core.AA_PKA_IPC
    aa_mass = core.AA_MASS_AVERAGE
    water_mass = core.WATER_MASS
    nb_peptide = 42
    pep0 = sequence.Peptide(header, seq, enz_name, aa_pka, aa_mass, water_mass,
                            nb_peptide)

    # Test function '__repr__()'
    assert pep0.__repr__() == "Original header: fake_sequence\nNo. peptide: "\
                              "42\nEnzyme: Pwet\nCleav. pos: 0\nPep. size: 8"\
                              "\nPep. mass: 1012.98488\npKa values from: IPC"\
                              "\nPep. pI: 2.91\nSequence: QWSDESDF\n"

    header = "fake_sequence"
    seq = "QWSDESDF"
    enz_name = "Pwet"
    aa_pka = core.AA_PKA_IPC
    aa_mass = core.AA_MASS_AVERAGE
    water_mass = core.WATER_MASS
    nb_peptide = 42
    pep1 = sequence.Peptide(header, seq, enz_name, aa_pka, aa_mass, water_mass, nb_peptide)

    header = "fake_sequence"
    seq = "QWSDESDW"
    enz_name = "Pwet"
    aa_pka = core.AA_PKA_IPC
    aa_mass = core.AA_MASS_AVERAGE
    water_mass = core.WATER_MASS
    nb_peptide = 42
    pep2 = sequence.Peptide(header, seq, enz_name, aa_pka, aa_mass, water_mass, nb_peptide)

    assert pep0 == pep1
    assert pep0 != pep2
    assert pep0 != 42

def test_sequence():
    """Test class 'Sequence'"""
    header = "fake_sequence"
    seq = "QWSDESDF"
    seq0 = sequence.Sequence(header, seq)

    # Test function '__repr__()'
    assert seq0.__repr__() == "Header: fake_sequence\nSequence: QWSDESDF\n"

    header = "fake_sequence"
    seq = "QWSDESDF"
    seq1 = sequence.Sequence(header, seq)

    header = "fake_sequdence"
    seq = "QWSDESDF"
    seq2 = sequence.Sequence(header, seq)

    header = "fake_sequence"
    seq = "QWSD>ESDF"
    seq3 = sequence.Sequence(header, seq)

    # Test function '__eq__()'
    assert seq0 == seq1
    assert seq0 != seq2
    assert seq0 != seq3
    assert seq0 != 42

def test_check_sequence(capsys):
    """ Test function 'check_sequence(seq)'"""
    # Correct one
    assert sequence.check_sequence("aiHZODHUoh") == "AIHZODHUOH"

    # Bad symbol
    with pytest.raises(ValueError) as pytest_wrapped_e:
        sequence.check_sequence("a%HZODHUoh")
    assert "amino acid \"%\" in A%HZODHUOH not "\
           "recognized." in str(pytest_wrapped_e.value)
