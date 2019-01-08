#!/usr/bin/env python3
# name:     InterProRunner.py
# author:   Keshav Dial

import sys

#INTERPROSCAN_LOCAL = "%s/interpro/interproscan.sh" % sys.path[0]
INTERPROSCAN_LOCAL= "/mnt/storage/grid/home/keshav/tools/interpro_1113/interproscan.sh"

def run_interpro_scan(faa_file, out_file):
    """ System Wrapper
     No Popen because we don't need to buffer output
    """
    import os
    arg_line = "%s -i  %s -b %s -goterms -pa -f json" % (INTERPROSCAN_LOCAL, 
    faa_file, out_file)
    os.system(arg_line)
    return 0

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Get InterProScan Results \
    from FAA file")
    parser.add_argument('faa_input', metavar="faa", type=str, nargs=1, 
    help="input FAA file")
    parser.add_argument('json_output', metavar='json', type=str, nargs=1,
    help="output json file name")
    args = parser.parse_args()
    tmp = run_interpro_scan(args.faa_input[0], args.json_output[0])
    # Will automatically append the '.json' extension
    print('Created "%s.json" output file' % (args.json_output[0]))
    return 0
    
if __name__ == '__main__':
    main()

