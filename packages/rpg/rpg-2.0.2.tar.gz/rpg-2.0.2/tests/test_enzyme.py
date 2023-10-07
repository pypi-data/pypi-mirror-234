"""Tests for digest.py"""
import pytest
import sys
from pathlib import Path
from .context import rpg
from rpg import enzyme
from rpg import rule
from rpg.enzymes_definition import AVAILABLE_ENZYMES

def test_enzyme(tmp_path):
    """Test class 'Enzyme'"""
    # First enzyme: cut after D not precedeed by S
    dict_rule = {}
    rule_txt = "(D,)"
    dict_rule[rule_txt] = True
    exc_txt = "(S)(D,)"
    dict_rule[exc_txt] = False
    all_rules = rule.create_rules(dict_rule)
    enz0 = enzyme.Enzyme(-1, "fake_enzyme1", all_rules)

    # Test function '__repr__()'
    res = enz0.__repr__()
    assert res == "Id: -1\nName: fake_enzyme1\nRatio Miscleavage: 0.00%\nRule"\
                  "s: [index=0\namino_acid=D\ncleavage=True\nposition=1\n\tin"\
                  "dex=-1\n\tamino_acid=S\n\tcleavage=False\n\tposition=-1\n]"\
                  "\n"

    dict_rule = {}
    rule_txt = "(D,)"
    dict_rule[rule_txt] = True
    exc_txt = "(S)(D,)"
    dict_rule[exc_txt] = False
    all_rules = rule.create_rules(dict_rule)
    enz1 = enzyme.Enzyme(-1, "fake_enzyme1", all_rules)
    # Second enzyme: cut after S
    dict_rule = {}
    rule_txt = "(S,)"
    dict_rule[rule_txt] = True
    all_rules = rule.create_rules(dict_rule)
    enz2 = enzyme.Enzyme(-1, "fake_enzyme2", all_rules)

    # Test function '__eq__()'
    assert enz0 == enz1
    assert enz0 != enz2
    assert enz0 != 42

    """Test function
    'write_enzyme_in_user_file(self, enz_file=DEFUSERENZFILE)'
    """
    output_file = tmp_path.joinpath("test_enzuser.py")
    dict_rule = {}
    rule_txt = "(D)(E,)"
    dict_rule[rule_txt] = True
    all_rules = rule.create_rules(dict_rule)
    new_enz = enzyme.Enzyme(-1, "fake_enzyme", all_rules)
    new_enz.write_enzyme_in_user_file(str(output_file))
    with open(output_file, encoding="utf-8") as outf:
        assert outf.read() == '\n\n\n# User-defined enzyme fake_enzyme\nEN'\
                              'Z = []\n\nE_1 = rule.Rule(0, "E", False, 1)'\
                              ' # Never cleaves after E, except...\nD_E_1M'\
                              '1 = rule.Rule(-1, "D", True, -1) # Always c'\
                              'leaves after E, preceded by D, except...\nE'\
                              '_1.rules.append(D_E_1M1)\nENZ.append(E_1)\n'\
                              '\nENZYME = enzyme.Enzyme(CPT_ENZ, "fake_enz'\
                              'yme", ENZ, 0)\n# Add it to available enzyme'\
                              's\nAVAILABLE_ENZYMES_USER.append(ENZYME)\nC'\
                              'PT_ENZ += 1\n'

def test_check_enzyme_name(capsys):
    """Test function 'check_enzyme_name(name_new_enz, all_name_enz)'."""

    # Already taken names
    all_name = ["pwet", "poulpe"]

    # Correct name
    seq_name = "0AzeRTY"
    res = enzyme.check_enzyme_name(seq_name, all_name)
    assert res is True

    # The enzyme name is already taken
    seq_name = "pwet"
    res = enzyme.check_enzyme_name(seq_name, all_name)
    assert res is False

    # No \t \n \r \f \v
    not_allowed = ["\t", "\\t", "\n", "\\n", "\r", "\\r", "\f", "\\f", "\v",
                   "\\v", " "]
    for i in not_allowed:
        seq_name = "AZE" + i + "RTY"
        res = enzyme.check_enzyme_name(seq_name, all_name)
        assert res is False

    # The enzyme name is empty
    seq_name = ""
    res = enzyme.check_enzyme_name(seq_name, all_name)
    assert res is False

    capsys.readouterr()

