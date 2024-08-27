#!/usr/bin/env python

#this script will take in : 
#H-to-z RBH
#Z-to -H RBH
#Human bmart table
#zfish bmart tabe

#and output: 
#TSV file w following columns: 
# 1) Human Gene ID 
# 2) Human protein ID 
# 3) Human Gene Name
# 4) Zebrafish Gene ID
# 5) Zebrafish protein ID 
# 6) Zebrafish Gene name

import argparse

def get_args():
    parser = argparse.ArgumentParser(description="create tsv file of RBH")
    parser.add_argument("-ht", help="human biomart table ", type = str) #type: str
    parser.add_argument("-hf", help="human RBF file ", type = str) #type: str
    parser.add_argument("-zt", help="zfish biomart table ", type = str) #type: str
    parser.add_argument("-zf", help="zfish RBF file ", type = str)
    parser.add_argument("-o", help="output tsv file name ") #type: str
    return parser.parse_args()

args = get_args()

human_table = args.ht
human_file = args.hf
zfish_table = args.zt
zfish_file = args.zf
out_file = args.o

#create two dictionaries out of the TSV files:

#dictionary of human biomart table 
#key : protein id 
#value : gene name, gene id (TUPLE)
#only store info that has a protein stable id

human_table_dict = {}

with open (human_table) as t:
    for line in t:
        spline = line.split() #split line to turn table into list 
        if len(spline) > 1: # removes entries that only have gene name and NO other info 
            if spline[1] != "": # if the protein stable ID exists: 
                prot_id = spline[1] #set key to protein stable ID 
                if len(spline) < 3: #if the gene name does NOT exist 
                    spline.append("") #append an empty string into index 2 so that every list is the same length 
                if prot_id not in human_table_dict:
                    human_table_dict[prot_id] = (spline[0],spline[2]) #set the velue equal to the tuple gene ID and Gene name 

#dictionary of zfish biomart table 
#key : protein id 
#value : gene name, gene id (TUPLE)
#only store info that has a protein stable id

zfish_table_dict = {}

with open (zfish_table) as t:
    for line in t:
        spline = line.split() #split line to turn table into list 
        if len(spline) > 1: # removes entries that only have gene name and NO other info 
            if spline[1] != "": # if the protein stable ID exists: 
                prot_id = spline[1] #set key to protein stable ID 
                if len(spline) < 3: #if the gene name does NOT exist 
                    spline.append("") #append an empty string into index 2 so that every list is the same length 
                if prot_id not in zfish_table_dict:
                    zfish_table_dict[prot_id] = (spline[0],spline[2]) #set the velue equal to the tuple gene ID and Gene name 

#create a dict w fish file 
#key = QUERY proteinID -> feild 0 fish protein 
#value = DB proteinID -> field 1 human protein 
fish_dict = {}

with open(zfish_file) as fh1:
    for line in fh1:
        split_hit = line.split()
        query = split_hit[0]
        db = split_hit[1]
        fish_dict[query] = db
print(f"length of fish dict {len(fish_dict)}")
# print(len(fish_dict))
#print(fish_dict)


#using human protein id from H-to_zfishdb file pull relevent info 
i = 0
human_gene_id: str = ""
human_protein_ID: str = ""
human_gene_name: str = ""
fish_gene_id: str = ""
fish_protein_ID: str = ""
fish_gene_name: str = ""

#i want to test if this check works:
j = 0
with open(human_file) as fh1:
    for line in fh1:
        split_hit = fh1.readline().split()
        value = split_hit[0]
        key = split_hit[1]
        if key in fish_dict and fish_dict[key] == value:
            j +=1
# print(len(fish_dict))
print(j)

with (open(human_file) as fh1,
      open(zfish_file) as fh2,
      open(out_file, "w") as out):
    while True:
        human_hit = fh1.readline()
        zfish_hit = fh2.readline()
        i += 1
        # print(human_hit)
        # print(zfish_hit)
        if human_hit == "":
            break
        # if i == 50:
        #     break
        #lets start pulling to info we need to print: 
        #pull all info from human file 
        split_human_hit = human_hit.split()
        split_zfish_hit = zfish_hit.split()
        human_protein_ID = split_human_hit[0]
        fish_protein_ID = split_zfish_hit[0]
        human_gene_id = human_table_dict[human_protein_ID][0]
        fish_gene_id = zfish_table_dict[fish_protein_ID][0]
        human_gene_name = human_table_dict[human_protein_ID][1]
        fish_gene_name = zfish_table_dict[fish_protein_ID][1]
        #if the fish protein id is in the dictionary and the human protein ID matches
        if fish_protein_ID in fish_dict and fish_dict[fish_protein_ID] == human_protein_ID:
            # for line in fh1:
            out.write(f"{human_gene_id}\t{human_protein_ID}\t{human_gene_name}\t{fish_gene_id}\t{fish_protein_ID}\t{fish_gene_name}\n")

        # print(human_protein_ID)
        # print(human_gene_id)
        # print(human_gene_name)
        # print("")
        # print(fish_protein_ID)
        # print(fish_gene_id)
        # print(fish_gene_name)
        # print(human_protein_ID)
        # print(zfish_protein_ID)
