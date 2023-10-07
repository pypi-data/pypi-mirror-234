# -*- coding: utf-8 -*-
#!/usr/bin/env python3.11

########################################################################
# Rapid Peptide Generator (RPG) is a software dedicated to predict     #
# cleavage sites of proteases. User can create his own enzyme,         #
# following a simple grammar.                                          #
#                                                                      #
# Author: Nicolas Maillet                                              #
# Copyright © 2018 Institut Pasteur, Paris.                            #
# See the COPYRIGHT file for details                                   #
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

"""Main file of RPG software, handle input/output and launch
necessary functions
"""

__version_info__ = ('2', '0', '2')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2023-10-06"
__author__ = "Nicolas Maillet"

import argparse
import os
import sys
import uuid
from pathlib import Path
#from context import rpg
from rpg import core
from rpg import digest
from rpg import enzyme
from rpg.enzymes_definition import AVAILABLE_ENZYMES
sys.path.insert(0, str(Path.home())) # Home path
from rpg_user import AVAILABLE_ENZYMES_USER

ALL_ENZYMES = AVAILABLE_ENZYMES + AVAILABLE_ENZYMES_USER
"""All available enzymes in RPG."""

def restricted_float(mc_val):
    """Restricts input miscleavage value to a float between 0 and 100.

    :param mc_val: value to test
    :type mc_val: float

    :return: the inputed value if correct
    :rtype: float

    :raises custom ValueError: if value is not between 0 and 100
    :raises custom TypeError: if value is not a float
    """
    try:
        mc_val = float(mc_val)
        if mc_val < 0 or mc_val > 100:
            core.handle_errors("miscleavage value should be between 0 and "\
                               "100.", 0, "Value ")
        return mc_val
    except ValueError:
        # Throw an error
        core.handle_errors("miscleavage value should be a float between 0 "\
                           "and 100.", 0, "Type ")

def restricted_int(mc_val):
    """Restricts input miscleavage value to a int.

    :param mc_val: value to test
    :type mc_val: int

    :return: the inputed value if correct
    :rtype: int

    :raises custom TypeError: if value is not an int
    """
    try:
        mc_val = int(mc_val)
        if mc_val < 0 :
            core.handle_errors("miscleavage value should be greater then 0.", 0, "Value ")
        return mc_val
    except ValueError:
        # Throw an error
        core.handle_errors("miscleavage value should be an integer.", 0,
                           "Type ")

def restricted_enzyme_id(enz_id):
    """Restrict input enzyme id to a str corresponding to an enzyme.

    :param mc_val: value to test
    :type mc_val: str

    :return: the inputed enzyme id
    :rtype: str
    """

    ids_available = []
    names_available = []
    for i in ALL_ENZYMES:
        ids_available.append(str(i.id_))
        names_available.append(i.name.casefold())
    if str(enz_id) not in ids_available and \
       str(enz_id).casefold() not in names_available:
        core.handle_errors(f"id {enz_id} does not correspond to any "\
                            "enzyme. Use -l to get enzyme ids.", 0,
                            "Input ")
    return str(enz_id)


def list_enzyme():
    """Print all available enzymes"""
    for enz in ALL_ENZYMES:
        print("%i: %s" % (enz.id_, enz.name))

def create_enzymes_to_use(enzymes, miscleavage):
    """Create the list of chosen :py:class:`~rpg.enzyme.Enzyme` to use.
    Each enzyme can be associated to a miscleavage value.

    :param enzymes: enzymes ids or names chosen by user
    :param miscleavage: associated miscleavage values
    :type enzymes: list(str)
    :type miscleavage: list(float)

    :return: list of enzyme's id with associated miscleavage values
    :rtype: list(int)
    """

    # Complete Enzymes to use (return)
    enzymes_to_use = []
    if enzymes:
        # Too much miscleavage values
        if len(miscleavage) > len(enzymes):
            core.handle_errors("Too much miscleavage values. Last values"
                               " will be ignored.")
            # Get only the first ones
            miscleavage = miscleavage[:len(enzymes)]
        cur_pos = -1
        # Get all enzymes with a given miscleavage
        for i, _ in enumerate(miscleavage):
            # In all available enzymes
            for enz in ALL_ENZYMES:
                # Get the current one
                if str(enz.id_) == str(enzymes[i]) or \
                   enz.name.casefold() == str(enzymes[i]).casefold():
                    # Change miscleavage ratio
                    enz.ratio_miscleavage = miscleavage[i]
                    # Add it
                    enzymes_to_use.append(enz)
            cur_pos = i
        # Get all enzymes without miscleavage value
        for i in enzymes[cur_pos + 1:]:
            # In all available enzymes
            for enz in ALL_ENZYMES:
                # Get the current one
                if str(enz.id_) == str(i) or enz.name.casefold() == str(i).casefold():
                    # Add it
                    enzymes_to_use.append(enz)
    # Return enzymes to use
    return enzymes_to_use
