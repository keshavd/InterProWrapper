#!/usr/bin/env python3
# name:     FaaFromPrism.py
# author:   Keshav Dial
# desc:     convert PRISM json to FAA file

from typing import List
import json
import argparse
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


def main():
    """ Command Line Interface for the script """
    parser = argparse.ArgumentParser(description="Get ORF FAA from PRISM JSON")
    parser.add_argument('prism_input', metavar="json", type=str, nargs=1,
                        help="input PRISM json file")
    parser.add_argument('faa_output', metavar='faa', type=str, nargs=1,
                        help="output FAA file name")
    args = parser.parse_args()
    entries = get_faa(args.prism_input[0], args.faa_output[0])
    print('Created "%s" with %d records' % (args.faa_output[0], entries))
    return 0


def get_orfs(prism_file: str, prodigal_only: bool = False) -> List[SeqRecord]:
    """ Generates BioPython Sequence Record Objects from PRISM JSON

    Parses a PRISM output JSON file and extracts all relevant information about
    open-reading frames (ORFs). Removes all asterisks from sequences. Uses the
    data to generate BioPython SeqRecord objects.

    Args:
        prism_file: location of the PRISM output JSON file
        prodigal_only: whether to extract exclusively PRODIGAL called ORFs

    Returns:
        all_records: a list of SeqRecords comprised of all captured ORF info
    """
    j = json.load(open(prism_file, "r"))
    clusters = j['prism_results']['clusters']
    all_records = []
    for i, c in enumerate(clusters):
        orfs = c['orfs']
        for ii, orf in enumerate(orfs):
            orf_name = orf['name']
            orf_seq = orf['sequence']
            orf_annotations = {
                "frame": orf['frame'],
                "start": orf['start'],
                "stop": orf['stop'],
                "mode": orf['mode']
            }
            # Strip asterisks
            orf_seq = orf_seq.replace("*", "")
            try:
                s = Seq(orf_seq)
                sr = SeqRecord(id=orf_name, seq=s,
                               description="cluster_%d_orf_%d" % (i, ii),
                               annotations=orf_annotations)
                if prodigal_only is True:
                    if orf_annotations['mode'] == "PRODIGAL":
                        all_records.append(sr)
                else:
                    all_records.append(sr)
            except Exception as e:
                print("Something went wrong with Cluster %d ORF %d" % (i, ii))
                print(e)
    return all_records


def get_faa(prism_file: str, out_file: str) -> int:
    """    Writes FAA file from PRISM file

    Creates the FASTA file of Open Reading Frames (ORFs) from a PRISM output
    JSON file.

    Args:
        prism_file: location of the PRISM output JSON file
        out_file: location to write the FASTA file to

    Returns:
        no_records: the number of records written
    """

    all_records = get_orfs(prism_file)
    with open(out_file, "w") as fh:
        no_records = SeqIO.write(all_records, fh, "fasta")
    return no_records


if __name__ == '__main__':
    main()

