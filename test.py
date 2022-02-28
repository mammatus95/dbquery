import argparse
import sqlite3

parser = argparse.ArgumentParser(description="Query a database and print the content on the shell")
parser.add_argument("name", type=str, help="Database name")
parser.add_argument("--info", help="Info database: Prints table names, column names and data typs and example data", action="store_true")
parser.add_argument("--table", "-t", type=str, help="Table name")
parser.add_argument("--order", "-o", type=str, help="Ordered by column")
parser.add_argument("--select", "-s", type=str, help="Which column to print out")
parser.add_argument("--visulation", "-v", type=str, help="Visualize one or meore columns of an existing table in the database.\n Example: type lightnings")

#parser.add_argument("--where", "-w", type=str, help="Filter database")
#parser.add_argument("--whereval", "-ov", type=str, help="Filter by value?")

args = parser.parse_args()


con = sqlite3.connect(args.name)
cur = con.cursor()

if args.info:
    info_query=[]
    for row in cur.execute('SELECT sql FROM sqlite_schema ORDER BY tbl_name, type DESC, name'):
        #print(type(row[0]))
        info_query.append(row[0].split("\n"))
    for info_str in info_query:
        tablenames = info_str[0].split(" ")[2]
        print("Table name: " + tablenames + "\n\nContains Columns:")
        info_str[1] = info_str[1].replace("               (","")
        col = info_str[1].split(", ")
        print("Column name      ! datatyp\n--------------------------")
        head_str=" "
        for i in col:
            print('{0: <16} !'.format(i.split(" ")[0]) + " " + i.split(" ")[1].replace(")",""))
            head_str += '{0: <18} ! '. format(i.split(" ")[0])
        
        #print out example data with default select statement
        print("\nExample data of table " + tablenames)
        print(head_str)
        exe_str='SELECT * FROM ' + tablenames
        count=0
        rows_example=5
        for row in cur.execute(exe_str):
            row_content=""
            count+=1
            for i in row:
                row_content += '{0: <18} ! '.format(i)
            print(row_content)
            if count > rows_example:
                break
        print("\n\n")
    exit(0)

if args.table:
    tablenames = args.table
else:
    for row in cur.execute('SELECT name FROM sqlite_schema WHERE type IN (\'table\',\'view\') AND name NOT LIKE \'sqlite_%\' ORDER BY 1'):
        tablenames = row[0]
#select
if args.select:
    exe_str='SELECT ' + args.select + ' FROM ' + tablenames
else:
    exe_str='SELECT * FROM ' + tablenames
#where
#if args.where and args.whereval:
#    exe_str+= " WHERE " + args.where+ " > " + args.whereval
if args.order:
    exe_str+= " ORDER BY " + args.order


print(" Command:", exe_str)
for row in cur.execute(exe_str):
    print(row)
print(" Command:", exe_str)