# Not tested
def get_enzymes_to_use(mode, id_enz_selected, miscleavage):
    """Get the list of chosen :py:class:`~rpg.enzyme.Enzyme` to use.
    Each enzyme (and associated miscleavage value) are inputed by
    user. If there is a problem, user is interrogated again.

    :param mode: Digestion mode. If 'concurrent', no miscleavage values are used
    :param enzymes: enzyme's ids or names chosen by user
    :param miscleavage: associated miscleavage values
    :type mode: str
    :type enzymes: list(str)
    :type miscleavage: list(float)

    :return: list of enzyme's id with associated miscleavage values
    :rtype: list(int)
    """

    # Get the correct Enzymes inputed
    enzymes_to_use = create_enzymes_to_use(id_enz_selected, miscleavage)
    # No good Enzymes inputed, let user choose
    if not enzymes_to_use:
        id_enz_inputed = []
        # Print all available enzymes
        list_enzyme()
        # Ask user to give correct enzymes ids
        while not enzymes_to_use:
            id_enz_inp = input("Choose which enzyme(s) to use, separated by"
                               " space (example: 1 5 6). (q) to quit:\n")
            # Quit
            if "q" in id_enz_inp:
                sys.exit(0)
            # Get a list of ids
            for i in id_enz_inp.split(" "):
                id_enz_inputed.append(i)

            mc_enz_inputed = []
            if mode == "sequential":
                mc_enz_inp = input("Percentage of miscleavage per inputed"
                                   " enzyme (default 0), separated by sapce"
                                   " (example: 1.2 5 6):\n")
                if mc_enz_inp:
                    # Get a list of int
                    for i in mc_enz_inp.split(" "):
                        try:
                            # Convert it to int
                            i = float(i)
                            mc_enz_inputed.append(i)
                        # Not an int?
                        except ValueError:
                            # Throw an error
                            core.handle_errors("'%s' should be an floating"
                                               " value. This values will be"
                                               " ignored." % i)
            # Get the correct Enzyme if enzymes inputed
            enzymes_to_use = create_enzymes_to_use(id_enz_inputed,
                                                   mc_enz_inputed)
    # Return Enzymes to use
    return enzymes_to_use

