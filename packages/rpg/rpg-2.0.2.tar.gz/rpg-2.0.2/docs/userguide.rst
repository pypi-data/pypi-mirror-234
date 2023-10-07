==========
User Guide
==========


Overview
========

You can run **Rapide Peptides Generator** using the standalone version called:

.. code-block:: shell

    rpg

You can obtain help by using:

.. code-block:: shell

    rpg --help


Installation
============

From pip
--------

The suggested way of installing the latest **RPG** version is through **pip**:

.. code-block:: shell

    pip3 install rpg

Then you can use:

.. code-block:: shell

    rpg --help

From source code
----------------

**RPG** is coded in Python. To manually install it from source, get the source and install **RPG** using:

.. code-block:: shell

    git clone https://gitlab.pasteur.fr/nmaillet/rpg/
    cd rpg
    python setup.py install

Using without installation
--------------------------

You can download the source code from Pasteur's **Gitlab**: https://gitlab.pasteur.fr/nmaillet/rpg/.

In order to directly run **RPG** from source, you need to copy file ``tests/context.py`` into ``rpg`` folder.

Then, uncomment line 42 of ``rpg/RapidPeptidesGenerator.py``. Modify:

.. code-block:: python

    #from context import rpg

To:

.. code-block:: python

    from context import rpg

Then, from the main **RPG** directory, use:

.. code-block:: shell

    python3 rpg/RapidPeptidesGenerator.py -\\-help

.. warning:: Using without installation is not recommended, as you need all requirements of `requirements.txt` installed locally and you may encounter issues with Sphinx autodoc or other unwanted behaviors.


Classical use
=============

Here are some typical examples of **RPG** usage.

Getting help
------------

To access build-in help, use:

.. code-block:: shell

    rpg -\\-help

Listing enzymes
---------------

To list all available enzymes, use:

.. code-block:: shell

    rpg -l

Performing digestion
--------------------

There are two digestion modes in **RPG**. In sequential mode, each protein will be digested by each enzyme, one by one. In concurrent mode, all enzymes are present at the same time during digestion. See :ref:`digestion` for more information.

.. _oneseq:

Sequential digestion of one sequence
""""""""""""""""""""""""""""""""""""

To perform sequential digestion of the sequence "QWSDORESDF" with enzymes 2 and 5 and store results in `output_file.fasta`, use:

.. code-block:: shell

    rpg -s QWSDORESDF -o output_file.fasta -e 2 5

.. _onefile:

Sequential digestion of a (multi)fasta file
"""""""""""""""""""""""""""""""""""""""""""

To perform sequential digestion of `input_file.fasta` with enzymes 2 and 5 and store results in `output_file.fasta`, use:

.. code-block:: shell

    rpg -i input_file.fasta -o output_file.fasta -e 2 5

Concurrent digestion of a (multi)fasta file
"""""""""""""""""""""""""""""""""""""""""""

To perform concurrent digestion of `input_file.fasta` with enzymes 2 and 5 and store results in `output_file.fasta`, use:

.. code-block:: shell

    rpg -i input_file.fasta -o output_file.fasta -e 2 5 -d c

Adding a new enzyme
-------------------

To extend the list of the available enzymes and add a new one, use:

.. code-block:: shell

    rpg -a

See :ref:`addenzyme` for more information.


Options
=======

Here are all available options in **RPG**:

**-h, -\\-help**: Show this help message and exit.

**-a, -\\-addenzyme**: Add a new user-defined enzyme. See :ref:`addenzyme` for more information.

**-b, -\\-delenzyme**: Delete a user-define enzyme. See :ref:`delenzyme` for more information.

**-d, -\\-digest**: Digestion mode. Either 's', 'sequential', 'c' or 'concurrent' (default: s). See :ref:`digestion` for more information.

**-e, -\\-enzymes**: Enzyme(s) id number or name to use (*e.g.* -e 1 Asp-N 10 to use enzymes 1, Asp-N and 10). Use -l first to get enzyme ids. See :ref:`enzymes` for more information.

