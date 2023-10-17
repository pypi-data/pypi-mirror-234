import plac, sys, os

from mdbrun import taxids, table, db, fasta, details, create,extract

SUB_COMMANDS = {'taxids': taxids.run, 'table': table.run, 'db': db.run,
                'fasta': fasta.run, 'details': details.run, 'create': create.run, 'extract': extract.run,
                }

USAGE = f"""
   markerdb: create a taxa-specific DNA marker database \n

   markerdb create    : create sqlite3 database and marker specific fasta
   markerdb extract   : extract taxa specific marker  fasta from sqlite3 database
   markerdb db        : create sqlite3 database with marker details
   markerdb table     : convert blast databases to table
   markerdb taxids    : extract taxids for the taxalist

   
   Run each command for more help.
   """


def run():
    """Create a taxa-specific DNA marker database"""

    # Print usage when no parameters are passed.
    if len(sys.argv) == 1:
        print(USAGE)
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Enter a subcommand")
        sys.exit(1)

    cmd = sys.argv[1]

    sys.argv.remove(cmd)

    # Raise an error is not a valid subcommand.
    if cmd not in SUB_COMMANDS:
        print(USAGE, file=sys.stderr)
        print(f"invalid command: {cmd}")
        sys.exit(-1)

    func = SUB_COMMANDS[cmd]
    plac.call(func)


if __name__ == '__main__':
    run()