# Not tested
def main():
    """Launcher of RapidPeptidesGenerator"""
    parser = argparse.ArgumentParser(description="This software takes protein "
                                                 "sequences as input (-i optio"
                                                 "n). All sequences will be cl"
                                                 "eaved according to selected "
                                                 "enzymes (-e option) and give"
                                                 "n miscleavage percentage ("
                                                 "-m option). Cleaving can be "
                                                 "sequential or concurrent (-d"
                                                 " option). Resulting peptides"
                                                 " are outputted in a file (-o"
                                                 " option) in fasta, csv or ts"
                                                 "v format (-f option). Classi"
                                                 "cal enzymes are included (-l"
                                                 " option to print available e"
                                                 "nzymes) but it is possible t"
                                                 "o define other enzymes (-a o"
                                                 "ption). See https://gitlab.p"
                                                 "asteur.fr/nmaillet/rpg/ and "
                                                 "https://rapid-peptide-genera"
                                                 "tor.readthedocs.io for more "
                                                 "informations.")
    group_launch = parser.add_mutually_exclusive_group(required=True)
    group_launch.add_argument("-a", "--addenzyme", action="store_true",
                              help="Create a new enzyme. See https://rapid-pe"\
                              "ptide-generator.readthedocs.io for more inform"\
                              "ation")
    group_launch.add_argument("-b", "--delenzyme", metavar="str",
                              help="Delete a user-define enzyme. See "\
                              "https://rapid-peptide-generator.readthedocs.io "\
                              "for more information")
    parser.add_argument("-d", "--digest", metavar="str",
                        choices=['s', 'sequential', 'c', 'concurrent'],
                        default="s", help="Digestion mode. Either 's', 'seque"
                        "ntial', 'c' or 'concurrent' (default: s)")
    parser.add_argument("-e", "--enzymes", metavar="str", default=[],
                        nargs='+', type=restricted_enzyme_id,
                        help="Id or name of enzyme(s) to use (e.g. -e 1 Asp-N "
                             "10 to use enzymes 1, Asp-N and 10). Use -l first"
                             " to get enzyme ids or names")
    parser.add_argument("-f", "--fmt", metavar="str",
                        choices=['fasta', 'csv', 'tsv'], default="fasta",
                        help="Output file format. Either 'fasta', 'csv', or "
                             "'tsv' (default: fasta)")
    group_launch.add_argument("-i", "--inputdata", metavar="path",
                              help="Input file, in fasta / fastq format "\
                                   "(gzipped or not)")
    group_launch.add_argument("-l", "--list", action="store_true",
                              help="Display the list of available enzymes")
    group_launch.add_argument("-s", "--sequence", metavar="str",
                              help="Input a single protein sequence without "\
                                   "commentary")
    group_mc = parser.add_mutually_exclusive_group(required=False)
    group_mc.add_argument("-m", "--miscleavage", metavar="float", default=[],
                        nargs='+', type=restricted_float,
                        help="Percentage of miscleavage, between 0 and 100,"
                        " by enzyme(s). It should be in the same order than "
                        "-enzymes options (e.g. -m 15 5 10). Only for sequenti"
                        "al digestion (default: 0)")
    group_mc.add_argument("-t", "--theoretical", metavar="int", default=[],
                        nargs='+', type=restricted_int,
                        help="Maximum number of miscleavages, by enzyme(s). "
                        "RPG will produce all theoretical peptides allowing "
                        "at most -t miscleavages. It should be in the same "
                        "order than -enzymes options (e.g. -t 1 3 2). Only "
                        "for sequential digestion (default: 0)")
    parser.add_argument("-n", "--noninteractive", action='store_true',
                        help="Non-interactive mode. No standard output, only "
                        "error(s) (--quiet enable, overwrite -v). If output "
                        "filename already exists, output file will be "
                        "overwritten.")
    parser.add_argument("-x", "--cleave", type=str, metavar="str", default=[],
                        nargs='+',
                        help="Cleavage site(s) when adding enzyme in non-inte"\
                        "ractive (e.g. -x \"(D or E,)\" or -x \"(D,)\" \"(E,)\"")

    parser.add_argument("-z", "--exception", type=str, metavar="str", default=[],
                        nargs='+',
                        help="Exception(s) when adding enzyme in non-interact"\
                        "ive (e.g. -z \"(D,)(W)\" \"(D,)(A)\"")

    parser.add_argument("-y", "--enzname", type=str, metavar="str", default="",
                        help="Enzyme's name when adding enzyme in non-interac"\
                        "tive.")
    parser.add_argument("-p", "--pka", metavar="str", choices=['ipc2', 'stryer', 'ipc'],
                        default="ipc2", help="Define pKa values. Either 'ipc2' "
                        "'stryer' or 'ipc' (default: ipc2)")
    parser.add_argument("-w", "--mass", metavar="str", choices=['avg', 'mono'],
                        default="avg", help="Define atomic mass values. "\
                        "Either 'avg' for average mass or 'mono' for "\
                        "monoisotopic mass (default: avg)")
    group_output = parser.add_mutually_exclusive_group()
    group_output.add_argument("-o", "--outputfile", type=str, metavar="str",
                              default="", help="Optional result file "
                              "to output result peptides.")
    group_output.add_argument("-r", "--randomname", action="store_true",
                              help="Random (not used) output file name")
    parser.add_argument("-c", "--processes", type=int, metavar="int", default=1,
                       help="Number of parallel processes to use (default: 1)")
    group_verbose = parser.add_mutually_exclusive_group()
    group_verbose.add_argument("-q", "--quiet", action="store_true",
                               help="No standard output, only error(s)")
    group_verbose.add_argument("-v", "--verbose", action="count", default=0,
                               help="Increase output verbosity. -vv will "
                               "increase more than -v")
    parser.add_argument("--version", action="version",
                        version="%(prog)s " + __version__ + " from " +
                        __revision_date__)
    args = parser.parse_args()

    # --addenzyme option
    if args.addenzyme:
        if args.noninteractive:
            # We need a name
            if not args.enzname:
                parser.error("argument -y/--enzname is mandatory")
            # We need at least a rule
            if not args.enzname:
                parser.error("argument -x/--cleave is mandatory")
            # Create the enzyme
            enzyme.user_creation_enzyme_non_interactive(ALL_ENZYMES,
                                                        args.enzname,
                                                        args.cleave,
                                                        args.exception)
        else:
            enzyme.user_creation_enzyme(ALL_ENZYMES)
        sys.exit(0)

    # --delenzyme option
    if args.delenzyme:
        enzyme.delete_enzyme(ALL_ENZYMES, args.delenzyme)
        sys.exit(0)

    # --digest option
    mode = "sequential"
    if args.digest == "c" or args.digest == "concurrent":
        mode = "concurrent"
        args.miscleavage = []  # No miscleavage on concurrent, infinite time

    # --pka option
    aa_pka = core.AA_PKA_IPC_2
    if args.pka == "stryer":
        aa_pka = core.AA_PKA_S
    elif args.pka == "ipc":
        aa_pka = core.AA_PKA_IPC

    # --mass option
    aa_mass = core.AA_MASS_AVERAGE
    water_mass = core.WATER_MASS
    if args.mass == "mono":
        aa_mass = core.AA_MASS_MONO
        water_mass = core.WATER_MASS_MONO

    # --list option
    if args.list:
        list_enzyme()
        sys.exit(0)

    # --nointeractive option
    if args.noninteractive:
        args.quiet = 1
        args.verbose = 0

    # Be sure to have at least 1 process
    if args.processes <= 0:
        parser.error("argument -c/--processes should be greater than 0")

    # input data
    input_data = None
    input_type = None
    if args.inputdata:
        if os.path.isfile(args.inputdata):
            input_data = args.inputdata
            input_type = "file"
        else:
            core.handle_errors("file not found (%s)." % args.inputdata, 0, "I"\
                               "nput ")
    elif args.sequence:
        input_data = args.sequence
        input_type = "sequence"

    # --outputfile / --randomname options
    output_file = "" # No output file (default)
    if args.randomname:
        # Generate a random file name
        output_file = str(uuid.uuid4().hex) + "." + args.fmt
        # Ensure the name is unique
        while os.path.isfile(output_file):
            # Generate a random file name
            output_file = str(uuid.uuid4().hex) + "." + args.fmt
    # Chosen file name if exist
    elif args.outputfile:
        # Given name
        tmpname = str(args.outputfile)
        # No extension?
        if "." not in tmpname:
            # Add default extension for this file format
            output_file = tmpname + "." + args.fmt
        else:
            output_file = tmpname
        # If interactive mode
        if not args.noninteractive:
            # This file already exist?
            while os.path.isfile(output_file):
                core.handle_errors("File '%s' already exit!" % output_file)
                # Don't overwrite it
                if input("Overwrite it? (y/n)\n") != "y":
                    tmpname = input("Output filename?\n")
                    # No extension?
                    if "." not in tmpname:
                        # Add default extension for this file format
                        output_file = tmpname + "." + args.fmt
                    else:
                        output_file = tmpname
                # Overwrite it
                else:
                    break

    # More mis cleavage than enzyme
    if len(args.miscleavage) > len(args.enzymes):
        core.handle_errors("Too much miscleavage values. Last values will "
                           "be ignored.")
        args.miscleavage = args.miscleavage[:len(args.enzymes)]

    # Get all enzymes inputed
    enzymes_to_use = get_enzymes_to_use(mode, args.enzymes, args.miscleavage)

    # Output options
    if args.verbose:
        print("Input: " + input_data)
        print("Enzyme(s) used: " + str([enz.name for enz in enzymes_to_use]))
        print("Mode: " + mode)
        print("miscleavage ratio: " +
              str([enz.ratio_miscleavage for enz in enzymes_to_use]))
        if output_file:
            print("Output file: " + os.path.abspath(output_file))

    # Make the actual digestion of input data
    results_digestion = digest.digest_from_input(input_data, input_type,
                                                 enzymes_to_use, mode, aa_pka,
                                                 aa_mass, water_mass,
                                                 args.processes)

    # We need to compute all theoretical peptides for at least one enzyme
    if args.theoretical:
        # More mis cleavage than enzyme
        if len(args.theoretical) > len(args.enzymes):
            core.handle_errors("Too much miscleavage values. Last values will "
                               "be ignored.")
        # Not enough mis cleavage values, complete with 0
        elif len(args.theoretical) < len(args.enzymes):
            args.theoretical += [0]*(len(args.enzymes) - len(args.theoretical))
        # Dict of enzymes/max mis cleavage
        enzymes_to_use = {}
        # Link enzyme to mc value
        for i, j in enumerate(args.enzymes):
            enzymes_to_use[enzyme.get_enz_name(ALL_ENZYMES, j)] = args.theoretical[i]
        # Compute the results
        digest.theoretical_peptides(results_digestion, enzymes_to_use)
    # Output results
    core.output_results(output_file, results_digestion, args.fmt, args.quiet,
                        args.verbose)

### Let'z go ###
if __name__ == '__main__':
    main()
    # The end
    sys.exit(0)
