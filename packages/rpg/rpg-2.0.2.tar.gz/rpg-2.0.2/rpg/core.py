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

"""Contains generic functions and global variables used by RPG"""
import sys
import gzip

AMINOACIDS = ["A", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
              "O", "P", "Q", "R", "S", "T", "U", "V", "W", "Y", "B", "X", "Z",
              "#", "*"]
"""All character accepted in a peptide."""


AA_MASS_AVERAGE = {"*" : 0.0,
                   "A" : 71.0788,
                   "C" : 103.1388,
                   "D" : 115.0886,
                   "E" : 129.1155,
                   "F" : 147.1766,
                   "G" : 57.0519,
                   "H" : 137.1411,
                   "I" : 113.1594,
                   "J" : 113.1594,
                   "K" : 128.1741,
                   "L" : 113.1594,
                   "M" : 131.1926,
                   "N" : 114.1038,
                   "O" : 237.3018,
                   "P" : 97.1167,
                   "Q" : 128.1307,
                   "R" : 156.1875,
                   "S" : 87.0782,
                   "T" : 101.1051,
                   "U" : 150.0388,
                   "V" : 99.1326,
                   "W" : 186.2132,
                   "Y" : 163.1760,
                   "B" : 0.0,
                   "X" : 0.0,
                   "Z" : 0.0,
                   "#" : 0.0}
""" Average mass of all amino acids."""

AA_MASS_MONO =  {"*" : 0.0,
                  "A" : 71.037113805,
                  "C" : 103.009184505,
                  "D" : 115.026943065,
                  "E" : 129.042593135,
                  "F" : 147.068413945,
                  "G" : 57.021463735,
                  "H" : 137.058911875,
                  "I" : 113.084064015,
                  "J" : 113.084064015,
                  "K" : 128.09496305,
                  "L" : 113.084064015,
                  "M" : 131.040484645,
                  "N" : 114.04292747,
                  "O" : 237.147726925,
                  "P" : 97.052763875,
                  "Q" : 128.05857754,
                  "R" : 156.10111105,
                  "S" : 87.032028435,
                  "T" : 101.047678505,
                  "U" : 150.953633405,
                  "V" : 99.068413945,
                  "W" : 186.07931298,
                  "Y" : 163.063328575,
                  "B" : 0.0,
                  "X" : 0.0,
                  "Z" : 0.0,
                  "#" : 0.0}
""" Monoisotopic mass of all amino acids."""

WATER_MASS = 18.01528
"""Mass of a water molecule."""
WATER_MASS_MONO = 18.0105647
"""Monoisotopic mass of a water molecule."""

# Biochemistry Stryer 7th
AA_PKA_S = {"Nterm" : 8.0,
            "C" : 8.3,
            "D" : 4.1,
            "E" : 4.1,
            "H" : 6.0,
            "K" : 10.8,
            "R" : 12.5,
            "Y" : 10.9,
            "Cterm" : 3.1}
"""pKa of important amino acid to compute pI (from Stryer)."""
# IPC_peptide
AA_PKA_IPC = {"Nterm" : 9.564,
              "C" : 8.297,
              "D" : 3.887,
              "E" : 4.317,
              "H" : 6.018,
              "K" : 10.517,
              "R" : 12.503,
              "Y" : 10.071,
              "Cterm" : 2.383}
"""pKa of important amino acid to compute pI (from IPC_peptide. See http://isoelectric.org/theory.html for details)."""
# IPC_peptide2
AA_PKA_IPC_2 = {"Nterm" : 7.947,
              "C" : 9.454,
              "D" : 3.969,
              "E" : 4.507,
              "H" : 6.439,
              "K" : 8.165,
              "R" : 11.493,
              "Y" : 9.153,
              "Cterm" : 2.977}
"""pKa of important amino acid to compute pI (from IPC_peptide2. See http://www.ipc2-isoelectric-point.org/ for details)."""

def handle_errors(message="", err=1, error_type=""):
    """Custom handling of errors and warnings.

    :param message: error message to print
    :param err: Type of message
    :param error_type: header of error to print
    :type message: str
    :type err: int
    :type error_type: str

    *Type of message* is:\n
    - **0** for critical error (exit)\n
    - **1** for warning (no exit, default)\n
    - **2** for print in stderr

    """

    if err == 0:
        print(error_type + "Error: " + message, file=sys.stderr)
        sys.exit(1)
    elif err == 2:
        print(error_type + message, file=sys.stderr)
    else:
        print(error_type + "Warning: " + message, file=sys.stderr)

def get_header(fmt="fasta"):
    """Construct a header for output file in `csv` or `tsv`.

    :param fmt: format of header
    :type fmt: str

    :return: formatted header
    :rtype: str or None

    Informations on the header are:\n
    Original_header No_pep Enzyme Cleav_pos Pep_size Pep_mass pI Seq\n
    No header for `fasta` or other format.
    """
    ret = None
    if fmt == "csv":
        separator = ","
    elif fmt == "tsv":
        separator = "\t"
    if fmt == "csv" or fmt == "tsv":
        ret = "Original_header" + separator + "No_peptide" + separator + \
              "Enzyme" + separator + "Cleaving_pos" + separator + \
              "Peptide_size" + separator + "Peptide_mass" + separator + "pI" +\
              separator + "Sequence"
    return ret

