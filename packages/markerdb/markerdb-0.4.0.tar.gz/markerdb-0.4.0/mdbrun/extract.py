#
# This script creates a sqlite3 database from an input table with the following columns
# 'accession','title','length','taxid','scientific_name','common_name','marker','genomic_location'
#
#  If a metadata file is specified, it


import sqlite3
import csv, os, plac, sys, uuid
from itertools import *


# LIMIT = 1000

def get_conn(dbname):
    """
    Creates database of name dbname
    """
    conn = ""
    try:
        conn = sqlite3.connect(dbname)
    except sqlite3.OperationalError:
        print(f"Database {dbname} not found.")

    return conn


def extract_sequences(marker, taxa, dbname, out=None):
    # Store species names
    with open(taxa, 'r') as f:
        species = [line.strip() for line in f.readlines()]

    # Output file
    if not out:
        out = f"{marker}_marker.fa"
    fo = open(out, "a")

    # Connect to database
    conn = get_conn(dbname)
    cursor = conn.cursor()

    for name in species:
        if marker == "ALL":
            cursor.execute(
                f"SELECT accession, seq FROM sequence WHERE taxid IN (SELECT distinct(taxid) from organism where scientific_name='{name}')")
        else:
            cursor.execute(
                f"SELECT accession, seq FROM sequence WHERE seq_marker='{marker}' AND taxid IN (SELECT distinct(taxid) from organism where scientific_name='{name}')")

        for row in cursor.fetchall():
            fo.write(f">{row[0]}\n{row[1]}\n")

    conn.close()


@plac.opt('marker', "Marker gene name, eg:COI")
@plac.opt('taxa', help="File listing taxa names")
@plac.opt('dbname', help="SQL database name")
@plac.opt('out', help="Output fasta filename ")
def run(marker, taxa, dbname, out=None):
    extract_sequences(marker, taxa, dbname, out)


if __name__ == "__main__":
    run()
