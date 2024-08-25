# Assignment 1 - Reciprocal Best Hits 

data lives: 
```
/projects/bgmp/shared/Bi623/PS7_RBH_Bi623/H_to_zfishdb.blastp
/projects/bgmp/shared/Bi623/PS7_RBH_Bi623/Z_to_homodb.blastp
```

working directory : 
/projects/bgmp/calz/bioinfo/Bi623/Assignment_1

Goal pt 1: 
sort by seq id and then sort by evalue and output to a new file 

```
$ sort -n -k 1 /projects/bgmp/shared/Bi623/PS7_RBH_Bi623/Z_to_homodb.blastp | sort -n -k11 > ./Z_to_homodb_SORTED.blastp
$ sort -n -k 1 /projects/bgmp/shared/Bi623/PS7_RBH_Bi623/H_to_zfishdb.blastp | sort -n -k 11 > ./H-to_zfishdb_SORTED.blasp
```
#### Python script to grab best hits 
python script to: 
filter blastp results to retain only best hit(s) (lowest e score) for each protein ID:\
[best_hits.py](best_hit.py)

ok the file is written but the output isnt comparing to wes' so i think my og sorted files were done wrong
the sort piping i was doing was was overwriting the sort of collum 1 w column 11 so I have to combine them into the same 
sort 

https://stackoverflow.com/questions/41231186/sort-by-multiple-columns-in-bash

```
$ sort -k 1,1 -k11,11g /projects/bgmp/shared/Bi623/PS7_RBH_Bi623/Z_to_homodb.blastp > ./Z_to_homodb_SORTED.blastp
$ sort -k 1,1 -k11,11g /projects/bgmp/shared/Bi623/PS7_RBH_Bi623/H_to_zfishdb.blastp > ./H-to_zfishdb_SORTED.blastp
```
ok i think that should give me well sorted files so Im gunna rerun them:

```
$ ./best_hit.py -f H-to_zfishdb_SORTED.blastp -o H-to_zfishdb_BESTHIT.blastp
$ ./best_hit.py -f Z_to_homodb_SORTED.blastp -o Z_to_homodb_BESTHIT.blastp 
```

ok i think that worked!! 

### part 2 rbh script: 

remove duplicates: 
loop through the file 2x 
1) is the query id (feild 0) a duplicate? if yes add it to a set 
2) write any line that is NOT IN THE SET to a new file 

leaving you with only 1 entry of every query

python script : 
[RBH.py](RBH.py)

ok holy cow i think that script just worked first time! 

```
./RBH.py -f H-to_zfishdb_BESTHIT.blastp -o H-to_zfishdb_RBH.blastp
./RBH.py -f Z_to_homodb_BESTHIT.blastp -o Z_to_homodb_RBH.blastp
```

#### checking the output results
ok great so I know they made files how do i know it worked? 

H-to_zfish: 
how many repeating column 1 are there in the file? 
```
$ cut -f 1 H-to_zfishdb_RBH.blastp | uniq -d 
```
NONE YAY!

how about the original best hits file? 
```
02:56 PM calz Assignment_1 $ cut -f 1 H-to_zfishdb_BESTHIT.blastp | uniq -d | head
ENSP00000000233
ENSP00000001146
ENSP00000002165
ENSP00000002829
ENSP00000003084
ENSP00000004531
ENSP00000004982
ENSP00000005178
ENSP00000005226
```
a bunch! doesnt super matter how many i guess but it seems like it successfully eliminated the repeated gene IDS and created my new files 

### part 3 output TSV of all RBH relationships

**six columns**
1) Human Gene ID 
2) Human protein ID 
3) Human Gene Name
4) Zebrafish Gene ID
5) Zebrafish protein ID 
6) Zebrafish Gene name

just for file organization sake I'm moving all my old output files into this folder:\
[old_out](old_out)

copying in the tables: 
```
03:04 PM calz PS7_RBH_Bi623 $ cp *mart* /projects/bgmp/calz/bioinfo/Bi623/Assignment_1
```
ok now i just have to rememeber anything about these tables lol: 

```
$ head Human_mart_export_112.txt 
Gene stable ID  Protein stable ID       Gene name
ENSG00000210049         MT-TF
ENSG00000211459         MT-RNR1
ENSG00000210077         MT-TV
ENSG00000210082         MT-RNR2
ENSG00000209082         MT-TL1
ENSG00000198888 ENSP00000354687 MT-ND1
ENSG00000210100         MT-TI
ENSG00000210107         MT-TQ
ENSG00000210112         MT-TM
```

ok lets start scripting: 
[create_tsv.py](create_tsv.py)