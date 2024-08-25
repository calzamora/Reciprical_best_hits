#!/usr/bin/env python

#this script will inout a .blastp file in output format 6 and output a file with only the unique hits in that same format

import argparse

def get_args():
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument("-f", help="input file ", type = str) #type: str
    parser.add_argument("-o", help="output file name ", type = str) #type: str
    return parser.parse_args()

args = get_args()

file = args.f 
out = args.o

#List to hold repeats as i loop through - this will be converted into a set
repeat_hits = []
query_id: str = "this is not a query"
last_query: str = "this wasn't the last written"
#first loop though this file is just creating a SET of the non-unique query id (column 1)
with open(file) as fh1:
    while True: 
        hit = fh1.readline()
        if hit == "":
            break
        hit = hit.split() #split by white space 
        query_id = hit[0]
        if query_id == last_query: #if the query id is the same as the last seen, add it to the list 
            repeat_hits.append(query_id)
        elif query_id != last_query:
            pass
        #set this query = to last query for next run 
        last_query = query_id

#set of repeat gene id's
set_repeats = set(repeat_hits)

#next loop will only write to the out file if the query id IS NOT in the set 
with open (file) as fh1, open (out, "w") as fh2:
    while True: 
        hit = fh1.readline()
        if hit == "":
            break
        split_hit = hit.split() #split by white space 
        query_id = split_hit[0]
        if query_id not in set_repeats:
            fh2.write(hit)
        elif query_id in set_repeats:
            pass