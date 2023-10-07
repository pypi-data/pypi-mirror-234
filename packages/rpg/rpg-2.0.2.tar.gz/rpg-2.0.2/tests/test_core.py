"""Tests for core.py"""
import gzip
import pytest
from .context import rpg
from rpg import core
from rpg import rule
from rpg import enzyme
from rpg import digest
from rpg import sequence

def test_handle_errors(capsys):
    """Test function 'handle_errors(msg="", err=1, error_type="")'"""
    # Error, then exit
    message = "This is a test"
    error = 0
    error_type = "Test "
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        core.handle_errors(message, error, error_type)
    _, err = capsys.readouterr()
    assert err == "Test Error: This is a test\n"
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

    # Warning test
    message = "This is a test"
    error = 1
    error_type = "Test "
    core.handle_errors(message, error, error_type)
    _, err = capsys.readouterr()
    assert err == "Test Warning: This is a test\n"

    # Writing in stderr test
    message = "This is a test"
    error = 2
    error_type = "Test "
    core.handle_errors(message, error, error_type)
    _, err = capsys.readouterr()
    assert err == "Test This is a test\n"

    # Default parameters
    message = "This is a test"
    core.handle_errors(message)
    _, err = capsys.readouterr()
    assert err == "Warning: This is a test\n"

def test_get_header():
    """Test function 'get_header(fmt="fasta")'"""
    res_fasta = None
    res_csv = "Original_header,No_peptide,Enzyme,Cleaving_pos,Peptide_size,Pe"\
              "ptide_mass,pI,Sequence"
    res_tsv = "Original_header\tNo_peptide\tEnzyme\tCleaving_pos\tPeptide_siz"\
              "e\tPeptide_mass\tpI\tSequence"
    assert core.get_header() == res_fasta
    assert core.get_header("csv") == res_csv
    assert core.get_header("tsv") == res_tsv
    assert core.get_header("pwet") == res_fasta