**-f, -\\-fmt**: Output file format. Either 'fasta', 'csv', or 'tsv' (default: fasta). See :ref:`formats` for more information.

**-i, -\\-inputdata**: Input file, in (multi)fasta / fastq format (gzipped or not). See :ref:`onefile` for example.

**-s, -\\-sequence**:  Input a single protein sequence without commentary. See :ref:`oneseq` for example.

**-l, -\\-list**: Display the list of available enzymes.

**-m, -\\-miscleavage**: Percentage of miscleavage, between 0 and 100, by enzyme(s). It should be in the same order as the -\\-enzymes options (*e.g.* -m 15 5.2 10). It works only for sequential digestion (default: 0). See :ref:`miscleavage` for more information.



**-t, -\\-theoretical**: Maximum number of miscleavages, by enzyme(s). RPG will produce all theoretical peptides allowing at most -t miscleavages. It should be in the same order than -\\-enzymes options (*e.g.* -t 1 3 2). Only for sequential digestion (default: 0). See :ref:`theoretical` for more information.


**-n, -\\-noninteractive**: Non-interactive mode. No standard output, only error(s) (-\\-quiet enable, overwrite -v). If output filename already exists, output file will be overwritten. See :ref:`nointer` for more information.

**-x, -\\-cleave**: Cleavage site(s) when adding enzyme in non-interactive mode (*e.g.* -x "(D or E,)", similar to -x "(D,)" "(E,)". See :ref:`addenzyme` for more information.

**-z, -\\-exception**: Exception(s) when adding enzyme in non-interactive mode (*e.g.* -z "(D,)(W)" "(D,)(A)". See :ref:`addenzyme` for more information.

**-y, -\\-enzname**: Enzyme's name when adding enzyme in non-interactive mode. See :ref:`addenzyme` for more information.

**-o, -\\-outputfile**: Result file to output resulting peptides (default './peptides.xxx' depending of -\\-fmt).

**-p, -\\-pka**: Define pKa values. Either 'ipc2', 'stryer' or 'ipc' (default: ipc2). IPC2 values come from `IPC_peptide in Supplementary Table S1 <https://doi.org/10.1093/nar/gkab295>`_, Stryer values from Biochemistry Stryer, 7th edition and IPC values from `IPC_peptide <http://isoelectric.org/theory.html>`_.

**-w, -\\-mass**: Define atomic mass values. Either 'avg' for average mass or 'mono' for monoisotopic mass.

**-r, -\\-randomname**: Random (not used) output name file. See :ref:`random` for more information.

**-c , -\\-processes**: Number of parallel processes to use (default: 1)

**-q, -\\-quiet**: No standard output, only error(s).

**-v, -\\-verbose**: Increase output verbosity. -vv will increased more than -v. See :ref:`verbose` for more information.

**-\\-version**: Show program's version number and exit.


.. _digestion:

Digestion modes
===============

There are two digestion modes in **RPG**. In 'sequential' mode, each protein will be digested by each enzyme, one by one. Launching 3 times **RPG** on the same protein with 3 different enzymes or launching one time **RPG** on the protein with the 3 enzymes in 'sequential' mode leads to exactly the same result.

In concurrent mode, all enzymes are present at the same time during digestion and exposure time is supposed to be infinite, *i.e.* all possible cleavages **will** occur (there is no miscleavage). In this mode, the cleavage of a first enzyme can make available the cleavage site of another enzyme.

Let's define two enzymes. The first is called 'afterP' (id 28) and cleaves after P. The second is called 'afterK' (id 29) and cleaves after K if there is no P just before. Digesting 'PKPKPKPK' using those two enzymes in sequential mode gives the following result (see :ref:`formats` for more information):

.. code-block:: shell

    $ rpg -s PKPKPKPK -e 28 29
    >Input_0_afterP_1_1_115.13198_5.54
    P
    >Input_1_afterP_3_2_243.30608_9.4
    KP
    >Input_2_afterP_5_2_243.30608_9.4
    KP
    >Input_3_afterP_7_2_243.30608_9.4
    KP
    >Input_4_afterP_8_1_146.18938_9.4
    K
    >Input_0_afterK_0_8_919.17848_11.27
    PKPKPKPK

'afterP' cleaves as expected and 'afterK' is not able to cleave anything.

Digesting 'PKPKPKPK' using those two enzymes in concurrent mode gives the following result:

.. code-block:: shell

    $ rpg -s PKPKPKPK -e 28 29 -d c
    >Input_0_afterP-afterK_1_1_115.13198_5.54
    P
    >Input_1_afterP-afterK_2_1_146.18938_9.4
    K
    >Input_2_afterP-afterK_3_1_115.13198_5.54
    P
    >Input_3_afterP-afterK_4_1_146.18938_9.4
    K
    >Input_4_afterP-afterK_5_1_115.13198_5.54
    P
    >Input_5_afterP-afterK_6_1_146.18938_9.4
    K
    >Input_6_afterP-afterK_7_1_115.13198_5.54
    P
    >Input_7_afterP-afterK_8_1_146.18938_9.4
    K

Here, we have to understand that 'afterP' cleaves at the same positions as in sequential mode and the products (mostly 'KP') are then cleaved by 'afterK'. Indeed, there is no more P before K, making 'afterK' able to cleave.

Default mode is 'sequential'. Reminder: you can input miscleavage values only for this mode.


.. _miscleavage:

Miscleavage
===========

Sometimes an enzyme does not cleave at a given position even if requirements are fulfilled. This event is called miscleavage and can have biological, chemical or physical origins. To take into account this behavior in **RPG**, one can assign a miscleavage value to an enzyme, expressed as a **percentage**.

For example, using:

.. code-block:: shell

    rpg -s QWSDORESDF -e 1 2 3 -m 1.4 2.6

will assign a miscleavage probability of `1.4%` to enzyme `1`, a miscleavage probability of `2.6%` to enzyme `2` and a miscleavage probability of `0%` to enzyme `3` (default behavior). For enzyme `1`, each cleavage will then have a probability of 0.014 to **not** occur.


.. _theoretical:

All theoretical miscleavage
===========================

You can compute all theoretical peptides with at most **n** miscleavages. **RPG** will then produce all peptides without any miscleavage, with 1 miscleavage, with 2 miscleavage, etc, up to **n**.

For example:

.. code-block:: shell

    $ rpg -s AAWBBBWCCCWD -e 3 -t 1
    >Input_0_BNPS-Skatole_3_3_346.38608_5.46
    AAW
    >Input_1_BNPS-Skatole_7_4_204.22848_5.46
    BBBW
    >Input_2_BNPS-Skatole_11_4_513.64488_5.45
    CCCW
    >Input_3_BNPS-Skatole_12_1_133.10388_3.48
    D
    >Input_4_BNPS-Skatole_7_7_532.59928_5.46
    AAWBBBW
    >Input_5_BNPS-Skatole_11_8_699.85808_5.45
    BBBWCCCW
    >Input_6_BNPS-Skatole_12_5_628.73348_3.48
    CCCWD
    >Input_7_BNPS-Skatole_11_11_1028.22888_5.45
    AAWBBBWCCCW
    >Input_8_BNPS-Skatole_12_9_814.94668_3.48
    BBBWCCCWD


.. _nointer:

Non-interactive mode
====================

Option **-n, -\\-noninteractive** force **RPG** to not print any standard output, only error(s) are displayed in the shell. It enable '-\\-quiet' option and overwrites -\\-verbose option. If output filename already exists, the output file will be systematically overwritten. This option is mostly used in cluster or pipeline when user does not want **RPG** to wait for input or display anything but errors.


.. _formats:

Output
======

Output of **RPG** contains the following information in one line for each generated peptide, in this order:

    - Header of original sequence or 'Input' if the sequence is directly inputed in **RPG**, *i.e.*, **-s**
    - Sequential numbering (starting from 0) of out-coming peptides for each of original sequence
    - Enzyme name used to obtain this peptide
    - Cleavage position on the original sequence (0 if no cleavage occurs)
    - Peptide size
    - Peptide molecular weight estimation
    - Peptide isoelectric point estimation (pI)

Then, on the next line:

    - Peptide sequence

Peptide molecular weight approximation is computed as the addition of average isotopic masses of each amino acid present in the peptide. Then the average isotopic mass of one water molecule is added to it. Molecular weight values are given in Dalton (Da). It does not take into consideration any digestion-induced modifications.

The isoelectric point is computed by solving Henderson–Hasselbalch equation using binary search. It is based on Lukasz P. Kozlowski work (http://isoelectric.org/index.html).

The default output is in multi-fasta format. The header then summarizes all this information. For example, on the following multi-fasta result:

.. code-block:: shell

    >Input_0_Asp-N_3_3_419.43738_5.54
    QWS
    >Input_1_Asp-N_8_5_742.78688_4.16
    ...

we can see that a sequence was directly inputed in **RPG** `(Input)`, the first peptide `(0)` was obtained with `Asp-N` and this enzyme cleaved after the `3rd` amino acid in the original sequence. The peptide has a size of `3` amino acids, a molecular weight estimated at `419.43738` Da and a theoretical isoelectric point of `5.54`. The full sequence is then written `(QWS)`. The output of the remaining peptides follows in the same format.

More information can be outputted using :ref:`verbose` option.


.. _random:

Random names
============

Option **-r, -\\-randomname** force **RPG** to use a random name for output file. When using it, **RPG** will not ask user output file name **nor location**. The output file will be created in the working directory. This option is generally used for testing or automatic tasks.


.. _verbose:

Verbosity
=========

Verbosity can be increased or decreased. The output file is not affected by **-v** or **-q** options.

With default verbosity level (no **-v** nor **-q** option), the output is:

.. code-block:: shell

    $ rpg -s QWSDORESDF -e 1
    >Input_0_Asp-N_3_3_419.43738_5.54
    QWS
    >Input_1_Asp-N_8_5_742.78688_4.16
    DORES
    >Input_2_Asp-N_10_2_280.28048_3.6
    DF

Increasing verbosity by one, *i.e.* using **-v**, adds information about used options. For example:

.. code-block:: shell

    $ rpg -s QWSDORESDF -e 1 -v
    Warning: File 'peptides.fasta' already exit!
    Overwrite it? (y/n)
    y
    Input: QWSDORESDF
    Enzyme(s) used: ['Asp-N']
    Mode: sequential
    miscleavage ratio: [0]
    Output file: /Users/nmaillet/Prog/RPG/peptides.fasta
    >Input_0_Asp-N_3_3_419.43738_5.54
    QWS
    >Input_1_Asp-N_8_5_742.78688_4.16
    DORES
    >Input_2_Asp-N_10_2_280.28048_3.6
    DF

Increasing verbosity by two, *i.e.* using **-vv**, also adds statistics about each of the digested proteins. For example:

.. code-block:: shell

    $ rpg -s QWSDORESDF -e 1 -vv
    Warning: File 'peptides.fasta' already exit!
    Overwrite it? (y/n)
    y
    Input: QWSDORESDF
    Enzyme(s) used: ['Asp-N']
    Mode: sequential
    miscleavage ratio: [0]
    Output file: /Users/nmaillet/Prog/RPG/peptides.fasta

    Number of cleavage: 2
    Cleavage position: 3, 8
    Number of miscleavage: 0
    miscleavage position: 
    miscleavage ratio: 0.00%
    Smallest peptide size: 2
    N terminal peptide: QWS
    C terminal peptide: DF
    >Input_0_Asp-N_3_3_419.43738_5.54
    QWS
    >Input_1_Asp-N_8_5_742.78688_4.16
    DORES
    >Input_2_Asp-N_10_2_280.28048_3.6
    DF

Decreasing verbosity, *i.e.* using **-q** option, removes all information but errors. For example:

.. code-block:: shell

    $ rpg -s QWSDORESDF -e 1 -q 
    Warning: File 'peptides.fasta' already exit!
    Overwrite it? (y/n)
    y


.. _addenzyme:

Creating a new enzyme
=====================

Option **-a, -\\-addenzyme** allows the user to define new enzymes. An enzyme contains one or several rules and exceptions.

In the following, nomenclature of `Schechter and Berger <https://www.ncbi.nlm.nih.gov/pubmed/6035483>`_ is used. Amino acids before the cleavage site are designated as `P1`, `P2`, `P3`, etc in the N-terminal direction, and as `P1'`, `P2'`, `P3'`, etc in the C-terminal direction. For example, with cleavage site represented as '|':

.. code-block:: none

    ...P3-P2-P1-|-P1'-P2'-P3'...

In **RPG**, this nomenclature is represented as:

.. code-block:: none

    ...(P3)(P2)(P1)(,)(P1')(P2')(P3')...


Definition of rules
-------------------

A rule specifies which amino acid is targeted by the enzyme, the cleavage position (*i.e.* **before** or **after** the targeted amino acid) and optionally the surrounding context. Each amino acid must be included in parentheses, *i.e.* '**(**' and '**)**' and the cleavage position is represented by a comma, *i.e.* '**,**'. The comma must always be directly before or after an closing or opening parenthesis, respectively.

For example, to define a cleavage occurring **before** A, one must input:

.. code-block:: none

    (,A)

To define a cleavage occurring **after** B, one must input:

.. code-block:: none

    (B,)

The surrounding context is specified by adding other amino acids, before or after the targeted one. For example, to define a cleavage occurring **before** A, position `P1'`, preceded by B in position `P1`, C in position `P3` and followed by D in position `P2'`, one must input:

.. code-block:: none

    (C)()(B)(,A)(D)

Note that this enzyme will only cleave if it finds the motif C*BAD, where * could be **any** amino acid. It will **not** cleave BAD, nor C*BA, BA, etc. For example, creating and using enzyme `rpg_example_userguide` (enzyme id 46):

.. code-block:: none

    $ rpg -a    
    Name of the new enzyme?
    rpg_example_userguide
    Create a cleaving rule (c) or an exception (e)? (q) to quit:
    c
    Write your cleaving rule, (q) to quit:
    (C)()(B)(,A)(D)
    Create a cleaving rule (c) or an exception (e)? (q) to quit:
    q
    Add another enzyme? (y/n)
    n

    $ rpg -s CWBADE -e 46
    >Input_0_rpg_example_userguide_3_3_307.36728_5.46
    CWB
    >Input_1_rpg_example_userguide_6_3_333.29818_3.4
    ADE

    $ rpg -s FAD -e 46
    >Input_0_rpg_example_userguide_0_3_351.35928_3.6
    FAD


In order for this enzyme to also cleave before AD (before A in `P1'` followed by D in `P2'` ), on top of the previous rule, one has to define one more rule in **RPG**:

.. code-block:: none

    (,A)(D)
    (C)()(B)(,A)(D)

It is important to note that for each enzyme, it is enough that one of the rule is broken for the cleavage to not occur. In this example, the defined enzyme will **not** cleave BAD, as it is specified that it will cleave before A preceded by B in `P1` **if there is C in `P3`**. Identically, it will **not** cleave C*BA*, as D is required in `P2'` for both rules.


.. code-block:: shell

    $rpg -a
    Name of the new enzyme?
    rpg_example_userguide
    Create a cleaving rule (c) or an exception (e)? (q) to quit:
    c
    Write your cleaving rule, (q) to quit:
    (,A)(D)
    Create a cleaving rule (c) or an exception (e)? (q) to quit:
    c
    Write your cleaving rule, (q) to quit:
    (C)()(B)(,A)(D)
    Create a cleaving rule (c) or an exception (e)? (q) to quit:
    q
    Add another enzyme? (y/n)
    n

    $ rpg -s CWBADE -e 46
    >Input_0_rpg_example_userguide_3_3_307.36728_5.46
    CWB
    >Input_1_rpg_example_userguide_6_3_333.29818_3.4
    ADE

    $ rpg -s FAD -e 46
    >Input_0_rpg_example_userguide_1_1_165.19188_5.54
    F
    >Input_1_rpg_example_userguide_3_2_204.18268_3.6
    AD

    $ rpg -s BAD -e 46
    >Input_0_rpg_example_userguide_0_3_204.18268_3.6
    BAD

The order of inputted rules is not relevant. In other words, this enzyme:

.. code-block:: none

    (,A)(D)
    (C)()(B)(,A)(D)

and this second one:

.. code-block:: none

    (C)()(B)(,A)(D)
    (,A)(D)

are identical.

It is possible to define none-related cleavage rules for the same enzyme, for example:

.. code-block:: none

    (G,)(G)
    (P)(W,)(E)(T)

This enzyme will cleave after G (position `P1`) followed by G in `P1'` and also after W (`P1`) preceded by P in `P2` and followed by E in `P1'` and T in `P2'`.

Note that each rule must concern only **one** cleavage site. It is not possible to input rule like:

.. code-block:: none

    (A,)(B,)

This would define an enzyme cleaving after A in `P1` followed by B in `P1'` but also cleaving after B in `P1` preceded by A in `P2`. The proper way to input this is by using two separate rules:

.. code-block:: none

    (A,)(B)
    (A)(B,)

However, it is possible to write rules in a more efficient way as explained in :ref:`easy`.


Definition of exceptions
------------------------

An exception specifies when a cleavage should **not** occur. **Exceptions must always be linked to a rule**.

For example, to define a cleavage occurring **before** A (`P1'` ), one must input:

.. code-block:: none

    (,A)

Exceptions can then be inputted. For example, to define "a cleavage occurs before A, except when P is in `P2'` ", the following exception needs to be added:

.. code-block:: none

    (,A)(P)

This enzyme will always cleave before A when not followed by P:

.. code-block:: shell

    rpg -a
    Name of the new enzyme?
    rpg_example_userguide
    Create a cleaving rule (c) or an exception (e)? (q) to quit:
    c
    Write your cleaving rule, (q) to quit:
    (,A)
    Create a cleaving rule (c) or an exception (e)? (q) to quit:
    e
    Write your exception rule, (q) to quit:
    (,A)(P)
    Create a cleaving rule (c) or an exception (e)? (q) to quit:
    q
    Add another enzyme? (y/n)
    n
    
    rpg -s CWBADE -e 46
    >Input_0_rpg_example_userguide_3_3_307.36728_5.46
    CWB
    >Input_1_rpg_example_userguide_6_3_333.29818_3.4
    ADE
    
    rpg -s CWBAPE -e 46
    >Input_0_rpg_example_userguide_0_6_604.67828_3.6
    CWBAPE

It is possible to input complex exceptions. For the previous enzyme, we can add the following exception:

.. code-block:: none

    (G)(T)()(,A)()(F)

This enzyme will always cleave before A (`P1'` ) when not followed by P (`P2'` ) or preceded by G in `P3`, T in `P2`, by any amino acid in `P1` and `P2'`, and F in `P3'` **at the same time**:

.. code-block:: shell

    rpg -a             
    Name of the new enzyme?
    rpg_example_userguide
    Create a cleaving rule (c) or an exception (e)? (q) to quit:
    c
    Write your cleaving rule, (q) to quit:
    (,A)
    Create a cleaving rule (c) or an exception (e)? (q) to quit:
    e
    Write your exception rule, (q) to quit:
    (,A)(P)
    Create a cleaving rule (c) or an exception (e)? (q) to quit:
    e
    Write your exception rule, (q) to quit:
    (G)(T)()(,A)()(F)
    Create a cleaving rule (c) or an exception (e)? (q) to quit:
    q
    Add another enzyme? (y/n)
    n
    
    rpg -s CWBADE -e 46
    >Input_0_rpg_example_userguide_3_3_307.36728_5.46
    CWB
    >Input_1_rpg_example_userguide_6_3_333.29818_3.4
    ADE
    
    rpg -s CWBAPE -e 46
    >Input_0_rpg_example_userguide_0_6_604.67828_3.6
    CWBAPE
    
    rpg -s GTBAMF -e 46
    >Input_0_rpg_example_userguide_0_6_525.62028_5.54
    GTBAMF

    rpg -s GTBAPE -e 46
    >Input_0_rpg_example_userguide_0_6_473.48328_3.6
    GTBAPE
    
    rpg -s GTBAME -e 46
    >Input_0_rpg_example_userguide_3_3_176.17228_5.54
    GTB
    >Input_1_rpg_example_userguide_6_3_349.40218_3.6
    AME

It is important to understand that an exception should always be linked to a rule. If one inputs this rule:

.. code-block:: none

    (A,)

followed by this exception:

.. code-block:: none

    (B,)(C)

the exception will not be taken into account. This enzyme will just always cleave after A.



.. _easy:

Easily writing complex enzymes
------------------------------

To make enzyme creation easier to use, two tricks are available.

The first one simplifies the definition of enzymes cleaving **before** and **after** a given amino acid. Defining an enzyme cleaving, for example, before **and** after A, can be done with two rules:

.. code-block:: none

    (,A)
    (A,)

or simply using:

.. code-block:: none

    (,A,)

The second trick is the use of the keyword `or`. This allows multiple possibilities for on position. For example:

.. code-block:: none

    (,A or B)

is equivalent to:

.. code-block:: none

    (,A)
    (,B)

.. warning:: do not input ``(,A or ,B)``, as a comma must always directly preceding or following a parenthesis.

Those two tricks help on complex enzymes. For example, :ref:`peps13` preferentially cleaves around F or L, sometimes before, sometimes after, depending on the context. More specifically, it will not cleave before F or L in `P1'` followed by P in `P2'`. It will not cleave before F or L in `P1'` preceded by R in `P1` or P in `P2` or H/K/R in `P3`. It will not cleave after F or L in `P1` followed by P in `P2'`. And it will not cleave after F or L in `P1` preceded by P in `P2` or H/K/R in `P3`.

It can be defined either by:

.. code-block:: none

    cleaving rules:

    (F,)
    (L,)
    (,F)
    (,L)

    exception rules:

    (,F)(P)
    (,L)(P)
    (R)(,F)
    (R)(,L)
    (P)()(,F)
    (P)()(,L)
    (H)()()(,F)
    (K)()()(,F)
    (R)()()(,F)
    (H)()()(,L)
    (K)()()(,L)
    (R)()()(,L)
    (F,)()(P)
    (L,)()(P)
    (P)(F,)
    (P)(L,)
    (H)()(F,)
    (K)()(F,)
    (R)()(F,)
    (H)()(L,)
    (K)()(L,)
    (R)()(L,)

or, in a condensed way:

.. code-block:: none

    cleaving rule:

    (,F or L,)

    exception rules:

    (,F or L)(P)
    (R)(,F or L)
    (P)()(,F or L)
    (H or K or R)()()(,F or L)
    (F or L,)()(P)
    (P)(F or L,)
    (H or K or R)()(F or L,)

Those two definitions are completely equivalent for **RPG**.


Example of enzymes
------------------

All available enzymes are in :ref:`enzymes`, including their **RPG**'s definition.

Non-interactive mode
--------------------

Using **-n, -\\-noninteractive** and **-a, -\\-addenzyme** options together is possible, but then requires to also use **-x, -\\-cleave** option to define cleaving site(s), **-y, --enzname** option to define the name of the enzyme and optionally **-z, --exception** option to define exceptions.


.. _delenzyme:

Deleting user-defined enzymes
=============================

All user-defined enzymes are stored in ``~/rpg_user.py``. This file is automatically generated by **RPG** and written in **Python**.

Each enzyme definition starts with:

.. code-block:: python

    # User-defined enzyme <name of the enzyme>

and finishes with:

.. code-block:: python

    CPT_ENZ += 1

followed by 3 blank line.

To remove an enzyme, use the option **-b, -\\-delenzyme** with the id or name of the user-defined enzyme to remove. It is not possible to remove predefined enzymes of **RPG**.

To remove all user-defined enzymes, just delete ``~/rpg_user.py`` file. It will be created again (empty) at the next launch of **RPG**.

Obviously, all deleted enzymes can not be recovered. If one wants to use them again they will need to be redefined in **RPG**, using **-a, -\\-addenzyme** option.
