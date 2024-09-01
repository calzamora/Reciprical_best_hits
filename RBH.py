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

print(human_file)
#create two dictionaries out of the TSV files:

#dictionary of human biomart table 
#key : protein id 
#value : gene id, gene name(TUPLE)

human_table_dict = {}

with open (human_table) as t:
    for line in t:
        spline = line.split() #split line to turn table into list  
        if len(spline) < 2: # removes entries that only have gene name and NO other info 
            pass
        #next case is if its = to 2 then we need to figure out if the gene hame or the proeinID id is missing 
        #do this by length -> the length is alwasy the same for the protein id adn gene id 
        if len(spline) == 2:
            if len(spline[1]) == 15: # human protein ID (in index pos 1) will alwasy equal 15 characters if the line contains the gene and protein id
                gene_ID = spline[0]
                protein_ID = spline[1]
                human_table_dict [protein_ID] = (gene_ID,"")
            elif len(spline[1]) != 15: #if it contains the gene_id and the gene name i dont care becasue I need the protein id
                pass
                # gene_name = spline[1]
                # protein_ID = spline[0]
                # human_table_dict [protein_ID] = ("",gene_name)
                # pass
        if len(spline) == 3: # 
            gene_ID = spline[0]
            protein_ID = spline[1]
            gene_name = spline[2]
            human_table_dict[protein_ID] = (gene_ID,gene_name)


# print(human_table_dict)
#dictionary of zfish biomart table 
#key : protein id 
#value : gene id, gene name(TUPLE)

zfish_table_dict = {}


with open (zfish_table) as t:
    for line in t:
        spline = line.split() #split line to turn table into list  
        if len(spline) < 2: # removes entries that only have gene name and NO other info 
            pass
        #next case is if its = to 2 then we need to figure out if the gene hame or the proeinID id is missing 
        #do this by length -> the length is alwasy the same for the protein id adn gene id 
        if len(spline) == 2:
            if len(spline[1]) == 18: # human protein ID (in index pos 1) will alwasy equal 15 characters if the line contains the gene and protein id
                gene_ID = spline[0]
                protein_ID = spline[1]
                zfish_table_dict [protein_ID] = (gene_ID,"")
            elif len(spline[1]) != 18: #if it contains the gene_id and the gene name i dont care becasue I need the protein id
                pass
                # gene_name = spline[1]
                # protein_ID = spline[0]
                # human_table_dict [protein_ID] = ("",gene_name)
                # pass
        if len(spline) == 3: # 
            gene_ID = spline[0]
            protein_ID = spline[1]
            gene_name = spline[2]
            zfish_table_dict[protein_ID] = (gene_ID,gene_name)

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
print(len(fish_dict))
print(fish_dict["ENSDARP00000096586"])
#print(fish_dict)


#using human protein id from H-to_zfishdb file pull relevent info 
i = 0
human_gene_id: str = ""
human_protein_ID: str = ""
human_gene_name: str = ""
fish_gene_id: str = ""
fish_protein_ID: str = ""
fish_gene_name: str = ""

import os

k= 0 
#i want to test if this check works:
with (open(human_file) as fh1,
    open(out_file, "w") as fh2):
    # print("working with file", os.getcwd(), human_file)
    fh2.write(f"Human Gene ID\tHuman Protein ID\tHuman Gene Name\tZfish Gene ID\tZfishProtein ID\tZfish Gene Name\n")
    for line in fh1:
        split_hit = line.split()
        Query_protein_ID = split_hit[0]
        Database_protein_ID = split_hit[1]
        if Database_protein_ID in fish_dict and fish_dict[Database_protein_ID] == Query_protein_ID:
            Human_Gene_ID = human_table_dict[Query_protein_ID][0]
            Human_Protein_ID = split_hit[0]
            Human_Gene_Name = human_table_dict[Query_protein_ID][1]
            Fish_Gene_ID = zfish_table_dict[Database_protein_ID][0]
            Fish_Protein_ID = split_hit[1]
            Fish_Gene_Name = zfish_table_dict[Database_protein_ID][1]
            k +=1
            fh2.write(f"{Human_Gene_ID}\t{Human_Protein_ID}\t{Human_Gene_Name}\t{Fish_Gene_ID}\t{Fish_Protein_ID}\t{Fish_Gene_Name}\n")

print(k)
print(Human_Gene_ID)
