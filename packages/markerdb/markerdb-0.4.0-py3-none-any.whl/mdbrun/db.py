#
# This script creates a sqlite3 database from an input table with the following columns
# 'accession','title','length','taxid','scientific_name','common_name','marker','genomic_location'
#
#  If a metadata file is specified, it


import sqlite3
import csv, os, plac, sys, uuid
from itertools import *

# LIMIT = 1000

STATUS_CODE = dict(N="native", NN="non-native", SOC="species of concern",
                   E="endemic", I="introduced", R="reported", W="watchlist",
                   X="extinct")

REGION_CODE = {
    "North America": 2,
    "Great Lakes Basin": 3,
    "Planet Earth": 4,
}


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


def create_db(dbname):
    if os.path.isfile(dbname):
        os.remove(dbname)

    conn = get_conn(dbname)
    curs = conn.cursor()

    # create fish occurrence table
    #
    curs.execute('''CREATE TABLE organism
                    (taxid PRIMARY KEY,scientific_name,common_name)''')

    curs.execute('''CREATE TABLE metadata
                    (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , scientific_name, common_name, region,status, FOREIGN KEY (scientific_name) REFERENCES organism(scientific_name))''')

    curs.execute('''CREATE TABLE sequence
                    (accession PRIMARY KEY, accession_version, length, seq_marker,title, seq, genomic_location, taxid, FOREIGN KEY (taxid) REFERENCES organism(taxid) )''')

    # Save table within database (Save changes)
    conn.commit()
    # conn.close()
    # curs.close()


def parse_metadata_file(fname):
    data = []

    stream = csv.DictReader(open(fname), delimiter="\t")

    for row in stream:
        genus = row.get('Genus')
        species = row.get('Species')
        subspecies = row.get('Subspecies')
        common_name = row.get('Common name')
        status = row.get('Status')
        region = row.get('Region')

        d = {'genus': genus, 'species': species, 'subspecies': subspecies,
             'common_name': common_name, 'status': status, 'region': region}

        data.append(d)

    return data


def store_seq(fasta):
    store = dict()
    fh = open(fasta)
    acc, seq = "", ""
    for row in fh:
        if row.startswith('>'):
            if acc != "":
                store[acc] = seq
                seq = ""
            acc = row.split(' ')[0]
            acc = acc.split(".")[0]
            acc = acc.replace(">", "")

        else:
            seq += row.strip()
    return store


def get_status(term):
    return STATUS_CODE.get(term, term)


def get_region_code(region):
    return REGION_CODE.get(region, 0)


def make_rows(terms, common_name, scientific_name, region, curr_id):
    data = []
    for term in terms:
        status = get_status(term)
        # region_code = get_region_code(region)
        # curr_id = curr_id +1

        data.append((scientific_name, common_name, region, status,))
    return data


def load_metadata(dbname, data):
    conn = get_conn(dbname)
    curs = conn.cursor()

    curr_id = 0
    for index, row in enumerate(data):
        genus = row['genus']
        species = row['species']
        subspecies = row['subspecies']
        common_name = row['common_name']
        region = row['region']
        scientific_name = " ".join([genus, species]) if subspecies == "" else " ".join([genus, species, subspecies])
        terms = row['status'].split("/")

        # parse status column
        # if a species has multiple status (separated by '/'), then add that many rows into the table.
        #
        if len(terms) == 1:

            term = row['status']

            status_code = term
            status = get_status(status_code)
            # region_code = get_region_code(region)
            curr_id = curr_id + 1
            vals = (scientific_name, common_name, region, status,)
            curs.execute('INSERT INTO metadata (scientific_name, common_name, region,status) VALUES (?,?,?,?)', vals)
        else:

            vals = make_rows(terms=terms, common_name=common_name, scientific_name=scientific_name, region=region,
                             curr_id=curr_id)
            curs.executemany('INSERT INTO metadata (scientific_name, common_name, region,status) VALUES (?,?,?,?)',
                             vals)
            curr_id = curr_id + len(terms)

        conn.commit()

    print("Metadata table creation Done")

    # indexing

    sql_commands = [
        'CREATE INDEX metadata_scientific_name ON metadata(scientific_name )',
        'CREATE INDEX metadata_common_name ON metadata(common_name )',
        'CREATE INDEX metadata_region ON metadata(region )',
        'CREATE INDEX metadata_status ON metadata(status )',

    ]

    for sql in sql_commands:
        curs.execute(sql)

    print("Indexing done")
    curs.close()
    conn.close()
    return


