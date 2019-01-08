#!/usr/bin/env python3
# name:     InterProParser.py
# author:   Keshav Dial
# desc:     Creates a InterPro JSON formatted similar to PRISM output

import argparse
import json
import re


def main():
    """ Command Line Interface for the Script """

    parser = argparse.ArgumentParser(description="Convert InterPro JSON to\
    PRISM-like format")
    parser.add_argument('json_input', metavar="json_in", type=str, nargs=1,
                        help="input JSON file")
    parser.add_argument('json_output', metavar='json_out', type=str, nargs=1,
                        help="output JSON file")
    args = parser.parse_args()
    json_obj = convert_ipr(args.json_input[0])
    tmp = write_json(json_obj, args.json_output[0])
    del tmp
    print('Converted "%s" to "%s"' % (args.json_input[0], args.json_output[0]))
    return 0


def convert_ipr(ip_json: str, full_json: bool = True) -> dict:
    """ Reformat an InterProScan Result

    Generates a new dictionary object with a schema similar to the PRISM output.

    Args:
        ip_json: location of the InterProScan output JSON file
        full_json: whether or not the InterProScan job contained all PRISM ORFs

    Returns:
        out_json: dictionary formatted in similar schema to PRISM
    """

    # Output File Prep
    out_json = {}
    interpro_results = {}
    out_json['interpro_results'] = interpro_results
    clusters = {}
    interpro_results['clusters'] = clusters

    # Parsing
    j = json.load(open(ip_json, "r"))
    # Get Version
    out_json['interproscan_version'] = j['interproscan-version']
    # Get Each InterPro Hit
    for r in j['results']:
        assignments = []
        for instance in r['xref']:
            orf_id = instance['id']
            description = instance['name']
            cluster_number = re.search("cluster_([0-9]*)_orf_([0-9]*)",
            description).group(1)
            orf_number = re.search("cluster_([0-9]*)_orf_([0-9]*)",
            description).group(2)
            assignments.append((int(cluster_number), int(orf_number), orf_id))
        # Fill in output json with object assignments
        domains = []
        go_results = []
        path_results = []
        for cluster_no, orf_no, orf_id in assignments:
            if clusters.get(cluster_no) is None:
                cluster = {}
                clusters[cluster_no] = cluster
            cluster = clusters[cluster_no]
            if cluster.get("orfs") is None:
                orfs = {}
                cluster['orfs'] = orfs
            orfs = clusters[cluster_no]['orfs']
            if orfs.get(orf_no) is None:
                orf = {}
                orfs[orf_no] = orf
            orf = orfs[orf_no]
            orf['id'] = orf_id
            orf['domains'] = domains
            orf['go_results'] = go_results
            orf['path_results'] = path_results
        # Fill in output dictionary with data
        for match in r['matches']:
            match_accession = match['signature']['accession']
            match_desc = match['signature']['description']
            try:
                # rewrite if signature has been integrated into InterPro
                match_accession = match['signature']['entry']['accession']
                match_desc = match['signature']['entry']['description']
            except (KeyError, TypeError):
                pass
            for loc in match['locations']:
                start = int(loc['start'])
                end = int(loc['end'])
                # Build domain entry
                domain = {
                    "start": start,
                    "end": end,
                    "id": match_accession,
                    "description": match_desc
                }
                domains.append(domain)
            try:
                # Look for associated Gene Ontology entries
                for go_result in match['signature']['entry']['goXRefs']:
                    go_results.append(go_result['id'])
            except (KeyError, TypeError):
                pass
            try:
                # Look for associated Pathways
                for path in match['signature']['entry']['pathwayXRefs']:
                    path_results.append(path['id'])
            except (KeyError, TypeError):
                pass

    # If the all ORFs in the PRISM were used, then format it identically to the
    # PRISM JSON
    if full_json is True:
        cluster_list = [[] for x in range(len(clusters))]  # prototype
        for cluster_no, cluster_dict in clusters.items():
            orf_list = [[] for x in range(len(cluster_dict['orfs']))]
            for orf_num, orf in cluster_dict['orfs'].items():
                orf_list[orf_num] = orf
            cluster_list[cluster_no] = {
                "orfs": orf_list
            }
        clusters = cluster_list
        interpro_results['clusters'] = clusters
    return out_json


def write_json(json_obj: dict, json_out: str) -> int:
    """ Writes the dictionary out the specified file

    Args:
        json_obj: dictionary structured like a JSON object
        json_out: location to write the JSON object to

    Returns:
        0: success
    """
    import json
    with open(json_out, 'w') as fh:
        tmp = json.dump(json_obj, fh)
        del tmp
    return 0


if __name__ == '__main__':
    main()