def test_output_results(capsys, tmp_path):
    """Test function 'output_results(output_file, all_seq_digested,
                                     fmt, quiet, verbose)'"""
    # Test file not found
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        core.output_results("/tmp", None, "csv", False, False)
    _, err = capsys.readouterr()
    assert err == "File Error: /tmp can't be open in 'w' mode\n"
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

    a_rule = {}
    rule_txt = "(S)(D,)"
    a_rule[rule_txt] = True
    all_rules = rule.create_rules(a_rule)
    enz1 = enzyme.Enzyme(-1, "fake_enzyme1", all_rules)
    enzymes = [enz1]
    mode = "sequential"

    # CSV output
    seq = "WQSDESDFZQSDESDF"
    aa_pka = core.AA_PKA_IPC
    aa_mass = core.AA_MASS_MONO
    water_mass = core.WATER_MASS_MONO
    all_seq_digested = digest.digest_from_input(seq, "sequence", enzymes, mode,
                                                aa_pka, aa_mass, water_mass)
    output_file = tmp_path.joinpath("test_result.csv")
    fmt = "csv"
    quiet = False
    verbose = 0
    core.output_results(str(output_file), all_seq_digested, fmt, quiet, verbose)
    out, err = capsys.readouterr()
    with open(output_file, encoding="utf-8") as outf:
        assert out == outf.read()
        assert out == "Original_header,No_peptide,Enzyme,Cleaving_"\
                      "pos,Peptide_size,Peptide_mass,pI,Sequence\n"\
                      "Input,0,fake_enzyme1,4,4,534.20743,3.14,WQS"\
                      "D\nInput,1,fake_enzyme1,7,3,349.11213,3.04,"\
                      "ESD\nInput,2,fake_enzyme1,12,5,495.19653,3."\
                      "14,FZQSD\nInput,3,fake_enzyme1,15,3,349.112"\
                      "13,3.04,ESD\nInput,4,fake_enzyme1,16,1,165."\
                      "07898,5.97,F\n"

    # CSV output
    seq = "WQSDESDFZQSDESDF"
    aa_pka = core.AA_PKA_IPC
    aa_mass = core.AA_MASS_AVERAGE
    water_mass = core.WATER_MASS
    all_seq_digested = digest.digest_from_input(seq, "sequence", enzymes, mode,
                                                aa_pka, aa_mass, water_mass)
    output_file = tmp_path.joinpath("test_result.csv")
    fmt = "csv"
    quiet = False
    verbose = 0
    core.output_results(str(output_file), all_seq_digested, fmt, quiet, verbose)
    out, err = capsys.readouterr()
    with open(output_file, encoding="utf-8") as outf:
        assert out == outf.read()
        assert out == "Original_header,No_peptide,Enzyme,Cleaving_"\
                      "pos,Peptide_size,Peptide_mass,pI,Sequence\n"\
                      "Input,0,fake_enzyme1,4,4,534.52598,3.14,WQS"\
                      "D\nInput,1,fake_enzyme1,7,3,349.29758,3.04,"\
                      "ESD\nInput,2,fake_enzyme1,12,5,495.48938,3."\
                      "14,FZQSD\nInput,3,fake_enzyme1,15,3,349.297"\
                      "58,3.04,ESD\nInput,4,fake_enzyme1,16,1,165."\
                      "19188,5.97,F\n"

    # TSV output
    output_file = tmp_path.joinpath("test_result.tsv")
    fmt = "tsv"
    quiet = False
    verbose = 0
    core.output_results(str(output_file), all_seq_digested, fmt, quiet, verbose)
    out, err = capsys.readouterr()
    with open(output_file, encoding="utf-8") as outf:
        assert out == outf.read()
        assert out == "Original_header\tNo_peptide\tEnzyme\tCleavi"\
                      "ng_pos\tPeptide_size\tPeptide_mass\tpI\tSeq"\
                      "uence\nInput\t0\tfake_enzyme1\t4\t4\t534.52"\
                      "598\t3.14\tWQSD\nInput\t1\tfake_enzyme1\t7"\
                      "\t3\t349.29758\t3.04\tESD\nInput\t2\tfake_e"\
                      "nzyme1\t12\t5\t495.48938\t3.14\tFZQSD\nInpu"\
                      "t\t3\tfake_enzyme1\t15\t3\t349.29758\t3.04"\
                      "\tESD\nInput\t4\tfake_enzyme1\t16\t1\t165.1"\
                      "9188\t5.97\tF\n"

    # Fasta output
    output_file = tmp_path.joinpath("test_result.fasta")
    fmt = "fasta"
    quiet = False
    verbose = 0
    core.output_results(str(output_file), all_seq_digested, fmt, quiet, verbose)
    out, err = capsys.readouterr()
    with open(output_file, encoding="utf-8") as outf:
        assert out == outf.read()
        assert out == ">Input_0_fake_enzyme1_4_4_534.52598_3.14\nW"\
                      "QSD\n>Input_1_fake_enzyme1_7_3_349.29758_3."\
                      "04\nESD\n>Input_2_fake_enzyme1_12_5_495.489"\
                      "38_3.14\nFZQSD\n>Input_3_fake_enzyme1_15_3_"\
                      "349.29758_3.04\nESD\n>Input_4_fake_enzyme1_"\
                      "16_1_165.19188_5.97\nF\n"

    # CSV output in quiet
    seq = "WQSDESDFZQSDESDF"
    all_seq_digested = digest.digest_from_input(seq, "sequence", enzymes, mode,
                                                aa_pka, aa_mass, water_mass)
    output_file = tmp_path.joinpath("test_result.csv")
    fmt = "csv"
    quiet = True
    verbose = 0
    core.output_results(str(output_file), all_seq_digested, fmt, quiet,
                        verbose)
    out, err = capsys.readouterr()
    # Quiet
    assert out == ""
    with open(output_file, encoding="utf-8") as outf:
        assert outf.read() == "Original_header,No_peptide,Enzyme,Cleaving_"\
                              "pos,Peptide_size,Peptide_mass,pI,Sequence\n"\
                              "Input,0,fake_enzyme1,4,4,534.52598,3.14,WQS"\
                              "D\nInput,1,fake_enzyme1,7,3,349.29758,3.04,"\
                              "ESD\nInput,2,fake_enzyme1,12,5,495.48938,3."\
                              "14,FZQSD\nInput,3,fake_enzyme1,15,3,349.297"\
                              "58,3.04,ESD\nInput,4,fake_enzyme1,16,1,165."\
                              "19188,5.97,F\n"

    # CSV output in verbose > 2
    seq = "WQSDESDFZQSDESDF"
    all_seq_digested = digest.digest_from_input(seq, "sequence", enzymes, mode,
                                                aa_pka, aa_mass, water_mass)
    output_file = tmp_path.joinpath("test_result.csv")
    fmt = "csv"
    quiet = False
    verbose = 3
    core.output_results(str(output_file), all_seq_digested, fmt, quiet,
                        verbose)
    out, err = capsys.readouterr()
    with open(output_file, encoding="utf-8") as outf:
        content = outf.read()
        assert content == "Original_header,No_peptide,Enzyme,Cleaving_"\
                          "pos,Peptide_size,Peptide_mass,pI,Sequence\n"\
                          "Input,0,fake_enzyme1,4,4,534.52598,3.14,WQS"\
                          "D\nInput,1,fake_enzyme1,7,3,349.29758,3.04,"\
                          "ESD\nInput,2,fake_enzyme1,12,5,495.48938,3."\
                          "14,FZQSD\nInput,3,fake_enzyme1,15,3,349.297"\
                          "58,3.04,ESD\nInput,4,fake_enzyme1,16,1,165."\
                          "19188,5.97,F\n"
        # Verbose > 2
        assert out == "\nNumber of cleavage: 4\nCleavage position: 4, 7, 12, 15\n"\
                      "Number of miscleavage: 0\nmiscleavage position: \nmis"\
                      "cleavage ratio: 0.00%\nSmallest peptide size: 1\nN termin"\
                      "al peptide: WQSD\nC terminal peptide: F\n" + content

    # No output file
    output_file = None
    fmt = "csv"
    quiet = False
    verbose = 3
    core.output_results(output_file, all_seq_digested, fmt, quiet,
                        verbose)
    out, err = capsys.readouterr()
    assert out == "\nNumber of cleavage: 4\nCleavage position: 4, 7, 12, 15\n"\
                  "Number of miscleavage: 0\nmiscleavage position: \nmis"\
                  "cleavage ratio: 0.00%\nSmallest peptide size: 1\nN termin"\
                  "al peptide: WQSD\nC terminal peptide: F\nOriginal_header,"\
                  "No_peptide,Enzyme,Cleaving_"\
                  "pos,Peptide_size,Peptide_mass,pI,Sequence\n"\
                  "Input,0,fake_enzyme1,4,4,534.52598,3.14,WQS"\
                  "D\nInput,1,fake_enzyme1,7,3,349.29758,3.04,"\
                  "ESD\nInput,2,fake_enzyme1,12,5,495.48938,3."\
                  "14,FZQSD\nInput,3,fake_enzyme1,15,3,349.297"\
                  "58,3.04,ESD\nInput,4,fake_enzyme1,16,1,165."\
                  "19188,5.97,F\n"

    # No output file et less verbose
    output_file = None
    fmt = "csv"
    quiet = False
    verbose = 1
    core.output_results(output_file, all_seq_digested, fmt, quiet,
                        verbose)
    out, err = capsys.readouterr()
    assert out == "Original_header,No_peptide,Enzyme,Cleaving_"\
                  "pos,Peptide_size,Peptide_mass,pI,Sequence\n"\
                  "Input,0,fake_enzyme1,4,4,534.52598,3.14,WQS"\
                  "D\nInput,1,fake_enzyme1,7,3,349.29758,3.04,"\
                  "ESD\nInput,2,fake_enzyme1,12,5,495.48938,3."\
                  "14,FZQSD\nInput,3,fake_enzyme1,15,3,349.297"\
                  "58,3.04,ESD\nInput,4,fake_enzyme1,16,1,165."\
                  "19188,5.97,F\n"

