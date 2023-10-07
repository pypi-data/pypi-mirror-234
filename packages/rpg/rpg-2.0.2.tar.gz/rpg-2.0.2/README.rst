RapidPeptidesGenerator (RPG)
============================

Rapid Peptides Generator (RPG) is a software dedicated to predict proteases-induced cleavage sites on amino acid sequences.

.. image:: https://badge.fury.io/py/rpg.svg
    :target: https://badge.fury.io/py/rpg
    :alt: Pypi repo

.. image:: https://gitlab.pasteur.fr/nmaillet/rpg/-/badges/release.svg
    :target: https://gitlab.pasteur.fr/nmaillet/rpg/-/releases
    :alt: Latest release

.. image:: https://gitlab.pasteur.fr/nmaillet/rpg/badges/master/pipeline.svg
    :target: https://gitlab.pasteur.fr/nmaillet/rpg/commits/master
    :alt: Build Status

.. image:: https://gitlab.pasteur.fr/nmaillet/rpg/badges/master/coverage.svg
    :target: https://gitlab.pasteur.fr/nmaillet/rpg/commits/master
    :alt: Coverage Report

.. image:: https://readthedocs.org/projects/rapid-peptide-generator/badge/?version=latest
    :target: https://rapid-peptide-generator.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

:note: RPG is tested with Gitlab Ci for the following Python version: 3.6 to 3.11
:issues: Please use https://gitlab.pasteur.fr/nmaillet/rpg
:publication: To cite RPG, please refer to https://doi.org/10.1093/nargab/lqz004


Overview
========

Rapid Peptides Generator (RPG), is a standalone software dedicated to predict proteases-induced cleavage sites on sequences.

RPG is a python tool taking a (multi-)fasta/fastq file (gzipped or not) of proteins as input and digest each of them. The digestion mode can be either 'concurrent', i.e. all enzymes are present at the same time during digestion, or 'sequential'. In sequential mode, each protein will be digested by each enzyme, one by one.

The resulting peptides contain information about positions of cleavage site, peptide sequences, length, mass as-well as an estimation of isoelectric point (pI) of each peptide. Shortly, the isoelectric point is the pH at which a peptide carries no net electrical charge and a good approximation can be computed on small molecules. Results are outputted in multi-fasta, CSV or TSV file.

Currently, 45 enzymes and chemicals are included in RPG. The user can easily design new enzymes, using a simple yet powerful grammar. This grammar allows the user to design complex enzymes like trypsin or thrombin, including many exceptions and different cleavage sites. User-defined enzymes are then interpreted by RPG and included in the local installation of the software.

RPG follows the standards for software development with continuous integration on Gitlab (https://gitlab.pasteur.fr/nmaillet/rpg) and automatic on-line documentation (https://rapid-peptide-generator.readthedocs.io).



Installation
============

In order to install RPG, you can use **pip**:

.. code-block:: shell

    pip3 install rpg

This command installs RPG and its Python dependencies.


Usage
=====

From the command line:

.. code-block:: shell

    rpg --help