def load_sequence(dbname, fname, fasta):
    conn = get_conn(dbname)
    curs = conn.cursor()

    stream = csv.DictReader(open(fname), delimiter="\t")
    info, seqs = dict(), list()

    for row in stream:
        acc_version = row['accession']
        acc = acc_version.split(".")[0]
        title = row.get('title')
        slen = row.get('length')
        taxid = row.get('taxid')
        sc_name = row.get('scientific_name')
        com_name = row.get('common_name')
        marker = row.get('marker')
        location = row.get('genomic_location')
        seq = fasta.get(acc, "")

        data = (acc, acc_version, slen, marker, title, seq, location, taxid)

        species_info = (taxid, sc_name, com_name)

        info[taxid] = species_info
        seqs.append(data)

        # curs.execute('INSERT INTO sequence VALUES (?,?,?,?,?,?,?)', data)
        # curs.execute('INSERT INTO organism VALUES (?,?,?)', species_info)

    # conn.commit()
    # print(" Sequence table creation done")

    # Create organism table
    for taxid, vals in info.items():
        # print(vals)
        curs.execute('INSERT INTO organism VALUES (?,?,?)', vals)
    print(" Organism table creation done")

    # Create sequence table
    for item in seqs:
        curs.execute('INSERT INTO sequence VALUES (?,?,?,?,?,?,?,?)', item)
    conn.commit()

    # Indexing

    sql_commands = [
        'CREATE INDEX sequence_taxid ON sequence(taxid)',
        'CREATE INDEX sequence_accession ON sequence(accession)',
        'CREATE INDEX sequence_accession_version ON sequence(accession_version)',
        'CREATE INDEX sequence_seq_marker ON sequence(seq_marker)',
        'CREATE INDEX sequence_genomic_location ON sequence(genomic_location)',
        'CREATE INDEX organism_taxid ON organism(taxid)',
        'CREATE INDEX organism_scientific_name ON organism(scientific_name)',
        'CREATE INDEX organism_common_name ON organism(common_name)',
    ]

    for sql in sql_commands:
        curs.execute(sql)

    print("Indexing done")
    curs.close()
    conn.close()

    return


def check_input(fname):
    """
    Checks if the input table contains the following columns
    accession,title,length,taxid,scientific_name,common_name,marker,genomic_location
    """
    cols = ['accession', 'title', 'length', 'taxid', 'scientific_name', 'common_name', 'marker', 'genomic_location']
    stream = csv.DictReader(open(fname), delimiter="\t")
    header = stream.fieldnames
    for c in cols:
        if c not in header:
            print(f"""Field(s) {c} not found in input file.\nColumns accession,title,length,taxid,scientific_name,\
common_name,marker,genomic_location must be present.\nExiting""")
            sys.exit()


@plac.pos('table', "tab-delimited file with marker details")
@plac.opt('dbname', help="SQL database name")
@plac.opt('seqs', help="Fasta file with marker sequences")
@plac.opt('metadata', help="tab-delimited metadata file")
def run(table, dbname='marker.db', seqs='marker.fa', metadata=None):
    check_input(table)
    # Create tmpdir for sqlite if the default has no space.
    TMPDIR = str(uuid.uuid4())
    os.mkdir(TMPDIR)
    os.environ['SQLITE_TMPDIR'] = TMPDIR
    create_db(dbname)

    if metadata:
        data = parse_metadata_file(metadata)
        load_metadata(dbname=dbname, data=data)

    seq_store = dict()
    if seqs:
        seq_store = store_seq(seqs)
    load_sequence(dbname=dbname, fname=table, fasta=seq_store)

    # Remove temporary directory
    os.rmdir(TMPDIR)
    return


if __name__ == "__main__":
    run()
