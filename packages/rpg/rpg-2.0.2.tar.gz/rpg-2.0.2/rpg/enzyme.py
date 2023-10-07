# -*- coding: utf-8 -*-

########################################################################
# Author: Nicolas Maillet                                              #
# Copyright © 2018 Institut Pasteur, Paris.                            #
# See the COPYRIGHT file for details                                   #
#                                                                      #
# This file is part of Rapid Peptide Generator (RPG) software.         #
#                                                                      #
# RPG is free software: you can redistribute it and/or modify          #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or    #
# any later version.                                                   #
#                                                                      #
# RPG is distributed in the hope that it will be useful,               #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public license    #
# along with RPG (LICENSE file).                                       #
# If not, see <http://www.gnu.org/licenses/>.                          #
########################################################################

"""Contains class and functions related to enzymes definition and use"""
import os
import re
import sys
from pathlib import Path
from rpg import core
from rpg import rule

DEFUSERENZFILE = str(Path.home()) + "/rpg_user.py"

# Create the enzymes_user file if it does not exist
if not os.path.isfile(DEFUSERENZFILE):
    with open(DEFUSERENZFILE, "w", encoding="Utf-8") as out_file:
        out_file.write("from rpg import enzyme\nfrom rpg import rule\n"\
                       "from rpg import enzymes_definition"\
                       "\n\nAVAILABLE_ENZYMES_USER = []\nCPT_ENZ = enzymes_de"\
                       "finition.CPT_ENZ\n\n### ENZYMES DECLARATION ###\n")

class Enzyme:
    """Definition of an cleaving enzyme containing specific rules.

    :param id_: id of the enzyme
    :param name: name of the enzyme
    :param rules: cleaving rules
    :param ratio_miscleavage: miscleavage ratio
    :type id_: int
    :type name: str
    :type rules: list(:py:class:`~rpg.rule.Rule`)
    :type ratio_miscleavage: float
    """
    def __init__(self, id_, name, rules, ratio_miscleavage=0):
        self.id_ = id_
        self.name = name
        self.ratio_miscleavage = ratio_miscleavage
        self.rules = rules

    # self representation for print
    def __repr__(self):
        return "Id: %s\nName: %s\nRatio Miscleavage: %.2f%%\nRules: %s\n" %\
            (self.id_, self.name, self.ratio_miscleavage, self.rules)

    # Equality between two Enzymes
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False

    def write_enzyme_in_user_file(self, enz_file=DEFUSERENZFILE):
        """Write enzyme to user's enzyme file as a Python function.

        :param enz_file: location of user file (default: ~/rpg_user.py)
        :type enz_file: str
        """
        if self.rules != []:
            # Comment and first line of the Enzyme
            ret = "\n\n\n# User-defined enzyme " + self.name + "\nENZ = []\n\n"
            # Write all the main rules and their su-rules
            for i in self.rules:
                ret += i.format_rule()
            # Write the end of the Enzyme
            ret += "ENZYME = enzyme.Enzyme(CPT_ENZ, \"" + self.name + "\", "\
                   "ENZ, 0)\n# Add it to available enzymes\nAVAILABLE_ENZYMES"\
                   "_USER.append(ENZYME)\nCPT_ENZ += 1\n"
            # Write all in the user file
            try:
                with open(enz_file, "a") as output_file:
                    output_file.write(ret)
            except IOError:
                core.handle_errors("'%s' can't be open in '%s' mode" %
                                   (enz_file, "a"), 0, "File ")

def get_enz_name(all_enzymes, name):
    """ Get the proper name of an enzyme

    :param all_enzymes: all already existing enzymes
    :param name: name or id of the enzyme
    :type all_enzymes: list(:py:class:`~rpg.enzyme.Enzyme`)
    :type name: str

    :return: The real name of an enzyme
    :rtype: str
    """
    enz_name = None
    # Get the name
    for i in all_enzymes:
        # Get the name of this enzyme
        if (str(name).isdigit() and i.id_ == int(name)) or \
           i.name.casefold() == str(name).casefold():
            enz_name = i.name.strip()
            break
    # Enzyme not found
    if not enz_name:
        core.handle_errors(f"Not able to find enzyme {name}.", 0)
    # Return the correct name of this enzyme
    return enz_name

