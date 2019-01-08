#!/usr/bin/env python3
# name:     InterProRunner.py
# author:   Keshav Dial

import argparse
import os

INTERPROSCAN_LOCAL = "/mnt/storage/grid/home/keshav/tools/interpro_1113/\
interproscan.sh"


def run_interpro_scan(faa_file: str, out_file: str) -> int:
    """ System Wrapper

    No Popen because we don't need to buffer output.

    Args:
        faa_file: location of the FASTA file with ORFs to be processed
        out_file: location to write the InterProScan output JSON (will add .json
         extension automatically)

    Returns:
        0: success
    """
    arg_line = "%s -i  %s -b %s -goterms -pa -f json" % (INTERPROSCAN_LOCAL,
                                                         faa_file, out_file)
    os.system(arg_line)
    return 0


def main():
    """ Command Line Interface for Script"""
    parser = argparse.ArgumentParser(description="Get InterProScan Results \
    from FAA file")
    parser.add_argument('faa_input', metavar="faa", type=str, nargs=1,
                        help="input FAA file")
    parser.add_argument('json_output', metavar='json', type=str, nargs=1,
                        help="output json file name")
    args = parser.parse_args()
    tmp = run_interpro_scan(args.faa_input[0], args.json_output[0])
    del tmp
    # Will automatically append the '.json' extension
    print('Created "%s.json" output file' % (args.json_output[0]))
    return 0


if __name__ == '__main__':
    main()

