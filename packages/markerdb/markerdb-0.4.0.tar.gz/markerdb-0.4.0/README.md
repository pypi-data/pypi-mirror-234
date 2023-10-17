# DNA Marker Database for Metabarcoding

Accurate species identification relies on the marker sequence's resolution and the quality and comprehensiveness of the
reference library.

This repository contains a tool for creating a DNA marker database suitable for metabarcoding studies. The database can
be tailored to include various organisms, taxonomic groups, and specific marker sequences.

The tool employs sequence information from BLAST databases and NCBI's taxonomy to create the reference database. It is compatible with sequences conforming to NCBI's taxonomy standards and supports multiple markers such as COI,
COII, COIII, 12S, 16S, Cytb, and rbcL. Users can add additional markers by editing the synonyms file.

### How does it work?

The tool utilizes sequence titles from BLAST databases to identify marker sequences and uses a synonyms file to obtain
alternative names for these markers. The TaxonKit tool is used to fetch taxonomy details.

The different steps involved are

1. Creates a table with sequence attributes from blast databases.
2. Extracts species taxids for all species under each taxa specified in a taxalist file.
3. Parses the synonyms file and the sequence titles obtained in step1 to extract marker-specific details.
4. Gets fasta sequences for the marker accessions obtained in step3.
5. Creates sqlite3 database with marker sequence details.

The entire process typically takes ~45 minutes using NCBI's `nt` database.

### Quick start

**How to install the tool?**

Step1: Install script

    pip install markerdb --upgrade

Step2: Install additional requirements

    conda install --file conda-requirements.txt

The tool uses Taxonkit for fetching taxonomy details. See [here](https://bioinf.shenwei.me/taxonkit/usage/#before-use)
for the additional requirements before using the Taxonkit for the first time.

**How to run**

The command below uses NCBI's nucleotide blast databases (nt) to extract fish specific COI marker sequences.
`nt` databases should be in the BLASTDB variable.

    markerdb create -m COI -t taxa.txt -b nt -s synonyms.csv

The above command will create a sqlite3 database with all the markers specified in the synonyms file and also extracts `COI` specific sequences in a file named `COI_marker.fa`.

Once the `sqlite3` database is created use the command below to extract any taxa and marker subsets.

    markerdb extract -m 12S -t taxa.txt -d marker.db -o 12S_markers.fa

To test the tool, use the blast databases included here.

    markerdb create -m COI -t taxa.txt -b blastdb/demo -s synonyms.csv

**Inputs**

1. Marker name ( eg: COI)
2. Taxa list (eg: taxa.txt)
3. NCBI's nucleotide blast databases (nt)
4. Synonyms file (eg.synonyms.csv)

**1.Marker Name:** Specify the marker gene for which the sequences must be obtained. The specified gene and its
alternative names must be present in the synonyms file. To extract all markers listed in the synonyms file, use 'ALL'.

**2.Taxa list:** This is a list of taxonomic names for which marker gene sequences are extracted. The list can contain
names at the species level or higher taxonomic ranks. Marker genes for all species and subspecies within each taxon are
extracted. For instance, specifying 'Viridiplantae' will yield marker genes for all plants. An example taxa list file is

    Coelacanthimorpha
    Hyperoartia
    Hyperotreti
    Actinopterygii
    Dipnoi
    Chondrichthyes

**3.Blast databases:** Indicate the BLAST database from which to extract marker sequences. If the database is not in the
system path, provide its absolute path, including the prefix. For example /export/refs/nt/nt.

**4. Synonyms file:** A comma separated file with alternative names for the marker genes. This file is provided in
this repository. Users can edit the file to add additional markers.


**Outputs**

The main outputs are

1. A FASTA file containing the marker sequences
2. SQLite3 database file with all marker sequences specified in the synonyms file (marker.db).

Additional files including sequence details from BLAST databases, species list and taxids, and marker accession list are
also provided in a separate folder.

### Additional details

**Getting NCBI blast databases**

Users can use the `update_blastdb.pl` script from the BLAST suite to download the preformatted databases. For example to
download `nt` blast databases use the command

    update_blastdb.pl --decompress nt

**Using custom blast databases**

Users can also create custom blast databases for use in the workflow. The sequences must adhere to NCBI taxonomy. To create custom blast databases, use `makeblastdb` command
from the BLAST suite. A taxid-map file connecting the sequence ids to the NCBI taxid must be provided with
the `-taxid_map` option while creating the custom databases.

    makeblastdb -in seq.fa -out blastdb/seq -dbtype 'nucl' -taxid_map taxa_map.txt -parse_seqids

A taxid map file would look like this

    #
    # cat taxa_map.txt
    #
    A 217026
    B 335001
    C 990597
    D 990597

### Makefile workflow

The tool is also implemented as a Makefile workflow. To run the workflow use the command

    make create_db MARKER=COI TAXA=taxa.txt BLAST_DB=blastdb/demo SYNONYMS=synonyms.csv

To get details on the usage of the Makefile, run the command `make`.

    make