def test_user_creation_enzyme_non_interactive(capsys):
    """Test function 'user_creation_enzyme_non_interactive(all_enzymes, name_new_enz, rules, exceptions)'."""

    all_name = AVAILABLE_ENZYMES
    user_file = str(Path.home()) + "/rpg_user.py"

    name = "Arg-C"
    rules = ["(R,)"]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        enzyme.user_creation_enzyme_non_interactive(all_name, name, rules)
    _, err = capsys.readouterr()
    assert err == "This name exist, please choose another name.\n"
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

    name = "Pwet-42"
    rules = ["(C,)", "D,"]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        enzyme.user_creation_enzyme_non_interactive(all_name, name, rules)
    _, err = capsys.readouterr()
    assert err == "Error, no opening parenthesis founded\n"
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

    all_name = AVAILABLE_ENZYMES
    name = "Pwet-42"
    rules = ["(C,)", "(D,)"]
    exceptions = ["(C,)(E)", "(F)"]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        enzyme.user_creation_enzyme_non_interactive(all_name, name, rules, exceptions)
    _, err = capsys.readouterr()
    assert err == "Error, no ',' founded\n"
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

    # Number of line of user file before inserting an enzyme
    nb_line = 1
    with open(user_file) as usr_file:
        for line in usr_file:
            nb_line += 1
    assert nb_line == 9

    all_name = AVAILABLE_ENZYMES
    name = "Pwet-42"
    rules = ["(C,)", "(D,)"]
    exceptions = ["(C,)(E)"]
    enzyme.user_creation_enzyme_non_interactive(all_name, name, rules, exceptions)

    # Number of line of user file after inserting an enzyme
    nb_line = 1
    with open(user_file) as usr_file:
        for line in usr_file:
            nb_line += 1
    assert nb_line == 27