def check_enzyme_name(name_new_enz, all_name_enz):
    """Validate the name of a new enzyme.

    :param name_new_enz: name of the new enzyme
    :param all_name_enz: names of already created enzymes
    :type name_new_enz: str
    :type all_name_enz: list(str)

    :return: True if name is correct
    :rtype: bool

    Enzyme name should not contains whitespace character (' ', \\\\t,
    \\\\n, \\\\r, \\\\f, \\\\v), be empty, a digit or be already used.
    """

    ret = True
    # If the enzyme name is already taken
    if name_new_enz in all_name_enz:
        core.handle_errors("This name exist, please choose another name.", 2)
        ret = False

    # Does it contain only digit character?
    if name_new_enz.isdigit():
        core.handle_errors("Enzyme name can't be only digits, please choose"\
                           " another name.", 2)
        ret = False

    # Does it contain ' ' character?
    res = re.search(" ", name_new_enz)
    if res:
        to_print = ""
        for _ in range(res.start()):
            to_print += " "
        to_print += "^\n"
        core.handle_errors(to_print + "Space character found at position " +
                           str(res.start() + 1) +
                           ", please choose another name.", 2)
        ret = False

    # Does it contain \t character?
    res = re.search("\t", name_new_enz)
    if res:
        to_print = ""
        for _ in range(res.start()):
            to_print += " "
        to_print += "^\n"
        core.handle_errors(to_print + "Tab character found at position " +
                           str(res.start() + 1) +
                           ", please choose another name.", 2)
        ret = False
    res = name_new_enz.find("\\t")
    if res != -1:
        to_print = ""
        for _ in range(res):
            to_print += " "
        to_print += "^\n"
        core.handle_errors(to_print + "Tab character found at position " +
                           str(res + 1) + ", please choose another name.", 2)
        ret = False

    # Does it contain \n character?
    res = re.search("\n", name_new_enz)
    if res:
        to_print = ""
        for _ in range(res.start()):
            to_print += " "
        to_print += "^\n"
        core.handle_errors(to_print + "Newline character found at position " +
                           str(res.start() + 1) +
                           ", please choose another name.", 2)
        ret = False
    res = name_new_enz.find("\\n")
    if res != -1:
        to_print = ""
        for _ in range(res):
            to_print += " "
        to_print += "^\n"
        core.handle_errors(to_print + "Newline character found at position " +
                           str(res + 1) + ", please choose another name.", 2)
        ret = False

    # Does it contain \r character?
    res = re.search("\r", name_new_enz)
    if res:
        to_print = ""
        for _ in range(res.start()):
            to_print += " "
        to_print += "^\n"
        core.handle_errors(to_print + "Carriage return (\\r) character found "
                           "at position " + str(res.start() + 1) +
                           ", please choose another name.", 2)
        ret = False
    res = name_new_enz.find("\\r")
    if res != -1:
        to_print = ""
        for _ in range(res):
            to_print += " "
        to_print += "^\n"
        core.handle_errors(to_print + "Carriage return (\\r) character found "
                           "at position " + str(res + 1) +
                           ", please choose another name.", 2)
        ret = False

    # Does it contain \f character?
    res = re.search("\f", name_new_enz)
    if res:
        to_print = ""
        for _ in range(res.start()):
            to_print += " "
        to_print += "^\n"
        core.handle_errors(to_print + "Form feed (\\f) character found at "
                           "position " + str(res.start() + 1) +
                           ", please choose another name.", 2)
        ret = False
    res = name_new_enz.find("\\f")
    if res != -1:
        to_print = ""
        for _ in range(res):
            to_print += " "
        to_print += "^\n"
        core.handle_errors(to_print + "Form feed (\\f) character found at "
                           "position " + str(res + 1) +
                           ", please choose another name.", 2)
        ret = False

    # Does it contain \v character?
    res = re.search("\v", name_new_enz)
    if res:
        to_print = ""
        for _ in range(res.start()):
            to_print += " "
        to_print += "^\n"
        core.handle_errors(to_print + "Vertical Tab (\\v) character found at "
                           "position " + str(res.start() + 1) +
                           ", please choose another name.", 2)
        ret = False
    res = name_new_enz.find("\\v")
    if res != -1:
        to_print = ""
        for _ in range(res):
            to_print += " "
        to_print += "^\n"
        core.handle_errors(to_print + "Vertical Tab (\\v) character found at "
                           "position " + str(res + 1) +
                           ", please choose another name.", 2)
        ret = False

    # Not empty
    if name_new_enz == "":
        core.handle_errors("Please choose a not empty name.", 2)
        ret = False

    return ret