def test_peptide():
    """Test class 'Peptide'"""
    header = "Test"
    seq = "QWSDESDF"
    enz_name = "fake_enzyme"
    aa_pka = core.AA_PKA_IPC
    aa_mass = core.AA_MASS_AVERAGE
    water_mass = core.WATER_MASS
    pep0 = sequence.Peptide(header, seq, enz_name, aa_pka, aa_mass, water_mass, 1, 3)
    # Test function '__repr__()'
    print_res = pep0.__repr__()
    assert print_res == "Original header: Test\nNo. peptide: 1\nEnzyme: fake_"\
                        "enzyme\nCleav. pos: 3\nPep. size: 8\nPep. mass: 1012"\
                        ".98488\npKa values from: IPC\nPep. pI: 2.91\nSequenc"\
                        "e: QWSDESDF\n"

    # Test function '__eq__()'
    pep1 = sequence.Peptide(header, seq, enz_name, aa_pka, aa_mass, water_mass, 1, 3)
    assert pep0 == pep1

    # Test function '__ne__()'
    pep2 = sequence.Peptide(header, seq, enz_name, aa_pka, aa_mass, water_mass, 1, 2)
    pep3 = sequence.Peptide(header, seq, enz_name, aa_pka, aa_mass, water_mass, 2, 3)
    pep4 = sequence.Peptide(header, seq, enz_name + "A", aa_pka, aa_mass, water_mass, 1, 3)
    pep5 = sequence.Peptide(header, seq + "A", enz_name, aa_pka, aa_mass, water_mass, 1, 3)
    pep6 = sequence.Peptide(header + "A", seq, enz_name, aa_pka, aa_mass, water_mass, 1, 3)
    assert pep0 != pep2
    assert pep0 != pep3
    assert pep0 != pep4
    assert pep0 != pep5
    assert pep0 != pep6

    # Test function '__format__()'
    format_res = pep0.__format__("csv")
    assert format_res == "Test,1,fake_enzyme,3,8,1012.98488,2.91,QWSDESDF"
    format_res = pep2.__format__("tsv")
    assert format_res == "Test\t1\tfake_enzyme\t2\t8\t1012.98488\t2.91\tQWSD"\
                         "ESDF"
    format_res = pep3.__format__("fasta")
    assert format_res == ">Test_2_fake_enzyme_3_8_1012.98488_2.91\nQWSDESDF"

    # Test function 'def get_isoelectric_point():'
    assert pep3.get_isoelectric_point() == 2.91


