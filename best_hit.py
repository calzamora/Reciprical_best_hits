#!/usr/bin/env python

#This script will take in a blasrp file in format 6 and output a new blastp file in the same format 
#but retain only the best hit(s) for each protein query 

import argparse

def get_args():
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument("-f", help="input file ", type = str) #type: str
    parser.add_argument("-o", help="output file name ", type = str) #type: str
    return parser.parse_args()

args = get_args()

file = args.f 
out = args.o


with open (file) as fh1, open (out, "w") as fh2: 
    last_written: str = "this is not a hit"
    last_escore: str = "this is not an escore"
    #read the file line by line
    while True: 
        line = fh1.readline()
        if line == "":
            break
        hit = line.split() #splits hit by tab 
        #if the line is a new protein id then write and reassign the last written variables
        if hit[0] != last_written:
            fh2.write(line)
            last_written = hit[0]
            last_escore = hit[10]
        #if the protein id was already see, only write if the e score is equal to the last
        #i dont have to worry abt overwriting cause the files are already sorted in accending order 
        elif hit[10] == last_escore:
            fh2.write(line)
            last_written = hit[0]
            last_escore = hit[10]
        else:
            pass
# print(last_written)
# print(last_escore)

