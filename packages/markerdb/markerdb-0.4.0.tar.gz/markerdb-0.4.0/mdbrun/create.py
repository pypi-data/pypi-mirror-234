# This script parses extracts taxa-specific marker sequence in fasta format from blast databases.
# Also, it creates an sqlite3 database with marker details.
# Required inputs are marker-name, taxalist, blast databases, synonyms file.
# Outputs are marker.fa and marker.db

import plac
from mdbrun import fasta, db, extract, taxids


@plac.opt('marker', help="Marker gene. Must be present in the synonyms file. 'ALL' for all markers.")
@plac.opt('taxalist', help="File listing taxa names")
@plac.opt('blastdb', "Path to blast databases including the prefix")
@plac.opt('synonyms', help="CSV file listing synonyms for marker genes. First name is the main identifier.")
@plac.opt('outfasta', help="Output marker fasta file.")
@plac.opt('dbname', help="SQL database name")
@plac.opt('metadata', help="tab-delimited metadata file", abbrev='f')
@plac.opt('intermediate', help="Folder with intermediate files.")
def run(marker, taxalist, blastdb='nt', synonyms="synonyms.csv", outfasta=None, dbname="marker.db",
        metadata=None, intermediate="misc"):
    # Create a master fasta file of ALL taxa-specific marker sequences.
    master_fasta = 'marker.fa'
    blast_table, species_tids, marker_table, acc_list, master_seqs = fasta.run('ALL', taxalist, blastdb, synonyms,
                                                                               master_fasta,
                                                                               intermediate)

    # Create sqlite3 database with marker sequence details.
    db.run(marker_table, dbname, master_seqs, metadata)

    # Get species names
    ft = open("species.txt", "w")
    for result in taxids.parse_names(taxalist, children=True):
        name, _ = result.split('\t')
        ft.write(f"{name}\n")
    ft.close()

    # Extract taxa specific marker sequences for each species
    extract.run(marker, "species.txt", dbname, out=outfasta)


if __name__ == "__main__":
    run()
