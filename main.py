def main():
    import argparse
    import os
    import sys
    home_path = sys.path[0]
    parser = argparse.ArgumentParser(description="InterPro Wrapper")
    parser.add_argument('prism_input', metavar="json_input", type=str, nargs=1, 
    help="input PRISM file")
    parser.add_argument('interpro_output', metavar='json_output', type=str, 
    nargs=1, help="output json file name")
    args = parser.parse_args()
    faa_out = "%s.faa" % args.prism_input[0]
    ip_out = "%s.faa.json" % args.prism_input[0]
    # Make FAA
    os.system("python %s/deps/FaaFromPrism.py %s %s" % (home_path, 
    args.prism_input[0], faa_out))
    # Call InterPro
    os.system("python %s/deps/InterProRunner.py %s %s" % (home_path, 
    faa_out, faa_out))
    # Convert InterPro
    os.system("python %s/deps/InterProParser.py %s %s" % (home_path,
    ip_out, args.interpro_output[0]))
    return 0


if __name__ == '__main__':
    main()

