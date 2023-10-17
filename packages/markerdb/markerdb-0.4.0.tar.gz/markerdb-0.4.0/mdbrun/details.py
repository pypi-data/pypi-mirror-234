import csv, sys, re, plac, os

# This script parses tab delimited file produced by blastdbcmd command
# and extracts taxa-specific marker sequence details.

# The input is tab-delimited file produced by blastdbcmd command with columns
# accession,title,seq_length,taxid,scientific_name,common_name

# The output of this script is a tab-delimited,taxa specific marker table with the following columns
# accession,title,length,taxid,scientific_name,common_name,marker,genomic_location

csv.field_size_limit(sys.maxsize)

MARKERS = []
marker_map = dict()

REGION = ["mitochondri", "chloroplast"]
region_map = {"mitochondri": "Mitochondria",
              "chloroplast": "Chloroplast"}


def read_taxids(fname):
    store = dict()
    stream = csv.reader(open(fname), delimiter="\t")
    for row in stream:
        name, tid = row[0], row[1]
        store[tid] = name if name else None
    return store


def match_patterns(title, pattern_list, func=lambda x: x.lower()):
    # Find a match in a list of patterns
    # Returns first match found.
    for pattern in pattern_list:
        # Apply extra function to pattern to
        # enhance/relax searches.
        pattern = func(pattern)
        # print("PPP", pattern)
        match = re.search(pattern, title)
        if match:
            return match.group(0)

    return


def parse_title(title):
    pattern_func = lambda p: r'\b' + p.lower() + r'\b'

    title = title.lower()
    # print(MARKERS)

    # Return the first matched marker and region
    marker = match_patterns(title, pattern_list=MARKERS, func=pattern_func)
    region = match_patterns(title, pattern_list=REGION)

    return marker, region


def parse_nt_table(fname, taxid, marker_gene, synonyms):
    """
    This file 'fname' is produced by blastdbcmd command and has the format
    accession\ttitle\tseq_length\ttaxid\tscientific_name\tcommon_name
    """

    check_inputs(fname, taxid, synonyms)

    genes = read_synonyms(synonyms)

    # Check marker gene
    check_input_marker(marker_gene, genes)

    taxids = read_taxids(taxid)

    header = ["accession", "title", "length", "taxid",
              "scientific_name", "common_name", "marker", "genomic_location", ]

    # print("\t".join(header))
    yield "\t".join(header)

    stream = csv.reader(open(fname), delimiter="\t")

    for row in stream:

        acc, title, taxid = row[0], row[1], row[3].strip()

        if taxid not in taxids:
            continue

        marker, genomic_location = parse_title(title)

        # if marker is None or genomic_location is None:
        #     continue

        if marker is None:
            continue

        if marker in marker_map:
            marker = marker_map[marker]

        if genomic_location in region_map:
            genomic_location = region_map[genomic_location]

        genomic_location = genomic_location if genomic_location else ""

        if marker_gene == "ALL" or marker.upper() == marker_gene.upper():
            out = "\t".join(row)
            parsed = "\t".join([out, marker, genomic_location])

            yield parsed


def check_input_marker(marker, genes):
    if marker != "ALL" and marker not in genes:
        print("Synonyms are not found for the input gene.")
        sys.exit()
    return


def check_inputs(table, taxid, synonyms):
    # Check if taxid file is present
    if not taxid:
        print(f"Taxid file must be given.")
        sys.exit()

    # Check if blast table file is present
    if not table:
        print(f""" Tab delimited file must be present.\n \
Columns include accession,title,length,taxid,scientific name,common name.""")
        sys.exit()

    # check synonyms file
    if not os.path.exists(synonyms):
        print(f"Synonyms file is not found")
        sys.exit()
    return


def read_synonyms(synonyms):
    # List of all marker genes
    genes = ["ALL"]

    stream = csv.reader(open(synonyms), delimiter=",")

    for row in stream:
        key, vals = row[0], row
        MARKERS.extend(vals)
        genes.append(key)

        # For easy mapping
        for n in vals:
            marker_map[n.lower()] = key

    return genes


@plac.opt('fname', "Tab-separated file with columns accession,title,length,taxid,scientific name,common name.")
@plac.opt('taxid', help="Tab delimited file with species names and taxid")
@plac.opt('marker', help="Marker gene. Must be present in the synonyms file")
@plac.opt('synonyms', help="CSV file listing synonyms for marker genes. First name is the main identifier.")
def run(fname, taxid, marker="ALL", synonyms="synonyms.csv"):
    for result in parse_nt_table(fname, taxid, marker, synonyms):
        print(result)


if __name__ == "__main__":
    run()
