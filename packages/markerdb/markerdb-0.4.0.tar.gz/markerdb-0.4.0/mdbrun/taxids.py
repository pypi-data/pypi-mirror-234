#
# This script takes a file with scientific names/taxon names and extracts all species/sub-species under it.
#
# Requirement - Taxonkit must be installed
#
# Input - A file that lists taxa name in each row.
#
# Output(s)
# 1. A file with taxids corresponding to the names in input. If --children is specified, taxids corresponding to
# the species and subspecies in the taxonomic lineage of the input names are printed.
# 2. missing.txt - A file named 'missing.txt' will be created in the output if taxids  could not be obtained for any of the input names.

import subprocess, plac


def get_taxid(fname):
    """
    Gets taxids for scientific names in a file.
    """
    cmd = f"cat {fname} | taxonkit name2taxid"
    result = subprocess.run([cmd], stdout=subprocess.PIPE, shell=True)
    return result.stdout.decode('utf-8')


def get_lower_taxa(taxids):
    """
    runs taxonkit list command and returns its  output.
    taxids is a comma separated list of tax-ids.
    """
    cmd = f"taxonkit list --show-rank --show-name --indent \"    \" --ids {taxids}"
    result = subprocess.run([cmd], stdout=subprocess.PIPE, shell=True)
    return result.stdout.decode('utf-8')


def parse_taxa(taxa_line):
    """
    Parses taxonkit ouput.
    """
    taxa_line = taxa_line.lstrip()
    arr = taxa_line.split(" ")
    tid, taxa, name = arr[0], arr[1], " ".join(arr[2:])
    taxa = taxa.replace('[', '')
    taxa = taxa.replace(']', '')

    return tid, taxa, name


def get_species(taxa_list):
    """
    taxonkit list command output is parsed and species/subspecies list are returned.
    taxa_list is a string with results of taxonkit list command.
    """
    species, subspecies = list(), list()

    # Split on empty new line to extract results corresponding to each taxid.
    taxa_groups = taxa_list.split("\n\n")

    # Parse each group line by line.
    for taxa_group in taxa_groups:
        taxa = taxa_group.split("\n")

        for taxa_line in taxa:

            tid, taxa, name = parse_taxa(taxa_line)

            if taxa == "species":
                species.append((name.strip(), tid))
            elif taxa == "subspecies":
                subspecies.append((name.strip(), tid))
            else:
                continue

    # Combine species and subspecies.
    all_species = species + subspecies

    all_species = set(all_species)

    return all_species


def write_missing(names):
    """
    Write taxon names with missing taxids to a file.
    """
    outfile = "missing.txt"
    out = open(outfile, "w")
    for n in names:
        out.write(n + "\n")


def print_taxids(stored):
    """
    Print taxids for each taxname.
    """
    for taxa, tid in stored.items():
        yield f"{taxa}\t{tid}"


def parse_names(fname, children=False, print_output=True):
    """
    Input file contains a list of scientific names.
    This code returns the taxid of the input name.
    If there are species or subspecies under the input in taxonomic lineage, it returns
    the taxids of those as well when --children is specified.
    """
    store = dict()
    missing = set()

    # Get taxids for all inputs
    res = get_taxid(fname).split("\n")

    # Go through each result and check if there are any missing.
    for r in res:

        try:
            taxa, tid = r.split("\t")
            taxa, tid = taxa.strip(), tid.strip()
            # special case with Bacteria
            if taxa == "Bacteria" and taxa in store and store[taxa] == '2':
                continue
            store[taxa] = tid if tid else missing.add(r)
        except:
            continue

    out = ""
    # Print missing names to "missing.txt"
    if missing:
        write_missing(missing)

    # Filter keys with none tids from store.
    filtered = {k: v for k, v in store.items() if v is not None}

    # If children is not specified, print taxids for inputs and exit.
    if not children:
        for line in print_taxids(filtered):
            yield line
        return

    # Get comma separated list of taxids.
    tids = ",".join(list(filtered.values()))

    # Get all species/subspecies under it.
    taxa_list = get_lower_taxa(tids).strip()

    # Write the species list
    species = get_species(taxa_list)

    # Print all species and subspecies if present else print taxid for the input name.
    if species:
        for s in species:
            # print("\t".join([s[0], s[1]]))
            yield "\t".join([s[0], s[1]])


@plac.pos('taxalist', "file listing taxa names")
@plac.flg('children', help="extract all species and sub-species under the taxa names")
def run(taxalist, children=False):
    for result in parse_names(taxalist, children):
        print(result)


if __name__ == "__main__":
    run()
