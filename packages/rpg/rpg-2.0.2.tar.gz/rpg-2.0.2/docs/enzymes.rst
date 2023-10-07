.. _enzymes:

==================
Enzyme definitions
==================
All default available enzymes (`enzymes_definition.py`) are listed bellow.

For each of them, there is the equivalent in `RPG` grammar.

In the following, nomenclature of `Schechter and Berger <https://www.ncbi.nlm.nih.gov/pubmed/6035483>`_ is used. Amino acids before the cleavage site are designated as `P1`, `P2`, `P3`, etc in the N-terminal direction, and as `P1'`, `P2'`, `P3'`, etc in the C-terminal direction. For example, with cleavage site represented as '|':

.. code-block:: none

    ...P3-P2-P1-|-P1'-P2'-P3'...

In **RPG**, this nomenclature is represented as:

.. code-block:: none

    ...(P3)(P2)(P1)(,)(P1')(P2')(P3')...

-----------------
Available enzymes
-----------------

==================  ==================  ==================
1: :ref:`arg-c`     2: :ref:`asp-n`     3: :ref:`bnps`
4: :ref:`brom`      5: :ref:`casp1`     6: :ref:`casp2`
7: :ref:`casp3`     8: :ref:`casp4`     9: :ref:`casp5`
10: :ref:`casp6`    11: :ref:`casp7`    12: :ref:`casp8`
13: :ref:`casp9`    14: :ref:`casp10`   15: :ref:`chymh`
16: :ref:`chyml`    17: :ref:`clost`    18: :ref:`cnbr`
19: :ref:`enter`    20: :ref:`fxa`      21: :ref:`ficin`
22: :ref:`form`     23: :ref:`gluc`     24: :ref:`glue`
25: :ref:`gran`     26: :ref:`hydro`    27: :ref:`iodo`
28: :ref:`lysc`     29: :ref:`lysn`     30: :ref:`neut`
31: :ref:`ntcb`     32: :ref:`pap`      33: :ref:`peps13`
34: :ref:`peps2`    35: :ref:`prol`     36: :ref:`protk`
37: :ref:`staphI`   38: :ref:`therm`    39: :ref:`throm`
40: :ref:`thromsg`  41: :ref:`tev`      42: :ref:`tryps`
43: :ref:`asp-n2`   44: :ref:`proa`     45: :ref:`elast`
==================  ==================  ==================

.. _arg-c:

Arg-C
.....

Arg-C proteinase preferentially cleaves after R (`P1`)

**RPG definition:**

cleaving rule:

* ``(R,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#ArgC



.. _asp-n:

Asp-N
.....

Asp-N Sequencing Grade preferentially cleaves before C or D (`P1'` )

**RPG definition:**

cleaving rule:

* ``(,C or D)``

More information: https://france.promega.com/resources/pubhub/using-endoproteinases-asp-n-and-glu-c-to-improve-protein-characterization/



.. _bnps:

BNPS-Skatole
............

BNPS-Skatole preferentially cleaves after W (`P1`)

**RPG definition:**

cleaving rule:

* ``(W,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#BNPS



.. _brom:

Bromelain
.........

Bromelain preferentially cleaves after K, A or Y (`P1`)

**RPG definition:**

cleaving rule:

* ``(K or A or Y,)``

More information: https://www.sigmaaldrich.com/life-science/biochemicals/biochemical-products.html?TablePage=16410479



.. _casp1:

Caspase 1
.........

Caspase 1 preferentially cleaves after D (`P1`) preceded by H, A or T in `P2` and preceded by F, W, Y or L in `P4`. It will not cleave if D is followed by P, E, D, Q ,K or R in `P1'`.

**RPG definition:**

cleaving rule:

* ``(F or W or Y or L)()(H or A or T)(D,)``

exception rule:

* ``(F or W or Y or L)()(H or A or T)(D,)(P or E or D or Q or K or R)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Casp1



.. _casp2:

Caspase 2
.........

Caspase 2 preferentially cleaves after D (`P1`) preceded by DVA or DEH. It will not cleave if D is followed by P, E, D, Q ,K or R in `P1'`. 

**RPG definition:**

cleaving rules:

* ``(D)(V)(A)(D,)``
* ``(D)(E)(H)(D,)``

exception rules:

* ``(D)(V)(A)(D,)(P or E or D or Q or K or R)``
* ``(D)(E)(H)(D,)(P or E or D or Q or K or R)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Casp2



.. _casp3:

Caspase 3
.........

Caspase 3 preferentially cleaves after D (`P1`) preceded by DMQ or DEV. It will not cleave if D is followed by P, E, D, Q ,K or R in `P1'`. 

**RPG definition:**

cleaving rules:

* ``(D)(M)(Q)(D,)``
* ``(D)(E)(V)(D,)``

exception rules:

* ``(D)(M)(Q)(D,)(P or E or D or Q or K or R)``
* ``(D)(E)(V)(D,)(P or E or D or Q or K or R)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Casp3



.. _casp4:

Caspase 4
.........

Caspase 4 preferentially cleaves after D (`P1`) preceded by LEV or (W/L)EH. It will not cleave if D is followed by P, E, D, Q ,K or R in `P1'`. 

**RPG definition:**

cleaving rules:

* ``(L)(E)(V)(D,)``
* ``(W or L)(E)(H)(D,)``

exception rules:

* ``(L)(E)(V)(D,)(P or E or D or Q or K or R)``
* ``(W or L)(E)(H)(D,)(P or E or D or Q or K or R)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Casp4



.. _casp5:

Caspase 5
.........

Caspase 5 preferentially cleaves after D (`P1`) preceded by (W/L)EH.

**RPG definition:**

cleaving rule:

* ``(W or L)(E)(H)(D,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Casp5



.. _casp6:

Caspase 6
.........

Caspase 6 preferentially cleaves after D (`P1`) preceded by VEI or VEH. It will not cleave if D is followed by P, E, D, Q ,K or R in `P1'`. 

**RPG definition:**

cleaving rule:

* ``(V)(E)(I or H)(D,)``

exception rule:

* ``(V)(E)(I or H)(D,)(P or E or D or Q or K or R)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Casp6



.. _casp7:

Caspase 7
.........

Caspase 7 preferentially cleaves after D (`P1`) preceded by DEV. It will not cleave if D is followed by P, E, D, Q ,K or R in `P1'`. 

**RPG definition:**

cleaving rule:

* ``(D)(E)(V)(D,)``

exception rule:

* ``(D)(E)(V)(D,)(P or E or D or Q or K or R)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Casp7



.. _casp8:

Caspase 8
.........

Caspase 8 preferentially cleaves after D (`P1`) preceded by (I/L)ET. It will not cleave if D is followed by P, E, D, Q ,K or R in `P1'`. 

**RPG definition:**

cleaving rule:

* ``(I or L)(E)(T)(D,)``

exception rule:

* ``(I or L)(E)(T)(D,)(P or E or D or Q or K or R)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Casp8



.. _casp9:

Caspase 9
.........

Caspase 9 preferentially cleaves after D (`P1`) preceded by LEH.

**RPG definition:**

cleaving rule:

* ``(L)(E)(H)(D,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Casp9



.. _casp10:

Caspase 10
..........

Caspase 10 preferentially cleaves after D (`P1`) preceded by IEA.

**RPG definition:**

cleaving rule:

* ``(I)(E)(A)(D,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Casp10



.. _chymh:

Chymotrypsin high specificity
.............................

This chymotrypsin preferentially cleaves after F, Y or W (`P1`) if not followed by P in `P1'`. It will not cleave after W followed by M in `P1'`.

**RPG definition:**

cleaving rule:

* ``(F or Y or W,)``

exception rules:

* ``(F or Y or W,)(P)``
* ``(W,)(M)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Chym



.. _chyml:

Chymotrypsin low specificity
.............................

This chymotrypsin preferentially cleaves after F, L, Y, W, M or H (`P1`) if not followed by P in `P1'`. It will not cleave after W followed by M in `P1'`. It will not cleave after M followed by Y in `P1'`. It will not cleave after H followed by D/M/W in `P1'`.

**RPG definition:**

cleaving rule:

* ``(F or L or Y or W or M or H,)``

exception rules:

* ``(F or L or Y or W or M or H,)(P)``
* ``(W,)(M)``
* ``(M,)(Y)``
* ``(H,)(D or M or W)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Chym



.. _clost:

Clostripain
...........

Clostripain (Clostridiopeptidase B) preferentially cleaves after R (`P1`).

**RPG definition:**

cleaving rule:

* ``(R,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Clost



.. _cnbr:

CNBr
....

CNBr preferentially cleaves after M (`P1`).

**RPG definition:**

cleaving rule:

* ``(M,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#CNBr



.. _enter:

Enterokinase
............

Enterokinase preferentially cleaves after K (`P1`) preceded by D/E in `P2`, `P3`, `P4` and `P5`.

**RPG definition:**

cleaving rule:

* ``(D or E)(D or E)(D or E)(D or E)(K,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Enter



.. _fxa:

Factor Xa
.........

Factor Xa preferentially cleaves after R (`P1`) preceded by G in `P2`, D/E in `P3` and A/F/I/L/V/W/G/T in `P4`.

**RPG definition:**

cleaving rule:

* ``(A or F or I or L or V or W or G or T)(D or E)(G)(R,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Xa



.. _ficin:

Ficin
.....

Ficin preferentially cleaves after G, S, E or Y (`P1`) preceded by A, V, I, L ,F, Y or W in `P2`.

**RPG definition:**

cleaving rule:

* ``(A or V or I or L or F or Y or W)(G or S or E or Y,)``

More information: https://www.sigmaaldrich.com/life-science/biochemicals/biochemical-products.html?TablePage=16410578



.. _form:

Formic acid
...........

Formic acid preferentially cleaves after D (`P1`).

**RPG definition:**

cleaving rule:

* ``(D,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#HCOOH



.. _gluc:

Glu-C
.....

Glu-C Sequencing Grade preferentially cleaves after D or E (`P1`).

**RPG definition:**

cleaving rule:

* ``(D or E,)``

More information: https://france.promega.com/resources/pubhub/using-endoproteinases-asp-n-and-glu-c-to-improve-protein-characterization/



.. _glue:

Glutamyl endopeptidase
......................

Glutamyl endopeptidase preferentially cleaves after E (`P1`).

**RPG definition:**

cleaving rule:

* ``(E,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Glu



.. _gran:

Granzyme B
..........

Granzyme B preferentially cleaves after D (`P1`) preceded by IEP.

**RPG definition:**

cleaving rule:

* ``(I)(E)(P)(D,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#GranB



.. _hydro:

Hydroxylamine
.............

Hydroxylamine (NH2OH) preferentially cleaves after N (`P1`) followed by G in `P1'`.

**RPG definition:**

cleaving rule:

* ``(N,)(G)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Hydro



.. _iodo:

Iodosobenzoic acid
..................

Iodosobenzoic acid preferentially cleaves after W (`P1`).

**RPG definition:**

cleaving rule:

* ``(W,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Iodo



.. _lysc:

Lys-C
.....

LysC Lysyl endopeptidase (Achromobacter proteinase I) preferentially cleaves after K (`P1`).

**RPG definition:**

cleaving rule:

* ``(K,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#LysC



.. _lysn:

Lys-N
.....

LysN Peptidyl-Lys metalloendopeptidase preferentially cleaves before K (`P1'` ).

**RPG definition:**

cleaving rule:

* ``(,K)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#LysN



.. _neut:

Neutrophil elastase
...................

Neutrophil elastase preferentially cleaves after A or V (`P1`).

**RPG definition:**

cleaving rule:

* ``(A or V,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Elast



.. _ntcb:

NTCB
....

NTCB +Ni (2-nitro-5-thiocyanobenzoic acid) preferentially cleaves before C (`P1'` ).

**RPG definition:**

cleaving rule:

* ``(,C)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#NTCB



.. _pap:

Papain
......

Papain preferentially cleaves after R or K (`P1`) preceded by A, V, I, L ,F, Y or W in `P2`. It will not cleave if followed by V in `P1'`.

**RPG definition:**

cleaving rule:

* ``(A or V or I or L or F or Y or W)(R or K,)``

exception rule:

* ``(A or V or I or L or F or Y or W)(R or K,)(V)``

More information: https://www.sigmaaldrich.com/life-science/biochemicals/biochemical-products.html?TablePage=16410606



.. _peps13:

Pepsin pH 1.3
.............

This pepsin preferentially cleaves around F or L (`P1` or `P1'` ). It will not cleave before F or L in `P1'` followed by P in `P2'`. It will not cleave before F or L in `P1'` preceded by R in `P1` or P in `P2` or H/K/R in `P3`. It will not cleave after F or L in `P1` followed by P in `P2'`. It will not cleave after F or L in `P1` preceded by P in `P2` or H/K/R in `P3`.

**RPG definition:**

cleaving rule:

* ``(,F or L,)``

exception rules:

* ``(,F or L)(P)``
* ``(R)(,F or L)``
* ``(P)()(,F or L)``
* ``(H or K or R)()()(,F or L)``
* ``(F or L,)()(P)``
* ``(P)(F or L,)``
* ``(H or K or R)()(F or L,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Peps



.. _peps2:

Pepsin pH >=2
.............

This pepsin preferentially cleaves around F, L, W or Y (`P1` or `P1'` ). It will not cleave before F, L, W or Y in `P1'` followed by P in `P2'`. It will not cleave before F, L, W or Y in `P1'` preceded by R in `P1` or P in `P2` or H/K/R in `P3`. It will not cleave after F, L, W or Y IN `P1` followed by P in `P2'`. It will not cleave after F, L, W or Y in `P1` preceded by P in `P2` or H/K/R in `P3`.

**RPG definition:**

cleaving rule:

* ``(,F or L or W or Y,)``

exception rules:

* ``(,F or L or W or Y)(P)``
* ``(R)(,F or L or W or Y)``
* ``(P)()(,F or L or W or Y)``
* ``(H or K or R)()()(,F or L or W or Y)``
* ``(F or L or W or Y,)()(P)``
* ``(P)(F or L or W or Y,)``
* ``(H or K or R)()(F or L or W or Y,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Peps



.. _prol:

Proline-endopeptidase
.....................

Proline-endopeptidase preferentially cleaves after P (`P1`) preceded by H, K or R in `P2` but will not cleaves if followed by P in `P1'`.

**RPG definition:**

cleaving rule:

* ``(H or K or R)(P,)``

exception rule:

* ``(H or K or R)(P,)(P)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Pro



.. _protk:

Proteinase K
.....................

Proteinase K preferentially cleaves after F, W, Y, T, E, A, V, L or I (`P1`). The predominant site of cleavage is the peptide bond adjacent to the carboxyl group of aliphatic and aromatic amino acids.

**RPG definition:**

cleaving rule:

* ``(F or W or Y or T or E or A or V or L or I,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#ProtK



.. _staphI:

Staphylococcal peptidase I
..........................

Staphylococcal peptidase I preferentially cleaves after E (`P1`). It will not cleave after E in `P1` preceded by E in `P2`, but cleaves after E in `P1` followed by E in `P1'`.

**RPG definition:**

cleaving rule:

* ``(E,)``

exception rule:

* ``(E)(E,)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Staph



.. _therm:

Thermolysin
...........

Thermolysin preferentially cleaves before A,F,I,L,M or V (`P1'` ) when not followed by P in `P2'` nor preceded by D or E in `P1`.

**RPG definition:**

cleaving rule:

* ``(,A or F or I or L or M or V)``

exception rules:

* ``(,A or F or I or L or M or V)(P)``
* ``(D or E)(,A or F or I or L or M or V)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Therm



.. _throm:

Thrombin (PeptideCutter)
........................

This thrombin preferentially cleaves after R (`P1`). Optimum cleavage is when R is preceded and followed by G (`P2` and `P1'` ). Cleavage also occurs when R is preceded by P in `P2` and A, F, I, L, V, W, G or T in `P3` and `P4`. It will not cleave after R followed by D/E in `P1'` or `P2'`.

It is not strictly coherent with the definition in PeptideCutter, as in this software there are differences between definition, summary and behavior of this enzyme.

**RPG definition:**

cleaving rules:

* ``(G)(R,)(G)``
* ``(A or F or I or L or V or W or G or T)(A or F or I or L or V or W or G or T)(P)(R,)``

exception rules:

* ``(A or F or I or L or V or W or G or T)(A or F or I or L or V or W or G or T)(P)(R,)(D or E)``
* ``(A or F or I or L or V or W or G or T)(A or F or I or L or V or W or G or T)(P)(R,)()(D or E)``

.. warning:: the following combined exception ``(A or F or I or L or V or W or G or T)(A or F or I or L or V or W or G or T)(P)(R,)(D or E)(D or E)`` cannot be used instead, as it will cleave on [...](R,)(D or E).

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Throm https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3288055/



.. _thromsg:

Thrombin SG
.........................

This thrombin (Sequencing Grade) preferentially cleaves after R (`P1`) preceded by P in `P2`, V in `P3` and L in `P4` and followed by G in `P1'` and S in `P2'`.

This thrombin is defined in several kits (see below).

**RPG definition:**

cleaving rule:

* ``(L)(V)(P)(R,)(G)(S)``

More information: see thrombin cleavage kits of 
`Abcam <http://www.abcam.com/thrombin-cleavage-kit-ab207000.html>`_,
`BioVision <https://www.biovision.com/documentation/datasheets/K377.pdf>`_, 
`Merck <http://www.merckmillipore.com/FR/fr/life-science-research/protein-sample-preparation/protein-purification/cleavage-enzymes/0Uqb.qB.V5gAAAFBOFJlvyyv,nav#thrombin>`_ or 
`Novagen <http://wolfson.huji.ac.il/purification/PDF/Protease_fusion_cleavage/NOVAGEN_Thrombin_kit.pdf>`_.



.. _tev:

Tobacco etch virus protease
...........................

Tobacco etch virus protease (TEV) preferentially cleaves after Q (`P1`) when followed by G or S in `P1'` and preceded by Y in `P3` and E in `P6`.

**RPG definition:**

cleaving rule:

* ``(E)()()(Y)()(Q,)(G or S)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#TEV



.. _tryps:

Trypsin
.......

Trypsin preferentially cleaves after K or R (`P1`). It will not cleave after K followed by P in `P1'` except if W in `P2`. It will not cleave after R followed by P in `P1'` except if M in `P2`. It will not cleave CKD, DKD, CKH, CKY, CRK, RRH nor RRR.

**RPG definition:**

cleaving rules:

* ``(K or R,)``
* ``(W)(K,)(P)``
* ``(M)(R,)(P)``

exception rules:

* ``(K or R,)(P)``
* ``(C)(K,)(D)``
* ``(D)(K,)(D)``
* ``(C)(K,)(H)``
* ``(C)(K,)(Y)``
* ``(C)(R,)(K)``
* ``(R)(R,)(H)``
* ``(R)(R,)(R)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#Tryps



.. _asp-n2:

Asp-N Endopeptidase
...................

Asp-N Sequencing Grade preferentially cleaves before D (`P1'` )

**RPG definition:**

cleaving rule:

* ``(,D)``

More information: https://web.expasy.org/peptide_cutter/peptidecutter_enzymes.html#AspN



.. _proa:

ProAlanase
..........

ProAlanase Sequencing Grade preferentially cleaves after A or P (`P1`).

**RPG definition:**

cleaving rule:

* ``(A or P,)``

More information: https://france.promega.com/products/mass-spectrometry/proteases-and-surfactants/proalanase-mass-spec-grade?catNum=VA2161



.. _elast:

Elastase
........

Elastase preferentially cleaves after A, V, S, G, L, or I (`P1`).

**RPG definition:**

cleaving rule:

* ``(A or V or S or G or L or or I,)``

More information: https://france.promega.com/products/mass-spectrometry/proteases-and-surfactants/elastase/?catNum=V1891