# Not tested
def user_creation_enzyme(all_enzymes):
    """Text-mod form to input a new enzyme.

    .. warning:: Not tested
    .. warning:: It could be a problem to immediately use the new enzyme (see in-code warning)
    """
    add_enzyme = "y"

    # All enzymes name
    all_name_enz = set()

    # Get all used names
    for enz in all_enzymes:
        all_name_enz.add(enz.name)

    # Adding enzyme
    while add_enzyme == "y":

        # Name of the enzyme
        name_new_enz = input("Name of the new enzyme?\n")
        while not check_enzyme_name(name_new_enz, all_name_enz):
            # Name of the enzyme
            name_new_enz = input("Name of the new enzyme?\n")

        # All the rules entered by user
        all_rules = {}
        # Input of user for creating rules
        def_rule = "_"
        while def_rule != "":
            # Type of rule?
            cutmp = ""
            # Ensure we got a correct value i.e. c, e or q
            while (cutmp != "c") and (cutmp != "e") and (cutmp != "q"):
                cutmp = input("Create a cleaving rule (c) or an exception (e)?"
                              " (q) to quit:\n")
            # Exit
            if cutmp == "q":
                break
            # Set the cut to what the user ask: e = False
            cut = False
            # c = True
            if cutmp == "c":
                cut = True
            # The rule is valid?
            validate_rule = ""
            # Until the rules is not properly defined:
            while validate_rule == "":
                # Cleaving rule
                if cut:
                    def_rule = input("Write your cleaving rule,"
                                     " (q) to quit:\n")
                # Exception rule
                else:
                    def_rule = input("Write your exception rule,"
                                     " (q) to quit:\n")
                # Quit?
                if def_rule == "q":
                    break
                # Check if input is coherent
                validate_rule = rule.check_rule(def_rule)
            # Add this rule
            if validate_rule != "":
                all_rules[validate_rule] = cut

        # Get all the rules in correct format
        correct_rules = rule.create_rules(all_rules)

        # Create the enzyme with fake id (auto-inc)
        # .. warning:: It could be a problem to immediately use the new enzyme
        new_enz = Enzyme(-1, name_new_enz, correct_rules)

        # Write in the user-defined enzymes file
        new_enz.write_enzyme_in_user_file()

        # Add it to known names
        all_name_enz.add(new_enz.name)

        # End of this new enzyme
        add_enzyme = input("Add another enzyme? (y/n)\n")

def user_creation_enzyme_non_interactive(all_enzymes, name_new_enz, rules, exceptions=None):
    """One-line input a new enzyme.

    :param all_enzymes: all already existing enzymes
    :param name: name of the enzyme to create
    :param rules: rules defining the new enzyme
    :param exceptions: exceptions defining the new enzyme
    :type all_enzymes: list(:py:class:`~rpg.enzyme.Enzyme`)
    :type name: str
    :type rules: list(str)
    :type exceptions: list(str)

    .. warning:: It could be a problem to immediately use the new enzyme (see in-code warning)
    """

    # All enzymes name
    all_name_enz = set()

    # Get all used names
    for enz in all_enzymes:
        all_name_enz.add(enz.name)

    # Is the name of the enzyme valid?
    if not check_enzyme_name(name_new_enz, all_name_enz):
        sys.exit(1)

    # All the rules entered by user
    all_rules = {}
    # For all cleavage rules
    for def_rule in rules:
        # Validate this rule
        validate_rule = rule.check_rule(def_rule)
        # This rule is not valid, exit
        if validate_rule == "":
            sys.exit(1)
        # Add this rule
        all_rules[validate_rule] = True

    # For all exceptions
    if exceptions:
        for def_rule in exceptions:
            # Validate this exception
            validate_rule = rule.check_rule(def_rule)
            # This exception is not valid, exit
            if validate_rule == "":
                sys.exit(1)
            # Add this exception
            all_rules[validate_rule] = False

    # Get all the rules in correct format
    correct_rules = rule.create_rules(all_rules)

    # Create the enzyme with fake id (auto-inc)
    # .. warning:: It could be a problem to immediately use the new enzyme
    new_enz = Enzyme(-1, name_new_enz, correct_rules)

    # Write in the user-defined enzymes file
    new_enz.write_enzyme_in_user_file()

    # Add it to known names
    all_name_enz.add(new_enz.name)

def delete_enzyme(all_enzymes, name):
    """ Delete an enzyme from user file 

    :param all_enzymes: all already existing enzymes
    :param name: name or id of the enzyme to delete
    :type all_enzymes: list(:py:class:`~rpg.enzyme.Enzyme`)
    :type name: str

    .. warning:: Partially tested, remove by ID can't be tested
    """
    user_content = ""
    # Get the whole content of user file
    with open(DEFUSERENZFILE, encoding="Utf-8") as user_file:
        for line in user_file:
            user_content += line

    # Get the name of the enzyme
    enz_name = get_enz_name(all_enzymes, name)

    # Beginning of what to remove
    beg_to_detect = f"# User-defined enzyme {re.escape(enz_name)}\n"
    # End of what to remove
    end_to_detect = f"ENZYME = enzyme\.Enzyme\(CPT_ENZ, \"{re.escape(enz_name)}\", ENZ, 0\)\n"
    # Get everything that needs to be removed
    res = re.findall(fr"\n\n\n{beg_to_detect}.*{end_to_detect}.*?\n.*?\n.*?\n", user_content, re.DOTALL)
    # We should have a single match
    if len(res) == 1:
        # Remove the content with escape to protect [ and more
        new_user_content = re.sub(re.escape(res[0]), r"", user_content, re.DOTALL)
        # Rewrite the user file
        with open(DEFUSERENZFILE, "w", encoding="Utf-8") as user_file:
            user_file.write(new_user_content)
    # More than one hit, we can't do much automatically
    else:
        # Exit and invite the user to manually edit the file
        core.handle_errors(f"Not able to remove enzyme {name}, please remove manually", 0)