def test_delete_enzyme(capsys):
    """Test function 'delete_enzyme(all_enzymes, name)'."""

    user_file = str(Path.home()) + "/rpg_user.py"

    # Number of line of user file after inserting enzyme in previous test
    nb_line = 1
    with open(user_file) as usr_file:
        for line in usr_file:
            nb_line += 1
    assert nb_line == 27
    # Virtually add enzyme Pwet-42
    tmp = list(AVAILABLE_ENZYMES)
    ENZ = []

    C_1 = rule.Rule(0, "C", True, 1) # Always cleaves after C, except...
    C_1E1 = rule.Rule(1, "E", False, -1) # Never cleaves after C, followed by E, except...
    C_1.rules.append(C_1E1)
    ENZ.append(C_1)

    D_1 = rule.Rule(0, "D", True, 1) # Always cleaves after D, except...
    ENZ.append(D_1)

    ENZYME = enzyme.Enzyme(44, "Pwet-42", ENZ, 0)
    # Add it to available enzymes
    tmp.append(ENZYME)
    # Delete it
    enzyme.delete_enzyme(tmp, "Pwet-42")

    # Normal process
    all_enz = AVAILABLE_ENZYMES
    name = "Pwet"
    rules = ["(R,)"]
    # Number of line of user file before inserting an enzyme
    nb_line = 1
    with open(user_file) as usr_file:
        for line in usr_file:
            nb_line += 1
    assert nb_line == 9
    # Add a new enzyme
    enzyme.user_creation_enzyme_non_interactive(all_enz, name, rules)
    # Number of line of user file after inserting an enzyme
    nb_line = 1
    with open(user_file) as usr_file:
        for line in usr_file:
            nb_line += 1
    assert nb_line == 22

    # Virtually add enzyme Pwet
    tmp = list(AVAILABLE_ENZYMES)
    ENZ = []

    R_1 = rule.Rule(0, "R", True, 1) # Always cleaves after R, except...
    ENZ.append(R_1)

    ENZYME = enzyme.Enzyme(44, "Pwet", ENZ, 0)
    # Add it to available enzymes
    tmp.append(ENZYME)

    # Delete it
    enzyme.delete_enzyme(tmp, "Pwet")
    # We should be back at 11 lines
    nb_line = 1
    with open(user_file) as usr_file:
        for line in usr_file:
            nb_line += 1
    assert nb_line == 9

    # Wrong name to delete
    name = "Pwet"
    rules = ["(R,)"]
    # Number of line of user file before inserting an enzyme
    nb_line = 1
    with open(user_file) as usr_file:
        for line in usr_file:
            nb_line += 1
    assert nb_line == 9
    # Add a new enzyme
    enzyme.user_creation_enzyme_non_interactive(all_enz, name, rules)
    # Number of line of user file after inserting an enzyme
    nb_line = 1
    with open(user_file) as usr_file:
        for line in usr_file:
            nb_line += 1
    assert nb_line == 22

    # Virtually add enzyme Pwet
    tmp = list(AVAILABLE_ENZYMES)
    ENZ = []

    R_1 = rule.Rule(0, "R", True, 1) # Always cleaves after R, except...
    ENZ.append(R_1)

    ENZYME = enzyme.Enzyme(44, "Pwet", ENZ, 0)
    # Add it to available enzymes
    tmp.append(ENZYME)

    # Delete it
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        enzyme.delete_enzyme(AVAILABLE_ENZYMES, "Pwett")
    _, err = capsys.readouterr()
    assert err == "Error: Not able to find enzyme Pwett.\n"
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    enzyme.delete_enzyme(tmp, "Pwet")
    # We should be back at 11 lines
    nb_line = 1
    with open(user_file) as usr_file:
        for line in usr_file:
            nb_line += 1
    assert nb_line == 9

    # Name with regex chat name
    name = "Pwe.[t"
    rules = ["(R,)"]
    # Number of line of user file before inserting an enzyme
    nb_line = 1
    with open(user_file) as usr_file:
        for line in usr_file:
            nb_line += 1
    assert nb_line == 9
    # Add a new enzyme
    enzyme.user_creation_enzyme_non_interactive(all_enz, name, rules)
    # Number of line of user file after inserting an enzyme
    nb_line = 1
    with open(user_file) as usr_file:
        for line in usr_file:
            nb_line += 1
    assert nb_line == 22
    # Virtually add enzyme Pwet
    tmp = list(AVAILABLE_ENZYMES)
    ENZ = []

    R_1 = rule.Rule(0, "R", True, 1) # Always cleaves after R, except...
    ENZ.append(R_1)

    ENZYME = enzyme.Enzyme(44, "Pwe.[t", ENZ, 0)
    # Add it to available enzymes
    tmp.append(ENZYME)
    # Delete it
    enzyme.delete_enzyme(tmp, "Pwe.[t")
    # We should be back at 11 lines
    nb_line = 1
    with open(user_file) as usr_file:
        for line in usr_file:
            nb_line += 1
    assert nb_line == 9

def test_get_enz_name(capsys):
    """Test function 'get_enz_name()'."""
    # Enzyme does not exist
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        enzyme.get_enz_name(AVAILABLE_ENZYMES, "Pwett")
    _, err = capsys.readouterr()
    assert err == "Error: Not able to find enzyme Pwett.\n"
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

    # Normal behavior
    assert enzyme.get_enz_name(AVAILABLE_ENZYMES, 42) == "Trypsin"

    # Normal behavior
    assert enzyme.get_enz_name(AVAILABLE_ENZYMES, "42") == "Trypsin"

    # Normal behavior
    assert enzyme.get_enz_name(AVAILABLE_ENZYMES, "trypsin") == "Trypsin"