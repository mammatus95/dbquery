import argparse
import sqlite3

parser = argparse.ArgumentParser(description="Query a database and print the content on the shell")
parser.add_argument("name", type=str, help="Database name")
parser.add_argument("--info", help="Info database", action="store_true")
parser.add_argument("--table", "-t", type=str, help="Table name")
parser.add_argument("--order", "-o", type=str, help="Ordered by column")
parser.add_argument("--select", "-s", type=str, help="Which column to print out")
#parser.add_argument("--where", "-w", type=str, help="Filter database")
#parser.add_argument("--whereval", "-ov", type=str, help="Filter by value?")

args = parser.parse_args()


con = sqlite3.connect(args.name)
cur = con.cursor()

if args.info:
    for row in cur.execute('SELECT sql FROM sqlite_schema ORDER BY tbl_name, type DESC, name'):
        print(row)
    exit(0)

if args.table:
    tablenames = args.table
else:
    for row in cur.execute('SELECT name FROM sqlite_schema WHERE type IN (\'table\',\'view\') AND name NOT LIKE \'sqlite_%\' ORDER BY 1'):
        tablenames =row[0]

if args.select:
    exe_str='SELECT ' + args.select + ' FROM ' + tablenames
else:
    exe_str='SELECT * FROM ' + tablenames
#if args.where and args.whereval:
#    exe_str+= " WHERE " + args.where+ " > " + args.whereval
if args.order:
    exe_str+= " ORDER BY " + args.order


print(" Command:" ,exe_str)
for row in cur.execute(exe_str):
    print(row)
print(" Command:" ,exe_str)