def test_next_read(capsys, tmp_path):
    """ Test function 'next_read(files)'"""
    # Test fasta (multi-line) file with two sequences
    fasta_file = tmp_path.joinpath("test.fasta")
    with open(fasta_file, "w", encoding="utf-8") as f_file:
        f_file.write(">Fake1\nACGTTATATGCTA\nTGTG\n>Fake2\nCAGTACTAGCA")
    # Only a portion of the file (from 0 to 3)
    res = core.next_read(fasta_file, 0, 3)
    # First read
    a_read = next(res, None)
    assert a_read == (">Fake1", "ACGTTATATGCTATGTG")
    # No second read
    a_read = next(res, None)
    assert a_read is None
    # Full file
    res = core.next_read(fasta_file, 0, 35)
    # First read
    a_read = next(res, None)
    assert a_read == (">Fake1", "ACGTTATATGCTATGTG")
    # No second read
    a_read = next(res, None)
    assert a_read == (">Fake2", "CAGTACTAGCA")

    # Test gzipped fasta file
    data = b">Fake1\nACGTTATATGCTATGT\n"
    fastagz_file = tmp_path.joinpath("test.fasta.gz")
    with gzip.open(fastagz_file, "wb") as fil:
        fil.write(data)
    res = core.next_read(fastagz_file, 0, 35)
    # First read
    a_read = next(res)
    assert a_read == (">Fake1", "ACGTTATATGCTATGT")

    # Test fastq file with two sequence
    fastq_file = tmp_path.joinpath("test.fastq")
    with open(fastq_file, "w", encoding="utf-8") as f_file:
        f_file.write("@Fake1\nACGTTATATGCTATGTG\n+Fake1\n5Q8D8=64DS-+DZ84!\n"\
                     "@Fake2\nATGCATGCTG\n+Fake1\n8173*8173!")
    # First sequence only (from 0 to 3)
    res = core.next_read(fastq_file, 0, 3)
    # First read
    a_read = next(res, None)
    assert a_read == ("@Fake1", "ACGTTATATGCTATGTG")
    # No second read
    a_read = next(res, None)
    assert a_read is None
    # Full file
    res = core.next_read(fastq_file, 0, 1000)
    # First read
    a_read = next(res, None)
    assert a_read == ("@Fake1", "ACGTTATATGCTATGTG")
    # Second read
    a_read = next(res, None)
    assert a_read == ("@Fake2", "ATGCATGCTG")

    # Test gzipped fastq file
    data = b"@Fake1\nACGTTATATGCTATGTG\n+Fake1\n5Q8D8=64DS-+DZ84!\n"
    fastqgz_file = tmp_path.joinpath("test.fastq.gz")
    with gzip.open(fastqgz_file, "wb") as fil:
        fil.write(data)
    res = core.next_read(fastqgz_file, 0, 35)
    # First read
    a_read = next(res)
    assert a_read == ("@Fake1", "ACGTTATATGCTATGTG")

    # Test wrong gzipped fastq file
    data = b"+Fake1\nACGTTATATGCTATGTG\n+Fake1\n5Q8D8=64DS-+DZ84!\n"
    fastqgz_file = tmp_path.joinpath("test.fastq.gz")
    with gzip.open(fastqgz_file, "wb") as fil:
        fil.write(data)
    with pytest.raises(ValueError) as pytest_wrapped_e:
        res = core.next_read(fastqgz_file, 0, 35)
        a_read = next(res)
    assert pytest_wrapped_e.type == ValueError
    assert str(pytest_wrapped_e.value) == "input file format not recognized (+)."

