""" Test for RapidPeptidesGenerator.py"""
import pytest
from .context import rpg
from rpg import RapidPeptidesGenerator

def test_restricted_float(capsys):
    """Test function 'restricted_float(mc_val)'"""
    # Error test
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        RapidPeptidesGenerator.restricted_float(-10)
    _, err = capsys.readouterr()
    assert err == "Value Error: miscleavage value should be between 0 and "\
                  "100.\n"
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        RapidPeptidesGenerator.restricted_float("z")
    _, err = capsys.readouterr()
    assert err == "Type Error: miscleavage value should be a float between"\
                  " 0 and 100.\n"
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    # Normal test
    assert RapidPeptidesGenerator.restricted_float(3) == 3.0

def test_restricted_enzyme_id(capsys):
    """Test function 'restricted_enzyme_id(enz_id)'"""
    # Error test
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        RapidPeptidesGenerator.restricted_enzyme_id(-10)
    _, err = capsys.readouterr()
    assert err == "Input Error: id -10 does not correspond to any enzyme. Use"\
                  " -l to get enzyme ids.\n"
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        RapidPeptidesGenerator.restricted_enzyme_id("z")
    _, err = capsys.readouterr()
    assert err == "Input Error: id z does not correspond to any enzyme. Use"\
                  " -l to get enzyme ids.\n"
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    # Normal test
    assert RapidPeptidesGenerator.restricted_enzyme_id(3) == "3"
    # Normal test
    assert RapidPeptidesGenerator.restricted_enzyme_id("asp-n") == "asp-n"

def test_restricted_int(capsys):
    """Test function 'restricted_int(mc_val)'"""
    # Error test
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        RapidPeptidesGenerator.restricted_int(-10)
    _, err = capsys.readouterr()
    assert err == "Value Error: miscleavage value should be greater then 0.\n"
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        RapidPeptidesGenerator.restricted_int("z")
    _, err = capsys.readouterr()
    assert err == "Type Error: miscleavage value should be an integer.\n"
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    # Normal test
    assert RapidPeptidesGenerator.restricted_int(3) == 3

def test_list_enzyme(capsys):
    """Test function 'list_enzyme()'
    This test should be run with empty user file
    """
    RapidPeptidesGenerator.list_enzyme()
    out, _ = capsys.readouterr()
    assert out == "1: Arg-C\n2: Asp-N\n3: BNPS-Skatole\n4: Bromelain\n5: Casp"\
    "ase-1\n6: Caspase-2\n7: Caspase-3\n8: Caspase-4\n9: Caspase-5\n10: Caspa"\
    "se-6\n11: Caspase-7\n12: Caspase-8\n13: Caspase-9\n14: Caspase-10\n15: C"\
    "hymotrypsin-high\n16: Chymotrypsin-low\n17: Clostripain\n18: CNBr\n19: E"\
    "nterokinase\n20: Factor-Xa\n21: Ficin\n22: Formic-acid\n23: Glu-C\n24: G"\
    "lutamyl-endopeptidase\n25: Granzyme-B\n26: Hydroxylamine\n27: Iodosobenz"\
    "oic-acid\n28: Lys-C\n29: Lys-N\n30: Neutrophil-elastase\n31: NTCB\n32: P"\
    "apain\n33: Pepsin-pH1.3\n34: Pepsin-pH>=2\n35: Proline-endopeptidase\n36"\
    ": Proteinase-K\n37: Staphylococcal-peptidase-I\n38: Thermolysin\n39: Thr"\
    "ombin\n40: Thrombin-SG\n41: Tobacco-Etch-Virus\n42: Trypsin\n43: Asp-N "\
    "Endopeptidase\n44: ProAlanase\n45: Elastase\n"

def test_create_enzymes_to_use(capsys):
    """Test function 'create_enzymes_to_use(enzymes, miscleavage)'"""
    enzymes = [23, 31, 29]
    miscleavage = [1.1, 20]
    res = RapidPeptidesGenerator.create_enzymes_to_use(enzymes, miscleavage)
    assert res.__repr__() == "[Id: 23\nName: Glu-C\nRatio Miscleavage: 1.10%"\
                             "\nRules: [index=0\namino_acid=D\ncleavage=True"\
                             "\nposition=1\n, index=0\namino_acid=E\ncleavage"\
                             "=True\nposition=1\n]\n, Id: 31\nName: NTCB\nRat"\
                             "io Miscleavage: 20.00%\nRules: [index=0\namino_"\
                             "acid=C\ncleavage=True\nposition=0\n]\n, Id: 29"\
                             "\nName: Lys-N\nRatio Miscleavage: 0.00%\nRules:"\
                             " [index=0\namino_acid=K\ncleavage=True\npositio"\
                             "n=0\n]\n]"
    enzymes = [23, 31]
    miscleavage = [1.1, 20, 40]
    res = RapidPeptidesGenerator.create_enzymes_to_use(enzymes, miscleavage)
    _, err = capsys.readouterr()
    assert err == "Warning: Too much miscleavage values. Last values will "\
                  "be ignored.\n"
    assert res.__repr__() == "[Id: 23\nName: Glu-C\nRatio Miscleavage: 1.10%"\
                             "\nRules: [index=0\namino_acid=D\ncleavage=True"\
                             "\nposition=1\n, index=0\namino_acid=E\ncleavage"\
                             "=True\nposition=1\n]\n, Id: 31\nName: NTCB\nRat"\
                             "io Miscleavage: 20.00%\nRules: [index=0\namino_"\
                             "acid=C\ncleavage=True\nposition=0\n]\n]"
