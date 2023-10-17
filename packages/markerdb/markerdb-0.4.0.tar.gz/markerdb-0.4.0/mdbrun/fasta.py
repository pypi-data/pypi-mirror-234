# This script parses extracts taxa-specific marker sequence in fasta format from blast databases.
# Required inputs are marker-name, taxalist, blast databases, synonyms file.


import plac, os, sys, csv, subprocess
from mdbrun import table, taxids, details


def create_folder(d):
    # Create the output folder if it doesn't exist
    if not os.path.exists(d):
        os.makedirs(d)
    return


def parse_synonyms(synonyms):
    store = list()
    stream = csv.reader(open(synonyms))
    for row in stream:
        store.append(row[0].upper())
    return store


def check_inputs(marker, taxalist, blastdb, synonyms):
    if marker == None:
        print()
        print(f" Marker is required.")
        print(f" Required inputs are  marker, taxalist, blastdb, synonyms.")
        print(f" Use -h to see all options.")
        print()
        sys.exit()

    mlist = parse_synonyms(synonyms)
    if marker != "ALL" and (marker != None and marker.upper() not in mlist):
        print(f"{marker} gene not found in synonyms file.")
        sys.exit()

    # Check if taxalist file is present
    if taxalist == None:
        print()
        print(f" Taxa list is required.")
        print(f" Required inputs are  marker, taxalist, blastdb, synonyms.")
        print(f" Use -h to see all options.")
        print()
        sys.exit()

    if not (taxalist or os.path.exists(taxalist)):
        print(f"Taxa list file is missing.")
        sys.exit()

    # Check if blast table file is present
    if not (os.path.exists(blastdb + ".nhr") or table.is_in_BLASTDB(blastdb)):
        print(f"Blast databases files are missing.Specify the path to blast databases along with the prefix.")
        sys.exit()

    # check synonyms file
    if not os.path.exists(synonyms):
        print(f"Synonyms file is not found")
        sys.exit()
    return


@plac.opt('marker', help="Marker gene. Must be present in the synonyms file. 'ALL' for all markers.")
@plac.opt('taxalist', help="File listing taxa names")
@plac.opt('blastdb', "Path to blast databases including the prefix")
@plac.opt('synonyms', help="CSV file listing synonyms for marker genes. First name is the main identifier.")
@plac.opt('outfasta', help="Output marker fasta file.")
@plac.opt('intermediate', help="Folder with intermediate files.")
def run(marker, taxalist, blastdb='nt', synonyms="synonyms.csv", outfasta="marker.fa", intermediate="misc"):
    # Check inputs
    check_inputs(marker, taxalist, blastdb, synonyms)

    # Create folder to store intermediate files.
    create_folder(intermediate)
    #
    # Step1 : Extract taxids for all species under each taxa in taxa list
    #
    taxa_fname = os.path.basename(taxalist)
    taxa_prefix, _ = os.path.splitext(taxa_fname)
    taxa_file = ".".join([taxa_prefix + "_tids", "txt"])
    taxa_file = os.path.join(intermediate, taxa_file)

    ft = open(taxa_file, "w")
    for result in taxids.parse_names(taxalist, children=True):
        ft.write(f"{result}\n")
    ft.close()
    #
    # Step2 : Extract sequence details from blast databases
    #
    # The columns in the resulting table are
    #  accession, title,sequence_length,taxid,scientific_name,common_name

    blast_table_prefix = os.path.basename(blastdb)
    blast_table = ".".join([blast_table_prefix, "txt"])
    blast_table = os.path.join(intermediate, blast_table)
    # Create table from blast databases.
    table.create_table(blastdb, out=blast_table)

    #
    # Step 3: Extract taxa-specific and marker-specific table.
    #
    marker_file = ".".join([taxa_prefix + "_marker_table", "txt"])
    marker_file = os.path.join(intermediate, marker_file)
    fm = open(marker_file, "w")
    for result in details.parse_nt_table(blast_table, taxa_file, marker, synonyms):
        fm.write(f"{result}\n")
    fm.close()

    #
    # Step 4 : Get marker-specific accession list
    #
    acc_file = ".".join([taxa_prefix + "_marker_acc", "txt"])
    acc_file = os.path.join(intermediate, acc_file)
    fa = open(acc_file, "w")
    stream = csv.DictReader(open(marker_file), delimiter="\t")
    for raw in stream:
        fa.write(f"{raw['accession']}\n")
    fa.close()

    #
    # Step 5 : Extract fasta sequences from accession
    blast_cmd = f"blastdbcmd -db {blastdb} -entry_batch {acc_file} > {outfasta}"
    subprocess.run(blast_cmd, shell=True)

    return blast_table, taxa_file, marker_file, acc_file, outfasta


if __name__ == "__main__":
    blast_table, taxa_file, marker_file, acc_file = run()