def output_results(output_file, all_seq_digested, fmt, quiet, verbose):
    """Output results of digestion in file and optionally in `stdout`.

    :param output_file: the file where to print results, if exist
    :param all_seq_digested: results of digestions
    :param fmt: output format (`csv`, `tsv` or `fasta`)
    :param quiet: quiet mode, no `stdout` message
    :param verbose: verbosity level
    :type output_file: str
    :type all_seq_digested: list(list(:py:class:`~rpg.digest.ResultOneDigestion`))
    :type fmt: str
    :type quiet: bool
    :type verbose: int
    """

    # Not output file
    if not output_file:
        # Header
        header = get_header(fmt)
        # If we have a header to print (csv/tsv)
        if header:
            # Stdout if small verbose
            if verbose < 2 and not quiet:
                print(header)
        # Print all peptides
        for one_seq in all_seq_digested:  # list of list of ResultOneDig
            # For all ResultOneDigestion
            for one_enz_res in one_seq:
                # Print on stdout
                if verbose >= 2:
                    # Big verbose
                    print(one_enz_res.get_more_info())
                    if header:
                        print(header)
                # Default stdout
                if not quiet:
                    print(format(one_enz_res, fmt), end='')
    # Output file exist
    else:
        try:
            with open(output_file, 'w') as outfile:
                # Header
                header = get_header(fmt)
                # If we have a header to print (csv/tsv)
                if header:
                    # Print it in file
                    outfile.write(header + "\n")
                    # Stdout if small verbose
                    if verbose < 2 and not quiet:
                        print(header)
                # Print all peptides
                for one_seq in all_seq_digested:  # list of list of ResultOneDi
                    # For all ResultOneDigestion
                    for one_enz_res in one_seq:
                        # Print results in file
                        outfile.write(format(one_enz_res, fmt))
                        # Print on stdout
                        if verbose >= 2:
                            # Big verbose
                            print(one_enz_res.get_more_info())
                            if header:
                                print(header)
                        # Default stdout
                        if not quiet:
                            print(format(one_enz_res, fmt), end='')
        except IOError:
            handle_errors(output_file + " can't be open in 'w' mode", 0,
                          "File ")

def next_read(file, offset_start, offset_end):
    """ Return each sequence between offsets range of a file
        as a tuple (header, seq) using a generator.
        Can be fasta or fastq, gzipped or not.

    :param file: fasta/fastq file to read
    :param offset_start: offset in the file from where to read
    :param offset_end: offset in the file until where to read
    :type file: str
    :type offset_start: int
    :type offset_end: int
    """
    # Is it a GZIP file?
    test_file = open(file, "rb")
    # Get the first values
    magic = test_file.read(2)
    # Close the file
    test_file.close()

    # Open the file, GZIP or not
    with (gzip.open(file, "rb") if magic == b"\x1f\x8b"
          else open(file, "rb")) as in_file:
        first_line = in_file.readline().decode('utf-8')
        # FASTQ file
        if first_line.startswith("@"):
            # Go to starting offset
            in_file.seek(offset_start)
            # Set current offset
            beg_line_offset = offset_start
            # Read each line from this point
            for line in in_file:
                # Consider this line as a header
                header = line.decode('utf-8').strip()
                # It is a proper fastq header
                if header.startswith("@"):
                    # The beginning of header is in the offset range
                    if beg_line_offset < offset_end:
                        # Get the sequence
                        sequence = in_file.readline().decode('utf-8').strip()
                        # Skip the two next lines
                        in_file.readline()
                        in_file.readline()
                        # Return header and sequence and wait for the next one
                        yield (header, sequence.upper())
                    # Out of offset, stop this loop
                    else:
                        break
                # Current offset
                beg_line_offset = in_file.tell()

        # (multi?)FASTA file
        elif first_line.startswith(">"):
            # Go to starting offset
            in_file.seek(offset_start)
            # Set current offset
            beg_line_offset = offset_start
            # Read each line from this point
            for line in in_file:
                # Consider this line as a header
                header = line.decode('utf-8').strip()
                # It is a proper fasta header
                if header.startswith(">"):
                    # The beginning of header is in the offset range
                    if beg_line_offset < offset_end:
                        # Get the sequence
                        sequence = in_file.readline().decode('utf-8').strip()
                        # Get current offset
                        current_offset = in_file.tell()
                        # Get next line
                        next_l = in_file.readline().decode('utf-8').strip()
                        # While this next line is not a fasta header...
                        while next_l and not next_l.startswith(">"):
                            # Add this to the Sequence
                            sequence += next_l
                            # Get current offset
                            current_offset = in_file.tell()
                            # Get next line
                            next_l = in_file.readline().decode('utf-8').strip()
                        # Next line is a fasta header, go back to its beginning
                        in_file.seek(current_offset)
                        # Return header and sequence and wait for the next one
                        yield (header, sequence.upper())
                    # Out of offset, stop this loop
                    else:
                        break
                # Current offset
                beg_line_offset = in_file.tell()
        # Not a valid file
        else:
            # Stop the generator with the error to show
            raise ValueError("input file format not recognized (%s)"\
                             "." % first_line[0])
