=========
CHANGELOG
=========
- `2.0.2 <https://gitlab.pasteur.fr/nmaillet/rpg/-/releases/2.0.2>`_
    Add Elastase, #45

    Update tmpdir to tmp_path in tests

- `2.0.1 <https://gitlab.pasteur.fr/nmaillet/rpg/-/releases/2.0.1>`_
    Fix argparse bug preventing -h option to correctly be displayed

    Correct typo

- `2.0.0 <https://gitlab.pasteur.fr/nmaillet/rpg/-/releases/2.0.0>`_
    Tested on Python 3.10 et 3.11
    
    Adding a two enzymes (43 and 44), Asp-N without cleaving Cysteines and ProAlanase
    
    Prevent RPG to take more CPUs than -c option
    
    Adding monoisotopic masses with option -w mono
    
    Adding an enzyme in non-interactive mode is now possible, using options -x to define the cleaving rules, -y to give the name of the enzyme and optionally -z to define exceptions
    
    Removing a user-define enzyme is now possible, using -b option
    
    -e option now accepts enzymes name (case-insensitive) and not only id
    
    Adding an option to compute all theoretical peptides with at most N miscleavages

- `1.2.4 <https://gitlab.pasteur.fr/nmaillet/rpg/-/releases/1.2.4>`_
    Remove 'deprecated' for IPC v1

- 1.2.3
    Add IPC2 pKa values (thanks Lukasz Kozlowski, see https://doi.org/10.1093/nar/gkab295). Add RPG's publication on documentation

- `1.2.2 <https://gitlab.pasteur.fr/nmaillet/rpg/-/releases/1.2.2>`_
    Correct a major bug arising when a new enzyme is define with at least 3 amino acids while the first one being the cleaving site

- 1.2.1
    Add functional tests

- 1.2.0
    Input files can be gzipped

    Input file can be processed in parallel (-c options for the number of processes to use)

    Remove Python 3.5 compatibility

- `1.1.0 <https://gitlab.pasteur.fr/nmaillet/rpg/-/releases/1.1.0>`_
    Modify input. Now, option -i only takes files. Use option -s to input sequence

- 1.0.9
    Correct a bug of random dict in the creation of new enzyme

    Modifying auto repr of a rule and argument name

    Fixing typo

- 1.0.8
    Adding doc for -p option

    Fixing typo

- 1.0.7
    Adding choice for pKa values (option -p)

    Fixing alphabetic order for enzymes

- 1.0.6
    No default output file, only stdout

    Fixing -e and -m behavior

- 1.0.5
    Fix version date inside RPG

- 1.0.4
    Fix version number inside RPG

- 1.0.3
    Support of Python 3.7

    Does not support Python 3.4

- 1.0.2
    Correct minor but funny typo

- 1.0.1
    Minor change in enzymes definition in user guide

- 1.0.0
    Correct a bug when to rules were applying at the same time

    Update user-guide

    Beta to stable

- 0.7.0
    Add the last 7 enzymes

    Correct block-code in user-guide

- 0.6.1
    Add 7 enzymes

    Correct some typo

- 0.6.0
    Finish docs

    Minor change in user-define enzymes
    
    Alpha to Beta version

- 0.5.4
    Bugfix: protect new enzyme name when a new enzyme is directly inputted

- 0.5.3
    Writing Doc

- 0.5.2
    Incorporating tests, rtfd and Gitlab