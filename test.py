"""
Script to query basic information about a database.

Change log:
Author            Date
M. Kretschmer  26.02.2022      First implementation
M. Kretschmer  28.02.2022      First steps of visulation, and improvements of the info option

"""

import argparse
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Query a database and print the content on the shell")
parser.add_argument("name", type=str, help="Database name")
parser.add_argument("--info", help="Info database: Prints table names, column names and data typs and example data", action="store_true")
parser.add_argument("--table", "-t", type=str, help="Table name")
parser.add_argument("--order", "-o", type=str, help="Ordered by column")
parser.add_argument("--select", "-s", type=str, help="Which column to print out")
parser.add_argument("--number", "-n", type=str, help="Number of rows you want to print on terminal")
parser.add_argument("--visulation", "-v", type=str, help="Visualize one or meore columns of an existing table in the database.\n Example: type,lightnings")

#parser.add_argument("--where", "-w", type=str, help="Filter database")
#parser.add_argument("--whereval", "-ov", type=str, help="Filter by value?")

args = parser.parse_args()


con = sqlite3.connect(args.name)
cur = con.cursor()

if args.number:
    printrows_num=int(args.number)
else:
    printrows_num=5

if args.info:
    info_query=[]
    for row in cur.execute('SELECT sql FROM sqlite_schema ORDER BY tbl_name, type DESC, name'):

        #print("Create command:", row[0], "\n\n")
        info_query.append(row[0].replace("\n","").replace(")","").replace("(","").split())
    for info_str in info_query:
        tablenames = info_str[2]#[0].split(" ")[2]
        print("Table name: " + tablenames)
        rows_num = cur.execute("SELECT COUNT(*) FROM " + tablenames).fetchall()[0][0]
        print("number of rows: " + str(rows_num) + "\n\nContains Columns:")
        #print(len(info_str))
        #info_str[1] = info_str[1].replace("               (","")
        col = info_str[3:]#.split(", ")
        #print(col)
        print("Column name      ! datatyp\n--------------------------")
        head_str=" "
        for i in range(0,len(col)):
            print('{0: <16} !'.format(col[i]) + " " + col[1])
            head_str += '{0: <18} ! '. format(col[i])
            i+=1
        
        #print out example data with default select statement
        print("\nExample data of table " + tablenames)
        print(head_str)
        exe_str='SELECT * FROM ' + tablenames
        count=0

        for row in cur.execute(exe_str):
            row_content=""
            count+=1
            for i in row:
                row_content += '{0: <18} ! '.format(i)
            print(row_content)
            if count > printrows_num:
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



#terminal output!
print(" Command:", exe_str)
count=0
for row in cur.execute(exe_str):
    count+=1
    print(row)
    if count > printrows_num:
        break

#visulation
if args.visulation:
    visulation = args.visulation.replace(" ", ",")
    col_num = len(visulation.split(","))
    rows_num = rows_num = cur.execute("SELECT COUNT(*) FROM " + tablenames).fetchall()[0][0]
    content_array = np.zeros((col_num,rows_num))
    #print(content_array.shape)
    exe_str='SELECT ' + visulation + ' FROM ' + tablenames
    i=0
    for row in cur.execute(exe_str):
        content_array[0,i] = row[0]
        content_array[1,i] = row[1]
        i+=1
    #print(content_array[1,2])
    num_bins = 50
    for j in range(0,col_num):
        fig, ax = plt.subplots()
        ax.set_title(tablenames + " by " + visulation.split(",")[j])
        n, bins, patches = ax.hist(content_array[j,:], num_bins, density=True)
        ax.set_xlabel(visulation.split(",")[j])
        ax.set_ylabel('Probability density')
        plt.savefig(visulation.split(",")[j] + ".png")
        plt.close()
